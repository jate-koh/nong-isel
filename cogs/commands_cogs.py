from constants import default_configs, default_flags
from commands import InfoCommands, RoleGroupChatCommands, RoleGroupCommands
from utilities import get_logger


async def setup(bot, configs=None, flags=None):

    logger = get_logger(module="Commands")
    logger.info("Loading commands...")

    if bot is None:
        logger.error("No bot provided")
        raise ValueError("No bot provided")

    if flags is not None:
        logger.info(f"Flags set.", json_data=flags)
    else:
        logger.warn("Using default flags.")
        flags = default_flags()

    if configs is not None:
        valid = {
            valid_key: configs[valid_key]
            for valid_key in configs.keys()
            if valid_key not in ["token", "guild_id", "emojis"]
        }
        valid["emojis"] = f"{str(len(configs["emojis"]))} emojis"
        logger.info(f"Configs set.", json_data=valid)
    else:
        logger.warn("Using default configs.")
        configs = default_configs()

    # Add cogs and slashes
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
        await bot.add_cog(
            InfoCommands(
                bot=bot,
                logger=logger,
                configs=configs,
            )
        )

    except Exception as error:
        logger.error(f"Error loading commands.", json_data=str(error))
