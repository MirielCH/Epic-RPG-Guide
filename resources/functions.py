# functions.py

import database
import emojis

async def design_field_traderate(area: database.Area) -> str:
    """Create field "trade rates" for area & trading"""
    field_value = f'{emojis.BP} 1 {emojis.FISH} ⇄ {emojis.LOG} {area.trade_fish_log}'
    if area.trade_apple_log > 0:
        field_value = f'{field_value}\n{emojis.BP} 1 {emojis.APPLE} ⇄ {emojis.LOG} {area.trade_apple_log}'
    if area.trade_ruby_log > 0:
        field_value = f'{field_value}\n{emojis.BP} 1 {emojis.RUBY} ⇄ {emojis.LOG} {area.trade_ruby_log}'

    return field_value


async def design_field_trades(area: database.Area, user: database.User) -> str:
    """Trades for area X for area & trading"""
    if area.area_no in (1,2,4,6,12,13,14,16,17,18,19,20,21):
        field_value = f'{emojis.BP} None'
    elif area.area_no == 3:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Dismantle {emojis.LOG_ULTRA} ULTRA logs and below\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)\n'
            f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.FISH} fish (B)'
        )
    elif area.area_no == 5:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.LOG_ULTRA} ULTRA logs and below\n'
            f'{emojis.BP} Dismantle {emojis.FISH_EPIC} EPIC fish and below\n'
            f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
            f'{emojis.BP} Trade {emojis.FISH} fish to {emojis.LOG} logs (A)\n'
            f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.APPLE} apples (D)'
        )
    elif area.area_no == 7:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)'
        )
    elif area.area_no == 8:
        if user.ascended:
            field_value = f'{emojis.BP} Dismantle {emojis.LOG_HYPER} HYPER logs and below'
        else:
            field_value = (
                f'{emojis.BP} If crafter <90: Dismantle {emojis.LOG_MEGA} MEGA logs and below\n'
                f'{emojis.BP} If crafter 90+: Dismantle {emojis.LOG_HYPER} HYPER logs and below'
            )
        field_value = (
            f'{field_value}\n'
            f'{emojis.BP} Dismantle {emojis.FISH_EPIC} EPIC fish and below\n'
            f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
            f'{emojis.BP} Trade {emojis.FISH} fish to {emojis.LOG} logs (A)\n'
            f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.APPLE} apples (D)'
        )
    elif area.area_no == 9:
        if user.ascended:
            field_value = f'{emojis.BP} Dismantle {emojis.LOG_SUPER} SUPER logs and below'
        else:
            field_value = (
                f'{emojis.BP} If crafter <90: Dismantle {emojis.LOG_EPIC} EPIC logs\n'
                f'{emojis.BP} If crafter 90+: Dismantle {emojis.LOG_SUPER} SUPER logs and below'
            )
        field_value = (
            f'{field_value}\n'
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)\n'
            f'{emojis.BP} Trade {emojis.LOG} logs to {emojis.FISH} fish (B)'
        )
    elif area.area_no == 10:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)'
        )
    elif area.area_no == 11:
        field_value = f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)'
    elif area.area_no == 15:
        field_value = (
            f'{emojis.BP} Dismantle {emojis.FISH_GOLDEN} golden fish and below\n'
            f'{emojis.BP} Dismantle {emojis.BANANA} bananas\n'
            f'{emojis.BP} Trade {emojis.RUBY} rubies to {emojis.LOG} logs (E)\n'
            f'{emojis.BP} Trade {emojis.FISH} fish to {emojis.LOG} logs (A)\n'
            f'{emojis.BP} Trade {emojis.APPLE} apples to {emojis.LOG} logs (C)'
        )
    else:
        field_value = f'{emojis.BP} N/A'

    return field_value


async def design_field_rec_gear(dungeon: database.Dungeon) -> str:
    """Create field "Recommended gear. May return None."""
    player_armor_enchant = '' if dungeon.player_armor_enchant is None else f'[{dungeon.player_armor_enchant}]'
    player_sword_enchant = '' if dungeon.player_sword_enchant is None else f'[{dungeon.player_sword_enchant}]'

    field_value = ''
    if dungeon.player_sword is not None:
        field_value = (
            f'{emojis.BP} {dungeon.player_sword.emoji} {dungeon.player_sword.name} {player_sword_enchant}'
        )
    if dungeon.player_armor is not None:
        field_value = (
            f'{field_value}\n{emojis.BP} {dungeon.player_armor.emoji} {dungeon.player_armor.name} '
            f'{player_armor_enchant}'
        )

    if field_value == '': field_value = None
    return field_value


async def design_field_rec_stats(dungeon: database.Dungeon, short_version: bool = False) -> str:
    """Design field "Recommended Stats" for areas & dungeons. NEEDS REFACTORING"""

    player_carry_def = ''
    if dungeon.player_carry_def is not None:
        if short_version:
            player_carry_def = f'({dungeon.player_carry_def})'
        else:
            player_carry_def = f'({dungeon.player_carry_def}+ to carry)'

    player_at = '-' if dungeon.player_at is None else f'{dungeon.player_at:,}'
    player_def = '-' if dungeon.player_def is None else f'{dungeon.player_def:,}'
    player_level = '-' if dungeon.player_level is None else f'{dungeon.player_level:,}'
    player_life = '-' if dungeon.player_life is None else f'{dungeon.player_life:,}'

    field_value = (
        f'{emojis.BP} {emojis.STAT_AT} **AT**: {player_at}\n'
        f'{emojis.BP} {emojis.STAT_DEF} **DEF**: {player_def} {player_carry_def}\n'
        f'{emojis.BP} {emojis.STAT_LIFE} **LIFE**: {player_life}\n'
        f'{emojis.BP} {emojis.STAT_LEVEL} **LEVEL**: {player_level}'
    )
    if 16 <= dungeon.dungeon_no <= 20:
        field_value = (
            f'{field_value}\n'
            f'{emojis.BP} _To be balanced!_'
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


async def default_footer(prefix):
    footer = f'Use {prefix}guide or {prefix}g to see all available guides.'

    return footer