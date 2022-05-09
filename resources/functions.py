# functions.py

from argparse import ArgumentError
import asyncio
import re
from typing import Union, Tuple

import discord
from discord.utils import MISSING
from discord.ext import commands

import database
from resources import emojis, settings, strings, views


def await_coroutine(coro):
    """Function to call a coroutine outside of an async function"""
    while True:
        try:
            coro.send(None)
        except StopIteration as error:
            return error.value


async def edit_interaction(interaction: Union[discord.Interaction, discord.WebhookMessage], **kwargs) -> None:
    """Edits a reponse. The response can either be an interaction OR a WebhookMessage"""
    content = kwargs.get('content', MISSING)
    embed = kwargs.get('embed', MISSING)
    view = kwargs.get('view', MISSING)
    file = kwargs.get('file', MISSING)
    if isinstance(interaction, discord.WebhookMessage):
        await interaction.edit(content=content, embed=embed, view=view)
    else:
        await interaction.edit_original_message(content=content, file=file, embed=embed, view=view)


def round_school(number: float) -> int:
    quotient, rest = divmod(number, 1)
    return int(quotient + ((rest >= 0.5) if (number > 0) else (rest > 0.5)))


# Design fields for embeds
async def design_field_traderate(area: database.Area) -> str:
    """Create field "trade rates" for area & trading"""
    field_value = f'{emojis.BP} 1 {emojis.FISH} ⇄ {emojis.LOG} {area.trade_fish_log}'
    if area.trade_apple_log > 0:
        field_value = f'{field_value}\n{emojis.BP} 1 {emojis.APPLE} ⇄ {emojis.LOG} {area.trade_apple_log}'
    if area.trade_ruby_log > 0:
        field_value = f'{field_value}\n{emojis.BP} 1 {emojis.RUBY} ⇄ {emojis.LOG} {area.trade_ruby_log}'

    return field_value


async def design_field_trades(area: database.Area, user: database.User) -> str:
    """Trades for area X for area & trading"""
    if area.area_no in (1,2,4,6,12,13,14,16,17,18,19,20,21):
        field_value = f'{emojis.BP} None'
    elif area.area_no == 3:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Dismantle {emojis.LOG_ULTRA} ULTRA logs and below\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)\n'
            f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.FISH} fish (B)'
        )
    elif area.area_no == 5:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.LOG_ULTRA} ULTRA logs and below\n'
            f'{emojis.BP} Dismantle {emojis.FISH_EPIC} EPIC fish and below\n'
            f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
            f'{emojis.BP} Trade {emojis.FISH} fish to {emojis.LOG} logs (A)\n'
            f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.APPLE} apples (D)'
        )
    elif area.area_no == 7:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)'
        )
    elif area.area_no == 8:
        if user.ascended:
            field_value = f'{emojis.BP} Dismantle {emojis.LOG_HYPER} HYPER logs and below'
        else:
            field_value = (
                f'{emojis.BP} If crafter <90: Dismantle {emojis.LOG_MEGA} MEGA logs and below\n'
                f'{emojis.BP} If crafter 90+: Dismantle {emojis.LOG_HYPER} HYPER logs and below'
            )
        field_value = (
            f'{field_value}\n'
            f'{emojis.BP} Dismantle {emojis.FISH_EPIC} EPIC fish and below\n'
            f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
            f'{emojis.BP} Trade {emojis.FISH} fish to {emojis.LOG} logs (A)\n'
            f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.APPLE} apples (D)'
        )
    elif area.area_no == 9:
        if user.ascended:
            field_value = f'{emojis.BP} Dismantle {emojis.LOG_SUPER} SUPER logs and below'
        else:
            field_value = (
                f'{emojis.BP} If crafter <90: Dismantle {emojis.LOG_EPIC} EPIC logs\n'
                f'{emojis.BP} If crafter 90+: Dismantle {emojis.LOG_SUPER} SUPER logs and below'
            )
        field_value = (
            f'{field_value}\n'
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)\n'
            f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.FISH} fish (B)'
        )
    elif area.area_no == 10:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)'
        )
    elif area.area_no == 11:
        field_value = f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)'
    elif area.area_no == 15:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.FISH_GOLDEN} golden fish and below\n'
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
            f'{emojis.BP} Trade {emojis.FISH} fish to {emojis.LOG} logs (A)\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)'
        )
    else:
        field_value = f'{emojis.BP} N/A'

    return field_value


async def design_field_rec_gear(dungeon: database.Dungeon) -> str:
    """Create field "Recommended gear. May return None."""
    player_armor_enchant = '' if dungeon.player_armor_enchant is None else f'[{dungeon.player_armor_enchant}]'
    player_sword_enchant = '' if dungeon.player_sword_enchant is None else f'[{dungeon.player_sword_enchant}]'

    field_value = ''
    if dungeon.player_sword is not None:
        field_value = (
            f'{emojis.BP} {dungeon.player_sword.emoji} {dungeon.player_sword.name} {player_sword_enchant}'
        )
    if dungeon.player_armor is not None:
        field_value = (
            f'{field_value}\n{emojis.BP} {dungeon.player_armor.emoji} {dungeon.player_armor.name} '
            f'{player_armor_enchant}'
        )

    if field_value == '': field_value = None
    return field_value


async def design_field_rec_stats(dungeon: database.Dungeon, short_version: bool = False) -> str:
    """Design field "Recommended Stats" for areas & dungeons. NEEDS REFACTORING"""

    player_carry_def = ''
    if dungeon.player_carry_def is not None:
        if short_version:
            player_carry_def = f'({dungeon.player_carry_def})'
        else:
            player_carry_def = f'({dungeon.player_carry_def}+ to carry)'

    player_at = '-' if dungeon.player_at is None else f'{dungeon.player_at:,}'
    player_def = '-' if dungeon.player_def is None else f'{dungeon.player_def:,}'
    player_level = '-' if dungeon.player_level is None else f'{dungeon.player_level:,}'
    player_life = '-' if dungeon.player_life is None else f'{dungeon.player_life:,}'

    field_value = (
        f'{emojis.BP} {emojis.STAT_AT} **AT**: {player_at}\n'
        f'{emojis.BP} {emojis.STAT_DEF} **DEF**: {player_def} {player_carry_def}\n'
        f'{emojis.BP} {emojis.STAT_LIFE} **LIFE**: {player_life}\n'
        f'{emojis.BP} {emojis.STAT_LEVEL} **LEVEL**: {player_level}'
    )
    if 16 <= dungeon.dungeon_no <= 20:
        field_value = (
            f'{field_value}\n'
            f'{emojis.BP} _To be balanced!_'
        )

    return field_value


# Get amount of material in inventory
async def inventory_get(inventory, material):

    if inventory.find(f'**{material}**:') > -1:
        mat_start = inventory.find(f'**{material}**:') + len(f'**{material}**:')+1
        mat_end = inventory.find(f'\\', mat_start)
        mat_end_bottom = inventory.find(f'\'', mat_start)
        mat = inventory[mat_start:mat_end].replace(',','')
        mat_bottom = inventory[mat_start:mat_end_bottom].replace(',','')
        if mat.isnumeric():
            mat = int(mat)
        elif mat_bottom.isnumeric():
            mat = int(mat_bottom)
        else:
            mat = 0
    else:
        mat = 0

    return mat


def round_school(number: float) -> int:
    quotient, rest = divmod(number, 1)
    return int(quotient + ((rest >= 0.5) if (number > 0) else (rest > 0.5)))


def format_string(string: str) -> str:
    """Format string to ASCII"""
    string = (
        string
        .encode('unicode-escape',errors='ignore')
        .decode('ASCII')
        .replace('\\','')
    )
    return string


async def calculate_amount(amount: str) -> int:
    """Returns the actual amount from a text.
    The argument can contain k, m or b (e.g. 100k).
    The calculated amount needs to result in a whole number.

    Returns
    -------
    The amount calculated (int) if valid.
    None if no valid amount could be calculated."""
    if amount.endswith('k'):
        try:
            amount = int(float(amount.replace('k','')) * 1_000)
        except:
            return None
    elif amount.endswith('m'):
        try:
            amount = int(float(amount.replace('m','')) * 1_000_000)
        except:
            return None
    elif amount.endswith('b'):
        try:
            amount = int(float(amount.replace('b','')) * 1_000_000_000)
        except:
            return None
    elif amount.endswith('t'):
        try:
            amount = int(float(amount.replace('t','')) * 1_000_000_000_000)
        except:
            return None
    else:
        try:
            amount = int(amount)
        except:
            return None
    return amount


async def default_footer(prefix):
    footer = f'Use {prefix}guide or {prefix}g to see all available guides.'

    return footer


# Wait for input
async def wait_for_bot_or_abort(ctx: discord.ApplicationContext, bot_message_task: asyncio.coroutine,
                                content: str) -> Union[discord.Message, None]:
    """Sends a message with an abort button that tells the user to input a command.
    This function then waits for both view input and bot_message_task.
    If the bot message task finishes first, the bot message is returned, otherwise return value is None.

    The abort button is removed after this function finishes.
    Make sure that the view timeout is longer than the bot message task timeout to get proper errors.

    Arguments
    ---------
    ctx: Context.
    bot_message_task: The task with the coroutine that waits for the EPIC RPG message.
    content: The content of the message that tells the user what to enter.

    Returns
    -------
    Bot message if message task finished first.
    None if the interaction was aborted or the view timed out first.

    Raises
    ------
    asyncio.TimeoutError if the bot message task timed out before the view timed out.
    This error is also logged to the database.
    """
    view = views.AbortView(ctx)
    interaction = await ctx.respond(content, view=view)
    view.interaction = interaction
    view_task = asyncio.ensure_future(view.wait())
    done, pending = await asyncio.wait([bot_message_task, view_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
    if view.value in ('abort','timeout'):
        await edit_interaction(interaction, content=strings.MSG_ABORTED, view=None)
    elif view.value is None:
        view.stop()
        asyncio.ensure_future(edit_interaction(interaction, view=None))
    bot_message = None
    if bot_message_task.done():
        try:
            bot_message = bot_message_task.result()
        except asyncio.CancelledError:
            pass
        except asyncio.TimeoutError as error:
            raise
        except Exception as error:
            await database.log_error(error, ctx)
            raise

    return bot_message


async def wait_for_profession_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the profession detail embed from EPIC RPG"""
    def epic_rpg_check(message):
        correct_message = False
        try:
            ctx_author = format_string(str(ctx.author.name))
            embed_author = format_string(str(message.embeds[0].author))
            field2 = message.embeds[0].fields[1]
            if f'{ctx_author}\'s professions' in embed_author and 'about this profession' in field2.name.lower():
                correct_message = True
        except:
            pass

        return (message.author.id == settings.EPIC_RPG_ID) and (message.channel == ctx.channel) and correct_message

    bot_message = await bot.wait_for('message', check=epic_rpg_check, timeout = settings.ABORT_TIMEOUT)

    return bot_message


async def wait_for_fun_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for a fun message"""
    def check(message):
        correct_message = False
        try:
            if 'y u ignore me' in message.content.lower() and ctx.author == message.author:
                correct_message = True
        except:
            pass

        return (message.channel == ctx.channel) and correct_message

    bot_message = await bot.wait_for('message', check=check, timeout = settings.ABORT_TIMEOUT)

    return bot_message


async def wait_for_profession_overview_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the profession overview embed from EPIC RPG"""
    def epic_rpg_check(message):
        correct_message = False
        try:
            ctx_author = format_string(str(ctx.author.name))
            embed_author = format_string(str(message.embeds[0].author))
            description = message.embeds[0].description
            if (f'{ctx_author}\'s professions' in embed_author
                and 'more information about a profession' in description.lower()):
                correct_message = True
        except:
            pass

        return (message.author.id == settings.EPIC_RPG_ID) and (message.channel == ctx.channel) and correct_message

    bot_message = await bot.wait_for('message', check=epic_rpg_check, timeout = settings.ABORT_TIMEOUT)

    return bot_message


async def wait_for_world_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the world embed from EPIC RPG"""
    def epic_rpg_check(message):
        correct_message = False
        try:
            field2 = message.embeds[0].fields[1]
            if 'daily monster' in field2.name.lower(): correct_message = True
        except:
            pass

        return (message.author.id == settings.EPIC_RPG_ID) and (message.channel == ctx.channel) and correct_message

    bot_message = await bot.wait_for('message', check=epic_rpg_check, timeout = settings.ABORT_TIMEOUT)

    return bot_message


async def wait_for_horse_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the horse embed from EPIC RPG"""
    def epic_rpg_check(message):
        correct_message = False
        try:
            ctx_author = format_string(str(ctx.author.name))
            embed_author = format_string(str(message.embeds[0].author))
            if f'{ctx_author}\'s horse' in embed_author:
                correct_message = True
        except:
            pass

        return (message.author.id == settings.EPIC_RPG_ID) and (message.channel == ctx.channel) and correct_message

    bot_message = await bot.wait_for('message', check=epic_rpg_check, timeout = settings.ABORT_TIMEOUT)

    return bot_message


async def wait_for_profile_or_progress_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the profile embed from EPIC RPG"""
    def epic_rpg_check(message):
        correct_message = False
        try:
            ctx_author = format_string(str(ctx.author.name))
            embed_author = format_string(str(message.embeds[0].author))
            if f'{ctx_author}\'s profile' in embed_author or f'{ctx_author}\'s progress' in embed_author:
                correct_message = True
        except:
            pass

        return (message.author.id == settings.EPIC_RPG_ID) and (message.channel == ctx.channel) and correct_message

    bot_message = await bot.wait_for('message', check=epic_rpg_check, timeout = settings.ABORT_TIMEOUT)

    return bot_message


async def wait_for_profile_or_stats_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the profile OR the stats embed from EPIC RPG"""
    def epic_rpg_check(message):
        correct_message = False
        try:
            ctx_author = format_string(str(ctx.author.name))
            embed_author = format_string(str(message.embeds[0].author))
            if f'{ctx_author}\'s profile' in embed_author or f'{ctx_author}\'s stats' in embed_author:
                correct_message = True
        except:
            pass

        return (message.author.id == settings.EPIC_RPG_ID) and (message.channel == ctx.channel) and correct_message

    bot_message = await bot.wait_for('message', check=epic_rpg_check, timeout = settings.ABORT_TIMEOUT)

    return bot_message


async def wait_for_inventory_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the inventory embed from EPIC RPG"""
    def epic_rpg_check(message):
        correct_message = False
        try:
            ctx_author = format_string(str(ctx.author.name))
            embed_author = format_string(str(message.embeds[0].author))
            if f'{ctx_author}\'s inventory' in embed_author:
                correct_message = True
        except:
            pass

        return (message.author.id == settings.EPIC_RPG_ID) and (message.channel == ctx.channel) and correct_message

    bot_message = await bot.wait_for('message', check=epic_rpg_check, timeout = settings.ABORT_TIMEOUT)

    return bot_message


# Extract values from game embeds
async def extract_data_from_profession_embed(ctx: discord.ApplicationContext,
                                             bot_message: discord.Message) -> Tuple[str, int, int, int]:
    """Extracts profession name and level from a profession embed.

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.

    Returns
    -------
    Tuple[
        Profession name: str,
        level: int,
        current xp: int,
        xp needed for next level: int
    ]

    Raises
    ------
    ValueError if something goes wrong during extraction.
    Also logs the errors to the database.
    """
    pr_field = bot_message.embeds[0].fields[0]
    profession_found = None
    for profession in strings.PROFESSIONS:
        if profession in pr_field.name.lower():
            profession_found = profession

    level_search = re.search('level\*\*: (.+?) \(', pr_field.value.lower())
    xp_search = re.search('xp\*\*: (.+?)/(.+?)$', pr_field.value.lower())
    try:
        level = int(level_search.group(1))
        current_xp = int(xp_search.group(1).replace(',',''))
        needed_xp = int(xp_search.group(2).replace(',',''))
    except Exception as error:
        await database.log_error(f'{profession_found.capitalize} data not found in profession message: {pr_field}', ctx)
        raise ValueError(error)

    return (profession_found, level, current_xp, needed_xp)


async def extract_data_from_profession_overview_embed(ctx: discord.ApplicationContext,
                                                      bot_message: discord.Message, profession: str) -> Tuple[str, int]:
    """Extracts the level for a profession from a profession embed.

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.
    profession: Name of the profession you want the level for.

    Returns
    -------
    Tuple[
        Profession name: str,
        level: int,
    ]

    Raises
    ------
    ValueError if something goes wrong during extraction.
    ArgumentError if the desired profession wasn't found.
    Also logs the errors to the database.
    """
    profession = profession.lower()
    if profession not in strings.PROFESSIONS:
        raise ArgumentError(f'Profession {profession} is not a valid profession.')
    fields = bot_message.embeds[0].fields
    for field in fields:
        if profession in field.name.lower():
            try:
                level = re.search('lv (.+?) \|', field.name.lower()).group(1)
                level = int(level)
            except Exception as error:
                await database.log_error(
                    f'{profession.capitalize} data not found in profession overview message field: {field}',
                    ctx
                )
                await database.log_error(error, ctx)
                raise ValueError(error)
            break
    return (profession, level)


async def extract_monster_name_from_world_embed(ctx: discord.ApplicationContext,
                                                bot_message: discord.Message) -> str:
    """Extracts monster name from the world embed.

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.

    Returns
    -------
    monster name: str

    Raises
    ------
    ValueError if something goes wrong during extraction.
    Also logs the errors to the database.
    """
    mob_field = bot_message.embeds[0].fields[1]
    name_search = re.search('> \*\*(.+?)\*\*', mob_field.value.lower())
    try:
        mob_name = name_search.group(1)
    except Exception as error:
        await database.log_error(f'Monster name not found in world message: {mob_field}', ctx)
        raise ValueError(error)

    return mob_name


async def extract_horse_data_from_horse_embed(ctx: discord.ApplicationContext,
                                              bot_message: discord.Message) -> Tuple[int, int]:
    """Extracts horse tier and level from a horse embed.

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.

    Returns
    -------
    Tuple[
        horse tier: int,
        horse level: int
    ]

    Raises
    ------
    ValueError if something goes wrong during extraction.
    Also logs the errors to the database.
    """
    data_field = bot_message.embeds[0].fields[0]
    tier_search = re.search('tier\*\* - (.+?) <', data_field.value.lower())
    level_search = re.search('level\*\* - (.+?) \(', data_field.value.lower())
    if level_search is None:
        level_search = re.search('level\*\* - (.+?)\\n', data_field.value.lower())
    try:
        tier = tier_search.group(1)
        tier = int(strings.NUMBERS_ROMAN_INTEGER[tier])
        level = int(level_search.group(1))
    except Exception as error:
        await database.log_error(f'Error extracting horse data in horse message: {data_field}', ctx)
        raise ValueError(error)

    return (tier, level)


async def extract_progress_data_from_profile_or_progress_embed(ctx: discord.ApplicationContext,
                                                   bot_message: discord.Message) -> Tuple[int, int]:
    """Extracts tt and max area from a profile embed.

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.

    Returns
    -------
    Tuple[
        current tt: int,
        max area: int (21 for top)
    ]

    Raises
    ------
    ValueError if something goes wrong during extraction.
    Also logs the errors to the database.
    """
    progress_field = bot_message.embeds[0].fields[0]
    tt_search = re.search('time travels\*\*: (.+?)$', progress_field.value.lower())
    area_search = re.search('max: (.+?)\)', progress_field.value.lower())
    try:
        tt = int(tt_search.group(1)) if tt_search is not None else 0
        area = area_search.group(1)
        if area.lower() == 'top': area = '21'
        area = int(area)
    except Exception as error:
        await database.log_error(
            f'Error extracting progress data in profile or progress message: {progress_field}',
            ctx
        )
        raise ValueError(error)

    return (tt, area)


async def extract_stats_from_profile_or_stats_embed(ctx: discord.ApplicationContext,
                                                    bot_message: discord.Message) -> Tuple[int, int, int]:
    """Extracts at, def and life from a profile or stats embed.

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.

    Returns
    -------
    Tuple[
        at: int,
        def: int,
        life: int
    ]

    Raises
    ------
    ValueError if something goes wrong during extraction.
    Also logs the errors to the database.
    """
    embed_author = str(bot_message.embeds[0].author)
    if 'profile' in embed_author:
        stats_field = bot_message.embeds[0].fields[1]
    else:
        stats_field = bot_message.embeds[0].fields[0]
    at_search = re.search('at\*\*: (.+?)\\n', stats_field.value.lower())
    def_search = re.search('def\*\*: (.+?)\\n', stats_field.value.lower())
    life_search = re.search('life\*\*: (.+?)\/(.+?)$', stats_field.value.lower())
    try:
        user_at = int(at_search.group(1))
        user_def = int(def_search.group(1))
        user_life = int(life_search.group(2))
    except Exception as error:
        await database.log_error(
            f'Error extracting stats in profile or stats message: {stats_field}',
            ctx
        )
        raise ValueError(error)

    return (user_at, user_def, user_life)