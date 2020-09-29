import discord
from discord.ext import commands
import os
import sys
import asyncio
import sqlite3

client = commands.Bot(command_prefix='!!')


@client.event
async def on_ready():
    print('I am online!')
    return await client.change_presence(activity=discord.Activity(type=1, name='play.reefcraft.net', url="http://store.reefcraft.net/"))


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('NzU5NDE4Mjg1OTM3OTE3OTUy.X29NZA.apwmqolNESdB4HqSlvAwSqjv5YA')
