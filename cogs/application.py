import discord
from discord.ext import commands
import asyncio
import sqlite3
from datetime import datetime
from pytz import timezone
import random

emojis = ['\U0001F4E9', '\U000023EF']


class Changelog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Application is loaded')

    @commands.group(invoke_without_command=True)
    async def application(self, ctx):
        embed = discord.Embed(title="Application Commands",
                              description="Channel: <#channel>", color=0)
        await ctx.send(embed=embed)

    @application.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.administrator:

            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f'SELECT channel_id FROM application WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if result is None:
                sql = ('INSERT INTO application(guild_id, channel_id) VALUES(?,?)')
                val = (ctx.guild.id, channel.id)
                await ctx.send(f'Message has been sent and channel has been set to {channel.mention}')
            elif result is not None:
                sql = ('UPDATE application SET channel_id = ? WHERE guild_id = ?')
                val = (channel.id, ctx.guild.id)
                await ctx.send(f'Message has been sent and channel has been updated to {channel.mention}')
            cursor.execute(sql, val)
            db.commit()
            cursor.execute(
                f'SELECT app_category FROM staffApp WHERE guild_id = {ctx.guild.id}')
            resultCat = cursor.fetchone()
            if resultCat is None:
                category = await ctx.guild.create_category('Staff-Application')
                sqql = ('INSERT INTO staffApp(guild_id, app_category) VALUES(?,?)')
                value = (category.id, ctx.guild.id)
                await ctx.send(f'Category has been set to {category}')
            elif resultCat is not None:
                await ctx.send('Category is already hooked')
            cursor.execute(sqql, value)
            db.commit()
            youtube = ':play_pause:'
            staff = ':envelope_with_arrow:'
            embed = discord.Embed(title="ReefCraft Applications", color=0)
            embed.add_field(
                name="** **", value=f"{youtube} YouTube Application\n\n{staff} Staff Application", inline=False)
            embed.add_field(name="\n\nInformation",
                            value="Reacting to one of the emotes will create a new text-channel, where you will write your applicaiton!")
            reaction_message = await channel.send(embed=embed)
            for emoji in emojis:
                await reaction_message.add_reaction(emoji)
            cursor.close()
            db.close()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        emoji = reaction.emoji
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id FROM application WHERE 1')
        channel = cursor.fetchone()
        channel_id = self.client.get_channel(int(channel[0]))
        cursor.execute('SELECT app_category FROM staffApp WHERE 1')
        categoryId = cursor.fetchone()
        category = int(categoryId[0])
        print(category)
        categoryTest = discord.CategoryChannel(category.id)
        #category = cursor.fetchone()
        #category_id = category[0]
        guild = user.guild
        categories = 1000
        if user.bot:
            return

        if emoji == "\U0001F4E9":
            await channel_id.send("You clicked the Staff Application")
            print(categories)
            await guild.create_text_channel("Staff", category=category)
        elif emoji == "\U000023EF":
            await channel_id.send("You clicked the Youtube Application")
        else:
            return


def setup(client):
    client.add_cog(Changelog(client))
