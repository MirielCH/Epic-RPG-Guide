# professions.py

import asyncio
from math import ceil
from typing import Optional

import discord

import database
from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_ASCENSION = 'Ascension'
TOPIC_CRAFTER = 'Crafter'
TOPIC_ENCHANTER = 'Enchanter'
TOPIC_LEVELING = 'How to level professions'
TOPIC_LOOTBOXER = 'Lootboxer'
TOPIC_MERCHANT = 'Merchant'
TOPIC_OVERVIEW = 'Overview'
TOPIC_WORKER = 'Worker'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_ASCENSION,
    TOPIC_LEVELING,
    TOPIC_CRAFTER,
    TOPIC_ENCHANTER,
    TOPIC_LOOTBOXER,
    TOPIC_MERCHANT,
    TOPIC_WORKER,
]


FOOD_EMOJIS = {
    'enchanter': emojis.FOOD_FRUIT_ICE_CREAM,
    'lootboxer': emojis.FOOD_FILLED_LOOTBOX,
    'worker': emojis.FOOD_BANANA_PICKAXE,
}

FOOD_NAMES = {
    'enchanter': 'fruit ice cream',
    'lootboxer': 'filled lootbox',
    'worker': 'banana pickaxe',
}


# --- Commands ---
async def command_professions_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Profession guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_professions_overview,
        TOPIC_ASCENSION: embed_ascension,
        TOPIC_LEVELING: embed_professions_leveling,
        TOPIC_CRAFTER: embed_professions_crafter,
        TOPIC_ENCHANTER: embed_professions_enchanter,
        TOPIC_LOOTBOXER: embed_professions_lootboxer,
        TOPIC_MERCHANT: embed_professions_merchant,
        TOPIC_WORKER: embed_professions_worker,
    }
    view = views.TopicView(ctx, topics_functions, active_topic=topic)
    embed = await topics_functions[topic]()
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    await functions.edit_interaction(interaction, view=None)


async def command_professions_calculator(
    bot: discord.Bot,
    ctx: discord.ApplicationContext,
    profession: Optional[str] = None,
    from_level: Optional[int] = None,
    to_level: Optional[int] = None
) -> None:
    """Profession calculator command"""
    current_xp = 0
    needed_xp = None
    from_level_defined = False if from_level is None else True
    if profession is None or from_level is None:
        command = f'/professions {profession}' if profession is not None else '/professions [profession]'
        bot_message_task = asyncio.ensure_future(functions.wait_for_profession_message(bot, ctx))
        try:
            content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name, emoji=emojis.EPIC_RPG_LOGO_SMALL,
                                                              command=command)
            bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
        except asyncio.TimeoutError:
            await ctx.respond(
                strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='profession'),
                ephemeral=True
            )
            return
        if bot_message is None: return
        profession_found, level_found, current_xp, needed_xp = (
            await functions.extract_data_from_profession_embed(ctx, bot_message)
        )
        if profession is not None and profession_found != profession:
            await ctx.respond(
                f'Wrong profession data found. You asked for a {profession} calculation but showed me the '
                f'{profession_found} message.',
                ephemeral=True
            )
            return
        if profession is None: profession = profession_found
        if from_level is None: from_level = level_found
    profession_data: database.Profession = await database.get_profession(profession)
    if to_level is not None:
        if from_level >= to_level:
            await ctx.respond(
                f'Calculating from level {from_level} to level {to_level} is not really a thing :thinking:\n'
                f'The level you want to calculate **to** has to be higher than the level you calculate **from**.',
                ephemeral=True
            )
            return
    if profession_data.xp[from_level+1] is None and from_level_defined:
        await ctx.respond(f'No data found for {profession} level {from_level+1}, sorry.')
        return
    try:
        embed = await asyncio.wait_for(embed_professions_calculator(profession_data, to_level, current_xp,
                                                                    from_level_defined, needed_xp, from_level),
                                        timeout=3.0)
    except asyncio.TimeoutError:
        await ctx.respond('Welp, something took too long here, calculation cancelled.', ephemeral=True)
        return
    if profession in ('enchanter', 'lootboxer', 'worker'):
        view = views.FollowupCraftingCalculatorView(ctx, FOOD_NAMES[profession], FOOD_EMOJIS[profession],
                                                    'Crafting calculator')
        interaction = await ctx.respond(embed=embed, view=view)
        view.interaction = interaction
        await view.wait()
        if view.value == 'triggered': await functions.edit_interaction(interaction, view=None)
    else:
        await ctx.respond(embed=embed)


# --- Embeds ---
async def embed_professions_overview() -> discord.Embed:
    """Professions overview"""
    worker = (
        f'{emojis.BP} Increases the chance to get better items with work commands\n'
        f'{emojis.BP} Level 101+: Adds a chance to find other items with work commands\n'
        f'{emojis.BP} For more details see topic `Worker`'
    )
    crafter = (
        f'{emojis.BP} Increases the chance to get 10% materials back when crafting\n'
        f'{emojis.BP} Level 101+: Increases the percentage of items returned\n'
        f'{emojis.BP} For more details see topic `Crafter`'
    )
    lootboxer = (
        f'{emojis.BP} Increases the bank XP bonus\n'
        f'{emojis.BP} Decreases the cost of horse training\n'
        f'{emojis.BP} Level 101+: Increases the maximum level of your horse\n'
        f'{emojis.BP} For more details see topic `Lootboxer`'
    )
    merchant = (
        f'{emojis.BP} Increases the amount of coins you get when selling items\n'
        f'{emojis.BP} Level 101+: You get {emojis.DRAGON_SCALE} dragon scales when selling mob drops\n'
        f'{emojis.BP} For more details see topic `Merchant`'
    )
    enchanter = (
        f'{emojis.BP} Increases the chance to get a better enchant when enchanting\n'\
        f'{emojis.BP} Level 101+: Adds a chance to win the price of the enchant instead of spending it\n'
        f'{emojis.BP} For more details see topic `Enchanter`'
    )
    calculator = (
        f'{emojis.BP} Use {emojis.LOGO}`/professions calculator` to calculate what you need to level up'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'PROFESSIONS',
        description = (
            f'There are 5 professions you can increase to get increasing bonuses.\n'
            f'Each profession has a bonus that caps at level 100. You can level further but it will take much longer and the bonuses for levels 101+ are different.\n'
            f'If you get all professions to level 100, you can ascend (see topic `Ascension`).'
        )
    )
    embed.add_field(name=f'WORKER {emojis.PR_WORKER}', value=worker, inline=False)
    embed.add_field(name=f'CRAFTER {emojis.PR_CRAFTER}', value=crafter, inline=False)
    embed.add_field(name=f'LOOTBOXER {emojis.PR_LOOTBOXER}', value=lootboxer, inline=False)
    embed.add_field(name=f'MERCHANT {emojis.PR_MERCHANT}', value=merchant, inline=False)
    embed.add_field(name=f'ENCHANTER {emojis.PR_ENCHANTER}', value=enchanter, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_professions_leveling() -> discord.Embed:
    """Professions leveling guide"""
    crafter = (
        f'{emojis.BP} This is the first profession you should level up\n'
        f'{emojis.BP} Level **before time traveling** with leftover materials\n'
        f'{emojis.BP} Trade everything to {emojis.LOG} logs and craft/dismantle {emojis.LOG_EPIC} EPIC logs\n'
        f'{emojis.BP} Craft in batches of 500 or 1000 (you can dismantle all at once)\n'
        f'{emojis.BP} Once you reach level 100, switch to leveling merchant'
    )
    merchant = (
        f'{emojis.BP} This is the second profession you should level up\n'
        f'{emojis.BP} Level **before time traveling** with leftover materials\n'
        f'{emojis.BP} Trade everything except {emojis.LOG_ULTRA} ULTRA logs to {emojis.LOG} logs\n'
        f'{emojis.BP} Sell {emojis.LOG_ULTRA} ULTRA logs\n'
        f'{emojis.BP} For each remaining level look up {emojis.EPIC_RPG_LOGO_SMALL}`/professions merchant` and '
        f'calculate the XP you need for the next level\n'
        f'{emojis.BP} Take 5x the XP amount and sell as many {emojis.LOG} logs\n'
        f'{emojis.BP} Once you reach level 100, focus on lootboxer and worker'
    )
    lootboxer = (
        f'{emojis.BP} Level up by opening lootboxes\n'
        f'{emojis.BP} Better lootboxes give more XP (see topic `Lootboxer`)\n'
        f'{emojis.BP} If lower than worker, consider cooking {emojis.FOOD_FILLED_LOOTBOX} filled lootboxes\n'
        f'{emojis.BP} It\'s usually not necessary to cook {emojis.FOOD_FILLED_LOOTBOX} filled lootboxes\n'
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/hunt mode: hardmode` whenever you have access (unlocks in A13)'
    )
    worker = (
        f'{emojis.BP} Level up by using work commands or cooking {emojis.FOOD_BANANA_PICKAXE} banana pickaxes\n'
        f'{emojis.BP} Higher tier work commands give more XP (see topic `Worker`)\n'
        f'{emojis.BP} Try to keep the level at about the same as lootboxer\n'
        f'{emojis.BP} If lower than lootboxer, consider cooking {emojis.FOOD_BANANA_PICKAXE} banana pickaxes\n'
    )
    enchanter = (
        f'{emojis.BP} This is the last profession you should level up (it\'s expensive and you need access to at least '
        f'{emojis.EPIC_RPG_LOGO_SMALL}`/transmute`)\n'
        f'{emojis.BP} Level before time traveling using {emojis.EPIC_RPG_LOGO_SMALL}`/transmute` or '
        f'{emojis.EPIC_RPG_LOGO_SMALL}`/transcend`\n'
        f'{emojis.BP} XP gain is based on the quality of the enchant you get (see topic `Enchanter`)\n'
        f'{emojis.BP} Costs around 3 billion coins without {emojis.HORSE_T8} T8+ horse\n'
        f'{emojis.BP} Costs around 2 billion coins with {emojis.HORSE_T8} T8+ horse'
    )
    ascended = (
        f'{emojis.BP} Increase crafter and merchant to 101, then focus exclusively on worker\n'
    )
    calculator = (
        f'{emojis.BP} Use {emojis.LOGO}`/professions calculator` to calculate what you need to level up'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HOW TO LEVEL PROFESSIONS',
        description = (
            f'This guide shows you how to level up professions to reach ascension (level 100).\n'
            f'Do not overfarm to get ascended as early as possible. It wastes a lot of time you could spend time '
            f'traveling. TT give high bonuses and ascension makes more sense if you already have access to all commands '
            f'up to area 15.\n'
            f'Thus, unless you can reach ascension easily, always time travel again instead of staying and farming.'
        )
    )
    embed.add_field(name=f'1. CRAFTER {emojis.PR_CRAFTER}', value=crafter, inline=False)
    embed.add_field(name=f'2. MERCHANT {emojis.PR_MERCHANT}', value=merchant, inline=False)
    embed.add_field(name=f'3. WORKER {emojis.PR_WORKER}', value=worker, inline=False)
    embed.add_field(name=f'4. LOOTBOXER {emojis.PR_LOOTBOXER}', value=lootboxer, inline=False)
    embed.add_field(name=f'5. ENCHANTER {emojis.PR_ENCHANTER}', value=enchanter, inline=False)
    embed.add_field(name='AFTER ASCENSION', value=ascended, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_professions_crafter() -> discord.Embed:
    """Crafter guide"""
    base_bonus = (
        f'{emojis.BP} Increases the chance to get 10% materials back when crafting\n'
        f'{emojis.BP} The chance at level 100 is 80%'
    )
    level_101 =(
        f'{emojis.BP} Increases the percentage of items returned\n'
        f'{emojis.BP} The percentage increases logarithmically'
    )
    how_to_get_xp = (
        f'{emojis.BP} Craft and dismantle\n'
        f'{emojis.BP} ~~Cook {emojis.FOOD_HEAVY_APPLE} heavy apples (100 XP each)~~ (don\'t do that)'
    )
    xp_gain = (
        f'{emojis.BP} A detailed list of all material and gear XP is available in the '
        f'[Wiki](https://epic-rpg.fandom.com/wiki/Professions#Crafter)'
    )
    calculator = (
        f'{emojis.BP} Use {emojis.LOGO}`/professions calculator` to calculate what you need to level up'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CRAFTER PROFESSION'
    )
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_professions_enchanter() -> discord.Embed:
    """Enchanter guide"""
    base_bonus = (
        f'{emojis.BP} Increases the chance to get a better enchant when enchanting\n'
        f'{emojis.BP} The exact chance increase is unknown'
    )
    level_101 =(
        f'{emojis.BP} Adds a chance to win the price of the enchant instead of spending it\n'
        f'{emojis.BP} The chance is 2% at level 101 and increases logarithmically with each level'
    )
    how_to_get_xp = (
        f'{emojis.BP} Use enchanting commands\n'
        f'{emojis.BLANK} The XP formula is [tt multiplier] * [command multiplier] * [enchantment xp]\n'
        f'{emojis.BLANK} Ex: If you enchant **Perfect** with {emojis.EPIC_RPG_LOGO_SMALL}`/transmute` in TT6, '
        f'you get `2 * 100 * 7` XP\n'
        f'{emojis.BP} ~~Cook {emojis.FOOD_FRUIT_ICE_CREAM} fruit ice cream (100 XP each)~~ (don\'t do that)'
    )
    xp_gain = (
        f'{emojis.BP} **Normie**: 0 XP\n'
        f'{emojis.BP} **Good**: 1 XP\n'
        f'{emojis.BP} **Great**: 2 XP\n'
        f'{emojis.BP} **Mega**: 3 XP\n'
        f'{emojis.BP} **Epic**: 4 XP\n'
        f'{emojis.BP} **Hyper**: 5 XP\n'
        f'{emojis.BP} **Ultimate**: 6 XP\n'
        f'{emojis.BP} **Perfect**: 7 XP\n'
        f'{emojis.BP} **EDGY**: 8 XP\n'
        f'{emojis.BP} **ULTRA-EDGY**: 9 XP\n'
        f'{emojis.BP} **OMEGA**: 10 XP\n'
        f'{emojis.BP} **ULTRA-OMEGA**: 11 XP\n'
        f'{emojis.BP} **GODLY**: 12 XP\n'
        f'{emojis.BP} **VOID**: 13 XP\n'
    )
    command_multipliers = (
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/enchant`: 1\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/refine`: 10\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/transmute`: 100\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/transcend`: 1,000'
    )
    tt_multiplier = (
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/time travel` to check your TT multiplier'
    )
    calculator = (
        f'{emojis.BP} Use {emojis.LOGO}`/professions calculator` to calculate what you need to level up'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ENCHANTER PROFESSION'
    )
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='COMMAND MULTIPLIERS', value=command_multipliers, inline=False)
    embed.add_field(name='TT MULTIPLIER', value=tt_multiplier, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_professions_lootboxer() -> discord.Embed:
    """Lootboxer guide"""
    base_bonus = (
        f'{emojis.BP} Increases the bank XP bonus\n'
        f'{emojis.BP} Decreases the cost of horse training\n'
        f'{emojis.BP} Horse training is 50 % cheaper at level 100\n'\
        f'{emojis.BP} The exact buff of the bank bonus unknown'
    )
    level_101 =(
        f'{emojis.BP} Increases the maximum level of your horse\n'
        f'{emojis.BP} The level increases by 1 per level after 100'
    )
    how_to_get_xp = (
        f'{emojis.BP} Open lootboxes\n'
        f'{emojis.BP} ~~Cook {emojis.FOOD_FILLED_LOOTBOX} filled lootboxes (100 XP each)~~ (don\'t do that)\n'
    )
    xp_gain = (
        f'{emojis.BP} {emojis.LB_COMMON} common lootbox: 4 XP\n'
        f'{emojis.BP} {emojis.LB_UNCOMMON} uncommon lootbox: 9 XP\n'
        f'{emojis.BP} {emojis.LB_RARE} rare lootbox: 17 XP\n'
        f'{emojis.BP} {emojis.LB_EPIC} EPIC lootbox: 30 XP\n'
        f'{emojis.BP} {emojis.LB_EDGY} EDGY lootbox: 65 XP\n'
        f'{emojis.BP} {emojis.LB_OMEGA} OMEGA lootbox: 800 XP\n'
        f'{emojis.BP} {emojis.LB_GODLY} GODLY lootbox: 15004 XP\n'
        f'{emojis.BP} {emojis.LB_VOID} VOID lootbox: Unknown\n'
    )
    calculator = (
        f'{emojis.BP} Use {emojis.LOGO}`/professions calculator` to calculate what you need to level up'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LOOTBOXER PROFESSION'
    )
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_professions_merchant() -> discord.Embed:
    """Merchant guide"""
    base_bonus = (
        f'{emojis.BP} Increases the amount of coins you get when selling items\n'
        f'{emojis.BP} You get 4.929395x more coins at level 100'
    )
    level_101 =(
        f'{emojis.BP} You get {emojis.DRAGON_SCALE} dragon scales when selling mob drops\n'
        f'{emojis.BP} You get 1 dragon scale per 50 mob drops at level 101 (2%)\n'
        f'{emojis.BP} This increases by 2% for every level\n'
    )
    how_to_get_xp = (
        f'{emojis.BP} Sell materials\n'
        f'{emojis.BP} Note that you don\'t get any XP when selling gear and other items\n'
        f'{emojis.BP} ~~Cook {emojis.FOOD_COIN_SANDWICH} coin sandwich (100 XP each)~~ (**DON\'T DO THAT**)\n'
    )
    xp_gain = (
        f'{emojis.BP} A detailed list of XP per amount sold is available in the '
        f'[Wiki](https://epic-rpg.fandom.com/wiki/Professions#Merchant)'
    )
    calculator = (
        f'{emojis.BP} Use {emojis.LOGO}`/professions calculator` to calculate what you need to level up'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MERCHANT PROFESSION'
    )
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_professions_worker() -> discord.Embed:
    """Worker guide"""
    base_bonus = (
        f'{emojis.BP} Increases the chance to get a better item with work commands\n'
        f'{emojis.BP} The chance increase is 50% at level 100'
    )
    level_101 =(
        f'{emojis.BP} Adds an increasing chance to find other items with top tier work commands\n'
        f'{emojis.BP} The chance is 4% at level 101 and increases by 4% for every level\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/bigboat` gets a chance to drop {emojis.BANANA} bananas\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/chainsaw` gets a chance to drop {emojis.FISH} normie fish\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/dynamite` gets a chance to drop {emojis.LOG_SUPER} SUPER logs\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/greenhouse` gets a chance to drop {emojis.RUBY} rubies'
    )
    how_to_get_xp = (
        f'{emojis.BP} Use work commands\n'
        f'{emojis.BP} Cook {emojis.FOOD_BANANA_PICKAXE} banana pickaxes (100 XP each)\n'
    )
    xp_gain = (
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/chop`, {emojis.EPIC_RPG_LOGO_SMALL}`/fish`, '
        f'{emojis.EPIC_RPG_LOGO_SMALL}`/pickup`, {emojis.EPIC_RPG_LOGO_SMALL}`/mine`: 4 XP\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/axe`, {emojis.EPIC_RPG_LOGO_SMALL}`/ladder`, '
        f'{emojis.EPIC_RPG_LOGO_SMALL}`/pickaxe`: 8 XP\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/net`: 9 XP\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/bowsaw`, {emojis.EPIC_RPG_LOGO_SMALL}`/tractor`, '
        f'{emojis.EPIC_RPG_LOGO_SMALL}`/drill`: 12 XP\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/boat`: 13 XP\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/chainsaw`: 16 XP\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/greenhouse`, {emojis.EPIC_RPG_LOGO_SMALL}`/dynamite`: 17 XP\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/bigboat`: 18 XP'
    )
    calculator = (
        f'{emojis.BP} Use {emojis.LOGO}`/professions calculator` to calculate what you need to level up'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'WORKER PROFESSION'
    )
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_ascension() -> discord.Embed:
    """Ascension"""
    requirements = (
        f'{emojis.BP} All 5 professions at level 100+ (see topic `How to level professions`)\n'
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 1+'
    )
    benefits =(
        f'{emojis.BP} Get more materials by using high tier work commands early\n'
        f'{emojis.BP} Get more XP by using {emojis.EPIC_RPG_LOGO_SMALL}`/hunt mode: hardmode` and '
        f'{emojis.EPIC_RPG_LOGO_SMALL}`/adventure mode: hardmode` early\n'
        f'{emojis.BP} Get higher enchants easier by using higher enchanting commands early\n'
        f'{emojis.BP} {emojis.RUBY} rubies and {emojis.BANANA} bananas are obtainable in area 1+'
    )
    notes = (
        f'{emojis.BP} Trade rates are still area locked\n'
        f'{emojis.BP} Higher tier logs and fish remain area locked. Use '
        f'{emojis.EPIC_RPG_LOGO_SMALL}`/help topic: [material]` to see the area they unlock in.'
    )
    calculator = (
        f'{emojis.BP} Use {emojis.LOGO}`/professions calculator` to calculate what you need to level up'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ASCENSION',
        description = (
            f'Ascension allows you to use **all** game commands you ever unlocked in **every** area.\n'
            f'This makes it much easier to get XP, materials and high enchants early.'
        )
    )
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='BENEFITS', value=benefits, inline=False)
    embed.add_field(name='NOTES', value=notes, inline=False)
    embed.add_field(name='CALCULATOR', value=calculator, inline=False)
    return embed


async def embed_professions_calculator(profession_data: database.Profession, to_level: int, current_xp: int,
                                       from_level_defined: bool, needed_xp: Optional[int] = None,
                                       from_level: Optional[int] = None) -> discord.Embed:
    """Professions calculator embed"""
    output_total = None
    next_level = from_level + 1
    profession = profession_data.name
    if profession_data.xp[next_level] is None and needed_xp is not None and not from_level_defined:
        await profession_data.update_level(next_level, needed_xp)
    if needed_xp is None: needed_xp = profession_data.xp[next_level]

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'PROFESSIONS CALCULATOR'
    )

    if profession in ('enchanter', 'lootboxer', 'worker'):
        xp = needed_xp - current_xp if not from_level_defined else profession_data.xp[next_level]
        item_total = item_amount = ceil(xp / 100)
        xp_total = xp
        item_total_wb = item_amount_wb = ceil(xp / 110)
        xp_rest = 100 - (xp % 100)
        xp_rest_wb = 110 - (xp % 110)
        if xp_rest == 100:
            xp_rest = 0
        if xp_rest_wb == 110:
            xp_rest_wb = 0

        output = (
            f'{emojis.BP} Level {from_level} to {next_level}: **{item_amount:,}** {FOOD_EMOJIS[profession]} '
            f'(if world buff: **{item_amount_wb:,}**)'
        )

        current_level = next_level
        for x in range(6):
            current_level += 1
            level_xp = profession_data.xp[current_level]
            if level_xp is None:
                output = (
                    f'{output}\n{emojis.BP} Level {current_level}+: No data yet'
                )
                current_level -= 1
                break
            actual_xp = level_xp - xp_rest
            actual_xp_wb = level_xp - xp_rest_wb
            item_amount = ceil(actual_xp / 100)
            item_amount_wb = ceil(actual_xp_wb / 110)
            xp_rest = 100 - (actual_xp % 100)
            xp_rest_wb = 110 - (actual_xp_wb % 110)
            if xp_rest == 100:
                xp_rest = 0
            if xp_rest_wb == 110:
                xp_rest_wb = 0
            output = (
                f'{output}\n{emojis.BP} Level {current_level-1} to {current_level}: '
                f'**{item_amount:,}** {FOOD_EMOJIS[profession]} (if world buff: **{item_amount_wb:,}**)'
            )
        if to_level is None: to_level = current_level
        if from_level < to_level:
            for current_level in range(from_level + 2, to_level + 1):
                level_xp = profession_data.xp[current_level]
                if level_xp is None:
                    output_total = (
                        f'{emojis.BP} Not enough data yet.\n'
                        f'{emojis.BLANK} I currently have data for up to level **{current_level-1}**.'
                    )
                    break
                xp_total += level_xp
                actual_xp = level_xp - xp_rest
                actual_xp_wb = level_xp - xp_rest_wb
                item_amount = ceil(actual_xp / 100)
                item_amount_wb = ceil(actual_xp_wb / 110)
                item_total = item_total + item_amount
                item_total_wb = item_total_wb + item_amount_wb
                xp_rest = 100 - (actual_xp % 100)
                xp_rest_wb = 110 - (actual_xp_wb % 110)
                if xp_rest == 100:
                    xp_rest = 0
                if xp_rest_wb == 110:
                    xp_rest_wb = 0

            if output_total is None:
                output_total = (
                    f'{emojis.BP} **{item_total:,}** {FOOD_EMOJIS[profession]} without world buff\n'
                    f'{emojis.BP} **{item_total_wb:,}** {FOOD_EMOJIS[profession]} with world buff\n'
                    f'{emojis.BP} XP required: **{xp_total:,}**\n'
                )
        if profession == 'enchanter':
            how_to_level = (
                f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/transmute` or {emojis.EPIC_RPG_LOGO_SMALL}`/transcend`\n'
                f'{emojis.BP} It\'s not recommended to cook {FOOD_EMOJIS[profession]} {FOOD_NAMES[profession]}, '
                f'but if you prefer doing so regardless, see the required amounts below'
            )
        else:
            how_to_level = f'{emojis.BP} Cook {FOOD_EMOJIS[profession]} {FOOD_NAMES[profession]}'
        description = f'**{profession.capitalize()}** level **{from_level}**'
        if to_level > from_level:
            description = f'{description} to **{to_level}**'
        embed.description = description
        embed.add_field(name='HOW TO LEVEL', value=how_to_level)
        embed.add_field(name='NEXT LEVELS', value=output, inline=False)
        if output_total is not None:
            embed.add_field(
                name=f'TOTAL {from_level} - {to_level}', value=output_total, inline=False
            )
        return embed

    if profession == 'merchant':
        xp = needed_xp - current_xp if not from_level_defined else profession_data.xp[next_level]
        item_total = item_amount = xp * 5
        xp_total = xp
        item_total_wb = item_amount_wb = 5 * ceil((item_amount / 1.1) / 5)

        output = (
            f'{emojis.BP} Level {from_level} to {next_level}: **{item_amount:,}** {emojis.LOG} '
            f'(if world buff: **{item_amount_wb:,}**)'
        )

        current_level = next_level
        for x in range(6):
            current_level += 1
            level_xp = profession_data.xp[current_level]
            if level_xp is None:
                output = (
                    f'{output}\n{emojis.BP} Level {current_level}+: No data yet'
                )
                current_level -= 1
                break
            item_amount = level_xp * 5
            item_amount_wb = 5 * ceil((item_amount / 1.1) / 5)
            output = (
                f'{output}\n{emojis.BP} Level {current_level-1} to {current_level}: '
                f'**{item_amount:,}** {emojis.LOG} (if world buff: **{item_amount_wb:,}**)'
            )
        if to_level is None: to_level = current_level
        if from_level < to_level:
            for current_level in range(from_level + 2, to_level + 1):
                level_xp = profession_data.xp[current_level]
                if level_xp is None:
                    output_total = (
                        f'{emojis.BP} Not enough data yet.\n'
                        f'{emojis.BLANK} I currently have data for up to level **{current_level-1}**.'
                    )
                    break
                xp_total += level_xp
                item_amount = level_xp * 5
                item_amount_wb = 5 * ceil((item_amount / 1.1) / 5)
                item_total = item_total + item_amount
                item_total_wb = item_total_wb + item_amount_wb

            if output_total is None:
                output_total = (
                    f'{emojis.BP} **{item_total:,}** {emojis.LOG} without world buff\n'
                    f'{emojis.BP} **{item_total_wb:,}** {emojis.LOG} with world buff\n'
                    f'{emojis.BP} XP required: **{xp_total:,}**\n'
                )

        description = f'**{profession.capitalize()}** level **{from_level}**'
        if to_level > from_level:
            description = f'{description} to **{to_level}**'
        embed.description = description
        embed.add_field(name='HOW TO LEVEL', value=f'{emojis.BP} Sell {emojis.LOG} wooden logs')
        embed.add_field(name='NEXT LEVELS', value=output, inline=False)
        if output_total is not None:
            embed.add_field(
                name=f'TOTAL {from_level} - {to_level}', value=output_total, inline=False
            )
        return embed

    if profession == 'crafter':
        returned_percentages = {
            101: 0.12,
            102: 0.1283,
            103: 0.1346,
            104: 0.14,
            105: 0.1447,
            106: 0.149,
            107: 0.1529,
        }
        async def calculate_logs(item_amount: int, returned_percentage: float, level: int) -> int:
            """Calculates how many logs it needs for a certain amount of epic logs"""
            base_log_amount_upper = 100_000_000_000
            base_log_amount_lower = 0
            while True:
                base_log_amount = log_amount = (base_log_amount_lower + base_log_amount_upper) // 2
                epic_log_amount = epic_log_amount_total = xp_totals = 0
                while True:
                    epic_log_amount, log_rest = divmod(log_amount, 25)
                    epic_log_amount_total += epic_log_amount
                    xp_totals += epic_log_amount * 2
                    if level >= 100:
                        returned_amount = functions.round_school(epic_log_amount * 25 * 0.8 * returned_percentage)
                        if returned_amount == 0: returned_amount = 1
                        log_rest += returned_amount
                    log_amount = log_rest + epic_log_amount * 20
                    if log_amount < 25: break
                if (item_amount-1) <= xp_totals <= (item_amount+1):
                    break
                elif xp_totals < item_amount:
                    base_log_amount_lower = base_log_amount - 1
                elif xp_totals > item_amount:
                    base_log_amount_upper = base_log_amount + 1
            return base_log_amount

        xp = needed_xp - current_xp if not from_level_defined else profession_data.xp[next_level]

        how_to_level = (
            f'{emojis.BP} Repeatedly craft & dismantle {emojis.LOG_EPIC} EPIC logs.\n'
            f'{emojis.BP} Due to the chance to get logs back, you should craft in batches.\n'
            f'{emojis.BLANK} The smaller the batches, the lower the overall risk.'
        )

        returned_percentage = returned_percentages[from_level] if from_level > 100 else 0.1
        log_amount = await calculate_logs(xp, returned_percentage, from_level)
        log_amount_total = log_amount
        xp_total = xp
        log_amount_wb = ceil(log_amount / 1.1)
        log_amount_total_wb = log_amount_wb
        output = (
            f'{emojis.BP} Level {from_level} to {next_level}: '
            f'~**{log_amount:,}** {emojis.LOG} (if world buff: ~**{log_amount_wb:,}**)'
        )
        current_level = next_level
        for x in range(6):
            current_level += 1
            level_xp = profession_data.xp[current_level]
            if level_xp is None:
                output = (
                    f'{output}\n{emojis.BP} Level {current_level}+: No data yet'
                )
                current_level -= 1
                break
            returned_percentage = returned_percentages[current_level-1] if current_level-1 > 100 else 0.1
            log_amount = await calculate_logs(level_xp, returned_percentage, current_level-1)
            log_amount_wb = ceil(log_amount / 1.1)
            output = (
                f'{output}\n{emojis.BP} Level {current_level-1} to {current_level}: '
                f'~**{log_amount:,}** {emojis.LOG} (if world buff: ~**{log_amount_wb:,}**)'
            )
            item_amount = level_xp
        if to_level is None: to_level = current_level
        if from_level < to_level:
            for current_level in range(from_level + 2, to_level + 1):
                level_xp = profession_data.xp[current_level]
                if level_xp is None:
                    output_total = (
                        f'{emojis.BP} Not enough data yet.\n'
                        f'{emojis.BLANK} I currently have data for up to level **{current_level-1}**.'
                    )
                    break
                xp_total += level_xp
                returned_percentage = returned_percentages[current_level-1] if current_level-1 > 100 else 0.1
                log_amount = await calculate_logs(level_xp, returned_percentage, current_level-1)
                log_amount_wb = ceil(log_amount / 1.1)
                log_amount_total += log_amount
                log_amount_total_wb += log_amount_wb

            if output_total is None:
                output_total = (
                    f'{emojis.BP} ~**{log_amount_total:,}** {emojis.LOG} without world buff\n'
                    f'{emojis.BP} ~**{log_amount_total_wb:,}** {emojis.LOG} with world buff\n'
                    f'{emojis.BP} XP required: **{xp_total:,}**\n'

                )
        note = (
            f'{emojis.BP} Levels 1-99 assume you get **no** logs back!\n'
            f'{emojis.BP} Levels 100+ include the crafter bonus\n'
        )
        description = f'**{profession.capitalize()}** level **{from_level}**'
        if to_level > from_level:
            description = f'{description} to **{to_level}**'
        embed.description = description
        embed.add_field(name='HOW TO LEVEL', value=how_to_level)
        embed.add_field(name='NEXT LEVELS', value=output, inline=False)
        if output_total is not None:
            embed.add_field(
                name=f'TOTAL {from_level} - {to_level}', value=output_total, inline=False
            )
        embed.add_field(name='NOTE', value=note)
        return embed