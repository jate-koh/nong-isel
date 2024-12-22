import discord
from discord.ext import commands
from discord.ext.commands import (
    CommandNotFound,
    MissingPermissions,
    MemberNotFound,
    MissingRequiredArgument,
)

from settings import configs
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


class OnJoinState(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"[b yellow] {member.name} joined the server")

        # Assign a role to the new member
        try:
            role = discord.utils.get(member.guild.roles, name="anonymous")
            if role is None:
                role = await member.guild.create_role(name="anonymous")

            print(f"[b yellow] Assigning role {role.name} to {member.name}")
            await member.add_roles(role)
        except Exception as error:
            print(f"[b red] Error assigning role to {member.name} - {error}")


class OnAddReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # Ignore bot reactions
        if member.bot:
            return

        with open("message_id.txt", "r") as f:
            string = f.read()
        message_id = int(string.split("\n")[0])

        # If not reaction on "Role Assignment" post
        if payload.message_id != message_id:
            return

        print(
            f'[b yellow] Reaction added on "Role Assignment" post detected by {payload.user_id}'
        )

        emoji = str(payload.emoji)
        role_name = next(
            (
                name
                for name, role_emoji in configs["emojis"].items()
                if role_emoji == emoji
            ),
            None,
        )

        if role_name:
            try:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    print(f"Assigning role '{role_name}' to {member}")
                    await member.add_roles(role)
            except Exception as error:
                print(f"[b red] Error assigning role to {member.name} - {error}")
        else:
            print(f"[b red] Error assigning role to {member.name} - Role not found")


class OnRemoveReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # Ignore bot reactions
        if member.bot:
            return

        with open("message_id.txt", "r") as f:
            string = f.read()
        message_id = int(string.split("\n")[0])

        # If not reaction on "Role Assignment" post
        if payload.message_id != message_id:
            return

        print(
            f'[b yellow] Reaction removed from "Role Assignment" post detected by {payload.user_id}'
        )

        emoji = str(payload.emoji)
        role_name = next(
            (
                name
                for name, role_emoji in configs["emojis"].items()
                if role_emoji == emoji
            ),
            None,
        )

        if role_name:
            try:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    print(f"Removing role '{role_name}' from {member}")
                    await member.remove_roles(role)
            except Exception as error:
                print(f"[b red] Error removing role from {member.name} - {error}")
        else:
            print(f"[b red] Error removing role from {member.name} - Role not found")


async def setup(bot):
    await bot.add_cog(ErrorState(bot))
    await bot.add_cog(ReadyState(bot))
    await bot.add_cog(OnJoinState(bot))
    await bot.add_cog(OnAddReaction(bot))
    await bot.add_cog(OnRemoveReaction(bot))
