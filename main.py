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
async def CleanDupes(ctx):
    correct_channel = discord.utils.get(botClient.get_all_channels(), id=726169466768982098)
    channel = ctx.channel
    message_history = {}
    two_weeks_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(weeks=2)
    await ctx.message.delete()

    if ctx.channel != correct_channel:
        print('incorrect channel')
        return
    else:
        async for message in channel.history(limit=None):
            if message.author.bot:
                continue

            if message.created_at < two_weeks_ago:
                await message.delete()
                await asyncio.sleep(2)
                continue

            if message.content in message_history:
                await message.delete()
                await asyncio.sleep(2)

            else:
                message_history[message.content] = message.id


botClient.run(TOKEN)