# database.py

from argparse import ArgumentError
from dataclasses import dataclass
from datetime import datetime
from multiprocessing.sharedctypes import Value
import sqlite3
import traceback
from typing import NamedTuple, Optional, Tuple, Union

import discord
from discord.ext import commands

from resources import emojis
from resources import logs, settings, strings


# Set name of database file
DB_FILE = settings.DB_FILE

# Open connection to the local database
ERG_DB = sqlite3.connect(DB_FILE, isolation_level=None)

# Internal errors
INTERNAL_ERROR_NO_DATA_FOUND = 'No data found in database.\nTable: {table}\nFunction: {function}\nSQL: {sql}'
INTERNAL_ERROR_NO_ARGUMENTS = 'You need to specify at least one keyword argument.\nTable: {table}\nFunction: {function}'
INTERNAL_ERROR_INVALID_ARGUMENTS = 'Invalid value {value} for argument {argument}.\nTable: {table}\nFunction: {function}'
INTERNAL_ERROR_DICT_TO_OBJECT = 'Error converting record into object\nFunction: {function}\nRecord: {record}\n'
INTERNAL_ERROR_SQLITE3 = 'Error executing SQL.\nError: {error}\nTable: {table}\nFunction: {function}\SQL: {sql}'


class FirstTimeUser(Exception):
    """Custom exception for first time users so they stop spamming my database"""
    def __init__(self, message="New user registered. This exception shouldn't be seen."):
        self.message = message
        super().__init__(self.message)


class NoDataFound(Exception):
    """Custom exception when no data is returned from the database"""
    pass

class NoArgumentsError(Exception):
    """Custom exception for when no arguments are passed to a function"""
    pass

class DirectMessageError(Exception):
    """Custom exception for when a user tries to use a command in direct messages"""
    pass


# Containers
class PetFusion(NamedTuple):
    """Container for pet fusion data"""
    tier: int
    tt_0_9: str
    tt_10_24: str
    tt_25_40: str
    tt_41_60: str
    tt_61_90: str
    tt_91_120: str
    tt_121_plus: str


class Ingredient(NamedTuple):
    """Container for ingredients"""
    amount: int
    name: str


class Item(NamedTuple):
    """Container for items"""
    item_type: str
    dismanteable: bool
    emoji: str
    requirements: str
    ingredients: Tuple[Ingredient]
    name: str
    score: float
    selling_price: int
    stat_at: int
    stat_def: int


class Dungeon(NamedTuple):
    """Container for dungeon data"""
    boss_at: int
    boss_emoji: str
    boss_life: float
    boss_name: str
    description: str
    dungeon_no: float
    key_price: int
    life_boost_needed: bool
    player_armor: Item
    player_armor_enchant: str
    player_at: int
    player_def: int
    player_carry_def: int
    player_level: int
    player_life: int
    player_sword: Item
    player_sword_enchant: str
    player_amount: Tuple[int, int] # min, max
    time_limit: int # seconds
    tt: int


class Area(NamedTuple):
    """Container for area data"""
    adv_dmg: Tuple[int, int]
    area_no: int
    description: str
    dungeon_no: float
    hunt_dmg: Tuple[int, int]
    new_commands: Tuple[str, str, str]
    money_tt1_nohorse: int
    money_tt1_t6horse: int
    money_tt3_nohorse: int
    money_tt3_t6horse: int
    money_tt5_nohorse: int
    money_tt5_t6horse: int
    money_tt10_nohorse: int
    money_tt10_t6horse: int
    trade_apple_log: int
    trade_fish_log: int
    trade_ruby_log: int
    unlocked_in_tt: int
    upgrade_armor: bool
    upgrade_armor_enchant: bool
    upgrade_sword: bool
    upgrade_sword_enchant: bool
    work_cmd_poor: str
    work_cmd_rich: str
    work_cmd_ascended: str


@dataclass
class Profession():
    """Container for profession data"""
    name: str
    xp: dict

    async def refresh(self) -> None:
        """Refreshes profession data from the database."""
        new_settings: Profession = await get_profession(self.name)
        self.xp = new_settings.xp

    async def update_level(self, level: int, xp: int) -> None:
        """Updates a profession level in the record in the database. Also calls refresh().

        Arguments
        ---------
        level: int - level to update
        xp: int - new xp for this level

        """
        await _update_profession_level(self, level, xp)
        await self.refresh()


class TimeTravel(NamedTuple):
    """Container for timetravel data"""
    a3_fish: int
    a5_apple: int
    tt: int
    tt_area: int
    unlock_area: int
    unlock_dungeon: int
    unlock_enchant: str
    unlock_misc: str
    unlock_title: str


class Title(NamedTuple):
    """Container for title data"""
    achievement_id: int
    command: str
    command_page: int
    requirements: str
    requires_id: int
    source: str
    tip: str
    title: str


class Setting(NamedTuple):
    """Container for a setting"""
    name: str
    value: str


@dataclass
class Monster():
    """Container for monster data"""
    activity: str
    areas: Tuple[int, int]
    drop_emoji: str
    drop_name: str
    emoji: str
    is_daily: bool
    name: str

    async def refresh(self) -> None:
        new_settings: Monster = await get_monster_by_name(self.name)
        self.activity = new_settings.activity
        self.areas = new_settings.areas
        self.is_daily = new_settings.is_daily
        self.drop_emoji = new_settings.drop_emoji
        self.drop_name = new_settings.drop_name
        self.emoji = new_settings.emoji

    async def set_daily(self) -> None:
        """Adds the current UTC date to the daily_mob_date column to mark the monster as daily. Also calls refresh()."""
        await _set_daily_monster(self)
        await self.refresh()

class Horse(NamedTuple):
    """Container for horse data"""
    def_level_bonus: float
    festive_level_bonus: float
    magic_level_bonus: float
    golden_level_bonus: float
    special_level_bonus: float
    strong_level_bonus: float
    super_special_level_bonus: float
    tank_level_bonus: float
    tier: int


class OracleAnswer(NamedTuple):
    """Container for oracle answers"""
    answer: str
    image_url: str


class Code(NamedTuple):
    """Container for codes"""
    code: str
    contents: str
    temporary: bool


class Tip(NamedTuple):
    """Container for tips"""
    id: int
    tip: str


@dataclass
class User():
    """Container for user data"""
    ascended: bool
    tt: int
    user_id: int

    async def refresh(self) -> None:
        """Refreshes user data from the database."""
        new_settings: User = await get_user(self.user_id)
        self.tt = new_settings.tt
        self.ascended = new_settings.ascended

    async def update(self, **kwargs) -> None:
        """Updates the user record in the database. Also calls refresh().

        Arguments
        ---------
        kwargs (column=value):
            ascended: bool
            tt: int
        """
        await _update_user(self, **kwargs)
        await self.refresh()


# Miscellaneous functions
async def _dict_to_dungeon(record: dict) -> Dungeon:
    """Creates a Dungeon object from a database record

    Arguments
    ---------
    record: Database record from table "dungeons" as a dict.

    Returns
    -------
    Dungeon object.

    Raises
    ------
    LookupError if something goes wrong reading the dict. Also logs this error to the database.
    """
    function_name = '_dict_to_dungeon'
    try:
        player_armor = player_sword = None
        if record['player_armor_name'] is not None:
            player_armor = await get_item(record['player_armor_name'])
        if record['player_sword_name'] is not None:
            player_sword = await get_item(record['player_sword_name'])
        dungeon = Dungeon(
            boss_at = record['boss_at'],
            boss_emoji = getattr(emojis, record['boss_emoji']) if record['boss_emoji'] is not None else None,
            boss_life = record['boss_life'],
            boss_name = record['boss_name'],
            description = record['description'],
            dungeon_no = record['dungeon'],
            key_price = record['key_price'],
            life_boost_needed = bool(record['life_boost_needed']),
            player_armor = player_armor,
            player_armor_enchant = record['player_armor_enchant'],
            player_at = record['player_at'],
            player_carry_def = record['player_carry_def'],
            player_def = record['player_def'],
            player_level = record['player_level'],
            player_life = record['player_life'],
            player_sword = player_sword,
            player_sword_enchant = record['player_sword_enchant'],
            player_amount = (record['min_players'], record['max_players']),
            time_limit = record['time_limit_s'],
            tt = record['tt']
        )
    except Exception as error:
        await log_error(
            INTERNAL_ERROR_DICT_TO_OBJECT.format(function=function_name, record=record)
        )
        raise LookupError(error)

    return dungeon


async def _dict_to_area(record: dict) -> Area:
    """Creates an Area object from a database record

    Arguments
    ---------
    record: Database record from table "areas" as a dict.

    Returns
    -------
    Area object.

    Raises
    ------
    LookupError if something goes wrong reading the dict. Also logs this error to the database.
    """
    function_name = '_dict_to_area'
    try:
        area = Area(
            adv_dmg = (record['adv_dmg_min'], record['adv_dmg_max']),
            area_no = record['area'],
            description = record['description'],
            dungeon_no = record['dungeon'],
            hunt_dmg = (record['hunt_dmg_min'], record['hunt_dmg_max']),
            new_commands = (record['new_cmd_1'], record['new_cmd_2'], record['new_cmd_3']),
            money_tt1_nohorse = record['money_tt1_nohorse'],
            money_tt1_t6horse = record['money_tt1_t6horse'],
            money_tt3_nohorse = record['money_tt3_nohorse'],
            money_tt3_t6horse = record['money_tt3_t6horse'],
            money_tt5_nohorse = record['money_tt5_nohorse'],
            money_tt5_t6horse = record['money_tt5_t6horse'],
            money_tt10_nohorse = record['money_tt10_nohorse'],
            money_tt10_t6horse = record['money_tt10_t6horse'],
            trade_apple_log = record['trade_apple_log'],
            trade_fish_log = record['trade_fish_log'],
            trade_ruby_log = record['trade_ruby_log'],
            unlocked_in_tt = record['unlocked_in_tt'],
            upgrade_armor = bool(record['upgrade_armor']),
            upgrade_armor_enchant = bool(record['upgrade_armor_enchant']),
            upgrade_sword = bool(record['upgrade_sword']),
            upgrade_sword_enchant = bool(record['upgrade_sword_enchant']),
            work_cmd_poor = record['work_cmd_poor'],
            work_cmd_rich = record['work_cmd_rich'],
            work_cmd_ascended = record['work_cmd_asc'],
        )
    except Exception as error:
        await log_error(
            INTERNAL_ERROR_DICT_TO_OBJECT.format(function=function_name, record=record)
        )
        raise LookupError(error)

    return area


async def _dict_to_monster(record: dict) -> Monster:
    """Creates a Monster object from a database record

    Arguments
    ---------
    record: Database record from table "monsters" as a dict.

    Returns
    -------
    Monster object.

    Raises
    ------
    LookupError if something goes wrong reading the dict. Also logs this error to the database.
    """
    function_name = '_dict_to_monster'
    try:
        is_daily = False
        if record['daily_mob_date'] is not None:
            today = datetime.utcnow().date()
            daily_date = datetime.fromisoformat(record['daily_mob_date'])
            if daily_date == today: is_daily = True
        monster = Monster(
            activity = record['activity'],
            areas = (record['area_from'], record['area_until']),
            drop_emoji = getattr(emojis, record['drop_emoji']) if record['drop_emoji'] is not None else None,
            drop_name = record['drop_name'],
            emoji = getattr(emojis, record['emoji']),
            is_daily = is_daily,
            name = record['name'],
        )
    except Exception as error:
        await log_error(
            INTERNAL_ERROR_DICT_TO_OBJECT.format(function=function_name, record=record)
        )
        raise LookupError(error)

    return monster


async def _dict_to_item(record: dict) -> Item:
    """Creates an Item object from a database record

    Arguments
    ---------
    record: Database record from table "items" as a dict.

    Returns
    -------
    Item object.

    Raises
    ------
    LookupError if something goes wrong reading the dict. Also logs this error to the database.
    """
    function_name = '_dict_to_item'
    try:
        item_name = record['name']
        record.pop('name')
        item_emoji = getattr(emojis, record['emoji'])
        record.pop('emoji')
        item_type = record['type']
        record.pop('type')
        requirements = record['requirements']
        record.pop('requirements')
        item_at = int(record['at'])
        record.pop('at')
        item_def = int(record['def'])
        record.pop('def')
        item_dismantleable = bool(record['dismantleable'])
        record.pop('dismantleable')
        item_score = record['score']
        record.pop('score')
        item_selling_price = record['selling_price']
        record.pop('selling_price')
        for name, amount in record.copy().items():
            if amount == 0: record.pop(name)
        ingredients = []
        for name, amount in record.items():
            ingredient = Ingredient(
                amount = amount,
                name = strings.item_columns_names[name]
            )
            ingredients.append(ingredient)
        ingredients.sort(key=lambda ingredient: ingredient.amount)
        item = Item(
            item_type = item_type,
            dismanteable = item_dismantleable,
            emoji = item_emoji,
            requirements = requirements,
            ingredients = ingredients,
            name = item_name,
            score = item_score,
            selling_price = item_selling_price,
            stat_at = item_at,
            stat_def = item_def
        )
    except Exception as error:
        await log_error(
            INTERNAL_ERROR_DICT_TO_OBJECT.format(function=function_name, record=record)
        )
        raise LookupError(error)

    return item


# --- Get Data ---
async def get_dungeon(dungeon_no: float) -> Dungeon:
    """Returns a dungeon from table "dungeons".

    Returns:
       Dungeon object.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found.
    """
    table = 'dungeons'
    function_name = 'get_dungeon'
    sql = f'SELECT * FROM {table} WHERE dungeon=?'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql,(dungeon_no,))
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    if not record:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound(f'Dungeon {dungeon_no} not found in database.')
    dungeon = await _dict_to_dungeon(dict(record))

    return dungeon


async def get_all_dungeons() -> Tuple[Dungeon]:
    """Gets all dungeons from the table "dungeons".

    Returns
    -------
    Tuple[Dungeon]

    Raises
    ------
    sqlite3.Error if something happened within the database.
    exceptions.NoDataFoundError if no dungeons were found.
    LookupError if something goes wrong reading the dict.
    Also logs all errors to the database.
    """
    table = 'dungeons'
    function_name = 'get_all_dungeons'
    sql = f'SELECT * FROM {table}'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur = ERG_DB.cursor()
        cur.execute(sql)
        records = cur.fetchall()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise

    if not records:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound('No dungeons found in database.')
    dungeons = []
    for record in records:
        dungeon = await _dict_to_dungeon(dict(record))
        dungeons.append(dungeon)

    return tuple(dungeons)


# Get dungeon data for the dungeon check command
async def get_dungeon_check_data(ctx, dungeon_no=0):

    try:
        cur=ERG_DB.cursor()
        if dungeon_no == 0:
            cur.execute('SELECT player_at, player_def, player_carry_def, player_life, dungeon FROM dungeons WHERE dungeon BETWEEN 1 AND 20')
            record = cur.fetchall()
        else:
            cur.execute('SELECT player_at, player_def, player_carry_def, player_life, dungeon FROM dungeons WHERE dungeon=?',(dungeon_no,))
            record = cur.fetchone()

        if record:
            dungeon_check_data = record
        else:
            await log_error('No recommended dungeon check data found in database.', ctx)

    except sqlite3.Error as error:
        logs.logger.error(error)
        await log_error(error, ctx)

    return dungeon_check_data


async def get_area(area_no: int) -> Area:
    """Returns an area from table "areas".

    Returns:
       Area object.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found.
    """
    table = 'areas'
    function_name = 'get_area'
    sql = f'SELECT * FROM areas WHERE area=?'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql, (area_no,))
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    if not record:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound(f'Area {area_no} not found in database.')
    area = await _dict_to_area(dict(record))

    return area


async def get_all_areas() -> Tuple[Area]:
    """Gets all areas from the table "areas".

    Returns
    -------
    Tuple[Area]

    Raises
    ------
    sqlite3.Error if something happened within the database.
    exceptions.NoDataFoundError if no dungeons were found.
    LookupError if something goes wrong reading the dict.
    Also logs all errors to the database.
    """
    table = 'areas'
    function_name = 'get_all_areas'
    sql = f'SELECT * FROM {table} ORDER BY area'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur = ERG_DB.cursor()
        cur.execute(sql)
        records = cur.fetchall()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise

    if not records:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound('No areas found in database.')
    areas = []
    for record in records:
        area = await _dict_to_area(dict(record))
        areas.append(area)

    return tuple(areas)


async def get_profession(name: str) -> Profession:
    """Returns a record from table "professions".

    Returns:
       Profession object.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found.
    """
    xp_columns = {
        'crafter': 'crafter_xp',
        'enchanter': 'enchanter_xp',
        'lootboxer': 'lootboxer_xp',
        'merchant': 'merchant_xp',
        'worker': 'worker_xp',
    }
    table = 'professions'
    function_name = 'get_profession'
    column = xp_columns.get(name, None)
    if column == None: raise NoDataFound(f'Unknown profession "{name}".')
    sql = f'SELECT level, {column} FROM professions ORDER BY level ASC'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql)
        records = cur.fetchall()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    if not records:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound(f'No data found in database for profession {name}.')
    profession_xp = {}
    for record in records:
        record = dict(record)
        profession_xp[record['level']] = record[column]

    profession = Profession(
        name = name,
        xp = profession_xp
    )

    return profession


async def get_time_travel(tt_no: int) -> TimeTravel:
    """Returns a record from table "timetravels".

    Returns:
       TimeTravel object.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found.
    """
    table = 'timetravels'
    function_name = 'get_time_travel'
    sql = f'SELECT * FROM timetravels WHERE tt=?'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql, (tt_no,))
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    if not record:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound(f'Time travel {tt_no} not found in database.')
    record = dict(record)
    tt = TimeTravel(
        a3_fish = record['a3_fish'],
        a5_apple = record['a5_apple'],
        tt = tt_no,
        tt_area = record['tt_area'],
        unlock_area = record['unlock_area'],
        unlock_dungeon = record['unlock_dungeon'],
        unlock_enchant = record['unlock_enchant'],
        unlock_misc = record['unlock_misc'],
        unlock_title = record['unlock_title'],
    )

    return tt


async def get_horse(tier: int) -> Horse:
    """Returns a record from table "horses".

    Returns:
       Horse object.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found.
    """
    table = 'horses'
    function_name = 'get_horse'
    sql = f'SELECT * FROM {table} WHERE tier=?'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql, (tier,))
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    if not record:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound(f'No data for horse tier {tier} found in database.')
    record = dict(record)
    horse_data = Horse(
        def_level_bonus = record['def_level_bonus'],
        festive_level_bonus = record['festive_level_bonus'],
        magic_level_bonus = record['magic_level_bonus'],
        golden_level_bonus = record['golden_level_bonus'],
        special_level_bonus = record['special_level_bonus'],
        strong_level_bonus = record['strong_level_bonus'],
        super_special_level_bonus = record['super_special_level_bonus'],
        tank_level_bonus = record['tank_level_bonus'],
        tier = record['tier'],
    )

    return horse_data


async def get_item(name: str) -> Item:
    """Returns an item from table "items".

    Returns:
       Item object.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found.
    """
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute('SELECT * FROM items WHERE name=?',(name,))
        record = cur.fetchone()
    except sqlite3.Error:
        raise
    if not record:
        raise NoDataFound
    record = dict(record)
    item_name = record['name']
    record.pop('name')
    item_emoji = getattr(emojis, record['emoji'])
    record.pop('emoji')
    item_type = record['type']
    record.pop('type')
    requirements = record['requirements']
    record.pop('requirements')
    item_at = int(record['at'])
    record.pop('at')
    item_def = int(record['def'])
    record.pop('def')
    item_dismantleable = bool(record['dismantleable'])
    record.pop('dismantleable')
    item_score = record['score']
    record.pop('score')
    item_selling_price = record['selling_price']
    record.pop('selling_price')
    for name, amount in record.copy().items():
        if amount == 0: record.pop(name)
    ingredients = []
    for name, amount in record.items():
        ingredient = Ingredient(
            amount = amount,
            name = strings.item_columns_names[name]
        )
        ingredients.append(ingredient)
    ingredients.sort(key=lambda ingredient: ingredient.amount)
    item = Item(
        item_type = item_type,
        dismanteable = item_dismantleable,
        emoji = item_emoji,
        requirements = requirements,
        ingredients = ingredients,
        name = item_name,
        score = item_score,
        selling_price = item_selling_price,
        stat_at = item_at,
        stat_def = item_def
    )

    return item


async def get_all_items() -> Tuple[Item]:
    """Gets all items from the table "items".

    Returns
    -------
    Tuple[Item]

    Raises
    ------
    sqlite3.Error if something happened within the database.
    exceptions.NoDataFoundError if no dungeons were found.
    LookupError if something goes wrong reading the dict.
    Also logs all errors to the database.
    """
    table = 'items'
    function_name = 'get_all_items'
    sql = f'SELECT * FROM {table} ORDER BY name ASC'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur = ERG_DB.cursor()
        cur.execute(sql)
        records = cur.fetchall()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise

    if not records:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound('No items found in database.')
    items = []
    for record in records:
        item = await _dict_to_item(dict(record))
        items.append(item)

    return tuple(items)


async def get_oracle_answer() -> OracleAnswer:
    """Get a random oracle answer

    Returns
    -------
    OracleAnswer object

    Raises
    ------
    sqlite3.Error if something happened within the database.
    exceptions.NoDataFoundError if no answer was found.
    LookupError if something goes wrong reading the dict.
    Also logs all errors to the database.
    """
    table = 'oracle_answers'
    function_name = 'get_oracle_answer'
    sql = f'SELECT * FROM {table} ORDER BY RANDOM() LIMIT 1'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur = ERG_DB.cursor()
        cur.execute(sql)
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise

    if not record:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound('No oracle answer found in database.')

    answer = OracleAnswer(
        answer = record['answer'],
        image_url = record['image_url'],
    )

    return answer


# Get tt unlocks
async def get_tt_unlocks(ctx, user_tt):
    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT t.tt, t.unlock_dungeon, t.unlock_area, t.unlock_enchant, t.unlock_title, t.unlock_misc FROM timetravel t WHERE tt=?', (user_tt,))
        record = cur.fetchone()

        if record:
            tt_unlock_data = record
        else:
            await log_error('No tt_unlock data found in database.', ctx)
    except sqlite3.Error as error:
        logs.logger.error(error)
        await log_error(error, ctx)

    return tt_unlock_data


# Get trade rate data
async def get_traderate_data(ctx, areas):

    try:
        cur=ERG_DB.cursor()

        if (type(areas) == str) and (areas == 'all'):
            cur.execute('SELECT area, trade_fish_log, trade_apple_log, trade_ruby_log FROM areas ORDER BY area')
            record = cur.fetchall()
        elif type(areas) == int:
            cur.execute('SELECT area, trade_fish_log, trade_apple_log, trade_ruby_log FROM areas WHERE area=?', (areas,))
            record = cur.fetchone()
        elif type(areas) in (list,tuple):
            cur.execute('SELECT area, trade_fish_log, trade_apple_log, trade_ruby_log FROM areas WHERE area BETWEEN ? and ?', (areas[0],areas[1],))
            record = cur.fetchall()
        else:
            await log_error('Parameter \'areas\' has an invalid format, could not get traderate data.', ctx)
            return

        if record:
            traderate_data = record
        else:
            await log_error('No trade rate data found in database.', ctx)
    except sqlite3.Error as error:
        logs.logger.error(error)
        await log_error(error, ctx)

    return traderate_data


async def get_tip(id: Optional[int] = None) -> Tip:
    """Get a tip. If no id is given, this returns a random tip.

    Returns
    -------
    Tip object

    Raises
    ------
    sqlite3.Error if something happened within the database.
    exceptions.NoDataFoundError if no answer was found.
    LookupError if something goes wrong reading the dict.
    Also logs all errors to the database.
    """
    table = 'tips'
    function_name = 'get_tip'
    if id is None:
        sql = f'SELECT * FROM {table} ORDER BY RANDOM() LIMIT 1'
    else:
        sql = f'SELECT * FROM {table} WHERE id = ?'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur = ERG_DB.cursor()
        if id is None:
            cur.execute(sql)
        else:
            cur.execute(sql, (id,))
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise

    if not record:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound('No tip found in database.')

    tip = Tip(
        id = record['id'],
        tip = record['tip'],
    )

    return tip


async def get_horse_data(ctx: commands.Context, tier: int) -> dict:
    """Returns all level bonuses for a horse tier

    Returns:
        Dict with the column names and the values of the tier.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found. This also logs an error.
    """
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute('SELECT * FROM horses WHERE tier=?',(tier,))
        record = cur.fetchone()
        if record:
            horse_data = dict(record)
        else:
            await log_error(
                ctx, INTERNAL_ERROR_NO_DATA_FOUND.format(table='horses',
                                                         function='get_horse_data',
                                                         select=f'Horse tier {tier}')
            )
            raise NoDataFound
    except sqlite3.Error:
        raise
    return horse_data


async def get_pet_fusions(tt_no: int) -> Tuple[PetFusion]:
    """Returns all pet fusions from the table pets.

    Returns:
       Tuple with PetFusion objects.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found. This also logs an error.
    """
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute('SELECT * FROM pets')
        records = cur.fetchall()
    except sqlite3.Error:
        raise
    if not records:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table='pets',
                                                function='get_pet_fusions',
                                                select=f'Time travel {tt_no}')
        )
        raise NoDataFound
    pet_fusions = []
    for record in records:
        record = dict(record)
        fusion = PetFusion(
            tier = record['pet_tier'],
            tt_0_9 = record['tt_0_9'],
            tt_10_24 = record['tt_10_24'],
            tt_25_40 = record['tt_25_40'],
            tt_41_60 = record['tt_41_60'],
            tt_61_90 = record['tt_61_90'],
            tt_91_120 = record['tt_91_120'],
            tt_121_plus = record['tt_121_plus'],
        )
        pet_fusions.append(fusion)

    return tuple(pet_fusions)


async def get_all_codes() -> Tuple[Code]:
    """Returns all codes from table "codes".

    Returns:
        Tuple with Code objects

    Raises:
        NoDataFoundError if there are no settings stored.
        sqlite3.Error if something happened within the database. Also logs it to the database.
    """
    table = 'codes'
    function_name = 'get_all_codes'
    sql = f'SELECT * FROM {table}'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql)
        records = cur.fetchall()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    codes = []
    for record in records:
        code = Code(
            code = record['code'],
            contents = record['contents'],
            temporary = True if record['temporary'] == 'True' else False
        )
        codes.append(code)

    return tuple(codes)


# Get redeemable codes
async def get_codes(ctx):

    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT * FROM codes ORDER BY code')
        records = cur.fetchall()

        if records:
            codes = records
        else:
            codes = []
            await log_error('No codes data found in database.', ctx)
    except sqlite3.Error as error:
        logs.logger.error(error)
        await log_error(error, ctx)

    return codes

# Get user count
async def get_user_number(ctx):

    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        record = cur.fetchone()

        if record:
            user_number = record
        else:
            await log_error('No user data found in database.', ctx)
    except sqlite3.Error as error:
        logs.logger.error(error)
        await log_error(error, ctx)

    return user_number


async def get_user_count() -> int:
    """Gets the amount of users in the table "users".

    Returns
    -------
    Amount of users: int

    Raises
    ------
    sqlite3.Error if something happened within the database. Also logs this error to the log file.
    """
    table = 'users'
    function_name = 'get_user_count'
    sql = f'SELECT COUNT(user_id) FROM {table}'
    try:
        cur = ERG_DB.cursor()
        cur.execute(sql)
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    (user_count,) = record

    return user_count


async def get_user(user_id: int) -> User:
    """Returns user settings from table "users".
    If none is found, a new record with the default settings TT0 and not ascended is
    inserted and an error is raised.

    Returns:
        User object

    Raises:
        FirstTimeUser if there are no settings stored.
        sqlite3.Error if something happened within the database. Also logs it to the database.
    """
    table = 'users'
    function_name = 'get_user'
    sql = f'SELECT * FROM {table} WHERE user_id = ?'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql, (user_id,))
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    if not record:
        cur.execute(f'INSERT INTO {table} VALUES (?, ?, ?)', (user_id, 0, False))
        raise FirstTimeUser
    record = dict(record)
    user = User(
        ascended = bool(record['ascended']),
        tt = record['tt'],
        user_id = record['user_id'],
    )

    return user


async def get_all_users() -> Tuple[User]:
    """Returns all user settings from table "users".
    This is only used for migration, can be deleted afterwards.

    Returns:
        Tuple with User objects

    Raises:
        FirstTimeUser if there are no settings stored.
        sqlite3.Error if something happened within the database. Also logs it to the database.
    """
    table = 'users'
    function_name = 'get_user'
    sql = f'SELECT * FROM {table}'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql)
        records = cur.fetchall()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    users = []
    for record in records:
        if record['ascended'] not in ('ascended', 'not ascended'): raise BaseException('Already migrated.')
        user = User(
            ascended = True if record['ascended'] == 'ascended' else False,
            tt = record['tt'],
            user_id = record['user_id'],
        )
        users.append(user)

    return tuple(users)


async def get_monster_by_name(name: str) -> Monster:
    """Returns a monster from table "monsters".

    Returns:
        Monster object

    Raises:
        NoDataFound is no monster is found.
        sqlite3.Error if something happened within the database. Also logs it to the database.
    """
    table = 'monsters'
    function_name = 'get_monster_by_name'
    sql = f'SELECT * FROM {table} WHERE name = ? COLLATE NOCASE'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql, (name,))
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    if not record:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound(f'No monster {name} found in database.')
    monster = await _dict_to_monster(dict(record))

    return monster


async def get_monster_by_area(area_from: int, area_until: int) -> Tuple[Monster]:
    """Returns monsters from table "users".

    Returns:
        Tuple with Monster objects

    Raises:
        sqlite3.Error if something happened within the database. Also logs it to the database.
    """
    table = 'monsters'
    function_name = 'get_monster_by_area'
    sql = f'SELECT * FROM {table} WHERE area_from <= ? AND area_until >= ?'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql, (area_from, area_until))
        records = cur.fetchall()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    monsters = []
    for record in records:
        monster = await _dict_to_monster(dict(record))
        monsters.append(monster)

    return tuple(monsters)


async def get_daily_monster(name: str) -> Monster:
    """Returns the daily monster from table "monsters". Returns None if no monster is set as daily.

    Returns:
        Monster object or None

    Raises:
        sqlite3.Error if something happened within the database. Also logs it to the database.
    """
    table = 'monsters'
    function_name = 'get_daily_monster'
    sql = f'SELECT * FROM {table} WHERE daily_mob_date = ?'
    today = datetime.utcnow().date()
    today_str = today.isoformat()
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql, (today_str,))
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    if not record: return None
    monster = await _dict_to_monster(dict(record))
    return monster


async def get_all_monsters() -> Tuple[Monster]:
    """Gets all monsters from the table "monsters".

    Returns
    -------
    Tuple[Monster]

    Raises
    ------
    sqlite3.Error if something happened within the database.
    exceptions.NoDataFoundError if no dungeons were found.
    LookupError if something goes wrong reading the dict.
    Also logs all errors to the database.
    """
    table = 'monsters'
    function_name = 'get_all_monsters'
    sql = f'SELECT * FROM {table} ORDER BY name ASC'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur = ERG_DB.cursor()
        cur.execute(sql)
        records = cur.fetchall()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise

    if not records:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound('No monsters found in database.')
    monsters = []
    for record in records:
        monster = await _dict_to_monster(dict(record))
        monsters.append(monster)

    return tuple(monsters)


async def get_monsters(search_string: str) -> Tuple[Title]:
    """Returns all monsters for a search query.

    Returns:
       Tuple with Monster objects.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found.
    """
    ERG_DB.row_factory = sqlite3.Row
    cur=ERG_DB.cursor()
    search_string = search_string.replace(' ','%').replace("'",'_')
    search_string = f'%{search_string}%'
    sql = "SELECT * FROM monsters WHERE name LIKE ? ORDER BY area_from ASC, area_until ASC"
    cur.execute(sql, (search_string,))
    records = cur.fetchall()
    if not records:
        raise NoDataFound
    monsters = []
    for record in records:
        monster = await _dict_to_monster(dict(record))
        monsters.append(monster)

    return tuple(monsters)


async def get_titles(search_string: str) -> Tuple[Title]:
    """Returns all titles for a search query.

    Returns:
       Tuple with Title objects.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found.
    """
    ERG_DB.row_factory = sqlite3.Row
    cur=ERG_DB.cursor()
    if search_string.isnumeric():
        cur.execute('SELECT * FROM titles WHERE id=?', (search_string,))
    else:
        search_string = search_string.replace(' ','%').replace("'",'_')
        search_string = f'%{search_string}%'
        sql = f"SELECT * FROM titles WHERE title LIKE ? or requirements LIKE ? ORDER BY id ASC"
        cur.execute(sql, (search_string, search_string))
    records = cur.fetchall()
    if not records:
        raise NoDataFound
    titles = []
    for record in records:
        record = dict(record)
        title = Title(
            achievement_id = record['id'],
            command = record['command'],
            command_page = record['command_page'],
            requirements = record['requirements'],
            requires_id = record['requires_id'],
            source = record['source'],
            tip = record['tip'],
            title = record['title']
        )
        titles.append(title)

    return tuple(titles)


async def get_settings() -> dict:
    """Returns all setting from table "settings".

    Returns:
       dict with all settings.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found.
    """
    table = 'settings'
    function_name = 'get_settings'
    sql = f'SELECT * FROM {table}'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql)
        records = cur.fetchall()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    if not records:
        await log_error(
            INTERNAL_ERROR_NO_DATA_FOUND.format(table=table, function=function_name, sql=sql)
        )
        raise NoDataFound('No settings not found in database.')

    return dict(records)


# --- Write Data ---
async def _update_user(user: User, **kwargs) -> None:
    """Updates user record. Use User.update() to trigger this function.

    Arguments
    ---------
    user_id: int
    kwargs (column=value):
        ascended: bool
        tt: int

    Raises
    ------
    sqlite3.Error if something happened within the database.
    NoArgumentsError if no kwargs are passed (need to pass at least one)
    Also logs all errors to the database.
    """
    table = 'users'
    function_name = '_update_user'
    if not kwargs:
        await log_error(
            INTERNAL_ERROR_NO_ARGUMENTS.format(table=table, function=function_name)
        )
        raise NoArgumentsError('You need to specify at least one keyword argument.')
    try:
        cur = ERG_DB.cursor()
        sql = f'UPDATE {table} SET'
        for kwarg in kwargs:
            sql = f'{sql} {kwarg} = :{kwarg},'
        sql = sql.strip(",")
        kwargs['user_id'] = user.user_id
        sql = f'{sql} WHERE user_id = :user_id'
        cur.execute(sql, kwargs)
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise


async def _update_profession_level(profession: Profession, level: int, xp: int) -> None:
    """Updates profession record. Use Profession.update_level() to trigger this function.

    Arguments
    ---------
    level: int
    kwargs (column=value):
        ascended: bool
        tt: int

    Raises
    ------
    sqlite3.Error if something happened within the database.
    NoArgumentsError if no kwargs are passed (need to pass at least one)
    Also logs all errors to the database.
    """
    table = 'professions'
    function_name = '_update_profession_level'
    if not 1 <= level <= 200:
        await log_error(
            INTERNAL_ERROR_INVALID_ARGUMENTS.format(value=level, argument='level', table=table, function=function_name)
        )
        raise NoArgumentsError(f'Invalid profession level ({level}).')
    if xp < 0:
        await log_error(
            INTERNAL_ERROR_INVALID_ARGUMENTS.format(value=xp, argument='xp', table=table, function=function_name)
        )
        raise NoArgumentsError(f'Invalid profession xo ({xp}).')
    try:
        cur = ERG_DB.cursor()
        xp_columns = {
            'crafter': 'crafter_xp',
            'enchanter': 'enchanter_xp',
            'lootboxer': 'lootboxer_xp',
            'merchant': 'merchant_xp',
            'worker': 'worker_xp',
        }
        sql = f'UPDATE {table} SET {xp_columns[profession.name]} = ? WHERE level = ?'
        cur.execute(sql, (xp, level))
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise


async def update_setting(name: str, value: str) -> None:
    """Updates a setting record.

    Arguments
    ---------
    name: str
    value: str

    Raises
    ------
    sqlite3.Error if something happened within the database.
    ArgumentError if value is None
    Also logs all errors to the database.
    """
    table = 'settings'
    function_name = 'update_setting'
    if name is None or value is None:
        await log_error(
            INTERNAL_ERROR_INVALID_ARGUMENTS.format(
                value=f'value: {value}, name: {name}', argument='name / value', table=table, function=function_name
            )
        )
        raise ArgumentError('Arguments can\'t be None.')
    try:
        cur = ERG_DB.cursor()
        sql = f'UPDATE {table} SET value = ? WHERE name = ?'
        cur.execute(sql, (value, name))
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise


async def _set_daily_monster(monster: Monster) -> None:
    """Sets today's daily date of a monster record. Use Monster.set_daily() to trigger this function.

    Raises
    ------
    sqlite3.Error if something happened within the database.
    NoArgumentsError if no kwargs are passed (need to pass at least one)
    Also logs all errors to the database.
    """
    table = 'monsters'
    function_name = '_set_daily_monster'
    try:
        today = datetime.utcnow().date()
        today_str = today.isoformat()
        cur = ERG_DB.cursor()
        sql = f'UPDATE {table} SET daily_mob_date = ? WHERE name = ?'
        cur.execute(sql, (today_str, monster.name))
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise


# --- Error Logging ---
async def log_error(error: Union[Exception, str], ctx: Optional[discord.ApplicationContext] = None):
    """Logs an error to the database and the logfile

    Arguments
    ---------
    error: Exception or a simple string.
    ctx: If context is available, the function will log the user input, the message timestamp
    and the user settings. If not, current time is used, settings and input are logged as "N/A".

    Raises
    ------
    sqlite3.Error when something goes wrong in the database. Also logs this error to the log file.
    """
    table = 'errors'
    function_name = 'log_error'
    sql = 'INSERT INTO errors VALUES (?, ?, ?, ?, ?)'
    timestamp = datetime.utcnow()
    if isinstance(ctx, discord.ApplicationContext):
        command_name = f'{ctx.command.full_parent_name} {ctx.command.name}'.strip()
        command_data = str(ctx.interaction.data.get('options','None'))
        try:
            user = await get_user(ctx.author.id)
            user_settings = f'TT{user.tt}, {"ascended" if user.ascended else "not ascended"}'
        except:
            user_settings = 'N/A'
    elif isinstance(ctx, commands.Context):
        command_name = f'{ctx.prefix}{ctx.invoked_with}'
        command_data = " ".join(ctx.args[2:])
        try:
            user = await get_user(ctx.author.id)
            user_settings = f'TT{user.tt}, {"ascended" if user.ascended else "not ascended"}'
        except:
            user_settings = 'N/A'
    else:
        user_settings = 'N/A'
        command_name = 'N/A'
        command_data = 'N/A'
    if hasattr(error, 'message'):
        error_message = error.message
    else:
        error_message = str(error)
    try:
        module = error.__class__.__module__
        if module is None or module == str.__class__.__module__:
            error_message = f'{error.__class__.__name__}\n{error_message}'
        if hasattr(error, '__traceback__'):
            traceback_str = "".join(traceback.format_tb(error.__traceback__))
        else:
            traceback_str = 'N/A'
        error_message = (
            f'{error_message}\n\n'
            f'Exception type:\n'
            f'{module}.{error.__class__.__name__}\n\n'
            f'Traceback:\n'
            f'{traceback_str}'
        )
    except Exception as error:
        error_message = f'{error_message}\n\nGot the following error while trying to get type and traceback:\n{error}'
    try:
        cur=ERG_DB.cursor()
        cur.execute(sql, (timestamp, command_name, command_data, error_message, user_settings))
    except sqlite3.Error as error:
        logs.logger.error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql),
            ctx
        )
        raise


async def get_weekly_profession() -> str:
    """Returns the weekly profession from table "professions_weekly". Returns None if not set yet for this week.

    Returns:
        Name of profession or None

    Raises:
        sqlite3.Error if something happened within the database. Also logs it to the database.
    """
    table = 'professions_weekly'
    function_name = 'get_weekly_profession'
    sql = f"SELECT * FROM {table} WHERE DATE(date) > DATE('now', 'weekday 0', '-7 days', 'start of day') ORDER BY date DESC"
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute(sql)
        record = cur.fetchone()
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise
    if not record: return None
    return record['profession']


async def set_weekly_profession(profession: str) -> None:
    """Sets today's date to a profession.

    Raises
    ------
    sqlite3.Error if something happened within the database.
    NoArgumentsError if no kwargs are passed (need to pass at least one)
    Also logs all errors to the database.
    """
    table = 'professions_weekly'
    function_name = 'set_weekly_profession'
    try:
        today = datetime.utcnow().date()
        today_str = today.isoformat()
        cur = ERG_DB.cursor()
        sql = f'UPDATE {table} SET date = ? WHERE profession = ?'
        cur.execute(sql, (today_str, profession.lower()))
    except sqlite3.Error as error:
        await log_error(
            INTERNAL_ERROR_SQLITE3.format(error=error, table=table, function=function_name, sql=sql)
        )
        raise