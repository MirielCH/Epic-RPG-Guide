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
import logging
import logging.handlers
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# Check if log file exists, if not, create empty one
if not os.path.isfile(global_data.logfile):
    open(global_data.logfile, 'a').close()

# Initialize logger
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.handlers.TimedRotatingFileHandler(filename=global_data.logfile,when='D',interval=1, encoding='utf-8', utc=True)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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
        
    return commands.when_mentioned_or(* prefix)(bot, ctx)

# Check database for stored prefix, if none is found, the default prefix $ is used, return only the prefix (returning the default prefix this is pretty pointless as the first command invoke already inserts the record)
async def get_prefix(bot, ctx):
    
    try:
        cur=erg_db.cursor()
        cur.execute('SELECT * FROM settings_guild where guild_id=?', (ctx.guild.id,))
        record = cur.fetchone()
        
        if record:
            prefix = record[1]
        else:
            prefix = global_data.default_prefix
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
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
        cur.execute(f'SELECT * FROM tt_mats WHERE tt=?', (user_tt,))
        record = cur.fetchone()
        
        if record:
            mats_data = record
        else:
            await log_error(ctx, 'No tt_mats data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)
        
    return mats_data

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
            return
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
async def log_error(ctx, error):
    try:
        cur=erg_db.cursor()
        cur.execute('INSERT INTO errors VALUES (?, ?, ?)', (ctx.message.created_at, ctx.message.content, str(error)))
    except sqlite3.Error as db_error:
        print(print(f'Error inserting error (ha) into database.\n{db_error}'))

# Welcome message to inform the user of his/her initial settings
async def first_time_user(bot, ctx):
    
    current_settings = await get_settings(bot, ctx)
    current_prefix = await get_prefix(bot, ctx)
    
    await ctx.send(f'Hey there, **{ctx.author.name}**. Looks like we haven\'t met before.\nI have set your progress to '\
                f'**TT {current_settings[0]}**, **{current_settings[1]}**.\n\n'\
                f'If I guessed wrong, please use `{current_prefix}setprogress` to change your settings.\n\n'\
                '**Note: This bot is still in development, more content will be added soon.**')

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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'\"guide\"'))

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, (commands.MissingPermissions)):
        await ctx.send(f'Sorry **{ctx.author.name}**, you need the permission `Manage Servers` to use this command.')
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
    
    if current_settings:
        username = ctx.author.name
        ascension = current_settings[1]
        settings = f'{emojis.bp} Current run: **TT {current_settings[0]}**\n'\
                   f'{emojis.bp} Ascension: **{ascension.capitalize()}**'
        
        embed = discord.Embed(
        color = global_data.color,
        )    
        
        embed.set_footer(text=f'Use \'setprogress\' to change your settings.')
        embed.set_thumbnail(url='attachment://thumbnail.png')
        embed.add_field(name=f'{username.upper()}\'S SETTINGS', value=settings, inline=False)
        
        await ctx.send(embed=embed)
    
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

# Long guide
@bot.command(name='guide',aliases=('help','g',))
async def guide_long(ctx, *args):
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'EPIC RPG GUIDE',
        description = f'All commands use the prefix `{await get_prefix(bot, ctx)}`.\n'\
                      '**Note: This bot is still in development, more content will be added soon.**'
    )    
    embed.set_footer(text=f'Tip: You can quickly open this guide with \'g\'')
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='PROGRESS', value=f'{emojis.bp} `dungeon [1-15]` / `d[1-15]` : Dungeon guides\n{emojis.bp} `area [1-15]` / `a[1-15]` : Area guides', inline=False)
    embed.add_field(name='CRAFTING', value=f'{emojis.bp} `enchants` / `e` : All enchants\n{emojis.bp} `drops` : Monster drops', inline=False)
    embed.add_field(name='TRADING', value=f'{emojis.bp} `trades` / `tr` : All area trades\n{emojis.bp} `traderates` / `trr` : All area trade rates', inline=False)
    embed.add_field(name='SETTINGS', value=f'{emojis.bp} `settings` : See your settings\n{emojis.bp} `setprogress` / `sp` : Change your settings', inline=False)
    embed.add_field(name='MISC', value=f'{emojis.bp} `tip` : See a random tip', inline=False)
    
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
        if len(args)>1:
            return
        else:
            try:
                if 1 <= int(args[0]) <= 15:
                    dungeon_data = await get_dungeon_data(ctx, int(args[0]))
                    dungeon_embed = await dungeons.dungeon(dungeon_data)
                    await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
            except:
                args_check = args[0]
                if not args_check.isnumeric():
                    return
                else:
                    await log_error(ctx, 'Error parsing command "dungeon"')
    else:
        try:
            dungeon_no = invoked.replace(f'{ctx.prefix}dungeon','').replace(f'{ctx.prefix}d','')           
            dungeon_data = await get_dungeon_data(ctx, int(dungeon_no))
            dungeon_embed = await dungeons.dungeon(dungeon_data)
            await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
        except:
            if (dungeon_no == '') or not dungeon_no.isnumeric():
                return
            else:
                await log_error(ctx, 'Error parsing command "dungeon"')

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
                    area_data = await get_area_data(ctx, int(area_no))
                    user_settings = await get_settings(bot, ctx)
                    traderate_data = await get_traderate_data(ctx, area_no)
                    user_settings_override = (25, user_settings[1],'override',)
                    if int(area_no) in (3,5):
                        mats_data = await get_mats_data(ctx, user_settings_override[0])
                    else:
                        mats_data = ''
                    area_embed = await areas.area(area_data, mats_data, traderate_data, user_settings_override, ctx.author.name, ctx.prefix)   
                    await ctx.send(file=area_embed[0], embed=area_embed[1])   
            except:
                return
        else:
            try:
                if 1 <= int(args[0]) <= 15:
                    area_data = await get_area_data(ctx. int(args[0]))
                    user_settings = await get_settings(bot, ctx)
                    traderate_data = await get_traderate_data(ctx, area_no)
                    if int(area_no) in (3,5):
                        mats_data = await get_mats_data(ctx, user_settings[0])
                    area_embed = await areas.area(area_data, mats_data, traderate_data, user_settings, ctx.author.name, ctx.prefix)
                    await ctx.send(file=area_embed[0], embed=area_embed[1])
            except:
                try:
                    args_full = str(args[0])
                    args_full = args_full.lower()
                    if args_full == 'full':
                        area_no = invoked.replace(args_full,'').replace(f' ','').replace(f'{ctx.prefix}area','').replace(f'{ctx.prefix}a','')
                        area_data = await get_area_data(ctx, int(area_no))
                        user_settings = await get_settings(bot, ctx)
                        traderate_data = await get_traderate_data(ctx, area_no)
                        user_settings_override = (25, user_settings[1],'override',)
                        if int(area_no) in (3,5):
                            mats_data = await get_mats_data(ctx, user_settings_override[0])
                        else:
                            mats_data = ''
                        area_embed = await areas.area(area_data, mats_data, traderate_data, user_settings_override, ctx.author.name, ctx.prefix)   
                        await ctx.send(file=area_embed[0], embed=area_embed[1])   
                except:
                    return
    else:
        try:
            area_no = invoked.replace(f'{ctx.prefix}area','').replace(f'{ctx.prefix}a','')
            area_data = await get_area_data(ctx, int(area_no))
            user_settings = await get_settings(bot, ctx)
            traderate_data = await get_traderate_data(ctx, area_no)
            if int(area_no) in (3,5):
                mats_data = await get_mats_data(ctx, user_settings[0])
            else:
                mats_data = ''
            area_embed = await areas.area(area_data, mats_data, traderate_data, user_settings, ctx.author.name, ctx.prefix)
            await ctx.send(file=area_embed[0], embed=area_embed[1])
        except:
            if area_no == '':
                return
            else:
                await log_error(ctx, 'Error parsing command "area"')

# Command "trades" - Returns recommended trades of all areas
@bot.command(aliases=('tr',))
async def trades(ctx):
    
    user_settings = await get_settings(bot, ctx)
    
    embed = await trading.trades(user_settings)
    
    await ctx.send(file=embed[0], embed=embed[1])

# Command "traderates" - Returns trade rates of all areas
@bot.command(aliases=('trr',))
async def traderates(ctx):
    
    traderate_data = await get_traderate_data(ctx, 'all')
    
    embed = await trading.traderates(traderate_data)
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "enchants"
@bot.command(aliases=('enchant','e',))
async def enchants(ctx):
    
    embed = await crafting.enchants()
    
    await ctx.send(file=embed[0], embed=embed[1])
    
# Command "drops" - Returns all monster drops and where to get them
@bot.command(aliases=('drop',))
async def drops(ctx):

    items = f'Area: 1~2\nSource: {emojis.mobwolf}\nValue: 5\'000\n'\
            f'{emojis.bp} {emojis.zombieeye} **Zombie Eye** - {emojis.mobzombie} Zombie in areas **3~4**\n'\
            f'{emojis.bp} {emojis.unicornhorn} **Unicorn Horn** - {emojis.mobunicorn} Unicorn in areas **5~6**\n'\
            f'{emojis.bp} {emojis.mermaidhair} **Mermaid Hair** - {emojis.mobmermaid} Mermaid in areas **7~8**\n'\
            f'{emojis.bp} {emojis.chip} **Chip** - {emojis.mobkillerrobot} Killer Robot in areas **9~10**\n'\
            f'{emojis.bp} Area: 11~14\n{emojis.bp} Source: {emojis.mobbabydragon}{emojis.mobteendragon}{emojis.mobadultdragon}\n{emojis.bp} Value: 250\'000 coins'

    embed = discord.Embed(
        color = global_data.color,
        title = f'MONSTER DROPS',
        description = f'These items drop when using `hunt` or `hunt together` or when opening lootboxes.\n{emojis.blank}'
    )    
    embed.set_footer(text=global_data.footer)
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'WOLF SKIN {emojis.wolfskin}', value=f'{emojis.bp} Area: 1~2\n{emojis.bp} Source: {emojis.mobwolf}\n{emojis.bp} Value: 500\n{emojis.blank}', inline=True)
    embed.add_field(name=f'ZOMBIE EYE {emojis.zombieeye}', value=f'{emojis.bp} Area: 3~4\n{emojis.bp} Source: {emojis.mobzombie}\n{emojis.bp} Value: 2\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'UNICORN HORN {emojis.unicornhorn}', value=f'{emojis.bp} Area: 5~6\n{emojis.bp} Source: {emojis.mobunicorn}\n{emojis.bp} Value: 7\'500\n{emojis.blank}', inline=True)
    embed.add_field(name=f'MERMAID HAIR {emojis.mermaidhair}', value=f'{emojis.bp} Area: 7~8\n{emojis.bp} Source: {emojis.mobmermaid}\n{emojis.bp} Value: 30\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'CHIP {emojis.chip}', value=f'{emojis.bp} Area: 9~10\n{emojis.bp} Source: {emojis.mobkillerrobot}\n{emojis.bp} Value: 100\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'DRAGON SCALE {emojis.dragonscale}', value=f'{emojis.bp} Area: 11~14\n{emojis.bp} Source: {emojis.mobbabydragon}{emojis.mobteendragon}{emojis.mobadultdragon}\n{emojis.bp} Value: 250\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'DROP CHANCE', value=f'{emojis.bp} All items have a 2% base drop chance\n{emojis.bp} The drop chance increases by ~25% every time you time travel\n{emojis.blank}', inline=False)
    
            
    await ctx.send(file=thumbnail, embed=embed)

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

bot.run(TOKEN)