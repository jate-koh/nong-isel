import discord
from discord.ext import commands
from discord.ext.commands import (
    CommandNotFound,
    MissingPermissions,
    MemberNotFound,
    MissingRequiredArgument,
    MissingAnyRole,
)

from utils import read_message_txt
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
        elif isinstance(error, MissingAnyRole):
            embed.description = "You don't have permission to use this command"
        else:
            raise error
            embed.description = f"An error occurred: {error}"
        await ctx.reply(embed=embed)


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

        try:
            # Assign a role to the new member
            role = discord.utils.get(member.guild.roles, name=configs["guest_role"])
            if role is None:
                role = await member.guild.create_role(name=configs["guest_role"])

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

        # Check if reaction is one of react message (in message_id.txt)
        list_of_post = read_message_txt(dict=True).get("message_id")

        # If not in list, return
        if payload.message_id not in list_of_post:
            return

        print(f"[b yellow] Role reaction added by {member.name}")

        emoji = str(payload.emoji)

        role_name = next(
            (
                f"{configs['role_prefix']}{name}"
                for name, role_emoji in configs["emojis"].items()
                if role_emoji == emoji
            ),
            None,
        )

        if role_name:
            # Assign a role to member
            try:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    print(f"Assigning role '{role_name}' to {member}")
                    await member.add_roles(role)
                else:
                    print(f"Role '{role_name}' not found")

                # Remove guest role
                guest_role = discord.utils.get(
                    member.guild.roles, name=configs["guest_role"]
                )
                if guest_role is not None:
                    print(
                        f"[b yellow] Removing guest role {guest_role.name} from {member.name}"
                    )
                    await member.remove_roles(guest_role)
                else:
                    print(f"[b yellow] Guest role not found")

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

        # Check if reaction is one of react message (in message_id.txt)
        list_of_post = read_message_txt(dict=True).get("message_id")

        # If not in list, return
        if payload.message_id not in list_of_post:
            return

        print(f"[b yellow] Role reaction removed by {member.name}")

        emoji = str(payload.emoji)
        role_name = next(
            (
                f"{configs['role_prefix']}{name}"
                for name, role_emoji in configs["emojis"].items()
                if role_emoji == emoji
            ),
            None,
        )

        if role_name:
            try:
                # Remove role from member
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    print(f"Removing role '{role_name}' from {member}")
                    await member.remove_roles(role)
                else:
                    print(f"Role '{role_name}' not found")

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
