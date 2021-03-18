# global_data.py

import os
import logging
import logging.handlers

# Get bot directory
bot_dir = os.path.dirname(__file__)

# Databases
dbfile = os.path.join(bot_dir, 'database/erg_db.db')
default_dbfile = os.path.join(bot_dir, 'database/erg_db_default.db')

# Pictures
thumbnail = os.path.join(bot_dir, 'images/erg.png')
dungeon11 = os.path.join(bot_dir, 'images/dungeon11.png')
dungeon13 = os.path.join(bot_dir, 'images/dungeon13.png')

# Prefix
default_prefix = '$'

# Embed color
color = 8983807

# Set default footer
async def default_footer(prefix):
    footer = f'Use {prefix}guide or {prefix}g to see all available guides.'
    
    return footer

# Open error log file, create if it not exists
logfile = os.path.join(bot_dir, 'logs/discord.log')
if not os.path.isfile(logfile):
    open(logfile, 'a').close()

# Initialize logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.handlers.TimedRotatingFileHandler(filename=logfile,when='D',interval=1, encoding='utf-8', utc=True)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)