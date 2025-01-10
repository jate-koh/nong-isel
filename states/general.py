from discord.ext import commands
from rich import print


class GeneralState(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def onReady(self):
        print(f"[b green] Bot is ready! Logged in as {self.bot.user}")
        print(
            f"[b yellow] Watching over guilds: {', '.join([guild.name for guild in self.bot.guilds])}"
        )
