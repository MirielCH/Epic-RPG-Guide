# xmas.py
"""Contains all christmas guides"""

import discord

from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_TLDR_GUIDE = 'TL;DR guide'
TOPIC_CHRISTMAS_AREA = 'Christmas area'
TOPIC_SANTEVIL = 'SANTEVIL event'
TOPIC_SNOWBALL = 'Snowball event'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_TLDR_GUIDE,
    TOPIC_CHRISTMAS_AREA,
    TOPIC_SANTEVIL,
    TOPIC_SNOWBALL,
]


# -- Items ---
ITEM_CANDY_CANE = 'Candy cane'
ITEM_CHRISTMAS_HAT = 'Christmas hat'
ITEM_CHRISTMAS_KEY = 'Christmas key'
ITEM_CHRISTMAS_SOCK = 'Christmas sock'
ITEM_CHRISTMAS_STAR = 'Christmas star'
ITEM_CHRISTMAS_STAR_PARTS = 'Christmas star parts'
ITEM_COOKIES_AND_MILK = 'Cookies and milk'
ITEM_EPIC_SNOWBALL = 'Epic snowball'
ITEM_FRUIT_CAKE = 'Fruit cake'
ITEM_GINGERBREAD = 'Gingerbread'
ITEM_HOLLY_LEAVES = 'Holly leaves'
ITEM_ORNAMENT = 'Ornament'
ITEM_ORNAMENT_PART = 'Ornament part'
ITEM_PINE_NEEDLE = 'Pine needle'
ITEM_PRESENT = 'Presents'
ITEM_SANTA_ARMOR = 'Santa armor'
ITEM_SANTA_HAIR = 'Santa hair'
ITEM_SANTA_SWORD = 'Santa sword'
ITEM_SLEEPY_POTION = 'Sleepy potion'
ITEM_SNOW_BOX = 'Snow box'
ITEM_SNOWBALL = 'Snowball'
ITEM_SNOWFLAKE = 'Snowflake'
ITEM_TIME_CAPSULE = 'TIME capsule'
ITEM_TIME_COOKIE = 'TIME cookie'

ITEMS = [
    ITEM_CANDY_CANE,
    ITEM_CHRISTMAS_HAT,
    ITEM_CHRISTMAS_KEY,
    ITEM_CHRISTMAS_SOCK,
    ITEM_CHRISTMAS_STAR,
    ITEM_CHRISTMAS_STAR_PARTS,
    ITEM_COOKIES_AND_MILK,
    ITEM_EPIC_SNOWBALL,
    ITEM_FRUIT_CAKE,
    ITEM_GINGERBREAD,
    ITEM_HOLLY_LEAVES,
    ITEM_ORNAMENT,
    ITEM_ORNAMENT_PART,
    ITEM_PINE_NEEDLE,
    ITEM_PRESENT,
    ITEM_SANTA_ARMOR,
    ITEM_SANTA_HAIR,
    ITEM_SANTA_SWORD,
    ITEM_SLEEPY_POTION,
    ITEM_SNOW_BOX,
    ITEM_SNOWBALL,
    ITEM_SNOWFLAKE,
    ITEM_TIME_CAPSULE,
    ITEM_TIME_COOKIE,
]

# --- Commands ---
async def command_xmas_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Christmas guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_overview,
        TOPIC_TLDR_GUIDE: embed_tldr_guide,
        TOPIC_CHRISTMAS_AREA: embed_christmas_area,
        TOPIC_SANTEVIL: embed_santevil,
        TOPIC_SNOWBALL: embed_snowball,
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


async def command_xmas_items(ctx: discord.ApplicationContext, item: str) -> None:
    """Christmas guide command"""
    items_emojis_functions = {
        ITEM_CANDY_CANE: (emojis.CANDY_CANE, embed_item_candy_cane),
        ITEM_CHRISTMAS_HAT: (emojis.XMAS_HAT, embed_item_christmas_hat),
        ITEM_CHRISTMAS_KEY: (emojis.CANDY_KEY, embed_item_christmas_key),
        ITEM_CHRISTMAS_SOCK: (emojis.XMAS_SOCKS, embed_item_christmas_sock),
        ITEM_CHRISTMAS_STAR: (emojis.XMAS_STAR, embed_item_christmas_star),
        ITEM_CHRISTMAS_STAR_PARTS: (emojis.XMAS_STAR_PART_1, embed_item_christmas_star_parts),
        ITEM_COOKIES_AND_MILK: (emojis.COOKIES_AND_MILK, embed_item_cookies_and_milk),
        ITEM_EPIC_SNOWBALL: (emojis.SNOWBALL_EPIC, embed_item_epic_snowball),
        ITEM_FRUIT_CAKE: (emojis.FRUIT_CAKE, embed_item_fruit_cake),
        ITEM_GINGERBREAD: (emojis.GINGERBREAD, embed_item_gingerbread),
        ITEM_HOLLY_LEAVES: (emojis.HOLLY_LEAVES, embed_item_holly_leaves),
        ITEM_ORNAMENT: (emojis.ORNAMENT, embed_item_ornament),
        ITEM_ORNAMENT_PART: (emojis.ORNAMENT_PART, embed_item_ornament_part),
        ITEM_PINE_NEEDLE: (emojis.PINE_NEEDLE, embed_item_pine_needle),
        ITEM_PRESENT: (emojis.PRESENT_VOID, embed_item_present),
        ITEM_SANTA_ARMOR: (emojis.ARMOR_SANTA, embed_item_santa_gear),
        ITEM_SANTA_HAIR: (emojis.SANTA_HAIR, embed_item_santa_hair),
        ITEM_SANTA_SWORD: (emojis.SWORD_SANTA, embed_item_santa_gear),
        ITEM_SLEEPY_POTION: (emojis.POTION_SLEEPY, embed_item_sleepy_potion),
        ITEM_SNOW_BOX: (emojis.SNOW_BOX, embed_item_snow_box),
        ITEM_SNOWBALL: (emojis.SNOWBALL, embed_item_snowball),
        ITEM_SNOWFLAKE: (emojis.SNOWFLAKE, embed_item_snowflake),
        ITEM_TIME_CAPSULE: (emojis.TIME_CAPSULE, embed_item_time_capsule),
        ITEM_TIME_COOKIE: (emojis.TIME_COOKIE, embed_item_time_cookie),
    }
    view = views.ItemView(ctx, items_emojis_functions, active_item=item)
    embed = await items_emojis_functions[item][1]()
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    try:
        await functions.edit_interaction(interaction, view=None)
    except discord.errors.NotFound:
        pass


# --- Embeds ---
async def embed_overview() -> discord.Embed:
    """Christmas overview embed"""
    activities = (
        f'{emojis.BP} Get various {strings.SLASH_COMMANDS_GUIDE["xmas items"]}\n'
        f'{emojis.BP} Complete daily and weekly {strings.SLASH_COMMANDS_EPIC_RPG["xmas tasks"]}\n'
        f'{emojis.BP} Craft various items (see {strings.SLASH_COMMANDS_EPIC_RPG["xmas recipes"]})\n'
        f'{emojis.BP} Find, craft and open {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} Get stuck in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas chimney"]}\n'
        f'{emojis.DETAIL} This event command has a `3`h cooldown\n'
        f'{emojis.BP} Open a door in your {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]} every day\n'
        f'{emojis.BP} Visit the christmas area (see topic `Christmas area`)\n'
        f'{emojis.BP} Beat the candy dragon in the christmas dungeon '
        f'(see {strings.SLASH_COMMANDS_EPIC_RPG["xmas info"]} `topic: dungeon`)\n'
        f'{emojis.BP} Complete the {strings.SLASH_COMMANDS_EPIC_RPG["xmas quests"]}\n'
        f'{emojis.BP} Decorate a {strings.SLASH_COMMANDS_EPIC_RPG["xmas tree"]}\n'
        f'{emojis.BP} Get into a snowball fight (see topic `Snowball event`)\n'
        f'{emojis.BP} Encounter the super rare SANTEVIL (see topic `SANTEVIL event`)\n'
        f'{emojis.BP} Buy rewards in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas shop"]}\n'
    )
    pets = (
        f'{emojis.BP} **A** {emojis.PET_PENGUIN} **penguin**!\n'
        f'{emojis.DETAIL} Drops from {emojis.PRESENT_VOID} VOID presents.\n'
        f'{emojis.DETAIL} Has the {emojis.SKILL_ANTARCTICIAN} antarctician skill which turns all fish found into EPIC.\n'
        f'{emojis.BP} **A** {emojis.PET_SNOWBALL} **snowball!**\n'
        f'{emojis.DETAIL} Reward for completing the tree.\n'
        f'{emojis.DETAIL} Has the {emojis.SKILL_GIFTER} gifter skill which can bring back lootboxes.\n'
        f'{emojis.BP} **A** {emojis.PET_SNOWMAN} **snowman!**\n'
        f'{emojis.DETAIL} Must be upgraded from a snowball pet with an {emojis.SNOWBALL_EPIC} EPIC snowball.\n'
        f'{emojis.DETAIL} Has the {emojis.SKILL_GIFTER} gifter skill but brings back better lootboxes than the snowball.\n'
    )
    bonuses = (
        f'{emojis.BP} Arena cooldown is reduced by `50`%\n'
        f'{emojis.BP} Double XP when eating {emojis.ARENA_COOKIE} arena cookies (**not** super cookies!)\n'
        f'{emojis.DETAIL} Note that even at double XP 1 super cookie is still worth more than 1000 cookies\n'
    )
    schedule = (
        f'{emojis.BP} Event started on December 1, 2022\n'
        f'{emojis.DETAIL} World boss starts later on December 5, 2022\n'
        f'{emojis.BP} Event ends on January 5, 2023, 23:55 UTC\n'
        f'{emojis.BP} Items will vanish on January 12, 2023, 23:55 UTC\n'
        f'{emojis.DETAIL} Exception: {emojis.TIME_COOKIE} TIME cookies do not vanish'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'CHRISTMAS EVENT 2022 {emojis.XMAS_TREE}',
        description = 'HO HO HO (yes, very imaginative, I know)'
    )
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='UNIQUE CHRISTMAS PETS YOU CAN GET', value=pets, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed


async def embed_christmas_area() -> discord.Embed:
    """Christmas area"""
    requirements = (
        f'{emojis.BP} Can only be reached by using a {emojis.GINGERBREAD} gingerbread\n'
        f'{emojis.BP} You can get {emojis.GINGERBREAD} gingerbread from {strings.SLASH_COMMANDS_EPIC_RPG["xmas tasks"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} Can be left anytime but accessing it again requires another {emojis.GINGERBREAD} gingerbread\n'
    )
    differences = (
        f'{emojis.BP} You get `2` christmas items ({emojis.SNOWBALL} or {emojis.PRESENT}) when using '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} You get normal mob drops in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} according to your **max** area\n'
        f'{emojis.BP} You do not get XP and coins from {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} and '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} You do not get any items from any fish command tiers\n'
        f'{emojis.BP} You get double the worker XP from all chop command tiers\n'
        f'{emojis.BP} You do not take damage from mobs in this area\n'
        f'{emojis.BP} Your cooldowns are reduced by `10`%\n'
    )
    dungeon = (
        f'{emojis.BP} This area features a unique christmas dungeon\n'
        f'{emojis.BP} For details about how it all works, see {strings.SLASH_COMMANDS_EPIC_RPG["xmas info"]} '
        f'`topic: dungeon`\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CHRISTMAS AREA (AREA 0)',
        description = 'This is a special christmas themed area that can only be entered during the christmas event.'
    )
    embed.add_field(name='HOW TO ACCESS', value=requirements, inline=False)
    embed.add_field(name='DIFFERENCES TO NORMAL AREAS', value=differences, inline=False)
    embed.add_field(name='CHRISTMAS DUNGEON', value=dungeon, inline=False)
    return embed


async def embed_tldr_guide() -> discord.Embed:
    """Christmas TL;DR guide"""
    tldr_guide = (
        f'{emojis.BP} Craft as many {emojis.COOKIES_AND_MILK} cookies and milk as you can\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["xmas chimney"]} on cooldown\n'
        f'{emojis.DETAIL} This event command has a `3`h cooldown\n'
        f'{emojis.BP} Complete your {strings.SLASH_COMMANDS_EPIC_RPG["xmas tasks"]} daily\n'
        f'{emojis.BP} Check your {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]} daily\n'
        f'{emojis.BP} **Optional**: Craft the {emojis.SWORD_SANTA}{emojis.ARMOR_SANTA} santa gear if you want to stay in '
        f'the christmas area as long as possible. This allows you to advance your max area beating the christmas dungeon.\n'
        f'{emojis.BP} Beat the christmas dungeon at least twice for the quest\n'
        f'{emojis.BP} Complete the christmas quests in {strings.SLASH_COMMANDS_EPIC_RPG["xmas quests"]}.\n'
        f'{emojis.DETAIL} Do the quest that tasks you to open 600 presents last.\n'
        f'{emojis.BP} Complete the tree in {strings.SLASH_COMMANDS_EPIC_RPG["xmas tree"]} before december 25th\n'
        f'{emojis.BP} Buy whatever you want from the shop in {strings.SLASH_COMMANDS_EPIC_RPG["xmas shop"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CHRISTMAS TL;DR GUIDE'
    )
    embed.add_field(name='WHAT TO DO', value=tldr_guide, inline=False)
    return embed


async def embed_snowball() -> discord.Embed:
    """Snowball event"""
    trigger = (
        f'{emojis.BP} Any command (chance unknown)\n'
        f'{emojis.BP} By using a {emojis.XMAS_HAT} christmas hat'
    )
    answers = (
        f'{emojis.BP} `fight`: Low chance to get more loot than `summon`, high chance to get less.\n'
        f'{emojis.BP} `summon`: 50/50 chance to get more or less loot\n'
        f'{emojis.BP} `sleep`: Very low chance to get more loot than `summon` and `fight`, very high chance to get less'
    )
    rewards = (
        f'{emojis.BP} {emojis.SNOWBALL} snowballs and {emojis.PRESENT} presents\n'
    )
    best_answer = (
        f'{emojis.BP} If you don\'t feel like gambling, `summon` is the safest answer\n'
        f'{emojis.BP} If you __do__ feel like gambling, `sleep` has the highest potential rewards'
    )
    note =(
        f'{emojis.BP} This event gives much higher rewards if it\'s triggered with a {emojis.XMAS_HAT} christmas hat\n'
        f'{emojis.BP} You always get some loot, even if you lose'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'SNOWBALL EVENT',
        description = 'This is a random personal christmas event in which the EPIC NPC starts a snowball fight with you.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='BEST ANSWER', value=best_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_santevil() -> discord.Embed:
    """SANTEVIL event"""
    trigger = (
        f'{emojis.BP} Any command (chance unknown, but very low)\n'
    )
    answers = (
        f'{emojis.BP} `ho`: You join the battle, but might not do much damage\n'
        f'{emojis.BP} `ho ho`: You do more damage, but have a chance to not get anything\n'
        f'{emojis.BP} `ho ho ho`: You do even more damage, but have a chance to **lose presents**\n'
    )
    rewards_win = (
        f'{emojis.BP} {emojis.PRESENT}{emojis.PRESENT_EPIC}{emojis.PRESENT_MEGA}{emojis.PRESENT_ULTRA}'
        f'{emojis.PRESENT_OMEGA}{emojis.PRESENT_GODLY}{emojis.PRESENT_VOID} random presents (common)\n'
        f'{emojis.BP} {emojis.SANTA_HAIR} santa hair (rare)\n'
    )
    best_answer = (
        f'{emojis.BP} Winning depends on how many people join the fight\n'
        f'{emojis.BP} If few people, do more damage, if more people, you can play it safer\n'
        f'{emojis.BP} If you don\'t care about your presents, just go for the most damage\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'SANTEVIL EVENT',
        description = 'This is a random multiplayer christmas event in which the legendary SANTEVIL spawns.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS IF SUCCESSFUL', value=rewards_win, inline=False)
    embed.add_field(name='BEST ANSWER', value=best_answer, inline=False)
    return embed


async def embed_item_candy_cane() -> discord.Embed:
    """Item: Candy cane"""
    source = (
        f'{emojis.BP} Mythic loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]} (`25` max)\n'
        f'{emojis.BP} You can get some in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]}\n'
        f'{emojis.BP} Random reward from the christmas dungeon '
        f'(see {strings.SLASH_COMMANDS_EPIC_RPG["xmas info"]} `topic: dungeon`)'
    )
    usage = (
        f'{emojis.BP} Lets you skip to the next area without doing the dungeon\n'
        f'{emojis.BP} Does **not** let you skip your last dungeon (e.g. D11 in {emojis.TIME_TRAVEL} TT 1)\n'
        f'{emojis.BP} Also rewards some {emojis.SNOWBALL} snowballs when used\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'CANDY CANE {emojis.CANDY_CANE}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_christmas_hat() -> discord.Embed:
    """Item: Christmas hat"""
    source = (
        f'{emojis.BP} Mythic loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]} (`20` max)\n'
        f'{emojis.BP} Random reward from the christmas dungeon '
        f'(see {strings.SLASH_COMMANDS_EPIC_RPG["xmas info"]} `topic: dungeon`)'
    )
    usage = (
        f'{emojis.BP} Spawns a snowball fight event '
        f'(see {strings.SLASH_COMMANDS_GUIDE["xmas guide"]} `topic: Snowball event`)\n'
        f'{emojis.DETAIL} The event gives higher rewards than normal when triggered with a hat\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'CHRISTMAS HAT {emojis.XMAS_HAT}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_christmas_key() -> discord.Embed:
    """Item: Christmas key"""
    source = (
        f'{emojis.BP} Can be crafted (see {strings.SLASH_COMMANDS_EPIC_RPG["xmas recipes"]})\n'
        f'{emojis.DETAIL} You need a {emojis.DUNGEON_KEY_1}{emojis.DUNGEON_KEY_10} dungeon key to craft this item. '
        f'A {emojis.TIME_KEY} TIME key also works.\n'
        f'{emojis.DETAIL} Dungeon keys are consumed when crafting, the TIME key is not.\n'
        f'{emojis.BP} Random reward from the christmas dungeon '
        f'(see {strings.SLASH_COMMANDS_EPIC_RPG["xmas info"]} `topic: dungeon`)'
    )
    usage = (
        f'{emojis.BP} Required to enter the christmas dungeon '
        f'(see {strings.SLASH_COMMANDS_EPIC_RPG["xmas info"]} `topic: dungeon`)'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'CHRISTMAS KEY {emojis.CANDY_KEY}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_christmas_sock() -> discord.Embed:
    """Item: Christmas sock"""
    source = (
        f'{emojis.BP} Pog loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} You can get some in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]}\n'
    )
    usage = (
        f'{emojis.BP} Increases your chance to drop higher tier presents.\n'
        f'{emojis.DETAIL} This effect is passive, just keep them in inventory.\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'CHRISTMAS SOCK {emojis.XMAS_SOCKS}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_christmas_star() -> discord.Embed:
    """Item: Christmas star"""
    source = (
        f'{emojis.BP} Can be crafted (see {strings.SLASH_COMMANDS_EPIC_RPG["xmas recipes"]}).\n'
        f'{emojis.DETAIL} You need to complete the {strings.SLASH_COMMANDS_EPIC_RPG["xmas quests"]} to get the parts.\n'
    )
    usage = (
        f'{emojis.BP} Required to complete the {strings.SLASH_COMMANDS_EPIC_RPG["xmas tree"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'CHRISTMAS STAR {emojis.XMAS_STAR}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_christmas_star_parts() -> discord.Embed:
    """Item: Christmas star parts"""
    source = (
        f'{emojis.BP} Acquired by completing the {strings.SLASH_COMMANDS_EPIC_RPG["xmas quests"]}\n'
    )
    usage = (
        f'{emojis.BP} Required to craft the christmas star (see item `Christmas star`)\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = (
            f'CHRISTMAS STAR PARTS {emojis.XMAS_STAR_PART_1}{emojis.XMAS_STAR_PART_2}{emojis.XMAS_STAR_PART_3}'
            f'{emojis.XMAS_STAR_PART_4}{emojis.XMAS_STAR_PART_5}'
        ),
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_cookies_and_milk() -> discord.Embed:
    """Item: Cookies and milk"""
    source = (
        f'{emojis.BP} Can be crafted (see {strings.SLASH_COMMANDS_EPIC_RPG["xmas recipes"]})\n'
    )
    usage = (
        f'{emojis.BP} Randomly resets command cooldowns\n'
        f'{emojis.DETAIL} Shorter cooldowns have a higher chance of being reset\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'COOKIES AND MILK {emojis.COOKIES_AND_MILK}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_epic_snowball() -> discord.Embed:
    """Item: Epic snowball"""
    source = (
        f'{emojis.BP} Very rare drop from various commands\n'
        f'{emojis.BP} Rare reward from the snowball fight (see {strings.SLASH_COMMANDS_GUIDE["xmas guide"]} '
        f'`topic: snowball event`)\n'
    )
    usage = (
        f'{emojis.BP} Upgrades one {emojis.PET_SNOWBALL} snowball pet to a {emojis.PET_SNOWMAN} snowman pet\n'
        f'{emojis.DETAIL} Still has the {emojis.SKILL_GIFTER} gifter skill, but a higher chance to get better '
        f'lootboxes\n'
        f'{emojis.DETAIL} If you have multiple snowball pets, the one chosen is random\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'EPIC SNOWBALL {emojis.SNOWBALL_EPIC}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_fruit_cake() -> discord.Embed:
    """Item: Fruit cake"""
    source = (
        f'{emojis.BP} Can be crafted (see {strings.SLASH_COMMANDS_EPIC_RPG["xmas recipes"]})\n'
    )
    usage = (
        f'{emojis.BP} Activates a world buff\n'
        f'{emojis.DETAIL} Increases the chance to get double snowballs in {strings.SLASH_COMMANDS_EPIC_RPG["arena"]} '
        f'by `30`% for 45min\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'FRUIT CAKE {emojis.FRUIT_CAKE}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_gingerbread() -> discord.Embed:
    """Item: Gingerbread"""
    source = (
        f'{emojis.BP} Mythic loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} Reward for completing weekly {strings.SLASH_COMMANDS_EPIC_RPG["xmas tasks"]}\n'
        f'{emojis.BP} You can get some in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]}\n'
    )
    usage = (
        f'{emojis.BP} Teleports you to the christmas area (see {strings.SLASH_COMMANDS_GUIDE["xmas guide"]} '
        f'`topic: christmas area`)\n'
        f'{emojis.BP} Used as a currency in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas shop"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'GINGERBREAD {emojis.GINGERBREAD}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_holly_leaves() -> discord.Embed:
    """Item: Holly leaves"""
    source = (
        f'{emojis.BP} Drops from {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
    )
    usage = (
        f'{emojis.BP} Used to join the world fight in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas wb"]}\n'
        f'{emojis.DETAIL} Note that this might be subject to change'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'HOLLY LEAVES {emojis.HOLLY_LEAVES}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_ornament() -> discord.Embed:
    """Item: Ornament"""
    source = (
        f'{emojis.BP} Drops from {strings.SLASH_COMMANDS_EPIC_RPG["training"]}, '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} and rarely other commands\n'
        f'{emojis.BP} Rare loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} Can be crafted (see {strings.SLASH_COMMANDS_EPIC_RPG["xmas recipes"]})\n'
        f'{emojis.BP} You can get some in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]}\n'
    )
    usage = (
        f'{emojis.BP} Required to complete the {strings.SLASH_COMMANDS_EPIC_RPG["xmas tree"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'ORNAMENT {emojis.ORNAMENT}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_ornament_part() -> discord.Embed:
    """Item: Ornament part"""
    source = (
        f'{emojis.BP} Uncommon loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} You can get some in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]}\n'
        f'{emojis.BP} Random reward from the snowball fight (see {strings.SLASH_COMMANDS_GUIDE["xmas guide"]} '
        f'`topic: snowball event`)\n'
    )
    usage = (
        f'{emojis.BP} Used to craft {emojis.ORNAMENT} ornaments (see {strings.SLASH_COMMANDS_EPIC_RPG["xmas recipes"]})\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'ORNAMENT PART {emojis.ORNAMENT_PART}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_pine_needle() -> discord.Embed:
    """Item: Pine needle"""
    source = (
        f'{emojis.BP} Drops from {strings.SLASH_COMMANDS_EPIC_RPG["training"]} and '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} Uncommon loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} You can get some in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]}\n'
        f'{emojis.BP} Random reward from the snowball fight (see {strings.SLASH_COMMANDS_GUIDE["xmas guide"]} '
        f'`topic: snowball event`)\n'
    )
    usage = (
        f'{emojis.BP} Required to complete the {strings.SLASH_COMMANDS_EPIC_RPG["xmas tree"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'PINE NEEDLE {emojis.PINE_NEEDLE}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_present() -> discord.Embed:
    """Item: Presents"""
    source = (
        f'{emojis.BP} Drops from various commands\n'
        f'{emojis.BP} Can be crafted (see {strings.SLASH_COMMANDS_EPIC_RPG["xmas recipes"]})\n'
        f'{emojis.BP} Uncommon loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} You can get some in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]}\n'
        f'{emojis.BP} Reward from {strings.SLASH_COMMANDS_EPIC_RPG["xmas quests"]}\n'
        f'{emojis.BP} Random reward from the snowball fight (see {strings.SLASH_COMMANDS_GUIDE["xmas guide"]} '
        f'`topic: snowball event`)\n'
    )
    usage_common = (
        f'{emojis.BP} If you need {emojis.SNOWFLAKE} snowflakes: Open them\n'
        f'{emojis.BP} Otherwise: Craft into {emojis.PRESENT_EPIC} EPIC\n'
        f'{emojis.BP} ...or of course lose them all with {strings.SLASH_COMMANDS_EPIC_RPG["xmas slots"]}\n'
    )
    usage_epic = (
        f'{emojis.BP} Craft into {emojis.PRESENT_MEGA} MEGA\n'
    )
    usage_mega = (
        f'{emojis.BP} Open them\n'
    )
    usage_ultra = (
        f'{emojis.BP} If you need mythic or pog items: Craft into {emojis.PRESENT_OMEGA} OMEGA\n'
        f'{emojis.BP} If you need a {emojis.CANDY_KEY} christmas key: Craft into {emojis.PRESENT_OMEGA} OMEGA\n'
        f'{emojis.BP} Otherwise: Open them\n'
    )
    usage_omega = (
        f'{emojis.BP} If you need mythic or pog items: Craft into {emojis.PRESENT_GODLY} GODLY\n'
        f'{emojis.BP} If you need a {emojis.CANDY_KEY} christmas key: Craft into {emojis.PRESENT_GODLY} GODLY\n'
        f'{emojis.BP} Otherwise: Open them\n'
    )
    usage_godly = (
        f'{emojis.BP} If you need a {emojis.CANDY_KEY} christmas key: Use for crafting\n'
        f'{emojis.BP} Otherwise: Open them\n'
    )
    usage_void = (
        f'{emojis.BP} Open them\n'
    )
    usage_otherwise = (
        f'{emojis.BP} Well, idk, gift them to your mother\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = (
            f'PRESENTS {emojis.PRESENT}{emojis.PRESENT_EPIC}{emojis.PRESENT_MEGA}{emojis.PRESENT_ULTRA}'
            f'{emojis.PRESENT_OMEGA}{emojis.PRESENT_GODLY}{emojis.PRESENT_VOID}'
        ),
    )
    embed.add_field(name=f'COMMON PRESENTS {emojis.PRESENT} USAGE', value=usage_common, inline=False)
    embed.add_field(name=f'EPIC PRESENTS {emojis.PRESENT_EPIC} USAGE', value=usage_epic, inline=False)
    embed.add_field(name=f'MEGA PRESENTS {emojis.PRESENT_MEGA} USAGE', value=usage_mega, inline=False)
    embed.add_field(name=f'ULTRA PRESENTS {emojis.PRESENT_ULTRA} USAGE', value=usage_ultra, inline=False)
    embed.add_field(name=f'OMEGA PRESENTS {emojis.PRESENT_OMEGA} USAGE', value=usage_omega, inline=False)
    embed.add_field(name=f'GODLY PRESENTS {emojis.PRESENT_GODLY} USAGE', value=usage_godly, inline=False)
    embed.add_field(name=f'VOID PRESENTS {emojis.PRESENT_VOID} USAGE', value=usage_void, inline=False)
    embed.add_field(name='IF YOU DON\'T LIKE ANY OF THESE OPTIONS', value=usage_otherwise, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_santa_gear() -> discord.Embed:
    """Item: Santa gear"""
    source = (
        f'{emojis.BP} Can be crafted (see {strings.SLASH_COMMANDS_EPIC_RPG["xmas recipes"]})\n'
    )
    usage = (
        f'{emojis.BP} Changes christmas dungeon behaviour (see {strings.SLASH_COMMANDS_EPIC_RPG["xmas info"]} `topic: dungeon`)\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SANTA GEAR {emojis.SWORD_SANTA}{emojis.ARMOR_SANTA}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_santa_hair() -> discord.Embed:
    """Item: Santa hair"""
    source = (
        f'{emojis.BP} Pog loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} Random reward from the SANTEVIL event (see {strings.SLASH_COMMANDS_GUIDE["xmas guide"]} '
        f'`topic: SANTEVIL event`)\n'
    )
    usage = (
        f'{emojis.BP} Used to craft the {emojis.SWORD_SANTA} santa sword and {emojis.ARMOR_SANTA} armor\n'
        f'{emojis.BP} Looks gross\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SANTA HAIR {emojis.SANTA_HAIR}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_sleepy_potion() -> discord.Embed:
    """Item: Sleepy potion"""
    source = (
        f'{emojis.BP} Mythic loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]} (`15` max)\n'
        f'{emojis.BP} Can be bought in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas shop"]} (`35` max)\n'
        f'{emojis.BP} You can get some in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]}\n'
        f'{emojis.BP} Random reward from the christmas dungeon '
        f'(see {strings.SLASH_COMMANDS_EPIC_RPG["xmas info"]} `topic: dungeon`)'
    )
    usage = (
        f'{emojis.BP} Reduces (almost) all cooldowns by 24h\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SLEEPY POTION {emojis.POTION_SLEEPY}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_snow_box() -> discord.Embed:
    """Item: Snow box"""
    source = (
        f'{emojis.BP} Rare loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]} (`15` max)\n'
        f'{emojis.BP} Can be bought in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas shop"]} (`10` max)\n'
        f'{emojis.BP} Reward from one of the {strings.SLASH_COMMANDS_EPIC_RPG["xmas quests"]}'
    )
    usage = (
        f'{emojis.BP} Can be opened to get 2 - 20 {emojis.SNOWBALL} snowballs\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SNOW BOX {emojis.SNOW_BOX}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_snowball() -> discord.Embed:
    """Item: Snowball"""
    source = (
        f'{emojis.BP} Drops from various commands\n'
        f'{emojis.BP} Common loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} Contained in {emojis.SNOW_BOX} snow boxes\n'
        f'{emojis.BP} Random reward from {strings.SLASH_COMMANDS_EPIC_RPG["xmas chimney"]}\n'
        f'{emojis.BP} You can get some in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas calendar"]}\n'
        f'{emojis.BP} You get some when using a {emojis.CANDY_CANE} candy cane\n'
        f'{emojis.BP} Random reward from the snowball fight (see {strings.SLASH_COMMANDS_GUIDE["xmas guide"]} '
        f'`topic: snowball event`)\n'
    )
    usage = (
        f'{emojis.BP} Used in various {strings.SLASH_COMMANDS_EPIC_RPG["xmas recipes"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SNOWBALL {emojis.SNOWBALL}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_snowflake() -> discord.Embed:
    """Item: Snowflake"""
    source = (
        f'{emojis.BP} Reward for completing {strings.SLASH_COMMANDS_EPIC_RPG["xmas tasks"]}\n'
        f'{emojis.BP} Common loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]}\n'
        f'{emojis.BP} Reward from one of the {strings.SLASH_COMMANDS_EPIC_RPG["xmas quests"]}'
    )
    usage = (
        f'{emojis.BP} Used as a currency in the {strings.SLASH_COMMANDS_EPIC_RPG["xmas shop"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SNOWFLAKE {emojis.SNOWFLAKE}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    return embed


async def embed_item_time_capsule() -> discord.Embed:
    """Item: Time capsule"""
    source = (
        f'{emojis.BP} Pog loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]} (`1` max)\n'
    )
    usage = (
        f'{emojis.BP} Increases your {emojis.TIME_TRAVEL} time travel count by 1\n'
        f'{emojis.DETAIL} Does **not** change your active area\n'
    )
    note = (
        f'{emojis.BP} This is not an event item, it will not vanish after the event\n'
        f'{emojis.BP} However, it will **not** be lost when time traveling\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'TIME CAPSULE {emojis.TIME_CAPSULE}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_item_time_cookie() -> discord.Embed:
    """Item: Time cookie"""
    source = (
        f'{emojis.BP} Rare loot from {strings.SLASH_COMMANDS_EPIC_RPG["xmas presents"]} (`30` max)\n'
        f'{emojis.BP} Reward from the personal world boss event if you choose `throw`\n'
    )
    usage = (
        f'{emojis.BP} Reduces (almost) all cooldowns by 10-15 minutes\n'
    )
    note = (
        f'{emojis.BP} This is not an event item, it will not vanish after the event\n'
        f'{emojis.BP} However, it will **not** be lost when time traveling\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'TIME COOKIE {emojis.TIME_COOKIE}',
    )
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='SOURCE', value=source, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed