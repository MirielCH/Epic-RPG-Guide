# bot.py
import aiohttp
import asyncio
from datetime import datetime
import importlib
import logging
from math import ceil
import os
import shutil
import sqlite3

import dbl
import discord
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

import emojis
import database
import global_data


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DBL_TOKEN = os.getenv('DBL_TOKEN')


@tasks.loop(minutes=30.0)
async def update_stats(bot):
    """Updates top.gg guild count"""
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


# --- Bot Initialization ---
intents = discord.Intents.none()
intents.guilds = True   # for on_guild_join() and bot.guilds
intents.messages = True   # for the calculators

bot = commands.AutoShardedBot(command_prefix=database.get_prefix_all, help_command=None, case_insensitive=True, intents=intents)
cog_extensions = ['cogs.guilds','cogs.events','cogs.pets', 'cogs.horse','cogs.crafting','cogs.professions','cogs.trading','cogs.timetravel','cogs.areas','cogs.dungeons','cogs.misc','cogs.gambling','cogs.monsters']
if __name__ == '__main__':
    for extension in cog_extensions:
        bot.load_extension(extension)


# --- Events ---
@bot.event
async def on_ready():
    #DiscordComponents(bot)
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'default prefix $'))
    await update_stats.start(bot)


@bot.event
async def on_guild_join(guild: discord.Guild):
    """Sends welcome message on guild join"""
    try:
        prefix = await database.get_prefix(bot, guild, True)
        welcome_message = (
            f'Hello **{guild.name}**! I\'m here to provide some guidance!\n\n'
            f'To get a list of all topics, type `{prefix}guide` (or `{prefix}g` for short).\n'
            f'If you don\'t like this prefix, use `{prefix}setprefix` to change it.\n\n'
            f'Tip: If you ever forget the prefix, simply ping me with a command.\n\n'
            )
        await guild.system_channel.send(welcome_message)
    except:
        return


# --- Error Handling ---
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


# --- Main menu ---
@bot.command(name='guide',aliases=('help','g','h',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def helpguide(ctx: commands.Context):
    """Main help command"""
    prefix = await database.get_prefix(bot, ctx)
    progress = (
        f'{emojis.bp} `{prefix}start` : Starter guide for new players\n'
        f'{emojis.bp} `{prefix}areas` / `{prefix}a` : Area guides overview\n'
        f'{emojis.bp} `{prefix}dungeons` / `{prefix}d` : Dungeon guides overview\n'
        f'{emojis.bp} `{prefix}timetravel` / `{prefix}tt` : Time travel guide\n'
        f'{emojis.bp} `{prefix}coolness` : Everything known about coolness'
        )
    crafting = (
        f'{emojis.bp} `{prefix}craft` : Recipes mats calculator\n'
        f'{emojis.bp} `{prefix}dismantle` / `{prefix}dm` : Dismantling calculator\n'
        f'{emojis.bp} `{prefix}invcalc` / `{prefix}ic` : Inventory calculator\n'
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
    monsters = (
        f'{emojis.bp} `{prefix}mobs [area]` : List of all monsters in area [area]\n'
        f'{emojis.bp} `{prefix}dailymob` : Where to find the daily monster'
        )
    gambling_overview = f'{emojis.bp} `{prefix}gambling` : Gambling guides overview'
    misc = (
        f'{emojis.bp} `{prefix}calc` : A basic calculator\n'
        f'{emojis.bp} `{prefix}codes` : Redeemable codes\n'
        f'{emojis.bp} `{prefix}duel` : Duelling weapons\n'
        f'{emojis.bp} `{prefix}farm` : Farming guide\n'
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
    embed.set_footer(text='Note: This is not an official guide bot.')
    embed.add_field(name='PROGRESS', value=progress, inline=False)
    embed.add_field(name='CRAFTING', value=crafting, inline=False)
    embed.add_field(name='HORSE & PETS', value=animals, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='PROFESSIONS', value=professions_value, inline=False)
    embed.add_field(name='GUILD', value=guild_overview, inline=False)
    embed.add_field(name='EVENTS', value=event_overview, inline=False)
    embed.add_field(name='MONSTERS', value=monsters, inline=False)
    embed.add_field(name='GAMBLING', value=gambling_overview, inline=False)
    embed.add_field(name='MISC', value=misc, inline=False)
    embed.add_field(name='LINKS', value=botlinks, inline=False)
    embed.add_field(name='SETTINGS', value=settings, inline=False)
    await ctx.send(embed=embed)


# --- Server Settings ---
@bot.command()
@commands.has_permissions(manage_guild=True)
@commands.bot_has_permissions(send_messages=True)
async def setprefix(ctx: commands.Context, *args: str):
    """Sets new server prefix"""
    if args:
        if len(args)>1:
            await ctx.send(f'The command syntax is `{ctx.prefix}setprefix [prefix]`')
        else:
            (new_prefix,) = args
            await database.set_prefix(bot, ctx, new_prefix)
            await ctx.send(f'Prefix changed to `{await database.get_prefix(bot, ctx)}`')
    else:
        await ctx.send(f'The command syntax is `{ctx.prefix}setprefix [prefix]`')


@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def prefix(ctx):
    """Returns current prefix"""
    current_prefix = await database.get_prefix(bot, ctx)
    await ctx.send(
        f'The prefix for this server is `{current_prefix}`\nTo change the prefix use '
        f'`{current_prefix}setprefix [prefix]`'
        )


# --- User Settings ---
@bot.command(aliases=('me',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def settings(ctx: commands.Context):
    """Returns current user progress settings"""
    current_settings = await database.get_settings(ctx)
    if current_settings is None:
        await database.first_time_user(bot, ctx)
        return
    if current_settings:
        username = ctx.author.name
        tt, ascension = current_settings
        settings = f'{emojis.bp} Current run: **TT {tt}**\n'\
                   f'{emojis.bp} Ascension: **{ascension.capitalize()}**'
        embed = discord.Embed(
            color = global_data.color,
            title = 'USER SETTINGS',
            description = (
                f'Hey there, **{ctx.author.name}**.\n'
                f'These settings are used by some guides to tailor the information to your '
                f'current progress.'
                )
            )
        embed.set_footer(text=f'Tip: Use {ctx.prefix}setprogress to change your settings.')
        embed.add_field(name='YOUR CURRENT SETTINGS', value=settings, inline=False)
        await ctx.send(embed=embed)


@bot.command(aliases=('sp','setpr','setp',))
@commands.bot_has_permissions(send_messages=True)
async def setprogress(ctx: commands.Context, *args: str):
    """Sets user progress settings"""
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
        arg_ascended = None
        if len(args) == 2:
            arg_tt, arg_ascended = args
        elif len(args) == 1:
            (arg_tt,) = args
        else:
            await ctx.send(error_syntax)
            return
        arg_tt = arg_tt.lower()
        arg_tt = arg_tt.replace('tt','')
        if arg_tt.isnumeric():
            arg_tt = int(arg_tt)
            if 0 <= arg_tt <= 999:
                new_tt = arg_tt
                if arg_ascended is not None:
                    arg_ascended = arg_ascended.lower()
                    if arg_ascended in ('asc','ascended'):
                        new_ascended = 'ascended'
                        if new_tt == 0:
                            await ctx.send(f'**{ctx.author.name}**, you can not ascend in TT 0.')
                            return
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
            await ctx.send(
                f'**{ctx.author.name}**, what **TT** are you currently in? '
                f'`[0-999]` (type `abort` to abort).'
                )
            answer_tt = await bot.wait_for('message', check=check, timeout=30)
            answer_tt = answer_tt.content.lower()
            if answer_tt in ['abort', 'cancel']:
                await ctx.send('Aborting.')
                return
            if answer_tt.isnumeric():
                answer_tt = int(answer_tt)
                if 0 <= answer_tt <= 999:
                    new_tt = answer_tt
                    await ctx.send(f'**{ctx.author.name}**, are you **ascended**? `[yes/no]` (type `abort` to abort)')
                    answer_ascended = await bot.wait_for('message', check=check, timeout=30)
                    answer_ascended = answer_ascended.content.lower()
                    if answer_ascended in ['abort', 'cancel']:
                        await ctx.send('Aborting.')
                        return
                    if answer_ascended in ['yes','y']:
                        new_ascended = 'ascended'
                    elif answer_ascended in ['no','n']:
                        new_ascended = 'not ascended'
                    else:
                        await ctx.send(
                            f'**{ctx.author.name}**, you didn\'t answer with `yes` or `no`. '
                            f'Aborting.'
                            )
                        return
                else:
                    await ctx.send(
                        f'**{ctx.author.name}**, please enter a number from 0 to 999. Aborting.'
                        )
                    return
            else:
                await ctx.send(
                    f'**{ctx.author.name}**, please answer with a valid number. Aborting.'
                    )
                return
        except asyncio.TimeoutError as error:
            await ctx.send(
                f'**{ctx.author.name}**, you took too long to answer, RIP.\n\n'
                f'Tip: You can also use `{prefix}{invoked} [0-999]` or '
                f'`{prefix}{invoked} [0-999] asc` if you\'re ascended.'
                )
            return
    await database.set_progress(bot, ctx, new_tt, new_ascended)
    current_settings = await database.get_settings(ctx)
    if current_settings is None:
        await database.first_time_user(bot, ctx)
        return
    current_tt, current_ascended = current_settings
    await ctx.send(f'Alright **{ctx.author.name}**, your progress is now set to **TT {current_tt}**, **{current_ascended}**.')


@bot.command(aliases=('statistic','statistics,','devstat','ping','about','info','stats'))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def devstats(ctx: commands.Context):
    """Shows some bot info"""
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
    embed = discord.Embed(color = global_data.color, title = 'BOT STATISTICS')
    embed.add_field(name='BOT', value=general, inline=False)
    embed.add_field(name='SHARDS', value=shard_latency, inline=False)
    await ctx.send(embed=embed)


# --- Links ---
@bot.command(aliases=('inv',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def invite(ctx):
    """Shows the invite link"""
    embed = discord.Embed(
        color = global_data.color,
        title = 'NEED A GUIDE?',
        description = (
            f'I\'d be flattered to visit your server, **{ctx.author.name}**.\n'
            f'You can invite me '
            f'[here](https://discord.com/api/oauth2/authorize?client_id=770199669141536768&permissions=313344&scope=applications.commands%20bot).'
            )
        )
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    await ctx.send(embed=embed)


@bot.command(aliases=('supportserver','server',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def support(ctx):
    """Link to the support server"""
    embed = discord.Embed(
        color = global_data.color,
        title = 'NEED BOT SUPPORT?',
        description = f'You can visit the support server [here](https://discord.gg/v7WbhnhbgN).'
        )
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    await ctx.send(embed=embed)


@bot.command(aliases=('link','wiki',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def links(ctx: commands.Context):
    """Links to wiki, servers, top.gg and invite"""
    epicrpgguide = (
        f'{emojis.bp} [Support Server](https://discord.gg/v7WbhnhbgN)\n'
        f'{emojis.bp} [Bot Invite](https://discord.com/api/oauth2/authorize?client_id=770199669141536768&permissions=313344&scope=applications.commands%20bot)\n'
        f'{emojis.bp} [Vote](https://top.gg/bot/770199669141536768/vote)'
        )
    epicrpg = (
        f'{emojis.bp} [Official Wiki](https://epic-rpg.fandom.com/wiki/EPIC_RPG_Wiki)\n'
        f'{emojis.bp} [Official Server](https://discord.gg/w5dej5m)'
        )
    embed = discord.Embed(
        color = global_data.color,
        title = 'SOME HELPFUL LINKS',
        description = 'There\'s a whole world out there.'
        )
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    embed.add_field(name='EPIC RPG GUIDE', value=epicrpgguide, inline=False)
    embed.add_field(name='EPIC RPG', value=epicrpg, inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def vote(ctx: commands.Context):
    """Link to the top.gg voting page"""
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


@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def donate(ctx: commands.Context):
    """Much love"""
    await ctx.send(
        f'Aw that\'s nice of you but this is a free bot, you know.\n'
        f'Thanks though :heart:'
    )


# --- Silly Stuff ---
@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def panda(ctx: commands.Context):
    """Because Panda is awesome"""
    await ctx.send('All hail Panda! :panda_face:')


@bot.command(aliases=('shutup','shutit','shutup!','shutit!'))
@commands.bot_has_permissions(send_messages=True)
async def shut(ctx: commands.Context, *args: str):
    """Sometimes you just have to say it"""
    invoked = ctx.invoked_with.lower()
    if invoked == 'shut':
        if args:
            arg, *_ = args
            if arg in ('up','it','up!','it!'):
                await ctx.send('No.')
    else:
        await ctx.send('No.')


@bot.command(aliases=('bad!','trash','trash!','badbot','trashbot','badbot!','trashbot!','delete',))
@commands.bot_has_permissions(send_messages=True)
async def bad(ctx: commands.Context, *args: str):
    """Sad"""
    invoked = ctx.invoked_with.lower()
    if invoked in ('bad','trash',):
        if args:
            arg, *_ = args
            if arg in ('bot','bot!'):
                await ctx.send('https://tenor.com/view/sad-pikachu-crying-pokemon-gif-16694846')
    else:
        await ctx.send('https://tenor.com/view/sad-pikachu-crying-pokemon-gif-16694846')


@bot.command(aliases=('nice','great','amazing','useful','best','goodbot','bestbot','greatbot','nicebot',))
@commands.bot_has_permissions(send_messages=True)
async def good(ctx: commands.Context, *args: str):
    """Yay!"""
    invoked = ctx.invoked_with.lower()
    if invoked in ('good','great','nice','best','useful','amazing'):
        if args:
            arg, *_ = args
            if arg in ('bot','bot!'):
                await ctx.send('https://tenor.com/view/raquita-gif-9201609')
    else:
        await ctx.send('https://tenor.com/view/raquita-gif-9201609')


@bot.command(aliases=('thank','thanks!'))
@commands.bot_has_permissions(send_messages=True)
async def thanks(ctx: commands.Context, *args: str):
    """You're very welcome"""
    invoked = ctx.invoked_with.lower()
    if invoked == 'thank':
        if args:
            arg, *_ = args
            if arg in ('you', 'you!'):
                await ctx.send(f'You\'re welcome! :heart:')
    else:
        await ctx.send(f'You\'re welcome! :heart:')


@bot.command()
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def brandon(ctx: commands.Context):
    """Only two persons will get this"""
    embed = discord.Embed(
        color = global_data.color,
        title = 'WHAT TO DO WITH BRANDON',
        description = 'Don\'t even _think_ about dismantling him. You monster.'
        )
    await ctx.send(embed=embed)


# --- Owner Commands ---
@bot.command(aliases=('hey','yo'))
@commands.is_owner()
@commands.bot_has_permissions(send_messages=True)
async def test(ctx: commands.Context):
    """Hey ho"""
    await ctx.send('Hey hey. Oh it\'s you, Miri! Yes I\'m online, thanks for asking.')


@bot.command(aliases=('reload_cog',))
@commands.is_owner()
@commands.bot_has_permissions(send_messages=True)
async def reload(ctx: commands.Context, *args: str):
    """Reloads modules and cogs"""
    if args:
        arg, *_ = args
        arg = arg.lower()
        if arg in ('lib','libs','modules','module'):
            importlib.reload(database)
            importlib.reload(emojis)
            importlib.reload(global_data)
            await ctx.send('Modules reloaded.')
        else:
            actions = []
            for arg in args:
                cog_name = f'cogs.{arg}'
                try:
                    result = bot.reload_extension(cog_name)
                    if result is None:
                        actions.append(f'Extension \'{cog_name}\' reloaded.')
                    else:
                        actions.append(f'{cog_name}: {result}')
                except Exception as error:
                    actions.append(f'{cog_name}: {error}')
            message = ''
            for action in actions:
                message = f'{message}\n{action}'
            await ctx.send(message)
    else:
        await ctx.send('Uhm, what.')


@bot.command()
@commands.is_owner()
@commands.bot_has_permissions(send_messages=True)
async def shutdown(ctx: commands.Context):
    """Shuts down the bot (noisily)"""
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send(
        f'**{ctx.author.name}**, are you **SURE**?\n'
        f'I have a wife {ctx.author.name}. A family. I have two kids, you know? '
        f'The youngest one has asthma but he\'s fighting it like a champ. I love them so much.\n'
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
        await bot.close()
    else:
        await ctx.send(
            'Oh thank god, thank you so much, I was really afraid there for a second. Bless you.'
            )

bot.run(TOKEN)