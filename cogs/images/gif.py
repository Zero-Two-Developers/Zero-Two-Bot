import discord
from discord.ext import commands
from random import randrange
import requests
import json
from cogs.core import utils
import naegin
from discord.ext.commands import Cog

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

def giphy_api(tag):
    url = 'http://api.giphy.com/v1/gifs/search?q={}&api_key=&limit=16'.format(tag)
    resposta = requests.get(url)
    resposta_json = json.loads(resposta.text)
    gif = resposta_json['data'][randrange(0, 15)]['id']
    return 'https://media.giphy.com/media/{}/giphy.gif'.format(gif)

class gif(Cog):
    def __init__(self, zt):
        self.zt = zt
        self.naegin = naegin.Client(zt.config('keys')['naeginApi'])
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='gif')
    async def gif_(self, ctx,*,arg):
        lang = self.zt.lang(ctx, "gif")
        try:                
            tag = arg
            resultado = giphy_api(tag)
            embed_gif = discord.Embed(color=color(self.zt))
            embed_gif.set_image(url=resultado)
            embed_gif.set_footer(text=self.zt.user.name, icon_url=self.zt.user.avatar_url)
            await ctx.send(embed=embed_gif)
            await ctx.message.delete()

        except:
            await ctx.send(lang["gif"][0])
    
    
    @commands.group()
    async def rimg(self, ctx):
        lang = self.zt.lang(ctx, "gif")
        if ctx.invoked_subcommand is None:
            shibe = json.loads(requests.get('http://shibe.online/api/shibes').text)
            embed = discord.Embed(description=lang["img"][0],color=color(self.zt))
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @rimg.command()
    async def shibe(self, ctx):
        shibe = json.loads(requests.get('http://shibe.online/api/shibes').text)
        embed = discord.Embed(color=color(self.zt)) \
        .set_image(url=shibe[0])
        await ctx.send(embed=embed)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @rimg.command()
    async def cat(self, ctx):
        shibe = json.loads(requests.get('http://shibe.online/api/cats').text)
        embed = discord.Embed(color=color(self.zt)) \
        .set_image(url=shibe[0])
        await ctx.send(embed=embed)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @rimg.command()
    async def bird(self, ctx):
        shibe = json.loads(requests.get('http://shibe.online/api/birds').text)
        embed = discord.Embed(color=color(self.zt)) \
        .set_image(url=shibe[0])
        await ctx.send(embed=embed)
    @commands.command()
    @commands.guild_only()
    async def img(self, ctx, *, tag: str=None):
        embed = utils.baseEmbed()
        if tag is None:
            embed.description = f'<{self.zt.emoji("Error")}> **| Você não especificou uma tag. Use `zt.img tags`.**'
            return await ctx.send(embed=embed)
        tag = tag.lower()
        if tag == 'tags' or tag == 'tag':
            embed.description = ('**' + ' - '.join([f'`{tag}`' for tag in await self.naegin.get_all_tags()]) + '**').title()
            return await ctx.send(embed=embed)
        if not tag in (await self.naegin.get_all_tags()):
            embed.description = f'<{self.zt.emoji("Error")}> **| Insira uma tag válida. Use `zt.img tags`.**'
            return await ctx.send(embed=embed)
        img = await self.naegin.get_random(tag)
        if not ctx.channel.nsfw and img.nsfw:
            embed.description = f'<{self.zt.emoji("Error")}> **| Só posso enviar isso em canais nsfw.**'
            return await ctx.send(embed=embed)
        embed.set_image(url=img.url)
        await ctx.send(embed=embed)
def setup(zt):
    zt.add_cog(gif(zt))