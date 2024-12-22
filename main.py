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
from cogs import info, states, roles

print(f"[b yellow] Python version: {sys.version}")
print(f"[b green] Initializing...")
intents = Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=configs["prefix"], intents=intents)

print(f"[b green] Loading cogs...")

basics = [info.setup(bot), roles.setup(bot)]
states = [states.setup(bot)]
cogs_array = [basics, states]

for cog_type in cogs_array:
    for cog in cog_type:
        try:
            asyncio.run(cog)
        except Exception as e:
            print(f"[b red] Error loading cog: {cog} - {e}")

print(f"[b green] Starting bot...")
bot.run(configs["token"])
