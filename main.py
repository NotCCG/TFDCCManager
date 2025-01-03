import time
from typing import Final
import os

import discord
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
import datetime
import asyncio

# Token Setup
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print('Token Setup: [COMPLETE]')

# Intents Setup
intents: Intents = Intents.default()
intents.message_content = True
time.sleep(0.5)
print('Intents Setup: [COMPLETE]')

# Bot Client Setup
botClient = commands.Bot(command_prefix='>/', intents=intents)
time.sleep(0.5)
print('Bot Client Setup: [COMPLETE]')
@botClient.event
async def on_ready():
    print("CCManager: [ONLINE]")


# Bot Stuffs
@botClient.command()
@commands.has_permissions(manage_messages=True)
async def Clean(ctx):
    approved_channels = [726169466768982098, 726169758806048839, 726171251852312576, 1291191686650789951]
    channel = ctx.channel
    message_history = {}
    two_weeks_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(weeks=2)
    await ctx.message.delete()

    if channel.id not in approved_channels:
        print('incorrect channel')
        await ctx.message.delete()
        return
    else:
        async for message in channel.history(limit=None):
            # Check to make sure the message is from a bot. Ignores if it is.
            if message.author.bot:
                continue

            # Check to see if the message is more than two weeks old, deletes if it is
            if message.created_at < two_weeks_ago:
                await message.delete()
                await asyncio.sleep(2)
                continue

            # Checks message content matches any in the message_history list. Deletes if it is.
            if message.content in message_history:
                await message.delete()
                await asyncio.sleep(2)

            # If the message does not match anything in the list, it is added.
            else:
                message_history[message.content] = message.id

# Error Handling, outputs error to console as bot will only be online as needed.
@Clean.error
async def cleanDupes_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        print('unauthorized user attempted use')
        await ctx.message.delete

# You're not a good person.
# You know that right?
# Good people, don't end up here.

botClient.run(TOKEN)