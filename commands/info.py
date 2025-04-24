import discord
from discord import app_commands
from discord.ext import commands

from constants import default_configs
from settings import configs as conf


class InfoCommands(commands.Cog):

    def __init__(self, bot, logger, configs=None):
        if bot is None or logger is None:
            raise ValueError("bot and logger are required")

        self.bot = bot
        self.logger = logger

        if configs is not None:
            self.configs = configs
        else:
            self.configs = default_configs()

    @commands.hybrid_command(
        name="info",
        description="Get information about the server",
        with_app_command=True,
    )
    @commands.has_any_role(conf["admin_role"])
    @app_commands.guilds()
    async def info(self, ctx):

        user = ctx.author
        self.logger.info(f"{user} requested server info.")

        embed = discord.Embed(
            title="Server Information",
            description=f"Server Name: {ctx.guild.name}\nMember Count: {ctx.guild.member_count}\nCreated At: {ctx.guild.created_at}",
            color=discord.Color.blue(),
        )
        embed.set_footer(text=f"Requested by {user.name}", icon_url=user.avatar.url)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(
        name="sync",
        description="Sync slash commands",
        with_app_command=True,
    )
    @commands.has_any_role(conf["admin_role"])
    async def sync(self, ctx):
        self.logger.info("Syncing slash commands.")
        await self.bot.tree.sync(guild=discord.Object(id=conf["guild_id"]))
        await ctx.reply("Slash commands synced.")


async def setup(bot):
    await bot.add_cog(InfoCommands(bot))
