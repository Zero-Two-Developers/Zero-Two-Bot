from discord import Embed
from discord.ext import commands

__all__ = ['baseEmbed', 'Paginator']

def baseEmbed(color=0xE9358B):
    return Embed(color=color)
class Paginator:
    def __init__(self, pages=[], ):
        self.paginator = commands.Paginator(prefix='**', suffix='**', max_size=1024)
