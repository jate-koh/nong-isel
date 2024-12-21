import discord
from discord.ext import commands
from settings import configs


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["server"])
    async def info(self, ctx):
        embed = discord.Embed(
            title="Server Information",
            description=f"Server Name: {ctx.guild.name}\nMember Count: {ctx.guild.member_count}\nCreated At: {ctx.guild.created_at}",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
