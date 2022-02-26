# settings.py

import os

from dotenv import load_dotenv


# Read tokens
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DBL_TOKEN = os.getenv('DBL_TOKEN')
DEBUG_MODE = True if os.getenv('DEBUG_MODE') == 'ON' else False

# Get bot directory
BOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Databases
DB_FILE = os.path.join(BOT_DIR, 'database/erg_db.db')
DEFAULT_DB_FILE = os.path.join(BOT_DIR, 'database/erg_db_default.db')
LOG_FILE = os.path.join(BOT_DIR, 'logs/discord.log')

# Pictures
IMG_THUMBNAIL = os.path.join(BOT_DIR, 'images/erg.png')
IMG_DUNGEON_11 = os.path.join(BOT_DIR, 'images/dungeon11.png')
IMG_DUNGEON_13 = os.path.join(BOT_DIR, 'images/dungeon13.png')

# Prefix
DEFAULT_PREFIX = '$'

# EPIC RPG user id
EPIC_RPG_ID = 555955826880413696

# Embed color
EMBED_COLOR = 0x8914FF