# global_data.py

import os

# Get bot directory
bot_dir = os.path.dirname(__file__)

# Databases
dbfile = os.path.join(bot_dir, 'erg_db.db')
default_dbfile = os.path.join(bot_dir, 'erg_db_default.db')

# Pictures
thumbnail = os.path.join(bot_dir, 'images/erg.png')

# Prefix
default_prefix = '$'

# Embed color
color = 8983807

# Set default footer
async def default_footer(prefix):
    footer = f'Use {prefix}guide or {prefix}g to see all available guides.'
    
    return footer

# Error log file
logfile = os.path.join(bot_dir, 'logs/discord.log')