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
TOPIC_TJ = 'Time jump'
TOPIC_TJ_SCORE = 'Time jump score'

TOPICS = [
    TOPIC_TT,
    TOPIC_TJ,
    TOPIC_TJ_SCORE,
]

MATERIALS_CURRENT = 'Calculate as is'
MATERIALS_TRADE = 'Trade materials to rubies'

MATERIALS_CALCULATION = [
    MATERIALS_CURRENT,
    MATERIALS_TRADE
]

# --- Commands ---
async def command_time_travel_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Timetravel guide command"""
    topics_functions = {
        TOPIC_TT: embed_time_travel,
        TOPIC_TJ: embed_time_jump,
        TOPIC_TJ_SCORE: embed_time_jump_score,
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
    if timetravel == 1000:
        await ctx.respond('https://c.tenor.com/OTU2-ychJwsAAAAC/lightning-squidward.gif')
        return
    tt: database.TimeTravel = await database.get_time_travel(timetravel)
    embed = await embed_time_travel_bonuses(tt, mytt)
    await ctx.respond(embed=embed)


async def command_tj_score_calculator(bot: discord.Bot, ctx: discord.ApplicationContext, area_no: int,
                                      trade_materials: bool) -> None:
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

    view = views.TimeJumpCalculationTypeView(ctx, area_no, inventory, trade_materials, embed_tj_score_calculator)
    embed = await embed_tj_score_calculator(area_no, inventory.lower(), trade_materials)
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()


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
        f'{emojis.BP} Arena cookies \n'
        f'{emojis.BP} Coins (this includes your bank account)\n'
        f'{emojis.BP} Dragon essences\n'
        f'{emojis.BP} Epic coins\n'
        f'{emojis.BP} Epic shop items\n'
        f'{emojis.BP} Event items (if an event is active)\n'
        f'{emojis.BP} GODLY horse tokens\n'
        f'{emojis.BP} Guild rings\n'
        f'{emojis.BP} Legendary toothbrushes\n'
        f'{emojis.BP} Magic chairs\n'
        f'{emojis.BP} Profession levels\n'
        f'{emojis.BP} OMEGA horse tokens\n'
        f'{emojis.BP} TIME dragon essences\n'
        f'{emojis.BP} Your guild\n'
        f'{emojis.BP} Your horse\n'
        f'{emojis.BP} Your marriage partner\n'
        f'{emojis.BP} Your pets\n'
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
    return embed


async def embed_time_travel_bonuses(tt: database.TimeTravel, mytt: bool = False):
    """Embed with details for specific time travel"""
    bonus_xp = (99 + tt.tt) * tt.tt / 2
    bonus_duel_xp = (99 + tt.tt) * tt.tt / 4
    bonus_drop_chance = (49 + tt.tt) * tt.tt / 2
    dynamite_rubies = 1 + (bonus_drop_chance / 100)
    greenhouse_watermelon_min = dynamite_rubies * 2
    greenhouse_watermelon_max = dynamite_rubies * 3
    bigboat_superfish = dynamite_rubies / 1.15
    chainsaw_ultimate = dynamite_rubies / 3.5
    dynamite_rubies = Decimal(dynamite_rubies).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    greenhouse_watermelon_min = Decimal(greenhouse_watermelon_min).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    greenhouse_watermelon_max = Decimal(greenhouse_watermelon_max).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    chainsaw_ultimate = Decimal(chainsaw_ultimate).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    rubies = int(dynamite_rubies)
    watermelon_min = int(greenhouse_watermelon_min)
    watermelon_max = int(greenhouse_watermelon_max)
    super_fish = int(bigboat_superfish)
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
    bonus_xp = f'{bonus_xp:,g}'
    bonus_duel_xp = f'{bonus_duel_xp:,g}'
    bonus_drop_chance = f'{bonus_drop_chance:,g}'
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
        f"{unlocks}{emojis.BP} **{bonus_xp} %** increased **XP** from everything except duels\n"
        f'{emojis.BP} **{bonus_duel_xp} %** increased **XP** from **duels**\n'
        f'{emojis.BP} **{bonus_drop_chance} %** extra chance to get **monster drops**\n'
        f'{emojis.BP} **{bonus_drop_chance} %** more **items** with work commands\n'
        f'{emojis.BP} **x{enchant_multiplier}** enchanting multiplier (_approximation formula_)\n'
    )
    if tt.tt > 1:
        unlocks = (
            f'{unlocks.strip()}\n'
            f'{emojis.BP} **{tt.tt + 5}** pet slots'
        )
    if tt.tt > 0:
        unlocks = (
            f'{unlocks.strip()}\n'
            f'{emojis.BP} Higher chance to get +1 tier in {strings.SLASH_COMMANDS_EPIC_RPG["horse breeding"]} and '
            f'{strings.SLASH_COMMANDS_EPIC_RPG["pets fusion"]} (chance unknown)\n'
        )
    coin_cap = f'{pow(tt.tt, 4) * 500_000_000:,}' if tt.tt > 0 else '100,000 - 14,400,000'
    field_coin_cap = (
        f'{emojis.BP} ~**{coin_cap}** {emojis.COIN} coins\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["coin cap calculator"]} to see your exact cap\n'
    )
    work_multiplier = (
        f'{emojis.BP} ~**{watermelon_min:,}**-**{watermelon_max:,}** {emojis.WATERMELON} with '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["greenhouse"]}\n'
        f'{emojis.BP} **{rubies:,}** {emojis.RUBY} with {strings.SLASH_COMMANDS_EPIC_RPG["dynamite"]}\n'
        f'{emojis.BP} **{rubies:,}** {emojis.LOG_HYPER} / {emojis.LOG_ULTRA} with {strings.SLASH_COMMANDS_EPIC_RPG["chainsaw"]}\n'
        f'{emojis.BP} ~**{super_fish:,}** {emojis.FISH_SUPER} with {strings.SLASH_COMMANDS_EPIC_RPG["bigboat"]}\n'
        f'{emojis.BP} ~**{ultimate_logs:,}** {emojis.LOG_ULTIMATE} with {strings.SLASH_COMMANDS_EPIC_RPG["chainsaw"]}\n'
    )
    prep_tt1_to_2 = (
        f'{emojis.BP} If your horse is T6+: Get 30m coins\n'
        f'{emojis.BP} If your horse is <T6: Get 50m coins\n'
        f'{emojis.BP} If you need money: Do boosted minibosses, use {strings.SLASH_COMMANDS_EPIC_RPG["drill"]} and '
        f'sell mob drops\n'
        f'{emojis.BP} If you need money and are impatient: sell {emojis.APPLE} apples\n'
        f'{emojis.BP} Level up professions (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} Sell everything else **except** the items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}\n'
        f'{emojis.BP} Don\'t forget to sell your armor and sword!'
    )
    prep_tt3_to_4 = (
        f'{emojis.BP} If your horse is T6+: Get 50m coins\n'
        f'{emojis.BP} If your horse is <T6: Get 150m coins\n'
        f'{emojis.BP} If you need money: Do boosted minibosses, use {strings.SLASH_COMMANDS_EPIC_RPG["dynamite"]} and '
        f'sell mob drops\n'
        f'{emojis.BP} If you need money and are impatient: sell {emojis.APPLE} apples\n'
        f'{emojis.BP} Level up professions if not done (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.BP} If you have materials left: Trade to {emojis.APPLE} apples and sell\n'
        f'{emojis.BP} Sell everything else **except** the items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}\n'
        f'{emojis.BP} Don\'t forget to sell your armor and sword!'
    )
    prep_tt5_to_9 = (
        f'{emojis.BP} If your horse is T6+: Get 150m coins\n'
        f'{emojis.BP} If your horse is <T6: Get 350m coins\n'
        f'{emojis.BP} If you need money: Do boosted minibosses, use {strings.SLASH_COMMANDS_EPIC_RPG["dynamite"]} and '
        f'sell mob drops\n'
        f'{emojis.BP} If you need money and are impatient: sell {emojis.APPLE} apples\n'
        f'{emojis.BP} Level up professions if not done (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.BP} If you have materials left: Trade to {emojis.APPLE} apples and sell\n'
        f'{emojis.BP} Sell everything else **except** the items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}\n'
        f'{emojis.BP} Don\'t forget to sell your armor and sword!'
    )
    prep_tt10_to_24 = (
        f'{emojis.BP} If your horse is T6+: Get 350m coins\n'
        f'{emojis.BP} If your horse is <T6: Get 850m coins\n'
        f'{emojis.BP} If you need money: Do boosted minibosses, use {strings.SLASH_COMMANDS_EPIC_RPG["dynamite"]} and '
        f'sell mob drops\n'
        f'{emojis.BP} If you need money and are impatient: sell {emojis.APPLE} apples\n'
        f'{emojis.BP} Level up professions if not done (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.BP} If you have materials left: Trade to {emojis.APPLE} apples and sell\n'
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
        f'{emojis.BP} If you need money and are impatient: sell {emojis.APPLE} apples\n'
        f'{emojis.BP} Level up professions if not done (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.BP} If you have materials left: Trade to {emojis.APPLE} apples and sell\n'
        f'{emojis.BP} Sell everything else **except** the items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}\n'
        f'{emojis.BP} Don\'t forget to sell your armor and sword!\n'
        f'{emojis.BP} Tip: Claim the {emojis.BADGE_AREA15} area 15 badge if you haven\'t yet '
        f'({strings.SLASH_COMMANDS_EPIC_RPG["badge claim"]} `id: 10`)\n'
    )
    prep_stt = (
        f'{emojis.BP} Get 850m coins\n'
        f'{emojis.BP} Level up professions if not done (see {strings.SLASH_COMMANDS_GUIDE["professions guide"]})\n'
        f'{emojis.BP} If you need a higher score: Trade to {emojis.RUBY} rubies\n'
        f'{emojis.BP} If you have materials left: Trade to {emojis.APPLE} apples and sell\n'
        f'{emojis.BP} Sell everything you don\'t need for your desired score\n'
        f'{emojis.BP} Do not sell items listed in {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'TIME TRAVEL {tt.tt} BONUSES',
        description = embed_description
    )
    embed.add_field(name='UNLOCKS & BONUSES', value=unlocks, inline=False)
    embed.add_field(name='WORK COMMAND YIELD', value=work_multiplier, inline=False)
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
        title = 'TIME JUMP',
        description = (
            f'Time jumping is unlocked once you reach {emojis.TIME_TRAVEL} TT 25. From this point onward you have '
            f'to use {strings.SLASH_COMMANDS_EPIC_RPG["time jump"]} to reach the next TT.\n'
            f'Time jump lets you choose a starter bonus. You can (and have to) choose **1** bonus.\n'
            f'These bonuses cost score points which are calculated based on your inventory and your gear '
            f'(see topic `Time jump score`).\n'
            f'Note: Time jump used to be called and is also known as **super time travel**.\n'
        )

    )
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='STARTER BONUSES', value=starter_bonuses, inline=False)
    return embed


async def embed_time_jump_score() -> discord.Embed:
    """STT score embed"""
    base = (
        f'{emojis.BP} If you are level 200, have the ULTRA-OMEGA set and your inventory is empty, you have 355.5 score'
    )
    gear = (
        f'{emojis.BP} {emojis.SWORD_ULTRAOMEGA} ULTRA-OMEGA sword = ~74 score\n'
        f'{emojis.BP} {emojis.ARMOR_ULTRAOMEGA} ULTRA-OMEGA armor = ~87 score'
    )
    level = (
        f'{emojis.BP} 1 level = 0.5 score\n'
        f'{emojis.BP} 1 {emojis.STAT_DEF} DEF + 1 {emojis.STAT_AT} AT + 5 {emojis.STAT_LIFE} HP = 0.4 score'
    )
    lootboxes = (
        f'{emojis.BP} 1 {emojis.LB_COMMON} common lootbox = 0.05 score\n'
        f'{emojis.BP} 1 {emojis.LB_UNCOMMON} uncommon lootbox = 0.1 score\n'
        f'{emojis.BP} 1 {emojis.LB_RARE} rare lootbox = 0.15 score\n'
        f'{emojis.BP} 1 {emojis.LB_EPIC} EPIC lootbox = 0.2 score\n'
        f'{emojis.BP} 1 {emojis.LB_EDGY} EDGY lootbox = 0.25 score\n'
        f'{emojis.BP} 1 {emojis.LB_OMEGA} OMEGA lootbox = 2.5 score\n'
        f'{emojis.BP} 1 {emojis.LB_GODLY} GODLY lootbox = 25 score'
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
    farming = (
        f'{emojis.BP} 35 {emojis.POTATO} potatoes = 1 score\n'
        f'{emojis.BP} 30 {emojis.CARROT} carrots = 1 score\n'
        f'{emojis.BP} 25 {emojis.BREAD} bread = 1 score (best value)\n'
        f'{emojis.BP} 1 {emojis.SEED_POTATO} potato seed = 1 score\n'
        f'{emojis.BP} 1 {emojis.SEED_CARROT} carrot seed = 1 score\n'
        f'{emojis.BP} 1 {emojis.SEED_BREAD} bread seed = 1 score\n'
        f'{emojis.BP} 2,500 {emojis.SEED} seed = 1 score (10k seeds max)\n'
    )
    mobdrops = (
        f'{emojis.BP} 20 {emojis.WOLF_SKIN} wolf skins = 1 score\n'
        f'{emojis.BP} 20 {emojis.ZOMBIE_EYE} zombie eyes = 2 score\n'
        f'{emojis.BP} 20 {emojis.UNICORN_HORN} unicorn horns = 3 score\n'
        f'{emojis.BP} 20 {emojis.MERMAID_HAIR} mermaid hairs = 4 score\n'
        f'{emojis.BP} 20 {emojis.CHIP} chips = 5 score\n'
        f'{emojis.BP} 2 {emojis.DRAGON_SCALE} dragon scales = 1 score\n'
        f'{emojis.BP} 1 {emojis.DARK_ENERGY} dark energy = 1 score\n'
    )
    enchants = (
        f'{emojis.BP} OMEGA = 1 score\n'
        f'{emojis.BP} ULTRA-OMEGA = 2 score\n'
        f'{emojis.BP} GODLY = 4 score\n'
        f'{emojis.BP} VOID = ? score\n'
    )
    misc = (
        f'{emojis.BP} Having at least 1 {emojis.LIFE_POTION} life potion = 1 score\n'
        f'{emojis.BP} 500,000 {emojis.LIFE_POTION} life potions = 1 score (1m potions max)\n'
        f'{emojis.BP} 2 {emojis.LOTTERY_TICKET} lottery tickets = 1 score (10 tickets max)\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TIME JUMP SCORE',
        description = (
            f'The score points for the starter bonuses of time jump are calculated based on your level, '
            f'inventory and your gear.\n'
            f'You can calculate the score of your inventory with {strings.SLASH_COMMANDS_GUIDE["time jump calculator"]}.'
        )
    )
    embed.add_field(name='BASE SCORE', value=base, inline=False)
    embed.add_field(name='LEVEL & STATS', value=level, inline=False)
    embed.add_field(name='GEAR', value=gear, inline=False)
    embed.add_field(name='ENCHANTS', value=enchants, inline=False)
    embed.add_field(name='LOOTBOXES', value=lootboxes, inline=False)
    embed.add_field(name='RUBIES', value=rubies, inline=False)
    embed.add_field(name='LOGS', value=logs, inline=False)
    embed.add_field(name='FISH', value=fish, inline=False)
    embed.add_field(name='FRUIT', value=fruit, inline=False)
    embed.add_field(name='FARM ITEMS', value=farming, inline=False)
    embed.add_field(name='MOB DROPS', value=mobdrops, inline=False)
    embed.add_field(name='OTHER ITEMS', value=misc, inline=False)
    return embed


async def embed_tj_score_calculator(area_no: int, inventory: str, trade_materials: bool) -> discord.Embed:
    """STT score calculator embed"""
    message_area = 'The TOP' if area_no == 21 else f'area {area_no}'
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
    score_lbrare = lbrare * 0.15
    score_lbepic = lbepic * 0.2
    score_lbedgy = lbedgy * 0.25
    score_lbomega = lbomega * 2.5
    score_lbgodly = lbgodly * 25
    score_lootboxes = (
        score_lbcommon + score_lbuncommon + score_lbrare + score_lbepic + score_lbedgy + score_lbomega + score_lbgodly
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
    score_total_lootboxes_farm_items = floor(score_lootboxes + score_farm_items)
    score_wolfskin = wolfskin / 20
    score_zombieeye = zombieeye / 10
    score_unicornhorn = unicornhorn / (20 / 3)
    score_mermaidhair = mermaidhair / 5
    score_chip = chip / 4
    score_dragonscale = dragonscale / 2
    score_darkenergy = darkenergy
    score_total_mobdrops = floor(
        score_wolfskin + score_zombieeye + score_unicornhorn + score_mermaidhair + score_chip + score_dragonscale
        + score_darkenergy
    )
    score_logultimate = logultimate * 40
    score_fishsuper = fishsuper * 8
    score_watermelon = watermelon / 12
    score_lifepotion = ceil(lifepotion / 500_000)
    score_lottery = ceil(lottery_ticket / 2)
    score_total_other = score_lottery + score_lifepotion

    field_lootboxes = (
        f'{emojis.BP} {lbcommon:,} {emojis.LB_COMMON} = {score_lbcommon:,.2f}\n'
        f'{emojis.BP} {lbuncommon:,} {emojis.LB_UNCOMMON} = {score_lbuncommon:,.2f}\n'
        f'{emojis.BP} {lbrare:,} {emojis.LB_RARE} = {score_lbrare:,.2f}\n'
        f'{emojis.BP} {lbepic:,} {emojis.LB_EPIC} = {score_lbepic:,.2f}\n'
        f'{emojis.BP} {lbedgy:,} {emojis.LB_EDGY} = {score_lbedgy:,.2f}\n'
        f'{emojis.BP} {lbomega:,} {emojis.LB_OMEGA} = {score_lbomega:,.2f}\n'
        f'{emojis.BP} {lbgodly:,} {emojis.LB_GODLY} = {score_lbgodly:,.2f}\n'
    )
    field_mobdrops = (
        f'{emojis.BP} {wolfskin:,} {emojis.WOLF_SKIN} = {score_wolfskin:,.2f}\n'
        f'{emojis.BP} {zombieeye:,} {emojis.ZOMBIE_EYE} = {score_zombieeye:,.2f}\n'
        f'{emojis.BP} {unicornhorn:,} {emojis.UNICORN_HORN} = {score_unicornhorn:,.2f}\n'
        f'{emojis.BP} {mermaidhair:,} {emojis.MERMAID_HAIR} = {score_mermaidhair:,.2f}\n'
        f'{emojis.BP} {chip:,} {emojis.CHIP} = {score_chip:,.2f}\n'
        f'{emojis.BP} {dragonscale:,} {emojis.DRAGON_SCALE} = {score_dragonscale:,.2f}\n'
        f'{emojis.BP} {darkenergy:,} {emojis.DARK_ENERGY} = {score_darkenergy:,.2f}\n'
    )
    field_farming = (
        f'{emojis.BP} {bread:,} {emojis.BREAD} = {score_bread:,.2f}\n'
        f'{emojis.BP} {carrot:,} {emojis.CARROT} = {score_carrot:,.2f}\n'
        f'{emojis.BP} {potato:,} {emojis.POTATO} = {score_potato:,.2f}\n'
        f'{emojis.BP} {seed:,} {emojis.SEED} = {score_seed:,.2f}\n'
        f'{emojis.BP} {seed_bread:,} {emojis.SEED_BREAD} = {score_seed_bread:,.2f}\n'
        f'{emojis.BP} {seed_carrot:,} {emojis.SEED_CARROT} = {score_seed_carrot:,.2f}\n'
        f'{emojis.BP} {seed_potato:,} {emojis.SEED_POTATO} = {score_seed_potato:,.2f}\n'
    )
    embed = discord.Embed(
        color=settings.EMBED_COLOR,
        title='TIME JUMP SCORE CALCULATOR',
    )
    embed.add_field(name='LOOTBOXES', value=field_lootboxes, inline=True)
    embed.add_field(name='FARM ITEMS', value=field_farming, inline=True)
    embed.add_field(name='MOB DROPS', value=field_mobdrops, inline=True)

    if trade_materials:
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

        score_ruby_a15 = ruby_a15 / 25
        score_ruby_a16 = ruby_a16 / 25
        score_total_materials_a15 = floor(score_ruby_a15 + score_logultimate + score_fishsuper + score_watermelon)
        score_total_materials_a16 = floor(score_ruby_a16 + score_logultimate + score_fishsuper + score_watermelon)
        score_total_a15 = score_total_lootboxes_farm_items + score_total_mobdrops + score_total_other + score_total_materials_a15
        score_total_a16 = score_total_lootboxes_farm_items + score_total_mobdrops + score_total_other + score_total_materials_a16
        ruby_a15_str = f'{ruby_a15:,}' if ruby_a15 != 0 else 'N/A'
        field_materials = (
            f'{emojis.BP} {ruby_a15_str} {emojis.RUBY} in A15 = {score_ruby_a15:,.2f}\n'
            f'{emojis.BP} {ruby_a16:,} {emojis.RUBY} in A16+ = {score_ruby_a16:,.2f}\n'
            f'{emojis.BP} {logultimate:,} {emojis.LOG_ULTIMATE} = {score_logultimate:,.2f}\n'
            f'{emojis.BP} {fishsuper:,} {emojis.FISH_SUPER} = {score_fishsuper:,.2f}\n'
            f'{emojis.BP} {watermelon:,} {emojis.WATERMELON} = {score_watermelon:,.2f}\n'
        )
        field_other = (
            f'{emojis.BP} {lifepotion:,} {emojis.LIFE_POTION} = {score_lifepotion:,.2f}\n'
            f'{emojis.BP} {lottery_ticket} {emojis.LOTTERY_TICKET} = {score_lottery:,.2f}\n'
        )
        score_total_a15_str = score_total_a15 if ruby_a15 != 0 else 'N/A'
        field_totals = (
            f'{emojis.BP} Lootboxes & farm items: **{score_total_lootboxes_farm_items}**\n'
            f'{emojis.BP} Mob drops: **{score_total_mobdrops}**\n'
            f'{emojis.BP} Other: **{score_total_other}**\n'
            f'{emojis.BP} Materials area 15: **{score_total_materials_a15}**\n'
            f'{emojis.BP} Materials areas 16+: **{score_total_materials_a16}**\n'
            f'{emojis.BP} Overall area 15: **{score_total_a15_str}**\n'
            f'{emojis.BP} Overall areas 16+: **{score_total_a16}**\n'
        )
        notes = (
            f'{emojis.BP} This calculation assumes that you trade **all** of your materials to rubies\n'
            f'{emojis.BP} This calculation calculates from your current area up to areas 15+\n'
            f'{emojis.BP} Gear, levels and stats are not included, this is only your inventory\n'
            f'{emojis.BP} Materials you may still need for crafting gear are not subtracted\n'
        )
        embed.description = (
            f'Your current area: **{message_area.capitalize()}**\n'
            f'Total score area 15: **{score_total_a15_str}**\n'
            f'Total score areas 16+: **{score_total_a16}**\n'
        )
        embed.add_field(name='MATERIALS', value=field_materials, inline=True)
        embed.add_field(name='OTHER', value=field_other, inline=True)
        embed.add_field(name='TOTALS', value=field_totals, inline=False)
        embed.add_field(name='NOTES', value=notes, inline=False)


    if not trade_materials:
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
        score_total_materials = floor(score_total_materials_1 + score_total_materials_2)
        score_total_other = score_lifepotion + score_lottery
        score_total = (
            score_total_lootboxes_farm_items + score_total_mobdrops + score_total_materials + score_total_other
        )

        field_materials_1 = (
            f'{emojis.BP} {log:,} {emojis.LOG} = {score_log:,.2f}\n'
            f'{emojis.BP} {logepic:,} {emojis.LOG_EPIC} = {score_logepic:,.2f}\n'
            f'{emojis.BP} {logsuper:,} {emojis.LOG_SUPER} = {score_logsuper:,.2f}\n'
            f'{emojis.BP} {logmega:,} {emojis.LOG_MEGA} = {score_logmega:,.2f}\n'
            f'{emojis.BP} {loghyper:,} {emojis.LOG_ULTIMATE} = {score_logultimate:,.2f}\n'
            f'{emojis.BP} {logultimate:,} {emojis.LOG_ULTIMATE} = {score_logultimate:,.2f}\n'
            f'{emojis.BP} {logultimate:,} {emojis.LOG_ULTIMATE} = {score_logultimate:,.2f}\n'
            f'{emojis.BP} {ruby:,} {emojis.RUBY} = {score_ruby:,.2f}\n'
        )
        field_materials_2 = (
            f'{emojis.BP} {fish:,} {emojis.FISH} = {score_fish:,.2f}\n'
            f'{emojis.BP} {fishgolden:,} {emojis.FISH_GOLDEN} = {score_fishgolden:,.2f}\n'
            f'{emojis.BP} {fishepic:,} {emojis.FISH_EPIC} = {score_fishepic:,.2f}\n'
            f'{emojis.BP} {fishsuper:,} {emojis.FISH_SUPER} = {score_fishsuper:,.2f}\n'
            f'{emojis.BP} {apple:,} {emojis.APPLE} = {score_apple:,.2f}\n'
            f'{emojis.BP} {banana:,} {emojis.BANANA} = {score_banana:,.2f}\n'
            f'{emojis.BP} {watermelon:,} {emojis.WATERMELON} = {score_watermelon:,.2f}\n'
        )
        field_other = (
            f'{emojis.BP} {lifepotion:,} {emojis.LIFE_POTION} = {score_lifepotion:,.2f}\n'
            f'{emojis.BP} {lottery_ticket} {emojis.LOTTERY_TICKET} = {score_lottery:,.2f}\n'
        )
        field_totals = (
            f'{emojis.BP} Lootboxes & farm items: **{score_total_lootboxes_farm_items}**\n'
            f'{emojis.BP} Mob drops: **{score_total_mobdrops}**\n'
            f'{emojis.BP} Other: **{score_total_other}**\n'
            f'{emojis.BP} Materials: **{score_total_materials}**\n'
            f'{emojis.BP} Overall: **{score_total}**\n'
        )
        notes = (
            f'{emojis.BP} This calculation shows your inventory value for your current area\n'
            f'{emojis.BP} Gear, levels and stats are not included, this is only your inventory\n'
            f'{emojis.BP} Materials you may still need for crafting gear are not subtracted\n'
        )
        embed.description = (
            f'Your current area: **{message_area.capitalize()}**\n'
            f'Total score: **{score_total}**\n'
        )
        embed.add_field(name='MATERIALS (I)', value=field_materials_1, inline=True)
        embed.add_field(name='MATERIALS (II)', value=field_materials_2, inline=True)
        embed.add_field(name='OTHER', value=field_other, inline=True)
        embed.add_field(name='TOTALS', value=field_totals, inline=False)
        embed.add_field(name='NOTES', value=notes, inline=False)

    return embed