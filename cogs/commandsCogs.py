from rich import print

from constants import default_configs, default_flags
from commands import InfoCommand, RoleGroupChatCommands, RoleGroupCommands


async def setup(bot, configs=None, flags=None):
    print(f"[b green] Loading commands...")

    if flags is not None:
        print(f"[b yellow] Flags are set: {flags}")
    else:
        print(f"[b yellow] Using default flags for Commands Cogs.")
        flags = default_flags()

    if configs is not None:
        valid = {
            valid_key: configs[valid_key]
            for valid_key in configs.keys()
            if valid_key not in ["token", "guild_id", "emojis"]
        }
        valid["emojis"] = f"{str(len(configs["emojis"]))} emojis"
        print(f"[b yellow] Configs are set for Commands Cogs: {valid}")
    else:
        print(f"[b yellow] Using default configs for Commands Cogs.")
        configs = default_configs()

    try:
        # Roles Commands
        await bot.add_cog(
            RoleGroupCommands(
                bot=bot,
                configs=configs,
                flags=flags,
            )
        )
        await bot.add_cog(
            RoleGroupChatCommands(
                bot=bot,
                configs=configs,
                flags=flags,
            )
        )

        # Informations Commands
        await bot.add_cog(InfoCommand(bot))

    except Exception as error:
        print(f"[b red] Error loading commands - {error}")
