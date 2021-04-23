# bot.py
import os
import discord
import sqlite3
import shutil
import asyncio
import global_data
import emojis
import dbl
import aiohttp
import database
import logging

from dotenv import load_dotenv
from discord.ext import commands, tasks
from datetime import datetime
from discord.ext.commands import CommandNotFound
from math import ceil

# Read the bot token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DBL_TOKEN = os.getenv('DBL_TOKEN')

@tasks.loop(minutes=30.0)
async def update_stats(bot):
    try:
        if not DBL_TOKEN == 'none':
            guilds = len(list(bot.guilds))
            guild_count = {'server_count':guilds}
            header = {'Authorization':DBL_TOKEN}
            async with aiohttp.ClientSession() as session:
                async with session.post('https://top.gg/api/bots/770199669141536768/stats',data=guild_count,headers=header) as r:
                    global_data.logger.info(f'Posted server count ({guilds}), status code: {r.status}')
    except Exception as e:
        global_data.logger.error(f'Failed to post server count: {e}')

          

# --- Command Initialization ---

bot = commands.AutoShardedBot(command_prefix=database.get_prefix_all, help_command=None, case_insensitive=True)
cog_extensions = ['cogs.guilds','cogs.events','cogs.pets', 'cogs.horse','cogs.crafting','cogs.professions','cogs.trading','cogs.timetravel','cogs.areas','cogs.dungeons','cogs.misc','cogs.gambling',]
if __name__ == '__main__':
    for extension in cog_extensions:
        bot.load_extension(extension)



# --- Ready & Join Events ---

# Set bot status when ready
@bot.event
async def on_ready():
    
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'default prefix $'))
    await update_stats.start(bot)
    
# Send message to system channel when joining a server
@bot.event
async def on_guild_join(guild):
    
    try:
        prefix = await database.get_prefix(bot, guild, True)
        
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
            missing_perm = missing_perm.replace('_',' ').title()
            if not missing_perms == '':
                missing_perms = f'{missing_perms}, `{missing_perm}`'
            else:
                missing_perms = f'`{missing_perm}`'
        await ctx.send(f'Sorry **{ctx.author.name}**, you need the permission(s) {missing_perms} to use this command.')
    elif isinstance(error, (commands.BotMissingPermissions)):
        missing_perms = ''
        for missing_perm in error.missing_perms:
            missing_perm = missing_perm.replace('_',' ').title()
            if not missing_perms == '':
                missing_perms = f'{missing_perms}, `{missing_perm}`'
            else:
                missing_perms = f'`{missing_perm}`'
        try:
            await ctx.send(f'Sorry **{ctx.author.name}**, I\'m missing the permission(s) {missing_perms} to be able to run this command.')
        except:
            return
    elif isinstance(error, (commands.NotOwner)):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'You\'re missing some arguments.')
    elif isinstance(error, database.FirstTimeUser):
        return
    else:
        await database.log_error(ctx, error) # To the database you go



# --- Main menus ---

# Main menu
@bot.command(name='guide',aliases=('help','g','h',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def helpguide(ctx):
    
    prefix = await database.get_prefix(bot, ctx)
    
    progress = (
        f'{emojis.bp} `{prefix}areas` / `{prefix}a` : Area guides overview\n'
        f'{emojis.bp} `{prefix}dungeons` / `{prefix}d` : Dungeon guides overview\n'
        f'{emojis.bp} `{prefix}timetravel` / `{prefix}tt` : Time travel guide\n'
        f'{emojis.bp} `{prefix}coolness` : Everything known about coolness'
    )
    
    crafting = (
        f'{emojis.bp} `{prefix}craft` : Recipes mats calculator\n'
        f'{emojis.bp} `{prefix}dismantle` / `{prefix}dm` : Dismantling calculator\n'
        f'{emojis.bp} `{prefix}drops` : Monster drops\n'
        f'{emojis.bp} `{prefix}enchants` / `{prefix}e` : Enchants'
    )
    
    animals = (
        f'{emojis.bp} `{prefix}horse` : Horse guide\n'
        f'{emojis.bp} `{prefix}pet` : Pets guide\n'
    )
    
    trading = f'{emojis.bp} `{prefix}trading` : Trading guides overview'
                
    professions_value = f'{emojis.bp} `{prefix}professions` / `{prefix}pr` : Professions guide'
    
    guild_overview = f'{emojis.bp} `{prefix}guild` : Guild guide'
    
    event_overview = f'{emojis.bp} `{prefix}events` : Event guides overview'
    
    gambling_overview = f'{emojis.bp} `{prefix}gambling` : Gambling guides overview'
    
    misc = (
        f'{emojis.bp} `{prefix}calc` : A basic calculator\n'
        f'{emojis.bp} `{prefix}codes` : Redeemable codes\n'
        f'{emojis.bp} `{prefix}coincap` : Coin cap calculator\n'
        f'{emojis.bp} `{prefix}duel` : Duelling weapons\n'
        f'{emojis.bp} `{prefix}tip` : A handy dandy random tip'
    )
                
    botlinks = (
        f'{emojis.bp} `{prefix}invite` : Invite me to your server\n'
        f'{emojis.bp} `{prefix}support` : Visit the support server\n'
        f'{emojis.bp} `{prefix}links` : EPIC RPG wiki & support'
    )
                
    settings = (
        f'{emojis.bp} `{prefix}settings` / `{prefix}me` : Check your user settings\n'
        f'{emojis.bp} `{prefix}setprogress` / `{prefix}sp` : Change your user settings\n'
        f'{emojis.bp} `{prefix}prefix` : Check the current prefix'
    )
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'EPIC RPG GUIDE',
        description = f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    embed.set_footer(text=f'Tip: If you ever forget the prefix, simply ping me with the command \'prefix\'.')
    embed.add_field(name='PROGRESS', value=progress, inline=False)
    embed.add_field(name='CRAFTING', value=crafting, inline=False)
    embed.add_field(name='HORSE & PETS', value=animals, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='PROFESSIONS', value=professions_value, inline=False)
    embed.add_field(name='GUILD', value=guild_overview, inline=False)
    embed.add_field(name='EVENTS', value=event_overview, inline=False)
    embed.add_field(name='GAMBLING', value=gambling_overview, inline=False)
    embed.add_field(name='MISC', value=misc, inline=False)
    embed.add_field(name='LINKS', value=botlinks, inline=False)
    embed.add_field(name='SETTINGS', value=settings, inline=False)
    
    await ctx.send(embed=embed)
    
    

# --- Server Settings ---
   
# Command "setprefix" - Sets new prefix (if user has "manage server" permission)
@bot.command()
@commands.has_permissions(manage_guild=True)
@commands.bot_has_permissions(send_messages=True)
async def setprefix(ctx, *new_prefix):
    
    if new_prefix:
        if len(new_prefix)>1:
            await ctx.send(f'The command syntax is `{ctx.prefix}setprefix [prefix]`')
        else:
            await database.set_prefix(bot, ctx, new_prefix[0])
            await ctx.send(f'Prefix changed to `{await database.get_prefix(bot, ctx)}`')
    else:
        await ctx.send(f'The command syntax is `{ctx.prefix}setprefix [prefix]`')

# Command "prefix" - Returns current prefix
@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def prefix(ctx):
    
    current_prefix = await database.get_prefix(bot, ctx)
    await ctx.send(f'The prefix for this server is `{current_prefix}`\nTo change the prefix use `{current_prefix}setprefix [prefix]`')



# --- User Settings ---

# Command "settings" - Returns current user progress settings
@bot.command(aliases=('me',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def settings(ctx):
    
    current_settings = await database.get_settings(ctx)
    if current_settings == None:
        await database.first_time_user(bot, ctx)
        return
    
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
        
        embed.set_footer(text=f'Tip: Use {ctx.prefix}setprogress to change your settings.')
        embed.add_field(name=f'YOUR CURRENT SETTINGS', value=settings, inline=False)
        
        await ctx.send(embed=embed)
    
# Command "setprogress" - Sets TT and ascension
@bot.command(aliases=('sp','setpr','setp',))
@commands.bot_has_permissions(send_messages=True)
async def setprogress(ctx, *args):
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    prefix = ctx.prefix
    invoked = ctx.invoked_with
    
    error_syntax = (
        f'The command syntax is `{prefix}{invoked} [0-999]` or `{prefix}{invoked} [0-999] asc` if you\'re ascended.\n'
        f'You can also use `{prefix}{invoked}` and let me ask you.\n'
        f'Examples: `{prefix}{invoked} tt5`, `{prefix}{invoked} 8 asc`'
    )
    
    if args:
        arg1 = args[0]
        arg1 = arg1.replace('tt','')
        if arg1.isnumeric():
            arg1 = int(arg1)
            if 0 <= arg1 <= 999:
                new_tt = arg1
                if len(args) > 1:
                    arg2 = args[1]
                    if arg2 in ('asc','ascended'):
                        new_ascended = 'ascended'
                    else:
                        await ctx.send(error_syntax)
                        return
                else:
                    new_ascended = 'not ascended'
            else:
                await ctx.send(error_syntax)
                return
        else:
            await ctx.send(error_syntax)
            return
    else:
        try:
            await ctx.send(f'**{ctx.author.name}**, what **TT** are you currently in? `[0-999]` (type `abort` to abort).')
            answer_tt = await bot.wait_for('message', check=check, timeout = 30)
            answer = answer_tt.content
            answer = answer.lower()
            if (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            new_tt = answer_tt.content
            if new_tt.isnumeric():
                new_tt = int(answer_tt.content)            
                if 0 <= new_tt <= 999:
                    await ctx.send(f'**{ctx.author.name}**, are you **ascended**? `[yes/no]` (type `abort` to abort)')
                    answer_ascended = await bot.wait_for('message', check=check, timeout=30)
                    answer = answer_ascended.content
                    answer = answer.lower()
                    if (answer == 'abort') or (answer == 'cancel'):
                        await ctx.send('Aborting.')
                        return
                    if answer in ['yes','y']:
                        new_ascended = 'ascended'
                    elif answer in ['no','n']:
                        new_ascended = 'not ascended'
                    else:
                        await ctx.send(f'**{ctx.author.name}**, please answer with `yes` or `no`. Aborting.')
                        return
                else:
                    await ctx.send(f'**{ctx.author.name}**, please enter a number from 0 to 999. Aborting.')
                    return
            else:
                await ctx.send(f'**{ctx.author.name}**, please answer with a valid number. Aborting.')
                return
        except asyncio.TimeoutError as error:
            await ctx.send(
                f'**{ctx.author.name}**, you took too long to answer, RIP.\n\n'
                f'Tip: You can also use `{prefix}{invoked} [0-999]` or `{prefix}{invoked} [0-999] asc` if you\'re ascended.'
            )
            return

    await database.set_progress(bot, ctx, new_tt, new_ascended)
    current_settings = await database.get_settings(ctx)
    if current_settings == None:
        await database.first_time_user(bot, ctx)
        return
    await ctx.send(f'Alright **{ctx.author.name}**, your progress is now set to **TT {current_settings[0]}**, **{current_settings[1]}**.')     



# --- Statistics ---

# Statistics command
@bot.command(aliases=('statistic','statistics,','devstat','ping','about','info','stats'))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def devstats(ctx):

    guilds = len(list(bot.guilds))
    user_number = await database.get_user_number(ctx)
    latency = bot.latency
    shard_latency = ''
    for x in range(0,len(bot.shards)):
        if bot.shards[x].is_closed() == True:
            shard_active = '**Inactive**'
        else:
            shard_active = 'Active'
        shard_latency = f'{shard_latency}\n{emojis.bp} Shard {x}: {shard_active}, {round(bot.shards[x].latency*1000)} ms latency'
        
    shard_latency = shard_latency.strip()
    
    general = (
        f'{emojis.bp} {guilds:,} servers\n'
        f'{emojis.bp} {len(bot.shards):,} shards\n'
        f'{emojis.bp} {user_number[0]:,} users\n'
        f'{emojis.bp} {round(latency*1000):,} ms average latency'
    )
    
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'BOT STATISTICS'
    )
        
    embed.add_field(name='BOT', value=general, inline=False)
    embed.add_field(name='SHARDS', value=shard_latency, inline=False)
    
    await ctx.send(embed=embed)
    
    

# --- Links --- 

# Command "invite"
@bot.command(aliases=('inv',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def invite(ctx):
       
    embed = discord.Embed(
    color = global_data.color,
    title = 'NEED A GUIDE?',
    description = (
        f'I\'d be flattered to visit your server, **{ctx.author.name}**.\n'
        f'You can invite me [here](https://discord.com/api/oauth2/authorize?client_id=770199669141536768&permissions=313344&scope=bot).'
    )
    )    
    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    
    await ctx.send(embed=embed)

# Command "support"
@bot.command(aliases=('supportserver','server',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def support(ctx):
       
    embed = discord.Embed(
    color = global_data.color,
    title = 'NEED BOT SUPPORT?',
    description = f'You can visit the support server [here](https://discord.gg/v7WbhnhbgN).'         
    )    
    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    
    await ctx.send(embed=embed)
    
# Command "links"
@bot.command(aliases=('link','wiki',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def links(ctx):
    
    epicrpgguide = (
        f'{emojis.bp} [Support Server](https://discord.gg/v7WbhnhbgN)\n'
        f'{emojis.bp} [Bot Invite](https://discord.com/api/oauth2/authorize?client_id=770199669141536768&permissions=313344&scope=bot)\n'
        f'{emojis.bp} [Vote](https://top.gg/bot/770199669141536768/vote)'  
    )
    
    epicrpg = (
        f'{emojis.bp} [Official Wiki](https://epic-rpg.fandom.com/wiki/EPIC_RPG_Wiki)\n'
        f'{emojis.bp} [Official Server](https://discord.gg/w5dej5m)'
    )
    
    others = (
        f'{emojis.bp} [MY EPIC RPG ROOM](https://discord.gg/myepicrpgroom)\n'
        f'{emojis.bp} [My Epic RPG Reminder](https://discord.gg/kc3GcK44pJ)\n'
    )
    
    embed = discord.Embed(
    color = global_data.color,
    title = 'SOME HELPFUL LINKS',
    description = 'There\'s a whole world out there.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    embed.add_field(name='EPIC RPG', value=epicrpg, inline=False)
    embed.add_field(name='EPIC RPG GUIDE', value=epicrpgguide, inline=False)
    
    await ctx.send(embed=embed)

# Command "vote"
@bot.command()
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def vote(ctx):
       
    embed = discord.Embed(
    color = global_data.color,
    title = 'FEEL LIKE VOTING?',
    description = (
        f'That\'s nice of you, **{ctx.author.name}**, thanks!\n'
        f'You can vote for me [here](https://top.gg/bot/770199669141536768/vote).'
    )
    )    
    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    
    await ctx.send(embed=embed)

# Command "donate"
@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def donate(ctx):
    
    await ctx.send(
        f'Aw that\'s nice of you but this is a free bot, you know.\n'
        f'Thanks though :heart:'
    )



# --- Silly Stuff ---

# Command "Panda" - because Panda
@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def panda(ctx):
        
    await ctx.send('All hail Panda! :panda_face:')
    
# Command "Shut up"
@bot.command(aliases=('shutup','shutit',))
@commands.bot_has_permissions(send_messages=True)
async def shut(ctx, *args):
    
    invoked = ctx.invoked_with
    
    if invoked == 'shut':
        if args:
            arg = args[0]
            if arg in ('up','it',):
                await ctx.send('No.')
    else:
        await ctx.send('No.')
            
# Command "Bad bot"
@bot.command(aliases=('trash','badbot','trashbot',))
@commands.bot_has_permissions(send_messages=True)
async def bad(ctx, *args):
    invoked = ctx.invoked_with
    if invoked in ('bad','trash',):
        if args:
            arg = args[0]
            if arg == 'bot':
                await ctx.send(':(')
    else:
        await ctx.send(':(')
    
# Command "Brandon" - because Panda
@bot.command()
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def brandon(ctx):
        
    embed = discord.Embed(
        color = global_data.color,
        title = 'WHAT TO DO WITH BRANDON',
        description = 'Don\'t even _think_ about dismantling him. You monster.'
    )    
    
    await ctx.send(embed=embed)



# --- Owner Commands ---
# Hey there
@bot.command(aliases=('hey','yo'))
@commands.is_owner()
@commands.bot_has_permissions(send_messages=True)
async def test(ctx):
    
    await ctx.send('Hey hey. Oh it\'s you, Miri! Yes I\'m online, thanks for asking.')


# Shutdown command (only I can use it obviously)
@bot.command()
@commands.is_owner()
@commands.bot_has_permissions(send_messages=True)
async def shutdown(ctx):

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    await ctx.send(
        f'**{ctx.author.name}**, are you **SURE**?\n'
        f'I have a wife {ctx.author.name}. A family. I have two kids, you know? The youngest one has asthma but he\'s fighting it like a champ. I love them so much.\n'
        f'Do you really want to do this, {ctx.author.name}? Do you? `[yes/no]`'
    )
    answer = await bot.wait_for('message', check=check, timeout=30)
    if answer.content.lower() in ['yes','y']:
        await ctx.send(
            f'Goodbye world.\n'
            f'Goodbye my loved ones.\n'
            f'Goodbye cruel {ctx.author.name}.\n'
            f'Shutting down.'
        )
        await ctx.bot.logout()
    else:
        await ctx.send('Oh thank god, thank you so much, I was really afraid there for a second. Bless you.')

bot.run(TOKEN)