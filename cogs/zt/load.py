import json
import discord
from discord.ext import commands
from discord.ext.commands import Cog

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

class Extload(Cog):
    def __init__(self, zt):
        self.zt = zt

    @commands.command(name='load', aliases=['carregar', 'ld'])
    async def load_(self, ctx, *, ext: str=''):
        ext = 'cogs.' + ext
        if not ctx.author.id in self.zt.config('ownerID'):
            return #mensaginha de proibido ne thomas
        try:
            self.zt.load_extension(ext)
            await ctx.send(embed=discord.Embed(color=color(self.zt), description=f'<{self.zt.emoji("carregando")}> **| Extensão `{ext[5:]}` carregada com sucesso.**'))
        except Exception as Error:
            await ctx.send(embed=discord.Embed(description=str(Error), color=color(self.zt)))
    @commands.command(name='unload', aliases=['descarregar', 'ul'])
    async def unload_(self, ctx, *, ext: str=''):
        ext = 'cogs.' + ext
        if not ctx.author.id in self.zt.config('ownerID'):
            return #mensaginha de proibido ne thomas
        try:
            self.zt.unload_extension(ext)
            await ctx.send(embed=discord.Embed(color=color(self.zt), description=f'<{self.zt.emoji("carregando")}> **| Extensão `{ext[5:]}` descarregada com sucesso.**'))
        except Exception as Error:
            await ctx.send(embed=discord.Embed(description=str(Error), color=color(self.zt)))
    @commands.command(name='reload', aliases=['recarregar', 'rld'])
    async def reload_(self, ctx, *, ext: str=''):
        ext = 'cogs.' + ext
        if not ctx.author.id in self.zt.config('ownerID'):
            return #mensaginha de proibido ne thomas
        try:
            self.zt.unload_extension(ext)
            self.zt.load_extension(ext)
            await ctx.send(embed=discord.Embed(color=color(self.zt), description=f'<{self.zt.emoji("carregando")}> **| Extensão `{ext[5:]}` recarregada com sucesso.**'))
        except Exception as Error:
            await ctx.send(embed=discord.Embed(description=str(Error), color=color(self.zt)))
    @commands.command(name='makeemojilist')
    async def list1(self, ctx):
        if not ctx.author.id in self.zt.config('ownerID'): return
        emojis = {}
        for guild in self.zt.config('emojiGuilds'):
            for emoji in self.zt.get_guild(guild).emojis:
                emojis[emoji.name] = str(emoji).strip('<>')
        with open('./data/config/emojis.json', 'w+') as jsonf:
            json.dump(emojis, jsonf)
        await ctx.send('Done!')
    
def setup(zt):
    zt.add_cog(Extload(zt))