import discord
from discord.ext import commands
import asyncio
import requests
import logging
import cassiopeia as cass
import traceback
from cogs.core import utils
from discord.ext.commands import Cog

class lol(Cog):
    def __init__(self, zt):
        self.zt = zt
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(pass_context = True)
    async def lol(self,ctx):
        def check3(m):
            return m.content and m.author == ctx.author
        embed = utils.baseEmbed()
        embed.description = self.zt.lang(ctx, "Lol")["Embed2"][0]
        embed.timestamp = ctx.message.created_at
        a = await ctx.send(embed=embed)
        await ctx.message.delete()
        try:
            msg = await self.zt.wait_for('message', check=check3, timeout=180)
            region = msg.content
            cass.set_default_region(region)
            embed1 = utils.baseEmbed()
            embed1.description = self.zt.lang(ctx, "Lol")["Embed2"][1]
            embed1.timestamp = ctx.message.created_at
            await a.edit(embed=embed1)
            try:
                await msg.delete()
            except:
                pass
            msg2 = await self.zt.wait_for('message', check=check3, timeout=180)
            nickname= msg2.content
            summoner = cass.get_summoner(name=nickname)
            try:
                await msg2.delete()
            except:
                pass
            await a.delete() 
            champ = " "
            try:
                for mastery in summoner.champion_masteries[:5]:
                    champ += ("**• {}:** ``{}``\n".format(mastery.champion.name, mastery.points).replace(" ",""))
            except:
                pass
            embed2 = utils.baseEmbed()
            embed2.description = "**Perfil de "+summoner.name+"**"
            embed2.timestamp = ctx.message.created_at
            embed2.set_thumbnail(url=summoner.profile_icon.url)
            embed2.add_field(name=self.zt.lang(ctx, "Lol")["Embed"][0],value=f'**{summoner.name}**',inline=False)
            embed2.add_field(name=self.zt.lang(ctx, "Lol")["Embed"][1],value=f'**{summoner.level}**',inline=False)
            try:
                embed2.add_field(name=self.zt.lang(ctx, "Lol")["Embed"][2],value=f'**{summoner.rank_last_season}**',inline=False)
            except:
                pass
            try:
                embed2.add_field(name=self.zt.lang(ctx, "Lol")["Embed"][3],value=(f'\n{champ}').replace("[","").replace("'","").replace("]","").replace(",","\n").replace('"',''),inline=False)
            except:
                pass
            await ctx.send(embed=embed2)
        except Exception as e:
            embed3 = utils.baseEmbed()
            embed3.description = f'<{self.zt.emoji("Error")}> **| {self.zt.lang(ctx, "Lol")["Embed"][4]}**'

            await ctx.send(embed=embed3)
            #traceback.print_exception(Exception, e, None)


def setup(zt):
    zt.add_cog(lol(zt))
    cass.set_riot_api_key(zt.config('keys')['lolApi'])
    cass.print_calls(False)