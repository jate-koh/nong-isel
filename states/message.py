import discord
import re
from discord.ext import commands
from rich import print
from sonyflake import SonyFlake

sf = SonyFlake()


class MessagesState(commands.Cog):
    def __init__(self, bot, logger, configs=None, flags=None):
        if bot is None or logger is None:
            raise ValueError("bot and logger are required")

        self.bot = bot
        self.logger = logger
        if configs is not None:
            self.configs = configs
        if flags is not None:
            self.flags = flags

    @commands.Cog.listener("on_message")
    async def onQuestionDMs(self, message):

        # Ignore messages from the bot
        if message.author == self.bot.user:
            return

        # Check if message is private
        if message.channel.type == discord.ChannelType.private:
            self.logger.info(f"Direct message received from '{message.author}'")
            guild = self.bot.get_guild(int(self.configs["guild_id"]))

            ############################## TESTING MODE ##############################
            if self.flags["disable_dm"] and self.flags["enable_testing"]:
                embed = discord.Embed(
                    title="Feature Disabled",
                    description="This feature is disabled by hoster.",
                    color=discord.Color.red(),
                )
                await message.reply(embed=embed)
                return
            ##########################################################################

            # Get the member's name for use in the ticket's channel. This is also the part where we enforce regex
            regex_str = re.compile(r"^(\d+)_(\d+)_(.+)$")
            member = guild.get_member(message.author.id)
            if member is None:
                self.logger.error(f"Member {message.author.id} not found in guild.")
                return

            self.logger.info(f"Their server alias is '{member.nick}'")

            # Enforce regex on the nickname
            try:
                matchgroups = regex_str.match(member.nick)
                groupno, studentid, studentname = matchgroups.groups()
            except (
                AttributeError,
                TypeError,
            ):  # .groups() called on a broken match group? user's fault.
                embed = discord.Embed(
                    title="Incorrect name format",
                    description="Please set your nickname according to the format before proceeding: `GroupNo_StudentID_Name`",
                    color=discord.Color.red(),
                )
                await message.reply(embed=embed)
                return

            # Check if author id is in records
            try:
                with open("ticket_id.txt", "r") as f:
                    for line in f:
                        if not line:
                            continue
                        if int(line.split(":")[1]) == int(message.author.id):
                            user_ticket = line.split(":")[0]
                            embed = discord.Embed(
                                title="You already have an open ticket",
                                color=discord.Color.red(),
                            )
                            embed.add_field(
                                name="Ticket ID",
                                value=discord.utils.get(
                                    guild.text_channels,
                                    name=user_ticket,
                                ).mention,
                                inline=False,
                            )
                            await message.reply(embed=embed)
                            return
            except FileNotFoundError:
                self.logger.warning(f"File ticket_id.txt not found.")
            except Exception as error:
                self.logger.error(f"Error reading ticket_id.txt - {error}")
                return

            # Create ticket ID
            ticket_id = sf.next_id()
            self.logger.info(f"Generated new ticket ID: {ticket_id}")

            # Make a relay message to Q&A channel
            try:
                main_qna_channel = self.bot.get_channel(
                    int(self.configs["qna_channel"])
                )
                if main_qna_channel is None:
                    self.logger.error(
                        f"Channel ID {self.configs['qna_channel']} not found."
                    )
                    return

                embed = discord.Embed(
                    title="Questions need responding",
                    description=message.content,
                    color=discord.Color.blue(),
                )
                embed.set_author(
                    name=message.author.name,
                    icon_url=message.author.avatar.url,
                )
                embed.add_field(
                    name="Ticket ID",
                    value=ticket_id,
                    inline=False,
                )
            except Exception as error:
                self.logger.error(
                    f"Error creating message for {self.configs['qna_channel']} - {error}"
                )
                return

            # Define roles for ticket channels
            overwrites = {
                # Deny everyone from seeing the ticket
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                # Allow users to see the ticket
                message.author: discord.PermissionOverwrite(view_channel=True),
                # Allow admins to see the ticket
                discord.utils.get(
                    guild.roles, name=self.configs["admin_role"]
                ): discord.PermissionOverwrite(view_channel=True),
            }

            # Add staff roles to the overwrites roles map
            for role in self.configs["staff_role"]:
                staff_role = discord.utils.get(guild.roles, name=role)
                if staff_role is not None:
                    overwrites[staff_role] = discord.PermissionOverwrite(
                        view_channel=True
                    )
                else:
                    self.logger.warning(f"Role {role} not found.")

            # Create tickets texts in the Q&A categories
            try:
                categories = discord.utils.get(
                    guild.categories,
                    id=int(self.configs["qna_category"]),
                )

                if categories is None:
                    self.logger.error(
                        f"Category ID {self.configs['qna_category']} not found."
                    )
                    return

                channelname = f"{studentid}-{studentname}"

                ticket_text_channel = await categories.create_text_channel(
                    channelname,
                    overwrites=overwrites,
                )

                await ticket_text_channel.move(beginning=True, category=categories)
            except Exception as error:
                self.logger.error(
                    f"Error creating ticket text channel in {self.configs['qna_category']} - {error}"
                )
                return

            # Send a message to the ticket text channel
            try:
                await ticket_text_channel.send(embed=embed)
            except Exception as error:
                self.logger.error(
                    f"Error sending message to {ticket_text_channel.name} - {error}"
                )
                return

            embed.add_field(
                name="Ticket Channel",
                value=ticket_text_channel.mention,
                inline=False,
            )

            # Send a message to the Q&A channel
            try:
                await main_qna_channel.send(embed=embed)
            except Exception as error:
                self.logger.error(
                    f"Error sending message to {main_qna_channel.name} - {error}"
                )
                return

            # Inform the user of the ticket channel in DMs
            try:
                embed = discord.Embed(
                    title="Response channel has been created",
                    description=f"You may continue your conversation at {ticket_text_channel.mention}",
                    color=discord.Color.green(),
                )
                embed.add_field(
                    name="Ticket ID",
                    value=ticket_id,
                    inline=False,
                )
                embed.add_field(
                    name="Ticket Channel",
                    value=ticket_text_channel.mention,
                    inline=False,
                )
                await message.reply(embed=embed)
            except Exception as error:
                self.logger.error(
                    f"Error sending DM to {message.author.name} - {error}"
                )
                return

            # Append ticket ID to records
            try:
                with open("ticket_id.txt", "a") as f:
                    f.write(f"{ticket_id}:{message.author.id}\n")
                    f.close()

                self.logger.info(
                    f"Ticket ID {ticket_id} from {message.author.id} ({message.author.name}) appended to ticket_id.txt"
                )
            except Exception as error:
                self.logger.error(
                    f"Error appending ticket ID to ticket_id.txt - {error}"
                )
                return
