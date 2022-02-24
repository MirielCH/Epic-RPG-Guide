# global_data.py

import logging
import logging.handlers
import os

from dotenv import load_dotenv

import emojis
import database
import global_data


# Read tokens
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DBL_TOKEN = os.getenv('DBL_TOKEN')
DEBUG_MODE = os.getenv('DEBUG_MODE')

# Get bot directory
BOT_DIR = os.path.dirname(__file__)

# Databases
DB_FILE = os.path.join(BOT_DIR, 'database/erg_db.db')
DEFAULT_DB_FILE = os.path.join(BOT_DIR, 'database/erg_db_default.db')

# Pictures
IMG_THUMBNAIL = os.path.join(BOT_DIR, 'images/erg.png')
IMG_DUNGEON_11 = os.path.join(BOT_DIR, 'images/dungeon11.png')
IMG_DUNGEON_13 = os.path.join(BOT_DIR, 'images/dungeon13.png')

# Prefix
DEFAULT_PREFIX = '$'

# EPIC RPG user id
EPIC_RPG_ID = 555955826880413696

# Default responses
MSG_ABORTING = 'Aborting.'
MSG_BOT_MESSAGE_NOT_FOUND = '**{user}**, couldn\'t find your {information} information, RIP.'
MSG_ERROR = 'Whelp, something went wrong here, sorry.'
MSG_SYNTAX = 'The command syntax is `{syntax}`'
MSG_WAIT_FOR_INPUT = '**{user}**, please type `{command}` (or `abort` to abort)'
MSG_WRONG_INPUT = 'Wrong input. Aborting.'

# Embed color
EMBED_COLOR = 0x8914FF

# Set default footer
async def default_footer(prefix):
    footer = f'Use {prefix}guide or {prefix}g to see all available guides.'

    return footer

# Open error log file, create if it not exists
logfile = os.path.join(BOT_DIR, 'logs/discord.log')
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
    'ed sw': 'chad sword',
    'edgy sw': 'chad sword',
    'chad sw': 'chad sword',
    'omega sw': 'omega sword',
    'o sw': 'omega sword',
    'ed sword': 'chad sword',
    'ed armor': 'chad armor',
    'ue sw': 'ultra-chad sword',
    'uc sw': 'ultra-chad sword',
    'ultra-edgy sw': 'ultra-chad sword',
    'ultra-chad sw': 'ultra-chad sword',
    'ue sword': 'ultra-chad sword',
    'uc sword': 'ultra-chad sword',
    'ultra-omega sw': 'ultra-omega sword',
    'ue armor': 'ultra-chad armor',
    'uc armor': 'ultra-chad armor',
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
    'f': 'normie fish',
    'fishes': 'normie fish',
    'fish': 'normie fish',
    'normiefish': 'normie fish',
    'normie fishes': 'normie fish',
    'normiefishes': 'normie fish',
    'gf': 'golden fish',
    'golden fishes': 'golden fish',
    'goldenfish': 'golden fish',
    'goldenfishes': 'golden fish',
    'ef': 'epic fish',
    'epicfish': 'epic fish',
    'epicfishes': 'epic fish',
    'epic fishes': 'epic fish',
    'brandon': 'epic fish',
    'l': 'wooden log',
    'wood': 'wooden log',
    'logs': 'wooden log',
    'log': 'wooden log',
    'wooden logs': 'wooden log',
    'woodenlog': 'wooden log',
    'woodenlogs': 'wooden log',
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
    'h': 'hairn',
    'melon': 'watermelon',
    'melons': 'watermelon',
    'water melon':'watermelon',
    'water melons':'watermelon',
    'watermelon':'watermelon',
    'wm': 'watermelon',
    'superfish': 'super fish',
    'superfishes': 'super fish',
    'super fishes': 'super fish',
    'sf': 'super fish',
    'ultimatelog': 'ultimate log',
    'ultimate logs': 'ultimate log',
    'ultimatelogs': 'ultimate log',
    'superarmor': 'super armor',
    'watermelon sw': 'watermelon sword',
    'melon sw': 'watermelon sword',
    'watermelonsw': 'watermelon sword',
    'watermelonsw': 'watermelon sword',
    'melonsw': 'watermelon sword',
    'melon sword': 'watermelon sword',
    'watermelonsword': 'watermelon sword',
    'wm sword': 'watermelon sword',
    'wmsword': 'watermelon sword',
    'watermelonarmor': 'watermelon armor',
    'melon armor': 'watermelon armor',
    'melonarmor': 'watermelon armor',
    'wm armor': 'watermelon armor',
    'wmarmor': 'watermelon armor',
    'scaledarmor': 'scaled armor',
    'scaledsword': 'scaled sword',
    'scaledsw': 'scaled sword',
    'scaled sw': 'scaled sword',
    'banana sw': 'banana sword',
    'bananasw': 'banana sword',
    'bananasword': 'banana sword',
    'epic sw': 'epic sword',
    'epicsw': 'epic sword',
    'epicsword': 'epic sword',
    'lootboxarmor': 'lootbox armor',
    'lbarmor': 'lootbox armor',
    'lb armor': 'lootbox armor',
    'lotterysword': 'lottery sword',
    'lotterysw': 'lottery sword',
    'lottery sw': 'lottery sword',
    'timesword': 'time sword',
    'timesw': 'time sword',
    'time sw': 'time sword',
    'timearmor': 'time armor',
    'voidsword': 'void sword',
    'voidsw': 'void sword',
    'void sw': 'void sword',
    'voidarmor': 'void armor',
    'abysssword': 'abyss sword',
    'abysssw': 'abyss sword',
    'abyss sw': 'abyss sword',
    'abyssarmor': 'abyss armor',
    'corruptedsword': 'corrupted sword',
    'corruptedsw': 'corrupted sword',
    'corrupted sw': 'corrupted sword',
    'corruptedarmor': 'corrupted armor',
    'spacesword': 'space sword',
    'spacesw': 'space sword',
    'space sw': 'space sword',
    'spacearmor': 'space armor',
    'woodenarmor': 'wooden armor',
    'tt': 'time travel',
    'timetravel': 'time travel',
    'darkenergy': 'dark energy',
    'basicsword': 'basic sword',
    'basicsw': 'basic sword',
    'basic sw': 'basic sword',
    'basicarmor': 'basic armor',
}

item_columns_names = {
    'apple': 'apple',
    'armor_basic': 'Basic Armor',
    'armor_chad': 'CHAD Armor',
    'armor_coin': 'Coin Armor',
    'armor_fish': 'Fish Armor',
    'armor_lootbox': 'Lootbox Armor',
    'armor_omega': 'OMEGA Armor',
    'armor_super': 'SUPER Armor',
    'armor_giga_chad': 'GIGA-CHAD Armor',
    'armor_ultra_omega': 'ULTRA-OMEGA Armor',
    'banana': 'banana',
    'bread': 'bread',
    'carrot': 'carrot',
    'chip': 'chip',
    'coin': 'coin',
    'cookie': 'arena cookie',
    'dark_energy': 'dark energy',
    'dragon_essence': 'dragon essence',
    'dragon_scale': 'dragon scale',
    'fish': 'normie fish',
    'fish_epic': 'EPIC fish',
    'fish_golden': 'golden fish',
    'fish_super': 'SUPER fish',
    'life_potion': 'life potion',
    'lb_common': 'common lootbox',
    'lb_edgy': 'EDGY lootbox',
    'lb_epic': 'EPIC lootbox',
    'lb_rare': 'rare lootbox',
    'lb_godly': 'GODLY lootbox',
    'lb_omega': 'OMEGA lootbox',
    'lb_uncommon': 'uncommon lootbox',
    'lb_void': 'VOID lootbox',
    'lottery_ticket': 'lottery ticket',
    'life': 'LIFE',
    'log': 'wooden log',
    'log_epic': 'EPIC log',
    'log_hyper': 'HYPER log',
    'log_mega': 'MEGA log',
    'log_super': 'SUPER log',
    'log_ultimate': 'ULTIMATE log',
    'log_ultra': 'ULTRA log',
    'mermaid_hair': 'mermaid hair',
    'potato': 'potato',
    'ruby': 'ruby',
    'unicorn_horn': 'unicorn horn',
    'sword_basic': 'Basic Sword',
    'sword_chad': 'CHAD Sword',
    'sword_electronical': 'Electronical Sword',
    'sword_godly': 'GODLY Sword',
    'sword_omega': 'OMEGA Sword',
    'sword_giga_chad': 'GIGA-CHAD Sword',
    'sword_ultra_omega': 'ULTRA-OMEGA Sword',
    'time_dragon_essence': 'TIME dragon essence',
    'time_travel': 'time travel',
    'water_melon': 'water melon',
    'watermelon': 'watermelon',
    'wolf_skin': 'wolf skin',
    'zombie_eye': 'zombie eye',
}

#--- Functions accessed by multiple cogs ----
# Create field "trade rates" for area & trading
async def design_field_traderate(traderate_data):

    field_value = f'{emojis.BP} 1 {emojis.FISH} ⇄ {emojis.LOG} {traderate_data[1]}'
    if not traderate_data[2] == 0:
        field_value = f'{field_value}\n{emojis.BP} 1 {emojis.APPLE} ⇄ {emojis.LOG} {traderate_data[2]}'
        if not traderate_data[3] == 0:
            field_value = f'{field_value}\n{emojis.BP} 1 {emojis.RUBY} ⇄ {emojis.LOG} {traderate_data[3]}'

    return (field_value)

# Trade for area X for area & trading
async def design_field_trades(area_no, ascended='not ascended'):

    if int(area_no) in (1,2,4,6,12,13,14):
        field_value = f'{emojis.BP} None'
    elif int(area_no) == 3:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Dismantle {emojis.LOG_ULTRA} ULTRA logs and below\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)\n'
            f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.FISH} fish (B)'
        )
    elif int(area_no) == 5:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.LOG_ULTRA} ULTRA logs and below\n'
            f'{emojis.BP} Dismantle {emojis.FISH_EPIC} EPIC fish and below\n'
            f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
            f'{emojis.BP} Trade {emojis.FISH} fish to {emojis.LOG} logs (A)\n'
            f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.APPLE} apples (D)'
        )
    elif int(area_no) == 7:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)'
        )
    elif int(area_no) == 8:
        if ascended == 'ascended':
            field_value = (
                f'{emojis.BP} Dismantle {emojis.LOG_HYPER} HYPER logs and below\n'
                f'{emojis.BP} Dismantle {emojis.FISH_EPIC} EPIC fish and below\n'
                f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
                f'{emojis.BP} Trade {emojis.FISH} fish to {emojis.LOG} logs (A)\n'
                f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.APPLE} apples (D)'
            )
        else:
            field_value = (
                f'{emojis.BP} If crafter <90: Dismantle {emojis.LOG_MEGA} MEGA logs and below\n'
                f'{emojis.BP} If crafter 90+: Dismantle {emojis.LOG_HYPER} HYPER logs and below\n'
                f'{emojis.BP} Dismantle {emojis.FISH_EPIC} EPIC fish and below\n'
                f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
                f'{emojis.BP} Trade {emojis.FISH} fish to {emojis.LOG} logs (A)\n'
                f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.APPLE} apples (D)'
            )
    elif int(area_no) == 9:
        if ascended == 'ascended':
            field_value = (
                f'{emojis.BP} Dismantle {emojis.LOG_SUPER} SUPER logs and below\n'
                f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
                f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
                f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)\n'
                f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.FISH} fish (B)'
            )
        else:
            field_value = (
                f'{emojis.BP} If crafter <90: Dismantle {emojis.LOG_EPIC} EPIC logs\n'
                f'{emojis.BP} If crafter 90+: Dismantle {emojis.LOG_SUPER} SUPER logs and below\n'
                f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
                f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
                f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)\n'
                f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.FISH} fish (B)'
            )
    elif int(area_no) == 10:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)'
        )
    elif int(area_no) == 11:
        field_value = f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)'
    elif int(area_no) == 15:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.FISH_GOLDEN} golden fish and below\n'
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
            f'{emojis.BP} Trade {emojis.FISH} fish to {emojis.LOG} logs (A)\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)'
        )
    else:
        field_value = f'{emojis.BP} N/A'

    return (field_value)


async def design_field_rec_stats(dungeon, short_version: bool = False) -> str:
    """Design field "Recommended Stats" for areas & dungeons. NEEDS REFACTORING"""
    if 16 <= dungeon.dungeon_no <= 21:
        return f'{emojis.BP} Currently unknown'

    if dungeon.dungeon_no.is_integer(): dungeon_no = int(dungeon.dungeon_no)

    life_boost = ''
    if not short_version and dungeon.life_boost_needed:
        if dungeon_no < 11:
            life_boost = '(buy boost if necessary)'
        else:
            life_boost = '(buy boost and cook food if necessary)'

    player_carry_def = ''
    if dungeon.player_carry_def is not None:
        if not short_version:
            player_carry_def = f'({dungeon.player_carry_def}+ to carry)'
        else:
            player_carry_def = f'({dungeon.player_carry_def})'

    player_at = '-' if dungeon.player_at is None else f'{dungeon.player_at:,}'
    player_def = '-' if dungeon.player_def is None else f'{dungeon.player_def:,}'
    player_level = '-' if dungeon.player_level is None else f'{dungeon.player_level:,}'
    player_life = '-' if dungeon.player_life is None else f'{dungeon.player_life:,}'

    if not short_version:
        field_value = (
            f'{emojis.BP} {emojis.STAT_AT} **AT**: {player_at}\n'
            f'{emojis.BP} {emojis.STAT_DEF} **DEF**: {player_def} {player_carry_def}\n'
            f'{emojis.BP} {emojis.STAT_LIFE} **LIFE**: {player_life} {life_boost}\n'
            f'{emojis.BP} {emojis.STAT_LEVEL} **LEVEL**: {player_level}'
        )
    else:
        field_value = (
            f'{emojis.STAT_AT} **AT**: {player_at}\n'
            f'{emojis.STAT_DEF} **DEF**: {player_def} {player_carry_def}\n'
            f'{emojis.STAT_LIFE} **LIFE**: {player_life} {life_boost}\n'
            f'{emojis.STAT_LEVEL} **LEVEL**: {player_level}\n{emojis.BLANK}'
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


def format_string(string: str) -> str:
    """Format string to ASCII"""
    string = (
        string
        .encode('unicode-escape',errors='ignore')
        .decode('ASCII')
        .replace('\\','')
    )
    return string