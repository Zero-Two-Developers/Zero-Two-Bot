import time
import asyncio
import discord
import datetime

from .utils import baseEmbed

from discord.ext import commands
from discord.ext.commands import Cog
def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

class CommandErrorHandler(Cog):
    def __init__(self, zt):
        self.zt = zt
    @Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if hasattr(ctx.command, 'on_error'):
                return
            if hasattr(ctx.cog, f'_{ctx.cog.__class__.__name__}__error'):
                return
            error = getattr(error, 'original', error)
            ignored = ()
            embed = baseEmbed()
            if isinstance(error, ignored):
                return
            elif isinstance(error, commands.CommandNotFound):
                command = ctx.message.content[len(ctx.prefix):].split(' ')[0]
                embed.description = f'<{self.zt.emoji("Error")}> {self.zt.lang(ctx, "CommandErrorHandler")["CommandNotFound"].replace("commandname", command)}'
                await ctx.send(embed=embed, delete_after=15)
                await asyncio.sleep(15)
                await ctx.message.delete()
            elif isinstance(error, commands.CommandOnCooldown):
                if ctx.command.name == 'coins':
                    timet = time.gmtime(int(error.retry_after))
                    timeout = ''
                    if timet.tm_hour > 0:
                        timeout += (f'{timet.tm_hour} hora' + ('s' if timet.tm_hour != 1 else '') + ', ')
                    if timet.tm_min > 0:
                        timeout += (f'{timet.tm_min} minuto' + ('s' if timet.tm_min != 1 else '') + ' e ')
                    timeout += (f'{timet.tm_sec} segundo' + ('s' if timet.tm_sec != 1 else ''))
                    embed.description = f'<{self.zt.emoji("Error")}> **|** {self.zt.lang(ctx, "CommandErrorHandler")["CommandOnCooldown2"].replace("retry_after",timeout)}'
                    return await ctx.send(embed=embed)
                    
                embed.description = f'<{self.zt.emoji("Error")}> **|** {self.zt.lang(ctx, "CommandErrorHandler")["CommandOnCooldown"].replace("retry_after", str(int(error.retry_after)))}'
                await ctx.send(embed=embed, delete_after=error.retry_after)
                await asyncio.sleep(error.retry_after)
                await ctx.message.delete()

        except Exception as e:
            await ctx.send(e)
        
def setup(zt):
    zt.add_cog(CommandErrorHandler(zt))