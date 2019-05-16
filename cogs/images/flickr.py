import discord
import flickrapi

from discord.ext import commands
from discord.ext.commands import Cog

flickr = flickrapi.FlickrAPI('', '', format='etree')

def color(zt):
    c = zt.config('colors')['default2']
    return discord.Colour.from_rgb(c[0], c[1], c[2])

class Flickr(Cog):
    def __init__(self, zt):
        self.zt = zt
    @commands.command(name='flickr', aliases=['random'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def flickr_(self, ctx, *, tag: str=None):
        if tag is None:
            return
        url = None
        photo1 = flickr.photos_search(text=tag, tags=tag, sort='relevance', safe_search=3, tag_mode='all', extras='description,url_l,url_o')
        photo2 = [p for p in photo1[0]]
        while url is None and len(photo2) > 0:
            photo = photo2[0]
            url = photo.get('url_o') or photo.get('url_l')
            photo2.pop()
        if not url:
            return await ctx.send('mano deu erro geral')
        embed=discord.Embed(color=color(self.zt), description=photo.get('description')) \
        .set_image(url=url)
        await ctx.send(embed=embed)

def setup(zt):
    zt.add_cog(Flickr(zt))