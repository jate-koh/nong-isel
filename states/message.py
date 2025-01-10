import discord
from discord.ext import commands
from rich import print


class MessagesState(commands.Cog):
    def __init__(self, bot, configs=None, flags=None):
        self.bot = bot
        if configs is not None:
            self.configs = configs
        if flags is not None:
            self.flags = flags

    @commands.Cog.listener("on_message")
    async def onDirectMessage(self, message):

        # Ignore messages from the bot
        if message.author == self.bot.user:
            return

        # Check if message is private
        if message.channel.type == discord.ChannelType.private:
            print(f"[b yellow] Direct message received from {message.author}")

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
