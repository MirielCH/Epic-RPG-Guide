# crafting.py

import asyncio
from typing import Optional, Union

import discord

from content import trading
import database
from resources import emojis
from resources import settings
from resources import functions, strings, views


DROP_BASIC = 'Normal drops (A1~A15)'
DROP_DARK_ENERGY = 'Dark Energy (A16~A20)'
DROP_EPIC_BERRY = 'EPIC berry'

DROP_TYPES = [
    DROP_BASIC,
    DROP_DARK_ENERGY,
    DROP_EPIC_BERRY,
]


# --- Commands ---
async def command_dropchance_calculator(bot: discord.Bot, ctx: discord.ApplicationContext,
                                        drop_type: str, timetravel: Optional[int] = None,
                                        horse_tier: Optional[int] = None,
                                        horse_epicness: Optional[int] = None) -> None:
    """Dropchance calculator command"""
    if timetravel is None:
        user: database.User = await database.get_user(ctx.author.id)
        timetravel = user.tt
    horse_data = {}
    if horse_tier is None or horse_epicness is None:
        bot_message_task = asyncio.ensure_future(functions.wait_for_horse_message(bot, ctx))
        try:
            content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                                command=strings.SLASH_COMMANDS_EPIC_RPG["horse stats"])
            bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
        except asyncio.TimeoutError:
            await ctx.respond(
                strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='horse'),
                ephemeral=True
            )
            return
        if bot_message is None: return
        horse_data = await functions.extract_horse_data_from_horse_embed(ctx, bot_message)
    if horse_tier is not None: horse_data['tier'] = horse_tier
    if horse_epicness is not None: horse_data['epicness'] = horse_epicness
    view = views.DropChanceCalculatorView(ctx, embed_dropchance, DROP_TYPES, drop_type, timetravel, horse_data)
    embed = await embed_dropchance(drop_type, timetravel, horse_data)
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    try:
        await functions.edit_interaction(interaction, view=None)
    except discord.errors.NotFound:
        pass


async def command_crafting_calculator(ctx: discord.ApplicationContext, item_name: str, amount: Union[str, int]) -> None:
    """Craft command"""
    item_name = item_name.replace('\n',' ')
    if len(item_name) > 200:
        await ctx.respond('Really?', ephemeral=True)
        return
    if isinstance(amount, str):
        amount = await functions.calculate_amount(amount)
        if amount is None:
            await ctx.respond(strings.MSG_INVALID_AMOUNT, ephemeral=True)
            return
        if amount < 1:
            await ctx.respond(strings.MSG_AMOUNT_TOO_LOW, ephemeral=True)
            return
        if amount > 999_000_000_000_000:
            await ctx.respond(strings.MSG_AMOUNT_TOO_HIGH, ephemeral=True)
            return
    #await ctx.defer()
    original_item_name = item_name
    item_name = item_name.lower()
    item_name = (
        item_name.replace('logs','log')
        .replace('ultra edgy','ultra-edgy')
        .replace('ultra omega','ultra-omega')
        .replace('uo ','ultra-omega ')
        .replace('creatures','creature')
        .replace('salads','salad')
        .replace('juices','juice')
        .replace('cookies','cookie')
        .replace('pickaxes','pickaxe')
        .replace('lootboxes','lootbox')
        .replace(' lb',' lootbox')
        .replace('sandwiches','sandwich')
        .replace('apples','apple')
        .replace('oranges','orange')
    )
    if item_name in strings.ITEM_ALIASES: item_name = strings.ITEM_ALIASES[item_name]
    try:
        item: database.Item = await database.get_item(item_name)
    except database.NoDataFound:
        await ctx.respond(f'Uhm, I don\'t know how to craft `{original_item_name}`, sorry.')
        return
    if item.item_type in ('sword', 'armor') and amount > 1:
        await ctx.respond(f'You can only craft 1 {item.emoji} `{item.name}`.')
        return
    if not item.ingredients:
        await ctx.respond(f'{item.emoji} `{item.name}` can not be crafted.')
        return
    breakdown_totals = await get_item_breakdown(item, amount)
    if amount == 1:
        message = f'To craft {item.emoji} `{item.name}` you need:'
    else:
        message = f'To craft **{amount:,}** {item.emoji} `{item.name}` you need:'
    for ingredient in item.ingredients:
        ingredient_item: database.Item = await database.get_item(ingredient.name)
        message = f'{message}\n> {ingredient.amount * amount:,} {ingredient_item.emoji} `{ingredient_item.name}`'
    if item.requirements is not None:
        message = f'{message}\n\nRequirements\n> {item.requirements}'
    if breakdown_totals != '':
        message = f'{message}\n\n{breakdown_totals}'
    if item.item_type in ('sword', 'armor'):
        await ctx.respond(message)
    else:
        view = views.FollowupCraftingCalculatorView(ctx, item.name, item.emoji, 'Calculate again')
        interaction = await ctx.respond(message, view=view)
        view.interaction = interaction
        await view.wait()
        if view.value == 'triggered':
            try:
                await functions.edit_interaction(interaction, view=None)
            except discord.errors.NotFound:
                pass


async def command_dismantling_calculator(ctx: discord.ApplicationContext, item_name: str, amount: str) -> None:
    """Dismantle command"""
    item_name = item_name.replace('\n',' ')
    if len(item_name) > 200:
        await ctx.respond('Really?', ephemeral=True)
        return
    amount = await functions.calculate_amount(amount)
    if amount is None:
        await ctx.respond(strings.MSG_INVALID_AMOUNT, ephemeral=True)
        return
    if amount > 999_000_000_000_000:
        await ctx.respond(strings.MSG_AMOUNT_TOO_HIGHT, ephemeral=True)
        return
    await ctx.defer()
    original_item_name = item_name
    item_name = item_name.lower()
    if item_name == 'brandon':
        await ctx.respond('I WILL NEVER ALLOW THAT. YOU MONSTER.')
        return
    if item_name in strings.ITEM_ALIASES:
        item_name = strings.ITEM_ALIASES[item_name]
    try:
        item: database.Item = await database.get_item(item_name)
    except database.NoDataFound:
        await ctx.respond(f'Uhm, I don\'t know an item called `{original_item_name}`, sorry.')
        return
    if not item.dismanteable:
        await ctx.respond(f'{item.emoji} `{item.name}` can not be dismantled.')
        return
    breakdown_totals = await get_item_breakdown(item, amount, dismantle=True)
    if amount == 1:
        message = f'By dismantling {item.emoji} `{item.name}` you get:'
    else:
        message = f'By dismantling **{amount:,}** {item.emoji} `{item.name}` you get:'
    for ingredient in item.ingredients:
        ingredient_item: database.Item = await database.get_item(ingredient.name)
        message = f'{message}\n> {int(ingredient.amount * amount * 0.8):,} {ingredient_item.emoji} `{ingredient_item.name}`'
    if breakdown_totals != '':
        message = f'{message}\n\n{breakdown_totals}'
    await ctx.respond(message)


async def command_inventory_calculator(bot: discord.Bot, ctx: discord.ApplicationContext, area_no: int,
                                       material: str) -> None:
    """Inventory calculator command"""
    bot_message_task = asyncio.ensure_future(functions.wait_for_inventory_message(bot, ctx))
    try:
        content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                          command=strings.SLASH_COMMANDS_EPIC_RPG["inventory"])
        bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
    except asyncio.TimeoutError:
        await ctx.respond(
            strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='inventory'),
            ephemeral=True
        )
        return
    if bot_message is None: return
    inventory = ''
    for field in bot_message.embeds[0].fields:
        inventory = f'{inventory}{field.value}\n'
    item: database.Item = await database.get_item(material)
    area: database.Area = await database.get_area(area_no)
    amount = await get_inventory_value(area, item, inventory)
    area_no_str = f'area **{area.area_no}**' if area.area_no != 21 else '**the TOP**'
    message = (
        f'Your inventory equals **{amount:,}** {item.emoji} {item.name}.\n'
        f'This calculation assumes you are in {area_no_str} now.'
    )
    if area.area_no in (1,2):
        message = (
            f'{message}\n\n'
            f'Apples and rubies are included in the calculation as follows:\n'
            f'{emojis.BP} 1 {emojis.APPLE} = 3 {emojis.LOG} = 3 {emojis.FISH} (trade value in A3)\n'
            f'{emojis.BP} 1 {emojis.RUBY} = 450 {emojis.LOG} = 225 {emojis.FISH}(trade value in A5)\n'
        )
    elif area.area_no in (3,4):
        message = (
            f'{message}\n\n'
            f'Rubies are included in the calculation as follows:\n'
            f'{emojis.BP} 1 {emojis.RUBY} = 450 {emojis.LOG} = 225 {emojis.FISH} (trade value in A5)\n'
        )
    if material in ('apple', 'normie fish', 'ruby', 'wooden log'):
        view = views.FollowupCommandView(ctx, 'Calculate trades')
        interaction = await ctx.respond(message, view=view)
        view.interaction = interaction
        await view.wait()
        if view.value == 'followup':
            await trading.command_trade_calculator(ctx, area_no, material, str(amount))
            await functions.edit_interaction(interaction, view=None)
    else:
        await ctx.respond(message)


# --- Functions ---
async def get_item_breakdown(item: database.Item, amount: int, dismantle: bool = False) -> str:
    """Generate item breakdown"""
    log_total = fish_total = apple_total = 0
    breakdown = ''
    multiplier = 0.8 if dismantle else 1
    base_totals = {}

    for ingredient in item.ingredients:
        ingredient_item: database.Item = await database.get_item(ingredient.name)
        if ingredient.name == 'wooden log':
            log_total += ingredient.amount * amount * multiplier
        elif ingredient.name == 'normie fish':
            fish_total += ingredient.amount * amount * multiplier
        elif ingredient.name == 'apple':
            apple_total += ingredient.amount * amount * multiplier
        if not ingredient_item.ingredients:
            if ingredient_item.item_type not in ('log', 'fish', 'fruit'):
                base_totals[ingredient.name] = (ingredient.amount * amount, ingredient_item.emoji)
            continue
        if ingredient_item.item_type not in ('log', 'fish', 'fruit'): continue
        current_ingredient = ingredient
        current_breakdown = ''
        current_amount = amount
        while True:
            current_amount = current_amount * current_ingredient.amount * multiplier
            if current_ingredient.name == 'wooden log':
                log_total += current_amount
            elif current_ingredient.name == 'normie fish':
                fish_total += current_amount
            elif current_ingredient.name == 'apple':
                apple_total += current_amount
            sub_item: database.Item = await database.get_item(current_ingredient.name)
            if current_breakdown == '':
                current_breakdown = f'> {int(current_amount):,} {sub_item.emoji}'
            else:
                current_breakdown = f'{current_breakdown} ➜ {int(current_amount):,} {sub_item.emoji}'
            if not sub_item.ingredients:
                breakdown = f'{breakdown}\n{current_breakdown}'
                break
            current_ingredient = sub_item.ingredients[0] # If he ever makes more sub ingredients, this will break

    message = ''
    if '➜' in breakdown:
        if dismantle:
            message = f'Full breakdown\n{breakdown.strip()}'
            return message.strip()
        message = f'Ingredients breakdown\n{breakdown.strip()}'
        message = f'{message}\n\nBase materials total'
        message = message.strip()
        if (log_total > 0 or fish_total > 0 or apple_total > 0) and not dismantle:
            if apple_total > 0: base_totals['apple'] = (apple_total, emojis.APPLE)
            if fish_total > 0: base_totals['normie fish'] = (fish_total, emojis.FISH)
            if log_total > 0: base_totals['wooden log'] = (log_total, emojis.LOG)
        for name, amount_emoji in sorted(base_totals.items(), key=lambda item: item[1][0]):
            message = f'{message}\n> {amount_emoji[0]:,} {amount_emoji[1]} `{name}`'

    return message.strip()


async def get_inventory_value(area: database.Area, item: database.Item, inventory: str) -> int:
    """Calculate item amount from an inventory"""
    inventory = inventory.lower()
    fish = await functions.inventory_get(inventory, 'normie fish')
    fishgolden = await functions.inventory_get(inventory, 'golden fish')
    fishepic = await functions.inventory_get(inventory, 'epic fish')
    log = await functions.inventory_get(inventory, 'wooden log')
    logepic = await functions.inventory_get(inventory, 'epic log')
    logsuper = await functions.inventory_get(inventory, 'super log')
    logmega = await functions.inventory_get(inventory, 'mega log')
    loghyper = await functions.inventory_get(inventory, 'hyper log')
    logultra = await functions.inventory_get(inventory, 'ultra log')
    apple = await functions.inventory_get(inventory, 'apple')
    banana = await functions.inventory_get(inventory, 'banana')
    ruby = await functions.inventory_get(inventory, 'ruby')

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
            log_calc = log_calc + (ruby * 225)
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
            log_calc = log_calc + (ruby * 225)
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


# --- Embeds ---
async def embed_dropchance(drop_type: str, timetravel: int, horse_data: dict) -> discord.Embed:
    """Dropchance"""
    tt_chance = (49 + timetravel) * timetravel / 2 / 100
    horse_chance = strings.HORSE_MULTIPLIER_DROPS[horse_data['tier']] * (1 + (horse_data['epicness'] // 5 * 0.04))
    horse_emoji = getattr(emojis, f'HORSE_T{horse_data["tier"]}')

    if drop_type == DROP_DARK_ENERGY:
        base_chance = 0.1
        drop_description = f'{emojis.DARK_ENERGY} **Dark energy**'
    elif drop_type == DROP_EPIC_BERRY:
        base_chance = 0.01
        drop_description = f'{emojis.EPIC_BERRY} **EPIC berry**'
    else:
        base_chance = 4
        drop_description = (
            f'{emojis.WOLF_SKIN}{emojis.ZOMBIE_EYE}{emojis.UNICORN_HORN}{emojis.MERMAID_HAIR}'
            f'{emojis.CHIP}{emojis.DRAGON_SCALE} **Normal drops**'
        )

    # Calculations
    drop_chance = base_chance * (1 + tt_chance) * horse_chance
    drop_chance_worldbuff = round(drop_chance * 1.2, 3)
    drop_chance_daily = round(drop_chance * 1.1, 3)
    drop_chance_worldbuff_daily = round(drop_chance * 1.3, 3)
    drop_chance_hm = round(drop_chance * 1.7, 3)
    drop_chance_worldbuff_hm = round(drop_chance * 1.2 * 1.7, 3)
    drop_chance_daily_hm = round(drop_chance * 1.1 * 1.7, 3)
    drop_chance_worldbuff_daily_hm = round(drop_chance * 1.3 * 1.7, 3)
    drop_chance = round(drop_chance, 3)
    if drop_chance >= 100: drop_chance = 100
    if drop_chance_worldbuff >= 100: drop_chance_worldbuff = 100
    if drop_chance_daily >= 100: drop_chance_daily = 100
    if drop_chance_worldbuff_daily >= 100: drop_chance_worldbuff_daily = 100
    if drop_chance_hm >= 100: drop_chance_hm = 100
    if drop_chance_worldbuff_hm >= 100: drop_chance_worldbuff_hm = 100
    if drop_chance_daily_hm >= 100: drop_chance_daily_hm = 100
    if drop_chance_worldbuff_daily_hm >= 100: drop_chance_worldbuff_daily_hm = 100
    f"{drop_chance:.3f}".rstrip('0').rstrip('.')
    field_drop_chance = (
        f'{emojis.BP} Base chance: `{drop_chance:g}`%\n'
        f'{emojis.BP} With active world buff: `{drop_chance_worldbuff:g}`%\n'
        f'{emojis.BP} If mob is daily mob: `{drop_chance_daily:g}`%\n'
        f'{emojis.BP} With active world buff _and_ mob as daily mob: `{drop_chance_worldbuff_daily:g}`%\n'
    )
    field_drop_chance_hardmode = (
        f'{emojis.BP} Base chance: `{drop_chance_hm:g}`%\n'
        f'{emojis.BP} With active world buff: `{drop_chance_worldbuff_hm:g}`%\n'
        f'{emojis.BP} If mob is daily mob: `{drop_chance_daily_hm:g}`%\n'
        f'{emojis.BP} With active world buff _and_ mob as daily mob: `{drop_chance_worldbuff_daily_hm:g}`%\n'
    )
    if drop_type == DROP_DARK_ENERGY:
        field_encounter_chance = (
            f'{emojis.BP} Every mob in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} can drop this item\n'
        )
    elif drop_type == DROP_EPIC_BERRY:
        field_encounter_chance = (
            f'{emojis.BP} Every mob in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} and '
            f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} can drop this item\n'
        )
    else:
        field_encounter_chance = (
            f'{emojis.BP} You have a 50% chance of encountering a mob in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
            f'that can drop an item\n'
            f'{emojis.DETAIL} Thus, the chance to get an item while hunting is __half__ of the values above\n'
        )
    embed = discord.Embed(
        title = 'DROP CHANCE CALCULATOR',
        color = settings.EMBED_COLOR,
        description = (
            f'{emojis.BP} Drop type: {drop_description}\n'
            f'{emojis.BP} Time travel: {emojis.TIME_TRAVEL} **{timetravel}**\n'
            f'{emojis.BP} Horse tier: {horse_emoji} **T{horse_data["tier"]}**\n'
            f'{emojis.BP} Horse epicness: **{horse_data["epicness"]}**\n'
        )
    )
    embed.add_field(name='NORMAL', value=field_drop_chance, inline=False)
    embed.add_field(name='HARDMODE', value=field_drop_chance_hardmode, inline=False)
    embed.add_field(name='ENCOUNTER CHANCE', value=field_encounter_chance, inline=False)
    return embed