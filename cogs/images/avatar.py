import discord
from discord.ext import commands
from discord.ext.commands import Cog

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

class avatar(Cog):
    def __init__(self, zt):
        self.zt = zt
 
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='avatar', aliases=['pic'])
    async def avatar(self, ctx, *,member: str=None):
        lang = self.zt.lang(ctx, "avatar")
        if member is not None:
            try:
                member = await commands.MemberConverter().convert(ctx, member)
            except commands.BadArgument:
                member = ctx.author
        else: 
            member = ctx.author
        if member == ctx.author:
            # embed = discord.Embed(color=color(self.zt), description=f'<{self.zt.emoji("MaleUser")}>'+lang["Embed"][0]+"\n<{}> [**Link**]({})".format(self.zt.emoji("Link"),member.avatar_url),timestamp = ctx.message.created_at) \
            embed = discord.Embed(color=color(self.zt), title=f'<{self.zt.emoji("MaleUser")}>'+lang["Embed"][0].replace("**", ""), url=member.avatar_url_as(format='png'), timestamp = ctx.message.created_at) \
            .set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
        else:
            # embed = discord.Embed(color=color(self.zt), description=f'<{self.zt.emoji("MaleUser")}>'+lang["Embed"][1].replace("Member.name",member.mention)+"\n<{}> [**Link Download**]({})".format(self.zt.emoji("Link"),member.avatar_url),timestamp = ctx.message.created_at) \
            embed = discord.Embed(color=color(self.zt), title=f'<{self.zt.emoji("MaleUser")}>'+lang["Embed"][1].replace("**", "").replace("Member.name", str(member)), url=member.avatar_url_as(format='png'), timestamp = ctx.message.created_at) \
            .set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
        
def setup(zt):
    zt.add_cog(avatar(zt))