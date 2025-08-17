import os
import sys
import json
from rich import print

try:
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    guild_id = os.getenv("GUILD_ID")
    qna_channel = os.getenv("QNA_CHANNEL")
    qna_category = os.getenv("QNA_CATEGORY")

except Exception as error:
    print(f"[b red] Error loading environment variables!")
    sys.exit()

if token == None or guild_id == None:
    print(f"[b red] Environment variables are missing!")
    sys.exit()


with open("./assets/emoji-cp.json", "r") as file:
    try:
        emojis = json.load(file)
    except json.JSONDecodeError as e:
        print(f"[b red] Error loading emojis JSON: {e}")
        sys.exit()
    except FileNotFoundError as e:
        print(f"[b red] File not found: {e}")
        sys.exit()
    except Exception as e:
        print(f"[b red] An unexpected error occurred: {e}")
        sys.exit()
    finally:
        file.close()

package = {"version": "1.0", "author": "CU-ISEL", "name": "nong-isel"}

configs = {
    "token": token,
    "guild_id": guild_id,
    "admin_role": "TA-Grad",
    "staff_role": ["TA"],
    "guest_role": "anonymous",
    "role_prefix": "G",
    "group_prefix": "Group-",
    "min_roles": 3,
    "max_roles": 63,
    "prefix": "!",
    "qna_channel": qna_channel,
    "qna_category": qna_category,
    "emojis": emojis,
}

test_flags = {
    "enable_testing": False,
    "disable_dm": True,
    "disable_role_assign": True,
    "disable_role_react": True,
}
