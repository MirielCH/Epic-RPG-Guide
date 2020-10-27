# bot.py
import os
import discord
import sqlite3
import shutil

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound
#from discord.ext.commands import MissingPermissions

# Read the bot token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set default prefix
default_prefix = '$'

# Set name of database files
dbfile = 'erg_db.db'
default_dbfile = 'erg_db_default.db'
#dbfile = os.path.abspath('erg_db.db')
#default_dbfile = os.path.abspath('erg_db_default.db')

# Check if database exists, if not, create empty one
if not os.path.isfile(dbfile):
    shutil.copy(default_dbfile,dbfile)

# Open connection to the local database    
erg_db = sqlite3.connect(dbfile, isolation_level=None)

bot = discord.Client()

# Check database for stored prefix, if none is found, a record is inserted and the default prefix $ is used, return all bot prefixes
def get_prefix_all(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM global_settings where guild_id=?', [message.guild.id,])
    record = cur.fetchone()
    
    if record:
        prefix = record[1]
    else:
        try:
            cur.execute('INSERT INTO global_settings VALUES (?, ?)', (message.guild.id, default_prefix,))
        except sqlite3.Error as error:
            print(f'Error inserting into database.\n{error}')

        prefix = default_prefix
        
    return commands.when_mentioned_or(*prefix)(bot, message)

# Check database for stored prefix, if none is found, the default prefix $ is used, return only the prefix
def get_prefix(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM global_settings where guild_id=?', [message.guild.id,])
    record = cur.fetchone()
    
    if record:
        prefix = record[1]
    else:
        prefix = default_prefix
        
    return prefix

# Set new prefix
def set_prefix(bot, message, new_prefix):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM global_settings where guild_id=?', [message.guild.id,])
    record = cur.fetchone()
    
    if record:
        try:
            cur.execute('UPDATE global_settings SET prefix = ? where guild_id = ?', (new_prefix, message.guild.id,))
        except sqlite3.Error as error:
            print(f'Error updating record in database.\n{error}')           
    else:
        try:
            cur.execute('INSERT INTO global_settings VALUES (?, ?)', (message.guild.id, new_prefix,))
        except sqlite3.Error as error:
            print(f'Error inserting into database.\n{error}')
        

bot = commands.Bot(command_prefix=get_prefix_all)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Suppresses errors if a command is entered that the bot doesn't recognize
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, (commands.MissingPermissions)):
        await ctx.send(f'Sorry, you are not allowed to use this command.')
    raise error

# Command "setprefix" - Sets new prefix (if user has "manage server" permission)
@bot.command()
@commands.has_permissions(manage_guild=True)
async def setprefix(ctx, *new_prefix):
    current_prefix = get_prefix(bot, ctx)
    if new_prefix:
        if len(new_prefix)>1:
            await ctx.send(f'Too many arguments.\nCommand syntax: `{current_prefix}setprefix [prefix]`')
        else:
            set_prefix(bot, ctx, new_prefix[0])
            await ctx.send(f'Prefix changed to `{get_prefix(bot, ctx)}`')
    else:
        await ctx.send(f'Command syntax: `{current_prefix}setprefix [prefix]`')

# Command "prefix" - Returns current prefix
@bot.command()
async def prefix(ctx, *args):
    current_prefix = get_prefix(bot, ctx)
    await ctx.send(f'The prefix for this server is `{current_prefix}`\nTo change the prefix use `{current_prefix}setprefix [prefix]`')
    
bot.run(TOKEN)