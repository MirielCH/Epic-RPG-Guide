# settings.py

import os

from dotenv import load_dotenv


# Read tokens
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DBL_TOKEN = os.getenv('DBL_TOKEN')
if DBL_TOKEN == 'none': DBL_TOKEN = None
DEBUG_MODE = True if os.getenv('DEBUG_MODE') == 'ON' else False

# Get bot directory
BOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
DB_FILE = os.path.join(BOT_DIR, 'database/erg_db.db')
DEFAULT_DB_FILE = os.path.join(BOT_DIR, 'database/erg_db_default.db')
LOG_FILE = os.path.join(BOT_DIR, 'logs/discord.log')

# User & server IDs
OWNER_ID = 619879176316649482
DEV_IDS = [OWNER_ID, 692796548282712074]
DEV_GUILDS = [730115558766411857,812650049565753355,774590797214515201] # Secret Valley, Charivari, Support server

# Pictures
IMG_THUMBNAIL = os.path.join(BOT_DIR, 'images/erg.png')
IMG_DUNGEON_11 = os.path.join(BOT_DIR, 'images/dungeon11.png')
IMG_DUNGEON_13 = os.path.join(BOT_DIR, 'images/dungeon13.png')
IMG_RASPI = os.path.join(BOT_DIR, 'images/raspi2.png')
IMG_CRANKY = os.path.join(BOT_DIR, 'images/cranky.png')

EPIC_RPG_ID = 555955826880413696
TESTY_ID = 1050765002950332456 # Miriel's test bot to test triggers

EMBED_COLOR = 0x8914FF

ABORT_TIMEOUT = 60

INTERACTION_TIMEOUT = 300