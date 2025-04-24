import discord
from discord.ext import commands
from discord.ext.commands import (
    CommandNotFound,
    MissingPermissions,
    MemberNotFound,
    MissingRequiredArgument,
    MissingAnyRole,
)


class ErrorState(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_command_error")
    async def onError(self, ctx, error):
        embed = discord.Embed(title="Error", color=discord.Color.red())
        if isinstance(error, CommandNotFound):
            embed.description = "Command not found"
        elif isinstance(error, MissingPermissions):
            embed.description = "You don't have permission to use this command"
        elif isinstance(error, MemberNotFound):
            embed.description = "Member not found"
        elif isinstance(error, MissingRequiredArgument):
            embed.description = "Missing required argument"
        elif isinstance(error, MissingAnyRole):
            embed.description = "You don't have permission to use this command"
        else:
            embed.description = f"An error occurred: {error}"
            await ctx.reply(embed=embed)
            raise error
