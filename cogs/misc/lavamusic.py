import os
import re
import math
import asyncio
import discord
import lavalink

from lavalink.events import *
from cogs.core import utils
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, zt):
        self.zt = zt

        if not hasattr(zt, 'lavalink'):
            zt.lavalink = lavalink.Client(zt.config('botInfo')['userID'])
            zt.lavalink.add_node('127.0.0.1', 2333, 'youshallnotpass', 'eu', 'default-node')
            zt.add_listener(zt.lavalink.voice_update_handler, 'on_socket_response')

        zt.lavalink.add_event_hook(self.track_hook)

    async def cog_unload(self):
        self.zt.lavalink._event_hooks.clear()

    async def track_hook(self, event):
        embed = utils.baseEmbed()

        if isinstance(event, TrackStartEvent):
            pass

        elif isinstance(event, TrackEndEvent):
            pass

        elif isinstance(event, QueueEndEvent):
            pass

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None

        if guild_check: 
            await self.ensure_voice(ctx)

        return guild_check 

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.zt._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        else:
            await ctx.send(error)
            #raise error
    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        player = self.zt.lavalink.players.get(ctx.guild.id)

        query = query.strip('<>')

        if not query.startswith('scsearch:') and not query.startswith('ytsearch:') and not re.compile('https?:\\/\\/(?:www\\.)?.+').match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        embed = utils.baseEmbed()

        if not results or not results['tracks']:
            embed.description = f'<{self.zt.emoji("Error")}> **| Não foi encontrado nada com esses termos.**'
            return await ctx.send(embed=embed)


        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.description = f'**<{self.zt.emoji("Verificado")}> | Playlist `{results["playlistInfo"]["name"]}` adicionada a queue.**'
            await ctx.send(embed=embed)
        else:
            track = results['tracks'][0]
            embed.description = f'**<{self.zt.emoji("Verificado")}> | [{track["info"]["title"]}]({track["info"]["uri"]}) adicionada a queue.**'
            await ctx.send(embed=embed)
            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['posição'])
    async def seek(self, ctx, *, time: str=''):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        seconds = re.compile('[0-9]+').search(time)
        if time == '' or not seconds:
            embed.description = f'<{self.zt.emoji("Error")}> **| Você precisa especificar o tempo para alterar a posição.**'
            return await ctx.send(embed=embed)

        seconds = int(seconds.group()) * 1000
        if time.startswith('-'):
            seconds *= -1

        track_time = player.position + seconds
        await player.seek(track_time)
        
        embed.description = f'**<{self.zt.emoji("Verificado")}> | Posição alterada para `{lavalink.utils.format_time(track_time)}`.**'
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['forceskip', 'pular'])
    async def skip(self, ctx, *, num: int=None):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            embed.description = f'<{self.zt.emoji("Error")}> **| Eu não estou tocando.**'   
            return await ctx.send(embed=embed)
        if num is None:
            await player.skip()
            embed.description = f'<{self.zt.emoji("Verificado")}> **| Música pulada.**'
            return await ctx.send(embed=embed)
        if num > len(player.queue) or num <0:
            embed.description = f'<{self.zt.emoji("Error")}> **| Digite um número valido.**'
            return await ctx.send(embed=embed)
        index = 0 
        while index < num:
            await player.skip()
            index += 1
        embed.description = f'<{self.zt.emoji("Verificado")}> **| {num} músicas puladas.**'
        await ctx.send(embed=embed)
            

    @commands.command(aliases=['parar'])
    async def stop(self, ctx):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            embed.description = f'**<{self.zt.emoji("Error")}> | Eu não estou tocando.**'
            return await ctx.send(embed=embed)

        player.queue.clear()
        await player.stop()
        embed.description = f'**<{self.zt.emoji("Verificado")}> | Player parado com sucesso.**'
        await ctx.send(embed=embed)

    @commands.command(aliases=['np', 'n', 'playing', 'agora'])
    async def now(self, ctx):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        if not player.current:
            embed.description = f'<{self.zt.emoji("Error")}> **| Eu não estou tocando.**'
            return await ctx.send(embed=embed)

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = 'Ao vivo'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'


        embed.description = song
        await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int = 1):
        raise commands.CommandNotFound()
        '''
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            embed.description = f'{self.zt.emoji("Error")} **| Minha queue está vazia.'
            return await ctx.send('Nothing queued.')

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=discord.Color.blurple(),
                            description=f'**{len(player.queue)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=embed)'''

    @commands.command(aliases=['resume', 'retomar', 'despausar', 'pausar', 'despausa', 'pausa'])
    async def pause(self, ctx):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            embed.description = f'<{self.zt.emoji("Error")}> **| Eu não estou tocando.**'
            return await ctx.send(embed=embed)

        if player.paused:
            await player.set_pause(False)
            await ctx.send(f'<{self.zt.emoji("Verificado")}> **| Música retomada com sucesso.**')
        else:
            await player.set_pause(True)
            await ctx.send(f'<{self.zt.emoji("Verificado")}> **| Música pausada com sucesso.**')

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int = None):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        if not volume:
            embed.description = f'**<{self.zt.emoji("Speaker")}> |{player.volume}%**'
            return await ctx.send(embed=embed)

        await player.set_volume(volume)
        await ctx.send(f'**<{self.zt.emoji("Speaker")}> | Volume alterado para {player.volume}%.**')

    @commands.command(aliases=['misturar'])
    async def shuffle(self, ctx):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)
        if not player.is_playing:
            embed.description = f'<{self.zt.emoji("Error")}> **| Eu não estou tocando.**'
            return await ctx.send(embed=embed)

        player.shuffle = not player.shuffle
        embed.description = f'**<{self.zt.emoji("Verificado")}> | Shuffle ' + ('ativado' if player.shuffle else 'desativado') + ' com sucesso.**'
        await ctx.send(embed=embed)

    @commands.command(aliases=['loop', 'repetir'])
    async def repeat(self, ctx):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            embed.description = f'<{self.zt.emoji("Error")}> **| Eu não estou tocando.**'
            return await ctx.send(embed=embed)

        player.repeat = not player.repeat
        embed.description = embed.description = f'**<{self.zt.emoji("Verificado")}> | Repetir ' + ('ativado' if player.repeat else 'desativado') + ' com sucesso.**'
        await ctx.send(embed=embed)

    @commands.command(aliases=['remover', 'rm'])
    async def remove(self, ctx, index: int):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            embed.description = f'<{self.zt.emoji("Error")}> **| Minha queue está vazia.**'
            return await ctx.send(embed=embed)

        if index > len(player.queue) or index < 1:
            embed.description = f'<{self.zt.emoji("Error")}> **| O número deve ser entre 1 e {len(player.queue)}.**'
            return await ctx.send(embed=embed)

        index -= 1
        removed = player.queue.pop(index)

        embed.description = f'<{self.zt.emoji("Verificado")}> **| [{removed.title}]({removed.uri}) removida da queue com sucesso.**'
        await ctx.send(embed=embed)

    @commands.command(aliases=['procurar'])
    async def find(self, ctx, *, query):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            embed.description = f'{self.zt.emoji("Error")}** | Não foi encontrado nada com esses termos.**'
            return await ctx.send(embed=embed)

        tracks = results['tracks'][:9] 

        embed.description = '**'
        for index, track in enumerate(tracks, start=1):
            track_title = track['info']['title']
            track_uri = track['info']['uri']
            embed.description += f'<{self.zt.emoji(f"{index}_")}> [{track_title}]({track_uri})\n\n'
        
        embed.description += '**'

        r = await ctx.send(embed=embed)
        for emoji in list(range(1, len(tracks)+1)):
            await r.add_reaction(self.zt.emoji(f"{emoji}_"))
            await asyncio.sleep(0.2)

    @commands.command(aliases=['dc', 'leave', 'sair', 'desconectar', 'quit'])
    async def disconnect(self, ctx):
        embed = utils.baseEmbed()

        player = self.zt.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            embed.description = f'<{self.zt.emoji("Error")}> **| Eu não estou conectado.**'
            return await ctx.send(embed=embed)

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        embed.description = f'<{self.zt.emoji("Verificado")}> **| Desconectado com sucesso.**'
        await ctx.send(embed=embed)

    @commands.command(aliases=['conectar', 'join', 'entrar'])
    async def connect(self, ctx, *, channel):
        pass

    @commands.command(aliases=['bass', 'boost', 'bass_boost'])
    async def bassboost(self, ctx, band: int, gain:float):
        player = self.zt.lavalink.players.get(ctx.guild.id)        
        await player.set_gain(band, gain)
        await ctx.send('ok')
        
        

    async def ensure_voice(self, ctx):
        embed = utils.baseEmbed()
        player = self.zt.lavalink.players.create(ctx.guild.id, endpoint=ctx.guild.region.value)

        should_connect = ctx.command.name in ('play', 'connect')
        if ctx.guild.id == 498011182620475412 and not 529365459397509130 in [role.id for role in ctx.author.roles]:
            raise commands.CheckFailure()
        if not ctx.author.voice or not ctx.author.voice.channel:
            embed.description = f'<{self.zt.emoji("Error")}> **| Você precisa estar em um canal de voz.**'
            await ctx.send(embed=embed)
            raise commands.CheckFailure()

        if not player.is_connected:
            if not should_connect:
                embed.description = f'<{self.zt.emoji("Error")}> **| Não estou conectada.**'
                await ctx.send(embed=embed)
                raise commands.CheckFailure()

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                embed.description = f'<{self.zt.emoji("Error")}> **| Você precisa estar no meu canal de voz.**'
                await ctx.send(embed=embed)
                raise commands.CheckFailure()


def setup(zt):
    zt.add_cog(Music(zt))