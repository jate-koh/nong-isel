import math
import discord
from discord.ext import commands

from utils import read_message_txt
from constants import default_configs, default_flags

# TODO:
# Provide configs for func args and @commands directive
# without importing from static settings
# but feed through instantiation.
from settings import configs as conf


class RoleGroupCommands(commands.Cog):

    def __init__(self, bot, logger, configs=None, flags=None):
        if bot is None or logger is None:
            raise ValueError("bot and logger are required")

        self.bot = bot
        self.logger = logger

        if configs is not None:
            self.configs = configs
        else:
            self.configs = default_configs()
        if flags is not None:
            self.flags = flags
        else:
            self.flags = default_flags()

    @commands.hybrid_command(
        name="createroles",
        with_app_command=True,
    )
    @commands.has_any_role(conf["admin_role"])
    async def create_roles(self, ctx, num_roles=conf["max_roles"], clear_all=False):
        self.logger.info(f"Running check...")

        guild = ctx.guild
        try:
            # Read from message text
            message_id, channel_id, current_num_roles = read_message_txt()

            # Check for exisitng messages
            if message_id is not None:
                self.logger.info(f"Existing messages found in local text.")

                channel = self.bot.get_channel(channel_id)
                if channel:
                    for id in message_id:
                        self.logger.info(f"Deleting exisiting message {id}")
                        try:
                            message = await channel.fetch_message(id)
                            await message.delete()
                        except discord.NotFound:
                            self.logger.warn(f"Message {id} not found.")
            else:
                self.logger.info("No existing messages found.")

            # Check for existing number of roles
            if current_num_roles is not None:
                self.logger.info(" Existing number of roles found in local text.")

                # Check if number of roles is valid
                # If Exceeds max number of roles
                if num_roles > self.configs["max_roles"]:
                    await ctx.send(
                        f"Maximum number of roles is {self.configs['max_roles']}"
                    )
                    return

                # If less than min number of roles
                if num_roles < self.configs["min_roles"]:
                    await ctx.send(
                        f"Minimum number of roles is {self.configs['min_roles']}"
                    )
                    return

                # If less than current number of roles, remove excess
                if num_roles < current_num_roles:
                    await self.clear_roles(
                        ctx,
                        start=num_roles + 1,
                        end=current_num_roles,
                        prefix=self.configs["role_prefix"],
                    )

                # If clear all is set
                if clear_all:
                    self.logger.info("Removing all existing roles...")
                    await self.clear_roles(
                        ctx,
                        start=1,
                        end=current_num_roles,
                        prefix=self.configs["role_prefix"],
                    )
            else:
                self.logger.info(f"No existing number of roles found.")

        except Exception as error:
            self.logger.error(
                "Error in preparation for setting up group roles.",
                json_data=str(error),
            )
            return

        self.logger.info("Setting up group roles and post for acquiring roles...")

        roles_to_emojis = {
            self.configs["role_prefix"] + str(i): self.configs["emojis"][str(i)]
            for i in range(1, num_roles + 1)
        }

        # Create roles if they don't exist
        for role_name in roles_to_emojis.keys():
            if not discord.utils.get(guild.roles, name=role_name):
                try:
                    self.logger.debug(f"Creating role: {role_name}")
                    await guild.create_role(name=role_name)
                except Exception as error:
                    self.logger.error(
                        f"Error creating role: {role_name}",
                        json_data=str(error),
                    )
            else:
                self.logger.warn(f"Role {role_name} already exists.")

        embed = discord.Embed(
            title="Acquire your Discord role here!",
            color=discord.Color.blue(),
        )
        message = await ctx.send(embed=embed)

        # Add reactions to the message
        # Each post has reaction limit of 20
        num_of_post = int(math.floor(num_roles / 20) + 1)

        react_posts = []
        for i in range(1, num_of_post + 1):
            try:
                self.logger.debug(f"Sending react post {i}...")
                embed = discord.Embed(
                    title=f"Group numbers: {20 * (i - 1) + 1} to {min(num_roles, 20 * i)}",
                    color=discord.Color.blue(),
                )
                post = await message.channel.send(embed=embed)
                react_posts.append(post)
            except Exception as error:
                self.logger.error(
                    f"Error sending react post {i + 1}", json_data=str(error)
                )

        # Add reaction to each post (each post has reaction limit of 20)
        self.logger.info("Adding reactions to react post...")

        chunks = []
        for post_num in range(1, num_of_post + 1):
            chunk = {
                str(i): roles_to_emojis.get(f"{self.configs["role_prefix"]}{i}")
                for i in range(
                    20 * (post_num - 1) + 1, min(num_roles, 20 * post_num) + 1
                )
            }
            chunks.append(chunk)

        self.logger.debug(f"Chunks", json_data=chunk)

        for post in react_posts:
            chunk_no = react_posts.index(post) + 1
            try:
                emoji_dict = chunks[chunk_no - 1]
                for emoji, role in emoji_dict.items():
                    self.logger.debug(
                        f"Adding reaction {emoji}, {role} to post {post.id}",
                    )
                    await post.add_reaction(role)
            except Exception as error:
                self.logger.error("Error adding reactions", json_data=str(error))

        # Save the message ID for tracking reactions
        with open("message_id.txt", "w+", encoding="utf-8") as f:
            f.write(str(message.id) + ",")  # Message ID of the initial post
            f.write(
                ",".join(str(post.id) for post in react_posts)
            )  #  Follow by react post IDs separated by commas
            f.write("\n")  # New line
            f.write(str(message.channel.id))  # Channel ID in the second line
            f.write("\n")  # New line
            f.write(str(num_roles))  # Number of roles in the third line
            f.close()  # Close the file

        self.logger.info("Role acquisition posts completed!")

    # TODO:
    # async def assign_roles_to_groups(self, ctx, roles):

    @commands.hybrid_command(name="clearroles", with_app_command=True)
    @commands.has_any_role(conf["admin_role"])
    async def clear_roles(
        self,
        ctx,
        start: int = 1,
        end: int = conf["max_roles"],
        prefix: str = conf["role_prefix"],
    ):
        self.logger.info(f"Clearing roles...")

        guild = ctx.guild
        try:
            for i in range(start, end + 1):
                # Remove all special symbols using regex
                role_name = f"{prefix}{i}"

                role = discord.utils.get(guild.roles, name=f"{role_name}")
                if role is not None:
                    self.logger.debug(f"Removing role {role.name}")
                    await role.delete()
                else:
                    self.logger.warn(f"Role {role_name} not found.")

        except Exception as error:
            self.logger.error("Error clearing roles", json_data=str(error))


class RoleGroupChatCommands(commands.Cog):

    def __init__(self, bot, logger, configs=None, flags=None):
        if bot is None or logger is None:
            raise ValueError("bot and logger are required")

        self.bot = bot
        self.logger = logger
        if configs is not None:
            self.configs = configs
        else:
            self.configs = default_configs()
        if flags is not None:
            self.flags = flags
        else:
            self.flags = default_flags()

    @commands.command(
        name="createchat",
    )
    @commands.has_any_role(conf["admin_role"])
    async def create_group_chat(self, ctx, clear_all: bool = False):
        guild = ctx.guild

        try:
            current_num_roles = read_message_txt(dict=True).get("current_role_num")

            # Check if no roles is created prior
            if current_num_roles is None:
                await ctx.send("No roles found. Create role first!")
                return

            # If chat number is lower than limit
            if current_num_roles < self.configs["min_roles"]:
                await ctx.send("Minimum number of roles is 3.")
                return

            # If chat number is higher than limit
            if current_num_roles > self.configs["max_roles"]:
                await ctx.send("Maximum number of roles is 63.")
                return

            # If remove all existing channel flag is set
            if clear_all:
                self.logger.info("Removing existing group channels...")
                await self.clear_channel(
                    ctx,
                    start=1,
                    end=current_num_roles,
                    clear_txt=False,
                    prefix=self.configs["group_prefix"],
                )

        except Exception as error:
            self.logger.error(
                "Error in pre-setup of group chat setup", json_data=str(error)
            )
            return

        self.logger.info("Setting up group chat...")

        # List of categories for second retry
        unsuccessful = []  # List of unsuccessful categories creation
        for i in range(1, int(current_num_roles) + 1):
            try:
                # Create category
                category_name = f"{self.configs['group_prefix']}{i}"
                if len(str(i)) == 1:  # If it is one digit, add a 0 in front
                    category_name = f"{self.configs['group_prefix']}0{i}"

                new_category = discord.utils.get(guild.categories, name=category_name)

                if not new_category:
                    self.logger.debug(f"Creating category: {category_name}")
                    await guild.create_category(name=category_name)
                else:
                    self.logger.warn(f"Category {category_name} already exists.")

                # Check if can be fetched
                if new_category:
                    # Create text and voice channel
                    text_name = f"{self.configs['group_prefix']}{i}"
                    if len(str(i)) == 1:  # If it is one digit, add a 0 in front
                        text_name = f"{self.configs['group_prefix']}0{i}"
                    voice_name = f"{self.configs['group_prefix']}{i}"
                    if len(str(i)) == 1:  # If it is one digit, add a 0 in front
                        voice_name = f"{self.configs['group_prefix']}0{i}"
                    self.logger.debug(
                        f"Creating text channel {text_name} and voice channel {voice_name} in category",
                    )
                    await guild.create_text_channel(text_name, category=new_category)
                    await guild.create_voice_channel(voice_name, category=new_category)

                    # Set permissions for new category
                    student_role = discord.utils.get(
                        guild.roles, name=f"{self.configs['role_prefix']}{i}"
                    )
                    ta_role = discord.utils.get(guild.roles, name="TA")

                    self.logger.debug(
                        f"Setting permissions for category {new_category.name}",
                    )
                    await new_category.set_permissions(
                        guild.default_role, read_messages=False, connect=False
                    )
                    await new_category.set_permissions(
                        student_role, read_messages=True, connect=True
                    )
                    await new_category.set_permissions(
                        ta_role, read_messages=True, connect=True
                    )
                else:
                    self.logger.warn(f"Category {category_name} not found.")
                    unsuccessful.append(category_name)

            except Exception as error:
                self.logger.error(
                    f"Error creating group channels", json_data=str(error)
                )

        await ctx.send("Group chat setup complete!")
        self.logger.info("Group chat setup complete!")
        self.logger.warn(f"Unsuccessful categories: {unsuccessful}")

    @commands.command(name="clearchannel")
    @commands.has_any_role(conf["admin_role"])
    async def clear_channel(
        self,
        ctx,
        start: int = 1,
        end: int = conf["max_roles"],
        clear_txt: bool = False,
        prefix: str = conf["group_prefix"],
    ):
        guild = ctx.guild

        self.logger.info("Clearing channels...")

        try:
            for i in range(start, end + 1):
                # If it is one digit, add a 0 in front
                text_name = f"{prefix}{i}"
                if len(str(i)) == 1:
                    text_name = f"{prefix}0{i}"

                # Remove all special symbols using regex
                # text_name = re.sub(r"[^a-zA-Z0-9]", "", text_name)

                # Make text name lowercase
                text_name = text_name.lower()

                text = discord.utils.get(guild.text_channels, name=f"{text_name}")
                if text is not None:
                    self.logger.debug(f"Removing text channels {text.name}")
                    await text.delete()
                else:
                    self.logger.warn(f"Text channel {text_name} not found.")

                # If it is one digit, add a 0 in front
                voice_name = f"{prefix}{i}"
                if len(str(i)) == 1:
                    voice_name = f"{prefix}0{i}"
                voice = discord.utils.get(guild.voice_channels, name=f"{voice_name}")
                if voice is not None:
                    self.logger.debug(f"Removing role's voice channels {voice.name}")
                    await voice.delete()
                else:
                    self.logger.warn(f"Voice channel {voice_name} not found.")

                # If it is one digit, add a 0 in front
                category_name = f"{prefix}{i}"
                if len(str(i)) == 1:
                    category_name = f"{prefix}0{i}"
                category = discord.utils.get(guild.categories, name=f"{category_name}")
                if category is not None:
                    self.logger.debug(f"Removing category {category.name}")
                    await category.delete()
                else:
                    self.logger.warn(f"Category {category_name} not found.")

        except Exception as error:
            self.logger.info(f"[b red] Error clearing channels - {error}")

        # Clear message text
        if clear_txt is True:
            with open("message_id.txt", "w+", encoding="utf-8") as f:
                f.write("")
