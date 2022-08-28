# xmas.py

import discord
from discord.ext import commands

from resources import emojis
from resources import settings
from resources import functions


# XMAS commands (cog)
class xmasCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    xmas_aliases = (
        'xmas',
        'christmas',
        'christmasevent',
        'xmasevent',
        'a0',
        'area0'
    )

    # Command "xmas"
    @commands.command(aliases=xmas_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def xmasguide(self, ctx, *args):
        items = [
            'candycane',
            'xmashat',
            'xmasstar',
            'xmasstarparts',
            'gingerbread',
            'ornament',
            'ornamentpart',
            'present',
            'pineneedle',
            'sleepypotion',
            'snowball',
            'snowbox',
            'snowflake',
            'hollyleaves',
            'cookiesandmilk',
            'fruitcake',
            'xmaskey'
        ]

        item_name_replacements = {
            'candycanes': 'candycane',
            'candy': 'candycane',
            'cane': 'candycane',
            'christmashat': 'xmashat',
            'hat': 'xmashat',
            'christmasstar': 'xmasstar',
            'star': 'xmasstar',
            'christmasstarpart': 'xmasstarparts',
            'christmasstarparts': 'xmasstarparts',
            'starpart': 'xmasstarparts',
            'starparts': 'xmasstarparts',
            'gingerbreads': 'gingerbread',
            'ornaments': 'ornament',
            'ornamentparts': 'ornamentpart',
            'presents': 'present',
            'commonpresent': 'present',
            'commonpresents': 'present',
            'normalpresent': 'present',
            'normalpresents': 'present',
            'pineneedles': 'pineneedle',
            'pine': 'pineneedle',
            'needle': 'pineneedle',
            'needles': 'pineneedle',
            'sleepypotions': 'sleepypotion',
            'potion': 'sleepypotion',
            'potions': 'sleepypotion',
            'sleepy': 'sleepypotion',
            'snowboxes': 'snowbox',
            'box': 'snowbox',
            'boxes': 'snowbox',
            'snow': 'snowball',
            'leaves': 'hollyleaves',
            'holly': 'hollyleaves',
            'hollyleave': 'hollyleaves',
            'cookies': 'cookiesandmilk',
            'milk': 'cookiesandmilk',
            'cookie': 'cookiesandmilk',
            'cookieandmilk': 'cookiesandmilk',
            'flake': 'snowflake',
            'key': 'xmaskey',
            'christmaskey': 'xmaskey',
            'dungeonkey': 'xmaskey',
            'cake': 'fruitcake',
            'fruit': 'fruitcake',
        }

        if args:
            arg_full = ''
            for arg in args:
                arg = arg.lower()
                arg_full = f'{arg_full}{arg}'

            if arg_full.replace('item','').replace('items','') in item_name_replacements:
                arg_full = item_name_replacements[arg_full.replace('item','').replace('items','')]

            if arg_full.replace('item','').replace('items','') in items:
                embed = await embed_xmas_item(ctx.prefix, arg_full.replace('item','').replace('items',''))
                await ctx.send(embed=embed)
                return
            elif arg_full.find('item') > -1:
                embed = await embed_xmas_item_overview(ctx.prefix)
                await ctx.send(embed=embed)
                return
            elif arg_full.find('area') > -1:
                embed = await embed_xmas_area(ctx.prefix)
                await ctx.send(embed=embed)
                return
            else:
                embed = await embed_xmas_overview(ctx.prefix)
                await ctx.send(embed=embed)
        else:
            invoked = ctx.invoked_with
            invoked = invoked.lower().replace(ctx.prefix,'')
            if invoked in ('a0','area0'):
                embed = await embed_xmas_area(ctx.prefix)
                await ctx.send(embed=embed)
                return
            else:
                embed = await embed_xmas_overview(ctx.prefix)
                await ctx.send(embed=embed)

# Initialization
def setup(bot):
    bot.add_cog(xmasCog(bot))


# --- Redundancies ---
# Additional guides
guide_items =       '`{prefix}xmas items` : List of all christmas items'
guide_area =        '`{prefix}xmas area` : Christmas area (area 0)'
guide_snowball =    '`{prefix}snowball` : Snowball fight event'
guide_tree =        '`rpg xmas tree` : Christmas tree guide'
guide_presents =    '`rpg xmas presents` : Presents contents and rarity'

# Footer
xmas_footer =       'Use {prefix}xmas to see all available christmas guides'


# --- Functions ---
# All christmas items
async def function_xmas_get_item(prefix,item):

    xmas_items = {
        'candycane': (
            f'CANDY CANE {emojis.CANDY_CANE}',
            f'{emojis.BP} Lets you skip to the next area without doing the dungeon\n'
            f'{emojis.BP} Does **not** let you skip your last dungeon (e.g. D11 in {emojis.TIME_TRAVEL} TT 1)\n'
            f'{emojis.BP} Also rewards some {emojis.SNOWBALL} snowballs when used\n'
            f'{emojis.BP} Mythic loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.BP} You can get some in the advent calendar (`rpg xmas calendar`)\n'
            f'{emojis.BP} Random reward from the christmas dungeon (see `rpg xmas info dungeon`)'
        ),
        'xmashat': (
            f'CHRISTMAS HAT {emojis.XMAS_HAT}',
            f'{emojis.BP} Spawns a snowball fight event when used (see `{prefix}snowball`)\n'
            f'{emojis.BP} The event gives higher rewards than normal when triggered with a hat\n'
            f'{emojis.BP} Mythic loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.BP} Random reward from the christmas dungeon (see `rpg xmas info dungeon`)'
        ),
        'xmaskey': (
            f'CHRISTMAS KEY {emojis.CANDY_KEY}',
            f'{emojis.BP} Required to enter the christmas dungeon in area 0 (see `rpg xmas info dungeon`)\n'
            f'{emojis.BP} Can be crafted (see `rpg xmas recipes`)\n'
            f'{emojis.BP} You need a dungeon key to craft this item. A TIME key also works.\n'
            f'{emojis.BP} Dungeon keys are consumed when crafting, the TIME key is not.\n'
            f'{emojis.BP} Note that you can **not** buy a dungeon key if you are in A15 and in TT10-24. In this case you '
            f'have to time travel to be able to craft a christmas key.'
        ),
        'xmasstar': (
            f'CHRISTMAS STAR {emojis.XMAS_STAR}',
            f'{emojis.BP} Used to decorate the tree (see `rpg xmas tree`)\n'
            f'{emojis.BP} Needs to be crafted (see `rpg xmas recipes`)'
        ),
        'xmasstarparts': (
            f'CHRISTMAS STAR PARTS {emojis.XMAS_STAR_PART_1}{emojis.XMAS_STAR_PART_2}{emojis.XMAS_STAR_PART_3}{emojis.XMAS_STAR_PART_4}{emojis.XMAS_STAR_PART_5}',
            f'{emojis.BP} Used to craft the {emojis.XMAS_STAR} christmas star\n'
            f'{emojis.BP} You can get 1 each by completing the quests (see `rpg xmas quests`)'
        ),
        'cookiesandmilk': (
            f'COOKIES AND MILK {emojis.COOKIES_AND_MILK}',
            f'{emojis.BP} Randomly resets command cooldowns (shorter ones have a higher chance)\n'
            f'{emojis.BP} Can be crafted (see `rpg xmas recipes`)'
        ),
        'fruitcake': (
            f'FRUIT CAKE {emojis.FRUIT_CAKE}',
            f'{emojis.BP} Activates a world buff (30% chance to get double the snowballs in `arena` for 45min)\n'
            f'{emojis.BP} Can be crafted (see `rpg xmas recipes`)'
        ),
        'gingerbread': (
            f'GINGERBREAD {emojis.GINGERBREAD}',
            f'{emojis.BP} Teleports you to the christmas area when used (see `{prefix}xmas area`)\n'
            f'{emojis.BP} Used to buy items in the shop (`rpg xmas shop`)\n'
            f'{emojis.BP} Mythic loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.BP} You can get some in the advent calendar (`rpg xmas calendar`)'
        ),
        'hollyleaves': (
            f'HOLLY LEAVES {emojis.HOLLY_LEAVES}',
            f'{emojis.BP} Used to join in the world boss fight (see `rpg xmas wb`)\n'
            f'{emojis.BP} Drops from `adventure`'
        ),
        'ornament': (
            f'ORNAMENT {emojis.ORNAMENT}',
            f'{emojis.BP} Used to decorate the tree (see `rpg xmas tree`)\n'
            f'{emojis.BP} Drops from `adventure`, `training` and rarely other commands\n'
            f'{emojis.BP} Can be crafted (see `rpg xmas recipes`)\n'
            f'{emojis.BP} Rare loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.BP} You can get some in the advent calendar (`rpg xmas calendar`)'
        ),
        'ornamentpart': (
            f'ORNAMENT PART{emojis.ORNAMENT_PART}',
            f'{emojis.BP} Used to craft {emojis.ORNAMENT} ornaments (see `rpg xmas recipes`)\n'
            f'{emojis.BP} Uncommon loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.BP} Random reward in the snowball fight event (see `{prefix}event snowball`)\n'
            f'{emojis.BP} You can get some in the advent calendar (`rpg xmas calendar`)'
        ),
        'present': (
            f'PRESENT {emojis.PRESENT}{emojis.PRESENT_EPIC}{emojis.PRESENT_MEGA}{emojis.PRESENT_ULTRA}{emojis.PRESENT_OMEGA}{emojis.PRESENT_GODLY}',
            f'{emojis.BP} Can be crafted into better presents (see `rpg xmas recipes`)\n'
            f'{emojis.BP} Drops from `rpg hunt`, `adventure`, `training`, `fish`, `duel`, `quest`, `epic quest`, `horse breeding`, `horse race`, `arena`, `miniboss`, `dungeon` (including all higher command tiers)\n'
            f'{emojis.BP} Can be opened to get loot (see `rpg xmas presents`)\n'
            f'{emojis.BP} You can get some in the advent calendar (`rpg xmas calendar`)\n'
            f'{emojis.BP} Can be gambled with `rpg xmas slots`\n'
        ),
        'pineneedle': (
            f'PINE NEEDLE {emojis.PINE_NEEDLE}',
            f'{emojis.BP} Used to decorate the tree (see `rpg xmas tree`)\n'
            f'{emojis.BP} Drops from `adventure`, `training`\n'
            f'{emojis.BP} Uncommon loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.BP} Random reward in the snowball fight event (see `{prefix}event snowball`)\n'
            f'{emojis.BP} You can get some in the advent calendar (`rpg xmas calendar`)'
        ),
        'sleepypotion': (
            f'SLEEPY POTION {emojis.SLEEPY_POTION}',
            f'{emojis.BP} Reduces all cooldowns by 24h when used\n'
            f'{emojis.BP} Mythic loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.BP} You can get some in the advent calendar (`rpg xmas calendar`)\n'
            f'{emojis.BP} Random reward from the christmas dungeon (see `rpg xmas info dungeon`)'
        ),
        'snowball': (
            f'SNOWBALL {emojis.SNOWBALL}',
            f'{emojis.BP} Used in various recipes (see `rpg xmas recipes`)\n'
            f'{emojis.BP} Drops from `hunt`, `adventure`, `training`, `fish`, `duel`, `quest`, `epic quest`, `horse breeding`, `horse race`, `arena`, `miniboss`, `dungeon` (including all higher command tiers)\n'
            f'{emojis.BP} Contained in {emojis.SNOW_BOX} snow boxes bought from the shop (`rpg xmas shop`)\n'
            f'{emojis.BP} Common loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.BP} You get some when using a {emojis.CANDY_CANE} candy cane\n'
            f'{emojis.BP} Random reward in the snowball fight event (see `{prefix}event snowball`)\n'
            f'{emojis.BP} You can get some in the advent calendar (`rpg xmas calendar`)'
        ),
        'snowbox': (
            f'SNOW BOX {emojis.SNOW_BOX}',
            f'{emojis.BP} Can be opened to get 2 - 20 {emojis.SNOWBALL} snowballs\n'
            f'{emojis.BP} Can be bought in the shop for 35 {emojis.SNOWFLAKE} (`rpg xmas shop`)\n'
            f'{emojis.BP} Rare loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.BP} You can get 4 by completing a quest (see `rpg xmas quests`)'
        ),
        'snowflake': (
            f'SNOWFLAKE {emojis.SNOWFLAKE}',
            f'{emojis.BP} Used to buy items in the shop (see `rpg xmas shop`)\n'
            f'{emojis.BP} Reward for completing tasks (see `rpg xmas tasks`)\n'
            f'{emojis.BP} Common loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.BP} You can get 1,000 by completing a quest (see `rpg xmas quests`)'
        )
    }


    if item == 'all':
        items = []
        for item in xmas_items:
            items.append(xmas_items[item])
    else:
        items = []
        if item in xmas_items:
            items.append(xmas_items[item])

    return items


# --- Embeds ---
# Christmas overview
async def embed_xmas_overview(prefix):

    whattodo = (
        f'{emojis.BP} Complete daily and weekly **tasks** (`rpg xmas tasks`)\n'
        f'{emojis.BP} Decorate a christmas **tree** to get a {emojis.PET_SNOWBALL} pet (see `rpg xmas tree`)\n'
        #f'{emojis.BP} **Recycle** your leftover materials (see `rpg xmas recycle`)\n'
        f'{emojis.BP} Craft **items** (see `{prefix}xmas items`)\n'
        f'{emojis.BP} Find, craft and open **presents** (see `{prefix}xmas presents`)\n'
        f'{emojis.BP} Defeat the **christmas slime** in `rpg hunt` (drops 100 presents)\n'
        f'{emojis.BP} Visit the **christmas area** (area 0) (see `{prefix}xmas area`)\n'
        f'{emojis.BP} Beat the candy dragon in the **christmas dungeon** in area 0 (see `rpg xmas info dungeon`)\n'
        f'{emojis.BP} Complete the christmas **quests** (see `rpg xmas quests`)\n'
        f'{emojis.BP} Buy various rewards in the **shop** (`rpg xmas shop`)\n'
        f'{emojis.BP} Open a door in your **advent calendar** every day (`rpg xmas calendar`)\n'
        f'{emojis.BP} Encounter the **snowball fight event** (see `{prefix}snowball`)\n'
        f'{emojis.BP} Gamble all your presents away with `rpg xmas slots`'
    )

    bonuses = (
        f'{emojis.BP} Arena cooldown is lowered to 12h\n'
        f'{emojis.BP} Double XP when eating {emojis.ARENA_COOKIE} arena cookies (**not** super cookies!)\n'
        f'{emojis.DETAIL} Note that even at double XP 1 super cookie is still worth more than 1000 cookies\n'
    )

    guide = (
        f'{emojis.BP} Complete your tasks daily / weekly in `rpg xmas tasks`\n'
        f'{emojis.BP} Check `rpg xmas calendar` daily\n'
        f'{emojis.BP} Use your presents according to `{prefix}xmas presents`\n'
        f'{emojis.BP} Beat the christmas dungeon at least twice for the quest\n'
        f'{emojis.BP} Complete the christmas quests in `rpg xmas quests` (do the quest that tasks you to open 600 presents last)\n'
        f'{emojis.BP} Complete the tree in `rpg xmas tree` before december 25th\n'
        f'{emojis.BP} Buy whatever you want from the shop in `rpg xmas shop`\n'
    )

    present = (
        f'{emojis.BP} {emojis.PRESENT} Common present: Use in the shop or craft into EPIC\n'
        f'{emojis.BP} {emojis.PRESENT_EPIC} EPIC present: Craft into MEGA\n'
        f'{emojis.BP} {emojis.PRESENT_MEGA} MEGA present: Open\n'
        f'{emojis.BP} {emojis.PRESENT_ULTRA} ULTRA present: Craft into OMEGA if you need mythic items or a christmas key, otherwise open\n'
        f'{emojis.BP} {emojis.PRESENT_OMEGA} OMEGA present: Craft into GODLY if you need mythic items or a christmas key, otherwise open\n'
        f'{emojis.BP} {emojis.PRESENT_GODLY} GODLY present: Use for christmas key if needed, otherwise open'
    )

    schedule = (
        f'{emojis.BP} Event starts on December 1, 2021\n'
        f'{emojis.BP} World boss fight starts on December 8, 2021\n'
        f'{emojis.BP} You stop getting items on January 5, 2022, 23:55 UTC\n'
        f'{emojis.BP} All leftover items will be deleted on January 12, 2021'
    )

    guides = (
        f'{emojis.BP} {guide_items.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_area.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_snowball.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_tree.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_presents.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CHRISTMAS EVENT 2021',
        description = 'Time to decorate.'
    )

    embed.add_field(name='TL;DR GUIDE', value=guide, inline=False)
    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='ALL ACTIVITIES', value=whattodo, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    #embed.add_field(name='WHAT TO DO WITH PRESENTS', value=present, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)

    return embed

# Look up christmas items
async def embed_xmas_item(prefix, item):

    items = await function_xmas_get_item(prefix,item)

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CHRISTMAS ITEMS',
    )

    embed.set_footer(text=f'{xmas_footer.format(prefix=prefix)}')

    present_extra = (
        f'{emojis.BP} {emojis.PRESENT} Common present: Craft into EPIC\n'
        f'{emojis.BP} {emojis.PRESENT_EPIC} EPIC present: Craft into MEGA\n'
        f'{emojis.BP} {emojis.PRESENT_MEGA} MEGA present: Open\n'
        f'{emojis.BP} {emojis.PRESENT_ULTRA} ULTRA present: Craft into OMEGA if you need mythic items or a christmas key, otherwise open\n'
        f'{emojis.BP} {emojis.PRESENT_OMEGA} OMEGA present: Craft into GODLY if you need mythic items or a christmas key, otherwise open\n'
        f'{emojis.BP} {emojis.PRESENT_GODLY} GODLY present: Use for christmas key if needed (you need at least 2 for the quest), otherwise open'
    )

    for item in items:
        embed.add_field(name=item[0], value=item[1], inline=False)
        if item[0].find('present') > -1:
            embed.add_field(name='WHAT TO DO WITH PRESENTS', value=present_extra, inline=False)

    return embed

# Christmas items overview
async def embed_xmas_item_overview(prefix):

    items = [
        'candy cane',
        'hat',
        'star',
        'star parts',
        'gingerbread',
        'ornament',
        'ornament part',
        'present',
        'pine needle',
        'sleepy potion',
        'snowball',
        'snow box',
        'snowflake',
        'holly leaves',
        'christmas key',
        'cookies and milk',
        'fruit cake'
    ]
    items = sorted(items)

    items_value = ''

    for item in items:
        items_value = f'{items_value}\n{emojis.BP} `{item}`'
    items_value.strip()

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CHRISTMAS ITEMS OVERVIEW',
        description = (
            f'This page lists the names of all christmas items.\n'
            f'Use `{prefix}xmas [item name]` to see details about an item.'
        )

    )

    embed.set_footer(text=f'{xmas_footer.format(prefix=prefix)}')

    embed.add_field(name='ITEM NAMES', value=items_value, inline=False)

    return embed

# Christmas area
async def embed_xmas_area(prefix):

    requirements = (
        f'{emojis.BP} Can only be reached by eating a {emojis.GINGERBREAD} gingerbread\n'
        f'{emojis.BP} You can get {emojis.GINGERBREAD} gingerbread from weekly tasks and presents (see `rpg xmas presents`)\n'
        f'{emojis.BP} Can be left anytime but accessing it again requires another {emojis.GINGERBREAD} gingerbread'
    )

    differences = (
        f'{emojis.BP} You get 2 christmas items ({emojis.SNOWBALL} or {emojis.PRESENT}) when using `hunt` or `adventure`\n'
        f'{emojis.BP} You get normal mob drops in `hunt` according to your **max** area\n'
        f'{emojis.BP} You do not get XP and coins from `hunt` and `adventure`\n'
        f'{emojis.BP} You do not get any items from `fish` commands\n'
        f'{emojis.BP} You get double the worker XP from `chop` commands\n'
        f'{emojis.BP} You get access to the christmas dungeon (see `rpg xmas info dungeon`)\n'
        f'{emojis.BP} You do not take damage from mobs in this area (you do take minimal general damage in `hunt` and '
        f'`adventure` because of the heal quest but no damage in `hunt together`)\n'
    )

    xmas_drops = (
        f'{emojis.BP} `hunt`: {emojis.PRESENT} presents, ???\n'
        f'{emojis.BP} `adventure`: {emojis.PRESENT} presents, {emojis.PINE_NEEDLE} pine needle, ???'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CHRISTMAS AREA (AREA 0)',
        description = 'This is a special christmas themed area that will only be accessible during the christmas event.'

    )

    embed.set_footer(text=f'{xmas_footer.format(prefix=prefix)}')
    embed.add_field(name='HOW TO ACCESS', value=requirements, inline=False)
    embed.add_field(name='DIFFERENCES TO NORMAL AREAS', value=differences, inline=False)

    return embed