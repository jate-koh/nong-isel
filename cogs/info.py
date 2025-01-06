import discord
from discord.ext import commands
from settings import configs
from rich import print


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["server", "guild", "guildinfo"])
    @commands.has_any_role(configs["admin_role"])
    async def info(self, ctx):

        user = ctx.author
        print(f"[b yellow] Server information requested by {user.name}")

        embed = discord.Embed(
            title="Server Information",
            description=f"Server Name: {ctx.guild.name}\nMember Count: {ctx.guild.member_count}\nCreated At: {ctx.guild.created_at}",
            color=discord.Color.blue(),
        )
        embed.set_footer(text=f"Requested by {user.name}", icon_url=user.avatar.url)
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
