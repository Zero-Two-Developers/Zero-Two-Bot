import psutil
import discord
from discord.ext import commands
from cogs.core.utils import baseEmbed
from cogs.zt.timeup import getuptime

cpuinfo = open('/proc/cpuinfo')
info = [{}]
for line in cpuinfo:
    name_value = [s.strip() for s in line.split(':', 1)]
    if len(name_value) != 2:
        continue
    name, value = name_value
    if not info or name in info[-1]:
        info.append({})
    info[-1][name] = value
cpuinfo.close()

class BotInfo(commands.Cog):
    def __init__(self, zt):
        self.zt = zt

    @commands.command(aliases=['bot_info', 'binfo'])
    @commands.guild_only()
    async def botinfo(self, ctx):
        thomas = await self.zt.get_user_info(171715191992483840)
        shiba = await self.zt.get_user_info(355750436424384524)
        lrv = await self.zt.get_user_info(286589600452050954)
        djinn = await self.zt.get_user_info(376460601909706773)
        ssd = psutil.disk_usage('/')
        memory = psutil.virtual_memory()
        uptime = getuptime(self.zt, ctx).replace("I'm online at ", '').replace("Ich bin online bei ", '').replace("Estoy en línea ", '').replace("Estou online à ", '')
        embed = baseEmbed() \
            .set_author(name=str(self.zt.user), icon_url=self.zt.user.avatar_url) \
                .add_field(name=f'<{self.zt.emoji("Moderator")}> Criadores:', value=f'`{thomas}\n{shiba}`') \
                    .add_field(name=f'<{self.zt.emoji("UserGroups")}> Ajudantes:', value=f'`{lrv}\n{djinn}`') \
                        .add_field(name=f'<{self.zt.emoji("Right")}> Prefixos:', value='`zt `, `zt.`, `02 `, `002`') \
                            .add_field(name=f'<{self.zt.emoji("MembershipCard")}> ID:', value=f'`{self.zt.user.id}`') \
                                .add_field(name=f'<{self.zt.emoji("RAM")}> Memória RAM usada:', value=f'`{"%.2f" % (memory.used/1024**3)}GB/{"%.2f" % (memory.total/1024**3)}GB ({memory.percent}%)`') \
                                    .add_field(name=f'<{self.zt.emoji("SSD")}> Armazenamento usado:', value=f'`{"%.2f" % (ssd.used/1024**3)}GB/{"%.2f" % (ssd.total/1024**3)}GB ({ssd.percent}%)`') \
                                        .add_field(name=f'<{self.zt.emoji("Electronics")}> CPU:', value=f'`{info[0]["cpu cores"]} x {info[0]["model name"]}`', inline=False) \
                                            .add_field(name=f'<{self.zt.emoji("Signal")}> Ping:', value=f'`{"%.0f" % (self.zt.latencies[ctx.guild.shard_id][1]*1000)}ms`') \
                                                .add_field(name=f'<{self.zt.emoji("Discord")}> Api:', value=f'`discord.py {discord.__version__}`') \
                                                    .add_field(name=f'<{self.zt.emoji("Python")}> Linguagem de programação:', value='`Python`')# \
                                                        # .add_field(name=f'<{self.zt.emoji("Clock")}> Uptime:', value=f'`{uptime}`') 
                                                        
        await ctx.send(embed=embed)



def setup(zt):
    zt.add_cog(BotInfo(zt))