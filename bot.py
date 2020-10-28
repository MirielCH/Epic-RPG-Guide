# bot.py
import os
import discord
import sqlite3
import shutil
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# Read the bot token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set default prefix
default_prefix = '$'

# Set name of database files
dbfile = 'erg_db.db'
default_dbfile = 'erg_db_default.db'

# Check if database exists, if not, create empty one
if not os.path.isfile(dbfile):
    shutil.copy(default_dbfile,dbfile)

# Open connection to the local database    
erg_db = sqlite3.connect(dbfile, isolation_level=None)

bot = discord.Client()

# Check database for stored prefix, if none is found, a record is inserted and the default prefix $ is used, return all bot prefixes
def get_prefix_all(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM settings_guild where guild_id=?', (message.guild.id,))
    record = cur.fetchone()
    
    if record:
        prefix = record[1]
    else:
        try:
            cur.execute('INSERT INTO settings_guild VALUES (?, ?)', (message.guild.id, default_prefix,))
        except sqlite3.Error as error:
            print(f'Error inserting into database.\n{error}')

        prefix = default_prefix
        
    return commands.when_mentioned_or(*prefix)(bot, message)

# Check database for stored prefix, if none is found, the default prefix $ is used, return only the prefix
def get_prefix(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM settings_guild where guild_id=?', (message.guild.id,))
    record = cur.fetchone()
    
    if record:
        prefix = record[1]
    else:
        prefix = default_prefix
        
    return prefix

# Set new prefix
def set_prefix(bot, message, new_prefix):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM settings_guild where guild_id=?', (message.guild.id,))
    record = cur.fetchone()
    
    if record:
        try:
            cur.execute('UPDATE settings_guild SET prefix = ? where guild_id = ?', (new_prefix, message.guild.id,))
        except sqlite3.Error as error:
            print(f'Error updating record in database.\n{error}')           
    else:
        try:
            cur.execute('INSERT INTO settings_guild VALUES (?, ?)', (message.guild.id, new_prefix,))
        except sqlite3.Error as error:
            print(f'Error inserting into database.\n{error}')
      
bot = commands.Bot(command_prefix=get_prefix_all)

# Check database for stored progress settings, if none is found, the default settings TT0 and not ascended are saved and used, return both
def get_settings(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM settings_user where user_id=?', (message.author.id,))
    record = cur.fetchone()
    
    if record:
        current_settings = (record[1], record[2])
    else:
        try:
            cur.execute('INSERT INTO settings_user VALUES (?, ?, ?)', (message.author.id, '0', 'false',))
            current_settings = get_settings(bot, message)
        except sqlite3.Error as error:
            print(f'Error inserting into database.\n{error}')    
  
    return current_settings

# Set progress settings
def set_progress(bot, message, new_tt, new_ascended):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM settings_user where user_id=?', (message.author.id,))
    record = cur.fetchone()
    
    if record:
        try:
            cur.execute('UPDATE settings_user SET timetravel = ?, ascended = ? where user_id = ?', (new_tt, new_ascended, message.author.id,))
        except sqlite3.Error as error:
            print(f'Error updating record in database.\n{error}')           
    else:
        try:
            cur.execute('INSERT INTO settings_user VALUES (?, ?, ?)', (message.author.id, new_tt, new_ascended,))
        except sqlite3.Error as error:
            print(f'Error inserting into database.\n{error}')

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

# Command "settings" - Returns current user progress settings
@bot.command()
async def settings(ctx, *args):
    current_settings = get_settings(bot, ctx)
    if current_settings[1] == 'true':
        current_ascension = 'ascended'
    else:
        current_ascension = 'not ascended'
    await ctx.send(f'You are currently set as TT{current_settings[0]}, {current_ascension}.')
    
# Command "setprogress" - Sets TT and ascension
@bot.command()
async def setprogress(ctx, *args):
    
    def check(m):
        return m.author == ctx.author
    
    try:
        await ctx.send('What TT are you currently in? `[0-999]`')
        answer_tt = await bot.wait_for('message', check=check, timeout = 30)
        try:            
            if 0 <= int(answer_tt.content) <= 999:
                new_tt = int(answer_tt.content)
                await ctx.send('Are you ascended? `[yes/no]`')
                answer_ascended = await bot.wait_for('message', check=check, timeout=30)
                if answer_ascended.content.lower() in ['yes','y']:
                    new_ascended = 'true'         
                    set_progress(bot, ctx, new_tt, new_ascended)  
                    current_settings = get_settings(bot, ctx)
                    if current_settings[1] == 'true':
                        current_ascension = 'ascended'
                    else:
                        current_ascension = 'not ascended'
                    await ctx.send(f'Settings changed, you are now set as TT{current_settings[0]}, {current_ascension}.')     
                elif answer_ascended.content.lower() in ['no','n']:
                    new_ascended = 'false'
                    set_progress(bot, ctx, new_tt, new_ascended)        
                    current_settings = get_settings(bot, ctx)
                    if current_settings[1] == 'true':
                        current_ascension = 'ascended'
                    else:
                        current_ascension = 'not ascended'
                    await ctx.send(f'Settings changed, you are now set as TT{current_settings[0]}, {current_ascension}.')     
                else:
                    await ctx.send('Please answer with `yes` or `no`. Aborting.')
            else:
                await ctx.send('Please enter a number from 0 to 999. Aborting.')
        except:
            await ctx.send('Please answer with a valid number. Aborting.')  
    except asyncio.TimeoutError as error:
        await ctx.send('You took too long to answer. Aborting.')

bot.run(TOKEN)