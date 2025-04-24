import discord
from discord.ext import commands

from constants import default_configs


class GeneralState(commands.Cog):

    def __init__(self, bot, logger, configs=None):
        if bot is None or logger is None:
            raise ValueError("bot and logger are required")

        self.bot = bot
        self.logger = logger
        if configs is not None:
            self.configs = configs
        else:
            self.configs = default_configs()

    @commands.Cog.listener("on_ready")
    async def onReady(self):
        self.logger.info(f"Bot is ready! Logged in as {self.bot.user}")
        self.logger.info(
            f"Watching over guilds: {', '.join([guild.name for guild in self.bot.guilds])}"
        )

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.custom, name="DMs me for questions!"
            )
        )
