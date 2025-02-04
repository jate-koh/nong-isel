from states import ErrorState, GeneralState, RoleState, MessagesState
from constants import default_configs, default_flags
from utilities import get_logger


async def setup(bot, configs=None, flags=None):

    logger = get_logger(module="States")
    logger.info("Loading states...")

    if bot is None:
        logger.error("No bot is provided")
        raise ValueError("No bot is provided.")

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

    try:
        # Cores
        await bot.add_cog(ErrorState(bot))
        await bot.add_cog(
            GeneralState(
                bot=bot,
                logger=logger,
            )
        )

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
                logger=logger,
                configs=configs,
                flags=flags,
            )
        )

    except Exception as error:
        logger.error("Error loading states cog", json_data=str(error))
