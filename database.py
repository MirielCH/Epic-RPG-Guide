# database.py

from datetime import datetime
import sqlite3
from typing import NamedTuple, Tuple, Union

import discord
from discord.ext import commands

import emojis
import global_data


# Set name of database file
DB_FILE = global_data.DB_FILE

# Open connection to the local database
ERG_DB = sqlite3.connect(DB_FILE, isolation_level=None)

# Internal errors
INTERNAL_ERROR_NO_DATA_FOUND = 'No data found in database.\nTable: {table}\nFunction: {function}\nSELECT: {select}'


class FirstTimeUser(commands.CommandError):
    """Custom exception for first time users so they stop spamming my database"""
    pass


class NoDataFound(Exception):
    """Exception when no data is returned from the database"""
    pass


# Containers
class PetFusion(NamedTuple):
    """Container for pet fusion data"""
    tier: int
    fusion: str


class PetTier(NamedTuple):
    """Container for pet tier data"""
    tier: int
    tt_no: int
    fusion_to_get_tier: PetFusion
    fusions_including_tier: Tuple[PetFusion]


class Ingredient(NamedTuple):
    """Container for ingredients"""
    amount: int
    name: str


class Item(NamedTuple):
    """Container for items"""
    item_type: str
    dismanteable: bool
    emoji: str
    ingredients: Tuple[Ingredient]
    name: str
    stat_at: int
    stat_def: int


class Title(NamedTuple):
    """Conatiner for title data"""
    achievement_id: int
    command: str
    requirements: str
    requires_id: int
    source: str
    tip: str
    title: str


# --- Get Data ---
async def get_all_prefixes(bot: commands.Bot, ctx: commands.Context) -> tuple:
    """Checks the database for a prefix. If no prefix is found, a record for the guild is created with the
    default prefix.

    Returns:
        A tuple with the current server prefix and the pingable bot
    """
    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT prefix FROM settings_guild where guild_id=?', (ctx.guild.id,))
        record = cur.fetchone()
        if record:
            (prefix,) = record
        else:
            cur.execute('INSERT INTO settings_guild VALUES (?, ?)', (ctx.guild.id, global_data.DEFAULT_PREFIX,))
            prefix = global_data.DEFAULT_PREFIX
    except sqlite3.Error as error:
        await log_error(ctx, error)

    return commands.when_mentioned_or(prefix)(bot, ctx)


async def get_prefix(ctx_or_guild: Union[commands.Context, discord.Guild]) -> str:
    """Check database for stored prefix. If no prefix is found, the default prefix is used"""
    guild_id = ctx_or_guild.guild.id if isinstance(ctx_or_guild, commands.Context) else ctx_or_guild.id
    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT prefix FROM settings_guild where guild_id=?', (guild_id,))
        record = cur.fetchone()
        prefix = record[0] if record else global_data.DEFAULT_PREFIX
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx_or_guild, error)

    return prefix

# Get dungeon data for the dungeon commands
async def get_dungeon_data(ctx, dungeon):

    if dungeon == 151:
        dungeon = 15
    elif dungeon == 152:
        dungeon = 15.2

    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT dungeons.*, i1.emoji, i2.emoji FROM dungeons INNER JOIN items i1 ON i1.name = dungeons.player_sword_name INNER JOIN items i2 ON i2.name = dungeons.player_armor_name WHERE dungeons.dungeon=?', (dungeon,))
        record = cur.fetchone()

        if record:
            dungeon_data = record
        else:
            await log_error(ctx, 'No dungeon data found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return dungeon_data

# Get dungeon data for the recommended stats of all dungeons
async def get_rec_stats_data(ctx):

    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT d.player_at, d.player_def, d.player_carry_def, d.player_life, d.life_boost_needed, d.player_level, d.dungeon FROM dungeons d WHERE dungeon BETWEEN 1 AND 16')
        record = cur.fetchall()

        if record:
            rec_stats_data = record
        else:
            await log_error(ctx, 'No recommended dungeon stats data found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return rec_stats_data

# Get dungeon data for the recommended gear of all dungeons
async def get_rec_gear_data(ctx, page):

    try:
        cur=ERG_DB.cursor()
        if page == 1:
            cur.execute('SELECT d.player_sword_name, d.player_sword_enchant, i1.emoji, d.player_armor_name, d.player_armor_enchant, i2.emoji, d.dungeon FROM dungeons d INNER JOIN items i1 ON i1.name = d.player_sword_name INNER JOIN items i2 ON i2.name = d.player_armor_name WHERE d.dungeon BETWEEN 1 and 9')
        elif page == 2:
            cur.execute('SELECT d.player_sword_name, d.player_sword_enchant, i1.emoji, d.player_armor_name, d.player_armor_enchant, i2.emoji, d.dungeon FROM dungeons d INNER JOIN items i1 ON i1.name = d.player_sword_name INNER JOIN items i2 ON i2.name = d.player_armor_name WHERE d.dungeon BETWEEN 10 and 16')
        record = cur.fetchall()

        if record:
            rec_gear_data = record
        else:
            await log_error(ctx, 'No recommended dungeon gear data found in database.')
    except sqlite3.Error as error:
        await log_error(ctx, error)

    return rec_gear_data

# Get dungeon data for the dungeon check command
async def get_dungeon_check_data(ctx, dungeon_no=0):

    try:
        cur=ERG_DB.cursor()
        if dungeon_no == 0:
            cur.execute('SELECT player_at, player_def, player_carry_def, player_life, dungeon FROM dungeons WHERE dungeon BETWEEN 1 AND 15')
            record = cur.fetchall()
        else:
            cur.execute('SELECT player_at, player_def, player_carry_def, player_life, dungeon FROM dungeons WHERE dungeon=?',(dungeon_no,))
            record = cur.fetchone()

        if record:
            dungeon_check_data = record
        else:
            await log_error(ctx, 'No recommended dungeon check data found in database.')

    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return dungeon_check_data

# Get area data for the area embeds
async def get_area_data(ctx, area):

    try:
        cur=ERG_DB.cursor()
        select_columns = 'a.area, a.work_cmd_poor, a.work_cmd_rich, a.work_cmd_asc, a.new_cmd_1, a.new_cmd_2, a.new_cmd_3, a.money_tt1_t6horse, a.money_tt1_nohorse, a.money_tt3_t6horse, a.money_tt3_nohorse, a.money_tt5_t6horse, a.money_tt5_nohorse, a.money_tt10_t6horse, a.money_tt10_nohorse, '\
                         'a.upgrade_sword, a.upgrade_sword_enchant, a.upgrade_armor, a.upgrade_armor_enchant, a.description, a.dungeon, i1.emoji, '\
                        'i2.emoji, d.player_at, d.player_def, d.player_carry_def, d.player_life, d.life_boost_needed, d.player_level, d.player_sword_name, d.player_sword_enchant, d.player_armor_name, d.player_armor_enchant'
        cur.execute(f'SELECT {select_columns} FROM areas a INNER JOIN dungeons d ON d.dungeon = a.dungeon INNER JOIN items i1 ON i1.name = d.player_sword_name INNER JOIN items i2 ON i2.name = d.player_armor_name WHERE a.area=?', (area,))
        record = cur.fetchone()

        if record:
            area_data = record
        else:
            await log_error(ctx, 'No area data found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return area_data

# Get mats data for the needed mats of area 3 and 5
async def get_mats_data(ctx, user_tt):
    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT t.tt, t.a3_fish, t.a5_apple FROM timetravel t WHERE tt=?', (user_tt,))
        record = cur.fetchone()

        if record:
            mats_data = record
        else:
            await log_error(ctx, 'No tt_mats data found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return mats_data


async def get_item(ctx: commands.Context, name: str) -> Item:
    """Returns an item from table "items".

    Returns:
       Item object.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found. This also logs an error.
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
    item_at = int(record['at'])
    record.pop('at')
    item_def = int(record['def'])
    record.pop('def')
    item_dismantleable = bool(record['dismantleable'])
    record.pop('dismantleable')
    for name, amount in record.copy().items():
        if amount == 0: record.pop(name)
    ingredients = []
    for name, amount in record.items():
        ingredient = Ingredient(
            amount = amount,
            name = global_data.item_columns_names[name]
        )
        ingredients.append(ingredient)
    ingredients.sort(key=lambda ingredient: ingredient.amount)
    item = Item(
        item_type = item_type,
        dismanteable = item_dismantleable,
        emoji = item_emoji,
        ingredients = ingredients,
        name = item_name,
        stat_at = item_at,
        stat_def = item_def
    )

    return item


# Get tt unlocks
async def get_tt_unlocks(ctx, user_tt):
    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT t.tt, t.unlock_dungeon, t.unlock_area, t.unlock_enchant, t.unlock_title, t.unlock_misc FROM timetravel t WHERE tt=?', (user_tt,))
        record = cur.fetchone()

        if record:
            tt_unlock_data = record
        else:
            await log_error(ctx, 'No tt_unlock data found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

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
            await log_error(ctx, 'Parameter \'areas\' has an invalid format, could not get traderate data.')
            return

        if record:
            traderate_data = record
        else:
            await log_error(ctx, 'No trade rate data found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return traderate_data

# Get profession XP
async def get_profession_levels(ctx, profession, levelrange):

    start_level, end_level = levelrange
    if profession == 'worker':
        query = 'SELECT level, worker_xp FROM professions WHERE level BETWEEN ? and ?'
    elif profession == 'merchant':
        query = 'SELECT level, merchant_xp FROM professions WHERE level BETWEEN ? and ?'
    elif profession == 'lootboxer':
        query = 'SELECT level, lootboxer_xp FROM professions WHERE level BETWEEN ? and ?'
    elif profession == 'enchanter':
        query = 'SELECT level, enchanter_xp FROM professions WHERE level BETWEEN ? and ?'
    else:
        await log_error(ctx, 'Unknown profession, could not generate profession query.')
        return

    try:
        cur=ERG_DB.cursor()
        cur.execute(query, (start_level, end_level,))
        record = cur.fetchall()
        if record:
            profession_levels = record
        else:
            await log_error(ctx, 'No profession data data found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return profession_levels

# Get random tip
async def get_tip(ctx, id=0):

    try:
        cur=ERG_DB.cursor()
        if id > 0:
            cur.execute('SELECT tip FROM tips WHERE id=?',(id,))
            record = cur.fetchone()
        elif id == 0:
            cur.execute('SELECT tip FROM tips ORDER BY RANDOM() LIMIT 1')
            record = cur.fetchone()

        if record:
            tip = record
        else:
            tip = ('There is no tip with that ID.',)
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

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


async def get_pet_tier(ctx: commands.Context, tier: int, tt_no: int) -> PetTier:
    """Returns a pet tier.

    Returns:
       PetTier object.

    Raises:
        sqlite3.Error if something goes wrong.
        NoDataFound if no data was found. This also logs an error.
    """
    if 0 <= tt_no <= 9:
        column = 'tt_0_9'
    elif 10 <= tt_no <= 24:
        column = 'tt_10_24'
    elif 25 <= tt_no <= 40:
        column = 'tt_25_40'
    elif 41 <= tt_no <= 60:
        column = 'tt_41_60'
    elif 61 <= tt_no <= 90:
        column = 'tt_61_90'
    else:
        column = 'tt_91_plus'
    try:
        ERG_DB.row_factory = sqlite3.Row
        cur=ERG_DB.cursor()
        cur.execute('SELECT * FROM pets WHERE pet_tier=?',(tier,))
        record_pet_tier = cur.fetchone()
        cur.execute(f"SELECT * FROM pets WHERE {column} LIKE 'T{tier} %' OR {column} LIKE '%T{tier}'")
        records_fusions = cur.fetchall()
    except sqlite3.Error:
        raise
    if not record_pet_tier:
        await log_error(
            ctx, INTERNAL_ERROR_NO_DATA_FOUND.format(table='pets',
                                                     function='get_pet_tier',
                                                     select=f'Pet tier {tier}')
        )
        raise NoDataFound
    record_pet_tier = dict(record_pet_tier)
    fusion_to_get_tier = PetFusion(
        tier = tier,
        fusion = record_pet_tier[column] if record_pet_tier[column] is not None else 'None'
    )
    fusions_including_tier = []
    for record in records_fusions:
        record = dict(record)
        fusion = PetFusion(
            tier = record['pet_tier'],
            fusion = record[column]
        )
        fusions_including_tier.append(fusion)
    pet_tier = PetTier(
        tier = tier,
        tt_no = tt_no,
        fusion_to_get_tier = fusion_to_get_tier,
        fusions_including_tier = tuple(fusions_including_tier)
    )

    return pet_tier


# Get redeemable codes
async def get_codes(ctx):

    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT * FROM codes ORDER BY code')
        records = cur.fetchall()

        if records:
            codes = records
        else:
            await log_error(ctx, 'No codes data found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return codes

# Get user count
async def get_user_number(ctx):

    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT COUNT(*) FROM settings_user')
        record = cur.fetchone()

        if record:
            user_number = record
        else:
            await log_error(ctx, 'No user data found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return user_number


async def get_user_settings(ctx: commands.Context) -> tuple:
    """Check database for user settings.
    If none is found, the default settings TT0 and not ascended are
    stored and an error is raised. There is NO return when this happens.

    Returns:
        List: [TT, Ascension].

    Raises:
        FirstTimeUser if there are no settings stored. This also sends the welcome message.
        sqlite3.Error if something happened within the database. Also logs it to the database.
    """
    try:
        cur=ERG_DB.cursor()
        user_id = ctx.author.id
        cur.execute('SELECT timetravel, ascended FROM settings_user where user_id=?', (user_id,))
        record = cur.fetchone()
        if record:
            user_settings = record
        else:
            cur.execute('INSERT INTO settings_user VALUES (?, ?, ?)', (user_id, 0, 'not ascended'))
            await first_time_user(ctx)
            raise FirstTimeUser
    except sqlite3.Error as error:
        await log_error(ctx, error)
        raise

    return list(user_settings)

# Get monster data by areas
async def get_mob_data(ctx, areas):
    """
    areas: tuple/list that contains two areas: from_area and until_area.
    Example: get_mob_data(ctx, (1,4,)) returns the mobs for areas 1, 2, 3 and 4
    """

    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT name, emoji, area_from, area_until, activity, drop_emoji FROM monsters WHERE area_from >= ? and area_until <= ?', (areas[0],areas[1],))
        record = cur.fetchall()


        if record:
            mob_data = record
        else:
            await log_error(ctx, 'No mob data found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return mob_data

# Get monster by name
async def get_mob_by_name(ctx, name):

    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT name, emoji, area_from, area_until, activity, drop_emoji FROM monsters WHERE name = ? COLLATE NOCASE', (name,))
        record = cur.fetchone()

        if record:
            mob = record
        else:
            mob = None
            await log_error(ctx, 'No mob found in database.')
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

    return mob


async def get_titles(ctx: commands.Context, search_string: str) -> Tuple[Title]:
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
        search_string = search_string.replace(' ','%').replace("'",'_').replace('’','_')
        search_string = f'%{search_string}%'
        sql = f"SELECT * FROM titles WHERE title LIKE ? or requirements LIKE ?"
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
            requirements = record['requirements'],
            requires_id = record['requires_id'],
            source = record['source'],
            tip = record['tip'],
            title = record['title']
        )
        titles.append(title)

    return tuple(titles)


# --- Write Data ---
# # Set new prefix
async def set_prefix(ctx, new_prefix):

    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT * FROM settings_guild where guild_id=?', (ctx.guild.id,))
        record = cur.fetchone()

        if record:
            cur.execute('UPDATE settings_guild SET prefix = ? where guild_id = ?', (new_prefix, ctx.guild.id,))
        else:
            cur.execute('INSERT INTO settings_guild VALUES (?, ?)', (ctx.guild.id, new_prefix,))
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)

# Set progress settings
async def set_progress(ctx, new_tt, new_ascended):

    try:
        cur=ERG_DB.cursor()
        cur.execute('SELECT * FROM settings_user where user_id=?', (ctx.author.id,))
        record = cur.fetchone()

        if record:
            cur.execute('UPDATE settings_user SET timetravel = ?, ascended = ? where user_id = ?', (new_tt, new_ascended, ctx.author.id,))
        else:
            cur.execute('INSERT INTO settings_user VALUES (?, ?, ?)', (ctx.author.id, new_tt, new_ascended,))
    except sqlite3.Error as error:
        global_data.logger.error(error)
        await log_error(ctx, error)


# --- Error Logging ---
async def log_error(ctx_or_guild: Union[commands.Context, discord.Guild], error: Union[Exception, str]):
    """Logs an error to the database and the logfile"""
    if isinstance(ctx_or_guild, commands.Context):
        ctx = ctx_or_guild
        timestamp = ctx.message.created_at
        user_input = ctx.message.content
        try:
            user_settings = await get_user_settings(ctx)
            user_tt, user_ascended = user_settings
            settings = f'TT{user_tt}, {user_ascended}'
        except:
            settings = 'N/A'
    else:
        settings = 'N/A'
        timestamp = datetime.utcnow()
        user_input = 'Error when joining a new guild'
    try:
        cur=ERG_DB.cursor()
        cur.execute('INSERT INTO errors VALUES (?, ?, ?, ?)', (timestamp, user_input, str(error), settings))
    except sqlite3.Error as db_error:
        global_data.logger.error(f'Error inserting error (ha) into database:\n{db_error}')


# --- First Time User ---
async def first_time_user(ctx: commands.Context) -> None:
    """Welcome message to inform the user of his/her initial settings"""
    try:
        user_settings = await get_user_settings(ctx)
    except Exception as error:
        if isinstance(error, FirstTimeUser):
            return
        else:
            await ctx.send(global_data.MSG_ERROR)
            return
    user_tt, user_ascension = user_settings
    prefix = ctx.prefix

    await ctx.send(
        f'Hey there, **{ctx.author.name}**. Looks like we haven\'t met before.\n'
        f'I have set your progress to **TT {user_tt}**, **{user_ascension}**.\n\n'
        f'** --> Please use `{prefix}{ctx.invoked_with}` again to use the bot.**\n\n'
        f'• If you don\'t know what this means, you probably haven\'t time traveled yet and are in TT 0. Check out `{prefix}tt` for some details.\n'
        f'• If you are in a higher TT, please use `{prefix}setprogress` (or `{prefix}sp`) to change your settings.\n\n'
        f'These settings are used by some guides (like the area guides) to only show you what is relevant to your current progress.'
    )