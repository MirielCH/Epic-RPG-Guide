# global_data.py

# Databases
dbfile = 'erg_db.db'
default_dbfile = 'erg_db_default.db'

# Pictures
thumbnail = './images/erg.png'

# Prefix
default_prefix = '$'

# Embed color
color = 8983807

# Set default footer
async def default_footer(prefix):
    footer = f'Use {prefix}guide or {prefix}g to see all available guides.'
    
    return footer

# Error log file
logfile = './logs/discord.log'