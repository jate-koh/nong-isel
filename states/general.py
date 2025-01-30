import discord
from discord.ext import commands
from rich import print

from constants import default_configs


class GeneralState(commands.Cog):

    def __init__(self, bot, configs=None):
        self.bot = bot

        if configs is not None:
            self.configs = configs
        else:
            self.configs = default_configs()

    @commands.Cog.listener("on_ready")
    async def onReady(self):
        print(f"[b green] Bot is ready! Logged in as {self.bot.user}")
        print(
            f"[b yellow] Watching over guilds: {', '.join([guild.name for guild in self.bot.guilds])}"
        )

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.custom, name="DMs me for questions!"
            )
        )
