# dungeons.py

import asyncio
from humanfriendly import format_timespan
from typing import Optional, Tuple

import discord

import database
from resources import emojis, functions, settings, strings, views


# --- Commands ---
async def command_dungeon_guide(ctx: discord.ApplicationContext, dungeon_no: float,
                                switch_view: Optional[discord.ui.View] = None) -> None:
    """Dungeon guide command"""
    if dungeon_no not in strings.DUNGEONS:
        await ctx.respond('Is that supposed to be a valid dungeon? :thinking:', ephemeral=True)
        return
    user = interaction = None
    full_guide = True
    if switch_view is not None:
        user = getattr(switch_view, 'db_user', None)
        full_guide = getattr(switch_view, 'full_guide', True)
        interaction = getattr(switch_view, 'interaction', None)
    view = views.DungeonGuideView(ctx, dungeon_no, embed_dungeon_guide, user, full_guide)
    embed = await embed_dungeon_guide(dungeon_no)
    if interaction is None:
        interaction = await ctx.respond(embed=embed, view=view)
    else:
        await functions.edit_interaction(interaction, embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    if view.value != 'switched':
        try:
            await functions.edit_interaction(interaction, view=None)
        except discord.errors.NotFound:
            pass


async def command_dungeon_check(bot: discord.Bot, ctx: discord.ApplicationContext, dungeon_no: float,
                                user_at: Optional[int] = None, user_def: Optional[int] = None,
                                user_life: Optional[int] = None,
                                switch_view: Optional[discord.ui.View] = None)  -> None:
    """Dungeon check command"""
    interaction = None
    if switch_view is not None:
        user_at = getattr(switch_view, 'user_at', None)
        user_def = getattr(switch_view, 'user_def', None)
        user_life = getattr(switch_view, 'user_life', None)
        interaction = getattr(switch_view, 'interaction', None)
    if user_at is None or user_def is None or user_life is None:
        bot_message_task = asyncio.ensure_future(functions.wait_for_profile_or_stats_message(bot, ctx))
        try:
            content = (
                f'**{ctx.author.name}**, please use {strings.SLASH_COMMANDS_EPIC_RPG["profile"]} '
                f'or {strings.SLASH_COMMANDS_EPIC_RPG["stats"]}.\n'
                f'Note that profile backgrounds are not supported.'
            )
            bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
        except asyncio.TimeoutError:
            await ctx.respond(
                strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='stats'),
                ephemeral=True
            )
            return
        if bot_message is None: return
        at_found, def_found, life_found = await functions.extract_stats_from_profile_or_stats_embed(ctx, bot_message)
        if user_at is None: user_at = at_found
        if user_def is None: user_def = def_found
        if user_life is None: user_life = life_found
    view = views.DungeonCheckView(bot, ctx, dungeon_no, user_at, user_def, user_life, embed_dungeon_check)
    embed = await embed_dungeon_check(dungeon_no, user_at, user_def, user_life)
    if interaction is None:
        interaction = await ctx.respond(embed=embed, view=view)
    else:
        await functions.edit_interaction(interaction, embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    if view.value != 'switched':
        try:
            await functions.edit_interaction(interaction, view=None)
        except discord.errors.NotFound:
            pass


# --- Functions ---
async def design_field_dungeon_check(dungeon_no: float, user_at: int, user_def: int, user_life: int) -> Tuple[str, str]:
    """Return a check result field and details about the resulst for one dungeon for the dungeon check embed"""
    dungeon: database.Dungeon = await database.get_dungeon(dungeon_no)
    if not dungeon_no == 15.2: dungeon_no = int(dungeon_no)

    check_at = 'N/A'
    check_def = 'N/A'
    check_carry_def = 'N/A'
    check_life = 'N/A'

    user_at_check_result = 'N/A'
    user_def_check_result = 'N/A'
    user_carry_def_check_result = 'N/A'
    user_life_check_result = 'N/A'

    check_results = ''

    if dungeon_no <= 9:
        if not dungeon.player_at == 0:
            if user_at < dungeon.player_at:
                if user_def >= dungeon.player_carry_def:
                    user_at_check_result = 'ignore'
                else:
                    user_at_check_result = 'fail'
            elif user_at >= dungeon.player_at:
                user_at_check_result = 'pass'
        else:
            check_at = f'{emojis.CHECK_IGNORE} **AT**: -'

        if not dungeon.player_def == 0:
            if user_def < dungeon.player_def:
                user_def_check_result = 'fail'
            elif user_def >= dungeon.player_def:
                user_def_check_result = 'pass'
        else:
            check_def = f'{emojis.CHECK_IGNORE} **DEF**: -'

        if not dungeon.player_carry_def == 0:
            if user_def < dungeon.player_carry_def:
                user_carry_def_check_result = 'fail'
            elif user_def >= dungeon.player_carry_def:
                user_carry_def_check_result = 'pass'
        else:
            check_carry_def = f'{emojis.CHECK_IGNORE} **Carry DEF**: -'

        if not dungeon.player_life == 0:
            if user_life < dungeon.player_life:
                if user_def >= dungeon.player_carry_def:
                        user_life_check_result = 'ignore'
                elif dungeon.player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (dungeon.player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (dungeon.player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                else:
                    user_life_check_result = 'fail'
            elif user_life >= dungeon.player_life:
                user_life_check_result = 'pass'
        else:
            check_life = f'{emojis.CHECK_IGNORE} **LIFE**: -'

    elif dungeon_no == 11:
        if user_at < dungeon.player_at:
            user_at_check_result = 'fail'
        elif user_at >= dungeon.player_at:
            user_at_check_result = 'pass'
        if user_life < dungeon.player_life:
            if user_at_check_result == 'pass':
                if dungeon.player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (dungeon.player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (dungeon.player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                elif (dungeon.player_life - user_life) <= 200:
                    user_life_check_result = 'warn'
                else:
                    user_life_check_result = 'fail'
            else:
                if dungeon.player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (dungeon.player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (dungeon.player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                else:
                    user_life_check_result = 'fail'
        elif user_life >= dungeon.player_life:
            user_life_check_result = 'pass'

    elif dungeon_no == 12:
        if user_def < dungeon.player_def:
            user_def_check_result = 'fail'
        elif user_def >= dungeon.player_def:
            user_def_check_result = 'pass'
        if user_life < dungeon.player_life:
            if dungeon.player_life - user_life <= 10:
                user_life_check_result = 'passA'
            elif 11 <= (dungeon.player_life - user_life) <= 25:
                user_life_check_result = 'passB'
            elif 26 <= (dungeon.player_life - user_life) <= 50:
                user_life_check_result = 'passC'
            else:
                user_life_check_result = 'fail'
        elif user_life >= dungeon.player_life:
            user_life_check_result = 'pass'

    elif dungeon_no == 13:
        if user_life < dungeon.player_life:
            user_life_check_result = 'fail'
        else:
            user_life_check_result = 'pass'

    elif dungeon_no == 14:
        if user_def < dungeon.player_def:
            user_def_check_result = 'fail'
        elif user_def >= dungeon.player_def:
            user_def_check_result = 'pass'
        if user_life < dungeon.player_life:
            if dungeon.player_life - user_life <= 10:
                user_life_check_result = 'passA'
            elif 11 <= (dungeon.player_life - user_life) <= 25:
                user_life_check_result = 'passB'
            elif 26 <= (dungeon.player_life - user_life) <= 50:
                user_life_check_result = 'passC'
            else:
                user_life_check_result = 'fail'
        elif user_life >= dungeon.player_life:
            user_life_check_result = 'pass'

    if user_at_check_result == 'pass':
        check_at = f'{emojis.CHECK_OK} **AT**: {dungeon.player_at}'
    elif user_at_check_result == 'warn':
        check_at = f'{emojis.CHECK_WARN} **AT**: {dungeon.player_at}'
    elif user_at_check_result == 'fail':
        check_at = f'{emojis.CHECK_FAIL} **AT**: {dungeon.player_at}'
    elif user_at_check_result == 'ignore':
        check_at = f'{emojis.CHECK_IGNORE} **AT**: {dungeon.player_at}'

    if user_def_check_result == 'pass':
        check_def = f'{emojis.CHECK_OK} **DEF**: {dungeon.player_def}'
    elif user_def_check_result == 'warn':
        check_def = f'{emojis.CHECK_WARN} **DEF**: {dungeon.player_def}'
    elif user_def_check_result == 'fail':
        check_def = f'{emojis.CHECK_FAIL} **DEF**: {dungeon.player_def}'
    elif user_def_check_result == 'ignore':
        check_def = f'{emojis.CHECK_IGNORE} **DEF**: {dungeon.player_def}'

    if user_carry_def_check_result == 'pass':
        check_carry_def = f'{emojis.CHECK_OK} **Carry DEF**: {dungeon.player_carry_def}'
    elif user_carry_def_check_result == 'warn':
        check_carry_def = f'{emojis.CHECK_WARN} **Carry DEF**: {dungeon.player_carry_def}'
    elif user_carry_def_check_result == 'fail':
        check_carry_def = f'{emojis.CHECK_FAIL} **Carry DEF**: {dungeon.player_carry_def}'
    elif user_carry_def_check_result == 'ignore':
        check_carry_def = f'{emojis.CHECK_IGNORE} **Carry DEF**: {dungeon.player_carry_def}'

    if user_life_check_result == 'pass':
        check_life = f'{emojis.CHECK_OK} **LIFE**: {dungeon.player_life}'
    elif user_life_check_result == 'passA':
        check_life = f'{emojis.CHECK_OK} **LIFE**: {dungeon.player_life} • {emojis.LIFE_BOOST}**A**'
    elif user_life_check_result == 'passB':
        check_life = f'{emojis.CHECK_OK} **LIFE**: {dungeon.player_life} • {emojis.LIFE_BOOST}**B**'
    elif user_life_check_result == 'passC':
        check_life = f'{emojis.CHECK_OK} **LIFE**: {dungeon.player_life} • {emojis.LIFE_BOOST}**C**'
    elif user_life_check_result == 'warn':
        check_life = f'{emojis.CHECK_WARN} **LIFE**: {dungeon.player_life}'
    elif user_life_check_result == 'fail':
        check_life = f'{emojis.CHECK_FAIL} **LIFE**: {dungeon.player_life}'
    elif user_life_check_result == 'ignore':
        check_life = f'{emojis.CHECK_IGNORE} **LIFE**: {dungeon.player_life}'

    field_value = ''
    if not check_at == 'N/A':
        field_value =   f'{emojis.BP} {check_at}'
    if not check_def == 'N/A':
        field_value =   f'{field_value}\n{emojis.BP} {check_def}'
    if not check_carry_def == 'N/A':
        field_value =   f'{field_value}\n{emojis.BP} {check_carry_def}'
    if not check_life == 'N/A':
        field_value =   f'{field_value}\n{emojis.BP} {check_life}'
    field_value = field_value.strip()
    if field_value == '':
        if dungeon_no <= 15.2:
            field_value = f'{emojis.BP} Stats irrelevant'
        else:
            field_value = f'{emojis.BP} Stats unknown'

    user_stats_check_results = [
        ['AT',user_at_check_result],
        ['DEF', user_def_check_result],
        ['LIFE', user_life_check_result]
    ]
    player_stats_check = [
        dungeon.player_at,
        dungeon.player_def,
        dungeon.player_life
    ]

    if dungeon_no in (10,15,15.2):
        check_results = f'{emojis.BP} Stats are irrelevant for this dungeon'
        if dungeon_no == 10:
            check_results = (
                f'{check_results}\n'
                f'{emojis.BP} This dungeon has gear requirements (see {strings.SLASH_COMMANDS_GUIDE["dungeon guide"]})'
            )
        elif dungeon_no in (15,15.2):
            dungeon_no = str(dungeon_no).replace('.','-')
            check_results = (
                f'{check_results}\n'
                f'{emojis.BP} This dungeon has various requirements (see {strings.SLASH_COMMANDS_GUIDE["dungeon guide"]})'
            )
    elif dungeon_no == 11:
        if user_at_check_result == 'fail':
            check_results = (
                f'{emojis.BP} You are not yet ready for this dungeon\n'
                f'{emojis.BP} You should increase your **AT** to **{dungeon.player_at}**'
            )
            if user_life_check_result == 'fail':
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} You should increase your **LIFE** to **{dungeon.player_life}** or more'
                )
        else:
            if user_life_check_result == 'warn':
                check_results = (
                    f'{emojis.BP} Your **LIFE** is below recommendation (**{dungeon.player_life}**)\n'
                    f'{emojis.BP} You can still attempt the dungeon though, maybe you get lucky!'
                )
            elif user_life_check_result == 'fail':
                check_results = (
                    f'{emojis.BP} You are not yet ready for this dungeon\n'
                    f'{emojis.BP} You should increase your **LIFE** to **{dungeon.player_life}** or more'
                )
            else:
                check_results = (
                    f'{emojis.BP} Your stats are high enough for this dungeon\n'
                    f'{emojis.BP} Note that this dungeon is luck based, so you can still die'
                )
                if (user_life_check_result == 'passA'):
                    check_results = (
                        f'{check_results}\n'
                        f'{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost A to reach recommended **LIFE**'
                    )
                if (user_life_check_result == 'passB'):
                    check_results = (
                        f'{check_results}\n'
                        f'{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost B to reach recommended **LIFE**'
                    )
                if (user_life_check_result == 'passC'):
                    check_results = (
                        f'{check_results}\n'
                        f'{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost C to reach recommended **LIFE**'
                    )
        check_results = (
            f'{check_results}\n{emojis.BP} This dungeon has gear requirements (see {strings.SLASH_COMMANDS_GUIDE["dungeon guide"]})'
        )
    elif dungeon_no == 12:
        if (user_def_check_result == 'fail') or (check_life == 'fail'):
            check_results = f'{emojis.BP} You are not yet ready for this dungeon'
            if user_def_check_result == 'fail':
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} You should increase your **DEF** to **{dungeon.player_def}**'
                )
            if user_life_check_result == 'fail':
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} You should increase your **LIFE** to **{dungeon.player_life}** or more'
                )
        else:
            check_results = f'{emojis.BP} You are ready for this dungeon'
            if (user_life_check_result == 'passA'):
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost A to reach recommended **LIFE**'
                )
            if (user_life_check_result == 'passB'):
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost B to reach recommended **LIFE**'
                )
            if (user_life_check_result == 'passC'):
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost C to reach recommended **LIFE**'
                )
            check_results = (
                f'{check_results}\n'
                f'{emojis.BP} Note that higher **LIFE** will still help in beating the dungeon'
            )
        check_results = (
            f'{check_results}\n'
            f'{emojis.BP} This dungeon has gear requirements (see {strings.SLASH_COMMANDS_GUIDE["dungeon guide"]})'
        )
    elif dungeon_no == 13:
        if user_life_check_result == 'fail':
            check_results = (
                f'{emojis.BP} You are not yet ready for this dungeon\n'
                f'{emojis.BP} You should increase your **LIFE** to **{dungeon.player_life}** or more\n'
                f'{emojis.BP} The **LIFE** is for crafting the {emojis.SWORD_OMEGA} OMEGA Sword, not the dungeon\n'
                f'{emojis.BP} **Important**: This is **base LIFE**, before buying a {emojis.LIFE_BOOST} LIFE boost'
            )
        else:
            check_results = f'{emojis.BP} Your stats are high enough for this dungeon'
        check_results = (
            f'{check_results}\n'
            f'{emojis.BP} This dungeon has gear requirements (see {strings.SLASH_COMMANDS_GUIDE["dungeon guide"]})'
        )

    elif dungeon_no == 14:
        if (user_def_check_result == 'fail') or user_life_check_result == 'fail':
            check_results = f'{emojis.BP} You are not yet ready for this dungeon'

            if user_def_check_result == 'fail':
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} You should increase your **DEF** to **{dungeon.player_def}**'
                )
            if user_life_check_result == 'fail':
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} You should increase your **LIFE** to **{dungeon.player_life}** or more'
                )
        else:
            check_results = f'{emojis.BP} Your stats are high enough for this dungeon'
            if (user_life_check_result == 'passA'):
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost A to reach recommended **LIFE**'
                )
            if (user_life_check_result == 'passB'):
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost B to reach recommended **LIFE**'
                )
            if (user_life_check_result == 'passC'):
                check_results = (
                    f'{check_results}\n'
                    f'{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost C to reach recommended **LIFE**'
                )
        check_results = (
            f'{check_results}\n'
            f'{emojis.BP} This dungeon has gear requirements (see {strings.SLASH_COMMANDS_GUIDE["dungeon guide"]})\n'
            f'{emojis.BP} If you are using a helper bot, 1,500 LIFE or less are usually enough'
        )

    elif 16 <= dungeon_no <= 21:
        check_results = f'{emojis.BP} Stats for this dungeon are currently unknown'
    else:
        if user_carry_def_check_result == 'pass':
            check_results = f'{emojis.BP} You are ready **and** can carry other players'
            for check in user_stats_check_results:
                if (check[1] == 'ignore') or (check[1] == 'warn'):
                    check_results = (
                        f'{check_results}\n'
                        f'{emojis.BP} Your **{check[0]}** is low but can be ignored because of your DEF'
                    )
        elif (user_at_check_result == 'fail') or (user_def_check_result == 'fail') or (user_life_check_result == 'fail'):
            check_results = f'{emojis.BP} You are not yet ready for this dungeon'
            for x, check in enumerate(user_stats_check_results):
                if check[1] == 'fail':
                    check_results = (
                        f'{check_results}\n'
                        f'{emojis.BP} You should increase your **{check[0]}** to **{player_stats_check[x]}**'
                    )
            check_results = (
                f'{check_results}\n'
                f'{emojis.BP} However, you can still do this dungeon if you get carried'
            )
        elif ((user_at_check_result == 'pass') and (user_def_check_result == 'pass')
               and ((user_life_check_result == 'pass') or (user_life_check_result == 'passA')
                    or (user_life_check_result == 'passB') or (user_life_check_result == 'passC'))):
            check_results = f'{emojis.BP} Your stats are high enough for this dungeon'
            if (user_life_check_result == 'passA'):
                check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost A to reach recommended **LIFE**'
            if (user_life_check_result == 'passB'):
                check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost B to reach recommended **LIFE**'
            if (user_life_check_result == 'passC'):
                check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost C to reach recommended **LIFE**'

    return (field_value, check_results)


# --- Embeds ---
async def embed_dungeon_guide(dungeon_no: float) -> Tuple[discord.File, discord.Embed]:
    """Creates dungeon guide embed"""
    dungeon: database.Dungeon = await database.get_dungeon(dungeon_no)
    img_dungeon = image_url = image_name = None
    boss_life = time_limit = player_amount = key_price = description = requirements = strategy = tips = rewards = None
    notes = None

    if dungeon.boss_life is not None:
        boss_life = int(dungeon.boss_life) if dungeon.boss_life.is_integer() else dungeon.boss_life
    dungeon_no = dungeon.dungeon_no

    field_rec_stats = await functions.design_field_rec_stats(dungeon)
    field_rec_gear = await functions.design_field_rec_gear(dungeon)
    if field_rec_gear is None: field_rec_gear = f'{emojis.BP} None'

    # Time limit
    if dungeon.time_limit is not None:
        time_limit = format_timespan(dungeon.time_limit)
        if 1 <= dungeon_no <= 9:
            time_limit = f'{time_limit} per player'

    # Amount of players and boss stats
    player_amount = f'{emojis.BP} {dungeon.player_amount[0]}'
    if dungeon.player_amount[0] != dungeon.player_amount[1]:
        player_amount = f'{player_amount}-{dungeon.player_amount[1]}'
    if dungeon.player_amount in ((1,1),(2,2)):
        boss_life = '-' if boss_life is None else f'{boss_life:,}'
    else:
        boss_life = '-' if boss_life is None else f'{boss_life:,} per player'
    boss_at = '-' if dungeon.boss_at is None else f'~{dungeon.boss_at:,}'
    if 16 <= dungeon_no <= 20:
        boss_at = 'Unknown'
        boss_life = 'Unknown'
    if dungeon_no == 14: boss_life = f'2x {boss_life}'

    # Key price
    if dungeon.key_price is not None:
        key_price = f'{dungeon.key_price:,} coins'
    else:
        if dungeon_no != 21:
            key_price = f'You can only enter this dungeon with a {emojis.HORSE_T6} T6+ horse'

    # Requirements
    if 1 <= dungeon_no <= 9:
        requirements = f'{emojis.BP} {emojis.DUNGEON_KEY_1} Dungeon key **OR** {emojis.HORSE_T6} T6+ horse'
    elif 10 <= dungeon_no <= 15.2:
        requirements = f'{emojis.BP} {emojis.DUNGEON_KEY_10} Dungeon key **OR** {emojis.HORSE_T6} T6+ horse'
    elif dungeon_no == 21:
        requirements = f'{emojis.BP} {emojis.HORSE_T9} T9+ horse (T10 recommended)'

    else:
        requirements = f'{emojis.BP} {emojis.HORSE_T6} T6+ horse'
    if dungeon_no in (10, 11, 13, 15, 15.2):
        requirements = f'{requirements}\n{emojis.BP} {dungeon.player_sword.emoji} {dungeon.player_sword.name}'
    if dungeon_no == 21:
        requirements = (
            f'{requirements}\n'
            f'{emojis.BP} {emojis.SWORD_GODLYCOOKIE} GODLY cookie (`eat` it to start the fight)\n'
            f'{emojis.BP} No gear (having a sword or armor results in instant death)\n'
            f'{emojis.BP} 15m+ {emojis.LOG} wooden logs to sell during the fight\n'
            f'{emojis.BP} **4** T10 or higher pets to send on adventures\n'
            f'{emojis.DETAIL} At least **3** of these pets **must** have the {emojis.SKILL_EPIC} EPIC skill\n'
            f'{emojis.DETAIL} Only **1** can have a {emojis.SKILL_TRAVELER} time traveler skill\n'
            f'{emojis.DETAIL} If a pet has the {emojis.SKILL_TRAVELER} time traveler skill, it must also be '
            f'{emojis.SKILL_EPIC} EPIC\n'
            f'{emojis.BP} No active pet adventures before the fight\n'
            f'{emojis.BP} 3,000+ {emojis.STAT_COOLNESS} coolness\n'
            f'{emojis.BP} 1,000+ {emojis.LIFE_POTION} life potions'
        )
    if dungeon_no in (10, 12, 14, 15):
        requirements = f'{requirements}\n{emojis.BP} {dungeon.player_armor.emoji} {dungeon.player_armor.name}'
    if dungeon_no in (15, 15.2):
        requirements = (
            f'{requirements}\n'
            f'{emojis.BP} {emojis.PET_CAT} T5+ cat pet\n'
            f'{emojis.BP} {emojis.PET_DOG} T5+ dog pet\n'
            f'{emojis.BP} {emojis.PET_DRAGON} T5+ dragon pet'
        )
    if dungeon.tt is not None:
        if dungeon.tt != 0: requirements = f'{requirements}\n{emojis.BP} {emojis.TIME_TRAVEL} TT {dungeon.tt:,}+'
    if dungeon_no == 15.2:
        requirements = f'{requirements}\n{emojis.BP} {emojis.STAT_COOLNESS} 2,000+ coolness'

    # Strategy
    if 1 <= dungeon_no <= 9:
        strategy = f'{emojis.BP} Use `stab` or `power`'
    elif dungeon_no == 10:
         strategy = (
            f'{emojis.BP} The player that starts the dungeon gets the attacker role\n'
            f'{emojis.BP} The other player gets the defender role\n'
            f'{emojis.BP} Attacker command sequence:\n'
            f'{emojis.BLANK} `charge edgy sword` x20\n'
            f'{emojis.BLANK} `attack`\n'
            f'{emojis.BP} Defender command sequence:\n'
            f'{emojis.BLANK} `weakness spell`\n'
            f'{emojis.BLANK} `protect` x3\n'
            f'{emojis.BLANK} `charge edgy armor` x2\n'
            f'{emojis.BLANK} `protect`\n'
            f'{emojis.BLANK} `invulnerability`\n'
            f'{emojis.BLANK} `healing spell`\n'
            f'{emojis.BLANK} `protect` x7\n'
            f'{emojis.BP} Note: The defender will die before the boss does'
        )
    elif dungeon_no == 13:
        strategy = (
            f'{emojis.BP} You start in room 1, 2 or 3\n'
            f'{emojis.BP} Your goal is to reach the dragon\'s room\n'
            f'{emojis.BP} In each room you will be asked one question\n'
            f'{emojis.BP} Your answer determines your next room\n'
            f'{emojis.BP} Refer to the image below for a walkthrough\n'
            f'{emojis.BP} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Dungeon_13)'
        )
    elif dungeon_no == 14:
        strategy = f'{emojis.BP} https://epic-rpg.fandom.com/wiki/Dungeon_14'
    elif dungeon_no == 15:
        strategy = f'{emojis.BP} https://epic-rpg.fandom.com/wiki/Dungeon_15.1'
    elif dungeon_no == 15.2:
        strategy = f'{emojis.BP} https://epic-rpg.fandom.com/wiki/Dungeon_15.2'
    elif 16 <= dungeon_no <= 19:
        strategy = f'{emojis.BP} Use `power`'
    elif dungeon_no == 20:
        strategy = (
            f'{emojis.BP} Use `power` if you can survive the damage\n'
            f'{emojis.BP} Use `sacrifice` if you are about to die'
        )

    # Tips
    if dungeon_no == 11:
        tips = (
            f'{emojis.BP} You can move left, right, up, down or pass\n'
            f'{emojis.BP} Your goal is to reach and hit the boss until it dies\n'
            f'{emojis.BP} Each point of AT you have does 1 damage to the boss\n'
            f'{emojis.BP} You can only attack if you stand right next to the boss\n'
            f'{emojis.BP} After you hit the boss, your position will reset\n'
            f'{emojis.BP} If you end up on a fireball, you take 100 damage\n'
            f'{emojis.BP} If you pass a turn, you take 10 damage\n'
            f'{emojis.BP} The board scrolls down one line with every move you make\n'
            f'{emojis.BP} You do **not** move down with the board\n'
            f'{emojis.BP} **The board moves first** when you make a move\n'
            f'{emojis.BP} Check the image below to see the movement behaviour\n'
            f'{emojis.BP} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Dungeon_11)'
        )
    elif dungeon_no == 12:
        tips = f'{emojis.BP} https://epic-rpg.fandom.com/wiki/Dungeon_12'

    # Rewards
    if 1 <= dungeon_no <= 14:
        rewards = f'{emojis.BP} Unlocks area {dungeon_no + 1:g} (see {strings.SLASH_COMMANDS_GUIDE["area guide"]})'
    elif dungeon_no == 15:
        rewards = (
            f'{emojis.BP} {emojis.TIME_KEY} TIME key to unlock time jumping (see '
            f'{strings.SLASH_COMMANDS_GUIDE["time travel guide"]})'
        )
    elif dungeon_no == 15.2:
        rewards = (
            f'{emojis.BP} Unlocks the TOP (see {strings.SLASH_COMMANDS_GUIDE["area guide"]})\n'
            f'{emojis.BP} {emojis.TIME_DRAGON_ESSENCE} TIME dragon essence\n'
            f'{emojis.DETAIL} Used to craft the {emojis.SWORD_GODLYCOOKIE} GODLY cookie to beat the EPIC NPC\n'
            f'{emojis.DETAIL} Used in the `shop` to buy {emojis.EPIC_JUMP} EPIC jump to get to area 16\n'
        )
    elif 16 <= dungeon_no <= 20:
        if 16 <= dungeon_no <= 19:
            rewards = (
                f'{emojis.BP} {emojis.EPIC_JUMP} EPIC jump to move to area {dungeon_no + 1:g} (if unsealed)'
            )
        else:
            rewards = (
                f'{emojis.BP} {emojis.EPIC_JUMP} EPIC jump'
            )
        rewards = (
            f'{rewards}\n'
            f'{emojis.DETAIL} Note: You can not have more than 1 in your inventory.\n'
            f'{emojis.BP} Unlocks the ability to get 1 additional {emojis.TIME_TRAVEL} TT every {21 - dungeon_no:g} TTs.\n'
            f'{emojis.DETAIL} This reward is permanent.\n'
            f'{emojis.BP} Chance to get a {emojis.PET_VOIDOG} VOIDog pet\n'
        )
    elif dungeon_no == 21:
        rewards = (
            f'{emojis.BP} {emojis.EPIC_JUMP} EPIC jump to move to area 16 (if unsealed)\n'
            f'{emojis.BP} Unlocks the ability to buy {emojis.EPIC_JUMP} EPIC jumps in the `shop`.\n'
            f'{emojis.DETAIL} This reward is permanent.'
        )

    # Notes
    if dungeon_no == 15.2:
        notes = (
            f'{emojis.BP} To enter this dungeon, you need to equip the {emojis.SWORD_GODLY} GODLY sword and start D15.\n'
            f'{emojis.DETAIL} Once you beat part 1, part 2 will automatically start.\n'
        )
    elif 16 <= dungeon_no <= 20:
        notes = (
            f'{emojis.BP} Carrying is not possible in this dungeon\n'
            f'{emojis.BP} You can redo this dungeon as long as you are in area {dungeon_no:g}\n'
        )
    elif dungeon_no == 21:
        notes = (
            f'{emojis.BP} This fight does not need your dungeon cooldown\n'
            f'{emojis.BP} The {emojis.SWORD_GODLYCOOKIE} GODLY cookie is **one time use**\n'
            f'{emojis.BP} The {emojis.EPIC_JUMP} EPIC jump you get is lost after TT\n'
        )

    # Images
    if dungeon_no == 11:
        image_url = 'https://erg.zoneseven.ch/ïmages/dungeon11.png'
        image_name = 'MOVEMENT BEHAVIOUR'
    elif dungeon_no == 13:
        image_url = 'https://erg.zoneseven.ch/images/dungeon13.png'
        image_name = 'WALKTHROUGH'

    dungeon_no = 15.1 if dungeon.dungeon_no == 15 else dungeon.dungeon_no
    title = f'DUNGEON {f"{dungeon_no:g}".replace(".","-")}' if dungeon_no != 21 else 'THE EPIC NPC FIGHT'

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = title,
        description = dungeon.description
    )

    embed.set_footer(text='Use "/dungeon check" to see if you are ready for this dungeon')
    embed.add_field(name='BOSS', value=f'{emojis.BP} {dungeon.boss_emoji} {dungeon.boss_name}', inline=False)
    if player_amount is not None:
        embed.add_field(name='PLAYERS', value=player_amount, inline=False)
    if time_limit is not None:
        embed.add_field(name='TIME LIMIT', value=f'{emojis.BP} {time_limit}', inline=False)
    if rewards is not None:
        embed.add_field(name='REWARDS', value=rewards, inline=False)
    if requirements is not None:
        embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    if key_price is not None:
        embed.add_field(name='DUNGEON KEY PRICE', value=f'{emojis.BP} {key_price}', inline=False)
    embed.add_field(
        name='BOSS STATS',
        value=(
            f'{emojis.BP} {emojis.STAT_AT} **AT**: {boss_at}\n'
            f'{emojis.BP} {emojis.STAT_LIFE} **LIFE**: {boss_life}'
        ),
            inline=False
    )
    embed.add_field(name='RECOMMENDED GEAR', value=field_rec_gear, inline=True)
    embed.add_field(name='RECOMMENDED STATS', value=field_rec_stats, inline=True)
    if strategy is not None: embed.add_field(name='STRATEGY', value=strategy, inline=False)
    if tips is not None: embed.add_field(name='TIPS', value=tips, inline=False)
    if notes is not None: embed.add_field(name='NOTE', value=notes, inline=False)
    if image_url is not None:
        embed.set_image(url=image_url)
        embed.add_field(name=image_name, value=f'** **', inline=False)
    return embed


async def embed_dungeon_check(dungeon_no: float, user_at: int, user_def: int, user_life: int) -> discord.Embed:
    """Embed with dungeon check"""
    legend = (
        f'{emojis.BP} {emojis.CHECK_OK} : Stat is above recommendation\n'
        f'{emojis.BP} {emojis.CHECK_IGNORE} : Stat is below rec. but you are above carry DEF\n'
        f'{emojis.BP} {emojis.CHECK_FAIL} : Stat is below recommendation\n'
        f'{emojis.BP} {emojis.CHECK_WARN} : Stat is below rec. but with a lot of luck it _might_ work\n'
        f'{emojis.BP} {emojis.LIFE_BOOST} : LIFE boost you have to buy to reach recommendation'
    )
    stats = (
        f'{emojis.BP} {emojis.STAT_AT} **AT**: {user_at:,}\n'
        f'{emojis.BP} {emojis.STAT_DEF} **DEF**: {user_def:,}\n'
        f'{emojis.BP} {emojis.STAT_LIFE} **LIFE**: {user_life:,}'
    )
    notes = (
        f'{emojis.BP} You can ignore this check for D1-D9 if you get carried\n'
        f'{emojis.BP} You can **not** get carried in D16-D20, the boss gets stronger if someone dies!\n'
        f'{emojis.BP} This check does **not** take into account required gear for D10+!\n'
    )
    dungeon_no_str = f'DUNGEON {dungeon_no:g}' if dungeon_no != 21 else 'EPIC NPC FIGHT'
    dungeon_no_str = dungeon_no_str.replace('.','-')
    dungeon_check_results, dungeon_check_details = await design_field_dungeon_check(dungeon_no, user_at, user_def, user_life)
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'{dungeon_no_str} STATS CHECK',
    )
    embed.set_footer(text='Use "/dungeon guide" to see more details about this dungeon')
    embed.add_field(name='YOUR STATS', value=stats, inline=False)
    embed.add_field(name='CHECK RESULT', value=dungeon_check_results, inline=False)
    if dungeon_check_details != '':
        embed.add_field(name='DETAILS', value=dungeon_check_details, inline=False)
    embed.add_field(name='LEGEND', value=legend, inline=False)
    return embed