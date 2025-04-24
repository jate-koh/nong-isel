# System Libs
import sys

# Discord Bot Libs
from discord import Intents

# Bots Components
from core import BotCore
from cogs import states_cogs, commands_cogs
from settings import configs, test_flags
from utilities import log


def main():
    log(f"Python version: {sys.version}", type="info")
    log(f"Initializing...", type="info")

    # Intents
    intents = Intents.default()
    intents.members = True
    intents.message_content = True

    try:
        bot = BotCore(configs=configs, flags=test_flags, intents=intents)
        bot.setupCogs(states_cogs=states_cogs, commands_cogs=commands_cogs)
        bot.run()
    except Exception as err:
        log(f"Error!", type="error", json_data=str(err))


if __name__ == "__main__":
    main()
