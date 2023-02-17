# functions.py

from argparse import ArgumentError
import asyncio
import re
from typing import Any, List, Optional, Union, Tuple

import discord
from discord.utils import MISSING
from discord.ext import commands

import database
from resources import emojis, settings, strings, views


USER_ID_FROM_ICON_URL = re.compile(r"avatars\/(.+?)\/")


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
        await interaction.edit_original_response(content=content, file=file, embed=embed, view=view)


def round_school(number: float) -> int:
    quotient, rest = divmod(number, 1)
    return int(quotient + ((rest >= 0.5) if (number > 0) else (rest > 0.5)))


async def send_slash_migration_message(ctx: commands.Context, new_command: str) -> None:
    """Sends a message telling the user to use slash."""
    await ctx.send(
        f'This is now a slash command:\n'
        f'➜ **{strings.SLASH_COMMANDS_GUIDE[new_command]}**\n'
    )


async def get_result_from_tasks(ctx: discord.ApplicationContext, tasks: List[asyncio.Task]) -> Any:
    """Returns the first result from several running asyncio tasks."""
    try:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    except asyncio.CancelledError:
        return
    for task in pending:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
    try:
        result = list(done)[0].result()
    except asyncio.CancelledError:
        pass
    except asyncio.TimeoutError as error:
        raise
    except Exception as error:
        await database.log_error(error, ctx)
        raise
    return result


async def get_guild_member_by_name(guild: discord.Guild, user_name: str) -> List[discord.Member]:
    """Returns all guild members found by the given name"""
    members = []
    for member in guild.members:
        if await format_string(member.name) == await format_string(user_name) and not member.bot:
            try:
                await database.get_user(member.id)
            except database.FirstTimeUser:
                continue
            members.append(member)
    return members


# --- Regex ---
async def get_match_from_patterns(patterns: List[str], string: str) -> re.Match:
    """Searches a string for a regex patterns out of a list of patterns and returns the first match.
    Returns None if no match is found.
    """
    for pattern in patterns:
        match = re.search(pattern, string, re.IGNORECASE)
        if match is not None: break
    return match


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
            field_value = f'{emojis.BP} Dismantle {emojis.LOG_ULTRA} ULTRA logs and below'
        else:
            field_value = (
                f'{emojis.BP} If crafter <90: Dismantle {emojis.LOG_MEGA} MEGA logs and below\n'
                f'{emojis.BP} If crafter 90+: Dismantle {emojis.LOG_HYPER} HYPER logs and below\n'
                f'{emojis.BP} If crafter 100+: Dismantle {emojis.LOG_ULTRA} ULTRA logs and below'
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
            field_value = (
                f'{emojis.BP} If crafter 100: Dismantle {emojis.LOG_SUPER} SUPER logs and below\n'
                f'{emojis.BP} If crafter 101+: Dismantle {emojis.LOG_MEGA} MEGA logs and below'
            )
        else:
            field_value = (
                f'{emojis.BP} If crafter <90: Dismantle {emojis.LOG_EPIC} EPIC logs\n'
                f'{emojis.BP} If crafter 90-100: Dismantle {emojis.LOG_SUPER} SUPER logs and below\n'
                f'{emojis.BP} If crafter 101+: Dismantle {emojis.LOG_MEGA} MEGA logs and below'
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
        try:
            await edit_interaction(interaction, content=strings.MSG_ABORTED, view=None)
        except discord.errors.NotFound:
            pass
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
    def epic_rpg_check(message_before: discord.Message, message_after: Optional[discord.Message] = None):
        correct_message = False
        message = message_after if message_after is not None else message_before
        if message.embeds:
            embed = message.embeds[0]
            if len(embed.fields) > 1 and embed.author:
                embed_author = format_string(str(embed.author.name))
                icon_url = embed.author.icon_url
                field2 = embed.fields[1].name
                try:
                    search_strings_field = [
                        'about this profession', #English
                        'acerca de esta profesión', #Spanish
                        'sobre esta profissão', #Portuguese
                    ]
                    user_id_match = re.search(USER_ID_FROM_ICON_URL, icon_url)
                    if user_id_match:
                        user_id = int(user_id_match.group(1))
                        search_strings_author = [
                            f'u2014 professions', #All languages
                        ]
                        if (any(search_string in embed_author for search_string in search_strings_author)
                            and any(search_string in field2.lower() for search_string in search_strings_field)
                            and user_id == ctx.author.id):
                            correct_message = True
                    else:
                        ctx_author = format_string(ctx.author.name)
                        search_strings_author = [
                            f'{ctx_author} u2014 professions', #All languages
                        ]
                        if (any(search_string in embed_author for search_string in search_strings_author)
                            and any(search_string in field2.lower() for search_string in search_strings_field)):
                            correct_message = True
                except:
                    pass

        return ((message.author.id in (settings.EPIC_RPG_ID, settings.TESTY_ID)) and (message.channel == ctx.channel)
                and correct_message)

    message_task = asyncio.ensure_future(bot.wait_for('message', check=epic_rpg_check,
                                                      timeout = settings.ABORT_TIMEOUT))
    message_edit_task = asyncio.ensure_future(bot.wait_for('message_edit', check=epic_rpg_check,
                                                           timeout = settings.ABORT_TIMEOUT))
    result = await get_result_from_tasks(ctx, [message_task, message_edit_task])
    return result[1] if isinstance(result, tuple) else result


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
    def epic_rpg_check(message_before: discord.Message, message_after: Optional[discord.Message] = None):
        correct_message = False
        message = message_after if message_after is not None else message_before
        if message.embeds:
            embed = message.embeds[0]
            if embed.author:
                embed_author = format_string(str(embed.author.name))
                icon_url = embed.author.icon_url
                description = embed.description
                try:
                    search_strings_description = [
                        'more information about a profession', #English
                        'más información acerca de una profesión', #Spanish
                        'mais informações sobre uma profissão', #Portuguese
                    ]
                    ctx_author = format_string(ctx.author.name)
                    user_id_match = re.search(USER_ID_FROM_ICON_URL, icon_url)
                    if user_id_match:
                        user_id = int(user_id_match.group(1))
                        search_strings_author = [
                            f'u2014 professions', #All languages
                        ]
                        if (any(search_string in embed_author for search_string in search_strings_author)
                            and any(search_string in description.lower() for search_string in search_strings_description)
                            and user_id == ctx.author.id):
                            correct_message = True
                    else:
                        search_strings_author = [
                            f'{ctx_author} u2014 professions', #All languages
                        ]
                        if (any(search_string in embed_author for search_string in search_strings_author)
                            and any(search_string in description.lower() for search_string in search_strings_description)):
                            correct_message = True
                except:
                    pass

        return ((message.author.id in (settings.EPIC_RPG_ID, settings.TESTY_ID)) and (message.channel == ctx.channel)
                and correct_message)

    message_task = asyncio.ensure_future(bot.wait_for('message', check=epic_rpg_check,
                                                      timeout = settings.ABORT_TIMEOUT))
    message_edit_task = asyncio.ensure_future(bot.wait_for('message_edit', check=epic_rpg_check,
                                                           timeout = settings.ABORT_TIMEOUT))
    result = await get_result_from_tasks(ctx, [message_task, message_edit_task])
    return result[1] if isinstance(result, tuple) else result


async def wait_for_world_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the world embed from EPIC RPG"""
    def epic_rpg_check(message_before: discord.Message, message_after: Optional[discord.Message] = None):
        correct_message = False
        message = message_after if message_after is not None else message_before
        if message.embeds:
            embed = message.embeds[0]
            if len(embed.fields) > 1:
                try:
                    search_strings = [
                        'daily monster', #English
                        'monstruo diario', #Spanish
                        'monstro diário', #Portuguese
                    ]
                    if any(search_string in embed.fields[1].name.lower() for search_string in search_strings):
                        correct_message = True
                except:
                    pass

        return ((message.author.id in (settings.EPIC_RPG_ID, settings.TESTY_ID)) and (message.channel == ctx.channel)
                and correct_message)

    message_task = asyncio.ensure_future(bot.wait_for('message', check=epic_rpg_check,
                                                      timeout = settings.ABORT_TIMEOUT))
    message_edit_task = asyncio.ensure_future(bot.wait_for('message_edit', check=epic_rpg_check,
                                                           timeout = settings.ABORT_TIMEOUT))
    result = await get_result_from_tasks(ctx, [message_task, message_edit_task])
    return result[1] if isinstance(result, tuple) else result


async def wait_for_boosts_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the boosts list from EPIC RPG"""
    def epic_rpg_check(message_before: discord.Message, message_after: Optional[discord.Message] = None):
        correct_message = False
        message = message_after if message_after is not None else message_before
        if message.embeds:
            embed = message.embeds[0]
            if embed.author:
                embed_author = format_string(str(embed.author.name))
                icon_url = embed.author.icon_url
                try:
                    user_id_match = re.search(USER_ID_FROM_ICON_URL, icon_url)
                    if user_id_match:
                        user_id = int(user_id_match.group(1))
                        search_strings = [
                            f'u2014 boosts', #All languages
                        ]
                        if (any(search_string in embed_author for search_string in search_strings)
                            and user_id == ctx.author.id):
                            correct_message = True
                    else:
                        ctx_author = format_string(ctx.author.name)
                        search_strings = [
                            f'{ctx_author} u2014 boosts', ##All languages
                        ]
                        if any(search_string in embed_author for search_string in search_strings):
                            correct_message = True
                except:
                    pass

        return ((message.author.id in (settings.EPIC_RPG_ID, settings.TESTY_ID)) and (message.channel == ctx.channel)
                and correct_message)

    message_task = asyncio.ensure_future(bot.wait_for('message', check=epic_rpg_check,
                                                      timeout = settings.ABORT_TIMEOUT))
    message_edit_task = asyncio.ensure_future(bot.wait_for('message_edit', check=epic_rpg_check,
                                                           timeout = settings.ABORT_TIMEOUT))
    result = await get_result_from_tasks(ctx, [message_task, message_edit_task])
    return result[1] if isinstance(result, tuple) else result


async def wait_for_horse_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the horse embed from EPIC RPG"""
    def epic_rpg_check(message_before: discord.Message, message_after: Optional[discord.Message] = None):
        correct_message = False
        message = message_after if message_after is not None else message_before
        if message.embeds:
            embed = message.embeds[0]
            if embed.author:
                embed_author = format_string(str(embed.author.name))
                icon_url = embed.author.icon_url
                try:
                    user_id_match = re.search(USER_ID_FROM_ICON_URL, icon_url)
                    if user_id_match:
                        user_id = int(user_id_match.group(1))
                        search_strings = [
                            f'u2014 horse', #All languages
                        ]
                        if (any(search_string in embed_author for search_string in search_strings)
                            and user_id == ctx.author.id):
                            correct_message = True
                    else:
                        ctx_author = format_string(ctx.author.name)
                        search_strings = [
                            f'{ctx_author} u2014 horse', ##All languages
                        ]
                        if any(search_string in embed_author for search_string in search_strings):
                            correct_message = True
                except:
                    pass

        return ((message.author.id in (settings.EPIC_RPG_ID, settings.TESTY_ID)) and (message.channel == ctx.channel)
                and correct_message)

    message_task = asyncio.ensure_future(bot.wait_for('message', check=epic_rpg_check,
                                                      timeout = settings.ABORT_TIMEOUT))
    message_edit_task = asyncio.ensure_future(bot.wait_for('message_edit', check=epic_rpg_check,
                                                           timeout = settings.ABORT_TIMEOUT))
    result = await get_result_from_tasks(ctx, [message_task, message_edit_task])
    return result[1] if isinstance(result, tuple) else result


async def wait_for_profile_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the profile embed from EPIC RPG"""
    def epic_rpg_check(message_before: discord.Message, message_after: Optional[discord.Message] = None):
        correct_message = False
        message = message_after if message_after is not None else message_before
        if message.embeds:
            embed = message.embeds[0]
            if embed.author:
                embed_author = format_string(str(embed.author.name))
                icon_url = embed.author.icon_url
                try:
                    user_id_match = re.search(USER_ID_FROM_ICON_URL, icon_url)
                    if user_id_match:
                        user_id = int(user_id_match.group(1))
                        search_strings = [
                            f'u2014 profile', ##All languages
                        ]
                        if (any(search_string in embed_author for search_string in search_strings)
                            and user_id == ctx.author.id):
                            correct_message = True
                    else:
                        ctx_author = format_string(ctx.author.name)
                        search_strings = [
                            f'{ctx_author} u2014 profile', ##All languages
                        ]
                        if any(search_string in embed_author for search_string in search_strings):
                            correct_message = True
                except:
                    pass

        return ((message.author.id in (settings.EPIC_RPG_ID, settings.TESTY_ID)) and (message.channel == ctx.channel)
                and correct_message)

    message_task = asyncio.ensure_future(bot.wait_for('message', check=epic_rpg_check,
                                                      timeout = settings.ABORT_TIMEOUT))
    message_edit_task = asyncio.ensure_future(bot.wait_for('message_edit', check=epic_rpg_check,
                                                           timeout = settings.ABORT_TIMEOUT))
    result = await get_result_from_tasks(ctx, [message_task, message_edit_task])
    return result[1] if isinstance(result, tuple) else result


async def wait_for_profile_or_progress_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the profile embed from EPIC RPG"""
    def epic_rpg_check(message_before: discord.Message, message_after: Optional[discord.Message] = None):
        correct_message = False
        message = message_after if message_after is not None else message_before
        if message.embeds:
            embed = message.embeds[0]
            if embed.author:
                embed_author = format_string(str(embed.author.name))
                icon_url = embed.author.icon_url
                try:
                    user_id_match = re.search(USER_ID_FROM_ICON_URL, icon_url)
                    if user_id_match:
                        user_id = int(user_id_match.group(1))
                        search_strings = [
                            f'u2014 profile', ##All languages
                            f'u2014 progress', ##All languages
                        ]
                        if (any(search_string in embed_author for search_string in search_strings)
                            and user_id == ctx.author.id):
                            correct_message = True
                    else:
                        ctx_author = format_string(ctx.author.name)
                        search_strings = [
                            f'{ctx_author} u2014 profile', ##All languages
                            f'{ctx_author} u2014 progress', ##All languages
                        ]
                        if any(search_string in embed_author for search_string in search_strings):
                            correct_message = True
                except:
                    pass

        return ((message.author.id in (settings.EPIC_RPG_ID, settings.TESTY_ID)) and (message.channel == ctx.channel)
                and correct_message)

    message_task = asyncio.ensure_future(bot.wait_for('message', check=epic_rpg_check,
                                                      timeout = settings.ABORT_TIMEOUT))
    message_edit_task = asyncio.ensure_future(bot.wait_for('message_edit', check=epic_rpg_check,
                                                           timeout = settings.ABORT_TIMEOUT))
    result = await get_result_from_tasks(ctx, [message_task, message_edit_task])
    return result[1] if isinstance(result, tuple) else result


async def wait_for_profile_or_stats_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the profile OR the stats embed from EPIC RPG"""
    def epic_rpg_check(message_before: discord.Message, message_after: Optional[discord.Message] = None):
        correct_message = False
        message = message_after if message_after is not None else message_before
        if message.embeds:
            embed = message.embeds[0]
            if embed.author:
                embed_author = format_string(str(embed.author.name))
                icon_url = embed.author.icon_url
                try:
                    user_id_match = re.search(USER_ID_FROM_ICON_URL, icon_url)
                    if user_id_match:
                        user_id = int(user_id_match.group(1))
                        search_strings = [
                            f'u2014 profile', ##All languages
                            f'u2014 stats', ##All languages
                        ]
                        if (any(search_string in embed_author for search_string in search_strings)
                            and user_id == ctx.author.id):
                            correct_message = True
                    else:
                        ctx_author = format_string(ctx.author.name)
                        search_strings = [
                            f'{ctx_author} u2014 profile', ##All languages
                            f'{ctx_author} u2014 stats', ##All languages
                        ]
                        if any(search_string in embed_author for search_string in search_strings):
                            correct_message = True
                except:
                    pass

        return ((message.author.id in (settings.EPIC_RPG_ID, settings.TESTY_ID)) and (message.channel == ctx.channel)
                and correct_message)

    message_task = asyncio.ensure_future(bot.wait_for('message', check=epic_rpg_check,
                                                      timeout = settings.ABORT_TIMEOUT))
    message_edit_task = asyncio.ensure_future(bot.wait_for('message_edit', check=epic_rpg_check,
                                                           timeout = settings.ABORT_TIMEOUT))
    result = await get_result_from_tasks(ctx, [message_task, message_edit_task])
    return result[1] if isinstance(result, tuple) else result


async def wait_for_inventory_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the inventory embed from EPIC RPG"""
    def epic_rpg_check(message_before: discord.Message, message_after: Optional[discord.Message] = None):
        correct_message = False
        message = message_after if message_after is not None else message_before
        if message.embeds:
            embed = message.embeds[0]
            if embed.author:
                embed_author = format_string(str(embed.author.name))
                icon_url = embed.author.icon_url
                try:
                    user_id_match = re.search(USER_ID_FROM_ICON_URL, icon_url)
                    if user_id_match:
                        user_id = int(user_id_match.group(1))
                        search_strings = [
                            f'u2014 inventory', #All languages
                        ]
                        if (any(search_string in embed_author for search_string in search_strings)
                            and user_id == ctx.author.id):
                            correct_message = True
                    else:
                        ctx_author = format_string(ctx.author.name)
                        search_strings = [
                            f'{ctx_author} u2014 inventory', ##All languages
                        ]
                        if any(search_string in embed_author for search_string in search_strings):
                            correct_message = True
                except:
                    pass

        return ((message.author.id in (settings.EPIC_RPG_ID, settings.TESTY_ID)) and (message.channel == ctx.channel)
                and correct_message)

    message_task = asyncio.ensure_future(bot.wait_for('message', check=epic_rpg_check,
                                                      timeout = settings.ABORT_TIMEOUT))
    message_edit_task = asyncio.ensure_future(bot.wait_for('message_edit', check=epic_rpg_check,
                                                           timeout = settings.ABORT_TIMEOUT))
    result = await get_result_from_tasks(ctx, [message_task, message_edit_task])
    return result[1] if isinstance(result, tuple) else result


async def wait_for_guild_message(bot: commands.Bot, ctx: discord.ApplicationContext) -> discord.Message:
    """Waits for and returns the message with the guild stats embed from EPIC RPG
    Note that this embed does not contain any user information, so this supports slash command only.
    """
    def epic_rpg_check(message_before: discord.Message, message_after: Optional[discord.Message] = None):
        correct_message = False
        message = message_after if message_after is not None else message_before
        try:
            if message.interaction is not None and message.embeds:
                embed_footer = message.embeds[0].footer.text
                search_strings = [
                    'your guild was raided', #English
                    'tu guild fue raideado', #Spanish
                    'sua guild foi raidad', #Portuguese
                ]
                if (any(search_string in embed_footer.lower() for search_string in search_strings)
                    and message.interaction.user == ctx.author):
                    correct_message = True
        except:
            pass
        return ((message.author.id in (settings.EPIC_RPG_ID, settings.TESTY_ID)) and (message.channel == ctx.channel)
                and correct_message)

    message_task = asyncio.ensure_future(bot.wait_for('message', check=epic_rpg_check,
                                                      timeout = settings.ABORT_TIMEOUT))
    message_edit_task = asyncio.ensure_future(bot.wait_for('message_edit', check=epic_rpg_check,
                                                           timeout = settings.ABORT_TIMEOUT))
    result = await get_result_from_tasks(ctx, [message_task, message_edit_task])
    return result[1] if isinstance(result, tuple) else result


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
    for profession in strings.PROFESSIONS.keys():
        if profession in pr_field.name.lower():
            profession_found = strings.PROFESSIONS[profession]
    search_patterns_level = [
        'level\*\*: (.+?) \(', #English
        'nivel\*\*: (.+?) \(', #Spanish
        'nível\*\*: (.+?) \(', #Portuguese
    ]
    level_match = await get_match_from_patterns(search_patterns_level, pr_field.value.lower())
    xp_match = re.search('xp\*\*: (.+?)/(.+?)$', pr_field.value.lower())
    try:
        level = int(level_match.group(1))
        current_xp = int(xp_match.group(1).replace(',',''))
        needed_xp = int(xp_match.group(2).replace(',',''))
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
    profession_translations = []
    for translation, profession_en in strings.PROFESSIONS.items():
        if profession_en == profession:
            profession_translations.append(translation)
    fields = bot_message.embeds[0].fields
    for field in fields:
        for profession_translation in profession_translations:
            if profession_translation in field.name.lower():
                search_patterns = [
                    'lv (.+?) \|', #English
                    'nv (.+?) \|', #Spanish, Portuguese
                ]
                level_match = await get_match_from_patterns(search_patterns, field.name.lower())
                try:
                    level = level_match.group(1)
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


async def extract_data_from_world_embed(ctx: discord.ApplicationContext,
                                                bot_message: discord.Message) -> str:
    """Extracts data from the world embed.

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.

    Returns
    -------
    Dict{
        'profession': str,
        'monster': str,
        'monster boost': bool,
        'lootbox boost': bool,
    }

    Raises
    ------
    ValueError if something goes wrong during extraction.
    Also logs the errors to the database.
    """
    world_data = {}
    profession_field = bot_message.embeds[0].fields[0]
    mob_field = bot_message.embeds[0].fields[1]
    boosts_field = bot_message.embeds[0].fields[2]

    profession_search = re.search(', \*\*(.+?)\*\* ', profession_field.value.lower())
    try:
        profession_name = profession_search.group(1)
    except Exception as error:
        await database.log_error(f'Weekly profession not found in world message: {profession_field}', ctx)
        raise ValueError(error)
    world_data['profession'] = profession_name

    name_search = re.search('> \*\*(.+?)\*\*', mob_field.value.lower())
    try:
        mob_name = name_search.group(1)
    except Exception as error:
        await database.log_error(f'Monster name not found in world message: {mob_field}', ctx)
        raise ValueError(error)
    world_data['monster'] = mob_name

    general_boosts = boosts_field.value.split('\n')
    monster_boost = False
    lootbox_boost = False
    if '|' in general_boosts[0]: monster_boost = True
    if '|' in general_boosts[1]: lootbox_boost = True
    world_data['monster boost'] = monster_boost
    world_data['lootbox boost'] = lootbox_boost

    return world_data


async def extract_data_from_boosts_embed(ctx: discord.ApplicationContext,
                                                bot_message: discord.Message) -> Tuple[str]:
    """Extracts active items from the boosts embed.

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.

    Returns
    -------
    Dict = {
        'active items': Tuple[str]
        'monster drop chance': int
        'profession xp': int
        'selling price': int
    }


    Raises
    ------
    ValueError if something goes wrong during extraction.
    Also logs the errors to the database.
    """
    boosts_data = {}
    potion_fields = boost_fields = ''
    for field in bot_message.embeds[0].fields:
        if potion_fields == '':
            potion_fields = field.value
        elif field.name == '':
            if boost_fields == '':
                potion_fields = f'{potion_fields}\n{field.value}'
            else:
                boost_fields = f'{boost_fields}\n{field.value}'
        else:
            boost_fields = field.value
    active_items = []
    for line in potion_fields.lower().split('\n'):
        item_name_search = re.search('> \*\*(.+?)\*\*:', line)
        try:
            item_name = item_name_search.group(1)
            active_items.append(item_name)
        except:
            continue
    boosts_data['active items'] = active_items

    monster_drop_chance = profession_xp = selling_price = 0
    for line in boost_fields.lower().split('\n'):
        monster_drops_match = re.search(' monster drops\*\*: \+(.+?)%', line)
        profession_xp_match = re.search(' profession xp\*\*: \+(.+?)%', line)
        selling_price_match = re.search(' sell price\*\*: \+(.+?)%', line)
        if monster_drops_match: monster_drop_chance += int(monster_drops_match.group(1).replace('.00',''))
        if profession_xp_match: profession_xp += int(profession_xp_match.group(1).replace('.00',''))
        if selling_price_match: selling_price += int(selling_price_match.group(1).replace('.00',''))
    boosts_data['monster drop chance'] = monster_drop_chance
    boosts_data['profession xp'] = profession_xp
    boosts_data['selling price'] = selling_price

    return boosts_data


async def extract_horse_data_from_horse_embed(ctx: discord.ApplicationContext,
                                              bot_message: discord.Message) -> dict:
    """Extracts horse tier and level from a horse embed.

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.

    Returns
    -------
    Dict[
        'tier': int,
        'level': int,
        'boost': float,
        'drop_chance': float,
    ]

    Raises
    ------
    ValueError if something goes wrong during extraction.
    Also logs the errors to the database.
    """
    data_field = bot_message.embeds[0].fields[0]
    search_patterns_tier = [
        'tier\*\* - (.+?) <', #English
        'tier del? caballo\*\* - (.+?) <', #Spanish
        'tier d[eo] cavalo\*\* - (.+?) <', #Portuguese
    ]
    search_patterns_level = [
        'level\*\* - (.+?) \(', #English 1
        'level\*\* - (.+?)\\n', #English 2
        'nivel del? caballo\*\* - (.+?) \(', #Spanish 1
        'nivel del? caballo\*\* - (.+?)\\n', #Spanish 2
        'nível d[eo] cavalo\*\* - (.+?) ?\(', #Portuguese 1
        'nível d[eo] cavalo\*\* - (.+?)\\n', #Portuguese 2
    ]
    search_patterns_boost = [
        'boost\*\* - (.+?)%', #English
        'boost del? caballo\*\* - (.+?)%', #Spanish
        'boost d[eo] cavalo\*\* - (.+?)%', #Portuguese
    ]
    search_patterns_epicness = [
        'epicness\*\* - (.+?)\n', #English
        'epicidad del? caballo\*\* - (.+?)\n', #Spanish
        'epicidade d[eo] cavalo\*\* - (.+?)\n', #Portuguese
    ]
    tier_match = await get_match_from_patterns(search_patterns_tier, data_field.value.lower())
    level_match = await get_match_from_patterns(search_patterns_level, data_field.value.lower())
    boost_match = await get_match_from_patterns(search_patterns_boost, data_field.value.lower())
    epicness_match = await get_match_from_patterns(search_patterns_epicness, data_field.value.lower())
    horse_data = {}
    try:
        tier = tier_match.group(1)
        horse_data['tier'] = int(strings.NUMBERS_ROMAN_INTEGER[tier])
        horse_data['level'] = int(level_match.group(1))
        horse_data['boost'] = float(boost_match.group(1))
        horse_data['epicness'] = int(epicness_match.group(1)) if epicness_match else 0
    except Exception as error:
        await database.log_error(f'Error extracting horse data in horse message: {data_field}', ctx)
        raise ValueError(error)

    return horse_data


async def extract_data_from_profile_embed(ctx: discord.ApplicationContext,
                                                   bot_message: discord.Message) -> Tuple[int, int]:
    """Extracts the following data from a profile embed:
    - level
    - max area
    - time travel
    - at
    - def
    - life
    - sword
    - sword enchant
    - armor
    - armor enchant
    - horse type (english)

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.

    Returns
    -------
    Dict[
        area_max: int (21 for top),
        armor: Item,
        at: int,
        def: int,
        enchant_armor: str ('' if no enchant),
        enchant_sword: str ('' if no enchant),
        horse_type: str,
        level: int,
        life: int,
        sword: Item,
        time_travel: int,
    ]

    Raises
    ------
    ValueError if something goes wrong during extraction.
    Also logs the errors to the database.
    """
    field_progress = bot_message.embeds[0].fields[0]
    field_stats = bot_message.embeds[0].fields[1]
    field_equipment = bot_message.embeds[0].fields[2]
    sword, armor, horse_type = field_equipment.value.split('\n')
    search_patterns_tt = [
        'time travels\*\*: (.+?)$', #English
        'viajes en el tiempo\*\*: (.+?)$', #Spanish
        'viagens no tempo\*\*: (.+?)$', #Portuguese
    ]
    search_patterns_area = [
        'max: (.+?)\)', #All languages
    ]
    search_patterns_level = [
        'level\*\*: (.+?)\(', #English & Spanish
        'n[ií]vel\*\*: (.+?)\(', #Spanish & Portuguese
    ]
    area_match = await get_match_from_patterns(search_patterns_area, field_progress.value.lower())
    at_match = re.search(r'at\*\*: (.+?)\n', field_stats.value.lower())
    def_match = re.search(r'def\*\*: (.+?)\n', field_stats.value.lower())
    armor_match = re.search(r'<:(.+?):', armor.lower())
    enchant_armor_match = re.search(r'\[(.+?)]', armor)
    sword_match = re.search(r'<:(.+?):', sword.lower())
    enchant_sword_match = re.search(r'\[(.+?)]', sword)
    horse_type_match = re.search(r'\[(.+?)]', horse_type.lower())
    level_match = await get_match_from_patterns(search_patterns_level, field_progress.value.lower())
    life_match = re.search(r'life\*\*: (.+?)\/(.+?)$', field_stats.value.lower())
    tt_match = await get_match_from_patterns(search_patterns_tt, field_progress.value.lower())
    profile_data = {}
    try:
        area_max = area_match.group(1)
        profile_data['area_max'] = 21 if area_max.lower() == 'top' else int(area_max)
        if armor_match:
            armor_name = strings.ITEM_ALIASES.get(armor_match.group(1), None)
            if armor_name is not None:
                armor_item = await database.get_item(armor_name)
            else:
                armor_item = None
        else:
            armor_item = None
        if sword_match:
            sword_name = strings.ITEM_ALIASES.get(sword_match.group(1), None)
            if sword_name is not None:
                sword_item = await database.get_item(sword_name)
            else:
                sword_item = None
        else:
            sword_item = None
        profile_data['armor'] = armor_item
        profile_data['sword'] = sword_item
        profile_data['at'] = int(at_match.group(1))
        profile_data['def'] = int(def_match.group(1))
        profile_data['level'] = int(level_match.group(1))
        profile_data['life'] = int(life_match.group(2))
        if enchant_armor_match:
            profile_data['enchant_armor'] = enchant_armor_match.group(1)
        else:
            profile_data['enchant_armor'] = 'No'
        if enchant_sword_match:
            profile_data['enchant_sword'] = enchant_sword_match.group(1)
        else:
            profile_data['enchant_sword'] = 'No'
        horse_type = horse_type_match.group(1)
        if horse_type in strings.HORSE_TYPES_ENGLISH: horse_type = strings.HORSE_TYPES_ENGLISH[horse_type]
        profile_data['horse_type'] = horse_type
        profile_data['time_travel'] = int(tt_match.group(1)) if tt_match is not None else 0
    except Exception as error:
        await database.log_error(
            f'Error extracting data in profile message: {error}\n'
            f'{field_progress}, {field_stats}, {field_equipment}',
            ctx
        )
        raise ValueError(error)

    return profile_data


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
    search_patterns_tt = [
        'time travels\*\*: (.+?)$', #English
        'viajes en el tiempo\*\*: (.+?)$', #Spanish
        'viagens no tempo\*\*: (.+?)$', #Portuguese
    ]
    search_patterns_area = [
        'max: (.+?)\)', #English & Spanish
    ]
    tt_match = await get_match_from_patterns(search_patterns_tt, progress_field.value.lower())
    area_match = await get_match_from_patterns(search_patterns_area, progress_field.value.lower())
    try:
        tt = int(tt_match.group(1)) if tt_match is not None else 0
        area = area_match.group(1)
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


async def extract_duel_bonus_from_guild_embed(ctx: discord.ApplicationContext,
                                              bot_message: discord.Message) -> int:
    """Extracts the guild duel bonus from a guild stats embed.

    Arguments
    ---------
    ctx: Context.
    bot_message: Message the data is extracted from.

    Returns
    -------
    int

    Raises
    ------
    ValueError if something goes wrong during extraction.
    Also logs the errors to the database.
    """
    progress_field = bot_message.embeds[0].fields[0]
    search_patterns = [
        'duel bonus\*\*: (.+?)%', #English
        'bonus en duel\*\*: (.+?)%', #Spanish
        'bônus de duel\*\*: (.+?)%', #Portuguese
    ]
    duel_bonus_match = await get_match_from_patterns(search_patterns, progress_field.value.lower())
    if duel_bonus_match:
        duel_bonus = int(duel_bonus_match.group(1))
    else:
        error = f'Error extracting duel bonus in guild stats message: {progress_field}'
        await database.log_error(
            f'Error extracting duel bonus in guild stats message: {progress_field}',
            ctx
        )
        raise ValueError(error)

    return duel_bonus


# Calculation
async def inventory_get(inventory: str, material: str) -> int:
    """Extracts the amount of a material from an inventory"""
    material_match = re.search(fr'\*\*{material}\*\*: (.+?)\n', inventory)
    return int(material_match.group(1).replace(',','')) if material_match else 0


async def get_inventory_value(area: database.Area, item: database.Item, inventory: str) -> int:
    """Calculate item amount from an inventory"""
    inventory = inventory.lower()
    fish = await inventory_get(inventory, 'normie fish')
    fishgolden = await inventory_get(inventory, 'golden fish')
    fishepic = await inventory_get(inventory, 'epic fish')
    log = await inventory_get(inventory, 'wooden log')
    logepic = await inventory_get(inventory, 'epic log')
    logsuper = await inventory_get(inventory, 'super log')
    logmega = await inventory_get(inventory, 'mega log')
    loghyper = await inventory_get(inventory, 'hyper log')
    logultra = await inventory_get(inventory, 'ultra log')
    apple = await inventory_get(inventory, 'apple')
    banana = await inventory_get(inventory, 'banana')
    ruby = await inventory_get(inventory, 'ruby')

    # Calculate logs
    if item.name.lower() == 'wooden log':
        loghyper_calc = loghyper + (logultra * 8)
        logmega_calc = logmega + (loghyper_calc * 8)
        logsuper_calc = logsuper + (logmega_calc * 8)
        logepic_calc = logepic + (logsuper_calc * 8)
        log_calc = log + (logepic_calc * 20)
        fishgolden_calc = fishgolden + (fishepic * 80)
        fish_calc = fish + (fishgolden_calc * 12)
        apple_calc = apple + (banana * 12)
        log_calc = log_calc + (fish_calc * area.trade_fish_log)
        if area.area_no in (1,2):
            log_calc = log_calc + (apple_calc * 3)
            log_calc = log_calc + (ruby * 450)
        elif area.area_no in (3,4):
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * 450)
        else:
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * area.trade_ruby_log)
        result_value = log_calc

    # Calculate epic logs
    if item.name.lower() == 'epic log':
        loghyper_calc = loghyper + (logultra * 8)
        logmega_calc = logmega + (loghyper_calc * 8)
        logsuper_calc = logsuper + (logmega_calc * 8)
        fishgolden_calc = fishgolden + (fishepic * 80)
        fish_calc = fish + (fishgolden_calc * 12)
        apple_calc = apple + (banana * 12)
        log_calc = log + (fish_calc * area.trade_fish_log)
        if area.area_no in (1,2):
            log_calc = log_calc + (apple_calc * 3)
            log_calc = log_calc + (ruby * 450)
        elif area.area_no in (3,4):
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * 450)
        else:
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * area.trade_ruby_log)
        logepic_calc = logepic + (logsuper_calc * 8) + log_calc // 25
        result_value = logepic_calc

    # Calculate super logs
    if item.name.lower() == 'super log':
        loghyper_calc = loghyper + (logultra * 8)
        logmega_calc = logmega + (loghyper_calc * 8)
        fishgolden_calc = fishgolden + (fishepic * 80)
        fish_calc = fish + (fishgolden_calc * 12)
        apple_calc = apple + (banana * 12)
        log_calc = log + (fish_calc * area.trade_fish_log)
        if area.area_no in (1,2):
            log_calc = log_calc + (apple_calc * 3)
            log_calc = log_calc + (ruby * 450)
        elif area.area_no in (3,4):
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * 450)
        else:
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * area.trade_ruby_log)
        logepic_calc = logepic + log_calc // 25
        logsuper_calc = logsuper + (logmega_calc * 8) + (logepic_calc // 10)
        result_value = logsuper_calc

    # Calculate mega logs
    if item.name.lower() == 'mega log':
        loghyper_calc = loghyper + (logultra * 8)
        fishgolden_calc = fishgolden + (fishepic * 80)
        fish_calc = fish + (fishgolden_calc * 12)
        apple_calc = apple + (banana * 12)
        log_calc = log + (fish_calc * area.trade_fish_log)
        if area.area_no in (1,2):
            log_calc = log_calc + (apple_calc * 3)
            log_calc = log_calc + (ruby * 450)
        elif area.area_no in (3,4):
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * 450)
        else:
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * area.trade_ruby_log)
        logepic_calc = logepic + log_calc // 25
        logsuper_calc = logsuper + (logepic_calc // 10)
        logmega_calc = logmega + (loghyper_calc * 8) + (logsuper_calc // 10)
        result_value = logmega_calc

    # Calculate hyper logs
    if item.name.lower() == 'hyper log':
        fishgolden_calc = fishgolden + (fishepic * 80)
        fish_calc = fish + (fishgolden_calc * 12)
        apple_calc = apple + (banana * 12)
        log_calc = log + (fish_calc * area.trade_fish_log)
        if area.area_no in (1,2):
            log_calc = log_calc + (apple_calc * 3)
            log_calc = log_calc + (ruby * 450)
        elif area.area_no in (3,4):
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * 450)
        else:
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * area.trade_ruby_log)
        logepic_calc = logepic + log_calc // 25
        logsuper_calc = logsuper + (logepic_calc // 10)
        logmega_calc = logmega + (logsuper_calc // 10)
        loghyper_calc = loghyper + (logultra * 8) + (logmega_calc // 10)
        result_value = loghyper_calc

    # Calculate ultra logs
    if item.name.lower() == 'ultra log':
        fishgolden_calc = fishgolden + (fishepic * 80)
        fish_calc = fish + (fishgolden_calc * 12)
        apple_calc = apple + (banana * 12)
        log_calc = log + (fish_calc * area.trade_fish_log)
        if area.area_no in (1,2):
            log_calc = log_calc + (apple_calc * 3)
            log_calc = log_calc + (ruby * 450)
        elif area.area_no in (3,4):
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * 450)
        else:
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * area.trade_ruby_log)
        logepic_calc = logepic + log_calc // 25
        logsuper_calc = logsuper + (logepic_calc // 10)
        logmega_calc = logmega + (logsuper_calc // 10)
        loghyper_calc = loghyper + (logmega_calc // 10)
        logultra_calc = logultra + (loghyper_calc // 10)
        result_value = logultra_calc

    # Calculate normie fish
    if item.name.lower() == 'normie fish':
        fishgolden_calc = fishgolden + (fishepic * 80)
        fish_calc = fish + (fishgolden_calc * 12)
        loghyper_calc = loghyper + (logultra * 8)
        logmega_calc = logmega + (loghyper_calc * 8)
        logsuper_calc = logsuper + (logmega_calc * 8)
        logepic_calc = logepic + (logsuper_calc * 8)
        log_calc = log + (logepic_calc * 20)
        apple_calc = apple + (banana * 12)
        if area.area_no in (1,2):
            log_calc = log_calc + (apple_calc * 3)
            fish_calc = fish_calc + (ruby * 225)
        elif area.area_no in (3,4):
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            fish_calc = fish_calc + (ruby * 225)
        else:
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * area.trade_ruby_log)
        fish_calc = fish_calc + (log_calc // area.trade_fish_log)
        result_value = fish_calc

    # Calculate golden fish
    if item.name.lower() == 'golden fish':
        loghyper_calc = loghyper + (logultra * 8)
        logmega_calc = logmega + (loghyper_calc * 8)
        logsuper_calc = logsuper + (logmega_calc * 8)
        logepic_calc = logepic + (logsuper_calc * 8)
        log_calc = log + (logepic_calc * 20)
        apple_calc = apple + (banana * 12)
        if area.area_no in (1,2):
            log_calc = log_calc + (apple_calc * 3)
            fish_calc = fish + (ruby * 225)
        elif area.area_no in (3,4):
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            fish_calc = fish + (ruby * 225)
        else:
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * area.trade_ruby_log)
            fish_calc = fish
        fish_calc = fish_calc + (log_calc // area.trade_fish_log)
        fishgolden_calc = fishgolden + (fishepic * 80) + (fish_calc // 15)
        result_value = fishgolden_calc

    # Calculate epic fish
    if item.name.lower() == 'epic fish':
        loghyper_calc = loghyper + (logultra * 8)
        logmega_calc = logmega + (loghyper_calc * 8)
        logsuper_calc = logsuper + (logmega_calc * 8)
        logepic_calc = logepic + (logsuper_calc * 8)
        log_calc = log + (logepic_calc * 20)
        apple_calc = apple + (banana * 12)
        if area.area_no in (1,2):
            log_calc = log_calc + (apple_calc * 3)
            fish_calc = fish + (ruby * 225)
        elif area.area_no in (3,4):
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            fish_calc = fish + (ruby * 225)
        else:
            fish_calc = fish
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
            log_calc = log_calc + (ruby * area.trade_ruby_log)
        fish_calc = fish_calc + (log_calc // area.trade_fish_log)
        fishgolden_calc = fishgolden + (fish_calc // 15)
        fishepic_calc = fishepic + (fishgolden_calc // 100)
        result_value = fishepic_calc

    # Calculate apples
    if item.name.lower() == 'apple':
        loghyper_calc = loghyper + (logultra * 8)
        logmega_calc = logmega + (loghyper_calc * 8)
        logsuper_calc = logsuper + (logmega_calc * 8)
        logepic_calc = logepic + (logsuper_calc * 8)
        log_calc = log + (logepic_calc * 20)
        apple_calc = apple + (banana * 12)
        fishgolden_calc = fishgolden + (fishepic * 80)
        fish_calc = fish + (fishgolden_calc * 12)
        log_calc = log_calc + (fish_calc * area.trade_fish_log)
        if area.area_no in (1,2,3,4):
            log_calc = log_calc + (ruby * 450)
        else:
            log_calc = log_calc + (ruby * area.trade_ruby_log)
        if area.area_no in (1,2):
            apple_calc = apple_calc + (log_calc // 3)
        else:
            apple_calc = apple_calc + (log_calc // area.trade_apple_log)
        result_value = apple_calc

    # Calculate bananas
    if item.name.lower() == 'banana':
        loghyper_calc = loghyper + (logultra * 8)
        logmega_calc = logmega + (loghyper_calc * 8)
        logsuper_calc = logsuper + (logmega_calc * 8)
        logepic_calc = logepic + (logsuper_calc * 8)
        log_calc = log + (logepic_calc * 20)
        fishgolden_calc = fishgolden + (fishepic * 80)
        fish_calc = fish + (fishgolden_calc * 12)
        log_calc = log_calc + (fish_calc * area.trade_fish_log)
        if area.area_no in (1,2,3,4):
            log_calc = log_calc + (ruby * 450)
        else:
            log_calc = log_calc + (ruby * area.trade_ruby_log)
        if area.area_no in (1,2):
            apple_calc = apple + (log_calc // 3)
        else:
            apple_calc = apple + (log_calc // area.trade_apple_log)
        banana_calc = banana + (apple_calc // 15)
        result_value = banana_calc

    # Calculate rubies
    if item.name.lower() == 'ruby':
        loghyper_calc = loghyper + (logultra * 8)
        logmega_calc = logmega + (loghyper_calc * 8)
        logsuper_calc = logsuper + (logmega_calc * 8)
        logepic_calc = logepic + (logsuper_calc * 8)
        log_calc = log + (logepic_calc * 20)
        apple_calc = apple + (banana * 12)
        fishgolden_calc = fishgolden + (fishepic * 80)
        fish_calc = fish + (fishgolden_calc * 12)
        log_calc = log_calc + (fish_calc * area.trade_fish_log)
        if area.area_no in (1,2):
            log_calc = log_calc + (apple_calc * 3)
        else:
            log_calc = log_calc + (apple_calc * area.trade_apple_log)
        if area.area_no in (1,2,3,4):
            ruby_calc = ruby + (log_calc // 450)
        else:
            ruby_calc = ruby + (log_calc // area.trade_ruby_log)
        result_value = ruby_calc

    return result_value