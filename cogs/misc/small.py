import discord
from discord.ext import commands
from cogs.core.utils import baseEmbed

class Small(commands.Cog):
    def __init__(self, zt):
        self.zt = zt
    
    @commands.command(name='ping')
    async def ping_(self, ctx):
        embed = baseEmbed()
        embed.description = f'**<{self.zt.emoji("Signal")}> | {"%.0f" % (self.zt.latencies[ctx.guild.shard_id][1]*1000)}ms**'
        await ctx.send(embed=embed)


def setup(zt):
    zt.add_cog(Small(zt))