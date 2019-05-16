import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get

class welcome(Cog):
    def __init__(self,zt):
        zt.self = zt
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command(name='set-bv',aliases=['welcome-setup','setup-bv','welcome'])
    async def bemvindo(self,ctx,*,channelid:int=None):
        if channelid is None: await ctx.send("Digite Um ID de canal")
        else:
            with open('welcome.json') as wel:
                wel.write(dict(f'{get(guild.id)}'))
            
def setup(zt):
    zt.add_cog(welcome(zt))
