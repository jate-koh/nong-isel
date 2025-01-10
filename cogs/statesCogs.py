from rich import print

from states import ErrorState, GeneralState, RoleState, MessagesState
from constants import default_configs, default_flags


async def setup(bot, configs=None, flags=None):
    print(f"[b green] Loading states...")

    if flags is not None:
        print(f"[b yellow] Flags are set: {flags}")
    else:
        print(f"[b yellow] Using default flags for States Cogs.")
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
        print(f"[b yellow] Using default configs for States Cogs.")
        configs = default_configs()

    try:
        # Cores
        await bot.add_cog(ErrorState(bot))
        await bot.add_cog(GeneralState(bot))

        # Q&A System
        await bot.add_cog(
            MessagesState(
                bot=bot,
                configs=configs,
                flags=flags,
            )
        )

        # Roles Assignment
        await bot.add_cog(
            RoleState(
                bot=bot,
                configs=configs,
                flags=flags,
            )
        )

    except Exception as error:
        print(f"[b red] Error loading states - {error}")
