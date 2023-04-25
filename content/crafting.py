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
DROP_EPIC_BERRY = 'EPIC berries'
DROP_LOOTBOX = 'Lootboxes'

DROP_TYPES = [
    DROP_BASIC,
    DROP_DARK_ENERGY,
    DROP_EPIC_BERRY,
    DROP_LOOTBOX,
]


# --- Commands ---
async def command_dropchance_calculator(bot: discord.Bot, ctx: discord.ApplicationContext,
                                        drop_type: str, timetravel: Optional[int] = None,
                                        horse_tier: Optional[int] = None,
                                        horse_epicness: Optional[int] = None,
                                        mob_world_boost: Optional[bool] = None,
                                        lootbox_world_boost: Optional[bool] = None,
                                        mob_boost_percentage: Optional[int] = None,
                                        lootbox_boost_percentage: Optional[int] = None) -> None:
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
    if mob_world_boost is None or lootbox_world_boost is None:
        bot_message_task = asyncio.ensure_future(functions.wait_for_world_message(bot, ctx))
        try:
            content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                            command=strings.SLASH_COMMANDS_EPIC_RPG["world"])
            bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
        except asyncio.TimeoutError:
            await ctx.respond(
                strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='world'),
                ephemeral=True
            )
            return
        if bot_message is None: return
        world_data = await functions.extract_data_from_world_embed(ctx, bot_message)
        mob_world_boost = world_data['monster boost']
        lootbox_world_boost = world_data['lootbox boost']
    if mob_boost_percentage is None or lootbox_boost_percentage is None:
        mob_boost_percentage = lootbox_boost_percentage = 0
        bot_message_task = asyncio.ensure_future(functions.wait_for_boosts_message(bot, ctx))
        try:
            content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                              command=strings.SLASH_COMMANDS_EPIC_RPG["boosts"])
            bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
        except asyncio.TimeoutError:
            await ctx.respond(
                strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='boosts'),
                ephemeral=True
            )
            return
        if bot_message is None: return
        boosts_data = await functions.extract_data_from_boosts_embed(ctx, bot_message)
        mob_boost_percentage = boosts_data['monster drop chance']
        lootbox_boost_percentage = boosts_data['lootbox drop chance']
    view = views.DropChanceCalculatorView(ctx, embed_dropchance, DROP_TYPES, drop_type, timetravel, horse_data,
                                          mob_world_boost, lootbox_world_boost, mob_boost_percentage,
                                          lootbox_boost_percentage)
    world_boost = lootbox_world_boost if drop_type == DROP_LOOTBOX else mob_world_boost
    boost_percentage = lootbox_boost_percentage if drop_type == DROP_LOOTBOX else mob_boost_percentage
    embed = await embed_dropchance(drop_type, timetravel, horse_data, world_boost, boost_percentage)
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
    amount = await functions.get_inventory_value(area, item, inventory)
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
        view = views.FollowupCommandView(ctx.author, 'Calculate trades')
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


# --- Embeds ---
async def embed_dropchance(drop_type: str, timetravel: int, horse_data: dict,
                           world_boost: bool, boost_percentage: int) -> discord.Embed:
    """Dropchance"""
    tt_chance = (49 + timetravel) * timetravel / 2 / 100
    horse_emoji = getattr(emojis, f'HORSE_T{horse_data["tier"]}')
    if drop_type == DROP_DARK_ENERGY:
        base_chance = 0.1
        drop_description = f'**Dark energy** {emojis.DARK_ENERGY} '
        horse_chance = strings.HORSE_MULTIPLIER_DROPS[horse_data['tier']] * (1 + (horse_data['epicness'] // 5 * 0.04))
    elif drop_type == DROP_EPIC_BERRY:
        base_chance = 0.01
        drop_description = f'**EPIC berries** {emojis.EPIC_BERRY}'
        horse_chance = strings.HORSE_MULTIPLIER_DROPS[horse_data['tier']] * (1 + (horse_data['epicness'] // 5 * 0.04))
    elif drop_type == DROP_LOOTBOX:
        base_chance = 2
        base_chance_adv = 10
        drop_description = (
            f'**Lootboxes**'
        )
        horse_chance = strings.HORSE_MULTIPLIER_LOOTBOX[horse_data['tier']] * (1 + (horse_data['epicness'] // 5 * 0.04))
    else:
        base_chance = 4
        drop_description = (
            f'**Normal drops** {emojis.WOLF_SKIN}{emojis.ZOMBIE_EYE}{emojis.UNICORN_HORN}{emojis.MERMAID_HAIR}'
            f'{emojis.CHIP}{emojis.DRAGON_SCALE}'
        )
        horse_chance = strings.HORSE_MULTIPLIER_DROPS[horse_data['tier']] * (1 + (horse_data['epicness'] // 5 * 0.04))

    embed = discord.Embed(
        title = 'DROP CHANCE CALCULATOR',
        color = settings.EMBED_COLOR,
        description = (
            f'{emojis.BP} Drop type: {drop_description}\n'
            f'{emojis.BP} Time travel: {emojis.TIME_TRAVEL} **{timetravel}**\n'
            f'{emojis.BP} Horse tier: {horse_emoji} **T{horse_data["tier"]}**\n'
            f'{emojis.BP} Horse epicness: **{horse_data["epicness"]}**\n'
            f'{emojis.BP} World boost active: **{"Yes" if world_boost else "No"}**\n'
            f'{emojis.BP} Boost percentage: **{boost_percentage}%**\n'
        )
    )

    # Calculations
    multiplier = 1.2 if world_boost else 1
    multiplier *= 1 + (boost_percentage / 100)
    
    if drop_type != DROP_LOOTBOX:
        drop_chance = base_chance * (1 + tt_chance) * horse_chance * multiplier
        drop_chance_daily = round(drop_chance * 1.3, 3)
        drop_chance_hm = round(drop_chance * 1.7, 3)
        drop_chance_daily_hm = round(drop_chance * 1.3 * 1.7, 3)
        drop_chance = round(drop_chance, 3)
        if drop_chance >= 100: drop_chance = 100
        if drop_chance_daily >= 100: drop_chance_daily = 100
        if drop_chance_hm >= 100: drop_chance_hm = 100
        if drop_chance_daily_hm >= 100: drop_chance_daily_hm = 100
        field_drop_chance = (
            f'{emojis.BP} Base chance: `{drop_chance:g}`%\n'
            f'{emojis.BP} If mob is daily mob: `{drop_chance_daily:g}`%\n'
        )
        field_drop_chance_hardmode = (
            f'{emojis.BP} Base chance: `{drop_chance_hm:g}`%\n'
            f'{emojis.BP} If mob is daily mob: `{drop_chance_daily_hm:g}`%\n'
        )
        embed.add_field(name='NORMAL', value=field_drop_chance, inline=False)
        embed.add_field(name='HARDMODE', value=field_drop_chance_hardmode, inline=False)
        
    if drop_type == DROP_LOOTBOX:
        drop_chance_hunt = base_chance * horse_chance * multiplier
        drop_chance_adv = base_chance_adv * horse_chance * multiplier
        drop_chance_hunt_daily = round(drop_chance_hunt * 1.3, 3)
        drop_chance_adv_daily = round(drop_chance_adv * 1.3, 3)
        drop_chance_hunt = round(drop_chance_hunt, 3)
        drop_chance_adv = round(drop_chance_adv, 3)
        field_drop_chance_hunt = (
            f'{emojis.BP} Base chance: `{drop_chance_hunt:g}`%\n'
            f'{emojis.BP} If mob is daily mob: `{drop_chance_hunt_daily:g}`%\n'
        )
        field_drop_chance_adv= (
            f'{emojis.BP} Base chance: `{drop_chance_adv:g}`%\n'
            f'{emojis.BP} If mob is daily mob: `{drop_chance_adv_daily:g}`%\n'
        )
        embed.add_field(name='HUNT', value=field_drop_chance_hunt, inline=False)
        embed.add_field(name='ADVENTURE', value=field_drop_chance_adv, inline=False)
        
    if drop_type == DROP_DARK_ENERGY:
        field_encounter_chance = (
            f'{emojis.BP} Every mob in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} can drop this item\n'
        )
    elif drop_type == DROP_BASIC:
        field_encounter_chance = (
            f'{emojis.BP} You have a `50`% chance of encountering a mob in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
            f'that can drop an item\n'
            f'{emojis.DETAIL} Thus, the chance to get an item while hunting is __half__ of the values above\n'
        )
    elif drop_type == DROP_LOOTBOX:
        field_encounter_chance = (
            f'{emojis.BP} Every mob in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} and '
            f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} can drop lootboxes\n'
            f'{emojis.BP} A chance over `100`% reduces the amount of lower quality lootboxes\n'
        )
    else:
        field_encounter_chance = (
            f'{emojis.BP} Every mob in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} and '
            f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} can drop this item\n'
        )
    if drop_type == DROP_LOOTBOX:
        field_boosts = (
            f'{emojis.BP} {emojis.POTION_LOOTBOX} `Lootbox potion`: +`35`% chance\n'
            f'{emojis.BP} {emojis.POTION_ELECTRONICAL} `Electronical potion`: +`20`% chance\n'
            f'{emojis.BP} {emojis.POTION_MONSTER} `Monster potion`: +`10`% chance\n'
        )
    else:
        field_boosts = (
            f'{emojis.BP} {emojis.POTION_VOID} `VOID potion`: +`50`% chance\n'
            f'{emojis.BP} {emojis.POTION_MONSTER} `Monster potion`: +`30`% chance\n'
            f'{emojis.BP} {emojis.POTION_ELECTRONICAL} `Electronical potion`: +`20`% chance\n'
            f'{emojis.BP} {emojis.POTION_DRAGON_BREATH} `Dragon breath potion`: +`5`% chance\n'
        )

    embed.add_field(name='NOTE', value=field_encounter_chance, inline=False)
    embed.add_field(name='POTIONS THAT INCREASE DROP CHANCE', value=field_boosts, inline=False)
    return embed