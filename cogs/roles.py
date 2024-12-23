import os
import re
import math
import discord
from discord.ext import commands

from settings import configs
from utils import read_message_txt

from rich import print


class RoleGroup(commands.Cog):
    """TODO: Find workaround for maximum reactions in a message!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="createroles", aliases=["setuproles", "setuprole", "createrole"]
    )
    async def create_roles(
        self, ctx, num_roles: int = configs["min_roles"], clear_all: bool = False
    ):
        print(f"[b yellow] Running pre-setup...")

        guild = ctx.guild
        try:
            message_id, channel_id, current_num_roles = read_message_txt()

            # Check for exisitng messages
            if message_id is not None:
                print(f"[b yellow] Existing messages found in local text.")

                channel = self.bot.get_channel(channel_id)
                if channel:
                    for id in message_id:
                        print(f"[b yellow] Deleting message {id}")
                        try:
                            message = await channel.fetch_message(id)
                            await message.delete()
                        except discord.NotFound:
                            print(f"[b yellow] Message {id} not found.")
                            pass
            else:
                print(f"[b yellow] No existing messages found.")

            # Check for existing number of roles
            if current_num_roles is not None:
                print(f"[b yellow] Existing number of roles found in local text.")

                if num_roles > configs["max_roles"]:
                    await ctx.send("Maximum number of roles is 63.")
                    return

                if num_roles < configs["min_roles"]:
                    await ctx.send("Minimum number of roles is 3.")
                    return

                if num_roles < current_num_roles:
                    await self.clear_roles(
                        ctx,
                        start=num_roles + 1,
                        end=current_num_roles,
                        prefix=configs["role_prefix"],
                    )

                if clear_all:
                    print(f"[b yellow] Removing all existing roles...")
                    await self.clear_roles(
                        ctx,
                        start=1,
                        end=current_num_roles,
                        prefix=configs["role_prefix"],
                    )
            else:
                print(f"[b yellow] No existing number of roles found.")

        except Exception as error:
            print(f"[b red] Error in preparation for setting up group roles- {error}")
            return

        print(f"[b yellow] Setting up group roles and post for acquiring roles...")

        roles_to_emojis = {
            configs["role_prefix"] + str(i): configs["emojis"][str(i)]
            for i in range(1, num_roles + 1)
        }

        # Create roles if they don't exist
        for role_name in roles_to_emojis.keys():
            if not discord.utils.get(guild.roles, name=role_name):
                try:
                    print(f"[b yellow] Creating role: {role_name}")
                    await guild.create_role(name=role_name)
                except Exception as error:
                    print(f"[b red] Error creating role: {role_name} - {error}")
            else:
                print(f"[b yellow] Role {role_name} already exists.")

        embed = discord.Embed(
            title="Acquire your Discord role here!",
            color=discord.Color.blue(),
        )
        message = await ctx.send(embed=embed)

        # Add reactions to the message
        # Each post has reaction limit of 20
        num_of_post = int(math.floor(num_roles / 20) + 1)

        react_posts = []
        for i in range(1, num_of_post):
            try:
                print(f"[b yellow] Sending react post {i + 1}...")
                embed = discord.Embed(
                    title=f"Group numbers: {20 * (i - 1) + 1} to {min(num_roles, 20 * i)}",
                    color=discord.Color.blue(),
                )
                post = await message.channel.send(embed=embed)
                react_posts.append(post)
            except Exception as error:
                print(f"[b red] Error sending react post {i + 1} - {error}")

        # Add reaction to each post (each post has reaction limit of 20)
        print(f"[b yellow] Adding reactions to react post...")

        chunks = []
        for post_num in range(1, num_of_post):
            chunk = {
                str(i): roles_to_emojis.get(f"{configs["role_prefix"]}{i}")
                for i in range(
                    20 * (post_num - 1) + 1, min(num_roles, 20 * post_num) + 1
                )
            }
            chunks.append(chunk)
        print(chunks)

        for post in react_posts:
            chunk_no = react_posts.index(post) + 1
            try:
                emoji_dict = chunks[chunk_no - 1]
                for emoji, role in emoji_dict.items():
                    print(
                        f"[b yellow] Adding reaction {emoji}, {role} to post {post.id}"
                    )
                    await post.add_reaction(role)
            except Exception as error:
                print(f"[b red] Error adding reactions - {error}")

        # Save the message ID for tracking reactions
        with open("message_id.txt", "w+") as f:
            f.write(str(message.id) + ",")  # Message ID of the initial post
            f.write(
                ",".join(str(post.id) for post in react_posts)
            )  #  Follow by react post IDs separated by commas
            f.write("\n")  # New line
            f.write(str(message.channel.id))  # Channel ID in the second line
            f.write("\n")  # New line
            f.write(str(num_roles))  # Number of roles in the third line
            f.close()  # Close the file

        print("[b green] Role acquisition posts completed!")

    @commands.command(name="clearroles")
    async def clear_roles(
        self,
        ctx,
        start: int = 1,
        end: int = configs["max_roles"],
        prefix: str = configs["role_prefix"],
    ):
        guild = ctx.guild

        print(f"[b yellow] Clearing roles...")

        try:
            for i in range(start, end + 1):
                # Remove all special symbols using regex
                role_name = f"{prefix}{i}"

                role = discord.utils.get(guild.roles, name=f"{role_name}")
                if role is not None:
                    print(f"[b yellow] Removing role {role.name}")
                    await role.delete()
                else:
                    print(f"[b yellow] Role {role_name} not found.")

        except Exception as error:
            print(f"[b red] Error clearing roles - {error}")


class RoleGroupChat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="createchat",
        aliases=[
            "createrolechat" "creategroupchat",
            "setuproleschat",
            "setuprolechat",
            "createroleschat",
        ],
    )
    async def create_group_chat(self, ctx, clear_all: bool = False):
        guild = ctx.guild

        try:
            current_num_roles = read_message_txt(dict=True).get("current_role_num")

            if current_num_roles is None:
                await ctx.send("No roles found. Create role first!")
                return

            if current_num_roles < configs["min_roles"]:
                await ctx.send("Minimum number of roles is 3.")
                return

            if current_num_roles > configs["max_roles"]:
                await ctx.send("Maximum number of roles is 63.")
                return

            if clear_all:
                print(f"[b yellow] Removing existing group channels...")
                await self.clear_channel(
                    ctx,
                    start=1,
                    end=current_num_roles,
                    clear_txt=False,
                    prefix=configs["group_prefix"],
                )

        except Exception as error:
            print(f"[b red] Error in pre-setup of group chat setup - {error}")
            return

        print(f"[b yellow] Setting up group chat...")

        # List of categories for second retry
        unsuccessful = []  # List of unsuccessful categories creation
        for i in range(1, int(current_num_roles) + 1):
            try:
                # Create category
                category_name = f"{configs['group_prefix']}{i}"
                if len(str(i)) == 1:  # If it is one digit, add a 0 in front
                    category_name = f"{configs['group_prefix']}0{i}"

                new_category = discord.utils.get(guild.categories, name=category_name)

                if not new_category:
                    print(f"[b yellow] Creating category: {category_name}")
                    await guild.create_category(name=category_name)
                else:
                    print(f"[b yellow] Category {category_name} already exists.")

                # Check if can be fetched
                if new_category:
                    # Create text and voice channel
                    text_name = f"{configs['group_prefix']}{i}"
                    if len(str(i)) == 1:  # If it is one digit, add a 0 in front
                        text_name = f"{configs['group_prefix']}0{i}"
                    voice_name = f"{configs['group_prefix']}{i}"
                    if len(str(i)) == 1:  # If it is one digit, add a 0 in front
                        voice_name = f"{configs['group_prefix']}0{i}"
                    print(
                        f"[b yellow] Creating text channel {text_name} and voice channel {voice_name} in category"
                    )
                    await guild.create_text_channel(text_name, category=new_category)
                    await guild.create_voice_channel(voice_name, category=new_category)

                    # Set permissions for new category
                    student_role = discord.utils.get(
                        guild.roles, name=f"{configs['role_prefix']}{i}"
                    )
                    ta_role = discord.utils.get(guild.roles, name="TA")

                    print(
                        f"[b yellow] Setting permissions for category {new_category.name}"
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
                    print(f"[b red] Category {category_name} not found.")
                    unsuccessful.append(category_name)

            except Exception as error:
                print(f"[b red] Error creating group channels - {error}")

        await ctx.send("Group chat setup complete!")
        print(f"[b green] Group chat setup complete!")
        print(f"[b yellow] Unsuccessful categories: {unsuccessful}")

    @commands.command(name="clearchannel")
    async def clear_channel(
        self,
        ctx,
        start: int = 1,
        end: int = configs["max_roles"],
        clear_txt: bool = False,
        prefix: str = configs["group_prefix"],
    ):
        guild = ctx.guild

        print(f"[b yellow] Clearing channels...")

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
                    print(f"[b yellow] Removing text channels {text.name}")
                    await text.delete()
                else:
                    print(f"[b yellow] Text channel {text_name} not found.")

                # If it is one digit, add a 0 in front
                voice_name = f"{prefix}{i}"
                if len(str(i)) == 1:
                    voice_name = f"{prefix}0{i}"
                voice = discord.utils.get(guild.voice_channels, name=f"{voice_name}")
                if voice is not None:
                    print(f"[b yellow] Removing role's voice channels {voice.name}")
                    await voice.delete()
                else:
                    print(f"[b yellow] Voice channel {voice_name} not found.")

                # If it is one digit, add a 0 in front
                category_name = f"{prefix}{i}"
                if len(str(i)) == 1:
                    category_name = f"{prefix}0{i}"
                category = discord.utils.get(guild.categories, name=f"{category_name}")
                if category is not None:
                    print(f"[b yellow] Removing category {category.name}")
                    await category.delete()
                else:
                    print(f"[b yellow] Category {category_name} not found.")

        except Exception as error:
            print(f"[b red] Error clearing channels - {error}")

        # write empty message_id.txt
        if clear_txt is True:
            with open("message_id.txt", "w+") as f:
                f.write("")


async def setup(bot):
    await bot.add_cog(RoleGroup(bot))
    await bot.add_cog(RoleGroupChat(bot))
