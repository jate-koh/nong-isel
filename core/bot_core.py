import asyncio
from discord import Intents
from discord.ext import commands
from rich import print

from constants import default_configs, default_flags


class BotCore:
    def __init__(self, configs=None, flags=None, intents=None):
        if configs is None:
            self.configs = default_configs()
        else:
            self.configs = configs

        if intents is None:
            self.intents = Intents.default()
            intents.members = True
            intents.message_content = True
        else:
            self.intents = intents

        if flags is None:
            self.flags = default_flags()
        else:
            self.flags = flags

        self.bot = commands.Bot(
            command_prefix=self.configs["prefix"], intents=self.intents
        )

        print(f"[b green] Bot Initialized.")

    def setupCogs(self, states_cogs, commands_cogs):
        if states_cogs is None and commands_cogs is None:
            print(f"[b yellow] No cogs to load.")
            return

        if states_cogs is not None:
            bot_states = [
                states_cogs.setup(
                    bot=self.bot,
                    configs=self.configs,
                    flags=self.flags,
                )
            ]
        else:
            bot_states = []

        if commands_cogs is not None:
            bot_commands = [
                commands_cogs.setup(
                    bot=self.bot,
                    configs=self.configs,
                    flags=self.flags,
                )
            ]
        else:
            bot_commands = []

        cogs_array = [bot_states, bot_commands]

        for cog_type in cogs_array:
            for cog in cog_type:
                try:
                    asyncio.run(cog)
                except Exception as error:
                    print(f"[b red] Error loading cog: {cog} - {error}")

    def run(self):
        if self.configs["token"]:
            print(f"[b green] Running bot...")
            self.bot.run(self.configs["token"])
        else:
            print(f"[b red] No token provided.")
            return

    def getBot(self):
        return self.bot

    def getConfigs(self):
        return self.configs

    def getFlags(self):
        return self.flags
