# bot.py
import os
import discord
import sqlite3
import shutil
import asyncio
import dungeons
import global_data

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# Read the bot token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set name of database files
dbfile = global_data.dbfile
default_dbfile = global_data.default_dbfile

# Check if database exists, if not, create empty one
if not os.path.isfile(dbfile):
    shutil.copy(default_dbfile,dbfile)

# Open connection to the local database    
erg_db = sqlite3.connect(dbfile, isolation_level=None)

bot = discord.Client()

# Check database for stored prefix, if none is found, a record is inserted and the default prefix $ is used, return all bot prefixes
async def get_prefix_all(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM settings_guild where guild_id=?', (message.guild.id,))
    record = cur.fetchone()
    
    if record:
        prefix = record[1]
    else:
        try:
            cur.execute('INSERT INTO settings_guild VALUES (?, ?)', (message.guild.id, global_data.default_prefix,))
        except sqlite3.Error as error:
            print(f'Error inserting into database.\n{error}')

        prefix = global_data.default_prefix
        
    return commands.when_mentioned_or(* prefix)(bot, message)

# Check database for stored prefix, if none is found, the default prefix $ is used, return only the prefix
async def get_prefix(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM settings_guild where guild_id=?', (message.guild.id,))
    record = cur.fetchone()
    
    if record:
        prefix = record[1]
    else:
        prefix = global_data.default_prefix
        
    return prefix

async def get_dungeon_data(dungeon):
    cur=erg_db.cursor()
    cur.execute('SELECT dungeons.*, g1.emoji, g2.emoji FROM dungeons INNER JOIN gear g1 ON g1.name = dungeons.player_sword_name INNER JOIN gear g2 ON g2.name = dungeons.player_armor_name WHERE dungeons.dungeon=?', (dungeon,))
    record = cur.fetchone()
    
    if record:
        dungeon_data = record
    else:
        print('Error while getting dungeon data.')
        
    return dungeon_data

# Set new prefix
async def set_prefix(bot, message, new_prefix):
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
      
# Check database for stored progress settings, if none is found, the default settings TT0 and not ascended are saved and used, return both
async def get_settings(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM settings_user where user_id=?', (message.author.id,))
    record = cur.fetchone()
    
    if record:
        current_settings = (record[1], record[2])
    else:
        try:
            cur.execute('INSERT INTO settings_user VALUES (?, ?, ?)', (message.author.id, '0', 'not ascended',))
            await first_time_user(bot, message)
            return
        except sqlite3.Error as error:
            print(f'Error inserting into database.\n{error}')    
  
    return current_settings

# Welcome message to inform the user of his/her initial settings
async def first_time_user(bot, message):
    current_settings = await get_settings(bot, message)
    await message.send(f'Hey there, **{message.author.name}**. Looks like we haven\'t met before.\nI have set your progress to '\
                f'**TT{current_settings[0]}**, **{current_settings[1]}**.\n'\
                f'If I guessed wrong, please use `setprogress` to change your settings.')

# Set progress settings
async def set_progress(bot, message, new_tt, new_ascended):
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

bot = commands.Bot(command_prefix=get_prefix_all)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Suppresses errors if a command is entered that the bot doesn't recognize
#@bot.event
#async def on_command_error(ctx, error):
 #   if isinstance(error, CommandNotFound):
  #      return
  #  elif isinstance(error, (commands.MissingPermissions)):
   #     await ctx.send(f'Sorry **{ctx.author.name}**, you are not allowed to use this command.')

# Command "setprefix" - Sets new prefix (if user has "manage server" permission)
@bot.command()
@commands.has_permissions(manage_guild=True)
async def setprefix(ctx, *new_prefix):
    if new_prefix:
        if len(new_prefix)>1:
            await ctx.send(f'Too many arguments.\nCommand syntax: `setprefix [prefix]`')
        else:
            await set_prefix(bot, ctx, new_prefix[0])
            await ctx.send(f'Prefix changed to `{await get_prefix(bot, ctx)}`')
    else:
        await ctx.send(f'Command syntax: `setprefix [prefix]`')

# Command "prefix" - Returns current prefix
@bot.command()
async def prefix(ctx):
    current_prefix = await get_prefix(bot, ctx)
    await ctx.send(f'The prefix for this server is `{current_prefix}`\nTo change the prefix use `setprefix [prefix]`')

# Command "settings" - Returns current user progress settings
@bot.command()
async def settings(ctx):
    current_settings = await get_settings(bot, ctx)
    await ctx.send(f'**{ctx.author.name}**, your progress is currently set to **TT{current_settings[0]}**, **{current_settings[1]}**.\n'\
        f'Use `setprogress` if you want to change your settings.')
    
# Command "setprogress" - Sets TT and ascension
@bot.command()
async def setprogress(ctx):
    
    def check(m):
        return m.author == ctx.author
    
    try:
        await ctx.send(f'**{ctx.author.name}**, what TT are you currently in? `[0-999]`')
        answer_tt = await bot.wait_for('message', check=check, timeout = 30)
        try:            
            if 0 <= int(answer_tt.content) <= 999:
                new_tt = int(answer_tt.content)
                await ctx.send(f'**{ctx.author.name}**, are you ascended? `[yes/no]`')
                answer_ascended = await bot.wait_for('message', check=check, timeout=30)
                if answer_ascended.content.lower() in ['yes','y']:
                    new_ascended = 'ascended'         
                    await set_progress(bot, ctx, new_tt, new_ascended)  
                    current_settings = await get_settings(bot, ctx)
                    await ctx.send(f'Alright **{ctx.author.name}**, your progress is now set to **TT{current_settings[0]}**, **{current_settings[1]}**.')     
                elif answer_ascended.content.lower() in ['no','n']:
                    new_ascended = 'not ascended'
                    await set_progress(bot, ctx, new_tt, new_ascended)        
                    current_settings = await get_settings(bot, ctx)
                    await ctx.send(f'Alright **{ctx.author.name}**, your progress is now set to **TT{current_settings[0]}**, **{current_settings[1]}**.')     
                else:
                    await ctx.send(f'**{ctx.author.name}**, please answer with `yes` or `no`. Aborting.')
            else:
                await ctx.send(f'**{ctx.author.name}**, please enter a number from 0 to 999. Aborting.')
        except:
            await ctx.send(f'**{ctx.author.name}**, please answer with a valid number. Aborting.')  
    except asyncio.TimeoutError as error:
        await ctx.send(f'**{ctx.author.name}**, you took too long to answer. Aborting.')

# Aliases: @commands.command(aliases=['testcommand', 'testing'])

# Dungeon 5
@bot.command()
async def d5(ctx):
    dungeon_data = await get_dungeon_data(5)
    dungeon_embed = await dungeons.dungeon(dungeon_data)
    
    await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])

bot.run(TOKEN)