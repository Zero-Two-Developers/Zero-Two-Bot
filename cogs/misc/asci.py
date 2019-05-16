import discord
import asyncio
from discord.ext import commands
from pyfiglet import Figlet
from discord.ext.commands import Cog

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

class asci(Cog):
    def __init__(self, zt):
        self.zt = zt


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(pass_context = True)
    async def asci(self,ctx, *, arg):
        lang = self.zt.lang(ctx, "asci")
        mensagem = arg.replace('é', 'e').replace('ê', 'e').replace('ẽ', 'e').replace('á', 'a').replace('ã', 'a').replace('â', 'a').replace('É', 'E').replace('Ê', 'E').replace('Ẽ', 'E').replace('Á', 'A').replace('Ã', 'A').replace('Â', 'A')
        #f = Figlet(font='slant')
        f = Figlet(font='larry3d')
        #f = Figlet(font='big')
        
        texto = f.renderText(mensagem)
        if len(texto) > 2000:
            embed = discord.Embed(color=color(self.zt), description=f'<{self.zt.emoji("Error")}> '+lang["asci"][0],timestamp = ctx.message.created_at)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await ctx.message.delete()
            await msg.delete()
            return
        await ctx.send("```py\n{}```".format(texto))

#1. http://www.figlet.org/examples.html
#2. http://www.figlet.org/fontdb.cgi
def setup(zt):
    zt.add_cog(asci(zt))
