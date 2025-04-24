import discord
from discord.ext import commands

from utils import read_message_txt
from constants import default_configs, default_flags


class RoleState(commands.Cog):
    def __init__(self, bot, db, logger, configs=None, flags=None):
        if bot is None or logger is None or db is None:
            raise ValueError("bot, database, and logger are required")

        self.bot = bot
        self.db = db
        self.logger = logger

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
        self.logger.info(f"{member.name} joined the server")

        ############################## TESTING MODE ##############################
        if self.flags["disable_role_assign"] and self.flags["enable_testing"]:
            self.logger.warn(f"Role assignment is disabled by test flags.")
            return
        ##########################################################################

        # Assign a role to the new member
        try:
            role = discord.utils.get(
                member.guild.roles, name=self.configs["guest_role"]
            )
            if role is None:
                role = await member.guild.create_role(name=self.configs["guest_role"])

            self.logger.info(f"Assigning role {role.name} to {member.name}")
            await member.add_roles(role)
        except Exception as error:
            self.logger.error(
                f"Error assigning role to {member.name}", json_data=str(error)
            )
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
            self.logger.warn("Role reaction is disabled by test flags.")
            return
        ##########################################################################

        # Check if reaction is one of react message (in message_id.txt)
        list_of_post = read_message_txt(dict=True).get("message_id")

        # If not in list, return
        if payload.message_id not in list_of_post:
            return

        self.logger.info(f"Role reaction added by {member.name}")

        emoji = str(payload.emoji)


        role_name = next(
            (
                f"{self.configs['role_prefix']}{name}"
                for name, role_emoji in self.configs["emojis"].items()
                if role_emoji == emoji
            ),
            None,
        )

        # print(emoji)

        if role_name:
            try:
                # Assign a role to the new member
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    self.logger.info(f"Assigning role {role.name} to {member.name}")
                    await member.add_roles(role)
                else:
                    self.logger.info(f"Role {role_name} not found")

                # Remove anonymous/guest role
                role = discord.utils.get(guild.roles, name=self.configs["guest_role"])
                if role:
                    await member.remove_roles(role)
                else:
                    self.logger.info(f"Role {self.configs['guest_role']} not found")

                self.db.insert_usergroup(member.id, role.id)

            except Exception as error:
                self.logger.error(
                    f"Error assigning role to {member.name}", json_data=str(error)
                )
                return
        else:
            self.logger.warn("Role not found.")

    @commands.Cog.listener("on_raw_reaction_remove")
    async def removeRoleOnUnReact(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # Ignore bot reactions
        if member.bot:
            return

        ############################## TESTING MODE ##############################
        if self.flags["disable_role_react"] and self.flags["enable_testing"]:
            self.logger.warn("Role reaction is disabled by test flags.")
            return
        ##########################################################################

        # Check if reaction is one of react message (in message_id.txt)
        list_of_post = read_message_txt(dict=True).get("message_id")

        # If not in list, return
        if payload.message_id not in list_of_post:
            return

        self.logger.info(f"Role reaction removed by {member.name}")

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
                # Remove role from member
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    self.logger.info(f"Removing role {role.name} from {member.name}")
                    await member.remove_roles(role)
                else:
                    self.logger.warn(f"Role {role_name} not found")

                # Add anonymous/guest role
                role = discord.utils.get(guild.roles, name=self.configs["guest_role"])
                if role:
                    await member.add_roles(role)
                else:
                    self.logger.info(f"Role {self.configs['guest_role']} not found")

            except Exception as error:
                self.logger.error(
                    f"Error removing role from {member.name}", json_data=str(error)
                )
                return
        else:
            self.logger.warn("Role not found.")
