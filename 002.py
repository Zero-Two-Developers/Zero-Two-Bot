import os
import sys
import json
import logging
import discord
import asyncio
import pymongo
import traceback
from cogs.zt import timeup
from discord.ext import commands
from json import dumps

basedb = {'lan': 'por', 'modulos':{'canais':{'logs':None,'bvimg':None,'bvmsg':None,'saidamsg':None,'music24/7':None},'cargos':{'mod':None,'captcha':None,'mute':None,'dj':None,'autorole':None},'onoff':{'logs':False,'bvimg':False,'bvimgmsg':False,'bvmsg':False,'bvmsgpv':False,'saidamsg':False,'music24/7':False,'captcha':False},'mensagens':{'bvmsg':None,'bvmsgpv':None,'bvimgmsg':None,'saidamsg':None}}}

with open('./data/config/config.json') as config:
    config = json.load(config)

def _config(keyword):
    return config[keyword]

def emoji(name: str):
    with open('./data/config/emojis.json') as emoji:
        emoji = json.load(emoji)
    return emoji[name]

with open('./data/config/extensions.json') as extensions:
    extensions = json.load(extensions)['extensions']

#logging.basicConfig(level=logging.DEBUG)

zt = commands.AutoShardedBot(command_prefix=config['prefix'], shard_count=2, shard_ids=(0, 1), case_insensitive=True)

def languages(ctx, cogname):
    with open('./data/traducoes/alemao.json') as alemao:
        alemao = json.load(alemao)

    with open('./data/traducoes/espanhol.json') as espanhol:
        espanhol = json.load(espanhol)

    with open('./data/traducoes/ingles.json') as ingles:
        ingles = json.load(ingles)

    with open('./data/traducoes/portugues.json') as portugues:
        portugues = json.load(portugues)
    lan = zt.db.Servers.find_one({'_id': ctx.guild.id})['lan']
        
    if lan == 'ale':
        return alemao[cogname]
    elif lan == 'esp':
        return espanhol[cogname]
    elif lan == 'ing':
        return ingles[cogname]
    elif lan == 'por':
        return portugues[cogname]


@zt.event
async def on_ready():
    dbservers = [guild['_id'] for guild in zt.db.Servers.find()]

    for guild in zt.guilds:
        if not guild.id in dbservers:
            bdb = basedb
            bdb['_id'] = guild.id
            zt.db.Servers.insert_one(bdb)
        

    while not zt.is_closed():
        await zt.change_presence(activity=discord.Game(name='002'), status=discord.Status.dnd)
        await asyncio.sleep(60)
        await zt.change_presence(activity=discord.Activity(name='Darling in the Franxx', type=discord.ActivityType.watching), status=discord.Status.dnd)
        await asyncio.sleep(60)
        # await zt.change_presence(activity=discord.Game(name=timeup.getuptime(zt, None)), status=discord.Status.dnd)
        # await asyncio.sleep(60)
        if hasattr(zt, 'lavalink'):
            await zt.change_presence(activity=discord.Activity(name=f'{len(zt.lavalink.players)} guilds.', type=discord.ActivityType.listening), status=discord.Status.dnd)
            await asyncio.sleep(60)

@zt.event
async def on_guild_join(guild):
    dbservers = [guild['_id'] for guild in zt.db.Servers.find()]
    if not guild.id in dbservers:
        mdb = basedb
        mdb['_id'] = guild.id
        zt.db.Servers.insert_one(basedb)
    else:
        zt.db.Servers.delete_one({'_id': guild.id})
        mdb = basedb
        mdb['_id'] = guild.id
        zt.db.Servers.insert_one(basedb)

@zt.event
async def on_guild_remove(guild):
    zt.db.Servers.delete_one({'_id': guild.id})

zt.lang = languages
zt.config = _config
zt.emoji = emoji
zt.extensions_ = extensions
zt.remove_command('help')

zt.db = pymongo.MongoClient('localhost')['002']

if __name__ == '__main__':
    for extension in zt.extensions_:
        try:
            zt.load_extension(extension)
        except Exception as e:
            print(e)
        
    zt.run(zt.config('keys')['discordApi'])