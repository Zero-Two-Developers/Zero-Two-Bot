import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Cog

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])


class enquete(Cog):
    def __init__(self, zt):
        self.zt = zt
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(pass_context = True, aliase=['votaçao'])
    async def enquete(self,ctx,*,arg):
        lang = self.zt.lang(ctx, "enquete")
        try: 
            sugestao = arg
            embed = discord.Embed(color=color(self.zt), timestamp=ctx.message.created_at,description=lang['vote'][0].format(self.zt.emoji("Verificado"),self.zt.emoji("Cancel")))
            embed.set_author(name=lang['vote'][1]+f" {ctx.message.author.display_name}")
            embed.add_field(name=lang['vote'][2], value="**"+sugestao+"**")
            embed.set_footer(text=lang['vote'][3])
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(self.zt.emoji("Verificado"))
            await msg.add_reaction(self.zt.emoji("Cancel"))
            await ctx.message.delete()
            await asyncio.sleep(86400) #86400 = 1dia

            def check(reaction, user):
                # await reaction.message.channel.get_message(reaction.message.id) is not None and
                return not str(reaction) in [f'<{self.zt.emoji("Verificado")}>',f'<{self.zt.emoji("Cancel")}>']
            '''while not self.zt.is_closed():
                try:
                    reaction, user = self.zt.wait_for('reaction_add', check=check, timeout=86400)
                    await reaction.message.remove_reaction(str(reaction).strip('<>'), user)
                except asyncio.TimeoutError:
                    return
                except:
                    pass'''
            msg = await msg.channel.get_message(msg.id)
            reactions_sim = [r.count for r in msg.reactions if str(r) == f'<{self.zt.emoji("Verificado")}>']
            reactions_nao = [r.count for r in msg.reactions if str(r) == f'<{self.zt.emoji("Cancel")}>']
            
            sim = 0
            nao = 0
            for count in reactions_sim:
                sim += count
            for count in reactions_nao:
                nao += count

            if sim > nao:
                await ctx.send(ctx.author.mention + lang['vote'][4]+f' <{self.zt.emoji("Verificado")}>')
            elif sim == nao:
                await ctx.send(ctx.author.mention + lang['vote'][5])
            else:
                await ctx.send(ctx.author.mention + lang['vote'][6]+f' <{self.zt.emoji("Cancel")}>')
            await msg.delete()
            embed = discord.Embed(colour=color(self.zt), timestamp=ctx.message.created_at)
            embed.set_author(name=lang['vote'][1] + f' {ctx.message.author.display_name}')
            embed.add_field(name=lang['vote'][2], value="**"+sugestao+"**",inline=False)
            embed.add_field(name=lang['vote'][7], value=lang['vote'][8].format(sim + nao - 2, sim-1, nao-1),inline=False)
            embed.set_footer(text=lang['vote'][9])
            await ctx.send(embed=embed)      
        except:
            embed3 = discord.Embed(colour=color(self.zt), timestamp=ctx.message.created_at)
            embed3.set_author(name=ctx.message.author.name + lang['vote'][10])
            embed3.set_footer(text="ZeroTwo © 2019")
            await ctx.send(embed=embed3)


def setup(zt):
    zt.add_cog(enquete(zt))
