# timetravel.py

import asyncio
from decimal import Decimal, ROUND_HALF_UP
from math import floor, ceil
from typing import Optional

import discord

import database
from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_TT = 'Time travel (TT)'
TOPIC_TJ = 'Time jump / Super time travel (STT)'

TOPICS = [
    TOPIC_TT,
    TOPIC_TJ,
]

TOPIC_SCORE_GEAR = 'Gear'
TOPIC_SCORE_MATERIALS = 'Materials'
TOPIC_SCORE_STATS = 'Stats & enchants'

TOPICS_SCORE = [
    TOPIC_SCORE_GEAR,
    TOPIC_SCORE_MATERIALS,
    TOPIC_SCORE_STATS,
]


# --- Calculator options ---
INVENTORY_CURRENT = 'Calculate as is'
INVENTORY_TRADE_A15 = 'Trade to A15 rubies'
INVENTORY_TRADE_A16 = 'Trade to A16+/TOP rubies'

TJ_CALCULATOR_INVENTORY = [
    INVENTORY_CURRENT,
    INVENTORY_TRADE_A15,
    INVENTORY_TRADE_A16,
]

STATS_NONE = 'No stats'
STATS_CURRENT = 'Current stats'
STATS_MANUAL = 'Manual input'

TJ_CALCULATOR_STATS = [
    STATS_NONE,
    STATS_CURRENT,
    STATS_MANUAL,
]

BOOSTS_NONE = 'No boosts'
BOOSTS_CURRENT = 'Current boosts'

TJ_CALCULATOR_BOOSTS = [
    BOOSTS_NONE,
    BOOSTS_CURRENT,
]

# --- Commands ---
async def command_time_travel_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Timetravel guide command"""
    topics_functions = {
        TOPIC_TT: embed_time_travel,
        TOPIC_TJ: embed_time_jump,
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


async def command_time_travel_bonuses(ctx: discord.ApplicationContext, timetravel: Optional[int] = None) -> None:
    """Timetravel guide command"""
    mytt = True if timetravel is None else False
    if timetravel is None:
        user: database.User = await database.get_user(ctx.author.id)
        timetravel = user.tt
    if timetravel == 1_000_000:
        await ctx.respond('https://c.tenor.com/OTU2-ychJwsAAAAC/lightning-squidward.gif')
        return
    tt: database.TimeTravel = await database.get_time_travel(timetravel)
    embed = await embed_time_travel_bonuses(tt, mytt)
    await ctx.respond(embed=embed)


async def command_time_jump_score(ctx: discord.ApplicationContext, topic: str) -> None:
    """Time jump score command"""
    topics_functions = {
        TOPIC_SCORE_GEAR: embed_time_jump_score_gear,
        TOPIC_SCORE_MATERIALS: embed_time_jump_score_materials,
        TOPIC_SCORE_STATS: embed_time_jump_score_stats,
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


async def command_time_jump_calculator(bot: discord.Bot, ctx: discord.ApplicationContext, area_no: int,
                                      option_inventory: str, option_stats: str, option_boosts: str) -> None:
    """STT score calculator command"""
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

    profile_data = {}
    boosts_data = {
        'at': 0,
        'def': 0,
        'life': 0,
    }
    if option_stats == STATS_CURRENT:
        bot_message_task = asyncio.ensure_future(functions.wait_for_profile_message(bot, ctx))
        try:
            content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                            command=strings.SLASH_COMMANDS_EPIC_RPG["profile"])
            bot_message_profile = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
        except asyncio.TimeoutError:
            await ctx.respond(
                strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='profile'),
                ephemeral=True
            )
            return
        if bot_message is None: return
        profile_data = await functions.extract_data_from_profile_embed(ctx, bot_message_profile)
        if option_boosts == BOOSTS_CURRENT:
            bot_message_task = asyncio.ensure_future(functions.wait_for_boosts_message(bot, ctx))
            try:
                content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                                command=strings.SLASH_COMMANDS_EPIC_RPG["boosts"])
                bot_message_boosts = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
            except asyncio.TimeoutError:
                await ctx.respond(
                    strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='boosts'),
                    ephemeral=True
                )
                return
            if bot_message is None: return
            boosts_data = await functions.extract_data_from_boosts_embed(ctx, bot_message_boosts)
        profile_data['horse_boost'] = 0
        profile_data['horse_epicness'] = 0
        profile_data['horse_level'] = 0
        profile_data['horse_tier'] = 0
        if profile_data['horse_type'] in ('magic', 'defender', 'strong', 'tank'):
            bot_message_task = asyncio.ensure_future(functions.wait_for_horse_message(bot, ctx))
            try:
                content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                                command=strings.SLASH_COMMANDS_EPIC_RPG["horse stats"])
                bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
            except asyncio.TimeoutError:
                await ctx.respond(
                    strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='horse stats'),
                    ephemeral=True
                )
                return
            if bot_message is None: return
            horse_data = await functions.extract_horse_data_from_horse_embed(ctx, bot_message)
            profile_data['horse_boost'] = horse_data['boost']
            profile_data['horse_epicness'] = horse_data['epicness']
            profile_data['horse_level'] = horse_data['level']
            profile_data['horse_tier'] = horse_data['tier']

    if option_stats == STATS_MANUAL:
        all_items_list = list(await database.get_all_items())
        all_items_list.sort(key=lambda item: item.score)
        profile_data['sword'] = None
        profile_data['armor'] = None
        all_items = {}
        for item in all_items_list:
            if item.name.lower() == 'ultra-omega sword':
                profile_data['sword'] = item
            if item.name.lower() == 'ultra-omega armor':
                profile_data['armor'] = item
            all_items[item.name] = item
        profile_data['level'] = 200
        profile_data['extra_at'] = 0
        profile_data['extra_def'] = 0
        profile_data['extra_life'] = 0
        profile_data['enchant_sword'] = 'OMEGA'
        profile_data['enchant_armor'] = 'OMEGA'

    embed = await embed_time_jump_calculator(area_no, inventory.lower(), profile_data, boosts_data, option_inventory,
                                             option_stats)
    if option_stats == STATS_MANUAL:
        view = views.TimeJumpCalculatorView(ctx, area_no, inventory.lower(), profile_data, boosts_data, option_inventory,
                                            option_stats, all_items, embed_time_jump_calculator)
        interaction = await ctx.respond(embed=embed, view=view)
        view.interaction = interaction
        await view.wait()
    else:
        await ctx.respond(embed=embed)


# --- Embeds ---
async def embed_time_travel() -> discord.Embed:
    """Time travel overview"""
    where = (
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 0: Beat dungeon 10, reach area 11\n'
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 1-2: Beat dungeon 11, reach area 12\n'
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 3-4: Beat dungeon 12, reach area 13\n'
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 5-9: Beat dungeon 13, reach area 14\n'
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 10-24: Beat dungeon 14, reach area 15\n'
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 25+: Beat dungeon 15-1\n'
    )
    keptitems = (
        f'{emojis.BP} Active boosts\n'
        f'{emojis.BP} Anniversary lootboxes\n'
        f'{emojis.BP} Arena cookies\n'
        f'{emojis.BP} Coins (this includes your bank account)\n'
        f'{emojis.BP} Dragon essences\n'
        f'{emojis.BP} EPIC berries\n'
        f'{emojis.BP} EPIC coins\n'
        f'{emojis.BP} EPIC shop items\n'
        f'{emojis.BP} Event items (if an event is active)\n'
        f'{emojis.BP} GODLY horse tokens\n'
        f'{emojis.BP} Guild rings\n'
        f'{emojis.BP} Legendary toothbrushes\n'
        f'{emojis.BP} Magic chairs\n'
        f'{emojis.BP} Mega boosts\n'
        f'{emojis.BP} Profession levels\n'
        f'{emojis.BP} OMEGA horse tokens\n'
        f'{emojis.BP} Party poppers\n'
        f'{emojis.BP} Round cards\n'
        f'{emojis.BP} TIME capsules\n'
        f'{emojis.BP} TIME cookies\n'
        f'{emojis.BP} TIME dragon essences\n'
        f'{emojis.BP} Wishing tokens\n'
        f'{emojis.BP} Your guild\n'
        f'{emojis.BP} Your horse\n'
        f'{emojis.BP} Your marriage partner\n'
        f'{emojis.BP} Your pets\n'
    )
    boosts = (
        f'{emojis.BP} {emojis.POTION_TIME} TIME potion: Keep `7.5`% of the items in your inventory\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TIME TRAVEL (TT)',
        description = (
            f'Resets your character to level 1 / area 1 but unlocks new game features and increases XP and drop chances.\n'
            f'To time travel, use {strings.SLASH_COMMANDS_EPIC_RPG["time travel"]} while meeting the requirements.\n'
            f'Warning: **You will lose everything except the items mentioned below**. So make sure you have done all '
            f'you want to do. You can check what you should do before time traveling by looking up the TT you are '
            f'going to travel to with {strings.SLASH_COMMANDS_GUIDE["time travel bonuses"]}.'
        )

    )
    embed.add_field(name='REQUIREMENTS FOR TIME TRAVEL', value=where, inline=False)
    embed.add_field(name='WHAT YOU KEEP', value=keptitems, inline=False)
    embed.add_field(name='POTIONS THAT AFFECT TIME TRAVEL', value=boosts, inline=False)
    return embed


async def embed_time_travel_bonuses(tt: database.TimeTravel, mytt: bool = False):
    """Embed with details for specific time travel"""
    bonus_xp = (99 + tt.tt) * tt.tt / 2
    bonus_duel_xp = (99 + tt.tt) * tt.tt / 4
    bonus_drop_chance = (49 + tt.tt) * tt.tt / 2
    berry_drop_chance = bonus_drop_chance / 10
    #artifacts_drop_chance = bonus_drop_chance / 4
    dynamite_rubies = 1 + (bonus_drop_chance / 100)
    crops_normal_min =  dynamite_rubies * 2
    crops_normal_max =  dynamite_rubies * 3
    crops_special_min = dynamite_rubies * 5
    crops_special_med = dynamite_rubies * 6
    crops_special_max = dynamite_rubies * 7
    greenhouse_watermelon_min = dynamite_rubies * 2
    greenhouse_watermelon_max = dynamite_rubies * 3
    chainsaw_mega = dynamite_rubies * 2
    bigboat_superfish = ceil(0.85 * dynamite_rubies)
    chainsaw_ultimate = dynamite_rubies / 3.5
    dynamite_rubies = Decimal(dynamite_rubies).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    #greenhouse_watermelon_min = Decimal(greenhouse_watermelon_min).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    #greenhouse_watermelon_max = Decimal(greenhouse_watermelon_max).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    chainsaw_ultimate = Decimal(chainsaw_ultimate).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    rubies = int(dynamite_rubies)
    crops_normal_min = int(crops_normal_min)
    crops_normal_max = int(crops_normal_max)
    crops_special_min = int(crops_special_min)
    crops_special_med = int(crops_special_med)
    crops_special_max = int(crops_special_max)
    watermelon_min = int(greenhouse_watermelon_min)
    watermelon_max = int(greenhouse_watermelon_max)
    super_fish = int(bigboat_superfish)
    mega_log = int(chainsaw_mega)
    ultimate_logs = int(chainsaw_ultimate)
    if ultimate_logs <= 0: ultimate_logs = 1
    if super_fish <= 0: super_fish = 1
    # Enchant multiplier formula is from a player, tested up to TT120 + 194 + 200. TT15 only one found to be wrong so far.
    tt_enchant_multipliers = {
        15: 6,
    }
    if tt.tt in tt_enchant_multipliers:
        enchant_multiplier = tt_enchant_multipliers[tt.tt]
    else:
        enchant_multiplier = round((tt.tt ** 2 / 64) + (7 * tt.tt / 73) + (19 / 35))
    bonus_xp = f'{bonus_xp:,.1f}'.replace('.0','')
    bonus_duel_xp = f'{bonus_duel_xp:,.1f}'.replace('.0','')
    bonus_drop_chance = f'{bonus_drop_chance:,.1f}'.replace('.0','')
    berry_drop_chance = f'{berry_drop_chance:,.1f}'.replace('.0','')
    #artifacts_drop_chance = f'{artifacts_drop_chance:,g}'
    if mytt:
        embed_description = (
            f'This is your current TT according to your settings.\n'
            f'If this is wrong, use {strings.SLASH_COMMANDS_GUIDE["set progress"]} to change it.'
        )
    else:
        embed_description = 'Allons-y !'
    unlocks = ''
    if tt.unlock_misc is not None:
        unlocks = f'{emojis.BP} Unlocks **{tt.unlock_misc}**\n'
    if tt.unlock_dungeon is not None:
        unlocks = f'{unlocks}{emojis.BP} Unlocks **dungeon {tt.unlock_dungeon}**\n'
    if tt.unlock_area is not None:
        unlocks = f'{unlocks}{emojis.BP} Unlocks **area {tt.unlock_area}**\n'
    if tt.unlock_enchant is not None:
        unlocks = f'{unlocks}{emojis.BP} Unlocks the **{tt.unlock_enchant}** enchant\n'
    if tt.unlock_title is not None:
        unlocks = f'{unlocks}{emojis.BP} Unlocks the title **{tt.unlock_title}**\n'
    unlocks = (
        f"{unlocks}{emojis.BP} `{bonus_xp}` % increased **XP** from everything except duels\n"
        f'{emojis.BP} `{bonus_duel_xp}` % increased **XP** from **duels**\n'
        f'{emojis.BP} `{bonus_drop_chance}` % extra chance to get **monster drops**\n'
        f'{emojis.BP} `{bonus_drop_chance}` % more **items** with work commands\n'
        f'{emojis.BP} `{berry_drop_chance}` % more **EPIC berries** with pickup commands\n'
        f'{emojis.BP} `x{enchant_multiplier:,}` **enchanting multiplier**\n'
    )
    if tt.tt > 1:
        unlocks = (
            f'{unlocks.strip()}\n'
            f'{emojis.BP} `{tt.tt + 5:,}` base **pet slots**\n'
            f'{emojis.DETAIL} Your total pet slots depend on the coolness pet slot multiplier\n'
            f'{emojis.DETAIL} See {strings.SLASH_COMMANDS_EPIC_RPG["ultraining progress"]} to see your multiplier\n'
        )
    if tt.tt > 0:
        unlocks = (
            f'{unlocks.strip()}\n'
            f'{emojis.BP} Higher chance to get `+1` tier in {strings.SLASH_COMMANDS_EPIC_RPG["horse breeding"]} and '
            f'{strings.SLASH_COMMANDS_EPIC_RPG["pets fusion"]} (chance unknown)\n'
            f'{emojis.BP} Higher chance to find **artifact parts**\n'
        )
    if tt.tt >= 50:
        unlocks = (
            f'{unlocks.strip()}\n'
            f'{emojis.BP} Unlocks ability to sell gear below GODLY without confirmation\n'
        )
    coin_cap = f'`{pow(tt.tt, 4) * 500_000_000:,}`' if tt.tt > 0 else '`100,000` - `14,400,000`'
    field_coin_cap = (
        f'{emojis.BP} ~{coin_cap} {emojis.COIN} coins\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["coin cap calculator"]} to see your exact cap\n'
    )
    work_multiplier = (
        f'{emojis.BP} `{crops_special_min:,}`, `{crops_special_med:,}` or `{crops_special_max:,}` {emojis.BREAD}'
        f'{emojis.CARROT}{emojis.POTATO} with {strings.SLASH_COMMANDS_EPIC_RPG["farm"]} from special seeds\n'
        f'{emojis.BP} `{crops_normal_min:,}` or `{crops_normal_max:,}` {emojis.BREAD}'
        f'{emojis.CARROT}{emojis.POTATO} with {strings.SLASH_COMMANDS_EPIC_RPG["farm"]} from normal seeds\n'
        f'{emojis.BP} ~`{watermelon_min:,}` - `{watermelon_max:,}` {emojis.WATERMELON} with '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["greenhouse"]}\n'
        f'{emojis.BP} `{mega_log:,}` {emojis.LOG_MEGA} with {strings.SLASH_COMMANDS_EPIC_RPG["chainsaw"]}\n'
        f'{emojis.BP} `{rubies:,}` {emojis.RUBY} with {strings.SLASH_COMMANDS_EPIC_RPG["dynamite"]}\n'
        f'{emojis.BP} `{rubies:,}` {emojis.LOG_HYPER} / {emojis.LOG_ULTRA} with {strings.SLASH_COMMANDS_EPIC_RPG["chainsaw"]}\n'
        f'{emojis.BP} ~`{super_fish:,}` {emojis.FISH_SUPER} with {strings.SLASH_COMMANDS_EPIC_RPG["bigboat"]}\n'
        f'{emojis.BP} ~`{ultimate_logs:,}` {emojis.LOG_ULTIMATE} with {strings.SLASH_COMMANDS_EPIC_RPG["chainsaw"]}\n'
    )
    prep_tt1_to_2 = (
        f'{emojis.BP} If your horse is T6+: Get 30m coins\n'
        f'{emojis.BP} If your horse is <T6: Get 50m coins\n'
        f'{emojis.BP} If you need money: Do boosted minibosses, use {strings.SLASH_COMMANDS_EPIC_RPG["drill"]} and '
        f'sell mob drops\n'
        f'{emojis.BP} If you need money and are impatient: sell apples\n'
        f'{emojis.BP} If you have leftover flasks: Brew potions that are useful in low areas\n'
        f'{emojis.BP} Level up professions (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} Sell everything else **except** the items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}\n'
        f'{emojis.BP} Don\'t forget to sell your armor and sword!'
    )
    prep_tt3_to_4 = (
        f'{emojis.BP} If your horse is T6+: Get 50m coins\n'
        f'{emojis.BP} If your horse is <T6: Get 150m coins\n'
        f'{emojis.BP} If you need money: Do boosted minibosses, use {strings.SLASH_COMMANDS_EPIC_RPG["dynamite"]} and '
        f'sell mob drops\n'
        f'{emojis.BP} If you need money and are impatient: sell apples\n'
        f'{emojis.BP} If you have leftover flasks: Brew potions that are useful in low areas\n'
        f'{emojis.BP} Level up professions if not done (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.BP} If you have materials left: Trade to apples and sell\n'
        f'{emojis.BP} Sell everything else **except** the items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}\n'
        f'{emojis.BP} Don\'t forget to sell your armor and sword!'
    )
    prep_tt5_to_9 = (
        f'{emojis.BP} If your horse is T6+: Get 150m coins\n'
        f'{emojis.BP} If your horse is <T6: Get 350m coins\n'
        f'{emojis.BP} If you need money: Do boosted minibosses, use {strings.SLASH_COMMANDS_EPIC_RPG["dynamite"]} and '
        f'sell mob drops\n'
        f'{emojis.BP} If you need money and are impatient: sell apples\n'
        f'{emojis.BP} If you have leftover flasks: Brew potions that are useful in low areas\n'
        f'{emojis.BP} Level up professions if not done (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.BP} If you have materials left: Trade to apples and sell\n'
        f'{emojis.BP} Sell everything else **except** the items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}\n'
        f'{emojis.BP} Don\'t forget to sell your armor and sword!'
    )
    prep_tt10_to_24 = (
        f'{emojis.BP} If your horse is T6+: Get 350m coins\n'
        f'{emojis.BP} If your horse is <T6: Get 850m coins\n'
        f'{emojis.BP} If you need money: Do boosted minibosses, use {strings.SLASH_COMMANDS_EPIC_RPG["dynamite"]} and '
        f'sell mob drops\n'
        f'{emojis.BP} If you need money and are impatient: sell apples\n'
        f'{emojis.BP} If you have leftover flasks: Brew potions that are useful in low areas\n'
        f'{emojis.BP} Level up professions if not done (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.BP} If you have materials left: Trade to apples and sell\n'
        f'{emojis.BP} Sell everything else **except** the items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}\n'
        f'{emojis.BP} Don\'t forget to sell your armor and sword!\n'
        f'{emojis.BP} Tip: Claim the {emojis.BADGE_AREA15} area 15 badge if you haven\'t yet '
        f'({strings.SLASH_COMMANDS_EPIC_RPG["badge claim"]} `id: 10`)\n'
    )
    prep_tt25 = (
        f'{emojis.BP} If your horse is T6+: Get 350m coins\n'
        f'{emojis.BP} If your horse is <T6: Get 850m coins\n'
        f'{emojis.BP} Note: You **need** a T6+ horse to do Dungeon 15\n'
        f'{emojis.BP} If you need money: Do boosted minibosses, use {strings.SLASH_COMMANDS_EPIC_RPG["dynamite"]} and '
        f'sell mob drops\n'
        f'{emojis.BP} If you need money and are impatient: sell apples\n'
        f'{emojis.BP} If you have leftover flasks: Brew potions that are useful in low areas\n'
        f'{emojis.BP} Level up professions if not done (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.BP} If you have materials left: Trade to apples and sell\n'
        f'{emojis.BP} Sell everything else **except** the items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}\n'
        f'{emojis.BP} Don\'t forget to sell your armor and sword!\n'
        f'{emojis.BP} Tip: Claim the {emojis.BADGE_AREA15} area 15 badge if you haven\'t yet '
        f'({strings.SLASH_COMMANDS_EPIC_RPG["badge claim"]} `id: 10`)\n'
    )
    prep_stt = (
        f'{emojis.BP} Get 850m coins\n'
        f'{emojis.BP} If you have leftover flasks: Brew potions that are useful in low areas\n'
        f'{emojis.BP} Level up professions if not done (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} If you need a higher score: Trade to {emojis.RUBY} rubies\n'
        f'{emojis.BP} If you have materials left: Trade to apples and sell\n'
        f'{emojis.BP} Sell everything you don\'t need for your desired score\n'
        f'{emojis.BP} Do not sell items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'TIME TRAVEL {tt.tt:,} BONUSES',
        description = embed_description
    )
    embed.add_field(name='UNLOCKS & BONUSES', value=unlocks, inline=False)
    embed.add_field(name='COMMAND YIELD', value=work_multiplier, inline=False)
    embed.add_field(name='COIN CAP', value=field_coin_cap, inline=False)
    if not mytt and tt.tt != 0:
        if 1 <= tt.tt <= 3:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt1_to_2, inline=False)
        elif 4 <= tt.tt <= 5:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt3_to_4, inline=False)
        elif 6 <= tt.tt <= 10:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt5_to_9, inline=False)
        elif 11 <= tt.tt <= 24:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt10_to_24, inline=False)
        elif tt.tt == 25:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt25, inline=False)
        else:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_stt, inline=False)
    return embed


async def embed_time_jump() -> discord.Embed:
    """Super timetravel guide"""
    requirements = (
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 25+\n'
        f'{emojis.BP} {emojis.TIME_KEY} TIME key (drops from the boss in dungeon 15-1)'
    )
    starter_bonuses = (
        f'{emojis.BP} Start with +25 LIFE (50 score)\n'
        f'{emojis.BP} Start with a new Tier I pet (300 score)\n'
        f'{emojis.BP} Start with +50 AT (400 score)\n'
        f'{emojis.BP} Start with +50 DEF (400 score)\n'
        f'{emojis.BP} Start with 35 of each monster drop (400 score)\n'
        f'{emojis.BP} Start with an OMEGA lootbox (500 score)\n'
        f'{emojis.BP} Start with a new Tier III pet (1,500 score)\n'
        f'{emojis.BP} Start with 10 ULTRA logs (1,750 score)\n'
        f'{emojis.BP} Start in area 2 (2,000 score)\n'
        f'{emojis.BP} Start with a new Tier I pet with 1 skill (4,500 score)\n'
        f'{emojis.BP} Start in area 3 (4,500 score)\n'
        f'{emojis.BP} Start with a GODLY lootbox (6,500 score)'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TIME JUMP / SUPER TIME TRAVEL (STT)',
        description = (
            f'Time jumping is unlocked once you reach {emojis.TIME_TRAVEL} TT 25. From this point onward you have '
            f'to use {strings.SLASH_COMMANDS_EPIC_RPG["time jump"]} to reach the next TT.\n'
            f'Time jump lets you choose a starter bonus. You can (and have to) choose **1** bonus.\n'
            f'These bonuses cost score points which are calculated based on your inventory and your gear '
            f'(see {strings.SLASH_COMMANDS_GUIDE["time jump score"]}).\n'
        )

    )
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='STARTER BONUSES', value=starter_bonuses, inline=False)
    return embed


async def embed_time_jump_score_stats() -> discord.Embed:
    """STT score stats & enchants embed"""
    base = (
        f'{emojis.BP} You have a base score of 8, regardless of anything else'
    )
    level = (
        f'{emojis.BP} 1 level without stats = 0.5 score\n'
        f'{emojis.BP} 1 level including its stats = 0.9 score\n'
    )
    stats = (
        f'{emojis.BP} 1 {emojis.STAT_AT} AT = 0.125 score\n'
        f'{emojis.BP} 1 {emojis.STAT_DEF} DEF = 0.15 score\n'
        f'{emojis.BP} 1 {emojis.STAT_LIFE} HP = 0.025 score\n'
        f'{emojis.DETAIL} Only **base** stats give score!\n'
        f'{emojis.DETAIL} This includes stats from level, food, boosts and gear\n'
    )
    enchants = (
        f'{emojis.BP} Enchants have a score that is 4x their bonus / 100\n'
        f'{emojis.DETAIL} Example: OMEGA enchant is `125 * 4 / 100` = 5 score\n'
    )
    calculation = (
        f'{emojis.BP} Add stats and level scores and ceil\n'
        f'{emojis.BP} Add both enchant scores and ceil\n'
    )
    calculator = (
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["time jump calculator"]} to calculate your score'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TIME JUMP SCORE • STATS & ENCHANTS',
    )
    embed.add_field(name='BASE SCORE', value=base, inline=False)
    embed.add_field(name='LEVEL', value=level, inline=False)
    embed.add_field(name='STATS', value=stats, inline=False)
    embed.add_field(name='ENCHANTS', value=enchants, inline=False)
    embed.add_field(name='HOW TO CALCULATE', value=calculation, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_time_jump_score_materials() -> discord.Embed:
    """STT score materials embed"""
    lootboxes = (
        f'{emojis.BP} 1 {emojis.LB_COMMON} common lootbox = 0.05 score\n'
        f'{emojis.BP} 1 {emojis.LB_UNCOMMON} uncommon lootbox = 0.1 score\n'
        f'{emojis.BP} 1 {emojis.LB_RARE} rare lootbox = 0.133... score\n'
        f'{emojis.BP} 1 {emojis.LB_EPIC} EPIC lootbox = 0.2 score\n'
        f'{emojis.BP} 1 {emojis.LB_EDGY} EDGY lootbox = 0.25 score\n'
        f'{emojis.BP} 1 {emojis.LB_OMEGA} OMEGA lootbox = 5 score\n'
        f'{emojis.BP} 1 {emojis.LB_GODLY} GODLY lootbox = 50 score\n'
        f'{emojis.BP} 1 {emojis.LB_VOID} VOID lootbox = 200 score\n'
    )
    farm_items = (
        f'{emojis.BP} 35 {emojis.POTATO} potatoes = 1 score\n'
        f'{emojis.BP} 30 {emojis.CARROT} carrots = 1 score\n'
        f'{emojis.BP} 25 {emojis.BREAD} bread = 1 score (best value)\n'
        f'{emojis.BP} 1 {emojis.SEED_POTATO} potato seed = 1 score\n'
        f'{emojis.BP} 1 {emojis.SEED_CARROT} carrot seed = 1 score\n'
        f'{emojis.BP} 1 {emojis.SEED_BREAD} bread seed = 1 score\n'
        f'{emojis.BP} 2,500 {emojis.SEED} seed = 1 score (10k seeds max)\n'
    )
    mob_drops = (
        f'{emojis.BP} 20 {emojis.WOLF_SKIN} wolf skins = 1 score\n'
        f'{emojis.BP} 20 {emojis.ZOMBIE_EYE} zombie eyes = 2 score\n'
        f'{emojis.BP} 20 {emojis.UNICORN_HORN} unicorn horns = 3 score\n'
        f'{emojis.BP} 20 {emojis.MERMAID_HAIR} mermaid hairs = 4 score\n'
        f'{emojis.BP} 20 {emojis.CHIP} chips = 5 score\n'
        f'{emojis.BP} 20 {emojis.DRAGON_SCALE} dragon scales = 10 score\n'
        f'{emojis.BP} 20 {emojis.DARK_ENERGY} dark energy = 15 score\n'
    )
    rubies = (
        f'{emojis.BP} 25 {emojis.RUBY} rubies = 1 score\n'
    )
    logs = (
        f'{emojis.BP} 25,000 {emojis.LOG} wooden logs = 1 score\n'
        f'{emojis.BP} 2,500 {emojis.LOG_EPIC} EPIC logs = 1 score\n'
        f'{emojis.BP} 250 {emojis.LOG_SUPER} SUPER logs = 1 score\n'
        f'{emojis.BP} 25 {emojis.LOG_MEGA} MEGA logs = 1 score\n'
        f'{emojis.BP} 2.5 {emojis.LOG_HYPER} HYPER log = 1 score\n'
        f'{emojis.BP} 1 {emojis.LOG_ULTRA} ULTRA log = 4 score\n'
        f'{emojis.BP} 1 {emojis.LOG_ULTIMATE} ULTIMATE log = 40 score\n'
    )
    fish = (
        f'{emojis.BP} 25,000 {emojis.FISH} normie fish = 1 score\n'
        f'{emojis.BP} 1,250 {emojis.FISH_GOLDEN} golden fish = 1 score\n'
        f'{emojis.BP} 12.5 {emojis.FISH_EPIC} EPIC fish = 1 score\n'
        f'{emojis.BP} 1 {emojis.FISH_SUPER} SUPER fish = 8 score\n'
    )
    fruit = (
        f'{emojis.BP} 5,000 {emojis.APPLE} apples = 1 score\n'
        f'{emojis.BP} 250 {emojis.BANANA} bananas = 1 score\n'
        f'{emojis.BP} 12 {emojis.WATERMELON} watermelons = 1 score\n'
    )
    other = (
        f'{emojis.BP} 500,000 {emojis.LIFE_POTION} life potions = 1 score (1m potions max)\n'
        f'{emojis.BP} 2 {emojis.LOTTERY_TICKET} lottery tickets = 1 score (200 tickets max)\n'
    )
    calculation = (
        f'{emojis.BP} Add lootbox and farm item scores and floor\n'
        f'{emojis.BP} Add mob drop scores and floor\n'
        f'{emojis.BP} Ceil life potion score\n'
        f'{emojis.BP} Ceil lottery ticket score\n'
        f'{emojis.BP} Add all other material scores and floor\n'
    )
    calculator = (
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["time jump calculator"]} to calculate your score'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TIME JUMP SCORE • MATERIALS',
    )
    embed.add_field(name='LOOTBOXES', value=lootboxes, inline=False)
    embed.add_field(name='FARM ITEMS', value=farm_items, inline=False)
    embed.add_field(name='MOB DROPS', value=mob_drops, inline=False)
    embed.add_field(name='RUBIES', value=rubies, inline=False)
    embed.add_field(name='LOGS', value=logs, inline=False)
    embed.add_field(name='FISH', value=fish, inline=False)
    embed.add_field(name='FRUIT', value=fruit, inline=False)
    embed.add_field(name='OTHER MATERIALS', value=other, inline=False)
    embed.add_field(name='HOW TO CALCULATE', value=calculation, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_time_jump_score_gear() -> discord.Embed:
    """STT score gear embed"""
    gear_basic = (
        f'{emojis.BP} {emojis.SWORD_BASIC} Basic Sword = 0.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_BASIC} Basic Armor = 0.5 score\n'
        f'{emojis.BP} {emojis.SWORD_WOODEN} Wooden Sword = 1 score\n'
        f'{emojis.BP} {emojis.ARMOR_FISH} Fish Armor = 1 score\n'
        f'{emojis.BP} {emojis.SWORD_FISH} Fish Sword = 1.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_WOLF} Wolf Armor = 1.5 score\n'
        f'{emojis.BP} {emojis.SWORD_APPLE} Apple Sword = 2 score\n'
        f'{emojis.BP} {emojis.ARMOR_EYE} Eye Armor = 2 score\n'
        f'{emojis.BP} {emojis.SWORD_ZOMBIE} Zombie Sword = 2.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_BANANA} Banana Armor = 2.5 score\n'
        f'{emojis.BP} {emojis.SWORD_RUBY} Ruby Sword = 3 score\n'
        f'{emojis.BP} {emojis.ARMOR_EPIC} Epic Armor = 3 score\n'
    )
    gear_advanced = (
        f'{emojis.BP} {emojis.SWORD_UNICORN} Unicorn Sword = 3.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_RUBY} Ruby Armor = 3.5 score\n'
        f'{emojis.BP} {emojis.SWORD_HAIR} Hair Sword = 4 score\n'
        f'{emojis.BP} {emojis.ARMOR_COIN} Coin Armor = 4 score\n'
        f'{emojis.BP} {emojis.SWORD_COIN} Coin Sword = 4.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_MERMAID} Mermaid Armor = 4.5 score\n'
        f'{emojis.BP} {emojis.SWORD_ELECTRONICAL} Electronical Sword = 5 score\n'
        f'{emojis.BP} {emojis.ARMOR_ELECTRONICAL} Electronical Armor = 5 score\n'
        f'{emojis.BP} {emojis.SWORD_EDGY} EDGY Sword = 5.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_EDGY} EDGY Armor = 5.5 score\n'
    )
    gear_forged = (
        f'{emojis.BP} {emojis.SWORD_ULTRAEDGY} ULTRA-EDGY Sword = 6 score\n'
        f'{emojis.BP} {emojis.ARMOR_ULTRAEDGY} ULTRA-EDGY Armor = 6 score\n'
        f'{emojis.BP} {emojis.SWORD_OMEGA} OMEGA Sword = 6.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_OMEGA} OMEGA Armor = 6.5 score\n'
        f'{emojis.BP} {emojis.SWORD_ULTRAOMEGA} ULTRA-OMEGA Sword = 7 score\n'
        f'{emojis.BP} {emojis.ARMOR_ULTRAOMEGA} ULTRA-OMEGA Armor = 7 score\n'
        f'{emojis.BP} {emojis.SWORD_GODLY} GODLY Sword = 7.5 score\n'
    )
    gear_tryhard = (
        f'{emojis.BP} {emojis.SWORD_BANANA} Banana Sword = 8 score\n'
        f'{emojis.BP} {emojis.ARMOR_SCALED} Scaled Armor = 8 score\n'
        f'{emojis.BP} {emojis.SWORD_SCALED} Scaled Sword = 8.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_WATERMELON} Watermelon Armor = 8.5 score\n'
        f'{emojis.BP} {emojis.SWORD_WATERMELON} Watermelon Sword = 9 score\n'
        f'{emojis.BP} {emojis.ARMOR_SUPER} Super Armor = 9 score\n'
        f'{emojis.BP} {emojis.SWORD_EPIC} Epic Sword = 9.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_LOOTBOX} Lootbox Armor = 9.5 score\n'
        f'{emojis.BP} {emojis.SWORD_LOTTERY} Lottery Sword = 10 score\n'
        f'{emojis.BP} {emojis.ARMOR_WOODEN} Wooden Armor = 10 score\n'
    )
    gear_void = (
        f'{emojis.BP} {emojis.SWORD_VOID} VOID Sword = 10.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_VOID} VOID Armor = 10.5 score\n'
        f'{emojis.BP} {emojis.SWORD_ABYSS} ABYSS Sword = 11 score\n'
        f'{emojis.BP} {emojis.ARMOR_ABYSS} ABYSS Armor = 11 score\n'
        f'{emojis.BP} {emojis.SWORD_CORRUPTED} CORRUPTED Sword = 11.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_CORRUPTED} CORRUPTED Armor = 11.5 score\n'
        f'{emojis.BP} {emojis.SWORD_SPACE} SPACE Sword = 12 score\n'
        f'{emojis.BP} {emojis.ARMOR_SPACE} SPACE Armor = 12 score\n'
        f'{emojis.BP} {emojis.SWORD_TIME} TIME Sword = 12.5 score\n'
        f'{emojis.BP} {emojis.ARMOR_TIME} TIME Armor = 12.5 score\n'
    )
    calculation = (
        f'{emojis.BP} Both scores are added and **not** rounded\n'
    )
    note = (
        f'{emojis.BP} These scores do **not** include AT and DEF of the gear!\n'
        f'{emojis.DETAIL} Stats are calculated seperately by the game\n'
        f'{emojis.DETAIL} See topic `Stats & enchants` for details\n'
        f'{emojis.BP} Gear not listed here doesn\'t have a known value yet\n'
    )
    calculator = (
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["time jump calculator"]} to calculate your score'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TIME JUMP SCORE • GEAR',
    )
    embed.add_field(name='BASIC GEAR', value=gear_basic, inline=False)
    embed.add_field(name='ADVANCED GEAR', value=gear_advanced, inline=False)
    embed.add_field(name='FORGED GEAR', value=gear_forged, inline=False)
    embed.add_field(name='TRYHARD GEAR', value=gear_tryhard, inline=False)
    embed.add_field(name='VOID GEAR', value=gear_void, inline=False)
    embed.add_field(name='HOW TO CALCULATE', value=calculation, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_time_jump_calculator(area_no: int, inventory: str, profile_data: dict, boosts_data: dict,
                                    option_inventory: str, option_stats: str) -> discord.Embed:
    """STT score calculator embed"""
    message_area = 'The TOP' if area_no == 21 else f'area {area_no}'
    if option_inventory == INVENTORY_CURRENT:
        calculated_area = message_area
    elif option_inventory == INVENTORY_TRADE_A15:
        calculated_area = 'area 15'
    else:
        calculated_area = 'areas 16+'
    inventory = inventory.lower()
    fish = await functions.inventory_get(inventory, 'normie fish')
    fishgolden = await functions.inventory_get(inventory, 'golden fish')
    fishepic = await functions.inventory_get(inventory, 'epic fish')
    fishsuper = await functions.inventory_get(inventory, 'super fish')
    log = await functions.inventory_get(inventory, 'wooden log')
    logepic = await functions.inventory_get(inventory, 'epic log')
    logsuper = await functions.inventory_get(inventory, 'super log')
    logmega = await functions.inventory_get(inventory, 'mega log')
    loghyper = await functions.inventory_get(inventory, 'hyper log')
    logultra = await functions.inventory_get(inventory, 'ultra log')
    logultimate = await functions.inventory_get(inventory, 'ultimate log')
    apple = await functions.inventory_get(inventory, 'apple')
    banana = await functions.inventory_get(inventory, 'banana')
    watermelon = await functions.inventory_get(inventory, 'watermelon')
    ruby = await functions.inventory_get(inventory, 'ruby')
    wolfskin = await functions.inventory_get(inventory, 'wolf skin')
    zombieeye = await functions.inventory_get(inventory, 'zombie eye')
    unicornhorn = await functions.inventory_get(inventory, 'unicorn horn')
    mermaidhair = await functions.inventory_get(inventory, 'mermaid hair')
    chip = await functions.inventory_get(inventory, 'chip')
    dragonscale = await functions.inventory_get(inventory, 'dragon scale')
    darkenergy = await functions.inventory_get(inventory, 'dark energy')
    lbcommon = await functions.inventory_get(inventory, 'common lootbox')
    lbuncommon = await functions.inventory_get(inventory, 'uncommon lootbox')
    lbrare = await functions.inventory_get(inventory, 'rare lootbox')
    lbepic = await functions.inventory_get(inventory, 'epic lootbox')
    lbedgy = await functions.inventory_get(inventory, 'edgy lootbox')
    lbomega = await functions.inventory_get(inventory, 'omega lootbox')
    lbgodly = await functions.inventory_get(inventory, 'godly lootbox')
    lbvoid = await functions.inventory_get(inventory, 'void lootbox')
    lifepotion = await functions.inventory_get(inventory, 'life potion')
    potato = await functions.inventory_get(inventory, 'potato')
    carrot = await functions.inventory_get(inventory, 'carrot')
    bread = await functions.inventory_get(inventory, 'bread')
    seed = await functions.inventory_get(inventory, 'seed')
    seed_bread = await functions.inventory_get(inventory, 'bread seed')
    seed_carrot = await functions.inventory_get(inventory, 'carrot seed')
    seed_potato = await functions.inventory_get(inventory, 'potato seed')
    lottery_ticket = await functions.inventory_get(inventory, 'lottery ticket')

    score_lbcommon = lbcommon * 0.05
    score_lbuncommon = lbuncommon * 0.1
    score_lbrare = lbrare * (0.4 / 3)
    score_lbepic = lbepic * 0.2
    score_lbedgy = lbedgy * 0.25
    score_lbomega = lbomega * 5
    score_lbgodly = lbgodly * 50
    score_lbvoid = lbvoid * 200
    score_lootboxes = (
        score_lbcommon + score_lbuncommon + score_lbrare + score_lbepic + score_lbedgy + score_lbomega + score_lbgodly
        + score_lbvoid
    )
    score_bread = bread / 25
    score_carrot = carrot / 30
    score_potato = potato / 35
    score_seed = seed / 2500
    score_seed_bread = seed_bread
    score_seed_carrot = seed_carrot
    score_seed_potato = seed_potato
    score_farm_items = (
        score_bread + score_carrot + score_potato + score_seed + score_seed_bread + score_seed_potato + score_seed_carrot
    )
    score_total_lootboxes_farm_items = score_lootboxes + score_farm_items
    score_wolfskin = wolfskin / 20
    score_zombieeye = zombieeye / 10
    score_unicornhorn = unicornhorn / (20 / 3)
    score_mermaidhair = mermaidhair / 5
    score_chip = chip / 4
    score_dragonscale = dragonscale / 2
    score_darkenergy = darkenergy * 0.75
    score_total_mobdrops = (
        score_wolfskin + score_zombieeye + score_unicornhorn + score_mermaidhair + score_chip + score_dragonscale
        + score_darkenergy
    )
    score_logultimate = logultimate * 40
    score_fishsuper = fishsuper * 8
    score_watermelon = watermelon / 12
    score_lifepotion = lifepotion / 500_000
    score_lottery = lottery_ticket / 2
    score_total_other = score_lottery + score_lifepotion
    score_total = floor(score_total_lootboxes_farm_items) + floor(score_total_mobdrops) + ceil(score_lottery) + ceil(score_lifepotion)

    field_lootboxes = (
        f'{emojis.BP} {lbcommon:,} {emojis.LB_COMMON} = {score_lbcommon:,.2f}\n'
        f'{emojis.BP} {lbuncommon:,} {emojis.LB_UNCOMMON} = {score_lbuncommon:,.2f}\n'
        f'{emojis.BP} {lbrare:,} {emojis.LB_RARE} = {score_lbrare:,.2f}\n'
        f'{emojis.BP} {lbepic:,} {emojis.LB_EPIC} = {score_lbepic:,.2f}\n'
        f'{emojis.BP} {lbedgy:,} {emojis.LB_EDGY} = {score_lbedgy:,.2f}\n'
        f'{emojis.BP} {lbomega:,} {emojis.LB_OMEGA} = {score_lbomega:,.2f}\n'
        f'{emojis.BP} {lbgodly:,} {emojis.LB_GODLY} = {score_lbgodly:,.2f}\n'
        f'{emojis.BP} {lbvoid:,} {emojis.LB_VOID} = {score_lbvoid:,.2f}\n'
        f'{emojis.BP} Total: **{score_lootboxes:,.2f}**\n'
    )
    field_mobdrops = (
        f'{emojis.BP} {wolfskin:,} {emojis.WOLF_SKIN} = {score_wolfskin:,.2f}\n'
        f'{emojis.BP} {zombieeye:,} {emojis.ZOMBIE_EYE} = {score_zombieeye:,.2f}\n'
        f'{emojis.BP} {unicornhorn:,} {emojis.UNICORN_HORN} = {score_unicornhorn:,.2f}\n'
        f'{emojis.BP} {mermaidhair:,} {emojis.MERMAID_HAIR} = {score_mermaidhair:,.2f}\n'
        f'{emojis.BP} {chip:,} {emojis.CHIP} = {score_chip:,.2f}\n'
        f'{emojis.BP} {dragonscale:,} {emojis.DRAGON_SCALE} = {score_dragonscale:,.2f}\n'
        f'{emojis.BP} {darkenergy:,} {emojis.DARK_ENERGY} = {score_darkenergy:,.2f}\n'
        f'{emojis.BP} Total: **{score_total_mobdrops:,.2f}**\n'
    )
    field_farming = (
        f'{emojis.BP} {bread:,} {emojis.BREAD} = {score_bread:,.2f}\n'
        f'{emojis.BP} {carrot:,} {emojis.CARROT} = {score_carrot:,.2f}\n'
        f'{emojis.BP} {potato:,} {emojis.POTATO} = {score_potato:,.2f}\n'
        f'{emojis.BP} {seed:,} {emojis.SEED} = {score_seed:,.2f}\n'
        f'{emojis.BP} {seed_bread:,} {emojis.SEED_BREAD} = {score_seed_bread:,.2f}\n'
        f'{emojis.BP} {seed_carrot:,} {emojis.SEED_CARROT} = {score_seed_carrot:,.2f}\n'
        f'{emojis.BP} {seed_potato:,} {emojis.SEED_POTATO} = {score_seed_potato:,.2f}\n'
        f'{emojis.BP} Total: **{score_farm_items:,.2f}**\n'
    )
    embed = discord.Embed(
        color=settings.EMBED_COLOR,
        title='TIME JUMP SCORE CALCULATOR',
        description = (
            f'{emojis.BP} Your current area: **{message_area.capitalize()}**\n'
            f'{emojis.BP} Inventory mode: **{option_inventory}**\n'
            f'{emojis.BP} Stats mode: **{option_stats}**'
        ),
    )
    embed.add_field(name='LOOTBOXES', value=field_lootboxes, inline=True)
    embed.add_field(name='FARM ITEMS', value=field_farming, inline=True)
    embed.add_field(name='MOB DROPS', value=field_mobdrops, inline=True)

    if option_inventory in (INVENTORY_TRADE_A15, INVENTORY_TRADE_A16):
        areas = await database.get_all_areas()
        all_areas = {}
        for area in areas:
            all_areas[area.area_no] = area
        current_area = all_areas[area_no]

        loghyper = loghyper + (logultra * 8)
        logmega = logmega + (loghyper * 8)
        logsuper = logsuper + (logmega * 8)
        logepic = logepic + (logsuper * 8)
        log = log + (logepic * 20)
        fishgolden = fishgolden + (fishepic * 80)
        fish = fish + (fishgolden * 12)
        apple = apple + (banana * 12)

        original_area = area_no
        areas_best_changes = []

        # Get the amount of logs for the current area
        log = log + (fish * current_area.trade_fish_log)
        if not current_area.trade_apple_log == 0:
            log = log + (apple * current_area.trade_apple_log)
            apple = 0
        if not current_area.trade_ruby_log == 0:
            log = log + (ruby * current_area.trade_ruby_log)
            ruby = 0

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
            else:
                fish_rate_change = 1
                apple_rate_change = 1
                ruby_rate_change = 1
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

        # Get the amount of logs in each area
        areas_log_amounts = []
        trade_fish_rate_next = None
        trade_apple_rate_next = None
        trade_ruby_rate_next = None
        for best_change in areas_best_changes[original_area-1:]:
            trade_area = best_change[0]
            trade_best_change = best_change[1]
            trade_fish_rate = best_change[2]
            trade_apple_rate = best_change[3]
            trade_ruby_rate = best_change[4]
            if not trade_area == len(areas_best_changes):
                next_area = areas_best_changes[trade_area]
                trade_fish_rate_next = next_area[2]
                trade_apple_rate_next = next_area[3]
                trade_ruby_rate_next = next_area[4]

            if not (trade_apple_rate_next == 0) and not (apple == 0):
                log = log + (apple * trade_apple_rate_next)
                apple = 0
            if not (trade_ruby_rate_next == 0) and not (ruby == 0):
                log = log + (ruby * trade_ruby_rate_next)
                ruby = 0

            if trade_area == original_area:
                areas_log_amounts.append([trade_area, log, trade_ruby_rate])

            if trade_best_change == 0:
                log = log / trade_fish_rate
                log = log * trade_fish_rate_next
            elif trade_best_change == 1:
                log = log / trade_apple_rate
                log = log * trade_apple_rate_next
            elif trade_best_change == 2:
                log = log / trade_ruby_rate
                log = log * trade_ruby_rate_next

            if not trade_area == len(areas_best_changes):
                areas_log_amounts.append([trade_area+1, log, trade_ruby_rate_next])

        a15 = a16 = (0,0,0)
        for log_amount in areas_log_amounts:
            if log_amount[0] == 15:
                a15 = log_amount
            elif log_amount[0] == 21:
                a16 = log_amount
        log_a15 = a15[1]
        ruby_rate_a15 = a15[2]
        try:
            ruby_a15 = floor(log_a15 / ruby_rate_a15)
        except ZeroDivisionError:
            ruby_a15 = 0
        log_a16 = a16[1]
        ruby_rate_a16 = a16[2]
        ruby_a16 = floor(log_a16 / ruby_rate_a16)

        if option_inventory == INVENTORY_TRADE_A15:
            ruby_str = f'{ruby_a15:,}' if ruby_a15 != 0 else 'N/A'
            score_ruby = ruby_a15 / 25
        else:
            ruby_str = f'{ruby_a16:,}'
            score_ruby = ruby_a16 / 25
        score_total_materials = score_ruby + score_logultimate + score_fishsuper + score_watermelon
        score_total += floor(score_total_materials)

        field_materials = (
            f'{emojis.BP} {ruby_str} {emojis.RUBY} = {score_ruby:,.2f}\n'
            f'{emojis.BP} {logultimate:,} {emojis.LOG_ULTIMATE} = {score_logultimate:,.2f}\n'
            f'{emojis.BP} {fishsuper:,} {emojis.FISH_SUPER} = {score_fishsuper:,.2f}\n'
            f'{emojis.BP} {watermelon:,} {emojis.WATERMELON} = {score_watermelon:,.2f}\n'
            f'{emojis.BP} Total: **{score_total_materials:,.2f}**\n'
        )
        field_other = (
            f'{emojis.BP} {lifepotion:,} {emojis.LIFE_POTION} = {score_lifepotion:,.2f}\n'
            f'{emojis.BP} {lottery_ticket} {emojis.LOTTERY_TICKET} = {score_lottery:,.2f}\n'
            f'{emojis.BP} Total: **{score_total_other:,.2f}**\n'
        )
        notes = (
            f'{emojis.BP} This calculation assumes that you trade **all** of your materials to rubies\n'
            f'{emojis.BP} Materials you may still need for crafting gear are not subtracted'
        )
        embed.add_field(name='MATERIALS', value=field_materials, inline=True)
        embed.add_field(name='OTHER', value=field_other, inline=True)


    if option_inventory == INVENTORY_CURRENT:
        score_log = log / 25_000
        score_logepic = logepic / 2_500
        score_logsuper = logsuper / 250
        score_logmega = logmega / 25
        score_loghyper = loghyper / 2.5
        score_logultra = logultra * 4
        score_ruby = ruby / 25
        score_total_materials_1 = (
            score_log + score_logepic + score_logsuper + score_logmega + score_loghyper + score_logultra
            + score_logultimate + score_ruby
        )
        score_fish = fish / 25_000
        score_fishgolden = fishgolden / 1_250
        score_fishepic = fishepic / 12.5
        score_apple = apple / 5_000
        score_banana = banana / 250
        score_total_materials_2 = (
            score_fish + score_fishgolden + score_fishepic + score_fishsuper + score_apple + score_banana
            + score_watermelon
        )
        score_total_materials = score_total_materials_1 + score_total_materials_2
        score_total_other = score_lifepotion + score_lottery
        score_total += floor(score_total_materials)

        field_materials_1 = (
            f'{emojis.BP} {log:,} {emojis.LOG} = {score_log:,.2f}\n'
            f'{emojis.BP} {logepic:,} {emojis.LOG_EPIC} = {score_logepic:,.2f}\n'
            f'{emojis.BP} {logsuper:,} {emojis.LOG_SUPER} = {score_logsuper:,.2f}\n'
            f'{emojis.BP} {logmega:,} {emojis.LOG_MEGA} = {score_logmega:,.2f}\n'
            f'{emojis.BP} {loghyper:,} {emojis.LOG_HYPER} = {score_loghyper:,.2f}\n'
            f'{emojis.BP} {logultra:,} {emojis.LOG_ULTRA} = {score_logultra:,.2f}\n'
            f'{emojis.BP} {logultimate:,} {emojis.LOG_ULTIMATE} = {score_logultimate:,.2f}\n'
            f'{emojis.BP} {ruby:,} {emojis.RUBY} = {score_ruby:,.2f}\n'
            f'{emojis.BP} Total: **{score_total_materials_1:,.2f}**\n'
        )
        field_materials_2 = (
            f'{emojis.BP} {fish:,} {emojis.FISH} = {score_fish:,.2f}\n'
            f'{emojis.BP} {fishgolden:,} {emojis.FISH_GOLDEN} = {score_fishgolden:,.2f}\n'
            f'{emojis.BP} {fishepic:,} {emojis.FISH_EPIC} = {score_fishepic:,.2f}\n'
            f'{emojis.BP} {fishsuper:,} {emojis.FISH_SUPER} = {score_fishsuper:,.2f}\n'
            f'{emojis.BP} {apple:,} {emojis.APPLE} = {score_apple:,.2f}\n'
            f'{emojis.BP} {banana:,} {emojis.BANANA} = {score_banana:,.2f}\n'
            f'{emojis.BP} {watermelon:,} {emojis.WATERMELON} = {score_watermelon:,.2f}\n'
            f'{emojis.BP} Total: **{score_total_materials_2:,.2f}**\n'
        )
        field_other = (
            f'{emojis.BP} {lifepotion:,} {emojis.LIFE_POTION} = {score_lifepotion:,.2f}\n'
            f'{emojis.BP} {lottery_ticket} {emojis.LOTTERY_TICKET} = {score_lottery:,.2f}\n'
            f'{emojis.BP} Total: **{score_total_other:,.2f}**\n'
        )
        notes = (
            f'{emojis.BP} This calculation shows your inventory as is\n'
            f'{emojis.BP} Materials you may still need for crafting gear are not subtracted'
        )
        embed.add_field(name='MATERIALS (I)', value=field_materials_1, inline=True)
        embed.add_field(name='MATERIALS (II)', value=field_materials_2, inline=True)
        embed.add_field(name='OTHER', value=field_other, inline=True)

    if option_stats in (STATS_CURRENT, STATS_MANUAL):
        enchant_multipliers = {
            'normie': 0.05,
            'good': 0.15,
            'great': 0.25,
            'mega': 0.4,
            'epic': 0.6,
            'hyper': 0.7,
            'ultimate': 0.8,
            'perfect': 0.9,
            'edgy': 0.95,
            'ultra-edgy': 1,
            'omega': 1.25,
            'ultra-omega': 1.5,
            'godly': 2,
            'void': 3,
        }
        armor_enchant_multiplier = enchant_multipliers.get(profile_data['enchant_armor'].lower(), 0)
        sword_enchant_multiplier = enchant_multipliers.get(profile_data['enchant_sword'].lower(), 0)
        score_sword_enchant = sword_enchant_multiplier * 4
        score_armor_enchant = armor_enchant_multiplier * 4
        score_enchants = score_armor_enchant + score_sword_enchant

        if option_stats == STATS_CURRENT:
            at_multiplier = def_multiplier = life_multiplier = 1
            if profile_data['horse_type'] in ('magic', 'strong', 'defender', 'tank'):
                horse_data: database.Horse = await database.get_horse(profile_data['horse_tier'])
                horse_epicness_type_factor = 1 + profile_data['horse_epicness'] * 0.005
                if profile_data['horse_type'] == 'magic':
                    horse_boost = horse_data.magic_level_bonus * profile_data['horse_level'] * horse_epicness_type_factor
                    armor_enchant_multiplier *= 1 + horse_boost / 100
                    sword_enchant_multiplier *= 1 + horse_boost / 100
                if profile_data['horse_type'] == 'strong':
                    horse_boost = horse_data.strong_level_bonus * profile_data['horse_level'] * horse_epicness_type_factor
                    at_multiplier += horse_boost / 100
                if profile_data['horse_type'] == 'defender':
                    horse_boost = horse_data.def_level_bonus * profile_data['horse_level'] * horse_epicness_type_factor
                    def_multiplier += horse_boost / 100
                if profile_data['horse_type'] == 'tank':
                    horse_boost = horse_data.tank_level_bonus * profile_data['horse_level'] * horse_epicness_type_factor
                    life_multiplier += horse_boost / 100
            base_at = functions.round_school(profile_data['at'] / (1 + sword_enchant_multiplier) / at_multiplier) - boosts_data['at']
            base_def = functions.round_school(profile_data['def'] / (1 + armor_enchant_multiplier) / def_multiplier) - boosts_data['def']
            base_life = functions.round_school(profile_data['life'] / life_multiplier) - boosts_data['life']
        else:
            sword_at = profile_data['sword'].stat_at if profile_data['sword'] is not None else 0
            armor_def = profile_data['armor'].stat_def if profile_data['armor'] is not None else 0
            base_at = profile_data['level'] + sword_at + profile_data['extra_at']
            base_def = profile_data['level'] + armor_def + profile_data['extra_def']
            base_life = 95 + (5 * profile_data['level']) + profile_data['extra_life']
        score_level = profile_data['level'] * 0.5
        score_at = base_at * 0.125
        score_def = base_def * 0.15
        score_life = base_life * (1 / 40)
        score_total_stats = score_at + score_def + score_life + score_level
        score_total += ceil(score_total_stats)
        field_stats = (
            f'{emojis.BP} {profile_data["level"]:,} {emojis.STAT_LEVEL} = {score_level:,.2f}\n'
            f'{emojis.BP} {base_at:,} {emojis.STAT_AT} = {score_at:,.2f}\n'
            f'{emojis.BP} {base_def:,} {emojis.STAT_DEF} = {score_def:,.2f}\n'
            f'{emojis.BP} {base_life:,} {emojis.STAT_LIFE} = {score_life:,.2f}\n'
            f'{emojis.BP} Total: **{score_total_stats:,.2f}**\n'
        )
        if profile_data['sword'] is not None:
            sword_item = profile_data['sword']
            sword = f'{sword_item.emoji} {sword_item.name} = {sword_item.score:,.2f}'
            score_sword = sword_item.score
        else:
            sword = 'No or unknown sword = 0.00'
            score_sword = 0
        if profile_data['armor'] is not None:
            armor_item = profile_data['armor']
            armor = f'{armor_item.emoji} {armor_item.name} = {armor_item.score:,.2f}'
            score_armor = armor_item.score
        else:
            armor = 'No or unknown armor = 0.00'
            score_armor = 0
        score_total_gear = score_enchants + score_armor + score_sword
        score_total += ceil(score_enchants) + score_armor + score_sword
        field_gear = (
            f'{emojis.BP} {sword}\n'
            f'{emojis.DETAIL} {emojis.PR_ENCHANTER} {profile_data["enchant_sword"]} enchant = '
            f'{score_sword_enchant:,.2f}\n'
            f'{emojis.BP} {armor}\n'
            f'{emojis.DETAIL} {emojis.PR_ENCHANTER} {profile_data["enchant_armor"]} enchant = '
            f'{score_armor_enchant:,.2f}\n'
            f'{emojis.BP} Total: **{score_total_gear:,.2f}**\n'
        )
        score_total += 8 # Unknown base score coming from wherever
        notes = (
            f'{notes}\n'
            f'{emojis.BP} This calculation shows an approximation of your full score\n'
            f'{emojis.DETAIL} This might not always be 100% accurate!\n'
            f'{emojis.DETAIL} An active quest adds 1 score which is not listed here'
        )
        embed.add_field(name='BASE STATS', value=field_stats, inline=True)
        embed.add_field(name='GEAR & ENCHANTS', value=field_gear, inline=True)

    field_totals = (
        f'{emojis.BP} Lootboxes & farm items: {score_total_lootboxes_farm_items:,.2f} ➜ {floor(score_total_lootboxes_farm_items)}\n'
        f'{emojis.BP} Mob drops: {score_total_mobdrops:,.2f} ➜ {floor(score_total_mobdrops)}\n'
        f'{emojis.BP} Materials: {score_total_materials:,.2f} ➜ {floor(score_total_materials)}\n'
        f'{emojis.BP} Life potions: {score_lifepotion:,.2f} ➜ {ceil(score_lifepotion)}\n'
        f'{emojis.BP} Lottery tickets: {score_lottery:,.2f} ➜ {ceil(score_lottery)}'
    )
    if option_stats in (STATS_CURRENT, STATS_MANUAL):
        field_totals = (
            f'{emojis.BP} Base score: 8\n'
            f'{field_totals}\n'
            f'{emojis.BP} Stats: {score_total_stats:,.2f} ➜ {ceil(score_total_stats)}\n'
            f'{emojis.BP} Gear: {score_armor + score_sword:,.2f} ➜ {score_armor + score_sword:g}\n'
            f'{emojis.BP} Enchants: {score_enchants:,.2f} ➜ {ceil(score_enchants)}'
        )
    field_totals = (
        f'{field_totals}\n'
        f'{emojis.BP} Total score {calculated_area}: **{score_total:,g}**\n'
    )
    embed.description = (
        f'{embed.description}\n'
        f'{emojis.BP} Total score: **{score_total:,g}**\n'
    )
    embed.add_field(name='TOTALS', value=field_totals, inline=False)
    embed.add_field(name='NOTE', value=notes, inline=False)

    return embed