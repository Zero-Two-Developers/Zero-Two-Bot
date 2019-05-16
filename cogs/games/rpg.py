import discord
from discord.ext import commands
import random
import pymongo
from discord.ext.commands import Cog

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

class rpg(Cog):
    def __init__(self, zt):
        self.zt = zt
 
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name='coins', aliases=['coin'])
    async def coins(self, ctx):
        lang = self.zt.lang(ctx, "rpgserver")
        coins = random.randint(100,500)
        sorte = random.randint(1,10)
        mult = random.randint(2,10)
        if sorte >= 8:
            coins *= mult
            embed = discord.Embed(color=color(self.zt), description=lang["coins"][1].format(ctx.author.mention,coins),timestamp = ctx.message.created_at)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=color(self.zt), description=lang["coins"][0].format(ctx.author.mention,coins),timestamp = ctx.message.created_at)
            await ctx.send(embed=embed)
            

        try:
            self.zt.db.Servers_rpg.insert_one({'_id': ctx.guild.id, f'{ctx.author.id}': {'money': 0}})
            playercoins = {f'{ctx.author.id}': {'money': 0}}

        except pymongo.errors.DuplicateKeyError:
            playercoins = self.zt.db.Servers_rpg.find_one({'_id': ctx.guild.id})
        if not f'{ctx.author.id}' in playercoins:
            playercoins = 0
        else:
            playercoins = playercoins[f'{ctx.author.id}']['money']

        self.zt.db.Servers_rpg.update_one({'_id': ctx.guild.id}, {'$set': {str(ctx.author.id): {'money': coins+playercoins}}})

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='rpgperfil', aliases=['rpgprofile'])
    async def rpgperfil_(self, ctx, *,member: str=None):
        lang = self.zt.lang(ctx, "rpgserver")
        if member is not None:
            try:
                member = await commands.MemberConverter().convert(ctx, member)
                msg = lang["rpgperfil"][1]
            except commands.BadArgument:
                member = ctx.author
                msg = lang["rpgperfil"][0]
        else: 
            member = ctx.author
            msg = lang["rpgperfil"][0]
        try:
            playercoins = self.zt.db.Servers_rpg.find_one({'_id': ctx.guild.id})[f'{member.id}']['money']
            embed = discord.Embed(color=color(self.zt),timestamp = ctx.message.created_at)\
            .set_author(name=msg + member.name)\
            .add_field(name=lang["rpgperfil"][3], value=playercoins)
            await ctx.send(embed=embed)
            
        except:
            embed = discord.Embed(color=color(self.zt), description=lang["rpgperfil"][2],timestamp = ctx.message.created_at)
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='apostar', aliases=['loteria'])
    async def apostar_(self, ctx,):
        n1 = str(random.randint(0,9))
        n2 = str(random.randint(0,9))
        n3 = str(random.randint(0,9))
        lang = self.zt.lang(ctx, "rpgserver")
        def check3(m):
            return m.author == ctx.author
        embed = discord.Embed(color=color(self.zt),description=lang["apostar"][0],timestamp = ctx.message.created_at)
        a = await ctx.send(embed=embed)
        await ctx.message.delete()
        try:
            msg = await self.zt.wait_for('message', check=check3, timeout=180)
            valor = int(msg.content)
        except:
            await ctx.send("ERROR")
        user_saldo = self.zt.db.Servers_rpg.find_one({'_id': ctx.guild.id})[f'{ctx.author.id}']['money']
        if valor > user_saldo:
            embed = discord.Embed(color=color(self.zt),description=lang["apostar"][1].format(user_saldo),timestamp = ctx.message.created_at)
            return await ctx.send(embed=embed)
        
        n1 = str(random.randint(0,9))
        n2 = str(random.randint(0,9))
        n3 = str(random.randint(0,9))
        numeros = [
            "000",
            "111",
            "222",
            "333",
            "444",
            "555",
            "666", 
            "777",   
            "888",
            "999"
        ]
        numeros_sortiados = n1 + n2 + n3
        if numeros_sortiados in numeros:
            valor_final = valor * 5
            embed = discord.Embed(color=color(self.zt),description=lang["apostar"][3].format(valor_final,numeros_sortiados),timestamp = ctx.message.created_at)
            return await ctx.send(embed=embed)
           # return await ctx.send("{} {}".format(valor_final,numeros_sortiados)) 
        elif n1 == n3 or n1 == n2 or n2 == n3:
            valor_final = valor * 2 
            embed = discord.Embed(color=color(self.zt),description=lang["apostar"][2].format(valor_final,numeros_sortiados),timestamp = ctx.message.created_at)
            return await ctx.send(embed=embed)
            #return await ctx.send("{} {}".format(valor_final,numeros_sortiados))
        else:
            valor_final = 0
            embed = discord.Embed(color=color(self.zt),description=lang["apostar"][4].format(valor_final,numeros_sortiados),timestamp = ctx.message.created_at)
            return await ctx.send(embed=embed)
            #return await ctx.send("{} {}".format(valor_final,numeros_sortiados))

        




def setup(zt):
    zt.add_cog(rpg(zt))