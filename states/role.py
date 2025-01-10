import discord
from discord.ext import commands
from rich import print

from utils import read_message_txt
from constants import default_configs, default_flags


class RoleState(commands.Cog):
    def __init__(self, bot, configs=None, flags=None):
        self.bot = bot
        if configs is not None:
            self.configs = configs
        else:
            self.configs = default_configs()
        if flags is not None:
            self.flags = flags
        else:
            self.flags = default_flags()

    @commands.Cog.listener("on_member_join")
    async def giveRoleOnJoin(self, member):
        print(f"[b yellow] {member.name} joined the server")

        ############################## TESTING MODE ##############################
        if self.flags["disable_role_assign"] and self.flags["enable_testing"]:
            print(f"[b yellow] Role assignment is disabled by test flags.")
            return
        ##########################################################################

        # Assign a role to the new member
        try:
            role = discord.utils.get(
                member.guild.roles, name=self.configs["guest_role"]
            )
            if role is None:
                role = await member.guild.create_role(name=self.configs["guest_role"])

            print(f"[b yellow] Assigning role {role.name} to {member.name}")
            await member.add_roles(role)
        except Exception as error:
            print(f"[b red] Error assigning role to {member.name} - {error}")
            return

    @commands.Cog.listener("on_raw_reaction_add")
    async def giveRoleOnReact(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # Ignore bot reactions
        if member.bot:
            return

        ############################## TESTING MODE ##############################
        if self.flags["disable_role_react"] and self.flags["enable_testing"]:
            print(f"[b yellow] Role reaction is disabled by test flags.")
            return
        ##########################################################################

        # Check if reaction is one of react message (in message_id.txt)
        list_of_post = read_message_txt(dict=True).get("message_id")

        # If not in list, return
        if payload.message_id not in list_of_post:
            return

        print(f"[b yellow] Role reaction added by {member.name}")

        emoji = str(payload.emoji)

        role_name = next(
            (
                f"{self.configs['role_prefix']}{name}"
                for name, role_emoji in self.configs["emojis"].items()
                if role_emoji == emoji
            ),
            None,
        )

        if role_name:
            try:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    print(f"[b yellow] Assigning role {role.name} to {member.name}")
                    await member.add_roles(role)
                else:
                    print(f"[b yellow] Role {role_name} not found")
            except Exception as error:
                print(f"[b red] Error assigning role to {member.name} - {error}")
                return
        else:
            print(f"[b red] Role not found.")

    @commands.Cog.listener("on_raw_reaction_remove")
    async def removeRoleOnUnReact(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # Ignore bot reactions
        if member.bot:
            return

        ############################## TESTING MODE ##############################
        if self.flags["disable_role_react"] and self.flags["enable_testing"]:
            print(f"[b yellow] Role reaction is disabled by test flags.")
            return
        ##########################################################################

        # Check if reaction is one of react message (in message_id.txt)
        list_of_post = read_message_txt(dict=True).get("message_id")

        # If not in list, return
        if payload.message_id not in list_of_post:
            return

        print(f"[b yellow] Role reaction removed by {member.name}")

        emoji = str(payload.emoji)
        role_name = next(
            (
                f"{self.configs['role_prefix']}{name}"
                for name, role_emoji in self.configs["emojis"].items()
                if role_emoji == emoji
            ),
            None,
        )

        if role_name:
            try:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    print(f"[b yellow] Removing role {role.name} from {member.name}")
                    await member.remove_roles(role)
                else:
                    print(f"[b yellow] Role {role_name} not found")
            except Exception as error:
                print(f"[b red] Error removing role from {member.name} - {error}")
                return
        else:
            print(f"[b red] Role not found.")
