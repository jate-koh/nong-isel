import discord
from discord.ext import commands
from rich import print
from sonyflake import SonyFlake

sf = SonyFlake()


class MessagesState(commands.Cog):
    def __init__(self, bot, configs=None, flags=None):
        self.bot = bot
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
            print(f"[b yellow] Direct message received from {message.author}")
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

            # Create ticket ID
            ticket_id = sf.next_id()
            print(f"[b yellow] Generated ticket ID: {ticket_id}")

            # Make a relay message to Q&A channel
            try:
                main_qna_channel = self.bot.get_channel(
                    int(self.configs["qna_channel"])
                )
                if main_qna_channel is None:
                    print(
                        f"[b red] Channel ID {self.configs['qna_channel']} not found."
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
                print(
                    f"[b red] Error creating message for {self.configs['qna_channel']} - {error}"
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

            # Create tickets texts in the Q&A categories
            try:
                categories = discord.utils.get(
                    guild.categories,
                    id=int(self.configs["qna_category"]),
                )

                if categories is None:
                    print(
                        f"[b red] Category ID {self.configs['qna_category']} not found."
                    )
                    return

                ticket_text_channel = await categories.create_text_channel(
                    name=ticket_id,
                    overwrites=overwrites,
                )
            except Exception as error:
                print(
                    f"[b red] Error creating ticket text channel in {self.configs['qna_category']} - {error}"
                )
                return

            # Send a message to the ticket text channel
            try:
                await ticket_text_channel.send(embed=embed)
            except Exception as error:
                print(
                    f"[b red] Error sending message to {ticket_text_channel.name} - {error}"
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
                print(
                    f"[b red] Error sending message to {main_qna_channel.name} - {error}"
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
                print(f"[b red] Error sending DM to {message.author.name} - {error}")
                return
