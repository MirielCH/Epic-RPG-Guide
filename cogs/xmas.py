# xmas.py

import discord
import emojis
import global_data

from discord.ext import commands

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
        items = ['candycane','xmashat','xmasstar','xmasstarparts','gingerbread','ornament','ornamentpart','present','pineneedle','sleepypotion','snow','snowbox','all']
    
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
        }

        if args:
            arg_full = ''
            for arg in args:
                arg = arg.lower()
                arg_full = f'{arg_full}{arg}'
            
            if arg_full.find('item') > -1:
                embed = await embed_xmas_item_overview(ctx.prefix)
                await ctx.send(embed=embed)
                return
            elif arg_full.find('area') > -1:
                embed = await embed_xmas_area(ctx.prefix)
                await ctx.send(embed=embed)
                return
            
            if arg_full in item_name_replacements:
                arg_full = item_name_replacements[arg_full]
            
            if arg_full in items:
                embed = await embed_xmas_item(ctx.prefix, arg_full)
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
            f'CANDY CANE {emojis.candycane}',
            f'{emojis.bp} Lets you skip to the next area without doing the dungeon\n'
            f'{emojis.bp} Does **not** let you skip your last dungeon (e.g. D11 in {emojis.timetravel} TT 1)\n'
            f'{emojis.bp} Also rewards some {emojis.snow} snow when used\n'
            f'{emojis.bp} Mythic loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.bp} You can get some in the advent calendar (`rpg xmas calendar`)'
        ),
        'xmashat': (
            f'CHRISTMAS HAT {emojis.xmashat}',
            f'{emojis.bp} Spawns a snowball fight event when used (see `{prefix}snowball`)\n'
            f'{emojis.bp} The event gives higher rewards than normal when triggered with a hat\n'
            f'{emojis.bp} Mythic loot from presents (see `rpg xmas presents`)'
        ),
        'xmasstar': (
            f'CHRISTMAS STAR {emojis.xmasstar}',
            f'{emojis.bp} Used to decorate the tree (see `{prefix}xmas tree`)\n'
            f'{emojis.bp} Needs to be crafted (see `rpg xmas recipes`)'
        ),
        'xmasstarparts': (
            f'CHRISTMAS STAR PARTS {emojis.xmasstarpart1}{emojis.xmasstarpart2}{emojis.xmasstarpart3}{emojis.xmasstarpart4}{emojis.xmasstarpart5}',
            f'{emojis.bp} Used to craft the {emojis.xmasstar} christmas star\n'
            f'{emojis.bp} You can get 1 each by completing the quests (see `rpg xmas quests`)'
        ),
        'gingerbread': (
            f'GINGERBREAD {emojis.gingerbread}',
            f'{emojis.bp} Teleports you to the christmas area when used (see `{prefix}xmas area`)\n'
            f'{emojis.bp} Used to buy the profile background in the shop (`rpg xmas shop`)\n'
            f'{emojis.bp} Mythic loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.bp} You can get 1 in the advent calendar (`rpg xmas calendar`)'
        ),
        'ornament': (
            f'ORNAMENT {emojis.ornament}',
            f'{emojis.bp} Used to decorate the tree (see `{prefix}xmas tree`)\n'
            f'{emojis.bp} Can be crafted (see `rpg xmas recipes`)\n'
            f'{emojis.bp} Rare loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.bp} You can get some in the advent calendar (`rpg xmas calendar`)'
        ),
        'ornamentpart': (
            f'ORNAMENT PART{emojis.ornamentpart}',
            f'{emojis.bp} Used to craft {emojis.ornament} ornaments (see `rpg xmas recipes`)\n'
            f'{emojis.bp} Uncommon loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.bp} You can get 1 in the advent calendar (`rpg xmas calendar`)'
        ),
        'present': (
            f'PRESENT {emojis.present}{emojis.presentepic}{emojis.presentmega}{emojis.presentultra}{emojis.presentomega}{emojis.presentgodly}',
            f'{emojis.bp} Used to buy items in the shop (`rpg xmas shop`)\n'
            f'{emojis.bp} Can be crafted into better presents (see `rpg xmas recipes`)\n'
            f'{emojis.bp} Can be opened to get some loot (see `rpg xmas presents`)\n'
            f'{emojis.bp} You can get some in the advent calendar (`rpg xmas calendar`)\n'
            f'{emojis.bp} Drops from `rpg hunt`, `adventure`, `training`, `fish`, `duel`, `quest`, `epic quest`, `horse breeding`, `horse race`, `arena`, `miniboss`, `dungeon` (including all higher command tiers)'
        ),
        'pineneedle': (
            f'PINE NEEDLE {emojis.pineneedle}',
            f'{emojis.bp} Used to decorate the tree (see `{prefix}xmas tree`)\n'
            f'{emojis.bp} Drops from `rpg adventure`, `training`\n'
            f'{emojis.bp} Uncommon loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.bp} You can get some in the advent calendar (`rpg xmas calendar`)'
        ),
        'sleepypotion': (
            f'SLEEPY POTION {emojis.sleepypotion}',
            f'{emojis.bp} Reduces all cooldowns by 24h when used\n'
            f'{emojis.bp} Mythic loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.bp} You can get some in the advent calendar (`rpg xmas calendar`)'
        ),
        'snow': (
            f'SNOW {emojis.snow}',
            f'{emojis.bp} Used in various recipes (see `rpg xmas recipes`)\n'
            f'{emojis.bp} Drops from `rpg hunt`, `adventure`, `training`, `fish`, `duel`, `quest`, `epic quest`, `horse breeding`, `horse race`, `arena`, `miniboss`, `dungeon` (including all higher command tiers)\n'
            f'{emojis.bp} Contained in {emojis.snowbox} snow boxes bought from the shop (`rpg xmas shop`)\n'
            f'{emojis.bp} Common loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.bp} You get some snow when using a {emojis.candycane} candy cane\n'
            f'{emojis.bp} You can get some in the advent calendar (`rpg xmas calendar`)'
        ),
        'snowbox': (
            f'SNOW BOX {emojis.snowbox}',
            f'{emojis.bp} Can be opened to get 2-20 {emojis.snow} snow\n'
            f'{emojis.bp} Can be bought in the shop for 15 {emojis.present} (`rpg xmas shop`)\n'
            f'{emojis.bp} Rare loot from presents (see `rpg xmas presents`)\n'
            f'{emojis.bp} You can get 2 by completing a quest (see `rpg xmas quests`)'
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
        f'{emojis.bp} Decorate a {emojis.xmastree} christmas **tree** to get a {emojis.petsnowball} pet (see `rpg xmas tree`)\n'
        f'{emojis.bp} **Recycle** your leftover materials (see `rpg xmas recycle`)\n'
        f'{emojis.bp} Find, craft and use **items and presents** (see `{prefix}xmas items`)\n'
        f'{emojis.bp} Defeat the {emojis.xmasslime} **christmas slime** in `rpg hunt` (drops 100 {emojis.present} presents)\n'
        f'{emojis.bp} Visit the **christmas area** (area 0) (see `{prefix}xmas area`)\n'
        f'{emojis.bp} Complete christmas **quests** (see `rpg xmas quests`)\n'
        f'{emojis.bp} Buy various rewards in the **shop** (`rpg xmas shop`)\n'
        f'{emojis.bp} Open a door in your **advent calendar** every day (`rpg xmas calendar`)\n'
        f'{emojis.bp} Defeat the EPIC NPC in a new random **snowball fight event** (see `{prefix}snowball`)\n'
        f'{emojis.bp} Gamble all your presents away with `rpg xmas slots`'
    )

    bonuses = (
        f'{emojis.bp} 2x XP when eating {emojis.arenacookie} arena cookies\n'
        f'{emojis.bp} Arena cooldown is lowered to 12h'
    )
    
    present = (
        f'{emojis.bp} {emojis.present} Common present: Use in the shop or craft into EPIC\n'
        f'{emojis.bp} {emojis.presentepic} EPIC present: Craft into MEGA\n'
        f'{emojis.bp} {emojis.presentmega} MEGA present: Open it\n'
        f'{emojis.bp} {emojis.presentultra} ULTRA present: Craft into OMEGA\n'
        f'{emojis.bp} {emojis.presentomega} OMEGA present: Craft into GODLY\n'
        f'{emojis.bp} {emojis.presentgodly} GODLY present: Open it'
    )

    schedule = (
        f'{emojis.bp} Event starts on December 1, 2020\n'
        f'{emojis.bp} You stop getting items on January 4, 2021, 20:00 UTC\n'
        f'{emojis.bp} All leftover items will be deleted on January 11, 2021'
    )
                
    guides = (
        f'{emojis.bp} {guide_items.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_area.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_snowball.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_tree.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_presents.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = f'CHRISTMAS EVENT 2020',
        description =   f'Time to decorate.'                    
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'ACTIVITIES', value=whattodo, inline=False)
    embed.add_field(name=f'BONUSES', value=bonuses, inline=False)
    embed.add_field(name=f'WHAT TO DO WITH PRESENTS', value=present, inline=False)
    embed.add_field(name=f'GUIDES', value=guides, inline=False)
    embed.add_field(name=f'EVENT SCHEDULE', value=schedule, inline=False)
            
    return embed

# Look up christmas items
async def embed_xmas_item(prefix, item):
    
    items = await function_xmas_get_item(prefix,item)
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'CHRISTMAS ITEMS',
    )    
    
    embed.set_footer(text=f'{xmas_footer.format(prefix=prefix)}')

    present_extra = (
        f'{emojis.bp} {emojis.present} Common present: Use in the shop or craft into EPIC\n'
        f'{emojis.bp} {emojis.presentepic} EPIC present: Craft into MEGA\n'
        f'{emojis.bp} {emojis.presentmega} MEGA present: Open it\n'
        f'{emojis.bp} {emojis.presentultra} ULTRA present: Craft into OMEGA\n'
        f'{emojis.bp} {emojis.presentomega} OMEGA present: Craft into GODLY\n'
        f'{emojis.bp} {emojis.presentgodly} GODLY present: Open it'
    )

    for item in items:
        embed.add_field(name=item[0], value=item[1], inline=False)
        if item[0].find('present') > -1:
            embed.add_field(name='WHAT TO DO WITH PRESENTS', value=present_extra, inline=False)
    
    return embed

# Christmas items overview
async def embed_xmas_item_overview(prefix):
    
    items = ['candy cane','hat','star','star parts','gingerbread','ornament','ornament part','present','pine needle','sleepy potion','snow','snow box']
    items = sorted(items)
    
    items_value = ''
    
    for item in items:
        items_value = f'{items_value}\n{emojis.bp} `{item}`'
    items_value.strip()
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'CHRISTMAS ITEMS OVERVIEW',
        description = (
            f'This page lists the names of all christmas items.\n'
            f'Use `{prefix}xmas [item name]` to see details about an item.\n'
            f'Tip: You can use `{prefix}xmas all` to see all items at once.'
        )
                      
    )    
    
    embed.set_footer(text=f'{xmas_footer.format(prefix=prefix)}')
    
    embed.add_field(name='ITEM NAMES', value=items_value, inline=False)
            
    return embed

# Christmas area
async def embed_xmas_area(prefix):
    
    requirements = (
        f'{emojis.bp} Can only be reached by eating a {emojis.gingerbread} gingerbread\n'
        f'{emojis.bp} {emojis.gingerbread} Gingerbread is a mythic drop from presents (see `rpg xmas presents`)\n'
        f'{emojis.bp} Can be left anytime but accessing it again requires another {emojis.gingerbread} gingerbread'
    )
                        
    differences = (
        f'{emojis.bp} You get 2 christmas items ({emojis.snow} or {emojis.present}) when using `hunt` or `adventure`\n'
        f'{emojis.bp} You get normal mob drops in `hunt` according to your **max** area\n'
        f'{emojis.bp} You do not take any damage in this area\n'
        f'{emojis.bp} You do not get XP and coins from `hunt` and `adventure`\n'
        f'{emojis.bp} You do not get any items from `fish` commands\n'
        f'{emojis.bp} You get double the worker XP from `chop` commands'
    )
                        
    xmas_drops = (
        f'{emojis.bp} `hunt`: {emojis.present} presents, ???\n'
        f'{emojis.bp} `adventure`: {emojis.present} presents, {emojis.pineneedle} pine needle, ???'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'CHRISTMAS AREA (AREA 0)',
        description = 'This is a special christmas themed area that will only be accessible during the christmas event.'
                      
    )    
    
    embed.set_footer(text=f'{xmas_footer.format(prefix=prefix)}')
    embed.add_field(name='HOW TO ACCESS', value=requirements, inline=False)
    embed.add_field(name='DIFFERENCES TO NORMAL AREAS', value=differences, inline=False)
            
    return embed