# areas.py

import discord
from discord.ext import commands

import database
from resources import emojis
from resources import settings
from resources import functions


# area commands (cog)
class areasCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    area_aliases = ['area','areas','top','thetop','atop','areatop']
    for x in range(1,21):
        area_aliases.append(f'a{x}')
        area_aliases.append(f'area{x}')

    @commands.command(name='a',aliases=(area_aliases))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def area(self, ctx: commands.Context, *args: str) -> None:
        """Command for areas, can be invoked with "aX", "a X", "areaX" and "area X".
        Optional parameters for TT and ascension
        """
        invoked = ctx.invoked_with.lower()
        prefix = ctx.prefix.lower()
        area_no = arg_tt = None
        arg_asc = False

        error_syntax = (
            f'The command syntax is `{prefix}area [#]` or `{prefix}a1`-`{prefix}a15`.\n'
            f'If you want to see an area guide for a specific TT (0 - 999), you can add the TT after the command. To see the ascended version, add `asc`.\n'
            f'Examples: `{prefix}a5 tt5`, `{prefix}a3 8 asc`'
        )

        error_area_no = 'There is no area {area_no}, lol.'
        error_general = 'Oops. Something went wrong here.'

        if invoked == 'areas':
            embed = await embed_areas_menu(ctx)
            await ctx.send(embed=embed)
            return

        if invoked in ('a','area'):
            if args:
                args = [arg.lower() for arg in args]
                arg1 = args[0]
                if arg1.isnumeric():
                    arg1 = int(arg1)
                    if 1 <= arg1 <= 20:
                        area_no = arg1
                    else:
                        await ctx.send(error_area_no.format(area_no=arg1))
                        return
                else:
                    if arg1 == 'top':
                        area_no = 21
                    else:
                        await ctx.send(error_area_no.format(area_no=arg1))
                        return

                if len(args) > 1:
                    arg2 = args[1]
                    arg2 = arg2.replace('tt','')
                    if arg2.isnumeric():
                        arg2 = int(arg2)
                        if 0 <= arg2 <= 999:
                            arg_tt = arg2
                        else:
                            await ctx.send(error_syntax)
                            return
                    else:
                        if arg2 in ('asc','ascended'):
                            arg_asc = True
                        else:
                            await ctx.send(error_syntax)
                            return
                    if len(args) > 2:
                        arg3 = args[2]
                        arg3 = arg3.replace('tt','')
                        if arg3.isnumeric():
                            arg3 = int(arg3)
                            if 0 <= arg3 <= 999:
                                arg_tt = arg3
                            else:
                                await ctx.send(error_syntax)
                                return
                        else:
                            if arg3 in ('asc','ascended'):
                                arg_asc = True
                            else:
                                await ctx.send(error_syntax)
                                return
            else:
                await ctx.send(error_syntax)
                return
        else:
            invoked_area = invoked.replace('area','').replace('a','')
            if invoked_area.isnumeric():
                invoked_area = int(invoked_area)
                if 1 <= invoked_area <= 20:
                    area_no = invoked_area
                else:
                    await ctx.send(error_general)
                    return
            else:
                if 'top' in invoked:
                    area_no = 21
                else:
                    await ctx.send(error_general)
                    return

            if args:
                args = [arg.lower() for arg in args]
                arg1 = args[0]
                arg1 = arg1.replace('tt','')
                if arg1.isnumeric():
                    arg1 = int(arg1)
                    if 0 <= arg1 <= 999:
                        arg_tt = arg1
                    else:
                        await ctx.send(error_syntax)
                        return
                else:
                    if arg1 in ('asc','ascended'):
                        arg_asc = True
                    else:
                        await ctx.send(error_syntax)
                        return
                if len(args) > 1:
                    arg2 = args[1]
                    arg2 = arg2.replace('tt','')
                    if arg2.isnumeric():
                        arg2 = int(arg2)
                        if 0 <= arg2 <= 999:
                            arg_tt = arg2
                        else:
                            await ctx.send(error_syntax)
                            return
                    else:
                        if arg2 in ('asc','ascended'):
                            arg_asc = True
                        else:
                            await ctx.send(error_syntax)
                            return

        area = await database.get_area(area_no)
        user: database.User = await database.get_user(ctx.author.id)
        if arg_tt is not None:
            user.tt = arg_tt
            if arg_tt >= 25: arg_asc = True
            if arg_asc:
                if arg_tt == 0:
                    await ctx.send(f'**{ctx.author.name}**, you can not ascend in TT 0.')
                    return
                user.ascended = True
            else:
                user.ascended = False
        else:
            if arg_asc:
                user.ascended = True

        embed = await embed_area(ctx, area, user)
        await ctx.send(embed=embed)

# Initialization
def setup(bot):
    bot.add_cog(areasCog(bot))


# --- Functions ---
async def design_field_quick_guide(ctx: commands.Context, area: database.Area, dungeon: database.Dungeon,
                             tt: database.TimeTravel, user: database.User) -> str:
    """Returns the quick guide for the area embed"""
    prefix = ctx.prefix
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
            f'{emojis.BP} Craft {emojis.SWORD_GODLYCOOKIE} GODLY cookie if you want to do the "final" fight'
        )

    if tt.tt_area == area.area_no:
        quick_guide = f'{emojis.BP} {emojis.TIME_TRAVEL} Prepare for time travel (see `{prefix}tt{user.tt + 1}`)'
        return quick_guide

    if ((area.area_no == 3 and tt.a3_fish > 0) or (area.area_no == 5 and tt.a5_apple > 0)):
        quick_guide = f'{emojis.BP} Farm the materials mentioned below'

    if dungeon.player_level is not None and dungeon.dungeon_no <= 15.2:
        quick_guide = f'{quick_guide}\n{emojis.BP} Reach level {dungeon.player_level:,}'
    if area.area_no == 9:
        quick_guide = (
            f'{quick_guide}\n'
            f'{emojis.BP} Go back to previous areas if you are missing materials for crafting the armor '
            f'(see `{prefix}drops`)'
        )
    if quick_guide_sword != '' or quick_guide_enchant_sword != '':
        quick_guide = f'{quick_guide}\n{quick_guide_sword}{quick_guide_enchant_sword}'
    if quick_guide_armor != '' or quick_guide_enchant_armor != '':
        quick_guide = f'{quick_guide}\n{quick_guide_armor}{quick_guide_enchant_armor}'
        if area.area_no == 7: quick_guide = f'{quick_guide} **(*)**'
    quick_guide = f'{quick_guide}\n{emojis.BP} Check below to see which lootboxes to buy, keep or open'
    if area.area_no in (3,5,7,9,10,11) and tt.tt_area != area.area_no:
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

    if 16 <= area.area_no <= 20:
        if area.area_no in (16,18):
            work_commands = (
                f'{emojis.BP} `bigboat` if you need {emojis.FISH_SUPER} SUPER fish\n'
                f'{emojis.BP} `chainsaw` otherwise'
            )
        elif area.area_no in (17,20):
            work_commands = f'{emojis.BP} `chainsaw`'
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
                f'{emojis.BP} `drill` if you need coins\n'
                f'{emojis.BP} `chainsaw` otherwise'
            )
        elif user.tt == 2 and 6 <= area.area_no <= 8:
            work_commands = (
               f'{emojis.BP} `pickaxe`'
            )
        else:
            if money_nohorse is None:
                work_commands = f'{emojis.BP} `{area.work_cmd_poor}`'
            else:
                if user.tt < 25:
                    work_commands = (
                        f'{emojis.BP} `{area.work_cmd_poor}` if < {money_nohorse}m coins and horse is < T6\n'
                        f'{emojis.BP} `{area.work_cmd_poor}` if < {money_t6horse}m coins and horse is T6+'
                    )
                else:
                    work_commands = (
                        f'{emojis.BP} `{area.work_cmd_poor}` if < {money_t6horse}m coins'
                    )
                work_commands = f'{work_commands}\n{emojis.BP} `{area.work_cmd_rich}` otherwise'

        if user.ascended:
            if 1 <= area.area_no <= 9:
                if user.tt == 1:
                    work_commands = f'{emojis.BP} `chainsaw`'
                elif 1 <= area.area_no <= 3:
                    work_commands = f'{emojis.BP} `dynamite`'
                elif 4 <= area.area_no <= 5:
                    work_commands = (
                        f'{emojis.BP} `chainsaw` if worker 115 or higher\n'
                        f'{emojis.BP} `dynamite` otherwise'
                    )
                elif 6 <= area.area_no <= 7:
                    work_commands = (
                        f'{emojis.BP} `greenhouse` if worker 102 or higher\n'
                        f'{emojis.BP} `dynamite` otherwise'
                    )
                elif area.area_no == 8:
                    work_commands = (
                        f'{emojis.BP} `chainsaw` if worker 109 or higher\n'
                        f'{emojis.BP} `dynamite` otherwise'
                    )
                elif area.area_no == 9:
                    work_commands = (
                        f'{emojis.BP} `greenhouse` if worker 107 or higher\n'
                        f'{emojis.BP} `dynamite` otherwise'
                    )
            elif area.area_no == 10:
                if user.tt == 1:
                    work_commands = f'{emojis.BP} `chainsaw`'
                else:
                    work_commands = (
                        f'{emojis.BP} `dynamite` if you have all the {emojis.LOG_ULTRA} ULTRA logs you need for forging\n'
                        f'{emojis.BP} `chainsaw` otherwise'
                    )
            elif area.area_no == 11:
                if user.tt == 1:
                    work_commands = f'{emojis.BP} `chainsaw`'
                else:
                    work_commands = (
                        f'{emojis.BP} `dynamite` if you have all the {emojis.LOG_ULTRA} ULTRA logs you need for forging\n'
                        f'{emojis.BP} `chainsaw` otherwise'
                    )
            else:
                work_commands = (
                    f'{emojis.BP} `dynamite` if you need coins\n'
                    f'{emojis.BP} `chainsaw` otherwise'
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


# --- Embeds ---
# Areas menu
async def embed_areas_menu(ctx):

    prefix = ctx.prefix

    area_guide = f'{emojis.BP} `{prefix}area [#]` / `{prefix}a1`-`{prefix}a15` : Guide for area 1~15'

    trading = (
        f'{emojis.BP} `{prefix}trades [#]` / `{prefix}tr1`-`{prefix}tr15` : Trades in area 1~15\n'
        f'{emojis.BP} `{prefix}trades` / `{prefix}tr` : Trades (all areas)\n'
        f'{emojis.BP} `{prefix}traderates` / `{prefix}trr` : Trade rates (all areas)'
    )

    drops = f'{emojis.BP} `{prefix}drops` : Monster drops'

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'AREA GUIDES',
        description = f'Hey **{ctx.author.name}**, what do you want to know?'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='AREAS', value=area_guide, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='MONSTER DROPS', value=drops, inline=False)

    return embed


async def embed_area(ctx: commands.Context, area: database.Area, user: database.User) -> discord.Embed:
    """Returns embed with area guide"""
    prefix = ctx.prefix
    dungeon: database.Dungeon = await database.get_dungeon(area.dungeon_no)
    tt_no = 25 if user.tt > 25 else user.tt
    tt: database.TimeTravel = await database.get_time_travel(tt_no)
    area_locked = traderates_next_area = next_area = area_req = None
    materials = new_commands = ''
    time_traveler_prepare = True if tt.tt_area == area.area_no else False
    if area.area_no == 15:
        next_area = await database.get_area(21)
    elif area.area_no < 20:
        next_area = await database.get_area(area.area_no + 1)

    # Footer
    guide_dungeon = 'top' if area.area_no == 21 else f'{area.dungeon_no:g}'
    footer = f'Tip: Use {prefix}d{guide_dungeon} for details about the next dungeon.'

    # Description
    description = f'{area.description}'

    # Area locked
    if user.tt < area.unlocked_in_tt:
        area_locked = (
            f'{emojis.BP} **You can not reach this area in your current TT**\n'
            f'{emojis.BP} This area is unlocked in {emojis.TIME_TRAVEL} TT {area.unlocked_in_tt}'
            )
        footer = f'Tip: See {prefix}tt for details about time traveling'

    # Area requirements
    unseal_time = {
        16: 15,
        17: 10,
        18: 5,
        19: 3,
        20: 2
    } # area: days
    if 2 <= area.area_no <= 15:
        area_req = (
            f'{emojis.BP} Complete dungeon {area.area_no - 1} (see `{prefix}d{area.area_no - 1}`)'
        )
    elif area.area_no == 21:
        area_req = (
            f'{emojis.BP} Complete dungeon 15-2 (see `{prefix}d15-2`)\n'
        )
    elif area.area_no == 16:
        area_req = (
            f'{emojis.BP} Complete the "final" fight in the TOP once (see `{prefix}dtop`)\n'
            f'{emojis.BP} This area needs to be unsealed by players from the TOP (see `rpg void`)\n'
            f'{emojis.BP} Once unsealed, the area will stay open for {unseal_time[area.area_no]} days\n'
            #f'{emojis.BP} To contribute, use `void add 16 [item] [amount]` while in the TOP\n'
            #f'{emojis.BP} Check `void` to see the current status and requirements\n'
            f'{emojis.BP} Requires an {emojis.EPIC_JUMP} EPIC jump to move to this area from the TOP\n'
            f'{emojis.BLANK} EPIC jumps are found in the `shop` and in dungeons 16-20\n'
        )
    elif 17 <= area.area_no <= 20:
        area_req = (
            f'{emojis.BP} Complete the "final" fight in the TOP once (see `{prefix}dtop`)\n'
            f'{emojis.BP} This area needs to be unsealed by players from area {area.area_no-1}(see `rpg void`)\n'
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
                new_commands = f'{new_commands}, `{new_command}`'
        if new_commands != '': new_commands = f'{emojis.BP} {new_commands.lstrip(", ")}'

    # Best work command
    work_commands = await design_field_work_commands(area, user)

    # Area damage
    if area.adv_dmg[1] is not None and area.hunt_dmg[1] is not None:
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
                f'{emojis.BP} `hunt`: ~**{hunt_dmg_max:,}**, '
                f'`hunt h`: ~**{hunt_dmg_max_hm:,}**\n'
                f'{emojis.BP} `adv`: ~**{adv_dmg_max:,}**, '
                f'`adv h`: ~**{adv_dmg_max_hm:,}**'
            )
        else:
            area_dmg = (
                f'{emojis.BP} `hunt`: **{hunt_dmg_min:,}**~**{hunt_dmg_max:,}**, '
                f'`hunt h`: **{hunt_dmg_min_hm:,}**~**{hunt_dmg_max_hm:,}**\n'
                f'{emojis.BP} `adv`: **{adv_dmg_min:,}**~**{adv_dmg_max:,}**, '
                f'`adv h`: **{adv_dmg_min_hm:,}**~**{adv_dmg_max_hm:,}**'
            )
        area_dmg = (
            f'{area_dmg}\n'
            f'{emojis.BLANK} Monster damage - (AT + DEF) = Actual damage'
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
    dungeon_no_str = 'THE "FINAL" FIGHT' if area.area_no == 21 else f'D{area.dungeon_no}'

    # Note
    guide_area = 'top' if area.area_no == 21 else area.area_no
    note = (
        f'{emojis.BP} To see the guide for another TT, use `{prefix}a{guide_area} [tt]` '
        f'or `{prefix}a{guide_area} [tt] asc`\n'
        f'{emojis.BP} To change your personal TT settings, use `{prefix}setprogress`.'
    )
    if area.area_no in (7,8):
        note = (
            f'{note}\n'
            f'{emojis.BP} **(*)** This armor is expensive. If you don\'t want to craft it, find a carry or '
            f'cook {emojis.FOOD_ORANGE_JUICE} orange juice or {emojis.FOOD_APPLE_JUICE} apple juice.'
        )

    # Title
    title = f'{area_no_str}  •  TT {user.tt}'
    if user.ascended: title = f'{title}, ASCENDED'

    # Create embed
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = title,
        description = description
    )
    embed.set_footer(text=footer)

    if area_locked is not None:
        embed.add_field(name='AREA LOCKED', value=area_locked, inline=False)
    embed.add_field(name='QUICK GUIDE', value=quick_guide, inline=False)
    if area_req is not None:
        embed.add_field(name=f'HOW TO REACH {area_no_str}', value=area_req, inline=False)
    if debuffs is not None:
        embed.add_field(name='AREA DEBUFFS', value=debuffs, inline=False)
    if field_monsters_hunt != '':
        embed.add_field(name='MONSTERS IN HUNT', value=field_monsters_hunt, inline=True)
    if field_monsters_hunt != '':
        embed.add_field(name='MONSTERS IN ADVENTURE', value=field_monsters_adv, inline=True)
    if area_dmg is not None:
        embed.add_field(name='MONSTER DAMAGE', value=area_dmg, inline=False)
    if show_new_commands and new_commands != '':
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
    embed.add_field(name=f'TRADE RATES {area_no_str}', value=traderates, inline=True)
    if traderates_next_area is not None and not time_traveler_prepare:
        embed.add_field(name=f'TRADE RATES {next_area_no_str}', value=traderates_next_area, inline=True)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed