import discord
import datetime
import asyncio
from discord.ext import commands
from discord.ext.commands import Cog

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

class Config(Cog):
    def __init__(self, zt):
        self.zt = zt
    @commands.command(name='config', aliases=['cfg'])
    @commands.guild_only()
    async def config_(self, ctx):
        if not ctx.author.id in self.zt.config('ownerID'):
            raise commands.CommandNotFound()
        try:
            embed = discord.Embed(color=color(self.zt), timestamp=datetime.datetime.utcnow()) \
            .set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url) \
            .add_field(name=f'<{self.zt.emoji("Logs")}> - conf. logs', value='\u200b', inline=False) \
            .add_field(name=f'<{self.zt.emoji("MembershipCard")}> - conf. cargos', value='\u200b', inline=False) \
            .add_field(name=f'<{self.zt.emoji("DoorOpened")}> - conf. bem vindo saida', value='\u200b', inline=False) \
            .add_field(name=f'<{self.zt.emoji("Captcha")}> - conf. captcha', value='\u200b', inline=False)
            configmsg = await ctx.send(embed=embed)
            def check(reaction, user):
                return reaction.message.channel == ctx.channel and user == ctx.author
            while not self.zt.is_closed():
                try:
                    guild = self.zt.db.Servers.find_one({'_id': ctx.guild.id})
                except:
                    self.zt.db.Servers.insert_one({'_id': ctx.guild.id, 'lan': 'por'})
                    guild = self.zt.db.Servers.find_one({'_id': ctx.guild.id})

                emojis = ['Logs', 'MembershipCard', 'DoorOpened', 'Captcha', 'Cancel']

                for emoji in emojis:
                    await configmsg.add_reaction(self.zt.emoji(emoji))
                    await asyncio.sleep(0.2)
                reaction, user = await self.zt.wait_for('reaction_add', check=check, timeout=120)
                try:
                    await configmsg.remove_reaction(reaction, user)
                    await asyncio.sleep(0.2)
                except:
                    pass
                for emoji in emojis:
                    await configmsg.remove_reaction(self.zt.emoji(emoji), self.zt.user)
                    await asyncio.sleep(0.2)
                baseEmbed = discord.Embed(color=color(self.zt), timestamp=datetime.datetime.utcnow()) \
                .set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url) 
                if str(reaction) == f'<{self.zt.emoji("DoorOpened")}>':
                    baseEmbed.description = f'<{self.zt.emoji("DoorOpened")}> - entrada\n\n<{self.zt.emoji("ExitSign")}> - saida'
                    await configmsg.edit(embed=baseEmbed)
                    
                elif str(reaction) == f'<{self.zt.emoji("Logs")}>':
                    baseEmbed.title = 'config.logs'
                    emojiLogs = ['Cancel']
                    while not self.zt.is_closed():
                        base2 = discord.Embed(color=color(self.zt), timestamp=datetime.datetime.utcnow()) \
                        .set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url) 
                        for emoji in emojiLogs:
                            await configmsg.add_reaction(self.zt.emoji(emoji))
                            await asyncio.sleep(0.2)
                        try:
                            reaction, user = await self.zt.wait_for('reaction_add', check=check, timeout=120)
                        except asyncio.TimeoutError:
                            break
                        for emoji in emojiLogs:
                            await configmsg.remove_reaction(self.zt.emoji(emoji), self.zt.user)
                        try:
                            await configmsg.remove_reaction(reaction, user)
                            await asyncio.sleep(0.2)
                        except discord.Forbidden:
                            pass
                        await configmsg.edit(embed=baseEmbed)          
                elif str(reaction) == f'<{self.zt.emoji("MembershipCard")}>':
                    baseEmbed.description = ''
                    await configmsg.edit(embed=baseEmbed)
                elif str(reaction) == f'<{self.zt.emoji("Captcha")}>':
                    baseEmbed.description = ''
                    await configmsg.edit(embed=baseEmbed)
                elif str(reaction) == f'<{self.zt.emoji("Cancel")}>':
                    await configmsg.delete()
                    return await ctx.message.delete()    
        except Exception as e:
            await ctx.send(e)
def setup(zt):
    zt.add_cog(Config(zt))