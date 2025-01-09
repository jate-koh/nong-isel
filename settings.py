import os
import discord
from rich import print

try:
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    guild_id = os.getenv("GUILD_ID")
except:
    print(f"[b red] Error loading environment variables!")
    exit()

if token == None or guild_id == None:
    print(f"[b red] Environment variables are missing!")
    exit()

package = {"version": "1.0", "author": "CU-ISEL", "name": "nong-isel"}

configs = {
    "token": token,
    "guild_id": guild_id,
    "admin_role": "TA Grad",
    "guest_role": "anonymous",
    "role_prefix": "G",
    "group_prefix": "Group-",
    "min_roles": 3,
    "max_roles": 63,
    "prefix": "!",
    "qna_channel": "1326000721350492215",
    "emojis": {
        "0": "<:00:1319603401834627082>",
        "1": "<:01:1319603438358630400>",
        "2": "<:02:1319603448936923136>",
        "3": "<:03:1319603460936564757>",
        "4": "<:04:1319603470507966574>",
        "5": "<:05:1319603480532615219>",
        "6": "<:06:1319603491509112915>",
        "7": "<:07:1319603501705461770>",
        "8": "<:08:1319603513541787648>",
        "9": "<:09:1319603531270979645>",
        "10": "<:10:1319603542465712149>",
        "11": "<:11:1319603555123855390>",
        "12": "<:12:1319603567920676896>",
        "13": "<:13:1319603577248809010>",
        "14": "<:14:1319603587361542194>",
        "15": "<:15:1319603601936748574>",
        "16": "<:16:1319603616646168660>",
        "17": "<:17:1319603629392662569>",
        "18": "<:18:1319603643175010314>",
        "19": "<:19:1319603656676479018>",
        "20": "<:20:1319603668705869855>",
        "21": "<:21:1319603682228174858>",
        "22": "<:22:1319603694580404284>",
        "23": "<:23:1319603709134508042>",
        "24": "<:24:1319603722325725194>",
        "25": "<:25:1319603738649825321>",
        "26": "<:26:1319603756710625340>",
        "27": "<:27:1319603772170833931>",
        "28": "<:28:1319603785022046261>",
        "29": "<:29:1319603801325305897>",
        "30": "<:30:1319603819289776148>",
        "31": "<:31:1319603833462325269>",
        "32": "<:32:1319603849534898216>",
        "33": "<:33:1319603862436450324>",
        "34": "<:34:1319603879075119124>",
        "35": "<:35:1319603896531816448>",
        "36": "<:36:1319603913388720178>",
        "37": "<:37:1319603929666814002>",
        "38": "<:38:1319603946767257680>",
        "39": "<:39:1319603987711787118>",
        "40": "<:40:1319604002190790738>",
        "41": "<:41:1319604016631517194>",
        "42": "<:42:1319604034784727063>",
        "43": "<:43:1319604052555726898>",
        "44": "<:44:1319604094230466580>",
        "45": "<:45:1319604118683390024>",
        "46": "<:46:1319604142808895488>",
        "47": "<:47:1319604179093946378>",
        "48": "<:48:1319604197410213908>",
        "49": "<:49:1319604216809127986>",
        "50": "<:50:1319604233766699068>",
        "51": "<:51:1319604256260751401>",
        "52": "<:52:1319604273939742761>",
        "53": "<:53:1319604290351792210>",
        "54": "<:54:1319604305614864465>",
        "55": "<:55:1319604321444167710>",
        "56": "<:56:1319604337986633771>",
        "57": "<:57:1319604353912410162>",
        "58": "<:58:1319604378742558762>",
        "59": "<:59:1319604395909971969>",
        "60": "<:60:1319604411202277387>",
        "61": "<:61:1319604423940636702>",
        "62": "<:62:1319604435755995227>",
        "63": "<:63:1319604449043415041>",
    },
}

test_flags = {
    "enable_testing": True,
    "disable_dm": True,
    "disable_role_assign": True,
    "disable_role_react": True,
}
