import os
import discord
from discord.ext import commands
from settings import configs

from rich import print


class RolesAssign(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setuproles", aliases=["rolesetup", "setuprole"])
    async def setup_role(self, ctx, max_roles: int = 3):

        # If the file message_id.txt exists on directory
        if os.path.exists("message_id.txt"):
            try:
                # Open the message ID file, read first line
                print(f"[b green] Deleting existing message...")

                with open("message_id.txt", "r") as f:
                    string = f.read()

                # split the string into channel ID and message ID with '\n'
                message_id, channel_id = string.split("\n")

                # If no message ID, return
                if message_id:
                    print(f"[b yellow] Existing message found in local text.")

                    channel = self.bot.get_channel(int(channel_id))
                    if channel:
                        message = await channel.fetch_message(int(message_id))
                        await message.delete()
                        print(f"[b green] Existing message deleted.")
                else:
                    print(f"[b green] No existing message found.")
            except Exception as error:
                print(f"[b red] Error deleting message - {error}")

        print(f"[b green] Setting up roles assignment post...")
        guild = ctx.guild

        if max_roles > 63:
            await ctx.send("Maximum number of roles is 63.")
            return

        if max_roles < 3:
            await ctx.send("Minimum number of roles is 3.")
            return

        roles_to_emojis = {
            str(i): configs["emojis"][str(i)] for i in range(1, max_roles + 1)
        }

        # Create roles if they don't exist
        for role_name in roles_to_emojis.keys():
            if not discord.utils.get(guild.roles, name=role_name):
                try:
                    print(f"[b green] Creating role: {role_name}")
                    await guild.create_role(name=role_name)
                except Exception as error:
                    print(f"[b red] Error creating role: {role_name} - {error}")

        # Send a message for users to react to
        description = "\n".join(
            [f"{emoji} - Role {name}" for name, emoji in roles_to_emojis.items()]
        )
        embed = discord.Embed(
            title="Role Assignment", description=description, color=discord.Color.blue()
        )
        message = await ctx.send(embed=embed)

        try:
            print("[b green] Adding reactions...")
            # Add reactions to the message
            for emoji in roles_to_emojis.values():
                await message.add_reaction(emoji)
        except Exception as error:
            print(f"[b red] Error adding reactions - {error}")

        # Save the message ID for tracking reactions
        with open("message_id.txt", "w+") as f:
            f.write(str(message.id))  # Message ID in the first line
            f.write("\n")  # New line
            f.write(str(message.channel.id))  # Channel ID in the second line
            f.close()  # Close the file

        print("[b green] Role Assignment post completed!")


async def setup(bot):
    await bot.add_cog(RolesAssign(bot))
