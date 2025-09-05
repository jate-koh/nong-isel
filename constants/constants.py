import os
import sys
from rich import print

try:
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    guild_id = os.getenv("GUILD_ID")

except Exception as error:
    print(f"[b red] Error loading environment variables!")
    sys.exit()

def_configs = {
    "token": token,
    "guild_id": guild_id,
    "admin_role": "Admin",
    "staff_role": [],
    "guest_role": "Guest",
    "role_prefix": "G",
    "group_prefix": "G-",
    "min_roles": 3,
    "max_roles": 63,
    "prefix": "!",
    "qna_channel": None,
    "qna_category": None,
    "emojis": {},
    "gmt": 7,
}

def_flags = {
    "enable_testing": False,
    "disable_dm": False,
    "disable_role_assign": False,
    "disable_role_react": False,
}

def_path = {
    "logs_dir": "./logs/bot.log",
    "debugs_dir": "./logs/debug.log",
    "db_dir": "./database/bot.sqlite",
}


def default_configs():
    return def_configs


def default_flags():
    return def_flags


def default_path():
    return def_path
