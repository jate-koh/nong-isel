# System Libs
import sys
import asyncio
import os

# Discord Bot Libs
import discord
from discord import Intents, app_commands
from discord.ext import commands
import dotenv
from rich import print

# Bot Settings
from settings import configs
from cogs import info

print(f"[b yellow] Python version: {sys.version}")
print(f"[b green] Initializing...")
intents = Intents.default()
intents.members = True
intents.message_content = True

print(f"[b green] Starting bot...")

bot = commands.Bot(command_prefix=configs["prefix"], intents=intents)


@bot.event
async def on_ready():

    print(f"[b green] Bot is ready! Logged in as {bot.user}")
    print(
        f"[b green] Watching over guilds: {', '.join([guild.name for guild in bot.guilds])}"
    )


print(f"[b green] Loading cogs...")

basics = [info.setup(bot)]

for cog in basics:
    asyncio.run(cog)

bot.run(configs["token"])
