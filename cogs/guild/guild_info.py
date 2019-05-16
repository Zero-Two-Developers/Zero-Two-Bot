import discord
from discord.ext import commands
from discord.ext.commands import Cog

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

class guild(Cog):
    def __init__(self, zt):
        self.zt = zt

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='server', aliases=['guild','guildinfo','serverinfo'])
    async def guildinfo_(self, ctx):
        lang = self.zt.lang(ctx, "guildinfo")
        serverinfo_embed = discord.Embed(colour=color(self.zt),timestamp=ctx.message.created_at)
        online = len([y.id for y in ctx.guild.members if y.status == discord.Status.online  and not y.bot])
        afk  = len([y.id for y in ctx.guild.members if y.status == y.status == discord.Status.idle and not y.bot])
        offline = len([y.id for y in ctx.guild.members if y.status == y.status == discord.Status.offline and not y.bot])
        dnd = len([y.id for y in ctx.guild.members if y.status == y.status == discord.Status.dnd and not y.bot])
        stream = len([y.id for y in ctx.guild.members if y.activity is not None and y.activity.type == 1 and not y.bot])
        bots= len([y.id for y in ctx.guild.members if y.bot])
        humanos = len([y.id for y in ctx.guild.members if not y.bot])
        usuario_total = bots+humanos
        membros = "<{}>".format(self.zt.emoji("online"))+lang["membros"][0]+str(online)+'``'+"\n<{}>".format(self.zt.emoji("ausente"))+lang["membros"][2]+str(afk)+'``'+"\n<{}>".format(self.zt.emoji("dnd"))+lang["membros"][1]+str(dnd)+'``'+"\n<{}>".format(self.zt.emoji("offline"))+lang["membros"][3]+str(offline)+'``'+"\n<{}>".format(self.zt.emoji("streamon"))+lang["membros"][4]+str(stream)+'``'+"\n<{}>".format(self.zt.emoji("bot"))+lang["membros"][5]+str(bots)+'``'
        emojis = len([y.id for y in ctx.guild.emojis])
        emoji = '``'+str(emojis)+"/100``"
        cargo = ctx.guild
        serverinfo_embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        serverinfo_embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
        serverinfo_embed.add_field(name=f"<{self.zt.emoji('Moderator')}> "+lang['guild'][0], value=f"{ctx.guild.owner.mention}",inline=True)
        serverinfo_embed.add_field(name=f"<{self.zt.emoji('MembershipCard')}> "+lang['guild'][1], value=f"``{ctx.guild.id}``",inline=True)
        serverinfo_embed.add_field(name=f"<{self.zt.emoji('Globe')}> "+lang['guild'][2], value=f"``{ctx.guild.region}``",inline=True)
        serverinfo_embed.add_field(name=f"<{self.zt.emoji('Today')}> "+lang['guild'][3],  value='``'+ctx.guild.created_at.strftime("%d %b %Y %H:%M")+'``',inline=True)
        serverinfo_embed.add_field(name=f'<{self.zt.emoji("Speaker")}> '+lang['guild'][4],value='``{}``'.format(len(ctx.guild.text_channels)),inline=True)
        serverinfo_embed.add_field(name=f'<{self.zt.emoji("ChatBubble")}> '+lang['guild'][5],value='``{}``'.format(len(ctx.guild.text_channels)),inline=True)
        serverinfo_embed.add_field(name=f"<{self.zt.emoji('Happy')}> Emojis: ", value=emoji,inline=False)
        serverinfo_embed.add_field(name=f'<{self.zt.emoji("MaleUser")}>'+lang['guild'][6]+'['+str(usuario_total)+']:', value=membros,inline=True)
        a = ', '.join([r.mention for r in cargo.roles if r.name != '@everyone'])
        if len(', '.join([r.mention for r in cargo.roles if r.name != '@everyone'])) > 1024:
            a = '\u200b'
        serverinfo_embed.add_field(name='<{}> {} {}'.format(self.zt.emoji("Cargos"),lang['guild'][7],str(len(ctx.guild.roles)-1)),value=a,inline=True)
        await ctx.send(embed=serverinfo_embed)


def setup(zt):
    zt.add_cog(guild(zt))