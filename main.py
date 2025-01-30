# System Libs
import sys
from rich import print

# Discord Bot Libs
from discord import Intents

# Bots Components
from core import BotCore
from settings import configs, test_flags
from cogs import states_cogs, commands_cogs


def main():
    print(f"[b yellow] Python version: {sys.version}")
    print(f"[b green] Initializing...")

    # Intents
    intents = Intents.default()
    intents.members = True
    intents.message_content = True

    # Bots
    bot = BotCore(configs=configs, flags=test_flags, intents=intents)
    bot.setupCogs(states_cogs=states_cogs, commands_cogs=commands_cogs)
    bot.run()


if __name__ == "__main__":
    main()
