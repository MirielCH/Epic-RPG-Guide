# horse.py
"""Contains all horse related guides and calculators"""

import asyncio
from math import floor
from typing import Optional

import discord

import database
from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_BREEDING = 'Breeding'
TOPIC_TIERS = 'Tiers'
TOPIC_TYPES = 'Types'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_BREEDING,
    TOPIC_TIERS,
    TOPIC_TYPES,
]


# --- Commands ---
async def command_horse_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Horse guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_overview,
        TOPIC_BREEDING: embed_breeding,
        TOPIC_TIERS: embed_tiers,
        TOPIC_TYPES: embed_types,
    }
    view = views.TopicView(ctx, topics_functions, active_topic=topic)
    embed = await topics_functions[topic]()
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    try:
        await functions.edit_interaction(interaction, view=None)
    except discord.errors.NotFound:
        pass


async def command_boost_calculator(bot: discord.Bot, ctx: discord.ApplicationContext,
                                   horse_tier: Optional[int] = None, horse_level: Optional[int] = None) -> str:
    """Horse boost calculator command"""
    if horse_tier is None or horse_level is None:
        bot_message_task = asyncio.ensure_future(functions.wait_for_horse_message(bot, ctx))
        try:
            content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                              command=strings.SLASH_COMMANDS_EPIC_RPG["horse stats"])
            bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
        except asyncio.TimeoutError:
            await ctx.respond(
                strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='horse'),
                ephemeral=True)
            return
        if bot_message is None: return
        horse_tier_found, horse_level_found = await functions.extract_horse_data_from_horse_embed(ctx, bot_message)
        if horse_tier is None: horse_tier = horse_tier_found
        if horse_level is None: horse_level = horse_level_found
    horse_emoji = getattr(emojis, f'HORSE_T{horse_tier}')
    try:
        horse_data: database.Horse = await database.get_horse(horse_tier)
    except:
        await ctx.respond(strings.MSG_ERROR, ephemeral=True)
        return
    await ctx.respond(
        f'Stat bonuses for a {horse_emoji} **T{horse_tier} L{horse_level}** horse:\n'
        f'{emojis.BP} **DEFENDER**: {horse_data.def_level_bonus * horse_level:,g}% extra DEF\n'
        f'{emojis.BP} **FESTIVE**: {horse_data.festive_level_bonus * horse_level:,g}% extra chance to spawn '
        f'random events\n'
        f'{emojis.BP} **GOLDEN**: {horse_data.golden_level_bonus * horse_level:,g}% extra coins from '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} **MAGIC**: {horse_data.magic_level_bonus * horse_level:,g}% increased enchantment efficiency\n'
        f'{emojis.BP} **SPECIAL**: {horse_data.special_level_bonus * horse_level:,g}% extra coins and XP from the '
        f'epic quest\n'
        #f'{emojis.BP} {emojis.HAL_PUMPKIN} **SPOOKY**: {strong_bonus * horse_level * 1.25:,g}% extra chance to find pumpkins and 5% extra '
        #f'chance to find bat slimes\n'
        f'{emojis.BP} **STRONG**: {horse_data.strong_level_bonus * horse_level:,g}% extra AT\n'
        f'{emojis.BP} **SUPER SPECIAL**: {horse_data.super_special_level_bonus * horse_level:,g}% extra coins and '
        f'XP from the epic quest\n'
        f'{emojis.BP} **TANK**: {horse_data.tank_level_bonus * horse_level:,g}% extra LIFE\n'
    )


async def command_horse_training_calculator(
    bot: discord.Bot,
    ctx: discord.ApplicationContext,
    horse_tier: Optional[int] = None,
    from_level: Optional[int] = None,
    to_level: Optional[int] = None,
    lootboxer_level: Optional[int] = None
) -> None:
        """Horse training calculator command"""
        if horse_tier is None or from_level is None:
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
            horse_tier_found, horse_level_found = await functions.extract_horse_data_from_horse_embed(ctx, bot_message)
            if horse_tier is None: horse_tier = horse_tier_found
            if from_level is None: from_level = horse_level_found
        if lootboxer_level is None:
            bot_message_task = asyncio.ensure_future(functions.wait_for_profession_overview_message(bot, ctx))
            try:
                content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                                  command=strings.SLASH_COMMANDS_EPIC_RPG["professions stats"])
                bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
            except asyncio.TimeoutError:
                await ctx.respond(
                    strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='profession'),
                    ephemeral=True
                )
                return
            if bot_message is None: return
            _, lootboxer_level = (
                await functions.extract_data_from_profession_overview_embed(ctx, bot_message, 'lootboxer')
            )
        horse_emoji = getattr(emojis, f'HORSE_T{horse_tier}')
        if lootboxer_level > 100:
            max_level = 10 * horse_tier + (lootboxer_level - 100)
        else:
            max_level = 10 * horse_tier
        if to_level is None: to_level = max_level
        if to_level > max_level:
            await ctx.respond(
                f'This is not a valid horse level. With a {horse_emoji} **T{horse_tier}** horse and lootboxer '
                f'**L{lootboxer_level}** your max horse level is **L{max_level}**.',
                ephemeral=True
            )
            return
        if from_level >= max_level:
            await ctx.respond(
                'Your horse is already maxed out.',
                ephemeral=True
            )
            return
        if from_level >= to_level:
            await ctx.respond(
                'The level you want to calculate to has to be higher than your current level.',
                ephemeral=True
            )
            return
        embed = await embed_horse_training_calculator(horse_tier, from_level, to_level, lootboxer_level)
        await ctx.respond(embed=embed)


# --- Embeds ---
async def embed_overview() -> discord.Embed:
    """Horse overview embed"""
    horse_tier = (
        f'{emojis.BP} Tiers range from I to X (1 to 10) (see topic `Tiers`)\n'
        f'{emojis.BP} Every tier unlocks new bonuses\n'
        f'{emojis.BP} Mainly increased by breeding with other horses (see topic `Breeding`)\n'
        f'{emojis.BP} Small chance of increasing in horse races (see {strings.SLASH_COMMANDS_GUIDE["event guide"]})'
    )
    horse_level = (
        f'{emojis.BP} Levels range from 1 to ([tier] * 10) + [lootboxer bonus]\n'
        f'{emojis.BP} Example: A T7 horse with lootboxer at 102 has a max level of 72\n'
        f'{emojis.BP} Leveling up increases the horse type bonus (see the [Wiki]'
        f'(https://epic-rpg.fandom.com/wiki/Horse#Horse_Types_and_Boosts))\n'
        f'{emojis.BP} Increased by using {strings.SLASH_COMMANDS_EPIC_RPG["horse training"]} which costs coins\n'
        f'{emojis.BP} Training cost is reduced by leveling up lootboxer (see '
        f'{strings.SLASH_COMMANDS_GUIDE["professions guide"]})'
    )
    horse_type = (
        f'{emojis.BP} There are 8 different types (see topic `Types`)\n'
        f'{emojis.BP} The exact bonus the type gives is dependent on the level\n'
        f'{emojis.BP} Randomly changes when breeding unless you have a {emojis.HORSE_TOKEN} horse token in your '
        f'inventory'
    )
    calculators = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["horse boost calculator"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["horse training calculator"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSES',
        description = 'Horses have tiers, levels and types which all give certain important bonuses.'
    )
    embed.add_field(name='TIER', value=horse_tier, inline=False)
    embed.add_field(name='LEVEL', value=horse_level, inline=False)
    embed.add_field(name='TYPE', value=horse_type, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    return embed


async def embed_tiers() -> discord.Embed:
    """Horse tiers embed"""
    buff_lootbox = '{increase}% buff to lootbox drop chance'
    buff_monsters = '{increase}% buff to monster drops drop chance'
    buff_coins = '{increase}% more coins when using {daily} and {weekly}'
    buff_pets = '{increase}% higher chance to find pets with {training} ({total}%)'
    command_daily = strings.SLASH_COMMANDS_EPIC_RPG["daily"]
    command_weekly = strings.SLASH_COMMANDS_EPIC_RPG["weekly"]
    command_training = strings.SLASH_COMMANDS_EPIC_RPG["training"]
    tier1 = f'{emojis.BP} No bonuses'
    tier2 = f'{emojis.BP} {buff_coins.format(increase=5, daily=command_daily, weekly=command_weekly)}'
    tier3 = f'{emojis.BP} {buff_coins.format(increase=10, daily=command_daily, weekly=command_weekly)}'
    tier4 = (
        f'{emojis.BP} Unlocks immortality in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} {buff_coins.format(increase=20, daily=command_daily, weekly=command_weekly)}'
    )
    tier5 = (
        f'{emojis.BP} Unlocks horse racing\n'
        f'{emojis.BP} {buff_lootbox.format(increase=20)}\n'
        f'{emojis.BP} {buff_coins.format(increase=30, daily=command_daily, weekly=command_weekly)}'
    )
    tier6 = (
        f'{emojis.BP} Unlocks free access to dungeons without dungeon keys\n'
        f'{emojis.BP} {buff_lootbox.format(increase=50)}\n'
        f'{emojis.BP} {buff_coins.format(increase=45, daily=command_daily, weekly=command_weekly)}'
    )
    tier7 = (
        f'{emojis.BP} {buff_monsters.format(increase=20)}\n'
        f'{emojis.BP} {buff_lootbox.format(increase=100)}\n'
        f'{emojis.BP} {buff_coins.format(increase=60, daily=command_daily, weekly=command_weekly)}'
    )
    tier8 = (
        f'{emojis.BP} Unlocks higher chance to get better enchants (% unknown)\n'
        f'{emojis.BP} {buff_monsters.format(increase=50)}\n'
        f'{emojis.BP} {buff_lootbox.format(increase=200)}\n'
        f'{emojis.BP} {buff_coins.format(increase=80, daily=command_daily, weekly=command_weekly)}'
    )
    tier9 = (
        f'{emojis.BP} {buff_pets.format(increase=150, total=10, training=command_training)}\n'
        f'{emojis.BP} {buff_monsters.format(increase=100)}\n'
        f'{emojis.BP} {buff_lootbox.format(increase=400)}\n'
        f'{emojis.BP} {buff_coins.format(increase=100, daily=command_daily, weekly=command_weekly)}\n'
    )
    tier10 = (
        f'{emojis.BP} Unlocks 2 extra badge slots\n'
        f'{emojis.BP} Adds a chance for another drop after each drop (mob drops and lootboxes)\n'
        f'{emojis.DETAIL} The chance is believed to be around 20-35%, depending on the item\n'
        f'{emojis.DETAIL} The better the item, the lower the chance\n'
        f'{emojis.BP} {buff_pets.format(increase=400, total=20, training=command_training)}\n'
        f'{emojis.BP} {buff_monsters.format(increase=200)}\n'
        f'{emojis.BP} {buff_lootbox.format(increase=650)}\n'
        f'{emojis.BP} {buff_coins.format(increase=200, daily=command_daily, weekly=command_weekly)}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSE TIERS',
        description = (
            f'Every horse tier unlocks additional bonuses.\n'
            f'Note: Every tier only lists the unlocks for this tier. You don\'t lose any previous unlocks when '
            f'tiering up.'
        )
    )
    embed.add_field(name=f'TIER I {emojis.HORSE_T1}', value=tier1, inline=False)
    embed.add_field(name=f'TIER II {emojis.HORSE_T2}', value=tier2, inline=False)
    embed.add_field(name=f'TIER III {emojis.HORSE_T3}', value=tier3, inline=False)
    embed.add_field(name=f'TIER IV {emojis.HORSE_T4}', value=tier4, inline=False)
    embed.add_field(name=f'TIER V {emojis.HORSE_T5}', value=tier5, inline=False)
    embed.add_field(name=f'TIER VI {emojis.HORSE_T6}', value=tier6, inline=False)
    embed.add_field(name=f'TIER VII {emojis.HORSE_T7}', value=tier7, inline=False)
    embed.add_field(name=f'TIER VIII {emojis.HORSE_T8}', value=tier8, inline=False)
    embed.add_field(name=f'TIER IX {emojis.HORSE_T9}', value=tier9, inline=False)
    embed.add_field(name=f'TIER X {emojis.HORSE_T10}', value=tier10, inline=False)
    return embed


async def embed_types() -> discord.Embed:
    """Horse types embed"""
    defender = (
        f'{emojis.BP} Increases overall DEF\n'
        f'{emojis.BP} The higher the horse level, the higher the DEF bonus\n'
        f'{emojis.BP} This type is better than MAGIC if you use EDGY or lower enchants\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    strong = (
        f'{emojis.BP} Increases overall AT\n'
        f'{emojis.BP} The higher the horse level, the higher the AT bonus\n'
        f'{emojis.BP} This type is better than MAGIC if you use EDGY or lower enchants\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    tank = (
        f'{emojis.BP} Increases overall LIFE\n'
        f'{emojis.BP} The higher the horse level, the higher the LIFE bonus\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    golden = (
        f'{emojis.BP} Increases the amount of coins from {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} The higher the horse level, the higher the coin bonus\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    special = (
        f'{emojis.BP} Unlocks the epic quest which gives more coins and XP than the regular quest\n'
        f'{emojis.BP} You can do up to 15 waves in the epic quest\n'
        f'{emojis.BP} The higher the horse level, the more coins and XP the epic quest gives\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    super_special = (
        f'{emojis.BP} Unlocks the epic quest which gives more coins and XP than the regular quest\n'
        f'{emojis.BP} You can do up to 100 waves in the epic quest\n'
        f'{emojis.BP} The higher the horse level, the more coins and XP the epic quest gives\n'
        f'{emojis.BP} The coin and XP bonus is 50% higher than SPECIAL\n'
        f'{emojis.BP} **You only have a chance getting this type when breeding two SPECIAL horses**\n'
        f'{emojis.BP} As with every type change, you need to breed **without** a horse token\n'
    )
    magic = (
        f'{emojis.BP} Increases the effectiveness of enchantments\n'
        f'{emojis.BP} The higher the horse level, the higher the increase\n'
        f'{emojis.BP} This type is better than DEFENDER / STRONG if you use ULTRA-EDGY or higher enchants\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    festive = (
        f'{emojis.BP} Increases the chance to trigger a random event when using commands\n'
        f'{emojis.BP} The higher the horse level, the higher the increase\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    spooky = (
        f'{emojis.BP} Increases the chance to find pumpkins and spawn bat slimes\n'
        f'{emojis.BP} The higher the horse level, the higher the pumpkin chance\n'
        f'{emojis.BP} The bat slime spawn chance increase is always 5%\n'
        f'{emojis.BP} To get this type, craft and use a {emojis.HAL_CANDY_FISH} candy fish'
    )
    besttype = (
        f'{emojis.BP} SPECIAL or SUPER SPECIAL if you are in {emojis.TIME_TRAVEL} TT 0-1\n'
        f'{emojis.BP} DEFENDER if you are {emojis.TIME_TRAVEL} TT 2+, not ascended\n'
        f'{emojis.BP} MAGIC if you are {emojis.TIME_TRAVEL} TT 2+, ascended\n'
    )
    calculators = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["horse boost calculator"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSE TYPES',
        description = (
            f'Each horse type has its unique bonuses.\n'
            f'The best type for you depends on your current TT and your horse tier and level.'
        )
    )
    embed.add_field(name='DEFENDER', value=defender, inline=False)
    embed.add_field(name='FESTIVE', value=festive, inline=False)
    embed.add_field(name='GOLDEN', value=golden, inline=False)
    embed.add_field(name='MAGIC', value=magic, inline=False)
    embed.add_field(name='SPECIAL', value=special, inline=False)
    #embed.add_field(name=f'SPOOKY {emojis.HAL_PUMPKIN}', value=spooky, inline=False)
    embed.add_field(name='STRONG', value=strong, inline=False)
    embed.add_field(name='SUPER SPECIAL', value=super_special, inline=False)
    embed.add_field(name='TANK', value=tank, inline=False)
    embed.add_field(name='WHICH TYPE TO CHOOSE', value=besttype, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    return embed


async def embed_breeding() -> discord.Embed:
    """Horse breeding embed"""
    howto = (
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["horse breeding"]}\n'
        f'{emojis.BP} You can only breed with a horse of the **same** tier\n'
        f'{emojis.BP} Ideally breed with a horse of the same level'
    )
    whereto = f'{emojis.BP} You can find players in the [official EPIC RPG server](https://discord.gg/w5dej5m)'
    horse_tier = (
        f'{emojis.BP} You have a chance to get +1 tier\n'
        f'{emojis.BP} The chance to tier up gets lower the higher your tier is\n'
        f'{emojis.BP} If one horse tiers up, the other one isn\'t guaranteed to do so too'
    )
    fail_count = (
        f'{emojis.BP} Everytime you don\'t tier up, you increase your fail count by 1\n'
        f'{emojis.BP} After a certain amount of fails, you will unlock an increased tier up chance\n'
        f'{emojis.BP} If you still don\'t tier up, you will unlock a guaranteed tier up at some point\n'
        f'{emojis.BP} The exact fail count needed depends on the horse tier\n'
        f'{emojis.BP} A {emojis.GODLY_HORSE_TOKEN} GODLY horse token increases the fail count by 50\n'
        f'{emojis.BP} This token can be earned in certain seasonal events\n'
    )
    chances = (
        f'{emojis.BP} T1 ➜ T2: 100% chance\n'
        f'{emojis.BP} T2 ➜ T3: 60% chance (guaranteed after 2 attempts)\n'
        f'{emojis.BP} T3 ➜ T4: 30% chance (guaranteed after 4 attempts)\n'
        f'{emojis.BP} T4 ➜ T5: 15% chance (guaranteed after 8 attempts)\n'
        f'{emojis.BP} T5 ➜ T6: 5% chance (guaranteed after 24 attempts)\n'
        f'{emojis.BP} T6 ➜ T7: 2% chance (guaranteed after 60 attempts)\n'
        f'{emojis.BP} T7 ➜ T8: 1% chance (guaranteed after 120 attempts)\n'
        f'{emojis.BP} T8 ➜ T9: chance unknown (guaranteed after 360 attempts)\n'
        f'{emojis.BP} T9 ➜ T10: chance unknown (guaranteed after 1080 attempts)\n'
    )
    horse_level = (
        f'{emojis.BP} The new horses will have an average of both horse\'s levels\n'
        f'{emojis.BP} Example: L20 horse + L24 horse = L22 horses\n'
        f'{emojis.BP} Example: L20 horse + L23 horse = L21 **or** L22 horses'
    )
    horse_type = (
        f'{emojis.BP} Breeding changes your horse type randomly\n'
        f'{emojis.BP} You can keep your type by buying a {emojis.HORSE_TOKEN} horse token\n'
        f'{emojis.BP} Note: Each breeding consumes 1 {emojis.HORSE_TOKEN} horse token'
    )
    calculators = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["horse boost calculator"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["horse training calculator"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSE BREEDING',
        description = 'You need to breed to increase your horse tier and/or get a different type.'
    )
    embed.add_field(name='HOW TO BREED', value=howto, inline=False)
    embed.add_field(name='WHERE TO BREED', value=whereto, inline=False)
    embed.add_field(name='IMPACT ON TIER', value=horse_tier, inline=False)
    embed.add_field(name='IMPACT ON LEVEL', value=horse_level, inline=False)
    embed.add_field(name='IMPACT ON TYPE', value=horse_type, inline=False)
    embed.add_field(name='TIER UP FAIL COUNT', value=fail_count, inline=False)
    embed.add_field(name='CHANCE TO TIER UP', value=chances, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    return embed


async def embed_horse_training_calculator(horse_tier: int, from_level: int, to_level: int,
                                          lootboxer_level: int) -> discord.Embed:
    """Horse training calculator embed"""
    horse_emoji = getattr(emojis, f'HORSE_T{horse_tier}')
    output = ''
    current_level = from_level
    for x in range(10):
        if (current_level + 1) > to_level: break
        level_cost = floor(
            ((current_level ** 4)
                * ((current_level ** 2) + (210 * current_level) + 2200) * (500 - (lootboxer_level**1.2))
                / 100000)
        )
        output = f'{output}\n{emojis.BP} Level {current_level} to {current_level+1}: **{level_cost:,}** {emojis.COIN}'
        current_level += 1
    level_cost_total = 0
    for current_level in range(from_level, to_level):
        level_cost = floor(
            ((current_level ** 4)
                * ((current_level ** 2) + (210 * current_level) + 2200) * (500 - (lootboxer_level**1.2))
                / 100000)
        )
        level_cost_total += level_cost
    output_total = f'{emojis.BP} **{level_cost_total:,}** {emojis.COIN}'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSE TRAINING CALCULATOR',
        description = (
            f'Horse: {horse_emoji} **T{horse_tier}**\n'
            f'Horse levels: **{from_level}** to **{to_level}**\n'
            f'Lootboxer level: **{lootboxer_level}**'
        )
    )
    embed.add_field(name='NEXT LEVELS', value=output, inline=False)
    embed.add_field(name=f'TOTAL {from_level} - {to_level}', value=output_total, inline=False)
    return embed