import discord
from discord.ext import commands
from discord.ext.commands import (
    CommandNotFound,
    MissingPermissions,
    MemberNotFound,
    MissingRequiredArgument,
)

from rich import print


class ErrorState(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(title="Error", color=discord.Color.red())
        if isinstance(error, CommandNotFound):
            embed.description = "Command not found"
        elif isinstance(error, MissingPermissions):
            embed.description = "You don't have permission to use this command"
        elif isinstance(error, MemberNotFound):
            embed.description = "Member not found"
        elif isinstance(error, MissingRequiredArgument):
            embed.description = "Missing required argument"
        else:
            raise error
            embed.description = f"An error occurred: {error}"
        await ctx.send(embed=embed)


class ReadyState(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[b green] Bot is ready! Logged in as {self.bot.user}")
        print(
            f"[b yellow] Watching over guilds: {', '.join([guild.name for guild in self.bot.guilds])}"
        )


async def setup(bot):
    await bot.add_cog(ErrorState(bot))
    await bot.add_cog(ReadyState(bot))
