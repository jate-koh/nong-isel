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
    "guest_role": "Guest",
    "role_prefix": "G",
    "group_prefix": "G-",
    "min_roles": 5,
    "max_roles": 60,
    "prefix": "!",
}

def_flags = {
    "enable_testing": False,
    "disable_dm": False,
    "disable_role_assign": False,
    "disable_role_react": False,
}


def default_configs():
    return def_configs


def default_flags():
    return def_flags
