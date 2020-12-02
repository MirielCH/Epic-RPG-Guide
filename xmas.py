# xmas.py (2020)

import discord
import emojis
import global_data

# Christmas overview
async def xmas_overview(prefix):

    whattodo =      f'{emojis.bp} Decorate a {emojis.xmastree} christmas **tree** to get a {emojis.petsnowball} pet (see `rpg xmas tree`)\n'\
                    f'{emojis.bp} Find, craft and use **items and presents** (see `{prefix}xmas items`)\n'\
                    f'{emojis.bp} Defeat the {emojis.xmasslime} **christmas slime** in `rpg hunt` (drops 100 {emojis.present} presents)\n'\
                    f'{emojis.bp} Visit the **christmas area** (area 0) (see `{prefix}xmas area`)\n'\
                    f'{emojis.bp} Complete christmas **quests** (see `rpg xmas quests`)\n'\
                    f'{emojis.bp} Buy various rewards in the **shop** (`rpg xmas shop`)\n'\
                    f'{emojis.bp} Open a door in your **advent calendar** every day (`rpg xmas calendar`)\n'\
                    f'{emojis.bp} Defeat the EPIC NPC in a new random **snowball fight event** (see `{prefix}snowball`)\n'\
                    f'{emojis.bp} Defeat a unique **world boss** in the [official server](https://discord.gg/epicrpg) (Dec 25)\n'\
                    f'{emojis.bp} Gamble all your presents away with `rpg xmas slots`'

    bonuses =       f'{emojis.bp} 2x XP when eating {emojis.arenacookie} arena cookies\n'\
                    f'{emojis.bp} Arena cooldown is lowered to 12h'

    schedule =      f'{emojis.bp} Event starts on December 1, 2020\n'\
                    f'{emojis.bp} Event ends on January 4, 2021, 20:00 UTC'
                
    guides =        f'{emojis.bp} `{prefix}xmas items` : List of all christmas items\n'\
                    f'{emojis.bp} `{prefix}xmas area` : Christmas area (area 0)\n'\
                    f'{emojis.bp} `{prefix}snowball` : Snowball fight event\n'\
                    f'{emojis.bp} `rpg xmas tree` : Christmas tree guide\n'\
                    f'{emojis.bp} `rpg xmas presents` : Presents contents and rarity'

    embed = discord.Embed(
        color = global_data.color,
        title = f'CHRISTMAS EVENT 2020',
        description =   f'Time to decorate.'
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))

    embed.add_field(name=f'ACTIVITIES', value=whattodo, inline=False)
    embed.add_field(name=f'BONUSES', value=bonuses, inline=False)
    embed.add_field(name=f'GUIDES', value=guides, inline=False)
    embed.add_field(name=f'EVENT SCHEDULE', value=schedule, inline=False)
            
    return embed

# All christmas items
async def xmas_get_item(prefix,item):
    
    xmas_items = {
        'candycane':            (f'CANDY CANE {emojis.candycane}',
                                f'{emojis.bp} Lets you skip to the next area without doing the dungeon\n'\
                                f'{emojis.bp} Does **not** let you skip your last dungeon (e.g. D11 in {emojis.timetravel} TT 1)\n'\
                                f'{emojis.bp} Also rewards some {emojis.snow} snow when used\n'\
                                f'{emojis.bp} Mythic loot from presents (see `rpg xmas presents`)\n'\
                                f'{emojis.bp} You can get 2 in the advent calendar (`rpg xmas calendar`)'),
        'xmashat':              (f'CHRISTMAS HAT {emojis.xmashat}',
                                f'{emojis.bp} Spawns a snowball fight event when used (see `{prefix}snowball`)\n'\
                                f'{emojis.bp} The event gives higher rewards than normal when triggered with a hat\n'\
                                f'{emojis.bp} Mythic loot from presents (see `rpg xmas presents`)'),
        'xmasstar':             (f'CHRISTMAS STAR {emojis.xmasstar}',
                                f'{emojis.bp} Used to decorate the tree (see `{prefix}xmas tree`)\n'\
                                f'{emojis.bp} Needs to be crafted (see `rpg xmas recipes`)'),
        'xmasstarparts':        (f'CHRISTMAS STAR PARTS {emojis.xmasstarpart1}{emojis.xmasstarpart2}{emojis.xmasstarpart3}{emojis.xmasstarpart4}{emojis.xmasstarpart5}',
                                f'{emojis.bp} Used to craft the {emojis.xmasstar} christmas star\n'\
                                f'{emojis.bp} You can get 1 each by completing the quests (see `rpg xmas quests`)'),
        'gingerbread':          (f'GINGERBREAD {emojis.gingerbread}',
                                f'{emojis.bp} Teleports you to the christmas area when used (see `{prefix}xmas area`)\n'\
                                f'{emojis.bp} Used to buy the profile background in the shop (`rpg xmas shop`)\n'\
                                f'{emojis.bp} Mythic loot from presents (see `rpg xmas presents`)'),
        'ornament':             (f'ORNAMENT {emojis.ornament}',
                                f'{emojis.bp} Used to decorate the tree (see `{prefix}xmas tree`)\n'\
                                f'{emojis.bp} Can be crafted (see `rpg xmas recipes`)\n'\
                                f'{emojis.bp} Rare loot from presents (see `rpg xmas presents`)\n'\
                                f'{emojis.bp} You can get 1 in the advent calendar (`rpg xmas calendar`)'),
        'ornamentpart':         (f'ORNAMENT PART{emojis.ornamentpart}',
                                f'{emojis.bp} Used to craft {emojis.ornament} ornaments (see `rpg xmas recipes`)\n'\
                                f'{emojis.bp} Uncommon loot from presents (see `rpg xmas presents`)\n'\
                                f'{emojis.bp} You can get 1 in the advent calendar (`rpg xmas calendar`)'),
        'present':              (f'PRESENT {emojis.present}',
                                f'{emojis.bp} Used to buy items in the shop (`rpg xmas shop`)\n'\
                                f'{emojis.bp} Can be crafted into better presents (see `rpg xmas recipes`)\n'\
                                f'{emojis.bp} Can be opened to get some loot (see `rpg xmas presents`)\n'\
                                f'{emojis.bp} Only open normal presents for the quest, always craft better ones after that\n'\
                                f'{emojis.bp} Drops from `rpg hunt`, `adventure`, `training`, `fish`, `duel`, `quest`, `epic quest`, `horse breeding`, `horse race`, `arena`, `miniboss`, `dungeon` (including all higher command tiers)'),
        'pineneedle':           (f'PINE NEEDLE {emojis.pineneedle}',
                                f'{emojis.bp} Used to decorate the tree (see `{prefix}xmas tree`)\n'\
                                f'{emojis.bp} Drops from `rpg adventure`, `training`\n'\
                                f'{emojis.bp} Uncommon loot from presents (see `rpg xmas presents`)\n'\
                                f'{emojis.bp} You can get 2 in the advent calendar (`rpg xmas calendar`)'),
        'sleepypotion':         (f'SLEEPY POTION {emojis.sleepypotion}',
                                f'{emojis.bp} Reduces all cooldowns by 24h when used\n'\
                                f'{emojis.bp} Mythic loot from presents (see `rpg xmas presents`)\n'\
                                f'{emojis.bp} You can get 2 in the advent calendar (`rpg xmas calendar`)'),
        'snow':                 (f'SNOW {emojis.snow}',
                                f'{emojis.bp} Used in various recipes (see `rpg xmas recipes`)\n'\
                                f'{emojis.bp} Drops from `rpg hunt`, `adventure`, `training`, `fish`, `duel`, `quest`, `epic quest`, `horse breeding`, `horse race`, `arena`, `miniboss`, `dungeon` (including all higher command tiers)\n'\
                                f'{emojis.bp} Contained in {emojis.snowbox} snow boxes bought from the shop (`rpg xmas shop`)\n'\
                                f'{emojis.bp} Common loot from presents (see `rpg xmas presents`)\n'\
                                f'{emojis.bp} You get some snow when using a {emojis.candycane} candy cane\n'\
                                f'{emojis.bp} You can get 2 in the advent calendar (`rpg xmas calendar`)'),
        'snowbox':              (f'SNOW BOX {emojis.snowbox}',
                                 f'{emojis.bp} Can be opened to get 2-20 {emojis.snow} snow\n'\
                                f'{emojis.bp} Can be bought in the shop for 15 {emojis.present} (`rpg xmas shop`)\n'\
                                f'{emojis.bp} Rare loot from presents (see `rpg xmas presents`)\n'\
                                f'{emojis.bp} You can get 2 by completing a quest (see `rpg xmas quests`)')       
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

# Look up christmas items
async def xmas_item(prefix, item):
    
    items = await xmas_get_item(prefix,item)
    
    embed = discord.Embed(
        color = global_data.color,
        title = f'CHRISTMAS ITEMS',
                      
    )    
    embed.set_footer(text=f'Use {prefix}xmas to see a christmas overview')

    for item in items:
        embed.add_field(name=item[0], value=item[1], inline=False)
            
    return embed

# Christmas items overview
async def xmas_item_overview(prefix):
    
    items = ['candy cane','hat','star','star parts','gingerbread','ornament','ornament part','present','pine needle','sleepy potion','snow','snow box']
    items = sorted(items)
    
    items_value = ''
    
    for item in items:
        items_value = f'{items_value}\n{emojis.bp} `{item}`'
    items_value.strip()
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'CHRISTMAS ITEMS OVERVIEW',
        description =   f'This page lists the names of all christmas items.\n'\
                        f'Use `{prefix}xmas [item name]` to see details about an item.\n'\
                        f'Tip: You can use `{prefix}xmas all` to see all items at once.'
                      
    )    
    embed.set_footer(text=f'Use {prefix}xmas to see all available christmas guides')
    embed.add_field(name='ITEM NAMES', value=items_value, inline=False)
            
    return embed

# Christmas area
async def xmas_area(prefix):
    
    requirements =      f'{emojis.bp} Can only be reached by eating a {emojis.gingerbread} gingerbread\n'\
                        f'{emojis.bp} {emojis.gingerbread} Gingerbread is a mythic drop from presents (see `rpg xmas presents`)\n'\
                        f'{emojis.bp} Can be left anytime but accessing it again requires another {emojis.gingerbread} gingerbread'
                        
    differences =       f'{emojis.bp} You get 2 christmas items ({emojis.snow} or {emojis.present}) when using `hunt` or `adventure`\n'\
                        f'{emojis.bp} You get normal mob drops in `hunt` according to your **max** area\n'\
                        f'{emojis.bp} You take damage according do your **max** area\n'\
                        f'{emojis.bp} You do not get XP and coins from `hunt` and `adventure`\n'\
                        f'{emojis.bp} You do not get any items from `fish` commands\n'\
                        f'{emojis.bp} You get double the worker XP from `chop` commands'
                        
    xmas_drops =        f'{emojis.bp} `hunt`: {emojis.present} presents, ???\n'\
                        f'{emojis.bp} `adventure`: {emojis.present} presents, {emojis.pineneedle} pine needle, ???\n'\
    
    
    
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'CHRISTMAS AREA (AREA 0)',
        description =   f'This is a special christmas themed area that will only be accessible during the christmas event.'
                      
    )    
    embed.set_footer(text=f'Use {prefix}xmas to see all available christmas guides')
    embed.add_field(name='HOW TO ACCESS', value=requirements, inline=False)
    embed.add_field(name='DIFFERENCES TO NORMAL AREAS', value=differences, inline=False)
    #embed.add_field(name='CHRISTMAS DROPS', value=xmas_drops, inline=False)
            
    return embed