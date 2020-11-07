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

# Get all necessary data for the dungeon embeds
async def get_dungeon_data(ctx, dungeon):
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT dungeons.*, g1.emoji, g2.emoji FROM dungeons INNER JOIN gear g1 ON g1.name = dungeons.player_sword_name INNER JOIN gear g2 ON g2.name = dungeons.player_armor_name WHERE dungeons.dungeon=?', (dungeon,))
        record = cur.fetchone()
        
        if record:
            dungeon_data = record
        else:
            await log_error(ctx, 'No dungeon data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return dungeon_data

# Get all necessary data for the recommended stats of all dungeons
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

# Get all necessary data for the recommended gear of all dungeons
async def get_rec_gear_data(ctx, page):
    
    try:
        cur=erg_db.cursor()
        if page == 1:
            cur.execute('SELECT d.player_sword_name, d.player_sword_enchant, g1.emoji, d.player_armor_name, d.player_armor_enchant, g2.emoji, d.dungeon FROM dungeons d INNER JOIN gear g1 ON g1.name = d.player_sword_name INNER JOIN gear g2 ON g2.name = d.player_armor_name WHERE d.dungeon BETWEEN 1 and 9')
        elif page == 2:
            cur.execute('SELECT d.player_sword_name, d.player_sword_enchant, g1.emoji, d.player_armor_name, d.player_armor_enchant, g2.emoji, d.dungeon FROM dungeons d INNER JOIN gear g1 ON g1.name = d.player_sword_name INNER JOIN gear g2 ON g2.name = d.player_armor_name WHERE d.dungeon BETWEEN 10 and 15')
        record = cur.fetchall()
        
        if record:
            rec_gear_data = record
        else:
            await log_error(ctx, 'No recommended dungeon gear data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return rec_gear_data

# Get all necessary data for the area embeds
async def get_area_data(ctx, area):
    
    try:
        cur=erg_db.cursor()
        select_columns = 'a.area, a.work_cmd_poor, a.work_cmd_rich, a.work_cmd_asc, a.new_cmd_1, a.new_cmd_2, a.new_cmd_3, a.rich_threshold_m, a.upgrade_sword, a.upgrade_sword_enchant, a.upgrade_armor, a.upgrade_armor_enchant, a.description, a.dungeon, g1.emoji, '\
                        'g2.emoji, d.player_at, d.player_def, d.player_carry_def, d.player_life, d.life_boost_needed, d.player_level, d.player_sword_name, d.player_sword_enchant, d.player_armor_name, d.player_armor_enchant'
        cur.execute(f'SELECT {select_columns} FROM areas a INNER JOIN dungeons d ON d.dungeon = a.dungeon INNER JOIN gear g1 ON g1.name = d.player_sword_name INNER JOIN gear g2 ON g2.name = d.player_armor_name WHERE a.area=?', (area,))
        record = cur.fetchone()
        
        if record:
            area_data = record
        else:
            await log_error(ctx, 'No area data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return area_data

# Get needed mats for area 3 and 5
async def get_mats_data(ctx, user_tt):
    try:
        cur=erg_db.cursor()
        cur.execute(f'SELECT t.tt, t.a3_fish, t.a5_apple FROM timetravel t WHERE tt=?', (user_tt,))
        record = cur.fetchone()
        
        if record:
            mats_data = record
        else:
            await log_error(ctx, 'No tt_mats data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return mats_data

# Get tt unlocks
async def get_tt_unlocks(ctx, user_tt):
    try:
        cur=erg_db.cursor()
        cur.execute(f'SELECT t.tt, t.unlock_dungeon, t.unlock_area, t.unlock_enchant, t.unlock_title, t.unlock_misc FROM timetravel t WHERE tt=?', (user_tt,))
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
            cur.execute(f'SELECT area, trade_fish_log, trade_apple_log, trade_ruby_log FROM areas ORDER BY area')
            record = cur.fetchall()
        else:
            cur.execute(f'SELECT area, trade_fish_log, trade_apple_log, trade_ruby_log FROM areas WHERE area=?', (area,))
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
        cur.execute(f'SELECT tip FROM tips ORDER BY RANDOM() LIMIT 1')
        record = cur.fetchone()
        
        if record:
            tip = record
        else:
            await log_error(ctx, 'No tips data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return tip

# Get user count
async def get_user_number(ctx):
    
    try:
        cur=erg_db.cursor()
        cur.execute(f'SELECT COUNT(*) FROM settings_user')
        record = cur.fetchone()
        
        if record:
            user_number = record
        else:
            await log_error(ctx, 'No user data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return user_number
   
# Check database for stored progress settings, if none is found, the default settings TT0 and not ascended are saved and used, return both
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

# Welcome message to inform the user of his/her initial settings
async def first_time_user(bot, ctx):
    
    current_settings = await get_settings(bot, ctx)
    
    await ctx.send(f'Hey there, **{ctx.author.name}**. Looks like we haven\'t met before.\nI have set your progress to '\
                f'**TT {current_settings[0]}**, **{current_settings[1]}**.\n\n'\
                f'If I guessed wrong, please use `{ctx.prefix}setprogress` to change your settings.\n\n'\
                '**Note: This bot is still in development, more content will be added soon.**')
    
    raise Exception("First time user, no need to continue")

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

bot = commands.Bot(command_prefix=get_prefix_all, help_command=None, case_insensitive=True)

# Set bot status when ready
@bot.event
async def on_ready():
    
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'default prefix $'))
    
# Send message to system channel when joining a server
@bot.event
async def on_guild_join(guild):
    
    prefix = await get_prefix(bot, guild, True)
    
    welcome_message =   f'Hello **{guild.name}**! I\'m here to provide some guidance!\n\n'\
                        f'To get a list of all topics, type `{prefix}guide` (or `{prefix}g` for short).\n'\
                        f'If you don\'t like this prefix, use `{prefix}setprefix` to change it.\n\n'\
                        f'Tip: If you ever forget the prefix, simply ping me with a command.\n\n'\
    
    await guild.system_channel.send(welcome_message)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f'Uhm, what.')
    elif isinstance(error, (commands.MissingPermissions)):
        await ctx.send(f'Sorry **{ctx.author.name}**, you need the permission `Manage Servers` to use this command.')
    elif isinstance(error, (commands.NotOwner)):
        await ctx.send(f'Sorry **{ctx.author.name}**, you are not allowed to do that.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'You\'re missing some arguments.')
    else:
        await log_error(ctx, error)
        
# Command "setprefix" - Sets new prefix (if user has "manage server" permission)
@bot.command()
@commands.has_permissions(manage_guild=True)
async def setprefix(ctx, *new_prefix):
    
    if new_prefix:
        if len(new_prefix)>1:
            await ctx.send(f'Too many arguments.\nThe command syntax is `{ctx.prefix}setprefix [prefix]`')
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

# Command "settings" - Returns current user progress settings
@bot.command()
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
@bot.command(aliases=('sp',))
async def setprogress(ctx):
    
    def check(m):
        return m.author == ctx.author
    
    try:
        await ctx.send(f'**{ctx.author.name}**, what **TT** are you currently in? `[0-999]`')
        answer_tt = await bot.wait_for('message', check=check, timeout = 30)
        try:            
            if 0 <= int(answer_tt.content) <= 999:
                new_tt = int(answer_tt.content)
                await ctx.send(f'**{ctx.author.name}**, are you **ascended**? `[yes/no]`')
                answer_ascended = await bot.wait_for('message', check=check, timeout=30)
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
        except:
            await ctx.send(f'**{ctx.author.name}**, please answer with a valid number. Aborting.')  
    except asyncio.TimeoutError as error:
        await ctx.send(f'**{ctx.author.name}**, you took too long to answer. Aborting.')

# Main guide
@bot.command(name='guide',aliases=('help','g',))
async def guide_long(ctx, *args):
    
    prefix = await get_prefix(bot, ctx)
    
    progress =  f'{emojis.bp} `{prefix}area [1-15]` / `{prefix}a[1-15]` : Area guides\n'\
                f'{emojis.bp} `{prefix}dungeon [1-15]` / `{prefix}d[1-15]` : Dungeon guides\n'\
                f'{emojis.bp} `{prefix}dungeongear` / `{prefix}dg` : Recommended gear for all dungeons\n'\
                f'{emojis.bp} `{prefix}dungeonstats` / `{prefix}ds` : Recommended stats for all dungeons\n'\
                f'{emojis.bp} `{prefix}timetravel` / `{prefix}tt` : Time travel guide'
    
    crafting =  f'{emojis.bp} `{prefix}drops` : Monster drops\n'\
                f'{emojis.bp} `{prefix}enchants` / `{prefix}e` : All enchants'
    
    trading =   f'{emojis.bp} `{prefix}trades` / `{prefix}tr` : All area trades\n'\
                f'{emojis.bp} `{prefix}traderates` / `{prefix}trr` : All area trade rates'
                
    professions_value =   f'{emojis.bp} `{prefix}professions` / `{prefix}pr` : Professions guide'
    
    misc =      f'{emojis.bp} `{prefix}codes` : Redeemable codes\n'\
                f'{emojis.bp} `{prefix}duel` : Duelling weapons\n'\
                f'{emojis.bp} `{prefix}tip` : A handy dandy random tip'
                
    settings =  f'{emojis.bp} `{prefix}settings` : Check your user settings\n'\
                f'{emojis.bp} `{prefix}setprogress` / `{prefix}sp` : Change your user settings\n'\
                f'{emojis.bp} `{prefix}prefix` : Check the current prefix'
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'EPIC RPG GUIDE',
        description =   f'Note: Some guides show information based on your user settings.\n'\
                        f'**This bot is still in development, more content will be added soon.**'
    )    
    embed.set_footer(text=f'Tip: If you ever forget the prefix, simply ping me with a command.')
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='PROGRESS', value=progress, inline=False)
    embed.add_field(name='CRAFTING', value=crafting, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='PROFESSIONS', value=professions_value, inline=False)
    embed.add_field(name='MISC', value=misc, inline=False)
    embed.add_field(name='SETTINGS', value=settings, inline=False)
    
    await ctx.send(file=thumbnail, embed=embed)

# Command for dungeons, can be invoked with "dX", "d X", "dungeonX" and "dungeon X"
dungeon_aliases = ['dungeon',]
for x in range(1,16):
    dungeon_aliases.append(f'd{x}')    
    dungeon_aliases.append(f'dungeon{x}') 

@bot.command(name='d',aliases=(dungeon_aliases))
async def dungeon(ctx, *args):
    
    invoked = ctx.message.content
    invoked = invoked.lower()
    if args:
        if len(args)>2:
            return
        elif len(args)==2:
            if args[0] == 'gear':
                try:
                    if int(args[1]) in (1,2):
                        x = await dungeongear(ctx, int(args[1]))
                        return
                except:
                    return
            else:
                return
        else:
            try:
                if 1 <= int(args[0]) <= 15:
                    dungeon_data = await get_dungeon_data(ctx, int(args[0]))
                    dungeon_embed = await dungeons.dungeon(dungeon_data, ctx.prefix)
                    await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
            except:
                if args[0] == 'gear':
                    x = await dungeongear(ctx, 1)
                    return
                elif args[0] == 'stats':
                    x = await dungeonstats(ctx)
                    return
                else:
                    args_check = args[0]
                    if not args_check.isnumeric():
                        return
                    else:
                        raise
    else:
        try:
            dungeon_no = invoked.replace(f'{ctx.prefix}dungeon','').replace(f'{ctx.prefix}d','')           
            dungeon_data = await get_dungeon_data(ctx, int(dungeon_no))
            dungeon_embed = await dungeons.dungeon(dungeon_data, ctx.prefix)
            await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
        except:
            if (dungeon_no == '') or not dungeon_no.isnumeric():
                return
            else:
                raise

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
    
    if len(args)>1:
        return
    elif len(args)==1:
        try:
            page = int(args[0])
            if page in (1,2):
                rec_gear_data = await get_rec_gear_data(ctx, page)
                embed = await dungeons.dungeon_rec_gear(rec_gear_data, ctx.prefix, page)
            else:
                return
        except:
            return
    else:
        page = invoked.replace(f'{ctx.prefix}dungeongear','').replace(f'{ctx.prefix}dgear','').replace(f'{ctx.prefix}dg','')
        try:
            page = int(page)
            rec_gear_data = await get_rec_gear_data(ctx, page)
            embed = await dungeons.dungeon_rec_gear(rec_gear_data, ctx.prefix, page)
        except:
            if page == '':
                rec_gear_data = await get_rec_gear_data(ctx, 1)
                embed = await dungeons.dungeon_rec_gear(rec_gear_data, ctx.prefix, 1)
            else:
                return

    await ctx.send(file=embed[0], embed=embed[1])

# Command for areas, can be invoked with "aX", "a X", "areaX" and "area X", optional parameter "full" to override the tt setting
area_aliases = ['area',]
for x in range(1,16):
    area_aliases.append(f'a{x}')    
    area_aliases.append(f'area{x}') 

@bot.command(name='a',aliases=(area_aliases))
async def area(ctx, *args):
    
    invoked = ctx.message.content
    invoked = invoked.lower()
    if args:
        if len(args) > 2:
            return        
        elif len(args) == 2:
            try:
                args_full = str(args[1])
                args_full = args_full.lower()
                if args_full == 'full':
                    area_no = invoked.replace(args_full,'').replace(f' ','').replace(f'{ctx.prefix}area','').replace(f'{ctx.prefix}a','')
                    area_no = int(area_no)
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
            except:
                return
        else:
            try:
                if 1 <= int(args[0]) <= 15:
                    area_no = int(args[0])
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
            except:
                try:
                    args_full = str(args[0])
                    args_full = args_full.lower()
                    if args_full == 'full':
                        area_no = invoked.replace(args_full,'').replace(f' ','').replace(f'{ctx.prefix}area','').replace(f'{ctx.prefix}a','')
                        area_no = int(area_no)
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
                except:
                    return
    else:
        try:
            area_no = invoked.replace(f'{ctx.prefix}area','').replace(f'{ctx.prefix}a','')
            area_no = int(area_no)
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
        except:
            if (area_no == '') or (area_no == 0):
                return
            else:
                raise

# Command "trades" - Returns recommended trades of all areas
@bot.command(aliases=('tr',))
async def trades(ctx):
    
    user_settings = await get_settings(bot, ctx)
    
    embed = await trading.trades(user_settings, ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])

# Command "traderates" - Returns trade rates of all areas
@bot.command(aliases=('trr',))
async def traderates(ctx):
    
    traderate_data = await get_traderate_data(ctx, 'all')
    
    embed = await trading.traderates(traderate_data, ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "enchants"
@bot.command(aliases=('enchant','e',))
async def enchants(ctx):
    
    embed = await crafting.enchants(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "drops" - Returns all monster drops and where to get them
@bot.command(aliases=('drop',))
async def drops(ctx):

    embed = await crafting.drops(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "horses" - Returns horse overview
@bot.command(name='horses', aliases=('horse','h',))
async def horses_overview(ctx):

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
    
# Command "duels" - Returns all duelling weapons
@bot.command(aliases=('duel',))
async def duels(ctx):

    embed = await misc.duels(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])

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
            return        
        else:
            try:
                if 1 <= int(args[0]) <= 25:
                    tt_data = await get_tt_unlocks(ctx, int(args[0]))
                else:
                    tt_data = (int(args[0]), 0, 0, '', '')
                    
                tt_embed = await misc.timetravel_specific(tt_data, ctx.prefix)
                await ctx.send(file=tt_embed[0], embed=tt_embed[1])
            except:                    
                return
    else:
        try:
            tt_no = invoked.replace(f'{ctx.prefix}timetravel','').replace(f'{ctx.prefix}tt','')
            
            if tt_no == '':
                tt_embed = await misc.timetravel(ctx.prefix)
                await ctx.send(file=tt_embed[0], embed=tt_embed[1])
            else:
                if 1 <= int(tt_no) <= 25:
                    tt_data = await get_tt_unlocks(ctx, int(tt_no))
                else:
                    tt_data = (int(tt_no), 0, 0, '', '', '')
                    
                tt_embed = await misc.timetravel_specific(tt_data, ctx.prefix)
                await ctx.send(file=tt_embed[0], embed=tt_embed[1])
        except:
            return

# Command "supertimetravel" - Information about super time travel
@bot.command(aliases=('stt',))
async def supertimetravel(ctx):
    
    tt_embed = await misc.supertimetravel(ctx.prefix)
    
    await ctx.send(file=tt_embed[0], embed=tt_embed[1])
    
# Command "sttscore" - Returns super time travel score calculations
@bot.command(aliases=('sttscore','superttscore','stts',))
async def supertimetravelscore(ctx):

    embed = await misc.supertimetravelscore(ctx.prefix)
    
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
    
    tt_data = await get_tt_unlocks(ctx, int(my_tt))
    tt_embed = await misc.timetravel_specific(tt_data, ctx.prefix, True)
    await ctx.send(file=tt_embed[0], embed=tt_embed[1])
    
# Command "professions" - Overview about professions
@bot.command(aliases=('pr','professions',))
async def profession(ctx):
    
    embed = await professions.professions_overview(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "prlevel" - How to level up professions
@bot.command(aliases=('prlevel','professionslevel','professionslevels','professionlevels','professionsleveling','professionleveling','prlevels','prleveling',))
async def professionlevel(ctx):
    
    embed = await professions.professions_leveling(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "prm" - Calculate logs to sell
@bot.command()
async def prm(ctx, *args):
    
    if (len(args) > 1) or (len(args) == 0):
        await ctx.send(f'The command syntax is `{ctx.prefix}prm [merchant xp]`')
    else:
        try:
            xp = int(args[0])
            logs = xp*5
            xp = f'{xp:,}'.replace(',','\'')
            logs = f'{logs:,}'.replace(',','\'')
            
            await ctx.send(f'You need to sell **{logs}** {emojis.log} wooden logs to get {xp} merchant XP.')
        except:
            await ctx.send(f'Please enter a valid number.')

# Command "ascension" - Ascension guide
@bot.command(aliases=('asc',))
async def ascension(ctx):
    
    embed = await professions.ascension(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])

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
@bot.command()
async def codes(ctx):
    
    embed = await misc.codes(ctx.prefix)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "invite"
@bot.command(aliases=('inv',))
async def invite(ctx):
    
    await ctx.send(f'I\'m flattered by your interest, but this bot is still in development and not yet available publicly.')
    
# Command "wiki"
@bot.command()
async def wiki(ctx):
    
    await ctx.send(f'You can find the EPIC RPG wiki here:\nhttps://epic-rpg.fandom.com/wiki/EPIC_RPG_Wiki')
    
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
    
# Command "me" - because Panda
@bot.command()
async def me(ctx):
    
    await ctx.send(f'You are **{ctx.author.name}**.\nDid you really need me to remind you?')

# Shutdown command (only I can use it obviously)
@bot.command()
@commands.is_owner()
async def shutdown(ctx):

    def check(m):
        return m.author == ctx.author
    
    await ctx.send(f'**{ctx.author.name}**, are you **SURE**? `[yes/no]`')
    answer_ascended = await bot.wait_for('message', check=check, timeout=30)
    if answer_ascended.content.lower() in ['yes','y']:
        await ctx.send(f'Shutting down.')
        await ctx.bot.logout()

# Statistics command (only I can use this)
@bot.command()
@commands.is_owner()
async def devstats(ctx):

    guilds = len(list(bot.guilds))
    user_number = await get_user_number(ctx)
    
    await ctx.send(f'I\'m currently in **{guilds} servers** and **{user_number[0]} users** have their settings stored.')

bot.run(TOKEN)