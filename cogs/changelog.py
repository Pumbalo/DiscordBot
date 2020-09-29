import discord
from discord.ext import commands
import asyncio
import sqlite3
from datetime import datetime
from pytz import timezone


class Changelog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Changelog is loaded')

    @commands.group(invoke_without_command=True)
    async def changelog(self, ctx):
        embed = discord.Embed(title="Changelog Commands",
                              description="Channel: <#channel>\nMessage: <message>", color=0)
        await ctx.send(embed=embed)

    @changelog.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.administrator:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f'SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if result is None:
                sql = ('INSERT INTO main(guild_id, channel_id) VALUES(?,?)')
                val = (ctx.guild.id, channel.id)
                await ctx.send(f'Channel has been set to {channel.mention}')
            elif result is not None:
                sql = ('UPDATE main SET channel_id = ? WHERE guild_id = ?')
                val = (channel.id, ctx.guild.id)
                await ctx.send(f'Channel has been updated to {channel.mention}')
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @changelog.command()
    async def message(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            est = timezone('EST')
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id FROM main WHERE 1')
            channel = cursor.fetchone()
            channel_id = self.client.get_channel(int(channel[0]))
            message = text.capitalize()
            embed = discord.Embed(
                title="Changelog", description=f"● {message}", color=0)
            embed.set_author(name='Reef Craft',
                             icon_url='https://cdn.discordapp.com/attachments/695804765023633449/727633388923781210/1.png')
            embed.set_footer(
                text=f'Published: {datetime.now(est).strftime("%Y-%m-%d %H:%M:%S")} By: {ctx.author}')
            await channel_id.send(embed=embed)
            cursor.close()
            db.close()


def setup(client):
    client.add_cog(Changelog(client))
