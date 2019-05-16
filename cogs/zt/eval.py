import os
import json
import pytz
import asyncio
import discord
import textwrap
import datetime
import requests
from discord.ext import commands
from discord.ext.commands import Cog

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

class Eval(Cog):
    def __init__(self, zt):
        self.zt = zt
    
    @Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 498011182620475412 and member.created_at > datetime.datetime(year=2019, month=2, day=1) and not member.bot:
            cat = member.created_at.replace(tzinfo=pytz.utc).astimezone(tz=pytz.timezone('America/Sao_Paulo')).strftime('`%d/%m/%Y %H:%M`')
            embed = discord.Embed(color=color(self.zt), description=f'**{member.mention} `{member.id}` entrou no servidor, com a conta criada em {cat}**') \
            .set_footer(text='Horário de Brasília.')
            embed.set_thumbnail(url=member.avatar_url)
            await self.zt.get_channel(548613630040473601).send(embed=embed)


    @commands.command(name='eval', aliases=['evl', 'debug'])
    async def eval_(self, ctx, *, evl: str=None):
        if not ctx.author.id in self.zt.config('ownerID'):
            return
        if 'await ' in evl:
            try:
                a = await eval(evl.replace('await ', ''))
            except Exception as e:
                a = e
            embed = discord.Embed(color=color(self.zt)) \
            .add_field(name='Input:', value=f'```py\n{evl}```') \
            .add_field(name='Output:', value=f'```\n{a}```')
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException:
                pass
        else:
            try:
                a = eval(evl)
            except Exception as e:
                a = e
            embed = discord.Embed(color=color(self.zt)) \
            .add_field(name=f'<{self.zt.emoji("Download")}> Input:', value=f'```py\n{evl}```') \
            .add_field(name=f'<{self.zt.emoji("Upload")}> Output:', value=f'```\n{a}```')
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException:
                pass
    '''@commands.command(aliases=['dg'])
    async def debug(self, ctx, *, evl):
        if not ctx.author.id in self.zt.config('ownerID'):
            return
        if evl.startswith('\n'):
            evl = evl[1:]
        if evl.startswith('```') and evl.endswith('```'):
            if evl.startswith('```py'):
                evl = evl[5:]
            else:
                evl = evl[3:]
            evl = evl[:len(evl)-3]'''

    @commands.command(name='testecooldown')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def teste(self, ctx):
        pass #a = 1/0
    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(aliases=['clear'])
    @commands.has_permissions(administrator=True)
    async def limpar(self, ctx, *, limit: int=100):
        try:
            limit += 1
            await ctx.channel.purge(limit=limit)
            
            #with open(f'{ctx.channel.id}.log', 'w+') as tmpfile:
                #for message in log[::-1]:
                    #tmpfile.write(f'\n [{message.created_at.strftime("%d/%m/%Y %H:%M")}] {message.author}({message.author.id}) | {message.content}')
            #await ctx.send(file=discord.File(f'{ctx.channel.id}.log', filename=f'clean.log'))
            #os.remove(f'{ctx.channel.id}.log')
        except Exception as e:
            await ctx.send(e)
    
    @commands.command()
    async def request(self, ctx, *, url):
        if not ctx.author.id in self.zt.config('ownerID'):
            return
        try:
            for jsonf in textwrap.TextWrapper(width=1991, drop_whitespace=False, placeholder='', replace_whitespace=False).wrap(json.dumps(json.loads(requests.get(url).text), indent=4)):
                await ctx.send('```json\n' + jsonf + '```')
                await asyncio.sleep(0.2)
        except Exception as e:
            await ctx.send(e)
            await asyncio.sleep(0.2)
        

    
def setup(zt):
    zt.add_cog(Eval(zt))

