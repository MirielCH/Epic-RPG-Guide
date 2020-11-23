# bot.py
import os
import discord
import sqlite3
import shutil
import asyncio
import dungeons
import global_data
import emojis
import areas
import trading
import crafting
import professions
import misc
import horses
import pets
import timetravel
import events
import logging
import logging.handlers

from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
from discord.ext.commands import CommandNotFound

# Check if log file exists, if not, create empty one
logfile = global_data.logfile
if not os.path.isfile(logfile):
    open(logfile, 'a').close()

# Initialize logger
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.handlers.TimedRotatingFileHandler(filename=logfile,when='D',interval=1, encoding='utf-8', utc=True)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Read the bot token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set name of database files
dbfile = global_data.dbfile
default_dbfile = global_data.default_dbfile

"""
# Check if database exists, if not, create empty one
if not os.path.isfile(dbfile):
    shutil.copy(default_dbfile,dbfile)
"""

# Open connection to the local database    
erg_db = sqlite3.connect(dbfile, isolation_level=None)

# Initialize bot
bot = discord.Client()

            
# --- Database: Get Data ---

# Check database for stored prefix, if none is found, a record is inserted and the default prefix $ is used, return all bot prefixes
async def get_prefix_all(bot, ctx):
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT * FROM settings_guild where guild_id=?', (ctx.guild.id,))
        record = cur.fetchone()
        
        if record:
            prefix = record[1]
        else:
            cur.execute('INSERT INTO settings_guild VALUES (?, ?)', (ctx.guild.id, global_data.default_prefix,))
            prefix = global_data.default_prefix
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return commands.when_mentioned_or(prefix)(bot, ctx)

# Check database for stored prefix, if none is found, the default prefix $ is used, return only the prefix (returning the default prefix this is pretty pointless as the first command invoke already inserts the record)
async def get_prefix(bot, ctx, guild_join=False):
    
    if guild_join == False:
        guild = ctx.guild
    else:
        guild = ctx
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT * FROM settings_guild where guild_id=?', (guild.id,))
        record = cur.fetchone()
        
        if record:
            prefix = record[1]
        else:
            prefix = global_data.default_prefix
    except sqlite3.Error as error:
        if guild_join == False:
            await log_error(ctx, error)
        else:
            await log_error(ctx, error, True)
        
    return prefix

# Get dungeon data for the dungeon commands
async def get_dungeon_data(ctx, dungeon):
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT dungeons.*, i1.emoji, i2.emoji FROM dungeons INNER JOIN items i1 ON i1.name = dungeons.player_sword_name INNER JOIN items i2 ON i2.name = dungeons.player_armor_name WHERE dungeons.dungeon=?', (dungeon,))
        record = cur.fetchone()
        
        if record:
            dungeon_data = record
        else:
            await log_error(ctx, 'No dungeon data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return dungeon_data

# Get dungeon data for the recommended stats of all dungeons
async def get_rec_stats_data(ctx):
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT d.player_at, d.player_def, d.player_carry_def, d.player_life, d.life_boost_needed, d.player_level, d.dungeon FROM dungeons d')
        record = cur.fetchall()
        
        if record:
            rec_stats_data = record
        else:
            await log_error(ctx, 'No recommended dungeon stats data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return rec_stats_data

# Get dungeon data for the recommended gear of all dungeons
async def get_rec_gear_data(ctx, page):
    
    try:
        cur=erg_db.cursor()
        if page == 1:
            cur.execute('SELECT d.player_sword_name, d.player_sword_enchant, i1.emoji, d.player_armor_name, d.player_armor_enchant, i2.emoji, d.dungeon FROM dungeons d INNER JOIN items i1 ON i1.name = d.player_sword_name INNER JOIN items i2 ON i2.name = d.player_armor_name WHERE d.dungeon BETWEEN 1 and 9')
        elif page == 2:
            cur.execute('SELECT d.player_sword_name, d.player_sword_enchant, i1.emoji, d.player_armor_name, d.player_armor_enchant, i2.emoji, d.dungeon FROM dungeons d INNER JOIN items i1 ON i1.name = d.player_sword_name INNER JOIN items i2 ON i2.name = d.player_armor_name WHERE d.dungeon BETWEEN 10 and 15')
        record = cur.fetchall()
        
        if record:
            rec_gear_data = record
        else:
            await log_error(ctx, 'No recommended dungeon gear data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return rec_gear_data

# Get dungeon data for the dungeon check command
async def get_dungeon_check_data(ctx, dungeon_no=0):
    
    try:
        cur=erg_db.cursor()
        if dungeon_no == 0:
            cur.execute('SELECT player_at, player_def, player_carry_def, player_life, dungeon FROM dungeons')
            record = cur.fetchall()
        else:
            cur.execute('SELECT player_at, player_def, player_carry_def, player_life, dungeon FROM dungeons WHERE dungeon=?',(dungeon_no,))
            record = cur.fetchone()
            
        if record:
            dungeon_check_data = record
        else:
            await log_error(ctx, 'No recommended dungeon check data found in database.')            
    
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return dungeon_check_data

# Get area data for the area embeds
async def get_area_data(ctx, area):
    
    try:
        cur=erg_db.cursor()
        select_columns = 'a.area, a.work_cmd_poor, a.work_cmd_rich, a.work_cmd_asc, a.new_cmd_1, a.new_cmd_2, a.new_cmd_3, a.rich_threshold_m, a.upgrade_sword, a.upgrade_sword_enchant, a.upgrade_armor, a.upgrade_armor_enchant, a.description, a.dungeon, i1.emoji, '\
                        'i2.emoji, d.player_at, d.player_def, d.player_carry_def, d.player_life, d.life_boost_needed, d.player_level, d.player_sword_name, d.player_sword_enchant, d.player_armor_name, d.player_armor_enchant'
        cur.execute(f'SELECT {select_columns} FROM areas a INNER JOIN dungeons d ON d.dungeon = a.dungeon INNER JOIN items i1 ON i1.name = d.player_sword_name INNER JOIN items i2 ON i2.name = d.player_armor_name WHERE a.area=?', (area,))
        record = cur.fetchone()
        
        if record:
            area_data = record
        else:
            await log_error(ctx, 'No area data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return area_data

# Get mats data for the needed mats of area 3 and 5
async def get_mats_data(ctx, user_tt):
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT t.tt, t.a3_fish, t.a5_apple FROM timetravel t WHERE tt=?', (user_tt,))
        record = cur.fetchone()
        
        if record:
            mats_data = record
        else:
            await log_error(ctx, 'No tt_mats data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return mats_data

# Get items
async def get_item_data(ctx, itemname):
    try:
        cur=erg_db.cursor()
        
        items_data = []
        
        if itemname == 'ultra log':
            itemnames = (itemname,'hyper log','mega log','super log','epic log','','','')
        elif itemname == 'hyper log':
            itemnames = (itemname,'mega log','super log','epic log','','','','')
        elif itemname == 'mega log':
            itemnames = (itemname,'super log','epic log','','','','','')
        elif itemname == 'super log':
            itemnames = (itemname,'epic log','','','','','','')
        elif itemname == 'epic fish':
            itemnames = (itemname,'golden fish','','','','','','')
        elif itemname == 'wooden sword':
            itemnames = (itemname,'epic log','','','','','','')
        elif itemname == 'fish sword':
            itemnames = (itemname,'golden fish','','','','','','')
        elif itemname == 'wolf armor':
            itemnames = (itemname,'epic log','','','','','','')
        elif itemname == 'apple sword':
            itemnames = (itemname,'super log','epic log','','','','','')
        elif itemname == 'eye armor':
            itemnames = (itemname,'super log','epic log','','','','','')
        elif itemname == 'zombie sword':
            itemnames = (itemname,'super log','epic log','','','','','')
        elif itemname == 'banana armor':
            itemnames = (itemname,'super log','epic log','banana','','','','')
        elif itemname == 'ruby sword':
            itemnames = (itemname,'mega log','super log','epic log','','','','')
        elif itemname == 'epic armor':
            itemnames = (itemname,'epic log','epic fish','golden fish','','','','')
        elif itemname == 'unicorn sword':
            itemnames = (itemname,'super log','epic log','','','','','')
        elif itemname == 'ruby armor':
            itemnames = (itemname,'mega log','super log','epic log','','','','')
        elif itemname == 'hair sword':
            itemnames = (itemname,'mega log','super log','epic log','','','','')
        elif itemname == 'coin armor':
            itemnames = (itemname,'hyper log','mega log','super log','epic log','','','')
        elif itemname == 'coin sword':
            itemnames = (itemname,'hyper log','mega log','super log','epic log','','','')
        elif itemname == 'mermaid armor':
            itemnames = (itemname,'mega log','super log','epic log','golden fish','','','')
        elif itemname == 'electronical sword':
            itemnames = (itemname,'hyper log','mega log','super log','epic log','','','')
        elif itemname == 'electronical armor':
            itemnames = (itemname,'hyper log','mega log','super log','epic log','','','')
        elif itemname == 'edgy sword':
            itemnames = (itemname,'ultra log','hyper log','mega log','super log', 'epic log','','')
        elif itemname == 'ultra-edgy sword':
            itemnames = (itemname,'ultra log','hyper log','mega log','super log', 'epic log','epic fish','golden fish')
        elif itemname == 'ultra-edgy armor':
            itemnames = (itemname,'ultra log','hyper log','mega log','super log', 'epic log','','')
        elif itemname == 'omega sword':
            itemnames = (itemname,'mega log','super log','epic log','', '','','')
        elif itemname == 'ultra-omega sword':
            itemnames = (itemname,'ultra log','hyper log','mega log','super log', 'epic log','','')
        elif itemname == 'baked fish':
            itemnames = (itemname,'epic log','epic fish','golden fish','','','','')
        elif itemname == 'fruit salad':
            itemnames = (itemname,'banana','','','','','','')
        elif itemname == 'apple juice':
            itemnames = (itemname,'hyper log','mega log','super log','epic log','','','')
        elif itemname == 'banana pickaxe':
            itemnames = (itemname,'mega log','super log','epic log','banana','','','')
        elif itemname == 'filled lootbox':
            itemnames = (itemname,'banana','','','','','','')
        elif itemname == 'coin sandwich':
            itemnames = (itemname,'epic fish','golden fish','banana','','','','')
        else:
            itemnames = (itemname,'','','','','','','')
            
        cur.execute('SELECT * FROM items WHERE name IN (?,?,?,?,?,?,?,?) ORDER BY level DESC;', itemnames)
        record = cur.fetchall()
            
        if record:
            items_columns = []
            colnames = cur.description
            
            for row in colnames:
                items_columns.append(row[0])
            items_data = [items_columns,]
            
            for row in record:
                items_data.append(list(row))
        else:
            items_data = ''
        
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return items_data

# Get tt unlocks
async def get_tt_unlocks(ctx, user_tt):
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT t.tt, t.unlock_dungeon, t.unlock_area, t.unlock_enchant, t.unlock_title, t.unlock_misc FROM timetravel t WHERE tt=?', (user_tt,))
        record = cur.fetchone()
        
        if record:
            tt_unlock_data = record
        else:
            await log_error(ctx, 'No tt_unlock data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return tt_unlock_data

# Get trade rate data
async def get_traderate_data(ctx, area):
    
    try:
        cur=erg_db.cursor()
        
        if area == 'all':
            cur.execute('SELECT area, trade_fish_log, trade_apple_log, trade_ruby_log FROM areas ORDER BY area')
            record = cur.fetchall()
        else:
            cur.execute('SELECT area, trade_fish_log, trade_apple_log, trade_ruby_log FROM areas WHERE area=?', (area,))
            record = cur.fetchone()
        
        if record:
            traderate_data = record
        else:
            await log_error(ctx, 'No trade rate data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return traderate_data

# Get random tip
async def get_tip(ctx):
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT tip FROM tips ORDER BY RANDOM() LIMIT 1')
        record = cur.fetchone()
        
        if record:
            tip = record
        else:
            await log_error(ctx, 'No tips data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return tip

# Get redeemable codes
async def get_codes(ctx):
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT * FROM codes ORDER BY code')
        record = cur.fetchall()
        
        if record:
            codes = record
        else:
            await log_error(ctx, 'No codes data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return codes

# Get user count
async def get_user_number(ctx):
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT COUNT(*) FROM settings_user')
        record = cur.fetchone()
        
        if record:
            user_number = record
        else:
            await log_error(ctx, 'No user data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return user_number
   
# Check database for user settings, if none is found, the default settings TT0 and not ascended are saved and used, return both
async def get_settings(bot, ctx):
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT * FROM settings_user where user_id=?', (ctx.author.id,))
        record = cur.fetchone()
        
        if record:
            current_settings = (record[1], record[2])
        else:
            cur.execute('INSERT INTO settings_user VALUES (?, ?, ?)', (ctx.author.id, '0', 'not ascended',))
            await first_time_user(bot, ctx)
            
    except sqlite3.Error as error:
        await log_error(ctx, error)    
  
    return current_settings


# --- Database: Write Data ---

# Set new prefix
async def set_prefix(bot, ctx, new_prefix):

    try:
        cur=erg_db.cursor()
        cur.execute('SELECT * FROM settings_guild where guild_id=?', (ctx.guild.id,))
        record = cur.fetchone()
        
        if record:
            cur.execute('UPDATE settings_guild SET prefix = ? where guild_id = ?', (new_prefix, ctx.guild.id,))           
        else:
            cur.execute('INSERT INTO settings_guild VALUES (?, ?)', (ctx.guild.id, new_prefix,))
    except sqlite3.Error as error:
        await log_error(ctx, error)

# Set progress settings
async def set_progress(bot, ctx, new_tt, new_ascended):
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT * FROM settings_user where user_id=?', (ctx.author.id,))
        record = cur.fetchone()
        
        if record:
            cur.execute('UPDATE settings_user SET timetravel = ?, ascended = ? where user_id = ?', (new_tt, new_ascended, ctx.author.id,))
        else:
            cur.execute('INSERT INTO settings_user VALUES (?, ?, ?)', (ctx.author.id, new_tt, new_ascended,))
    except sqlite3.Error as error:
        await log_error(ctx, error)


# --- Error Logging ---

# Error logging
async def log_error(ctx, error, guild_join=False):
    
    if guild_join == False:
        try:
            settings = ''
            try:
                user_settings = await get_settings(bot, ctx)
                settings = f'TT{user_settings[0]}, {user_settings[1]}'
            except:
                settings = 'N/A'
            cur=erg_db.cursor()
            cur.execute('INSERT INTO errors VALUES (?, ?, ?, ?)', (ctx.message.created_at, ctx.message.content, str(error), settings))
        except sqlite3.Error as db_error:
            print(print(f'Error inserting error (ha) into database.\n{db_error}'))
    else:
        try:
            cur=erg_db.cursor()
            cur.execute('INSERT INTO errors VALUES (?, ?, ?, ?)', (datetime.now(), 'Error when joining a new guild', str(error), 'N/A'))
        except sqlite3.Error as db_error:
            print(print(f'Error inserting error (ha) into database.\n{db_error}'))


# --- First Time User ---

# Welcome message to inform the user of his/her initial settings
async def first_time_user(bot, ctx):
    
    try:
        current_settings = await get_settings(bot, ctx)
        
        await ctx.send(f'Hey there, **{ctx.author.name}**. Looks like we haven\'t met before.\nI have set your progress to '\
                    f'**TT {current_settings[0]}**, **{current_settings[1]}**.\n\n'\
                    f'If I guessed wrong, please use `{ctx.prefix}setprogress` to change your settings.\n\n'\
                    'These settings are used by some guides (like the area guides) to only show you what is relevant to your current progress.')
    except:
        raise
    else:
        raise FirstTimeUser("First time user, pls ignore")


# --- Command Initialization ---

bot = commands.Bot(command_prefix=get_prefix_all, help_command=None, case_insensitive=True)


# Custom exception for first time users so they stop spamming my database
class FirstTimeUser(commands.CommandError):
        def __init__(self, argument):
            self.argument = argument

# --- Ready & Join Events ---

# Set bot status when ready
@bot.event
async def on_ready():
    
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'default prefix $'))
    
# Send message to system channel when joining a server
@bot.event
async def on_guild_join(guild):
    
    try:
        prefix = await get_prefix(bot, guild, True)
        
        welcome_message =   f'Hello **{guild.name}**! I\'m here to provide some guidance!\n\n'\
                            f'To get a list of all topics, type `{prefix}guide` (or `{prefix}g` for short).\n'\
                            f'If you don\'t like this prefix, use `{prefix}setprefix` to change it.\n\n'\
                            f'Tip: If you ever forget the prefix, simply ping me with a command.\n\n'\
        
        await guild.system_channel.send(welcome_message)
    except:
        return


# --- Error Handling ---

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, (commands.MissingPermissions)):
        missing_perms = ''
        for missing_perm in error.missing_perms:
            if not missing_perms == '':
                missing_perms = f'{missing_perms}, `{missing_perm}`'
            else:
                missing_perms = f'`{missing_perm}`'
        await ctx.send(f'Sorry **{ctx.author.name}**, you need the permission(s) {missing_perms} to use this command.')
    elif isinstance(error, (commands.NotOwner)):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'You\'re missing some arguments.')
    elif isinstance(error, FirstTimeUser):
        return
    else:
        await log_error(ctx, error)


# --- Server Settings ---
   
# Command "setprefix" - Sets new prefix (if user has "manage server" permission)
@bot.command()
@commands.has_permissions(manage_guild=True)
async def setprefix(ctx, *new_prefix):
    
    if new_prefix:
        if len(new_prefix)>1:
            await ctx.send(f'The command syntax is `{ctx.prefix}setprefix [prefix]`')
        else:
            await set_prefix(bot, ctx, new_prefix[0])
            await ctx.send(f'Prefix changed to `{await get_prefix(bot, ctx)}`')
    else:
        await ctx.send(f'The command syntax is `{ctx.prefix}setprefix [prefix]`')

# Command "prefix" - Returns current prefix
@bot.command()
async def prefix(ctx):
    
    current_prefix = await get_prefix(bot, ctx)
    await ctx.send(f'The prefix for this server is `{current_prefix}`\nTo change the prefix use `{current_prefix}setprefix [prefix]`')


# --- User Settings ---

# Command "settings" - Returns current user progress settings
@bot.command(aliases=('me',))
async def settings(ctx):
    
    current_settings = await get_settings(bot, ctx)
    
    if current_settings:
        username = ctx.author.name
        ascension = current_settings[1]
        
        settings = f'{emojis.bp} Current run: **TT {current_settings[0]}**\n'\
                   f'{emojis.bp} Ascension: **{ascension.capitalize()}**'
        
        embed = discord.Embed(
        color = global_data.color,
        title = f'USER SETTINGS',
        description =   f'Hey there, **{ctx.author.name}**.\n'\
                        f'These settings are used by some guides to tailor the information to your current progress.'
        )    
        
        thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
        embed.set_thumbnail(url='attachment://thumbnail.png')
        embed.set_footer(text=f'Tip: Use {ctx.prefix}setprogress to change your settings.')
        embed.set_thumbnail(url='attachment://thumbnail.png')
        embed.add_field(name=f'YOUR CURRENT SETTINGS', value=settings, inline=False)
        
        await ctx.send(file=thumbnail, embed=embed)
    
# Command "setprogress" - Sets TT and ascension
@bot.command(aliases=('sp','setpr','setp',))
async def setprogress(ctx):
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        await ctx.send(f'**{ctx.author.name}**, what **TT** are you currently in? `[0-999]` (type `abort` to abort).')
        answer_tt = await bot.wait_for('message', check=check, timeout = 30)
        if (answer_tt.content == 'abort') or (answer_tt.content == 'cancel'):
            await ctx.send(f'Aborting.')
            return
        new_tt = answer_tt.content
        if new_tt.isnumeric():
            new_tt = int(answer_tt.content)            
            if 0 <= new_tt <= 999:
                await ctx.send(f'**{ctx.author.name}**, are you **ascended**? `[yes/no]` (type `abort` to abort)')
                answer_ascended = await bot.wait_for('message', check=check, timeout=30)
                if (answer_ascended.content == 'abort') or (answer_ascended.content == 'cancel'):
                            await ctx.send(f'Aborting.')
                            return
                if answer_ascended.content.lower() in ['yes','y']:
                    new_ascended = 'ascended'         
                    await set_progress(bot, ctx, new_tt, new_ascended)  
                    current_settings = await get_settings(bot, ctx)
                    await ctx.send(f'Alright **{ctx.author.name}**, your progress is now set to **TT {current_settings[0]}**, **{current_settings[1]}**.')     
                elif answer_ascended.content.lower() in ['no','n']:
                    new_ascended = 'not ascended'
                    await set_progress(bot, ctx, new_tt, new_ascended)        
                    current_settings = await get_settings(bot, ctx)
                    await ctx.send(f'Alright **{ctx.author.name}**, your progress is now set to **TT {current_settings[0]}**, **{current_settings[1]}**.')     
                else:
                    await ctx.send(f'**{ctx.author.name}**, please answer with `yes` or `no`. Aborting.')
            else:
                await ctx.send(f'**{ctx.author.name}**, please enter a number from 0 to 999. Aborting.')
        else:
            await ctx.send(f'**{ctx.author.name}**, please answer with a valid number. Aborting.')  
    except asyncio.TimeoutError as error:
        await ctx.send(f'**{ctx.author.name}**, you took too long to answer, RIP.')


# --- Main menus ---

# Main menu
@bot.command(name='guide',aliases=('help','g','h',))
async def guide_long(ctx):
    
    prefix = await get_prefix(bot, ctx)
    
    progress =  f'{emojis.bp} `{prefix}areas` : Area guides overview\n'\
                f'{emojis.bp} `{prefix}dungeons` : Dungeon guides overview\n'\
                f'{emojis.bp} `{prefix}timetravel` / `{prefix}tt` : Time travel guide\n'\
                f'{emojis.bp} `{prefix}coolness` : Everything known about coolness'
    
    crafting =  f'{emojis.bp} `{prefix}craft [amount] [item]` : Recipes mats calculator\n'\
                f'{emojis.bp} `{prefix}drops` : Monster drops\n'\
                f'{emojis.bp} `{prefix}enchants` / `{prefix}e` : Enchants'
    
    animals =   f'{emojis.bp} `{prefix}horse` : Horse guide\n'\
                f'{emojis.bp} `{prefix}pets` : Pets guide\n'\
    
    trading =   f'{emojis.bp} `{prefix}trading` : Trading guides overview'
                
    professions_value = f'{emojis.bp} `{prefix}professions` / `{prefix}pr` : Professions guide'
    
    event_overview =    f'{emojis.bp} `{prefix}events` : Event guides overview'
    
    misc =      f'{emojis.bp} `{prefix}codes` : Redeemable codes\n'\
                f'{emojis.bp} `{prefix}duel` : Duelling weapons\n'\
                f'{emojis.bp} `{prefix}tip` : A handy dandy random tip'
                
    botlinks =  f'{emojis.bp} `{prefix}invite` : Invite me to your server\n'\
                f'{emojis.bp} `{prefix}support` : Visit the support server\n'\
                f'{emojis.bp} `{prefix}links` : Other links you might be interested in'
                
    settings =  f'{emojis.bp} `{prefix}settings` / `{prefix}me` : Check your user settings\n'\
                f'{emojis.bp} `{prefix}setprogress` / `{prefix}sp` : Change your user settings\n'\
                f'{emojis.bp} `{prefix}prefix` : Check the current prefix'
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'EPIC RPG GUIDE',
        description =   f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    embed.set_footer(text=f'Tip: If you ever forget the prefix, simply ping me with the command \'prefix\'.')
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='PROGRESS', value=progress, inline=False)
    embed.add_field(name='CRAFTING', value=crafting, inline=False)
    embed.add_field(name='HORSE & PETS', value=animals, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='PROFESSIONS', value=professions_value, inline=False)
    embed.add_field(name='EVENTS', value=event_overview, inline=False)
    embed.add_field(name='MISC', value=misc, inline=False)
    embed.add_field(name='LINKS', value=botlinks, inline=False)
    embed.add_field(name='SETTINGS', value=settings, inline=False)
    
    await ctx.send(file=thumbnail, embed=embed)

# Areas menu
@bot.command()
async def areaguide(ctx):
    
    prefix = await get_prefix(bot, ctx)
    
    area_guide =    f'{emojis.bp} `{prefix}area [#]` / `{prefix}a1`-`{prefix}a15` : Guide for area 1~15'
                    
    trading =       f'{emojis.bp} `{prefix}trades [#]` / `{prefix}tr1`-`{prefix}tr15` : Trades in area 1~15\n'\
                    f'{emojis.bp} `{prefix}trades` / `{prefix}tr` : Trades (all areas)\n'\
                    f'{emojis.bp} `{prefix}traderates` / `{prefix}trr` : Trade rates (all areas)'
    
    drops =         f'{emojis.bp} `{prefix}drops` : Monster drops'
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'AREA GUIDES',
        description =   f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='AREAS', value=area_guide, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='MONSTER DROPS', value=drops, inline=False)
    
    await ctx.send(file=thumbnail, embed=embed)
    
# Dungeons menu
@bot.command()
async def dungeonguide(ctx):
    
    prefix = await get_prefix(bot, ctx)
    
    dungeon_guide = f'{emojis.bp} `{prefix}dungeon [#]` / `{prefix}d1`-`{prefix}d15` : Guide for dungeon 1~15\n'\
                    f'{emojis.bp} `{prefix}dgear` / `{prefix}dg` : Recommended gear (all dungeons)\n'\
                    f'{emojis.bp} `{prefix}dstats` / `{prefix}ds` : Recommended stats (all dungeons)'
    
    statscheck =    f'{emojis.bp} `{prefix}dc1`-`{prefix}dc15` : Dungeon 1~15 stats check\n'\
                    f'{emojis.bp} `{prefix}dcheck` / `{prefix}dc` : Dungeon stats check (all dungeons)'
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'DUNGEON GUIDES',
        description =   f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='DUNGEONS', value=dungeon_guide, inline=False)
    embed.add_field(name='STATS CHECK', value=statscheck, inline=False)
    
    await ctx.send(file=thumbnail, embed=embed)

# Trading menu
@bot.command(aliases=('trading',))
async def tradingguide(ctx):
    
    prefix = await get_prefix(bot, ctx)
                    
    trading =       f'{emojis.bp} `{prefix}trades [#]` / `{prefix}tr1`-`{prefix}tr15` : Trades in area 1~15\n'\
                    f'{emojis.bp} `{prefix}trades` / `{prefix}tr` : Trades (all areas)\n'\
                    f'{emojis.bp} `{prefix}traderates` / `{prefix}trr` : Trade rates'
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'TRADING GUIDES',
        description =   f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='TRADING', value=trading, inline=False)
    
    await ctx.send(file=thumbnail, embed=embed)


# --- Dungeons ---

# Command for dungeons, can be invoked with "dX", "d X", "dungeonX" and "dungeon X"
dungeon_aliases = ['dungeon','dung','dungeons',]
for x in range(1,16):
    dungeon_aliases.append(f'd{x}')    
    dungeon_aliases.append(f'dungeon{x}') 
    dungeon_aliases.append(f'dung{x}')

@bot.command(name='d',aliases=(dungeon_aliases))
async def dungeon(ctx, *args):
    
    invoked = ctx.message.content
    invoked = invoked.lower()
    prefix = ctx.prefix
    prefix = prefix.lower()
    
    if args:
        if len(args)>2:
            if len(args)==3:
                arg1 = args[0]
                arg2 = args[1]
                arg3 = args[2]
                if arg1.isnumeric() and arg2.isnumeric() and arg3.isnumeric():
                    await ctx.send(f'Uhm, you may have confused this command with the command `{ctx.prefix}dc`.')
                    return
            else:
                return
        elif len(args) == 2:
            arg = args[0]
            arg = arg.lower()
            if arg == 'gear':
                page = args[1]
                if page.isnumeric():
                    page = int(page)
                    if page in (1,2):
                        await dungeongear(ctx, page)
                        return
                else:
                    await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d15`')           
            else:
                await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d15`')
        elif len(args) == 1:
            arg = args[0]
            arg = arg.lower()
            if arg.isnumeric():
                arg = int(arg)
                if 1 <= arg <= 15:
                    dungeon_data = await get_dungeon_data(ctx, arg)
                    dungeon_embed = await dungeons.dungeon(dungeon_data, ctx.prefix)
                    await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
                else:
                    await ctx.send(f'There is no dungeon {arg}, lol.') 
            else:
                if arg == 'gear':
                    await dungeongear(ctx, 1)
                    return
                elif arg == 'stats':
                    await dungeonstats(ctx)
                    return
                else:
                    await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d15`')
    else:
        dungeon_no = invoked.replace(f'{prefix}dungeons','').replace(f'{prefix}dungeon','').replace(f'{prefix}dung','').replace(f'{prefix}d','')           
        if dungeon_no.isnumeric():
            dungeon_no = int(dungeon_no)
            if 1 <= dungeon_no <= 15:
                dungeon_data = await get_dungeon_data(ctx, dungeon_no)
                dungeon_embed = await dungeons.dungeon(dungeon_data, ctx.prefix)
                await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
            else:
                await ctx.send(f'There is no dungeon {dungeon_no}, lol.') 
        else:
            if dungeon_no == '':
                await dungeonguide(ctx)
                return
            else:
                await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d15`')

# Command "dungeonstats" - Returns recommended stats for all dungeons
@bot.command(aliases=('dstats','ds',))
async def dungeonstats(ctx):
    
    rec_stats_data = await get_rec_stats_data(ctx)
    
    embed = await dungeons.dungeon_rec_stats(rec_stats_data, ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "dungeongear" - Returns recommended gear for all dungeons
@bot.command(aliases=('dgear','dg','dg1','dg2',))
async def dungeongear(ctx, *args):
    
    invoked = ctx.message.content
    invoked = invoked.lower()
    
    if args:
        if len(args)>1:
            await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with}`, `{ctx.prefix}{ctx.invoked_with} [1-2]` or `{ctx.prefix}dg1`-`{ctx.prefix}dg2`') 
            return
        elif len(args)==1:
            page = args[0]
            if page.isnumeric():
                    page = int(page)
                    if page in (1,2):
                        rec_gear_data = await get_rec_gear_data(ctx, page)
                        embed = await dungeons.dungeon_rec_gear(rec_gear_data, ctx.prefix, page)
                        await ctx.send(file=embed[0], embed=embed[1])
                    else:
                        await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with}`, `{ctx.prefix}{ctx.invoked_with} [1-2]` or `{ctx.prefix}dg1`-`{ctx.prefix}dg2`') 
                        return
            else:
                await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with}`, `{ctx.prefix}{ctx.invoked_with} [1-2]` or `{ctx.prefix}dg1`-`{ctx.prefix}dg2`') 
                return
    else:
        page = invoked.replace(f'{ctx.prefix}dungeongear','').replace(f'{ctx.prefix}dgear','').replace(f'{ctx.prefix}dg','')
        if page.isnumeric():
            page = int(page)
            rec_gear_data = await get_rec_gear_data(ctx, page)
            embed = await dungeons.dungeon_rec_gear(rec_gear_data, ctx.prefix, page)
            await ctx.send(file=embed[0], embed=embed[1])
        else:
            if page == '':
                rec_gear_data = await get_rec_gear_data(ctx, 1)
                embed = await dungeons.dungeon_rec_gear(rec_gear_data, ctx.prefix, 1)
                await ctx.send(file=embed[0], embed=embed[1])
            else:
                await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with}`, `{ctx.prefix}{ctx.invoked_with} [1-2]` or `{ctx.prefix}dg1`-`{ctx.prefix}dg2`') 
                return

# Command "dungeoncheck" - Checks user stats against recommended stats
@bot.command(aliases=('dcheck','dungcheck','dc','check',))
async def dungeoncheck(ctx, *args):
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    def epic_rpg_check(m):
        correct_embed = False
        try:
            if (str(m.embeds[0].author).find(f'{ctx.author.name}\'s profile') > 1) or (str(m.embeds[0].author).find(f'{ctx.author.name}\'s stats') > 1):
                correct_embed = True
            else:
                correct_embed = False
        except:
            correct_embed = False
        
        return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed
    
    try: 
        dungeon_no = 0
        if len(args) == 0:
            explanation =   f'This command shows you for which dungeons your stats are high enough.\n'\
                            f'You have the following options:\n'\
                            f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} auto` to let me read your stats.\n{emojis.blank} This works with default profiles (no background) and `rpg stats`.\n'\
                            f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually'
            await ctx.send(explanation)
        elif len(args) == 1:
            try:
                arg = args[0]
                arg = arg.lower()
                if arg == 'auto':
                    await ctx.send(f'**{ctx.author.name}**, please type:\n{emojis.bp} `rpg stats` if you are an EPIC RPG donor\n{emojis.blank} or\n{emojis.bp} `rpg p` if you are not\n{emojis.blank} or\n{emojis.bp} `abort` to abort\n\nNote: `rpg p` does **not** work with profile backgrounds.\nIf you have a background and are not a donor, please use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.')
                    answer_user_profile = await bot.wait_for('message', check=check, timeout = 30)
                    answer = answer_user_profile.content
                    answer = answer.lower()
                    if (answer == 'rpg p') or (answer == 'rpg profile') or (answer == 'rpg stats'):
                        answer_bot_at = await bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                        try:
                            profile = str(answer_bot_at.embeds[0].fields[1])
                        except:
                            try:
                                profile = str(answer_bot_at.embeds[0].fields[0])
                            except:
                                await ctx.send(f'Whelp, something went wrong here, sorry.\nIf you have a profile background, use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually.')
                                return
                        start_at = profile.find('**AT**') + 8
                        end_at = profile.find('<:', start_at) - 2
                        user_at = profile[start_at:end_at]
                        user_at = user_at.replace(',','')
                        start_def = profile.find('**DEF**') + 9
                        end_def = profile.find(':', start_def) - 2
                        user_def = profile[start_def:end_def]
                        user_def = user_def.replace(',','')
                        start_current_life = profile.find('**LIFE**') + 10
                        start_life = profile.find('/', start_current_life) + 1
                        end_life = profile.find('\',', start_life)
                        user_life = profile[start_life:end_life]
                        user_life = user_life.replace(',','')
                    elif (answer_user_profile.content == 'abort') or (answer_user_profile.content == 'cancel'):
                        await ctx.send(f'Aborting.')
                        return
                    else:
                        await ctx.send(f'Wrong input. Aborting.')
                        return
                    if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                        user_at = int(user_at)
                        user_def = int(user_def)
                        user_life = int(user_life)
                    else:
                        await ctx.send(f'Whelp, something went wrong here, sorry. Aborting.')
                        return
                    user_stats = [user_at, user_def, user_life]
                    if dungeon_no == 0:
                        dungeon_check_data = await get_dungeon_check_data(ctx)
                        embed = await dungeons.dungeon_check_stats(dungeon_check_data, user_stats, ctx)
                    else:
                        dungeon_check_data = await get_dungeon_check_data(ctx, dungeon_no)
                        embed = await dungeons.dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                    await ctx.send(file=embed[0], embed=embed[1])
                else:
                    await ctx.send(f'The command syntax is:\n• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\nor\n•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.')
                    return
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profile, RIP.\nIf you have a profile background: Use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.')
        elif len(args) == 3:
            user_at = args[0]
            user_def = args[1]
            user_life = args[2]
            if (user_at.find('-') != -1) or (user_def.find('-') != -1) or (user_life.find('-') != -1):
                await ctx.send(f'Did you play backwards? Send a post card from area -5.')
                return
            else:
                if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                    user_at = int(args[0])
                    user_def = int(args[1])
                    user_life = int(args[2])
                    if (user_at == 0) or (user_def == 0) or (user_life == 0) or (user_at > 10000) or (user_def > 10000) or (user_life > 10000):
                        await ctx.send(f'NICE STATS. Not gonna buy it though.')
                        return 
                    else:
                        dungeon_check_data = await get_dungeon_check_data(ctx)
                        user_stats = [user_at, user_def, user_life]
                        embed = await dungeons.dungeon_check_stats(dungeon_check_data, user_stats, ctx)
                        await ctx.send(file=embed[0], embed=embed[1])
                else:
                    await ctx.send(f'These stats look suspicious. Try actual numbers.')
        else:
            await ctx.send(f'The command syntax is:\n• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\nor\n•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.')
    except:
        raise            

# Command "dungeoncheckX" - Checks user stats against recommended stats of a specific dungeon

dungeon_check_aliases = ['dcheck1','check1','dungcheck1','dc1',]
for x in range(2,16):
    dungeon_check_aliases.append(f'dcheck{x}')    
    dungeon_check_aliases.append(f'check{x}')
    dungeon_check_aliases.append(f'dungeoncheck{x}') 
    dungeon_check_aliases.append(f'dungcheck{x}')
    dungeon_check_aliases.append(f'dc{x}')

@bot.command(aliases=dungeon_check_aliases)
async def dungeoncheck1(ctx, *args):
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
        
    def epic_rpg_check(m):
        correct_embed = False
        try:
            if (str(m.embeds[0].author).find(f'{ctx.author.name}\'s profile') > 1) or (str(m.embeds[0].author).find(f'{ctx.author.name}\'s stats') > 1):
                correct_embed = True
            else:
                correct_embed = False
        except:
            correct_embed = False
        
        return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed
    
    try: 
        invoked = ctx.invoked_with
        invoked = invoked.lower()
        
        dungeon_no = invoked.replace(f'dungeoncheck','').replace(f'dungcheck','').replace(f'dcheck','').replace(f'check','').replace(f'dc','')
        dungeon_no = int(dungeon_no)
    
        if dungeon_no in (10,15):
            user_stats = (0,0,0)
            dungeon_check_data = await get_dungeon_check_data(ctx, dungeon_no)
            embed = await dungeons.dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
            await ctx.send(file=embed[0], embed=embed[1])
        else:
            if len(args) == 0:
                explanation =   f'This command shows you if your stats are high enough for dungeon **{dungeon_no}**.\n'\
                                f'You have the following options:\n'\
                                f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} auto` to let me read your stats.\n{emojis.blank} This works with default profiles (no background) and `rpg stats`.\n'\
                                f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually'
                await ctx.send(explanation)
            elif len(args) == 1:
                arg = args[0]
                arg = arg.lower()
                if arg == 'auto':
                    try:
                        await ctx.send(f'**{ctx.author.name}**, please type:\n{emojis.bp} `rpg stats` if you are an EPIC RPG donor\n{emojis.blank} or\n{emojis.bp} `rpg p` if you are not\n{emojis.blank} or\n{emojis.bp} `abort` to abort\n\nNote: `rpg p` does **not** work with profile backgrounds.\nIf you have a background and are not a donor, please use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.')
                        answer_user_at = await bot.wait_for('message', check=check, timeout = 30)
                        answer = answer_user_at.content
                        answer = answer.lower()
                        if (answer == 'rpg p') or (answer == 'rpg profile') or (answer == 'rpg stats'):
                            answer_bot_at = await bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                            try:
                                profile = str(answer_bot_at.embeds[0].fields[1])
                            except:
                                try:
                                    profile = str(answer_bot_at.embeds[0].fields[0])
                                except:
                                    await ctx.send(f'Whelp, something went wrong here, sorry.\nIf you have a profile background, use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually.')
                                    return
                            start_at = profile.find('**AT**') + 8
                            end_at = profile.find('<:', start_at) - 2
                            user_at = profile[start_at:end_at]
                            start_def = profile.find('**DEF**') + 9
                            end_def = profile.find(':', start_def) - 2
                            user_def = profile[start_def:end_def]
                            start_current_life = profile.find('**LIFE**') + 10
                            start_life = profile.find('/', start_current_life) + 1
                            end_life = profile.find('\',', start_life)
                            user_life = profile[start_life:end_life]
                        elif (answer_user_at.content == 'abort') or (answer_user_at.content == 'cancel'):
                            await ctx.send(f'Aborting.')
                            return
                        else:
                            await ctx.send(f'Wrong input. Aborting.')
                            return
                        if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                            user_at = int(user_at)
                            user_def = int(user_def)
                            user_life = int(user_life)
                        else:
                            await ctx.send(f'Whelp, something went wrong here, sorry. Aborting.')
                            return
                        dungeon_check_data = await get_dungeon_check_data(ctx, dungeon_no)
                        user_stats = [user_at, user_def, user_life]
                        embed = await dungeons.dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                        await ctx.send(file=embed[0], embed=embed[1])
                    except asyncio.TimeoutError as error:
                        await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profile, RIP.\nIf you have a profile background: Use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.')
                else:
                    await ctx.send(f'The command syntax is:\n• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\nor\n•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.')
                    return
            elif len(args) == 3:
                user_at = args[0]
                user_def = args[1]
                user_life = args[2]
                if (user_at.find('-') != -1) or (user_def.find('-') != -1) or (user_life.find('-') != -1):
                    await ctx.send(f'Did you play backwards? Send a post card from area -5.')
                    return
                else:
                    if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                        user_at = int(args[0])
                        user_def = int(args[1])
                        user_life = int(args[2])
                        if (user_at == 0) or (user_def == 0) or (user_life == 0) or (user_at > 10000) or (user_def > 10000) or (user_life > 10000):
                            await ctx.send(f'NICE STATS. Not gonna buy it though.')
                            return 
                        else:
                            dungeon_check_data = await get_dungeon_check_data(ctx, dungeon_no)
                            user_stats = [user_at, user_def, user_life]
                            embed = await dungeons.dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                            await ctx.send(file=embed[0], embed=embed[1])
                    else:
                        await ctx.send(f'These stats look suspicious. Try actual numbers.')
            else:
                await ctx.send(f'The command syntax is:\n• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\nor\n•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.')
    except:
        raise            


# --- Areas ---

# Command for areas, can be invoked with "aX", "a X", "areaX" and "area X", optional parameter "full" to override the tt setting
area_aliases = ['area','areas',]
for x in range(1,16):
    area_aliases.append(f'a{x}')    
    area_aliases.append(f'area{x}') 

@bot.command(name='a',aliases=(area_aliases))
async def area(ctx, *args):
    
    invoked = ctx.message.content
    invoked = invoked.lower()
    prefix = ctx.prefix
    prefix = prefix.lower()
    if args:
        if len(args) > 2:
            await ctx.send(f'The command syntax is `{prefix}area [#]` or `{prefix}a1`-`{prefix}a15`')           
        elif len(args) == 2:
            try:
                args_full = str(args[1])
                args_full = args_full.lower()
                if args_full == 'full':
                    area_no = invoked.replace(args_full,'').replace(f' ','').replace(f'{prefix}area','').replace(f'{prefix}a','')
                    if area_no.isnumeric():
                        area_no = int(area_no)
                        if 1<= area_no <= 15:
                            area_data = await get_area_data(ctx, area_no)
                            user_settings = await get_settings(bot, ctx)
                            traderate_data = await get_traderate_data(ctx, area_no)
                            if area_no < 15:
                                traderate_data_next = await get_traderate_data(ctx, area_no+1)
                            else:
                                traderate_data_next = ''
                            user_settings_override = (25, user_settings[1],'override',)
                            if area_no in (3,5):
                                mats_data = await get_mats_data(ctx, user_settings_override[0])
                            else:
                                mats_data = ''
                            area_embed = await areas.area(area_data, mats_data, traderate_data, traderate_data_next, user_settings_override, ctx.author.name, ctx.prefix)   
                            await ctx.send(file=area_embed[0], embed=area_embed[1])   
                        else:
                            await ctx.send(f'There is no area {area_no}, lol.')           
            except:
                return
        else:
            try:
                area_no = args[0]
                if area_no.isnumeric():
                    area_no = int(area_no)
                    if 1 <= area_no <= 15:
                        area_data = await get_area_data(ctx, area_no)
                        user_settings = await get_settings(bot, ctx)
                        traderate_data = await get_traderate_data(ctx, area_no)
                        if area_no < 15:
                            traderate_data_next = await get_traderate_data(ctx, area_no+1)
                        else:
                            traderate_data_next = ''
                        if area_no in (3,5):
                            if user_settings[0] <= 25:
                                mats_data = await get_mats_data(ctx, user_settings[0])
                            else:
                                mats_data = await get_mats_data(ctx, 25)
                        else:
                            mats_data = ''
                        area_embed = await areas.area(area_data, mats_data, traderate_data, traderate_data_next, user_settings, ctx.author.name, ctx.prefix)
                        await ctx.send(file=area_embed[0], embed=area_embed[1])
                    else:
                        await ctx.send(f'There is no area {area_no}, lol.')
                else:
                    args_full = str(args[0])
                    args_full = args_full.lower()
                    if args_full == 'full':
                        area_no = invoked.replace(args_full,'').replace(f' ','').replace(f'{prefix}area','').replace(f'{prefix}a','')
                        if area_no.isnumeric():
                            area_no = int(area_no)
                            if 1 <= area_no <= 15:
                                area_data = await get_area_data(ctx, int(area_no))
                                user_settings = await get_settings(bot, ctx)
                                traderate_data = await get_traderate_data(ctx, area_no)
                                if area_no < 15:
                                    traderate_data_next = await get_traderate_data(ctx, area_no+1)
                                else:
                                    traderate_data_next = ''
                                user_settings_override = (25, user_settings[1],'override',)
                                if area_no in (3,5):
                                    mats_data = await get_mats_data(ctx, user_settings_override[0])
                                else:
                                    mats_data = ''
                                area_embed = await areas.area(area_data, mats_data, traderate_data, traderate_data_next, user_settings_override, ctx.author.name, ctx.prefix)   
                                await ctx.send(file=area_embed[0], embed=area_embed[1])
                            else:
                                await ctx.send(f'There is no area {area_no}, lol.')
                    else:
                        await ctx.send(f'The command syntax is `{prefix}area [#]` or `{prefix}a1`-`{prefix}a15`')           
            except:
                await ctx.send(f'The command syntax is `{prefix}area [#]` or `{prefix}a1`-`{prefix}a15`')           
    else:
        area_no = invoked.replace(f'{prefix}areas','').replace(f'{prefix}area','').replace(f'{prefix}a','')
        if area_no.isnumeric():
            area_no = int(area_no)
            if not area_no == 0:
                area_data = await get_area_data(ctx, area_no)
                user_settings = await get_settings(bot, ctx)
                traderate_data = await get_traderate_data(ctx, area_no)
                if area_no < 15:
                    traderate_data_next = await get_traderate_data(ctx, area_no+1)
                else:
                    traderate_data_next = ''
                if area_no in (3,5):
                    if user_settings[0] <= 25:
                        mats_data = await get_mats_data(ctx, user_settings[0])
                    else:
                        mats_data = await get_mats_data(ctx, 25)
                else:
                    mats_data = ''
                area_embed = await areas.area(area_data, mats_data, traderate_data, traderate_data_next, user_settings, ctx.author.name, ctx.prefix)
        else:
            if area_no == '':
                await areaguide(ctx)
                return
            else:
                await ctx.send(f'Uhm, what.')           
                return
        await ctx.send(file=area_embed[0], embed=area_embed[1])

# Command "trades" - Returns recommended trades of one area or all areas
trades_aliases = ['tr','trade',]
for x in range(1,16):
    trades_aliases.append(f'tr{x}')    
    trades_aliases.append(f'trades{x}')
    trades_aliases.append(f'trade{x}') 

@bot.command(aliases=trades_aliases)
async def trades(ctx, *args):
    
    user_settings = await get_settings(bot, ctx)
    
    invoked = ctx.message.content
    invoked = invoked.lower()
    prefix = ctx.prefix
    prefix = prefix.lower()
    
    if args:
        if len(args)>1:
            await ctx.send(f'The command syntax is `{prefix}{ctx.invoked_with} [#]` or `{prefix}tr1`-`{prefix}tr15`\nOr you can use `{prefix}trade` to see the trades of all areas.')
            return
        elif len(args)==1:
            area_no = args[0]
            if area_no.isnumeric():
                area_no = int(area_no)
                if 1 <= area_no <= 15:
                    embed = await trading.trades_area_specific(user_settings, area_no, ctx.prefix)
                    await ctx.send(file=embed[0], embed=embed[1])
                else:
                    await ctx.send(f'There is no area {area_no}, lol.')
                    return
            else:
                await ctx.send(f'The command syntax is `{prefix}{ctx.invoked_with} [#]` or `{prefix}tr1`-`{prefix}tr15`\nOr you can use `{prefix}trade` to see the trades of all areas.')
                return
        else:
            await ctx.send(f'The command syntax is `{prefix}{ctx.invoked_with} [#]` or `{prefix}tr1`-`{prefix}tr15`\nOr you can use `{prefix}trade` to see the trades of all areas.')
            return
    else:
        area_no = invoked.replace(f'{prefix}trades','').replace(f'{prefix}trade','').replace(f'{prefix}tr','')
        if area_no.isnumeric():
            area_no = int(area_no)
            if 1 <= area_no <= 15:
                embed = await trading.trades_area_specific(user_settings, area_no, ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
            else:
                await ctx.send(f'There is no area {area_no}, lol.')
                return       
        else:
            if area_no == '':             
                embed = await trading.trades(user_settings, ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
            else:
                await ctx.send(f'The command syntax is `{prefix}{ctx.invoked_with} [#]` or `{prefix}tr1`-`{prefix}tr15`\nOr you can use `{prefix}trade` to see the trades of all areas.')

# Command "traderates" - Returns trade rates of all areas
@bot.command(aliases=('trr','rates','rate','traderate',))
async def traderates(ctx):
    
    traderate_data = await get_traderate_data(ctx, 'all')
    
    embed = await trading.traderates(traderate_data, ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])


# --- Crafting ---

# Command "enchants"
@bot.command(aliases=('enchant','e','enchanting',))
async def enchants(ctx):
    
    embed = await crafting.enchants(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "drops" - Returns all monster drops and where to get them
@bot.command(aliases=('drop','mobdrop','mobdrops','monsterdrop','monsterdrops',))
async def drops(ctx):

    embed = await crafting.drops(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])

# Command "craft" - Calculates mats you need for amount of items
@bot.command(aliases=('materials','matsfor','mats','cook',))
async def craft(ctx, *args):

    invoked = ctx.message.content
    invoked = invoked.lower()
    
    if args:
        itemname = ''
        amount = 1
        for arg in args:
            if not arg.lstrip('-').replace('.','').replace(',','').replace('\'','').isnumeric():
                itemname = f'{itemname} {arg}'
                itemname = itemname.strip()
            else:
                try:
                    if (arg.find('.') != -1) or (arg.find(',') != -1):
                        await ctx.send(f'I\'m no Einstein, sorry. Please give me the amount with numbers only. :eyes:')
                        return
                    elif (arg.find('-') != -1) or (int(arg) == 0):
                        await ctx.send(f'You wanna do _what_? Craft **{arg}** items?? Have some :bread: instead.')
                        return
                    elif int(arg) >= 100000000000:
                        await ctx.send(f'Are you trying to break me or something? :thinking:')
                        return
                    else:
                        amount = int(arg)
                except:
                    await ctx.send(f'Are you trying to break me or something? :thinking:')
                    return
                
        if not itemname == '' and amount >= 1:
            try:
                itemname_replaced = itemname.replace('logs','log').replace('ultra edgy','ultra-edgy').replace('ultra omega','ultra-omega').replace('uo ','ultra-omega ')
                itemname_replaced = itemname_replaced.replace('creatures','creature').replace('salads','salad').replace('juices','juice').replace('cookies','cookie').replace('pickaxes','pickaxe')
                itemname_replaced = itemname_replaced.replace('lootboxes','lootbox').replace(' lb',' lootbox').replace('sandwiches','sandwich').replace('apples','apple')       
                
                shortcuts = {   
                    'ed sw': 'edgy sword',
                    'ed sword': 'edgy sword',
                    'ed armor': 'edgy armor',
                    'ue sw': 'ultra-edgy sword',
                    'ue armor': 'ultra-edgy armor',
                    'brandon': 'epic fish',
                    'salad': 'fruit salad',
                    'creature': 'mutant creature',
                    'cookie': 'super cookie',
                    'supercookie': 'super cookie',
                    'juice': 'apple juice',
                    'pickaxe': 'banana pickaxe',
                    'sandwich': 'coin sandwich',
                    'lootbox': 'filled lootbox',
                    'bananas': 'banana',
                    'ultralog': 'ultra log',
                    'hyperlog': 'hyper log',
                    'megalog': 'mega log',
                    'epiclog': 'epic log',
                    'goldenfish': 'golden fish',
                    'epicfish': 'epic fish',
                    'gf': 'golden fish',
                    'ef': 'epic fish',
                    'el': 'epic log',
                    'sl': 'super log',
                    'ml': 'mega log',
                    'hl': 'hyper log',
                    'ul': 'ultra log',
                    'bf': 'baked fish',
                    'mc': 'mutant creature',
                    'fs': 'fruit salad',
                    'aj': 'apple juice',
                    'sc': 'super cookie',
                    'bp': 'banana pickaxe',
                    'ha': 'heavy apple',
                    'fl': 'filled lootbox',
                    'cs': 'coin sandwich',
                    'lb': 'filled lootbox'                   
                }
                
                if itemname_replaced in shortcuts:
                    itemname_replaced = shortcuts[itemname_replaced]                
                
                items_data = await get_item_data(ctx, itemname_replaced)
                if items_data == '':
                    await ctx.send(f'Uhm, I don\'t know an item called `{itemname}`, sorry.')
                    return
            except:
                await ctx.send(f'Uhm, I don\'t know an item called `{itemname}`, sorry.')
                return
            
            items_values = items_data[1]
            itemtype = items_values[1]
            
            if ((itemtype == 'sword') or (itemtype == 'armor')) and (amount > 1):
                await ctx.send(f'You can only craft 1 {getattr(emojis, items_values[3])} {items_values[2]}.')
                return
            
            mats = await crafting.mats(items_data, amount, ctx.prefix)
            await ctx.send(mats)
        else:
            await ctx.send(f'The command syntax is `{ctx.prefix}craft [amount] [item]` or `{ctx.prefix}craft [item] [amount]`\nYou can omit the amount if you want to see the materials for one item only.')
    else:
        await ctx.send(f'The command syntax is `{ctx.prefix}craft [amount] [item]` or `{ctx.prefix}craft [item] [amount]`\nYou can omit the amount if you want to see the materials for one item only.')


# --- Horses ---

# Command "horses"
@bot.command(name='horses', aliases=('horse',))
async def horses_overview(ctx, *args):

    invoked = ctx.message.content
    invoked = invoked.lower()
    if args:
        if len(args)>1:
            return
        elif len(args)==1:
            if (args[0] == 'tier') or (args[0] == 'tiers'):
                    x = await horsetier(ctx)
                    return
            elif (args[0] == 'type') or (args[0] == 'types'):
                    x = await horsetype(ctx)
                    return
            elif (args[0] == 'breed') or (args[0] == 'breeding'):
                    x = await horsebreed(ctx)
                    return
            else:
                return
        else:
            return
    else:
        embed = await horses.horses(ctx.prefix)
        await ctx.send(file=embed[0], embed=embed[1])
    
# Command "horsetier" - Returns horse tier bonuses
@bot.command(aliases=('htier','horsestier','horsetiers','horsestiers',))
async def horsetier(ctx):

    embed = await horses.horsetiers(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "horsetype" - Returns horse type bonuses
@bot.command(aliases=('htype','horsestype','horsetypes','horsestypes',))
async def horsetype(ctx):

    embed = await horses.horsetypes(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "horsebreed" - Returns horse breed details
@bot.command(aliases=('hbreed','hbreeding','breed','breeding','horsebreeding','horsesbreed','horsesbreeding','breedhorse','breedhorses','breedinghorse','breedingshorses',))
async def horsebreed(ctx):

    embed = await horses.horsebreeding(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    

# --- Pets ---

# Command "pets" - Returns pets overview
@bot.command(name='pets', aliases=('pet',))
async def pets_overview(ctx, *args):

    invoked = ctx.message.content
    invoked = invoked.lower()
    if args:
        if len(args)>1:
            return
        elif len(args)==1:
            if (args[0] == 'catch') or (args[0] == 'find') or (args[0] == 'finding') or (args[0] == 'catching'):
                    x = await petcatch(ctx)
                    return
            elif (args[0] == 'fusion') or (args[0] == 'fusing'):
                    x = await petfusion(ctx)
                    return
            elif (args[0] == 'skill') or (args[0] == 'skills'):
                    x = await petskills(ctx)
                    return
            elif (args[0] == 'adv') or (args[0] == 'adventures') or (args[0] == 'adventure'):
                    x = await petsadventure(ctx)
                    return
            else:
                return
        else:
            return
    else:
        embed = await pets.pets(ctx.prefix)
        await ctx.send(file=embed[0], embed=embed[1])

# Command "petcatch" - How to catch pets
@bot.command(aliases=('petscatch','petscatching','petcatching','petfind','petsfind','petfinding','petsfinding','catchpet','findpet','catchingpet','findingpet','catchpets','findpets','catchingpets','findingpets',))
async def petcatch(ctx):

    embed = await pets.petscatch(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "petfusion" - Pets fusion guide
@bot.command(aliases=('petsfusion','fusion','petfusing','petsfusing','fusing','fusepet','fusepets','fusingpet','fusingpets',))
async def petfusion(ctx):

    embed = await pets.petsfusion(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "petskills" - Pet skills
@bot.command(aliases=('petsskills','petskill','skill','skills','petsskill',))
async def petskills(ctx):

    embed = await pets.petsskills(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])

# Command "petsadventures" - Pet adventures
@bot.command(aliases=('petsadv','petsadventures','petadv','petadventure','petadventures',))
async def petsadventure(ctx):

    embed = await pets.petsadventures(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])


# --- Events ---

# Command "events" - Main event command
@bot.command(name='events', aliases=('event','enchantevent','epicguard','guard','jail','heal','healevent','arena','arenaevent','coinrain','rain','cointrumpet','trumpet','catch','catchevent','epictree','tree','epicseed','seed','chop','chopevent','god','godevent','boss','legendary','legendaryboss','bossevent','legendarybossevent',\
                                    'megalodon','fish','fishevent','megalodonevent','miniboss','minibossevent','specialtrade','tradeevent','specialtradeevent','bigarena','arenabig','bigarenaevent','lottery','ticket','lotteryticket','notsominiboss','notsominibossevent','notsomini',\
                                    'race','racing','hrace','horserace','horseracing','lootbox','lootboxevent','lb','lbevent'))
async def events_overview(ctx, *args):

    invoked = ctx.invoked_with
    invoked = invoked.lower()

    if args:
        event_name = ''
        for arg in args:
            event_name = f'{event_name}{arg}'
        event_name = event_name.lower().replace(' ','').strip()
        if event_name.find('enchant') > -1:
                embed = await events.event_enchant(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('guard') > -1) or (event_name.find('jail') > -1):
                embed = await events.event_epicguard(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif event_name.find('god') > -1:
                embed = await events.event_god(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('heal') > -1) or (event_name.find('mysterious') > -1) or (event_name.find('potion') > -1):
                embed = await events.event_heal(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('legendary') > -1) or (event_name == 'boss'):
                embed = await events.event_legendary(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('lootbox') > -1) or (event_name == 'lb'):
                embed = await events.event_lootbox(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif event_name == 'arena':
                embed = await events.event_arena(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('coin') > -1) or (event_name.find('rain') > -1) or (event_name.find('trumpet') > -1) or (event_name.find('catch') > -1):
                embed = await events.event_coinrain(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('tree') > -1) or (event_name.find('seed') > -1) or (event_name.find('chop') > -1):
                embed = await events.event_epictree(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('megalodon') > -1) or (event_name.find('ultrabait') > -1) or (event_name.find('fish') > -1):
                embed = await events.event_megalodon(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif event_name == 'miniboss':
                embed = await events.event_miniboss(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('specialtrade') > -1) or (event_name.find('trade') > -1):
                embed = await events.event_specialtrade(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('bigarena') > -1):
                embed = await events.event_bigarena(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('horserace') > -1) or (event_name.find('race') > -1):
                embed = await events.event_horserace(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('lottery') > -1) or (event_name.find('ticket') > -1):
                embed = await events.event_lottery(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        elif (event_name.find('notsomini') > -1):
                embed = await events.event_notsominiboss(ctx.prefix)
                await ctx.send(file=embed[0], embed=embed[1])
        else:
            await ctx.send(f'I can\'t find any event with that name\nUse `{ctx.prefix}events` to see a list of all events.')          
    else:
        if invoked.find('enchant') > -1:
            embed = await events.event_enchant(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('guard') > -1) or (invoked.find('jail') > -1):
            embed = await events.event_epicguard(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('heal') > -1):
            embed = await events.event_heal(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif invoked in ('arena','arenaevent'):
            embed = await events.event_arena(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('rain') > -1) or (invoked.find('trumpet') > -1) or (invoked.find('catch') > -1):
            embed = await events.event_coinrain(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('tree') > -1) or (invoked.find('seed') > -1) or (invoked.find('chop') > -1):
            embed = await events.event_epictree(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif invoked.find('god') > -1:
            embed = await events.event_god(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked in ('boss','bossevent')) or (invoked.find('legendary') > -1):
            embed = await events.event_legendary(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('megalodon') > -1) or (invoked.find('fish') > -1):
            embed = await events.event_megalodon(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif invoked in ('miniboss','minibossevent'):
            embed = await events.event_miniboss(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('trade') > -1):
            embed = await events.event_specialtrade(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('bigarena') > -1) or (invoked.find('arenabig') > -1):
            embed = await events.event_bigarena(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('race') > -1) or (invoked.find('racing') > -1):
            embed = await events.event_horserace(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('lottery') > -1) or (invoked.find('ticket') > -1):
            embed = await events.event_lottery(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('notsomini') > -1):
            embed = await events.event_notsominiboss(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        elif (invoked.find('lootbox') > -1) or (invoked.find('lb') > -1):
            embed = await events.event_lootbox(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])
        else:
            embed = await events.events_overview(ctx.prefix)
            await ctx.send(file=embed[0], embed=embed[1])


# --- Time Travel ---

# Command "ttX" - Specific tt information
tt_aliases = ['timetravel',]
for x in range(1,1000):
    tt_aliases.append(f'tt{x}')    
    tt_aliases.append(f'timetravel{x}') 

@bot.command(name='tt',aliases=(tt_aliases))
async def timetravel_specific(ctx, *args):
    
    invoked = ctx.message.content
    invoked = invoked.lower()
    
    if args:
        if len(args) > 1:
            await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [1-999]` or `{ctx.prefix}tt1`-`{ctx.prefix}tt999`')
            return       
        else:
            tt_no = args[0]
            if tt_no.isnumeric():
                tt_no = int(tt_no)
                if 1 <= tt_no <= 999:
                    if 1 <= tt_no <= 25:
                        tt_data = await get_tt_unlocks(ctx, tt_no)
                    else:
                        tt_data = (tt_no, 0, 0, '', '')
                else:
                    await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [1-999]` or `{ctx.prefix}tt1`-`{ctx.prefix}tt999`')
                    return
                    
                tt_embed = await timetravel.timetravel_specific(tt_data, ctx.prefix)
                await ctx.send(file=tt_embed[0], embed=tt_embed[1])
            else:
                await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [1-999]` or `{ctx.prefix}tt1`-`{ctx.prefix}tt999`')
    else:
        tt_no = invoked.replace(f'{ctx.prefix}timetravel','').replace(f'{ctx.prefix}tt','')
        
        if tt_no == '':
            tt_embed = await timetravel.timetravel(ctx.prefix)
            await ctx.send(file=tt_embed[0], embed=tt_embed[1])
        else:
            if tt_no.isnumeric():
                tt_no = int(tt_no)
                if 1 <= tt_no <= 999:
                    if 1 <= tt_no <= 25:
                        tt_data = await get_tt_unlocks(ctx, int(tt_no))
                    else:
                        tt_data = (tt_no, 0, 0, '', '', '')
                    tt_embed = await timetravel.timetravel_specific(tt_data, ctx.prefix)
                    await ctx.send(file=tt_embed[0], embed=tt_embed[1])
                else:
                    await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [1-999]` or `{ctx.prefix}tt1`-`{ctx.prefix}tt999`')
                    return
            else:
                await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [1-999]` or `{ctx.prefix}tt1`-`{ctx.prefix}tt999`')
                return

# Command "supertimetravel" - Information about super time travel
@bot.command(aliases=('stt','supertt',))
async def supertimetravel(ctx):
    
    tt_embed = await timetravel.supertimetravel(ctx.prefix)
    
    await ctx.send(file=tt_embed[0], embed=tt_embed[1])
    
# Command "sttscore" - Returns super time travel score calculations
@bot.command(aliases=('sttscore','superttscore','stts',))
async def supertimetravelscore(ctx):

    embed = await timetravel.supertimetravelscore(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])

# Command "tt1000" - Because they will try
@bot.command(aliases=('timetravel1000',))
async def tt1000(ctx):
    
    await ctx.send('https://tenor.com/view/doctorwho-hi-gif-7297611')

# Command "mytt" - Information about user's TT
@bot.command(aliases=('mytimetravel',))
async def mytt(ctx):
    
    user_settings = await get_settings(bot, ctx)
    my_tt = int(user_settings[0])
    
    if 1 <= my_tt <= 25:    
        tt_data = await get_tt_unlocks(ctx, int(my_tt))
    else:
        tt_data = (my_tt,0,0,'','','')
    tt_embed = await timetravel.timetravel_specific(tt_data, ctx.prefix, True)
    await ctx.send(file=tt_embed[0], embed=tt_embed[1])
    

# --- Professions ---

# Command "professions" - Overview about professions
@bot.command(aliases=('pr','professions','prof','profs',))
async def profession(ctx):
    
    embed = await professions.professions_overview(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "prlevel" - How to level up professions
@bot.command(aliases=('prlevel','professionslevel','professionslevels','professionlevels','professionsleveling','professionleveling','prlevels','prleveling','proflevel','proflevels','profslevel','profslevels','prlvl',))
async def professionlevel(ctx):
    
    embed = await professions.professions_leveling(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "prm" - Calculate logs to sell
@bot.command()
async def prm(ctx, *args):
    
    if (len(args) > 1) or (len(args) == 0):
        await ctx.send(f'The command syntax is `{ctx.prefix}prm [merchant xp]`.\nExample: `{ctx.prefix}prm 1234`')
    else:
        try:
            xp = int(args[0])
            logs = xp*5
            xp = f'{xp:,}'.replace(',','\'')
            logs = f'{logs:,}'.replace(',','\'')
            
            await ctx.send(f'You need to sell **{logs}** {emojis.log} `wooden log` to get {xp} merchant XP.')
        except:
            await ctx.send(f'Please enter a valid number.')
            
# Command "prc" - Info about crafting
@bot.command()
async def prc(ctx):
    
    await ctx.send(f'To level up crafter, repeatedly craft {emojis.logepic} EPIC logs in batches of 500.\nSee `{ctx.prefix}prlevel` for more information.')
    
# Command "pre" - Info about enchanting
@bot.command()
async def pre(ctx):
    
    await ctx.send(f'To level up enchanter, repeatedly use `transmute`.\nSee `{ctx.prefix}prlevel` for more information.')
    
# Command "prw" - Info about worker
@bot.command()
async def prw(ctx):
    
    await ctx.send(f'To level up worker, use work commands!\nSee `{ctx.prefix}prlevel` for more information.')
    
# Command "prl" - Info about lootboxer
@bot.command()
async def prl(ctx):
    
    await ctx.send(f'To level up lootboxer, open lootboxes!\nSee `{ctx.prefix}prlevel` for more information.')

# Command "ascension" - Ascension guide
@bot.command(aliases=('asc','ascended','ascend',))
async def ascension(ctx):
    
    embed = await professions.ascension(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])


# --- Miscellaneous ---

# Command "tip" - Returns a random tip
@bot.command(aliases=('tips',))
async def tip(ctx):
    
    tip = await get_tip(ctx)
    
    embed = discord.Embed(
        color = global_data.color,
        title = f'TIP',
        description = tip[0]
    )    
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
    await ctx.send(file=thumbnail, embed=embed)
    
# Command "codes" - Redeemable codes
@bot.command(aliases=('code',))
async def codes(ctx):
    
    codes = await get_codes(ctx)
    
    embed = await misc.codes(ctx.prefix, codes)
    
    await ctx.send(file=embed[0], embed=embed[1])

# Command "duels" - Returns all duelling weapons
@bot.command(aliases=('duel','duelling','dueling','duelweapons','duelweapon',))

async def duels(ctx):

    embed = await misc.duels(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])

# Command "coolness" - Coolness guide
@bot.command(aliases=('cool',))

async def coolness(ctx):

    embed = await misc.coolness(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])

# Command "badges" - Badge guide
@bot.command(aliases=('badge',))

async def badges(ctx):

    embed = await misc.badges(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    

# --- Links --- 

# Command "invite"
@bot.command(aliases=('inv',))
async def invite(ctx):
       
    embed = discord.Embed(
    color = global_data.color,
    title = f'NEED A GUIDE?',
    description =   f'I\'d be flattered to visit your server, **{ctx.author.name}**.\n'\
                    f'You can invite me [here](https://discord.com/api/oauth2/authorize?client_id=770199669141536768&permissions=313344&scope=bot).'                  
    )    
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    
    await ctx.send(file=thumbnail, embed=embed)

# Command "support"
@bot.command(aliases=('supportserver','server',))
async def support(ctx):
       
    embed = discord.Embed(
    color = global_data.color,
    title = f'NEED BOT SUPPORT?',
    description =   f'You can visit the support server [here](https://discord.gg/v7WbhnhbgN).'
                    
    )    
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    
    await ctx.send(file=thumbnail, embed=embed)
    
# Command "links"
@bot.command(aliases=('link','wiki',))
async def links(ctx):
    
    epicrpgguide =  f'{emojis.bp} [Support Server](https://discord.gg/v7WbhnhbgN)\n'\
                    f'{emojis.bp} [Bot Invite](https://discord.com/api/oauth2/authorize?client_id=770199669141536768&permissions=313344&scope=bot) (**please see `{ctx.prefix}inv` if the invitation fails**)'  
    
    epicrpg =       f'{emojis.bp} [Official Wiki](https://epic-rpg.fandom.com/wiki/EPIC_RPG_Wiki)\n'\
                    f'{emojis.bp} [Official Server](https://discord.gg/w5dej5m)'
    
    others =        f'{emojis.bp} [MY EPIC RPG ROOM](https://discord.gg/myepicrpgroom)\n'\
                    f'{emojis.bp} [My Epic RPG Reminder](https://discord.gg/kc3GcK44pJ)\n'\
    
    embed = discord.Embed(
    color = global_data.color,
    title = f'SOME HELPFUL LINKS',
    description =   f'There\'s a whole world out there.\n'\

    )    
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    embed.add_field(name=f'EPIC RPG GUIDE', value=epicrpgguide, inline=False)
    embed.add_field(name=f'EPIC RPG', value=epicrpg, inline=False)
    embed.add_field(name=f'EPIC RPG COMMUNITIES', value=others, inline=False)
    
    await ctx.send(file=thumbnail, embed=embed)


# --- Silly Stuff ---

# Command "Panda" - because Panda
@bot.command()
async def panda(ctx):
        
    await ctx.send('All hail Panda! :panda_face:')
    
# Command "Brandon" - because Panda
@bot.command()
async def brandon(ctx):
        
    embed = discord.Embed(
        color = global_data.color,
        title = f'WHAT TO DO WITH BRANDON',
        description = 'Don\'t even _think_ about dismantling him. You monster.'
    )    
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
    await ctx.send(file=thumbnail, embed=embed)


# --- Testing ---
@bot.command()
@commands.is_owner()
async def test(ctx):
    
    seconds = 86400
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    seconds1 = 77760
    days1 = seconds1 // 86400
    hours1 = (seconds1 % 86400) // 3600
    minutes1 = (seconds1 % 3600) // 60
    seconds1 = seconds1 % 60
    
    seconds2 = 69120
    days2 = seconds2 // 86400
    hours2 = (seconds2 % 86400) // 3600
    minutes2 = (seconds2 % 3600) // 60
    seconds2 = seconds2 % 60
    
    seconds3 = 56160
    days3 = seconds3 // 86400
    hours3 = (seconds3 % 86400) // 3600
    minutes3 = (seconds3 % 3600) // 60
    seconds3 = seconds3 % 60
    
    embed = discord.Embed(
        color = global_data.color,
        title = f'COMMAND COOLDOWNS',
        description = f'This page shows all the **default** cooldowns. If you want to see all donator cooldowns, use `{ctx.prefix}cd [command]`'
    )    
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='COOLDOWN', value=f'{emojis.bp} `dungeon | miniboss | not so mini boss`\n{emojis.blank}:one: {days}d / :two: {hours1}h {minutes1}m {seconds1}s / :three: {hours2}h {minutes2}m {seconds2}s / :four: {hours3}h {minutes3}m {seconds3}s', inline=False)
    
    await ctx.send(file=thumbnail, embed=embed)


# --- Owner Commands ---

# Shutdown command (only I can use it obviously)
@bot.command()
@commands.is_owner()
async def shutdown(ctx):

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    await ctx.send(f'**{ctx.author.name}**, are you **SURE**? `[yes/no]`')
    answer_ascended = await bot.wait_for('message', check=check, timeout=30)
    if answer_ascended.content.lower() in ['yes','y']:
        await ctx.send(f'Shutting down.')
        await ctx.bot.logout()
    else:
        await ctx.send(f'Phew, was afraid there for a second.')

# Statistics command (only I can use this)
@bot.command(aliases=('devstat',))
@commands.is_owner()
async def devstats(ctx):

    guilds = len(list(bot.guilds))
    user_number = await get_user_number(ctx)
    
    await ctx.send(f'I\'m currently in **{guilds} servers**, and **{user_number[0]} users** have their settings stored.')

bot.run(TOKEN)