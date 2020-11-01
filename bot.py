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

# Initialize bot
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

# Check database for stored prefix, if none is found, the default prefix $ is used, return only the prefix (returning the default prefix this is pretty pointless as the first command invoke already inserts the record)
async def get_prefix(bot, message):
    
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM settings_guild where guild_id=?', (message.guild.id,))
    record = cur.fetchone()
    
    if record:
        prefix = record[1]
    else:
        prefix = global_data.default_prefix
        
    return prefix

# Get all necessary data for the dungeon embeds
async def get_dungeon_data(dungeon):
    
    cur=erg_db.cursor()
    cur.execute('SELECT dungeons.*, g1.emoji, g2.emoji FROM dungeons INNER JOIN gear g1 ON g1.name = dungeons.player_sword_name INNER JOIN gear g2 ON g2.name = dungeons.player_armor_name WHERE dungeons.dungeon=?', (dungeon,))
    record = cur.fetchone()
    
    if record:
        dungeon_data = record
    else:
        print('Error while getting dungeon data.')
        
    return dungeon_data

# Get all necessary data for the area embeds
async def get_area_data(area):
    
    cur=erg_db.cursor()
    select_columns = 'areas.*, g1.emoji, g2.emoji, d.player_at, d.player_def, d.player_carry_def, d.player_life, d.life_boost_needed, d.player_level, d.player_sword_name, d.player_sword_enchant, d.player_armor_name, d.player_armor_enchant'
    cur.execute(f'SELECT {select_columns} FROM areas INNER JOIN dungeons d ON d.dungeon = areas.dungeon INNER JOIN gear g1 ON g1.name = d.player_sword_name INNER JOIN gear g2 ON g2.name = d.player_armor_name WHERE areas.area=?', (area,))
    record = cur.fetchone()
    
    if record:
        area_data = record
    else:
        print('Error while getting area data.')
        
    return area_data

# Get needed mats for area 3 and 5
async def get_mats_data(user_tt):
    
    cur=erg_db.cursor()
    cur.execute(f'SELECT * FROM tt_mats WHERE tt=?', (user_tt,))
    record = cur.fetchone()
    
    if record:
        mats_data = record
    else:
        print('Error while getting materials data.')
        
    return mats_data

# Get random tip
async def get_tip():
    
    cur=erg_db.cursor()
    cur.execute(f'SELECT tip FROM tips ORDER BY RANDOM() LIMIT 1')
    record = cur.fetchone()
    
    if record:
        tip = record
    else:
        print('Error while getting tips.')
        
    return tip

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
                f'**TT {current_settings[0]}**, **{current_settings[1]}**.\n'\
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

bot = commands.Bot(command_prefix=get_prefix_all, help_command=None, case_insensitive=True)

# Set bot status when ready
@bot.event
async def on_ready():
    
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'\"guide\"'))

# Suppresses errors if a command is entered that the bot doesn't recognize
"""
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, (commands.MissingPermissions)):
        await ctx.send(f'Sorry **{ctx.author.name}**, you are not allowed to use this command.')
"""
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
        await ctx.send(f'**{ctx.author.name}**, your progress is currently set to **TT {current_settings[0]}**, **{current_settings[1]}**.\n'\
                       f'Use `setprogress` if you want to change your settings.')
    
# Command "setprogress" - Sets TT and ascension
@bot.command(aliases=('sp',))
async def setprogress(ctx):
    
    def check(m):
        return m.author == ctx.author
    
    try:
        await ctx.send(f'**{ctx.author.name}**, what {emojis.timetravel} **TT** are you currently in? `[0-999]`')
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
@bot.command(name='guide',aliases=('help',))
async def guide_long(ctx, *args):
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'EPIC RPG GUIDE',
        description = f'All commands use the prefix `{await get_prefix(bot, ctx)}`.'
    )    
    embed.set_footer(text='Tip: Use "g" to see a more compact guide.')
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='PROGRESS', value=f'{emojis.bp} `dungeon [1-15]` : Dungeon guides\n{emojis.bp} `area [1-15]` : Area guides', inline=False)
    embed.add_field(name='TRADING', value=f'{emojis.bp} `trades` : All area trades\n{emojis.bp} `traderates` : All area trade rates', inline=False)
    embed.add_field(name='SETTINGS', value=f'{emojis.bp} `settings` : Shows your settings\n{emojis.bp} `setprogress` : Sets your settings', inline=False)
    embed.add_field(name='MISC', value=f'{emojis.bp} `tip` : Shows a random tip\n{emojis.bp} `shortcuts` : Shows all shortcuts', inline=False)
    
    await ctx.send(file=thumbnail, embed=embed)

# Short guide
@bot.command(name='g')
async def guide_short(ctx, *args):
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'EPIC RPG GUIDE',
        description = f'All commands use the prefix `{await get_prefix(bot, ctx)}`.'
    )    
    embed.set_footer(text='Tip: Use "guide" to see the full guide.')
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='PROGRESS', value=f'{emojis.bp} `dungeon [1-15]`\n{emojis.bp} `area [1-15]`', inline=True)
    embed.add_field(name='TRADING', value=f'{emojis.bp} `trades`\n {emojis.bp} `traderates`', inline=True)
    embed.add_field(name='SETTINGS', value=f'{emojis.bp} `settings`\n{emojis.bp} `setprogress`', inline=True)
    embed.add_field(name='MISC', value=f'{emojis.bp} `tip`\n{emojis.bp} `shortcuts`', inline=True)
    
    await ctx.send(file=thumbnail, embed=embed)
    
# Shortcuts
@bot.command(aliases=('shortcut','sc',))
async def shortcuts(ctx, *args):
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'EPIC RPG GUIDE SHORTCUTS',
        description = f'All commands use the prefix `{await get_prefix(bot, ctx)}`.'
    )    
    embed.set_footer(text='Tip: Use "guide" to see the full guide.')
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='PROGRESS', value=f'{emojis.bp} `dungeon [1-15]` : `d1`-`d15`\n{emojis.bp} `area [1-15]` : `a1`-`a15`', inline=False)
    embed.add_field(name='TRADING', value=f'{emojis.bp} `trades` : `tr`\n{emojis.bp} `traderates` : `trr`', inline=False)
    embed.add_field(name='SETTINGS', value=f'{emojis.bp} `setprogress` : `sp`', inline=False)
    embed.add_field(name='MISC', value=f'{emojis.bp} `shortcuts` : `sc`', inline=False)
    
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
                    dungeon_data = await get_dungeon_data(int(args[0]))
                    dungeon_embed = await dungeons.dungeon(dungeon_data)
                    await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
            except:
                args_check = args[0]
                if not args_check.isnumeric():
                    return
                else:
                    print(f'Error parsing command \"dungeon\"')
    else:
        try:
            dungeon_no = invoked.replace(f'{ctx.prefix}dungeon','').replace(f'{ctx.prefix}d','')           
            dungeon_data = await get_dungeon_data(int(dungeon_no))
            dungeon_embed = await dungeons.dungeon(dungeon_data)
            await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
        except:
            if (dungeon_no == '') or not dungeon_no.isnumeric():
                return
            else:
                print(f'Error parsing command \"dungeon\"')

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
                    area_data = await get_area_data(int(area_no))
                    user_settings = await get_settings(bot, ctx)
                    user_settings_override = (25, user_settings[1],'override',)
                    if int(area_no) in (3,5):
                        mats_data = await get_mats_data(user_settings_override[0])
                    else:
                        mats_data = ''
                    area_embed = await areas.area(area_data, mats_data, user_settings_override, ctx.author.name, ctx.prefix)   
                    await ctx.send(file=area_embed[0], embed=area_embed[1])   
            except:
                return
        else:
            try:
                if 1 <= int(args[0]) <= 15:
                    area_data = await get_area_data(int(args[0]))
                    user_settings = await get_settings(bot, ctx)
                    if int(area_no) in (3,5):
                        mats_data = await get_mats_data(user_settings[0])
                    area_embed = await areas.area(area_data, mats_data, user_settings, ctx.author.name, ctx.prefix)
                    await ctx.send(file=area_embed[0], embed=area_embed[1])
            except:
                try:
                    args_full = str(args[0])
                    args_full = args_full.lower()
                    if args_full == 'full':
                        area_no = invoked.replace(args_full,'').replace(f' ','').replace(f'{ctx.prefix}area','').replace(f'{ctx.prefix}a','')
                        area_data = await get_area_data(int(area_no))
                        user_settings = await get_settings(bot, ctx)
                        user_settings_override = (25, user_settings[1],'override',)
                        if int(area_no) in (3,5):
                            mats_data = await get_mats_data(user_settings_override[0])
                        else:
                            mats_data = ''
                        area_embed = await areas.area(area_data, mats_data, user_settings_override, ctx.author.name, ctx.prefix)   
                        await ctx.send(file=area_embed[0], embed=area_embed[1])   
                except:
                    return
    else:
        try:
            area_no = invoked.replace(f'{ctx.prefix}area','').replace(f'{ctx.prefix}a','')
            area_data = await get_area_data(int(area_no))
            user_settings = await get_settings(bot, ctx)
            if int(area_no) in (3,5):
                mats_data = await get_mats_data(user_settings[0])
            else:
                mats_data = ''
            area_embed = await areas.area(area_data, mats_data, user_settings, ctx.author.name, ctx.prefix)
            await ctx.send(file=area_embed[0], embed=area_embed[1])
        except:
            if area_no == '':
                return
            else:
                print(f'Error parsing command \"area\"')

# Command "trades" - Returns recommended trades of all areas
@bot.command(aliases=('tr',))
async def trades(ctx):
    
    user_settings = await get_settings(bot, ctx)
    
    embed = await trading.trades(user_settings)
    
    await ctx.send(file=embed[0], embed=embed[1])

# Command "trades" - Returns recommended trades of all areas
@bot.command(aliases=('trr',))
async def traderates(ctx):
        
    embed = await trading.traderates()
    
    await ctx.send(file=embed[0], embed=embed[1])

# Command "tip" - Returns a random tip
@bot.command(aliases=('tips',))
async def tip(ctx):
    
    tip = await get_tip()
    
    embed = discord.Embed(
        color = global_data.color,
        title = f'TIP',
        description = tip[0]
    )    
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
    await ctx.send(file=thumbnail, embed=embed)

bot.run(TOKEN)