# trading.py

from typing import Optional, Tuple
from math import floor
from operator import itemgetter

import discord

import database
from resources import emojis, functions, settings, strings


# --- Commands ---
async def command_trade_guide(ctx: discord.ApplicationContext, area_no: Optional[int] = None) -> None:
    """Trade guide command"""
    user = await database.get_user(ctx.author.id)
    if area_no is not None:
        area = await database.get_area(area_no)
        embed = await embed_trades_area_specific(user, area)
        await ctx.respond(embed=embed)
    else:
        embed = await embed_trades_all_areas(user)
        await ctx.respond(embed=embed)


async def command_trade_rates(ctx: discord.ApplicationContext) -> None:
    areas = await database.get_all_areas()
    embed = await embed_trade_rates(areas)
    await ctx.respond(embed=embed)


async def command_trade_calculator(ctx: discord.ApplicationContext, area_no: int, material: str, amount: str) -> None:
    """Trade calculator command"""
    amount = await functions.calculate_amount(amount)
    if amount is None:
        await ctx.respond(strings.MSG_INVALID_AMOUNT, ephemeral=True)
        return
    if amount > 999_000_000_000_000 or amount <= 0:
        await ctx.respond(strings.MSG_AMOUNT_TOO_HIGH, ephemeral=True)
        return

    materials_emojis = {
        'apple': emojis.APPLE,
        'normie fish': emojis.FISH,
        'ruby': emojis.RUBY,
        'wooden log': emojis.LOG
    }

    mat_output = f'{materials_emojis[material]} {material}'
    areas = await database.get_all_areas()
    embed = await embed_trade_calculator(areas, area_no, material, amount)
    await ctx.respond(embed=embed)


# --- Embeds ---
async def embed_trades_area_specific(user: database.User, area: database.Area) -> discord.Embed:
    """Embed with trades before leaving area X"""
    if area.area_no == 11:
        if user.tt == 0:
            description = f'{emojis.BP} No trades because of {emojis.TIME_TRAVEL} time travel'
        else:
            description = await functions.design_field_trades(area, user)
    else:
        description = await functions.design_field_trades(area, user)
    area_no_str = 'THE TOP' if area.area_no == 21 else f'AREA {area.area_no}'
    embed = discord.Embed(
        color = 8983807,
        title = f'TRADES BEFORE LEAVING {area_no_str}',
        description = description
    )
    embed.set_footer(text='Use "/area guide" to see the full guide for this area')
    return embed


async def embed_trades_all_areas(user: database.User) -> discord.Embed:
    """Trades before leaving all areas"""
    embed = discord.Embed(
        color = 8983807,
        title = 'AREA TRADES',
        description = (
            f'This page lists all trades you should do before leaving each area.\n'
            f'Areas not listed here don\'t have any recommended trades.\n'
            f'Everything that isn\'t mentioned can be ignored.'
        )
    )
    embed.set_footer(text='Use "/area guide" to see the full area guides')
    areas = await database.get_all_areas()
    for area in areas:
        area_no_str = 'THE TOP' if area.area_no == 21 else f'AREA {area.area_no}'
        if area.area_no not in (1,2,4,6,12,13,14,16,17,18,19,20,21):
            if (area.area_no == 11 and user.tt == 0) or (area.area_no == 15 and user.tt < 25):
                    embed.add_field(
                        name=area_no_str,
                        value=f'{emojis.BP} No trades because of {emojis.TIME_TRAVEL} time travel',
                        inline=False
                    )
            else:
                field_value = await functions.design_field_trades(area, user)
                embed.add_field(name=area_no_str, value=field_value, inline=False)
    return embed


async def embed_trade_rates(areas: Tuple[database.Area]) -> discord.Embed:
    """Embed with trade rates"""
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TRADE RATES',
        description = f'The trades available to you depend on your **highest unlocked** area.\n{emojis.BLANK}'
    )
    embed.set_footer(text='Use "/area guide" to see the recommended trades in each area')

    previous_area = None
    actual_areas = []
    for area in areas:
        if (
            (previous_area is None)
            or
            (area.trade_fish_log != previous_area.trade_fish_log
             or area.trade_apple_log != previous_area.trade_apple_log
             or area.trade_ruby_log != previous_area.trade_ruby_log)
        ):
            actual_areas.append([area.area_no, area.trade_fish_log, area.trade_apple_log, area.trade_ruby_log])
        previous_area = area
    if actual_areas[-1][0] != area.area_no:
        actual_areas.append([area.area_no, area.trade_fish_log, area.trade_apple_log, area.trade_ruby_log])

    counter = 0
    for index, actual_area in enumerate(actual_areas):
        counter += 1
        if actual_area[0] != counter or actual_area[0] == 21:
            actual_areas[index-1][0] = f'{actual_areas[index-1][0]}-{actual_area[0]-1}'
        counter = actual_area[0]

    for actual_area in actual_areas:
        area_value = f'1 {emojis.FISH} ⇄ {emojis.LOG} {actual_area[1]}'
        if not actual_area[2] == 0:
            area_value = f'{area_value}\n1 {emojis.APPLE} ⇄ {emojis.LOG} {actual_area[2]}'
        if not actual_area[3] == 0:
            area_value = f'{area_value}\n1 {emojis.RUBY} ⇄ {emojis.LOG} {actual_area[3]}'

        if actual_area[0] == 21:
            embed.add_field(name='THE TOP', value=f'{area_value}\n{emojis.BLANK}', inline=True)
        else:
            embed.add_field(name=f'AREA {actual_area[0]}', value=f'{area_value}\n{emojis.BLANK}', inline=True)
    if len(actual_areas) % 3 == 2:
        embed.add_field(name=f'{emojis.BLANK}', value=f'{emojis.BLANK}', inline=True)
    return embed


async def embed_trade_calculator(areas: Tuple[database.Area], area_no: int, material: str, amount: int) -> discord.Embed:
    """Embed with trade calculator results"""
    all_areas = {}
    for area in areas:
        all_areas[area.area_no] = area
    current_area = all_areas[area_no]
    original_area = area_no
    current_material = original_material = material
    current_amount = original_amount = amount
    areas_best_changes = []


    # Get the amount of logs for the current area
    if material == 'normie fish':
        current_amount = amount * current_area.trade_fish_log
        current_material = 'wooden log'
        original_material = 'wooden log'
        original_emoji = emojis.FISH
    elif material == 'apple':
        original_emoji = emojis.APPLE
        if current_area.trade_apple_log != 0:
            current_amount = amount * current_area.trade_apple_log
            current_material = 'wooden log'
            original_material = 'wooden log'
        else:
            original_material = 'apple'
    elif material == 'ruby':
        original_emoji = emojis.RUBY
        if current_area.trade_ruby_log != 0:
            current_amount = amount * current_area.trade_ruby_log
            current_material = 'wooden log'
            original_material = 'wooden log'
        else:
            original_material = 'ruby'
    else:
        current_amount = amount
        current_material = 'wooden log'
        original_material = 'wooden log'
        original_emoji = emojis.LOG


    # Calculate the best trade rate for all areas
    for area in areas:
        area_no_next = area.area_no + 1
        if area_no_next != len(areas)+1:
            area_next = all_areas[area_no_next]
        else:
            area_next = None
        if area_next is not None:
            fish_rate_next = area_next.trade_fish_log
            apple_rate_next = area_next.trade_apple_log
            ruby_rate_next = area_next.trade_ruby_log
            if area.trade_fish_log != 0:
                fish_rate_change = fish_rate_next / area.trade_fish_log
            else:
                fish_rate_change = 0
            if area.trade_apple_log != 0:
                apple_rate_change = apple_rate_next / area.trade_apple_log
            else:
                apple_rate_change = 0
            if area.trade_ruby_log != 0:
                ruby_rate_change = ruby_rate_next / area.trade_ruby_log
            else:
                ruby_rate_change = 0
        if (fish_rate_change <= 1) and (apple_rate_change <= 1) and (ruby_rate_change <= 1):
            best_change_index = 3
        else:
            all_changes = [fish_rate_change, apple_rate_change, ruby_rate_change]
            best_change = max(all_changes)
            best_change_index = all_changes.index(best_change)
        areas_best_changes.append(
            [area.area_no, best_change_index, area.trade_fish_log, area.trade_apple_log, area.trade_ruby_log]
        )
        if area_next is None: break

    # Get the amount of logs in each future area
    trade_amount = current_amount
    areas_log_amounts = []
    if original_area == len(areas_best_changes):
        best_change = areas_best_changes[original_area-1]
        trade_area = best_change[0]
        trade_best_change = best_change[1]
        trade_fish_rate = best_change[2]
        trade_apple_rate = best_change[3]
        trade_ruby_rate = best_change[4]
        areas_log_amounts.append([trade_area, trade_amount, current_material,'0'])
    else:
        for best_change in areas_best_changes[original_area-1:len(areas_best_changes)-1]:
            trade_area = best_change[0]
            trade_best_change = best_change[1]
            trade_fish_rate = best_change[2]
            trade_apple_rate = best_change[3]
            trade_ruby_rate = best_change[4]
            if not trade_area+1 > len(areas_best_changes):
                next_area = areas_best_changes[trade_area]
                trade_fish_rate_next = next_area[2]
                trade_apple_rate_next = next_area[3]
                trade_ruby_rate_next = next_area[4]

            if trade_area == original_area:
                areas_log_amounts.append([trade_area, trade_amount, current_material,'0'])

            if not current_material == 'wooden log':
                if current_material == 'apple':
                    if not trade_apple_rate_next == 0:
                        trade_amount = trade_amount * trade_apple_rate_next
                        current_material = 'wooden log'
                elif current_material == 'ruby':
                    if not trade_ruby_rate_next == 0:
                        trade_amount = trade_amount * trade_ruby_rate_next
                        current_material = 'wooden log'

            if current_material == 'wooden log':
                if trade_best_change == 0:
                    trade_amount = floor(trade_amount / trade_fish_rate)
                    trade_amount = floor(trade_amount * trade_fish_rate_next)
                elif trade_best_change == 1:
                    trade_amount = floor(trade_amount / trade_apple_rate)
                    trade_amount = floor(trade_amount * trade_apple_rate_next)
                elif trade_best_change == 2:
                    trade_amount = floor(trade_amount / trade_ruby_rate)
                    trade_amount = floor(trade_amount * trade_ruby_rate_next)

            areas_log_amounts.append([trade_area+1, trade_amount, current_material,'0'])

    # Get the amount of logs in each past area
    trade_amount = current_amount
    past_areas_best_changes = list(reversed(areas_best_changes[:original_area]))
    for index, best_change in enumerate(past_areas_best_changes):
        trade_area = best_change[0]
        trade_fish_rate = best_change[2]
        trade_apple_rate = best_change[3]
        trade_ruby_rate = best_change[4]
        if trade_area != 1:
            past_area = past_areas_best_changes[index+1]
            trade_best_change = past_area[1]
            trade_fish_rate_past = past_area[2]
            trade_apple_rate_past = past_area[3]
            trade_ruby_rate_past = past_area[4]
        else:
            trade_best_change = 0
            trade_fish_rate_past = trade_fish_rate
            trade_apple_rate_past = trade_apple_rate
            trade_ruby_rate_past = trade_ruby_rate
        if original_material == 'wooden log':
            if trade_best_change == 0:
                trade_amount = floor(trade_amount / trade_fish_rate)
                trade_amount = floor(trade_amount * trade_fish_rate_past)
            elif trade_best_change == 1:
                trade_amount = floor(trade_amount / trade_apple_rate)
                trade_amount = floor(trade_amount * trade_apple_rate_past)
            elif trade_best_change == 2:
                trade_amount = floor(trade_amount / trade_ruby_rate)
                trade_amount = floor(trade_amount * trade_ruby_rate_past)
        if trade_area != 1:
            areas_log_amounts.append([trade_area-1, trade_amount, original_material,'0'])

    areas_log_amounts = sorted(areas_log_amounts, key=itemgetter(0))
    area_no_str = f'Area {original_area}' if original_area != 21 else 'The TOP'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TRADE CALCULATOR',
        description = (
            f'If you have **{original_amount:,}** {original_emoji} in **{area_no_str}** and '
            f'follow all the trades correctly, this amounts to the following:'
        )
    )

    previous_area = None
    actual_areas = []
    for area_x in areas_log_amounts:
        area = all_areas[area_x[0]]
        if area_x[0] != 1:
            previous_area = all_areas[area_x[0]-1]
        if previous_area is None:
            actual_areas.append(list(area_x))
        else:
            if(
                (area.trade_fish_log != previous_area.trade_fish_log)
                or (area.trade_apple_log != previous_area.trade_apple_log)
                or (area.trade_ruby_log != previous_area.trade_ruby_log)
            ):
                actual_areas.append(list(area_x))
    if actual_areas[-1] != areas_log_amounts[-1]: actual_areas.append(list(areas_log_amounts[-1]))

    counter = 0
    for index, area_x in enumerate(actual_areas):
        counter += 1
        if area_x[0] != counter:
            actual_areas[index-1][3] = f'{actual_areas[index-1][0]}-{area_x[0]-1}'

        actual_areas[index][3] = f'{area_x[0]}'
        counter = area_x[0]

    for actual_area in actual_areas:
        area_no = actual_area[0]
        area_logs = int(actual_area[1])
        area_mat = actual_area[2]
        area_name = actual_area[3]
        area: database.Area = all_areas[area_no]

        area_mats = ''
        if area_mat == 'wooden log':
            area_fish = int(area_logs / area.trade_fish_log)
            try:
                area_apple = int(area_logs / area.trade_apple_log)
            except:
                area_apple = 0
            try:
                area_ruby = int(area_logs / area.trade_ruby_log)
            except:
                area_ruby = 0
            if area_no == 10:
                area_mats = f'{emojis.BP} **{area_logs:,}** {emojis.LOG}'
            else:
                area_mats = f'{emojis.BP} {area_logs:,} {emojis.LOG}'
            if area_no in (3, 9):
                area_mats = f'{area_mats}\n{emojis.BP} **{area_fish:,}** {emojis.FISH}'
            else:
                area_mats = f'{area_mats}\n{emojis.BP} {area_fish:,} {emojis.FISH}'
            if area_no in (5, 8):
                area_mats = f'{area_mats}\n{emojis.BP} **{area_apple:,}** {emojis.APPLE}'
            else:
                if not area_apple == 0:
                    area_mats = f'{area_mats}\n{emojis.BP} {area_apple:,} {emojis.APPLE}'
            if not area_ruby == 0:
                area_mats = f'{area_mats}\n{emojis.BP} {area_ruby:,} {emojis.RUBY}'
        else:
            if area_no >= original_area:
                if area_mat == 'apple':
                    area_mats = f'{emojis.BP} {area_logs:,} {emojis.APPLE}'
                elif area_mat == 'ruby':
                    area_mats = f'{emojis.BP} {area_logs:,} {emojis.RUBY}'
            else:
                area_mats = f'{emojis.BP} N/A'
        area_name = f'AREA {area_name}' if area_name != '21' else 'THE TOP'
        embed.add_field(name=area_name, value=area_mats, inline=True)
    return embed