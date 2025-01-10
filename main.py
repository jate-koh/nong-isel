# System Libs
import sys
import asyncio
from rich import print

# Discord Bot Libs
from discord import Intents
from discord.ext import commands

# Bot Settings
from settings import configs, test_flags
from cogs import statesCogs, commandsCogs


def main():
    print(f"[b yellow] Python version: {sys.version}")
    print(f"[b green] Initializing...")
    intents = Intents.default()
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(command_prefix=configs["prefix"], intents=intents)

    print(f"[b green] Loading cogs...")

    bot_commands = [
        commandsCogs.setup(
            bot=bot,
            configs=configs,
            flags=test_flags,
        ),
    ]
    bot_states = [
        statesCogs.setup(
            bot=bot,
            configs=configs,
            flags=test_flags,
        )
    ]
    cogs_array = [bot_commands, bot_states]

    for cog_type in cogs_array:
        for cog in cog_type:
            try:
                asyncio.run(cog)
            except Exception as e:
                print(f"[b red] Error loading cog: {cog} - {e}")

    print(f"[b green] Starting bot...")
    bot.run(configs["token"])


if __name__ == "__main__":
    main()
