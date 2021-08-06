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
from typing import Union

import dbl
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

import emojis
import database
import global_data


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DBL_TOKEN = os.getenv('DBL_TOKEN')


@tasks.loop(minutes=30.0)
async def update_stats(bot: commands.Bot):
    """Updates top.gg guild count

    Args:
        bot (commands.Bot)
    """
    try:
        if DBL_TOKEN != 'none':
            guilds = len(list(bot.guilds))
            guild_count = {'server_count':guilds}
            header = {'Authorization':DBL_TOKEN}
            async with aiohttp.ClientSession() as session:
                async with session.post('https://top.gg/api/bots/770199669141536768/stats',
                                        data=guild_count,headers=header) as request:
                    global_data.logger.info(
                        f'Posted server count ({guilds}), status code: {request.status}'
                        )
    except Exception as error:
        global_data.logger.error(f'Failed to post server count: {error}')


# --- Bot Initialization ---
intents = discord.Intents.none()
intents.guilds = True   # for on_guild_join() and bot.guilds
intents.messages = True   # for the calculators that read the game

prefixes = database.get_prefix_all
bot = commands.AutoShardedBot(command_prefix=prefixes, help_command=None,
                              case_insensitive=True, intents=intents)
cog_extensions = [
    'cogs.guilds',
    'cogs.events',
    'cogs.pets',
    'cogs.horse',
    'cogs.crafting',
    'cogs.professions',
    'cogs.trading',
    'cogs.timetravel',
    'cogs.areas',
    'cogs.dungeons',
    'cogs.misc',
    'cogs.gambling',
    'cogs.monsters'
    ]
if __name__ == '__main__':
    for extension in cog_extensions:
        bot.load_extension(extension)


# --- Events ---
@bot.event
async def on_ready():
    #DiscordComponents(bot)
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name='default prefix $'))
    await update_stats.start(bot)


@bot.event
async def on_guild_join(guild: discord.Guild):
    """Sends welcome message on guild join

    Args:
        guild (discord.Guild)
    """
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
async def on_command_error(ctx: commands.Context, error: Exception):
    """Runs when an error occurs and handles them accordingly.
    Interesting errors get written to the database for further review.

    Args:
        ctx (commands.Context)
        error (Exception)
    """
    async def send_error(ctx: commands.Context, error: Union[Exception, str]):
        """Sends error message as embed"""
        embed = discord.Embed(title='An error occured')
        embed.add_field(name='Command', value=f'`{ctx.command.qualified_name}`', inline=False)
        embed.add_field(name='Error', value=f'```\n{error}\n```', inline=False)
        await ctx.send(embed=embed)

    if isinstance(error, (commands.CommandNotFound, database.FirstTimeUser, commands.NotOwner)):
        return
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(f'Command `{ctx.command.qualified_name}` is temporarily disabled.')
    elif isinstance(error, (commands.MissingPermissions, commands.MissingRequiredArgument,
                            commands.TooManyArguments, commands.BadArgument)):
        await send_error(ctx, error)
    elif isinstance(error, commands.BotMissingPermissions):
        if 'send_messages' in error.missing_perms:
            return
        elif 'embed_links' in error.missing_perms:
            await ctx.send(error)
        else:
            await send_error(ctx, error)
    else:
        await database.log_error(ctx, error)


# --- Main menu ---
@bot.command(name='guide',aliases=('help','g','h',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def helpguide(ctx: commands.Context):
    """Main help command

    Args:
        ctx (commands.Context)
    """
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
    """Sets new server prefix

    Args:
        ctx (commands.Context)
    """
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
async def prefix(ctx: commands.Context):
    """Returns current prefix

    Args:
        ctx (commands.Context)
    """
    current_prefix = await database.get_prefix(bot, ctx)
    await ctx.send(
        f'The prefix for this server is `{current_prefix}`\nTo change the prefix use '
        f'`{current_prefix}setprefix [prefix]`'
        )


# --- User Settings ---
@bot.command(aliases=('me',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def settings(ctx: commands.Context):
    """Returns current user progress settings

    Args:
        ctx (commands.Context)
    """
    current_settings = await database.get_settings(ctx)
    if current_settings is None:
        await database.first_time_user(bot, ctx)
        return
    else:
        username = ctx.author.name
        tt, ascension = current_settings
        settings = (
            f'{emojis.bp} Current run: **TT {tt}**\n'
            f'{emojis.bp} Ascension: **{ascension.capitalize()}**'
            )
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
    """Sets user progress settings

    Args:
        ctx (commands.Context)
    """
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    async def set_progress(new_tt: int, new_ascended: str):
        await database.set_progress(bot, ctx, new_tt, new_ascended)
        current_settings = await database.get_settings(ctx)
        if current_settings is None:
            await database.first_time_user(bot, ctx)
            return
        current_tt, current_ascended = current_settings
        await ctx.send(
            f'Alright **{ctx.author.name}**, your progress is now set to **TT {current_tt}**, '
            f'**{current_ascended}**.'
            )

    ascension = {
                'ascended': 'ascended',
                'asc': 'ascended',
                'yes': 'ascended',
                'y': 'ascended',
                'no': 'not ascended',
                'not': 'not ascended',
                'n': 'not ascended'
                }

    error_syntax = (
        f'The command syntax is `{prefix}{invoked} [0-999]` or `{prefix}{invoked} [0-999] asc` '
        f'if you\'re ascended.\n'
        f'You can also use `{prefix}{invoked}` and let me ask you.\n\n'
        f'Examples: `{prefix}{invoked} tt5`, `{prefix}{invoked} 8 asc`'
        )

    prefix = ctx.prefix
    invoked = ctx.invoked_with
    if args:
        args = [arg.lower() for arg in args]
        arg_tt, *arg_ascended = args
        try:
            new_tt = int(arg_tt.replace('tt',''))
        except:
            await ctx.send(error_syntax)
            return
        if new_tt not in range (0, 1000):
            await ctx.send(error_syntax)
            return
        if arg_ascended:
            arg_ascended, *_ = arg_ascended
            new_ascended = ascension.get(arg_ascended, None)
            if new_ascended is None:
                await ctx.send(error_syntax)
                return
            if (new_ascended == 'ascended') and (new_tt == 0):
                await ctx.send(f'**{ctx.author.name}**, you can not ascend in TT 0.')
                return
        else:
            new_ascended = 'not ascended'
        await set_progress(new_tt, new_ascended)
        return

    try:
        await ctx.send(
            f'**{ctx.author.name}**, what **TT** are you currently in? '
            f'`[0-999]` (type `abort` to abort).'
            )
        answer_tt = await bot.wait_for('message', check=check, timeout=30)
        answer_tt = answer_tt.content.lower()
        if answer_tt in ('abort', 'cancel'):
            await ctx.send('Aborting.')
            return
        try:
            new_tt = int(answer_tt)
        except:
            await ctx.send(
                f'**{ctx.author.name}**, you didn\'t answer with a valid number. Aborting.'
                )
            return
        if new_tt not in range(0, 1000):
            await ctx.send(
                f'**{ctx.author.name}**, you didn\'t enter a number from 0 to 999. Aborting.'
                )
            return
        await ctx.send(
            f'**{ctx.author.name}**, are you **ascended**? `[yes/no]` '
            f'(type `abort` to abort)'
            )
        answer_ascended = await bot.wait_for('message', check=check, timeout=30)
        answer_ascended = answer_ascended.content.lower()
        if answer_ascended in ('abort', 'cancel'):
            await ctx.send('Aborting.')
            return
        new_ascended = ascension.get(answer_ascended, None)
        if new_ascended is None:
            await ctx.send(
                f'**{ctx.author.name}**, you didn\'t answer with `yes` or `no`. '
                f'Aborting.'
                )
            return
        await set_progress(new_tt, new_ascended)
        return
    except asyncio.TimeoutError as error:
        await ctx.send(
            f'**{ctx.author.name}**, you took too long to answer, RIP.\n\n'
            f'Tip: You can also use `{prefix}{invoked} [0-999]` or '
            f'`{prefix}{invoked} [0-999] asc` if you\'re ascended.'
            )
        return


@bot.command(aliases=('statistic','statistics,','devstat','ping','about','info','stats'))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def devstats(ctx: commands.Context):
    """Shows some bot info

    Args:
        ctx (commands.Context)
    """
    user_count, *_ = await database.get_user_number(ctx)
    closed_shards = 0
    for shard_id in bot.shards:
        if bot.get_shard(shard_id).is_closed():
            closed_shards += 1
    general = (
        f'{emojis.bp} {len(bot.guilds):,} servers\n'
        f'{emojis.bp} {user_count:,} users\n'
        f'{emojis.bp} {len(bot.shards):,} shards ({closed_shards:,} shards offline)\n'
        f'{emojis.bp} {round(bot.latency*1000):,} ms average latency'
        )
    current_shard = bot.get_shard(ctx.guild.shard_id)
    start_time = datetime.utcnow()
    message = await ctx.send('Testing API latency...')
    end_time = datetime.utcnow()
    elapsed_time = end_time - start_time
    current_shard_status = (
        f'{emojis.bp} Shard: {current_shard.id+1} of {len(bot.shards):,}\n'
        f'{emojis.bp} Bot latency: {round(current_shard.latency*1000):,} ms\n'
        f'{emojis.bp} API latency: {round(elapsed_time.total_seconds()*1000):,} ms'
        )
    creator = f'{emojis.bp} Miriel#0001'
    thanks = (
        f'{emojis.bp} FlyingPanda#0328\n'
        f'{emojis.bp} All the math geniuses in the support server'
        )
    embed = discord.Embed(color = global_data.color, title = 'ABOUT EPIC RPG GUIDE')
    embed.add_field(name='BOT STATS', value=general, inline=False)
    embed.add_field(name='CURRENT SHARD', value=current_shard_status, inline=False)
    embed.add_field(name='CREATOR', value=creator, inline=False)
    embed.add_field(name='SPECIAL THANKS TO', value=thanks, inline=False)
    await message.edit(content=None, embed=embed)


# --- Links ---
@bot.command(aliases=('inv',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def invite(ctx: commands.Context):
    """Shows the invite link

    Args:
        ctx (commands.Context)
    """
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
async def support(ctx: commands.Context):
    """Link to the support server

    Args:
        ctx (commands.Context)
    """
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
    """Links to wiki, servers, top.gg and invite

    Args:
        ctx (commands.Context)
    """
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
    """Link to the top.gg voting page

    Args:
        ctx (commands.Context)
    """
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
    """Much love

    Args:
        ctx (commands.Context)
    """
    await ctx.send(
        f'Aw that\'s nice of you but this is a free bot, you know.\n'
        f'Thanks though :heart:'
    )


# --- Silly Stuff ---
@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def panda(ctx: commands.Context):
    """Because Panda is awesome

    Args:
        ctx (commands.Context)
    """
    await ctx.send('All hail Panda! :panda_face:')


@bot.command(aliases=('shutup','shutit','shutup!','shutit!'))
@commands.bot_has_permissions(send_messages=True)
async def shut(ctx: commands.Context, *args: str):
    """Sometimes you just have to say it

    Args:
        ctx (commands.Context)
        *args (str)
    """
    invoked = ctx.invoked_with.lower()
    if invoked == 'shut':
        if args:
            args = [arg.lower() for arg in args]
            arg, *_ = args
            if arg in ('up','it','up!','it!'):
                await ctx.send('No.')
    else:
        await ctx.send('No.')


@bot.command(aliases=('bad!','trash','trash!','badbot','trashbot','badbot!','trashbot!','delete',))
@commands.bot_has_permissions(send_messages=True)
async def bad(ctx: commands.Context, *args: str):
    """Sad

    Args:
        ctx (commands.Context)
        *args (str)
    """
    invoked = ctx.invoked_with.lower()
    if invoked in ('bad','trash',):
        if args:
            args = [arg.lower() for arg in args]
            arg, *_ = args
            if arg in ('bot','bot!'):
                await ctx.send('https://tenor.com/view/sad-pikachu-crying-pokemon-gif-16694846')
    else:
        await ctx.send('https://tenor.com/view/sad-pikachu-crying-pokemon-gif-16694846')


@bot.command(aliases=('nice','great','amazing','useful','best','goodbot','bestbot',
                      'greatbot','nicebot',))
@commands.bot_has_permissions(send_messages=True)
async def good(ctx: commands.Context, *args: str):
    """Yay!

    Args:
        ctx (commands.Context)
        *args (str)
    """
    invoked = ctx.invoked_with.lower()
    if invoked in ('good','great','nice','best','useful','amazing'):
        if args:
            args = [arg.lower() for arg in args]
            arg, *_ = args
            if arg in ('bot','bot!'):
                await ctx.send('https://tenor.com/view/raquita-gif-9201609')
    else:
        await ctx.send('https://tenor.com/view/raquita-gif-9201609')


@bot.command(aliases=('thank','thanks!'))
@commands.bot_has_permissions(send_messages=True)
async def thanks(ctx: commands.Context, *args: str):
    """You're very welcome

    Args:
        ctx (commands.Context)
        *args (str)
    """
    invoked = ctx.invoked_with.lower()
    if invoked == 'thank':
        if args:
            args = [arg.lower() for arg in args]
            arg, *_ = args
            if arg in ('you', 'you!'):
                await ctx.send(f'You\'re welcome! :heart:')
    else:
        await ctx.send(f'You\'re welcome! :heart:')


@bot.command()
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def brandon(ctx: commands.Context):
    """Only three people will get this

    Args:
        ctx (commands.Context)
    """
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
    """Hey ho

    Args:
        ctx (commands.Context)
    """
    await ctx.send('Hey hey. Oh it\'s you, Miri! Yes I\'m online, thanks for asking.')


@bot.command(aliases=('reload_cog',))
@commands.is_owner()
@commands.bot_has_permissions(send_messages=True)
async def reload(ctx: commands.Context, *args: str):
    """Reloads modules and cogs

    Args:
        ctx (commands.Context)
        *args (str)
    """
    if args:
        args = [arg.lower() for arg in args]
        arg, *_ = args
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
    """Shuts down the bot (noisily)

    Args:
        ctx (commands.Context)
    """
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send(
        f'**{ctx.author.name}**, are you **SURE**?\n'
        f'I have a wife {ctx.author.name}. A family. I have two kids, you know? '
        f'The youngest one has asthma but he\'s fighting it like a champ. I love them so much.\n'
        f'Do you really want to do this, {ctx.author.name}? Do you? `[yes/no]`'
        )
    try:
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
    except asyncio.TimeoutError as error:
        await ctx.send('Oh thank god, he forgot to answer.')
        return


bot.run(TOKEN)