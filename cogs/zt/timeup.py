import discord
from discord.ext import commands
import time
import datetime
from datetime import datetime
import psutil
import os
from discord.ext.commands import Cog

time1 = datetime.now()

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

def getuptime(zt, ctx):
    '''
        lang = zt.lang(ctx, 'timeup')['time']
        segundos = round((datetime.now() - time1).total_seconds())
        p = psutil.Process(os.getpid())
        tempo = p.create_time()
        w = int(tempo) - int(tempo) + segundos
        minute = 60
        hour = minute * 60
        day = hour * 24
        days = int(w / day)
        hours = int((w % day) / hour)
        minutes = int((w % hour) / minute)
        seconds = int(w % minute)
        timeout = ''
        if days > 0:
            timeout += (f'{days} ' + (lang[0] if days == 1 else lang[8]) + ', ')
        if hour > 0:
            timeout += (f'{hours} ' + (lang[1] if hours == 1 else lang[2]) + ', ')
        if minutes > 0:
            timeout += (f'{minutes} ' + (lang[3] if minutes == 1 else lang[4]) + ' e ')
        timeout += (f'{seconds} ' + (lang[5] if seconds == 1 else lang[6]))
        
        return ("{}".format(lang[7]) % timeout + f'{minutes}')'''
    lang = zt.lang(ctx, 'timeup')
    segundos = round((datetime.now() - time1).total_seconds())
    p = psutil.Process(os.getpid())  # p.create_time()
    tempo = p.create_time()
    w = int(tempo) - int(tempo) + segundos
    minute = 60
    hour = minute * 60
    day = hour * 24
    days = int(w / day)
    hours = int((w % day) / hour)
    minutes = int((w % hour) / minute)
    seconds = int(w % minute)
    string = ""
    if days > 0:
        string += str(days) + " " + (days == 1 and "{}".format(lang["time"][0]) or "{}".format(lang["time"][8])) + ", "
    if len(string) > 0 or hours > 0:
        string += str(hours) + " " + (hours == 1 and "{}".format(lang["time"][1]) or "{}".format(lang["time"][2])) + ", "
    if len(string) > 0 or minutes > 0:
        string += str(minutes) + " " + (minutes == 1 and "{}".format(lang["time"][3]) or "{}".format(lang["time"][4])) + ", "
    string += str(seconds) + " " + (seconds == 1 and "{}".format(lang["time"][5]) or "{}".format(lang["time"][6]))
    return ("{}".format(lang["time"][7]) % string)

class timeup(Cog):
    def __init__(self,zt):
        self.zt = zt
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='timeup', aliases=['uptime'])
    async def timeup(self, ctx):
        embed = discord.Embed(color=color(self.zt), description=f'<{self.zt.emoji("online")}> **'+getuptime(self.zt, ctx)+"**",timestamp = ctx.message.created_at)
        await ctx.send(embed=embed)
        


def setup(zt):
    zt.add_cog(timeup(zt))