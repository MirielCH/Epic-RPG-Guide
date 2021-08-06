# global_data.py

import logging
import logging.handlers
import os

import emojis

# Get bot directory
bot_dir = os.path.dirname(__file__)

# Databases
dbfile = os.path.join(bot_dir, 'database/erg_db.db')
default_dbfile = os.path.join(bot_dir, 'database/erg_db_default.db')

# Pictures
thumbnail = os.path.join(bot_dir, 'images/erg.png')
dungeon11 = os.path.join(bot_dir, 'images/dungeon11.png')
dungeon13 = os.path.join(bot_dir, 'images/dungeon13.png')

# Prefix
default_prefix = '$'

# Embed color
color = 0x8914FF

# Set default footer
async def default_footer(prefix):
    footer = f'Use {prefix}guide or {prefix}g to see all available guides.'

    return footer

# Open error log file, create if it not exists
logfile = os.path.join(bot_dir, 'logs/discord.log')
if not os.path.isfile(logfile):
    open(logfile, 'a').close()

# Initialize logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.handlers.TimedRotatingFileHandler(filename=logfile,when='D',interval=1, encoding='utf-8', utc=True)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#--- Data accessed by multiple cogs ---
item_aliases = {
    'ed sw': 'edgy sword',
    'edgy sw': 'edgy sword',
    'omega sw': 'omega sword',
    'o sw': 'omega sword',
    'ed sword': 'edgy sword',
    'ed armor': 'edgy armor',
    'ue sw': 'ultra-edgy sword',
    'ultra-edgy sw': 'ultra-edgy sword',
    'ue sword': 'ultra-edgy sword',
    'ultra-omega sw': 'ultra-omega sword',
    'ue armor': 'ultra-edgy armor',
    'godly sw': 'godly sword',
    'g sword': 'godly sword',
    'g sw': 'godly sword',
    'unicorn sw': 'unicorn sword',
    'ruby sw': 'ruby sword',
    'fish sw': 'fish sword',
    'apple sw': 'apple sword',
    'zombie sw': 'zombie sword',
    'wooden sw': 'wooden sword',
    'hair sw': 'hair sword',
    'coin sw': 'coin sword',
    'electronical sw': 'electronical sword',
    'f': 'fish',
    'fishes': 'fish',
    'normie fish': 'fish',
    'normiefish': 'fish',
    'normie fishes': 'fish',
    'normiefishes': 'fish',
    'gf': 'golden fish',
    'golden fishes': 'golden fish',
    'goldenfish': 'golden fish',
    'goldenfishes': 'golden fish',
    'ef': 'epic fish',
    'epicfish': 'epic fish',
    'epicfishes': 'epic fish',
    'epic fishes': 'epic fish',
    'brandon': 'epic fish',
    'l': 'log',
    'wood': 'log',
    'logs': 'log',
    'wooden log': 'log',
    'wooden logs': 'log',
    'woodenlog': 'log',
    'woodenlogs': 'log',
    'el': 'epic log',
    'epic logs': 'epic log',
    'epic wood': 'epic log',
    'epiclog': 'epic log',
    'epiclogs': 'epic log',
    'epicwood': 'epic log',
    'sl': 'super log',
    'super logs': 'super log',
    'super wood': 'super log',
    'superlog': 'super log',
    'superlogs': 'super log',
    'superwood': 'super log',
    'super': 'super log',
    'ml': 'mega log',
    'mega logs': 'mega log',
    'mega wood': 'mega log',
    'megalog': 'mega log',
    'megalogs': 'mega log',
    'megawood': 'mega log',
    'mega': 'mega log',
    'hl': 'hyper log',
    'hyper logs': 'hyper log',
    'hyper wood': 'hyper log',
    'hyperlog': 'hyper log',
    'hyperlogs': 'hyper log',
    'hyperwood': 'hyper log',
    'hyper': 'hyper log',
    'ul': 'ultra log',
    'ultra logs': 'ultra log',
    'ultra wood': 'ultra log',
    'ultralog': 'ultra log',
    'ultralogs': 'ultra log',
    'ultrawood': 'ultra log',
    'ultra': 'ultra log',
    'a': 'apple',
    'apples': 'apple',
    'bananas': 'banana',
    'r': 'ruby',
    'rubies': 'ruby',
    'rubys': 'ruby',
    'bf': 'baked fish',
    'fs': 'fruit salad',
    'salad': 'fruit salad',
    'salads': 'fruit salad',
    'fruit salads': 'fruit salad',
    'aj': 'apple juice',
    'apple juices': 'apple juice',
    'bp': 'banana pickaxe',
    'pickaxe': 'banana pickaxe',
    'pickaxes': 'banana pickaxe',
    'pick': 'banana pickaxe',
    'picks': 'banana pickaxe',
    'heavy apples': 'heavy apple',
    'ha': 'heavy apple',
    'heavy': 'heavy apple',
    'sc': 'super cookie',
    'cookie': 'super cookie',
    'cookies': 'super cookie',
    'super cookies': 'super cookie',
    'supercookie': 'super cookie',
    'supercookies': 'super cookie',
    'fl': 'filled lootbox',
    'lb': 'filled lootbox',
    'lootbox': 'filled lootbox',
    'lootboxes': 'filled lootbox',
    'filled lootboxes': 'filled lootbox',
    'lbs': 'filled lootbox',
    'cs': 'coin sandwich',
    'coin': 'coin sandwich',
    'sandwich': 'coin sandwich',
    'sandwiches': 'coin sandwich',
    'coin sandwiches': 'coin sandwich',
    'ice cream': 'fruit ice cream',
    'ice': 'fruit ice cream',
    'cream': 'fruit ice cream',
    'ice creams': 'fruit ice cream',
    'icecreams': 'fruit ice cream',
    'icecream': 'fruit ice cream',
    'fruit ice creams': 'fruit ice cream',
    'fruit ice': 'fruit ice cream',
    'fruitice': 'fruit ice cream',
    'hairns': 'hairn',
    'oj': 'orange juice',
    'orange': 'orange juice',
    'oranges': 'orange juice',
    'orange juices': 'orange juice',
    'carrot breads': 'carrot bread',
    'cb': 'carrot bread',
    'cc': 'carrotato chips',
    'carrotato': 'carrotato chips',
    'chips': 'carrotato chips',
    'h': 'hairn'
}

#--- Functions accessed by multiple cogs ----
# Create field "trade rates" for area & trading
async def design_field_traderate(traderate_data):

    field_value = f'{emojis.bp} 1 {emojis.fish} ⇄ {emojis.log} {traderate_data[1]}'
    if not traderate_data[2] == 0:
        field_value = f'{field_value}\n{emojis.bp} 1 {emojis.apple} ⇄ {emojis.log} {traderate_data[2]}'
        if not traderate_data[3] == 0:
            field_value = f'{field_value}\n{emojis.bp} 1 {emojis.ruby} ⇄ {emojis.log} {traderate_data[3]}'

    return (field_value)

# Trade for area X for area & trading
async def design_field_trades(area_no, ascended='not ascended'):

    if int(area_no) in (1,2,4,6,12,13,14):
        field_value = f'{emojis.bp} None'
    elif int(area_no) == 3:
        field_value = (
            f'{emojis.bp} Dismantle {emojis.fruitbanana} bananas\n'
            f'{emojis.bp} Dismantle {emojis.logultra} ULTRA logs and below\n'
            f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs\n'
            f'{emojis.bp} Trade {emojis.log} logs to {emojis.fish} fish'
        )
    elif int(area_no) == 5:
        field_value = (
            f'{emojis.bp} Dismantle {emojis.logultra} ULTRA logs and below\n'
            f'{emojis.bp} Dismantle {emojis.fishepic} EPIC fish and below\n'
            f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'
            f'{emojis.bp} Trade {emojis.fish} fish to {emojis.log} logs\n'
            f'{emojis.bp} Trade {emojis.log} logs to {emojis.apple} apples'
        )
    elif int(area_no) == 7:
        field_value = (
            f'{emojis.bp} Dismantle {emojis.fruitbanana} bananas\n'
            f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs'
        )
    elif int(area_no) == 8:
        if ascended == 'ascended':
            field_value = (
                f'{emojis.bp} Dismantle {emojis.loghyper} HYPER logs and below\n'
                f'{emojis.bp} Dismantle {emojis.fishepic} EPIC fish and below\n'
                f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'
                f'{emojis.bp} Trade {emojis.fish} fish to {emojis.log} logs\n'
                f'{emojis.bp} Trade {emojis.log} logs to {emojis.apple} apples'
            )
        else:
            field_value = (
                f'{emojis.bp} If crafter <90: Dismantle {emojis.logmega} MEGA logs and below\n'
                f'{emojis.bp} If crafter 90+: Dismantle {emojis.loghyper} HYPER logs and below\n'
                f'{emojis.bp} Dismantle {emojis.fishepic} EPIC fish and below\n'
                f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'
                f'{emojis.bp} Trade {emojis.fish} fish to {emojis.log} logs\n'
                f'{emojis.bp} Trade {emojis.log} logs to {emojis.apple} apples'
            )
    elif int(area_no) == 9:
        if ascended == 'ascended':
            field_value = (
                f'{emojis.bp} Dismantle {emojis.logsuper} SUPER logs and below\n'
                f'{emojis.bp} Dismantle {emojis.fruitbanana} bananas\n'
                f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'
                f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs\n'
                f'{emojis.bp} Trade {emojis.log} logs to {emojis.fish} fish'
            )
        else:
            field_value = (
                f'{emojis.bp} If crafter <90: Dismantle {emojis.logepic} EPIC logs\n'
                f'{emojis.bp} If crafter 90+: Dismantle {emojis.logsuper} SUPER logs and below\n'
                f'{emojis.bp} Dismantle {emojis.fruitbanana} bananas\n'
                f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'
                f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs\n'
                f'{emojis.bp} Trade {emojis.log} logs to {emojis.fish} fish'
            )
    elif int(area_no) == 10:
        field_value = (
            f'{emojis.bp} Dismantle {emojis.fruitbanana} bananas\n'
            f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs'
        )
    elif int(area_no) == 11:
        field_value = f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs'
    elif int(area_no) == 15:
        field_value = (
            f'{emojis.bp} Dismantle {emojis.fishgolden} golden fish and below\n'
            f'{emojis.bp} Dismantle {emojis.fruitbanana} bananas\n'
            f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'
            f'{emojis.bp} Trade {emojis.fish} fish to {emojis.log} logs\n'
            f'{emojis.bp} Trade {emojis.apple} apple to {emojis.log} logs'
        )
    else:
        field_value = f'{emojis.bp} N/A'

    return (field_value)

# Create field "Recommended Stats" for areas & dungeons
async def design_field_rec_stats(field_rec_stats_data, short_version=False):

    player_at = field_rec_stats_data[0]
    player_def = field_rec_stats_data[1]
    player_carry_def = field_rec_stats_data[2]
    player_life = field_rec_stats_data[3]
    life_boost = field_rec_stats_data[4]
    player_level = field_rec_stats_data[5]
    dungeon_no = field_rec_stats_data[6]

    if not dungeon_no == 15.2:
        dungeon_no = int(dungeon_no)

    player_at = f'{player_at:,}'
    player_def = f'{player_def:,}'
    player_life = f'{player_life:,}'

    if short_version == False:
        if life_boost == 'true':
            if dungeon_no < 11:
                life_boost = '(buy boost if necessary)'
            else:
                life_boost = '(buy boost and cook food if necessary)'
        else:
            life_boost = ''
    else:
        life_boost = ''

    if not player_carry_def == 0:
        if short_version == False:
            player_carry_def = f'({player_carry_def}+ to carry)'
        else:
            player_carry_def = f'({player_carry_def})'
    else:
        player_carry_def = ''

    if player_at == '0':
        player_at = '-'

    if player_def == '0':
        player_def = '-'

    if player_life == '0':
        player_life = '-'

    if player_level == 0:
        player_level = '-'

    if short_version == False:
        field_value = (
            f'{emojis.bp} {emojis.statat} **AT**: {player_at}\n'
            f'{emojis.bp} {emojis.statdef} **DEF**: {player_def} {player_carry_def}\n'
            f'{emojis.bp} {emojis.statlife} **LIFE**: {player_life} {life_boost}\n'
            f'{emojis.bp} {emojis.statlevel} **LEVEL**: {player_level}'
        )
    else:
        field_value = (
            f'{emojis.statat} **AT**: {player_at}\n'
            f'{emojis.statdef} **DEF**: {player_def} {player_carry_def}\n'
            f'{emojis.statlife} **LIFE**: {player_life} {life_boost}\n'
            f'{emojis.statlevel} **LEVEL**: {player_level}\n{emojis.blank}'
        )

    return field_value

# Get amount of material in inventory
async def inventory_get(inventory, material):

    if inventory.find(f'**{material}**:') > -1:
        mat_start = inventory.find(f'**{material}**:') + len(f'**{material}**:')+1
        mat_end = inventory.find(f'\\', mat_start)
        mat_end_bottom = inventory.find(f'\'', mat_start)
        mat = inventory[mat_start:mat_end]
        mat_bottom = inventory[mat_start:mat_end_bottom]
        if mat.isnumeric():
            mat = int(mat)
        elif mat_bottom.isnumeric():
            mat = int(mat_bottom)
        else:
            mat = 0
    else:
        mat = 0

    return mat