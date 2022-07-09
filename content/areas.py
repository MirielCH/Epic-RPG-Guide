# areas.py

import asyncio
from typing import Optional, Union

import discord
from discord.ext import commands

import database
from resources import emojis, functions, settings, strings, views


# --- Commands ---
async def command_area_guide(ctx: discord.ApplicationContext, area_no: int, tt_no: Optional[int] = None,
                             ascension: Optional[str] = None, length: Optional[str] = None,
                             switch_view: Optional[discord.ui.View] = None) -> None:
    """Area guide command"""
    full_guide = user = interaction = None
    if switch_view is not None:
        user = getattr(switch_view, 'db_user', None)
        full_guide = getattr(switch_view, 'full_guide', True)
        interaction = getattr(switch_view, 'interaction', None)
    if user is None:
        user: database.User = await database.get_user(ctx.author.id)
    if full_guide is None:
        full_guide = True if length == strings.CHOICE_GUIDE_FULL else False
    if tt_no is not None: user.tt = tt_no
    if ascension is not None:
        user.ascended = True if ascension == strings.CHOICE_ASCENDED else False
    if user.tt == 0 and user.ascended:
        await ctx.respond(
            f'Invalid combination. You can\'t ascend in {emojis.TIME_TRAVEL} TT 0.',
            ephemeral=True
        )
        return
    if user.tt >= 25 and not user.ascended:
        await ctx.respond(
            f'Invalid combination. {emojis.TIME_TRAVEL} TT 25+ needs to be ascended.',
            ephemeral=True
        )
        return
    view = views.AreaGuideView(ctx, area_no, user, full_guide, embed_area_guide)
    embed = await embed_area_guide(ctx, area_no, user, full_guide)
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


async def command_area_check(bot: discord.Bot, ctx: discord.ApplicationContext, area_no: int,
                             user_at: Optional[int] = None, user_def: Optional[int] = None,
                             user_life: Optional[int] = None,
                             switch_view: Optional[discord.ui.View] = None)  -> None:
    """Area check command"""
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
                f'**{ctx.author.name}**, please use {emojis.EPIC_RPG_LOGO_SMALL}</profile:958554803422781460> '
                f'or {emojis.EPIC_RPG_LOGO_SMALL}</stats:958558818831315004>\n'
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
    view = views.AreaCheckView(bot, ctx, area_no, user_at, user_def, user_life, embed_area_check)
    embed = await embed_area_check(area_no, user_at, user_def, user_life)
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
async def design_field_quick_guide(ctx: commands.Context, area: database.Area, dungeon: database.Dungeon,
                             tt: database.TimeTravel, user: database.User) -> str:
    """Returns the quick guide for the area embed"""
    quick_guide_sword = quick_guide_armor = quick_guide_enchant_sword = quick_guide_enchant_armor = quick_guide = ''

    action = 'Craft' if area.area_no < 11 else 'Forge'
    if area.upgrade_sword:
        quick_guide_sword = f'{emojis.BP} {action} {dungeon.player_sword.emoji} {dungeon.player_sword.name}'
    if area.upgrade_armor:
        quick_guide_armor = f'{emojis.BP} {action} {dungeon.player_armor.emoji} {dungeon.player_armor.name}'
    if dungeon.player_sword_enchant is not None:
        if area.upgrade_sword:
            quick_guide_enchant_sword = f' and enchant to {dungeon.player_sword_enchant}'
            if dungeon.player_sword_enchant != 'VOID':
                quick_guide_enchant_sword = f'{quick_guide_enchant_sword} or higher'
        elif area.upgrade_sword_enchant:
                quick_guide_enchant_sword = (
                    f'{emojis.BP} Enchant {dungeon.player_sword.emoji} {dungeon.player_sword.name} '
                    f'to {dungeon.player_sword_enchant}'
                )
                if dungeon.player_sword_enchant != 'VOID':
                    quick_guide_enchant_sword = f'{quick_guide_enchant_sword} or higher'

    if dungeon.player_armor_enchant is not None:
        if area.upgrade_armor:
            quick_guide_enchant_armor = f' and enchant to {dungeon.player_armor_enchant}'
            if dungeon.player_armor_enchant != 'VOID':
                quick_guide_enchant_armor = f'{quick_guide_enchant_armor} or higher'
        elif area.upgrade_armor_enchant:
                quick_guide_enchant_armor = (
                    f'{emojis.BP} Enchant {dungeon.player_armor.emoji} {dungeon.player_armor.name} to '
                    f'{dungeon.player_armor_enchant}'
                )
                if dungeon.player_armor_enchant != 'VOID':
                    quick_guide_enchant_armor = f'{quick_guide_enchant_armor} or higher'

    if area.area_no == 21:
        quick_guide_sword = (
            f'{emojis.BP} Craft {emojis.SWORD_GODLYCOOKIE} GODLY cookie if you want to do the EPIC NPC fight'
        )

    if tt.tt_area == area.area_no:
        quick_guide = (
            f'{emojis.BP} {emojis.TIME_TRAVEL} Prepare for time travel '
            f'(see {emojis.LOGO}`/time travel bonuses`)'
        )
        return quick_guide

    if ((area.area_no == 3 and tt.a3_fish > 0) or (area.area_no == 5 and tt.a5_apple > 0)):
        quick_guide = f'{emojis.BP} Farm the materials mentioned below'

    if dungeon.player_level is not None and dungeon.dungeon_no <= 15.2:
        quick_guide = f'{quick_guide}\n{emojis.BP} Reach level {dungeon.player_level:,}'
    if area.area_no == 9:
        quick_guide = (
            f'{quick_guide}\n'
            f'{emojis.BP} Go back to previous areas if you are missing materials for crafting the armor '
            f'(see {emojis.LOGO}`/monster drops`)'
        )
    if quick_guide_sword != '' or quick_guide_enchant_sword != '':
        quick_guide = f'{quick_guide}\n{quick_guide_sword}{quick_guide_enchant_sword}'
    if quick_guide_armor != '' or quick_guide_enchant_armor != '':
        quick_guide = f'{quick_guide}\n{quick_guide_armor}{quick_guide_enchant_armor}'
        if area.area_no == 7: quick_guide = f'{quick_guide} **(*)**'
    quick_guide = f'{quick_guide}\n{emojis.BP} Check below to see which lootboxes to buy, keep or open'
    if area.area_no in (3,5,7,8,9,10,11) and tt.tt_area != area.area_no:
        quick_guide = f'{quick_guide}\n{emojis.BP} Trade before leaving (see trades below)'

    return quick_guide


async def design_field_debuffs(area: database.Area) -> str:
    """Returns the debuffs for the area embed"""
    if area.area_no < 16 or area.area_no > 20: return None

    all_area_caps = {
        16: ('17292 AT, 11528 DEF, 25k LIFE'),
        17: ('72050 AT, 48994 DEF, 60k LIFE'),
        18: ('288200 AT, 201740 DEF, 300k LIFE'),
        19: ('1m AT, 600k DEF, 1.5m LIFE'),
        20: ('4.323m AT, 4.323m DEF, 10m LIFE'),
    } # Including VOID enchants and horse

    debuffs = (
        f'{emojis.BP} AT, DEF and LIFE are capped\n'
        f'{emojis.BLANK} Equipment ignores this cap'
    )
    if area.area_no == 16:
        debuffs = (
            f'{debuffs}\n'
            f'{emojis.BP} Every command drains 1% LIFE\n'
            f'{emojis.BP} `heal` reduces max LIFE\n'
            f'{emojis.BP} Lootboxes contain no items\n'
        )
    elif area.area_no == 17:
        debuffs = (
            f'{debuffs}\n'
            f'{emojis.BP} Every command drains 0.75% of your levels\n'
            f'{emojis.BP} `farm` has a high chance to give no items\n'
            f'{emojis.BP} `craft`, `dismantle`, `forge`, `cook`, `eat`, `withdraw` and `deposit` can fail\n'
            f'{emojis.BLANK }If this happens, you will lose the items from that command'
        )
    elif area.area_no == 18:
        debuffs = (
            f'{debuffs}\n'
            f'{emojis.BP} Monsters can drop a negative amount of items\n'
            f'{emojis.BP} Command cooldowns are randomized when the area is unsealed\n'
            f'{emojis.BP} Enchants may randomly disappear / reappear\n'
            f'{emojis.BP} `cook` has a chance to have the opposite effect\n'
        )
    elif area.area_no == 19:
        debuffs = (
            f'{debuffs}\n'
            f'{emojis.BP} Items have a chance to randomly vanish from inventory\n'
            f'{emojis.BP} `dice` and `coinflip` do not work properly\n'
            f'{emojis.BP} `heal`, `cook`, `farm` and all work commands do not work at all\n'
            f'{emojis.BP} Your horse buff is not available\n'
        )
    elif area.area_no == 20:
        debuffs = (
            f'{debuffs}\n'
            f'{emojis.BP} Every command drains 500 profession XP from a random profession\n'
            f'{emojis.BP} Every command has a chance of removing 1 {emojis.TIME_TRAVEL} TT\n'
            f'{emojis.BP} Your horse has a chance of losing levels\n'
            f'{emojis.BP} Recently obtained pets (up to T5) have a chance of losing a tier or vanishing\n'
            f'{emojis.BP} `time travel` and `super time travel` do not work\n'
            f'{emojis.BP} Command cooldowns can randomly change and be displayed wrong\n'
            f'{emojis.BP} While this area is unsealed, A20 monsters have a 0.01% chance of appearing in all areas '
            f'down to A1\n'
        )

    return debuffs


async def design_field_work_commands(area: database.Area, user: database.User) -> str:
    """Returns the best work commands for the area embed"""

    work_commands = None
    emoji = emojis.EPIC_RPG_LOGO_SMALL

    if 16 <= area.area_no <= 20:
        if area.area_no in (16,18):
            work_commands = (
                f'{emojis.BP} {emoji}`/bigboat` if you need {emojis.FISH_SUPER} SUPER fish\n'
                f'{emojis.BP} {emoji}`/chainsaw` otherwise'
            )
        elif area.area_no in (17,20):
            work_commands = f'{emojis.BP} {emoji}`/chainsaw`'
        elif area.area_no == 19:
            work_commands = None
        return work_commands

    if user.tt in (0,1):
        money_nohorse = area.money_tt1_nohorse
        money_t6horse = area.money_tt1_t6horse
    elif user.tt in (2,3):
        money_nohorse = area.money_tt3_nohorse
        money_t6horse = area.money_tt3_t6horse
    elif user.tt in (4,5,6,7,8):
        money_nohorse = area.money_tt5_nohorse
        money_t6horse = area.money_tt5_t6horse
    else:
        money_nohorse = area.money_tt10_nohorse
        money_t6horse = area.money_tt10_t6horse

    if not user.ascended or (user.ascended and user.tt == 1):
        if user.tt == 0 and area.area_no == 11:
            work_commands = (
                f'{emojis.BP} {emoji}`/drill` if you need coins\n'
                f'{emojis.BP} {emoji}`/chainsaw` otherwise'
            )
        elif user.tt == 2 and 6 <= area.area_no <= 8:
            work_commands = (
               f'{emojis.BP} {emoji}`/pickaxe`'
            )
        else:
            if money_nohorse is None:
                work_commands = f'{emojis.BP} {emoji}`{area.work_cmd_rich}`'
            else:
                if user.tt < 25:
                    work_commands = (
                        f'{emojis.BP} {emoji}`{area.work_cmd_poor}` if < {money_nohorse}m coins and horse is < T6\n'
                        f'{emojis.BP} {emoji}`{area.work_cmd_poor}` if < {money_t6horse}m coins and horse is T6+'
                    )
                else:
                    work_commands = (
                        f'{emojis.BP} {emoji}`{area.work_cmd_poor}` if < {money_t6horse}m coins'
                    )
                work_commands = f'{work_commands}\n{emojis.BP} {emoji}`{area.work_cmd_rich}` otherwise'

    if user.ascended:
        if 1 <= area.area_no <= 9:
            if user.tt == 1:
                work_commands = f'{emojis.BP} {emoji}`/chainsaw`'
            elif 1 <= area.area_no <= 3:
                work_commands = f'{emojis.BP} {emoji}`/dynamite`'
            elif 4 <= area.area_no <= 5:
                work_commands = (
                    f'{emojis.BP} {emoji}`/chainsaw` if worker 115 or higher\n'
                    f'{emojis.BP} {emoji}`/dynamite` otherwise'
                )
            elif 6 <= area.area_no <= 7:
                work_commands = (
                    f'{emojis.BP} {emoji}`/greenhouse` if worker 102 or higher\n'
                    f'{emojis.BP} {emoji}`/dynamite` otherwise'
                )
            elif area.area_no == 8:
                work_commands = (
                    f'{emojis.BP} {emoji}`/chainsaw` if worker 109 or higher\n'
                    f'{emojis.BP} {emoji}`/dynamite` otherwise'
                )
            elif area.area_no == 9:
                work_commands = (
                    f'{emojis.BP} {emoji}`/greenhouse` if worker 107 or higher\n'
                    f'{emojis.BP} {emoji}`/dynamite` otherwise'
                )
        elif area.area_no == 10:
            if user.tt == 1:
                work_commands = f'{emojis.BP} {emoji}`/chainsaw`'
            else:
                work_commands = (
                    f'{emojis.BP} {emoji}`/dynamite` if you have all the {emojis.LOG_ULTRA} ULTRA logs you need for forging\n'
                    f'{emojis.BP} {emoji}`/chainsaw` otherwise'
                )
        elif area.area_no == 11:
            if user.tt == 1:
                work_commands = f'{emojis.BP} {emoji}`/chainsaw`'
            else:
                work_commands = (
                    f'{emojis.BP} {emoji}`/dynamite` if you have all the {emojis.LOG_ULTRA} ULTRA logs you need for forging\n'
                    f'{emojis.BP} {emoji}`/chainsaw` otherwise'
                )
        else:
            work_commands = (
                f'{emojis.BP} {emoji}`/dynamite` if you need coins\n'
                f'{emojis.BP} {emoji}`/chainsaw` otherwise'
            )

    return work_commands


async def design_field_lootboxes(area: database.Area, user: database.User) -> str:
    """Returns the lootbox guide for the area embed"""
    buy_tt0 = 'Whatever lootbox you have unlocked and can afford'

    if 1 <= area.area_no <= 2:
        if user.tt < 25:
            lootboxes = (
                f'{emojis.BP} Buy: {buy_tt0 if user.tt == 0 else f"{emojis.LB_EDGY} EDGY"}\n'
                f'{emojis.BP} Keep: {emojis.LB_RARE} Rare and {emojis.LB_EPIC} EPIC until A3\n'
                f'{emojis.BP} Keep: {emojis.LB_EDGY} EDGY until A5\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
        else:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: {emojis.LB_RARE} Rare and {emojis.LB_EPIC} EPIC until A3\n'
                f'{emojis.BP} Keep: {emojis.LB_EDGY} EDGY until A5\n'
                f'{emojis.BP} Keep: 12 {emojis.LB_OMEGA} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_GODLY} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )

    elif area.area_no == 3:
        if user.tt < 25:
            lootboxes = (
                f'{emojis.BP} Buy: {buy_tt0 if user.tt == 0 else f"{emojis.LB_EDGY} EDGY"}\n'
                f'{emojis.BP} Keep: {emojis.LB_EDGY} EDGY until A5\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
        else:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: {emojis.LB_EDGY} EDGY until A5\n'
                f'{emojis.BP} Keep: 12 {emojis.LB_OMEGA} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_GODLY} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )

    elif area.area_no == 4:
        if user.tt < 25:
            lootboxes = (
                f'{emojis.BP} Buy: {buy_tt0 if user.tt == 0 else f"{emojis.LB_EDGY} EDGY"}\n'
                f'{emojis.BP} Keep: {emojis.LB_EPIC} EPIC and {emojis.LB_EDGY} EDGY until A5\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
        else:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: {emojis.LB_EPIC} EPIC and {emojis.LB_EDGY} EDGY until A5\n'
                f'{emojis.BP} Keep: 12 {emojis.LB_OMEGA} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_GODLY} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )

    elif area.area_no == 5:
        if user.tt < 25:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Open: All lootboxes'
            )
        else:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: 12 {emojis.LB_OMEGA} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_GODLY} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )

    elif area.area_no == 6:
        if user.tt < 10:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: {emojis.LB_EDGY} EDGY until A7\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
        elif 10 <= user.tt <= 24:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: {emojis.LB_EDGY} EDGY until A7\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_OMEGA} OMEGA for {emojis.ARMOR_OMEGA} OMEGA Armor\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
        else:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: {emojis.LB_EDGY} EDGY until A7\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_OMEGA} OMEGA for {emojis.ARMOR_OMEGA} OMEGA Armor\n'
                f'{emojis.BP} Keep: 12 {emojis.LB_OMEGA} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_GODLY} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )

    elif 7 <= area.area_no <= 9:
        if user.tt < 10:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Open: All lootboxes'
            )
        elif 10 <= user.tt <= 24:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_OMEGA} OMEGA for {emojis.ARMOR_OMEGA} OMEGA Armor\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
        else:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_OMEGA} OMEGA for {emojis.ARMOR_OMEGA} OMEGA Armor\n'
                f'{emojis.BP} Keep: 12 {emojis.LB_OMEGA} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_GODLY} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )

    elif area.area_no == 10:
        if user.tt == 0:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Open: All lootboxes'
            )
        elif 1 <= user.tt <= 9:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: {emojis.LB_OMEGA} OMEGA until A11 if you already have an ULTRA '
                f'log for the EDGY sword\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
        elif 10 <= user.tt <= 24:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_OMEGA} OMEGA for {emojis.ARMOR_OMEGA} OMEGA Armor\n'
                f'{emojis.BP} Keep: {emojis.LB_OMEGA} OMEGA until A11 if you already have an ULTRA '
                f'log for the EDGY sword\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
        else:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_OMEGA} OMEGA for {emojis.ARMOR_OMEGA} OMEGA Armor\n'
                f'{emojis.BP} Keep: 12 {emojis.LB_OMEGA} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Keep: {emojis.LB_OMEGA} OMEGA until A11 if you already have an ULTRA '
                f'log for the EDGY sword\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_GODLY} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )

    elif 11 <= area.area_no <= 14:
        if user.tt < 10:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Open: All lootboxes'
            )
        elif 10 <= user.tt <= 24:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_OMEGA} OMEGA for {emojis.ARMOR_OMEGA} OMEGA Armor\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
        else:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_OMEGA} OMEGA for {emojis.ARMOR_OMEGA} OMEGA Armor\n'
                f'{emojis.BP} Keep: 12 {emojis.LB_OMEGA} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_GODLY} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
    elif area.area_no == 15:
        if user.tt < 25:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Open: All lootboxes'
            )
        else:
            lootboxes = (
                f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
                f'{emojis.BP} Keep: 12 {emojis.LB_OMEGA} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Keep: 1 {emojis.LB_GODLY} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.BP} Open: All lootboxes you don\'t need to keep'
            )
    elif area.area_no == 16:
        lootboxes = (
            f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
            f'{emojis.BP} Open: **Nothing** because of the debuff'
        )
    elif area.area_no > 16:
        lootboxes = (
            f'{emojis.BP} Buy: {emojis.LB_EDGY} EDGY\n'
            f'{emojis.BP} Open: All lootboxes'
        )

    return lootboxes


async def design_field_area_check(area_no: int, user_at: int, user_def: int, user_life: int) -> str:
    """Returns a check result field value for one area for the area check embed"""
    area: database.Area = await database.get_area(area_no)
    user_at_def = user_at + user_def
    hunt_dmg_min = area.hunt_dmg[0]
    hunt_dmg_max = area.hunt_dmg[1]
    hunt_dmg_min_hm = functions.round_school(hunt_dmg_min*1.7)
    hunt_dmg_max_hm = functions.round_school(hunt_dmg_max*1.7)
    adv_dmg_min = area.adv_dmg[0]
    adv_dmg_max = area.adv_dmg[1]
    adv_dmg_min_hm = functions.round_school(adv_dmg_min*1.7)
    adv_dmg_max_hm = functions.round_school(adv_dmg_max*1.7)

    hunt_taken_dmg_min = hunt_dmg_min - user_at_def
    hunt_taken_dmg_min_hm = hunt_dmg_min_hm - user_at_def
    hunt_taken_dmg_max = hunt_dmg_max - user_at_def
    hunt_taken_dmg_max_hm = hunt_dmg_max_hm - user_at_def
    adv_taken_dmg_min = adv_dmg_min - user_at_def
    adv_taken_dmg_max = adv_dmg_max - user_at_def
    adv_taken_dmg_min_hm = adv_dmg_min_hm - user_at_def
    adv_taken_dmg_max_hm = adv_dmg_max_hm - user_at_def

    if hunt_taken_dmg_min < 0: hunt_taken_dmg_min = 0
    if hunt_taken_dmg_min_hm < 0: hunt_taken_dmg_min_hm = 0
    if hunt_taken_dmg_max < 0: hunt_taken_dmg_max = 0
    if hunt_taken_dmg_max_hm < 0: hunt_taken_dmg_max_hm = 0
    if adv_taken_dmg_min < 0: adv_taken_dmg_min = 0
    if adv_taken_dmg_min_hm < 0: adv_taken_dmg_min_hm = 0
    if adv_taken_dmg_max < 0: adv_taken_dmg_max = 0
    if adv_taken_dmg_max_hm < 0: adv_taken_dmg_max_hm = 0

    if hunt_taken_dmg_max == 0:
        hunt_emoji = emojis.CHECK_OK
    elif hunt_taken_dmg_max < user_life:
        hunt_emoji = emojis.CHECK_IGNORE
    elif hunt_taken_dmg_min < user_life:
        hunt_emoji = emojis.CHECK_WARN
    else:
        hunt_emoji = emojis.CHECK_FAIL
    if hunt_taken_dmg_max_hm == 0:
        hunt_hm_emoji = emojis.CHECK_OK
    elif hunt_taken_dmg_max_hm < user_life:
        hunt_hm_emoji = emojis.CHECK_IGNORE
    elif hunt_taken_dmg_min_hm < user_life:
        hunt_hm_emoji = emojis.CHECK_WARN
    else:
        hunt_hm_emoji = emojis.CHECK_FAIL

    if adv_taken_dmg_max == 0:
        adv_emoji = emojis.CHECK_OK
    elif adv_taken_dmg_max < user_life:
        adv_emoji = emojis.CHECK_IGNORE
    elif adv_taken_dmg_min < user_life:
        adv_emoji = emojis.CHECK_WARN
    else:
        adv_emoji = emojis.CHECK_FAIL
    if adv_taken_dmg_max_hm == 0:
        adv_hm_emoji = emojis.CHECK_OK
    elif adv_taken_dmg_max_hm < user_life:
        adv_hm_emoji = emojis.CHECK_IGNORE
    elif adv_taken_dmg_min_hm < user_life:
        adv_hm_emoji = emojis.CHECK_WARN
    else:
        adv_hm_emoji = emojis.CHECK_FAIL

    if hunt_taken_dmg_min == hunt_taken_dmg_max:
        hunt_dmg_taken_str = f'{hunt_taken_dmg_max:,}'
    else:
        hunt_dmg_taken_str = f'{hunt_taken_dmg_min:,}-{hunt_taken_dmg_max:,}'
    if hunt_taken_dmg_min_hm == hunt_taken_dmg_max_hm:
        hunt_dmg_taken_hm_str = f'{hunt_taken_dmg_max_hm:,}'
    else:
        hunt_dmg_taken_hm_str = f'{hunt_taken_dmg_min_hm:,}-{hunt_taken_dmg_max_hm:,}'
    if adv_taken_dmg_min == adv_taken_dmg_max:
        adv_dmg_taken_str = f'{adv_taken_dmg_max:,}'
    else:
        adv_dmg_taken_str = f'{adv_taken_dmg_min}-{adv_taken_dmg_max}'
    if adv_taken_dmg_min_hm == adv_taken_dmg_max_hm:
        adv_dmg_taken_hm_str = f'{adv_taken_dmg_max_hm:,}'
    else:
        adv_dmg_taken_hm_str = f'{adv_taken_dmg_min_hm:,}-{adv_taken_dmg_max_hm:,}'

    if 1 <= area_no <= 15:
        result = (
            f'{emojis.BP} {hunt_emoji} **Hunt**: {hunt_dmg_taken_str} damage\n'
            f'{emojis.BP} {hunt_hm_emoji} **Hunt hardmode**: {hunt_dmg_taken_hm_str} damage\n'
            f'{emojis.BP} {adv_emoji} **Adventure**: {adv_dmg_taken_str} damage\n'
            f'{emojis.BP} {adv_hm_emoji} **Adventure hardmode**: {adv_dmg_taken_hm_str} damage\n'
        )
    else:
        result = (
            f'{emojis.BP} {hunt_emoji} **Hunt**: {hunt_taken_dmg_max:,} damage\n'
            f'{emojis.BP} {hunt_hm_emoji} **Hunt hardmode**: {hunt_taken_dmg_max_hm:,} damage\n'
            f'{emojis.BP} {adv_emoji} **Adventure**: {adv_taken_dmg_max:,} damage\n'
            f'{emojis.BP} {adv_hm_emoji} **Adventure hardmode**: {adv_taken_dmg_max_hm:,} damage\n'
        )
    return result


# --- Embeds ---
async def embed_area_guide(ctx: commands.Context, area_no: int, user: database.User, full_version: bool) -> discord.Embed:
    """Returns embed with area guide"""
    area = await database.get_area(area_no)
    dungeon: database.Dungeon = await database.get_dungeon(area.dungeon_no)
    tt_no = 25 if user.tt > 25 else user.tt
    tt: database.TimeTravel = await database.get_time_travel(tt_no)
    area_locked = traderates_next_area = next_area = area_req = area_dmg = None
    materials = new_commands = ''
    time_traveler_prepare = True if tt.tt_area == area.area_no else False
    if area.area_no == 15:
        next_area = await database.get_area(21)
    elif area.area_no < 20:
        next_area = await database.get_area(area.area_no + 1)

    # Footer
    footer = 'Use "/dungeon guide" to see details about the next dungeon.'

    # Description
    description = f'{area.description}'

    # Area locked
    if user.tt < area.unlocked_in_tt:
        area_locked = (
            f'{emojis.BP} **You can not reach this area in your current TT**\n'
            f'{emojis.BP} This area is unlocked in {emojis.TIME_TRAVEL} TT {area.unlocked_in_tt}'
            )
        footer = f'Tip: See "/time travel guide" for details about time traveling'

    # Area requirements
    unseal_time = {
        16: 21,
        17: 18,
        18: 15,
        19: 12,
        20: 9
    } # area: days
    if 2 <= area.area_no <= 15:
        area_req = (
            f'{emojis.BP} Complete dungeon {area.area_no - 1}'
        )
    elif area.area_no == 21:
        area_req = (
            f'{emojis.BP} Complete dungeon 15-2\n'
        )
    elif area.area_no == 16:
        area_req = (
            f'{emojis.BP} Complete the EPIC NPC fight in the TOP once\n'
            f'{emojis.BP} This area needs to be unsealed by players from the TOP '
            f'(see {emojis.EPIC_RPG_LOGO_SMALL}`/void info`)\n'
            f'{emojis.BP} Once unsealed, the area will stay open for {unseal_time[area.area_no]} days\n'
            #f'{emojis.BP} To contribute, use `void add 16 [item] [amount]` while in the TOP\n'
            #f'{emojis.BP} Check `void` to see the current status and requirements\n'
            f'{emojis.BP} Requires an {emojis.EPIC_JUMP} EPIC jump to move to this area from the TOP\n'
            f'{emojis.BLANK} EPIC jumps are found in the `shop` and in dungeons 16-20\n'
        )
    elif 17 <= area.area_no <= 20:
        area_req = (
            f'{emojis.BP} Complete the EPIC NPC fight in the TOP once\n'
            f'{emojis.BP} This area needs to be unsealed by players from area {area.area_no-1} '
            f'(see {emojis.EPIC_RPG_LOGO_SMALL}`/void info`)\n'
            f'{emojis.BP} Once unsealed, the area will stay open for {unseal_time[area.area_no]} days\n'
            #f'{emojis.BP} To contribute, use `void add {area.area_no} [item] [amount]` while in area {area.area_no-1}\n'
            #f'{emojis.BP} Check `void` to see the current status and requirements\n'
            f'{emojis.BP} Requires an {emojis.EPIC_JUMP} EPIC jump to move to this area from area {area.area_no-1}\n'
            f'{emojis.BLANK} EPIC jumps are found in the `shop` and in dungeons 16-20\n'
        )
    if area.unlocked_in_tt > 0:
        area_req = (
            f'{emojis.BP} {emojis.TIME_TRAVEL} TT {area.unlocked_in_tt}+\n'
            f'{area_req}'
        )

    # Guick guide
    quick_guide = await design_field_quick_guide(ctx, area, dungeon, tt, user)

    # Debuffs
    debuffs = await design_field_debuffs(area)

    # Recommended dungeon stats
    field_rec_stats = await functions.design_field_rec_stats(dungeon)

    # Recommended gear
    field_rec_gear = await functions.design_field_rec_gear(dungeon)
    if field_rec_gear is None: field_rec_gear = f'{emojis.BP} None'
    if area.area_no in (7,8): field_rec_gear = f'{field_rec_gear} **(*)**'

    # New commands
    show_new_commands = False
    if not user.ascended:
        show_new_commands = True
    else:
        if area.area_no >= 12 and user.tt == 1: show_new_commands = True
        elif area.area_no >= 13 and user.tt in (2,3): show_new_commands = True
        elif area.area_no >= 14 and user.tt in (4,5): show_new_commands = True
        elif area.area_no >= 15 and 6 <= user.tt <= 10: show_new_commands = True
        elif area.area_no == 21: show_new_commands = True
    if show_new_commands:
        for new_command in area.new_commands:
            if new_command is not None:
                new_commands = f'{new_commands}, {emojis.EPIC_RPG_LOGO_SMALL}`{new_command}`'
        if new_commands != '': new_commands = f'{emojis.BP} {new_commands.lstrip(", ")}'

    # Best work command
    work_commands = await design_field_work_commands(area, user)

    # Area damage
    if area.adv_dmg[1] > 0 and area.hunt_dmg[1] > 0:
        hunt_dmg_min = area.hunt_dmg[0]
        hunt_dmg_max = area.hunt_dmg[1]
        hunt_dmg_min_hm = functions.round_school(hunt_dmg_min*1.7)
        hunt_dmg_max_hm = functions.round_school(hunt_dmg_max*1.7)
        adv_dmg_min = area.adv_dmg[0]
        adv_dmg_max = area.adv_dmg[1]
        adv_dmg_min_hm = functions.round_school(adv_dmg_min*1.7)
        adv_dmg_max_hm = functions.round_school(adv_dmg_max*1.7)

        if 16 <= area.area_no <= 20:
            area_dmg = (
                f'{emojis.BP} Hunt: ~**{hunt_dmg_max:,}** normal, ~**{hunt_dmg_max_hm:,}** hardmode\n'
                f'{emojis.BP} Adventure: ~**{adv_dmg_max:,}** normal, ~**{adv_dmg_max_hm:,}** hardmode'
            )
        else:
            area_dmg = (
                f'{emojis.BP} Hunt: **{hunt_dmg_min:,}**~**{hunt_dmg_max:,}** normal, '
                f'**{hunt_dmg_min_hm:,}**~**{hunt_dmg_max_hm:,}** hardmode\n'
                f'{emojis.BP} Adventure: **{adv_dmg_min:,}**~**{adv_dmg_max:,}** normal, '
                f'**{adv_dmg_min_hm:,}**~**{adv_dmg_max_hm:,}** hardmode'
            )
        area_dmg = (
            f'{area_dmg}\n'
            f'{emojis.BLANK} Use {emojis.LOGO}`/area check` to see your actual damage'
        )

    # Lootboxes
    lootboxes = await design_field_lootboxes(area, user)

    # Materials areas 3, 5 and 8
    if area.area_no == 5:
        materials = (
            f'{emojis.BP} 30+ {emojis.WOLF_SKIN} wolf skins\n'
            f'{emojis.BP} 30+ {emojis.ZOMBIE_EYE} zombie eyes\n'
            f'{emojis.BP} 30+ {emojis.UNICORN_HORN} unicorn horns (after crafting)'
        )
        if tt.a5_apple > 0:
            materials = f'{materials}\n{emojis.BP} {tt.a5_apple:,} {emojis.APPLE} apples'

    if area.area_no == 3:
        materials = ''
        if 1 <= user.tt <= 4:
            materials = (
                f'{emojis.BP} 20 {emojis.WOLF_SKIN} wolf skins\n'
                f'{emojis.BP} 20 {emojis.ZOMBIE_EYE} zombie eyes'
            )

        if tt.a3_fish > 0:
            materials = f'{materials}\n{emojis.BP} {tt.a3_fish:,} {emojis.FISH} normie fish'
            if user.ascended: materials = f'{materials} (1 {emojis.RUBY} = 225 {emojis.FISH})'
        if user.tt >= 25:
            materials = f'{materials}\n{emojis.BLANK} Note: This does not include materials for STT score.'

    if area.area_no == 8:
        materials = f'{emojis.BP} 30 {emojis.MERMAID_HAIR} mermaid hairs\n'

    # Trades
    trades = await functions.design_field_trades(area, user)
    trades_name = 'TRADES BEFORE LEAVING'
    if area.area_no == 15: trades_name = f'{trades_name} (IF YOU DO D15-2)'

    # Trade rates
    traderates = await functions.design_field_traderate(area)
    if next_area is not None:
        traderates_next_area = await functions.design_field_traderate(next_area)

    # Monsters
    field_monsters_hunt = ''
    field_monsters_adv = ''
    monsters = await database.get_monster_by_area(area.area_no, area.area_no)
    for monster in monsters:
        if monster.activity == 'hunt':
            field_monsters_hunt = f'{field_monsters_hunt}\n{emojis.BP} {monster.emoji} {monster.name}'
            if monster.drop_emoji is not None:
                field_monsters_hunt = f'{field_monsters_hunt} (drops {monster.drop_emoji})'
        elif monster.activity == 'adventure':
            field_monsters_adv = f'{field_monsters_adv}\n{emojis.BP} {monster.emoji} {monster.name}'


    area_no_str = 'THE TOP' if area.area_no == 21 else f'AREA {area.area_no}'
    next_area_no_str = 'THE TOP' if area.area_no == 15 else f'AREA {area.area_no + 1}'
    dungeon_no_str = 'EPIC NPC FIGHT' if area.area_no == 21 else f'D{area.dungeon_no}'

    # Note
    guide_area = 'top' if area.area_no == 21 else area.area_no
    note = (
        f'{emojis.BP} To change your personal TT settings, use {emojis.LOGO}`/set progress`.'
    )
    if area.area_no in (7,8):
        note = (
            f'{note}\n'
            f'{emojis.BP} **(*)** This armor is expensive. If you don\'t want to craft it, find a carry or '
            f'cook {emojis.FOOD_ORANGE_JUICE} orange juice or {emojis.FOOD_APPLE_JUICE} apple juice.'
        )
    if 16 <= area.area_no <= 19:
        note = (
            f'{note}\n'
            f'{emojis.BP} If you time travel in this area, you get an additional {area.area_no - 15} '
            f'{emojis.TIME_TRAVEL} time travels'
        )

    # Title
    title = f'{area_no_str}  •  TT {user.tt}'
    if user.ascended: title = f'{title}, ASCENDED'

    # Create embed
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = title,
    )
    embed.set_footer(text=footer)
    if full_version:
        embed.description = description
    if area_locked is not None:
        embed.add_field(name='AREA LOCKED', value=area_locked, inline=False)
    if full_version:
        embed.add_field(name='QUICK GUIDE', value=quick_guide, inline=False)
    if area_req is not None and full_version:
        embed.add_field(name=f'HOW TO REACH {area_no_str}', value=area_req, inline=False)
    if debuffs is not None:
        embed.add_field(name='AREA DEBUFFS', value=debuffs, inline=False)
    if field_monsters_hunt != '' and full_version:
        embed.add_field(name='MONSTERS IN HUNT', value=field_monsters_hunt, inline=True)
    if field_monsters_hunt != '' and full_version:
        embed.add_field(name='MONSTERS IN ADVENTURE', value=field_monsters_adv, inline=True)
    if area_dmg is not None and full_version:
        embed.add_field(name='MONSTER DAMAGE', value=area_dmg, inline=False)
    if show_new_commands and new_commands != '' and full_version:
        embed.add_field(name='NEW COMMANDS', value=new_commands, inline=False)
    if work_commands is not None:
        embed.add_field(name='BEST WORK COMMAND', value=work_commands, inline=False)
    if not time_traveler_prepare:
        embed.add_field(name='LOOTBOXES', value=lootboxes, inline=False)
        embed.add_field(name=f'RECOMMENDED GEAR FOR {dungeon_no_str}', value=field_rec_gear, inline=True)
        embed.add_field(name=f'RECOMMENDED STATS FOR {dungeon_no_str}', value=field_rec_stats, inline=True)
    if materials != '':
        embed.add_field(name='MATERIALS TO FARM', value=materials, inline=False)
    if not time_traveler_prepare:
        embed.add_field(name=trades_name, value=trades, inline=False)
    if full_version:
        embed.add_field(name=f'TRADE RATES {area_no_str}', value=traderates, inline=True)
    if traderates_next_area is not None and not time_traveler_prepare and full_version:
        embed.add_field(name=f'TRADE RATES {next_area_no_str}', value=traderates_next_area, inline=True)
    if full_version:
        embed.add_field(name='NOTE', value=note, inline=False)

    return embed


async def embed_area_check(area_no: int, user_at: int, user_def: int, user_life: int) -> discord.Embed:
    """Embed with area check"""
    legend = (
        f'{emojis.BP} {emojis.CHECK_OK} : You will take no damage\n'
        f'{emojis.BP} {emojis.CHECK_IGNORE} : You will take damage but survive if healed up\n'
        f'{emojis.BP} {emojis.CHECK_WARN} : If you are lucky and healed up, you _might_ survive\n'
        f'{emojis.BP} {emojis.CHECK_FAIL} : It was nice knowing you, RIP\n'
    )
    stats = (
        f'{emojis.BP} {emojis.STAT_AT} **AT**: {user_at:,}\n'
        f'{emojis.BP} {emojis.STAT_DEF} **DEF**: {user_def:,}\n'
        f'{emojis.BP} {emojis.STAT_LIFE} **LIFE**: {user_life:,}'
    )
    area_no_str = 'the TOP' if area_no == 21 else f'area {area_no}'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'{area_no_str.upper()} DAMAGE CHECK',
    )
    embed.add_field(name='YOUR STATS', value=stats, inline=False)
    area_check_field = await design_field_area_check(area_no, user_at, user_def, user_life)
    embed.add_field(name='DAMAGE TAKEN', value=area_check_field, inline=False)
    embed.add_field(name='LEGEND', value=legend, inline=False)
    return embed