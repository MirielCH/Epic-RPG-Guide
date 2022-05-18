# misc.py

import asyncio
from decimal import Decimal, ROUND_HALF_UP
from pyexpat.errors import messages
from typing import Optional

import discord

import database
from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_BEGINNER_FIRST_RUN = 'Your first run'
TOPIC_FARMING_USAGE = 'Crops usage and value'

TOPICS_BEGINNER = [
    TOPIC_OVERVIEW,
    TOPIC_BEGINNER_FIRST_RUN,
]

TOPICS_FARMING = [
    TOPIC_OVERVIEW,
    TOPIC_FARMING_USAGE,
]


# --- Commands ---
async def command_codes(ctx: discord.ApplicationContext) -> None:
    """Codes command"""
    embed = await embed_codes()
    await ctx.respond(embed=embed)


async def command_badges(ctx: discord.ApplicationContext) -> None:
    """Badges command"""
    embed = await embed_badges()
    await ctx.respond(embed=embed)


async def command_coolness_guide(ctx: discord.ApplicationContext) -> None:
    """Coolness command"""
    embed = await embed_coolness_guide()
    await ctx.respond(embed=embed)


async def command_farming_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Farming command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_farming_overview,
        TOPIC_FARMING_USAGE: embed_farming_usage,
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


async def command_beginner_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Beginner guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_beginner_overview,
        TOPIC_BEGINNER_FIRST_RUN: embed_beginner_first_run,
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


async def command_tip(ctx: discord.ApplicationContext, tip_id: Optional[int] = None) -> None:
    """Tip command"""
    try:
        tip: database.Tip = await database.get_tip(tip_id)
    except database.NoDataFound:
        await ctx.respond('There is no tip with that ID yet :cry:', ephemeral=True)
        return
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'TIP #{tip.id}',
        description = tip.tip
    )
    await ctx.respond(embed=embed)


async def command_calculator(ctx: discord.ApplicationContext, calculation: str) -> None:
    """Calculator command"""
    def formatNumber(num):
        if num % 1 == 0:
            return int(num)
        else:
            num = num.quantize(Decimal('1.1234567890'), rounding=ROUND_HALF_UP)
            return num
    calculation = calculation.replace(' ','')
    allowedchars = set('1234567890.-+/*%()')
    if not set(calculation).issubset(allowedchars) or '**' in calculation:
        message = (
            f'Invalid characters. Please only use numbers and supported operators.\n'
            f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
        )
        await ctx.respond(message, ephemeral=True)
        return
    error_parsing = (
        f'Error while parsing your input. Please check your input.\n'
        f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
    )
    # Parse open the calculation, convert all numbers to float and store it as a list
    # This is necessary because Python has the annoying habit of allowing infinite integers which can completely lockup a system. Floats have overflow protection.
    pos = 1
    calculation_parsed = []
    number = ''
    last_char_was_operator = False # Not really accurate name, I only use it to check for *, % and /. Multiple + and - are allowed.
    last_char_was_number = False
    calculation_sliced = calculation
    try:
        while pos != len(calculation) + 1:
            slice = calculation_sliced[0:1]
            allowedcharacters = set('1234567890.-+/*%()')
            if set(slice).issubset(allowedcharacters):
                if slice.isnumeric():
                    if last_char_was_number:
                        number = f'{number}{slice}'
                    else:
                        number = slice
                        last_char_was_number = True
                    last_char_was_operator = False
                else:
                    if slice == '.':
                        if number == '':
                            number = f'0{slice}'
                            last_char_was_number = True
                        else:
                            number = f'{number}{slice}'
                    else:
                        if number != '':
                            calculation_parsed.append(Decimal(float(number)))
                            number = ''

                        if slice in ('*','%','/'):
                            if last_char_was_operator:
                                await ctx.respond(error_parsing, ephemeral=True)
                                return
                            else:
                                calculation_parsed.append(slice)
                                last_char_was_operator = True
                        else:
                            calculation_parsed.append(slice)
                            last_char_was_operator = False
                        last_char_was_number = False
            else:
                await ctx.respond(error_parsing, ephemeral=True)
                return

            calculation_sliced = calculation_sliced[1:]
            pos += 1
        else:
            if number != '':
                calculation_parsed.append(Decimal(float(number)))
    except:
        await ctx.respond(error_parsing, ephemeral=True)
        return

    # Reassemble and execute calculation
    calculation_reassembled = ''
    for slice in calculation_parsed:
        calculation_reassembled = f'{calculation_reassembled}{slice}'
    try:
        #result = eval(calculation_reassembled) # This line seems useless
        result = Decimal(eval(calculation_reassembled))
        result = formatNumber(result)
        if isinstance(result, int):
            result = f'{result:,}'
        else:
            result = f'{result:,}'.rstrip('0').rstrip('.')
        if len(result) > 2000:
            await ctx.respond(
                'Well. Whatever you calculated, the result is too long to display. GG.',
                ephemeral=True
            )
            return
    except:
        await ctx.respond(
            f'Well, _that_ didn\'t calculate to anything useful.\n'
            f'What were you trying to do there? :thinking:',
            ephemeral=True
        )
        return
    await ctx.respond(result)


async def command_coincap_calculator(
    bot: discord.Bot,
    ctx: discord.ApplicationContext,
    timetravel: Optional[int] = None,
    area_no: Optional[int] = None
) -> str:
    """Coincap calculator message"""
    if timetravel is None or area_no is None:
        bot_message_task = asyncio.ensure_future(functions.wait_for_profile_or_progress_message(bot, ctx))
        try:
            content = (
                f'**{ctx.author.name}**, please use {emojis.EPIC_RPG_LOGO_SMALL}`/profile` '
                f'or {emojis.EPIC_RPG_LOGO_SMALL}`/progress`\n'
                f'Note that profile backgrounds are not supported.'
            )
            bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
        except asyncio.TimeoutError:
            await ctx.respond(
                strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='profile'),
                ephemeral=True
            )
            return
        if bot_message is None: return
        tt_found, area_found = await functions.extract_progress_data_from_profile_or_progress_embed(ctx, bot_message)
        if timetravel is None: timetravel = tt_found
        if area_no is None: area_no = area_found
    coin_cap = pow(timetravel, 4) * 500_000_000 + pow(area_no, 2) * 100_000
    if area_no == 1: coin_cap += 1
    area_str = 'the TOP' if area_no == 21 else f'area {area_no}'
    await ctx.respond(
        f'The coin cap for **TT {timetravel}**, **{area_str}** is '
        f'**{coin_cap:,}** {emojis.COIN} coins.\n'
        f'You can not receive coins with {emojis.EPIC_RPG_LOGO_SMALL}`/give`, {emojis.EPIC_RPG_LOGO_SMALL}`/multidice` '
        f'or {emojis.EPIC_RPG_LOGO_SMALL}`/miniboss` if you would exceed this cap.'
    )


# --- Embeds ---
async def embed_codes():
    """Codes"""
    temporary_value = temporary_value_2 = temporary_value_3 = permanent_value = ''
    codes = await database.get_all_codes()
    for code in codes:
        if code.temporary:
            temporary_value_check = f'{temporary_value}\n{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
            temporary_value_2_check = f'{temporary_value_2}\n{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
            if len(temporary_value_2_check) > 1024:
                temporary_value_3 = f'{temporary_value_3}\n{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
            elif len(temporary_value_check) > 1024:
                temporary_value_2 = f'{temporary_value_2}\n{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
            else:
                temporary_value = f'{temporary_value}\n{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
        else:
            permanent_value = f'{permanent_value}\n{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
    if permanent_value == '': permanent_value = f'{emojis.BP} No codes currently known'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'REDEEMABLE CODES',
        description = (
            f'Use these codes with {emojis.EPIC_RPG_LOGO_SMALL}`/code` to get some free goodies.\n'
            f'Every code can only be redeemed once.'
        )
    )
    if not temporary_value == '':
        embed.add_field(name='EVENT CODES', value=temporary_value, inline=False)
    if temporary_value_2 != '':
        embed.add_field(name='MORE EVENT CODES', value=temporary_value_2, inline=False)
    if temporary_value_3 != '':
        embed.add_field(name='EVEN MORE EVENT CODES', value=temporary_value_3, inline=False)
    embed.add_field(name='PERMANENT CODES', value=permanent_value, inline=False)
    return embed


async def embed_badges() -> discord.Embed:
    """Badges"""
    badges_coolness = (
        f'{emojis.BP} {emojis.BADGE_C1} : Unlocked with 1 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C100} : Unlocked with 100 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C200} : Unlocked with 200 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C500} : Unlocked with 500 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C1000} : Unlocked with 1,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C2000} : Unlocked with 2,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C5000} : Unlocked with 5,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C10000} : Unlocked with 10,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C20000} : Unlocked with 20,000 {emojis.STAT_COOLNESS} coolness\n'
    )
    badges_achievements = (
        f'{emojis.BP} {emojis.BADGE_A10} : Unlocked with 10 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A25} : Unlocked with 25 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A75} : Unlocked with 75 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A125} : Unlocked with 125 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A175} : Unlocked with 175 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A225} : Unlocked with 225 achievements\n'
    )
    badges_other = (
        f'{emojis.BP} {emojis.BADGE_AREA15} : Unlocked by reaching area 15 ({emojis.TIME_TRAVEL} TT 10)\n'
        f'{emojis.BP} {emojis.BADGE_TOP} : Unlocked by beating D15-2 and reaching the TOP\n'
        f'{emojis.BP} {emojis.BADGE_EPIC_NPC} : Unlocked by beating the EPIC NPC in the TOP\n'
        f'{emojis.BP} {emojis.BADGE_OMEGA} : Unlock requirements unknown\n'
        f'{emojis.BP} {emojis.BADGE_GODLY} : Unlock requirements unknown\n'
    )
    howtouse = (
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/badge list` to see all badges\n'
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/badge unlocked` to see the badges you unlocked\n'
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/badge claim` to claim a badge\n'
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/badge select` to activate or deactivate a badge'
    )
    note = (
        f'{emojis.BP} You can have 3 badges active (5 with a {emojis.HORSE_T10} T10 horse)\n'
        f'{emojis.BP} You can only claim badges you have unlocked\n'
        f'{emojis.BP} If you don\'t know how to get coolness, see {emojis.LOGO}`/coolness guide`'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'BADGES',
        description = 'Badges are cosmetic only profile decorations.'
    )
    embed.add_field(name='ACHIEVEMENT BADGES', value=badges_achievements, inline=False)
    embed.add_field(name='COOLNESS BADGES', value=badges_coolness, inline=False)
    embed.add_field(name='OTHER BADGES', value=badges_other, inline=False)
    embed.add_field(name='HOW TO USE', value=howtouse, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_coolness_guide() -> discord.Embed:
    """Coolness guide"""
    usage = (
        f'{emojis.BP} Unlocks cosmetic only profile badges (see {emojis.LOGO}`/badges`)\n'
        f'{emojis.BP} You need at least 2,000 coolness for dungeon 15-2'
    )
    req = f'{emojis.BP} Unlocks when you reach area 12 in {emojis.TIME_TRAVEL}TT 1'
    howtoget = (
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/ultraining` awards 2 coolness per stage '
        f'(see {emojis.LOGO}`/ultraining guide`)\n'
        f'{emojis.BP} Do an adventure with full HP and survive with 1 HP\n'
        f'{emojis.BP} Open {emojis.LB_OMEGA} OMEGA and {emojis.LB_GODLY} GODLY lootboxes\n'
        f'{emojis.BP} Get HYPER, ULTRA or ULTIMATE logs from work commands\n'
        f'{emojis.BP} Forge ULTRA-EDGY or higher gear\n'
        f'{emojis.BP} Ascend a pet\n'
        f'{emojis.BP} Do other \'cool\' actions that are currently unknown'
    )
    note = (
        f'{emojis.BP} You don\'t lose coolness when you time travel\n'
        f'{emojis.BP} You can get coolness in every area once it\'s unlocked\n'
        f'{emojis.BP} If you have 100+, you get less (except from {emojis.EPIC_RPG_LOGO_SMALL}`/ultraining`)\n'
        f'{emojis.BP} You can check your coolness by using {emojis.EPIC_RPG_LOGO_SMALL}`/ultraining progress: true`\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'COOLNESS {emojis.STAT_COOLNESS}',
        description = 'Coolness is a stat you start collecting once you reach area 12.'
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='REQUIREMENTS', value=req, inline=False)
    embed.add_field(name='HOW TO GET COOLNESS', value=howtoget, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_farming_overview() -> discord.Embed:
    """Farming guide overview"""
    planting_normal = (
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/farm` to plant {emojis.SEED} seeds. '
        f'Buy seeds in the shop for 4,000 coins.\n'
        f'{emojis.BP} This gives you XP and either {emojis.BREAD} bread, {emojis.CARROT} carrots or '
        f'{emojis.POTATO} potatoes\n'
        f'{emojis.BP} You have a 4% chance to receive special seeds (see below)\n'
        f'{emojis.BP} The cooldown of the command is 10m (donor reduction applies)'
    )
    planting_special = (
        f'{emojis.BP} There are three special seeds: {emojis.SEED_BREAD} bread, {emojis.SEED_CARROT} carrot and '
        f'{emojis.SEED_POTATO} potato seed\n'
        f'{emojis.BP} You can plant them with {emojis.EPIC_RPG_LOGO_SMALL}`/farm` '
        f'(e.g. {emojis.EPIC_RPG_LOGO_SMALL}`/farm seed: carrot`)\n'
        f'{emojis.BP} The crop will be the same type (e.g. a {emojis.SEED_CARROT} carrot seed gives you '
        f'{emojis.CARROT} carrots)\n'
        f'{emojis.BP} You have a 65% chance to get 1 seed and a 10% chance to get 2 seeds back'
    )
    what_to_plant = (
        f'{emojis.BP} If you want to cook food for levels or stats: {emojis.CARROT} carrots\n'
        f'{emojis.BP} If you want to get more coins or a higher STT score: {emojis.BREAD} bread\n'
        f'{emojis.BP} If you want to flex potatoes for some reason: {emojis.POTATO} potatoes'
    )
    note = (
        f'{emojis.BP} Farming is unlocked in area 4\n'
        f'{emojis.BP} The amount of items you gain increases with your TT\n'
        f'{emojis.BP} You can not farm in the TOP'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'FARMING GUIDE',
        description = f'It ain\'t much, but it\'s honest work.'
    )
    embed.add_field(name='PLANTING NORMAL SEEDS', value=planting_normal, inline=False)
    embed.add_field(name='PLANTING SPECIAL SEEDS', value=planting_special, inline=False)
    embed.add_field(name='WHAT TO FARM?', value=what_to_plant, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_farming_usage() -> discord.Embed:
    """Farming item usage"""
    usage_bread = (
        f'{emojis.BP} {emojis.SWORD_HAIR} `Hair Sword` ➜ 4 {emojis.MERMAID_HAIR} + **220** {emojis.BREAD}\n'
        f'{emojis.BP} {emojis.ARMOR_ELECTRONICAL} `Electronical Armor` ➜ 12 {emojis.CHIP} + 1 {emojis.LOG_HYPER} + '
        f'**180** {emojis.BREAD}\n'
        f'{emojis.BP} {emojis.FOOD_CARROT_BREAD} `Carrot Bread` (+1 Level) ➜ **1** {emojis.BREAD} + '
        f'160 {emojis.CARROT}\n'
        f'{emojis.BP} Can be sold for 3,000 coins and 3 merchant XP\n'
        f'{emojis.BP} Heals the player and gives a temporary +5 LIFE when eaten '
        f'({emojis.EPIC_RPG_LOGO_SMALL}`/heal item: bread`)'
    )
    usage_carrot = (
        f'{emojis.BP} {emojis.FOOD_CARROT_BREAD} `Carrot Bread` (+1 Level) ➜ 1 {emojis.BREAD} + **160** '
        f'{emojis.CARROT}\n'
        f'{emojis.BP} {emojis.FOOD_ORANGE_JUICE} `Orange Juice` (+3 AT, +3 DEF) ➜ **320** {emojis.CARROT}\n'
        f'{emojis.BP} {emojis.FOOD_CARROTATO_CHIPS} `Carrotato Chips` (+25 random profession XP) ➜ 80 {emojis.POTATO} '
        f'+ **80** {emojis.CARROT}\n'
        f'{emojis.BP} Can be sold for 2,500 coins and 3 merchant XP\n'
        f'{emojis.BP} Can be used to change the horse name with {emojis.EPIC_RPG_LOGO_SMALL}`/horse feed`'
    )
    usage_potato = (
        f'{emojis.BP} {emojis.SWORD_RUBY} `Ruby Sword` ➜ 4 {emojis.RUBY} + 1 {emojis.LOG_MEGA} + **36** '
        f'{emojis.POTATO}\n'
        f'{emojis.BP} {emojis.ARMOR_RUBY} `Ruby Armor` ➜ 7 {emojis.RUBY} + 4 {emojis.UNICORN_HORN} + **120** '
        f'{emojis.POTATO} + 2 {emojis.LOG_MEGA}\n'
        f'{emojis.BP} {emojis.SWORD_ELECTRONICAL} `Electronical Sword` ➜ 8 {emojis.CHIP} + 1 {emojis.LOG_MEGA} '
        f'+ **140** {emojis.POTATO}\n'
        f'{emojis.BP} {emojis.SWORD_WATERMELON} `Watermelon Sword` ➜ 1 {emojis.WATERMELON} + **10** {emojis.POTATO}\n'
        f'{emojis.BP} {emojis.FOOD_CARROTATO_CHIPS} `Carrotato Chips` (+25 random profession XP) '
        f'➜ **80** {emojis.POTATO} + 80 {emojis.CARROT}\n'
        f'{emojis.BP} Can be sold for 2,000 coins and 3 merchant XP'
    )
    stt_score = (
        f'{emojis.BP} 25 {emojis.BREAD} bread = 1 score\n'
        f'{emojis.BP} 30 {emojis.CARROT} carrots = 1 score\n'
        f'{emojis.BP} 35 {emojis.POTATO} potatoes = 1 score\n'
    )
    what_to_plant = (
        f'{emojis.BP} If you want to cook food for levels or stats: {emojis.CARROT} carrots\n'
        f'{emojis.BP} If you want to get more coins or a higher STT score: {emojis.BREAD} bread\n'
        f'{emojis.BP} If you want to flex potatoes for some reason: {emojis.POTATO} potatoes'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CROPS USAGE AND VALUE',
        description = f'It ain\'t much, but it\'s honest work.'
    )
    embed.add_field(name='BREAD USAGE', value=usage_bread, inline=False)
    embed.add_field(name='CARROT USAGE', value=usage_carrot, inline=False)
    embed.add_field(name='POTATO USAGE', value=usage_potato, inline=False)
    embed.add_field(name='STT SCORE', value=stt_score, inline=False)
    embed.add_field(name='WHAT TO FARM?', value=what_to_plant, inline=False)
    return embed


async def embed_beginner_overview() -> discord.Embed:
    """Beginner guide overview"""
    goal = (
        f'The goal is to advance until you reach your highest reachable area. At that point you can time travel.\n'
        f'Think of this as new game+. This resets your progress but unlocks more of the game. For more information '
        f'see {emojis.LOGO}`/timetravel guide`.\n'
        f'To check out the available commands in this game, use {emojis.EPIC_RPG_LOGO_SMALL}`/start` '
        f'and {emojis.EPIC_RPG_LOGO_SMALL}`/help`.'
    )
    areas_dungeons = (
        f'You advance by moving through areas. You can check what you should do in each area in the area guides '
        f'(see {emojis.LOGO}`/area guide`).\n'
        f'To leave an area and advance to the next one you have to beat the dungeon for that area (so to leave area 1 '
        f'you do dungeon 1).\n'
        f'Dungeons 1 to 9 are simple tank and spank affairs, there is no gear check. So, if needed, you can enter them '
        f'undergeared and get carried.\n'
        f'**This does not work for dungeons 10+**. To enter those you **need** to have certain gear.'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'BEGINNER GUIDE',
        description = 'Welcome to EPIC RPG! This is a guide to help you out with your first run.'
    )
    embed.add_field(name='GOAL OF THE GAME', value=goal, inline=False)
    embed.add_field(name='AREAS & DUNGEONS', value=areas_dungeons, inline=False)
    return embed


async def embed_beginner_first_run() -> discord.Embed:
    """Beginner first run guide"""
    first_run = (
        f'Your first run is called TT0 (time travel 0) because you haven\'t time traveled yet. In TT0 you need to '
        f'reach area 11 which means you need to beat dungeon 10.\n'
        f'Now, as mentioned, D10 has gear requirements, so you can not cheese that dungeon, you **need** to craft '
        f'the following gear:\n'
        f'{emojis.SWORD_EDGY} EDGY Sword (requires 1 {emojis.LOG_ULTRA} ULTRA log)\n'
        f'{emojis.ARMOR_EDGY} EDGY Armor (requires a lot of mob drops)\n'
        f'The ULTRA log needed for the sword equals 250,000 wooden logs and the mob drops for the armor are pretty '
        f'rare (see {emojis.LOGO}`/monster drops`).\n'
        f'This means that your main goal in TT0 is to farm enough materials to be able to craft this shiny EDGY gear.'
    )
    grinding_trades = (
        f'Grinding all those materials takes time, so you want to do this smartly.\n'
        f'Trade rates are the single most important thing in this game to help you saving time. Every area has '
        f'different trade rates, so every time you advance, your trade rates change (see {emojis.LOGO}`/trade rates`). '
        f'You can **not** go back to earlier trade rates, these are tied to your highest unlocked area.\n'
        f'This means you can save a lot of time and materials if you farm **early** and exploit the trade rate '
        f'changes to multiply your inventory. See {emojis.LOGO}`/trade guide` for more trading info.\n'
        f'In TT0 the most important area is **area 5**. You want to stay there until you have the recommended '
        f'materials (see {emojis.LOGO}`/area guide area: 5`).\n'
        f'If you do this, you will save a ton of time later on and be able to craft that EDGY gear as soon as '
        f'you reach areas 9 and 10. Don\'t forget to check out the area guides for other recommendations.'
    )
    tips = (
        f'{emojis.BP} Yes, farming in area 5 is boring. But do not leave the area early, you **will** regret it.\n'
        f'{emojis.BP} Do not craft the EDGY Sword before area 10. You will lose materials if you do.'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'YOUR FIRST RUN',
        description = 'Welcome to EPIC RPG! This is a guide to help you out with your first run.'
    )
    embed.add_field(name='YOUR FIRST RUN', value=first_run, inline=False)
    embed.add_field(name='GRINDING & TRADES', value=grinding_trades, inline=False)
    embed.add_field(name='TIPS', value=tips, inline=False)
    return embed