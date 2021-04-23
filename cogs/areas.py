# areas.py

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import discord
import emojis
import global_data
import database

from discord.ext import commands
from math import ceil

# area commands (cog)
class areasCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Command for areas, can be invoked with "aX", "a X", "areaX" and "area X", optional parameters for TT and ascension
    area_aliases = ['area','areas',]
    for x in range(1,16):
        area_aliases.append(f'a{x}')    
        area_aliases.append(f'area{x}') 

    @commands.command(name='a',aliases=(area_aliases))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def area(self, ctx, *args):
        
        invoked = ctx.invoked_with
        invoked = invoked.lower()
        prefix = ctx.prefix
        prefix = prefix.lower()
        area_no = None
        arg_tt = None
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
                arg1 = args[0]
                if arg1.isnumeric():
                    arg1 = int(arg1)
                    if 1 <= arg1 <= 15:
                        area_no = arg1
                    else:
                        await ctx.send(error_area_no.format(area_no=arg1))
                        return
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
                if 1 <= invoked_area <= 15:
                    area_no = invoked_area
                else:
                    await ctx.send(error_general)
                    return
            else:
                await ctx.send(error_general)
                return
            
            if args:
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
        
        area_data = await database.get_area_data(ctx, area_no)
        user_settings = await database.get_settings(ctx)
        if not user_settings == None:
            user_settings = list(user_settings)
        
        if user_settings == None:
            await database.first_time_user(self.bot, ctx)
            return
        
        if not arg_tt == None:
            user_settings[0] = arg_tt
            
            if arg_asc == True:
                user_settings[1] = 'ascended'
            else:
                user_settings[1] = 'not ascended'
        else:
            if arg_asc == True:
                user_settings[1] = 'ascended'
            
        traderate_data = await database.get_traderate_data(ctx, area_no)
        
        if area_no < 15:
            traderate_data_next = await database.get_traderate_data(ctx, area_no+1)
        else:
            traderate_data_next = ''
        
        if area_no in (3,5):
            if user_settings[0] <= 25:
                mats_data = await database.get_mats_data(ctx, user_settings[0])
            else:
                mats_data = await database.get_mats_data(ctx, 25)
        else:
            mats_data = ''
        
        embed = await embed_area(area_data, mats_data, traderate_data, traderate_data_next, user_settings, ctx.author.name, ctx.prefix)
        await ctx.send(embed=embed)

# Initialization
def setup(bot):
    bot.add_cog(areasCog(bot))

                  

# --- Embeds ---
# Areas menu
async def embed_areas_menu(ctx):
    
    prefix = ctx.prefix
    
    area_guide = f'{emojis.bp} `{prefix}area [#]` / `{prefix}a1`-`{prefix}a15` : Guide for area 1~15'
                    
    trading = (
        f'{emojis.bp} `{prefix}trades [#]` / `{prefix}tr1`-`{prefix}tr15` : Trades in area 1~15\n'
        f'{emojis.bp} `{prefix}trades` / `{prefix}tr` : Trades (all areas)\n'
        f'{emojis.bp} `{prefix}traderates` / `{prefix}trr` : Trade rates (all areas)'
    )
    
    drops = f'{emojis.bp} `{prefix}drops` : Monster drops'
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'AREA GUIDES',
        description = f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='AREAS', value=area_guide, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='MONSTER DROPS', value=drops, inline=False)
    
    return embed

# Area guide
async def embed_area(area_data, mats_data, traderate_data, traderate_data_next, user_settings, user_name, prefix):
    
    area_no = int(area_data[0])
    work_cmd_poor = area_data[1]
    work_cmd_rich = area_data[2]
    work_cmd_asc = area_data[3]
    new_cmd_1 = area_data[4]
    new_cmd_2 = area_data[5]
    new_cmd_3 = area_data[6]
    money_tt1_t6horse = area_data[7]
    money_tt1_nohorse = area_data[8]
    money_tt3_t6horse = area_data[9]
    money_tt3_nohorse = area_data[10]
    money_tt5_t6horse = area_data[11]
    money_tt5_nohorse = area_data[12]
    money_tt10_t6horse = area_data[13]
    money_tt10_nohorse = area_data[14]
    upgrade_sword = area_data[15]
    upgrade_sword_enchant = area_data[16]
    upgrade_armor = area_data[17]
    upgrade_armor_enchant = area_data[18]
    area_description = area_data[19]
    dungeon_no = area_data[20]
    player_sword_emoji = getattr(emojis, area_data[21])
    player_armor_emoji = getattr(emojis, area_data[22])
    player_at = area_data[23]
    player_def = area_data[24]
    player_carry_def = area_data[25]
    player_life = area_data[26]
    life_boost = area_data[27]
    player_level = area_data[28]
    player_sword = area_data[29]
    player_sword_enchant = area_data[30]
    player_armor = area_data[31]
    player_armor_enchant = area_data[32]
    user_tt = int(user_settings[0])
    user_asc = user_settings[1]

    if not mats_data == '':
        mats_fish = mats_data[1] 
        mats_apple = mats_data[2]

    field_rec_stats_data = (player_at, player_def, player_carry_def, player_life, life_boost, player_level, dungeon_no)
    field_rec_stats = await global_data.design_field_rec_stats(field_rec_stats_data)
    
    if ((area_no == 12) and (user_tt < 1)) or ((area_no == 13) and (user_tt < 3)) or ((area_no == 14) and (user_tt < 5)) or ((area_no == 15) and (user_tt < 10)):
        time_traveller_area_locked = True
    else:
        time_traveller_area_locked = False
    
    if ((area_no == 11) and (user_tt == 0)) or ((area_no == 12) and (1 <= user_tt <= 2)) or ((area_no == 13) and (3 <= user_tt <= 4)) or ((area_no == 14) and (5 <= user_tt <= 9)) or ((area_no == 15) and (10 <= user_tt <= 24)):
        time_traveller_prepare = True
    else:
        time_traveller_prepare = False
        
    # Footer
    footer = f'Tip: Use {prefix}d{dungeon_no} for details about the next dungeon.'
        
    # Description
    description = f'{area_description}'
    
    # Area locked
    if time_traveller_area_locked == True:
        area_locked = f'{emojis.bp} **You can not reach this area in your current TT**'
        footer = f'Tip: See {prefix}tt for details about time traveling'
    else:
        area_locked = ''
        
    # Quick Guide
    quick_guide_sword = ''
    quick_guide_armor = ''
    quick_guide_enchant_sword = ''
    quick_guide_enchant_armor = ''
    
    if upgrade_sword == 'true':
        quick_guide_sword = f'\n{emojis.bp} Craft {player_sword_emoji} {player_sword}'
    
    if upgrade_armor == 'true':
        quick_guide_armor = f'\n{emojis.bp} Craft {player_armor_emoji} {player_armor}'
    
    if not player_sword_enchant == '':
        if upgrade_sword == 'true':
            quick_guide_enchant_sword = f' and enchant to [{player_sword_enchant}+]'
        else:
            if upgrade_sword_enchant == 'true':
                quick_guide_enchant_sword = f'\n{emojis.bp} Enchant {player_sword_emoji} {player_sword} to [{player_sword_enchant}+]'
        player_sword_enchant = f'[{player_sword_enchant}]'
    
    if not player_armor_enchant == '':
        if upgrade_armor == 'true':
            quick_guide_enchant_armor = f' and enchant to [{player_armor_enchant}+]'
        else:
            if upgrade_armor_enchant == 'true':
                quick_guide_enchant_armor = f'\n{emojis.bp} Enchant {player_armor_emoji} {player_armor} to [{player_armor_enchant}+]'
        player_armor_enchant = f'[{player_armor_enchant}]'

    if time_traveller_prepare == True:
        quick_guide = f'{emojis.bp} {emojis.timetravel} Prepare for time travel (see `{prefix}tt{user_tt+1}`)'
    elif (1 <= area_no <= 4) and (user_tt == 0) :
        if not player_level == 0:
            quick_guide = (
                f'{emojis.bp} Reach level {player_level}'
                f'{quick_guide_sword}{quick_guide_enchant_sword}'
                f'{quick_guide_armor}{quick_guide_enchant_armor}\n'
                f'{emojis.bp} Check below to see which lootboxes to buy, keep or open'
            )
        else:
            quick_guide = (
                f'{quick_guide_sword}{quick_guide_enchant_sword}'
                f'{quick_guide_armor}{quick_guide_enchant_armor}'
            )
    elif (area_no == 3) and (user_tt > 0):
        quick_guide = (
            f'{emojis.bp} Farm the materials mentioned below\n'
            f'{emojis.bp} Reach level {player_level}'
            f'{quick_guide_sword}{quick_guide_enchant_sword}'
            f'{quick_guide_armor}{quick_guide_enchant_armor}\n'
            f'{emojis.bp} Check below to see which lootboxes to buy, keep or open'
        )
    elif area_no in (5,8):
        if not player_level == 0:
            quick_guide = (
                f'{emojis.bp} Farm the materials mentioned below\n'
                f'{emojis.bp} Reach level {player_level}'
                f'{quick_guide_sword}{quick_guide_enchant_sword}'
                f'{quick_guide_armor}{quick_guide_enchant_armor}\n'
                f'{emojis.bp} Check below to see which lootboxes to buy, keep or open'
            )
        else:
            quick_guide = (
                f'{emojis.bp} Farm the materials mentioned below\n'
                f'{quick_guide_sword}{quick_guide_enchant_sword}'
                f'{quick_guide_armor}{quick_guide_enchant_armor}\n'
                f'{emojis.bp} Check below to see which lootboxes to buy, keep or open'
            )
    elif area_no == 9:
        if not player_level == 0:
            quick_guide = (
                f'{emojis.bp} Go back to previous areas if you are missing materials for crafting the armor (see `{prefix}drops`)\n'
                f'{emojis.bp} Reach level {player_level}'
                f'{quick_guide_sword}{quick_guide_enchant_sword}'
                f'{quick_guide_armor}{quick_guide_enchant_armor}\n'
                f'{emojis.bp} Check below to see which lootboxes to buy, keep or open'
            )
        else:
            quick_guide = (
                f'{emojis.bp} Go back to previous areas if you are missing materials for crafting the armor (see `{prefix}drops`)\n'
                f'{quick_guide_sword}{quick_guide_enchant_sword}'
                f'{quick_guide_armor}{quick_guide_enchant_armor}\n'
                f'{emojis.bp} Check below to see which lootboxes to buy, keep or open'
            )
    else:
        if not player_level == 0:
            if area_no == 3:
                quick_guide = (
                    f'{emojis.bp} Reach level {player_level}'
                    f'{quick_guide_sword}{quick_guide_enchant_sword}'
                    f'{quick_guide_armor}{quick_guide_enchant_armor}\n'
                    f'{emojis.bp} Check below to see which lootboxes to buy, keep or open'
                )
            else:
                quick_guide = (
                    f'{emojis.bp} Reach level {player_level}'
                    f'{quick_guide_sword}{quick_guide_enchant_sword}'
                    f'{quick_guide_armor}{quick_guide_enchant_armor}\n'
                    f'{emojis.bp} Check below to see which lootboxes to buy, keep or open'
                )
        else:
            quick_guide = (
                f'{quick_guide_sword}{quick_guide_enchant_sword}'
                f'{quick_guide_armor}{quick_guide_enchant_armor}\n'
                f'{emojis.bp} Check below to see which lootboxes to buy, keep or open'
            )
    if not (int(area_no) in (1,2,4,6,12,13,14,15)) and not (time_traveller_prepare == True):
        quick_guide = f'{quick_guide}\n{emojis.bp} Trade before leaving (see trades below)'
    
    # New commands
    if ((area_no == 4) and (user_tt > 0)) or ((area_no == 11) and (user_tt > 0)) or ((area_no == 12) and (user_tt > 1)):
        new_cmd_1 = ''
    elif ((area_no == 12) and (user_tt in (1,2))) or ((area_no == 13) and (user_tt in (3,4))) or ((area_no == 14) and (5 <= user_tt <= 9)) or ((area_no == 15) and (10 <= user_tt <= 14)):
        new_cmd_1 = 'time travel'
        
    new_cmd = ''
    all_new_cmd = [new_cmd_1, new_cmd_2, new_cmd_3,]
    all_new_cmd = filter(lambda entry: entry != '', all_new_cmd)
    
    for x in all_new_cmd:
        if not new_cmd == '':
            new_cmd = f'{new_cmd}, `{x}`'
        else:
            new_cmd = f'`{x}`'
    
    # Best work commands
    if user_tt in (0,1):
        money_nohorse = money_tt1_nohorse
        money_t6horse = money_tt1_t6horse
    elif user_tt in (2,3):
        money_nohorse = money_tt3_nohorse
        money_t6horse = money_tt3_t6horse
    elif user_tt in (4,5,6,7,8):
        money_nohorse = money_tt5_nohorse
        money_t6horse = money_tt5_t6horse
    elif user_tt > 8:
        money_nohorse = money_tt10_nohorse
        money_t6horse = money_tt10_t6horse

    if 1 <= area_no <= 9:
        if user_asc == 'ascended':
            if 1 <= area_no <= 3:
                work_cmd = f'{emojis.bp} `ascended dynamite`'
            elif 4 <= area_no <= 5:
                work_cmd = (
                    f'{emojis.bp} `ascended chainsaw` if worker 113 or higher\n'
                    f'{emojis.bp} `ascended dynamite` otherwise'
                )
            elif 6 <= area_no <= 7:
                work_cmd = (
                    f'{emojis.bp} `ascended greenhouse` if worker 104 or higher\n'
                    f'{emojis.bp} `ascended dynamite` otherwise'
                )
            elif area_no == 8:
                work_cmd = (
                    f'{emojis.bp} `ascended chainsaw` if worker 110 or higher\n'
                    f'{emojis.bp} `ascended dynamite` otherwise'
                )
            elif area_no == 9:
                work_cmd = (
                    f'{emojis.bp} `ascended greenhouse` if worker 108 or higher\n'
                    f'{emojis.bp} `ascended dynamite` otherwise'
                )
        else:
            if money_nohorse == -1:
                work_cmd = f'{emojis.bp} `{work_cmd_poor}`'
            else:
                work_cmd = (
                    f'{emojis.bp} `{work_cmd_poor}` if < {money_nohorse}m coins and horse is < T6\n'
                    f'{emojis.bp} `{work_cmd_poor}` if < {money_t6horse}m coins and horse is T6+\n'
                    f'{emojis.bp} `{work_cmd_rich}` otherwise'
                )
    elif area_no == 10:
            if user_asc == 'ascended':
                work_cmd = (
                    f'{emojis.bp} `ascended dynamite` if you have all the {emojis.logultra} ULTRA logs you need for forging\n'
                    f'{emojis.bp} `chainsaw` otherwise'
                )
            else:
                if money_nohorse == -1:
                    work_cmd = f'{emojis.bp} `{work_cmd_poor}`'
                else:
                    work_cmd = (
                        f'{emojis.bp} `{work_cmd_poor}` if < {money_nohorse}m coins and horse is < T6\n'
                        f'{emojis.bp} `{work_cmd_poor}` if < {money_t6horse}m coins and horse is T6+\n'
                        f'{emojis.bp} `{work_cmd_rich}` otherwise'
                    )
    elif area_no == 11:
            if user_tt == 0:
                work_cmd = (
                    f'{emojis.bp} `chainsaw` if you need logs\n'
                    f'{emojis.bp} `greenhouse` if you need apples or bananas\n'
                    f'{emojis.bp} `drill` if you need coins'
                )
            else:
                if user_asc == 'ascended':
                    work_cmd = (
                        f'{emojis.bp} `ascended dynamite` if you have all the {emojis.logultra} ULTRA logs you need for forging\n'
                        f'{emojis.bp} `chainsaw` otherwise'
                    )
                else:
                    work_cmd =  (
                        f'{emojis.bp} `greenhouse` if you need apples or bananas\n'
                        f'{emojis.bp} `{work_cmd_poor}` if < {money_nohorse}m coins and horse is < T6\n'
                        f'{emojis.bp} `{work_cmd_poor}` if < {money_t6horse}m coins and horse is T6+\n'
                        f'{emojis.bp} `chainsaw` otherwise'
                    )
    elif 12 <= area_no <= 15:
        if ((area_no == 12) and (user_tt in (1,2))) or ((area_no == 13) and (user_tt in (3,4))) or ((area_no == 14) and (user_tt in (5,6,7,8))):
            work_cmd = (
                f'{emojis.bp} `greenhouse` if you need apples or bananas\n'
                f'{emojis.bp} `dynamite` if you need coins\n'
                f'{emojis.bp} `chainsaw` otherwise'
            )
        else:
            if not money_nohorse == 0:
                work_cmd = (
                    f'{emojis.bp} `greenhouse` if you need apples or bananas\n'
                    f'{emojis.bp} `{work_cmd_poor}` if < {money_nohorse}m coins and horse is < T6\n'
                    f'{emojis.bp} `{work_cmd_poor}` if < {money_t6horse}m coins and horse is T6+\n'
                    f'{emojis.bp} `chainsaw` otherwise'
                )
            else:
                work_cmd = (
                    f'{emojis.bp} `greenhouse` if you need apples or bananas\n'
                    f'{emojis.bp} `dynamite` if you need coins\n'
                    f'{emojis.bp} `chainsaw` otherwise'
                )
    
    # Lootboxes
    if user_tt == 0:
        if 1 <= area_no <= 4:
            lootboxes = (
                f'{emojis.bp} Buy: Whatever lootbox you have unlocked and can afford\n'
                f'{emojis.bp} Keep: {emojis.lbedgy} EDGY until A5\n'
                f'{emojis.bp} Open: All lootboxes you don\'t need to keep'
            )
        elif area_no >= 5:
            lootboxes = (
                f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                f'{emojis.bp} Open: All lootboxes'
            )
    elif 1 <= user_tt <= 9:
        if 1 <= area_no <= 4:
            if user_asc == 'ascended':
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Keep: {emojis.lbedgy} EDGY until A5\n'
                    f'{emojis.bp} Open: All lootboxes you don\'t need to keep'
                )
            else:
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Keep: {emojis.lbedgy} EDGY until A5\n'
                    f'{emojis.bp} Keep: {emojis.lbrare} Rare until A11 if you plan to level lootboxer\n'
                    f'{emojis.bp} Open: All lootboxes you don\'t need to keep'
                )
        elif 5 <= area_no <= 10:
            if user_asc == 'ascended':
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Open: All lootboxes'
                )
            else:
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Keep: {emojis.lbrare} Rare until A11 if you plan to level lootboxer\n'
                    f'{emojis.bp} Open: All lootboxes you don\'t need to keep'
                )
        elif area_no >= 11:
            if user_asc == 'ascended':
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Open: All lootboxes'
                )
            else:
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Cook {emojis.foodfilledlootbox} filled lootboxes if you need to level lootboxer\n'
                    f'{emojis.bp} Open: All lootboxes you don\'t need to cook'
                )
    elif 10 <= user_tt <= 24:
        if 1 <= area_no <= 4:
            if user_asc == 'ascended':
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Keep: {emojis.lbedgy} EDGY until A5\n'
                    f'{emojis.bp} Open: All lootboxes you don\'t need to keep'
                )
            else:
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Keep: {emojis.lbedgy} EDGY until A5\n'
                    f'{emojis.bp} Keep: {emojis.lbrare} Rare until A11 if you plan to level lootboxer\n'
                    f'{emojis.bp} Open: All lootboxes you don\'t need to keep'
                )
        elif area_no == 5:
            if user_asc == 'ascended':
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Open: All lootboxes'
                )
            else:
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Keep: {emojis.lbrare} Rare until A11 if you plan to level lootboxer\n'
                    f'{emojis.bp} Open: All lootboxes you don\'t need to keep'
                )
        elif 6 <= area_no <= 10:
            if user_asc == 'ascended':
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Keep: 1 {emojis.lbomega} OMEGA for D14 ({emojis.armoromega} OMEGA Armor)\n'
                    f'{emojis.bp} Open: All lootboxes you don\'t need to keep'
                )
            else:
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Keep: {emojis.lbrare} Rare until A11 if you plan to level lootboxer\n'
                    f'{emojis.bp} Keep: 1 {emojis.lbomega} OMEGA for D14 ({emojis.armoromega} OMEGA Armor)\n'
                    f'{emojis.bp} Open: All lootboxes you don\'t need to keep'
                )
        elif area_no >= 11:
            if user_asc == 'ascended':
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Keep: 1 {emojis.lbomega} OMEGA for D14 ({emojis.armoromega} OMEGA Armor)\n'
                    f'{emojis.bp} Open: All other lootboxes'
                )
            else:
                lootboxes = (
                    f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                    f'{emojis.bp} Keep: 1 {emojis.lbomega} OMEGA for D14 ({emojis.armoromega} OMEGA Armor)\n'
                    f'{emojis.bp} Cook {emojis.foodfilledlootbox} filled lootboxes if you need to level lootboxer\n'
                    f'{emojis.bp} Open: All lootboxes you don\'t need to keep or cook'
                )
    elif user_tt >= 25:
        if 1 <= area_no <= 4:
            lootboxes = (
                f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                f'{emojis.bp} Keep: {emojis.lbcommon} Common, {emojis.lbuncommon} Uncommon for STT score\n'
                f'{emojis.bp} Keep: {emojis.lbedgy} until A5\n'
                f'{emojis.bp} Open: {emojis.lbrare} Rare, {emojis.lbepic} EPIC, {emojis.lbomega} OMEGA, {emojis.lbgodly} GODLY'
            )
        if area_no == 5:
            lootboxes = (
                f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                f'{emojis.bp} Keep: {emojis.lbcommon} Common, {emojis.lbuncommon} Uncommon for STT score\n'
                f'{emojis.bp} Open: {emojis.lbrare} Rare, {emojis.lbepic} EPIC, {emojis.lbedgy} EDGY, {emojis.lbomega} OMEGA, {emojis.lbgodly} GODLY'
            )
        elif 6 <= area_no <= 9:
            lootboxes = (
                f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                f'{emojis.bp} Keep: {emojis.lbcommon} Common, {emojis.lbuncommon} Uncommon, {emojis.lbrare} Rare for STT score\n'
                f'{emojis.bp} Keep: 1 {emojis.lbomega} OMEGA for {emojis.armoromega} OMEGA Armor\n'
                f'{emojis.bp} Keep: 15 {emojis.lbomega} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.bp} Keep: 1 {emojis.lbgodly} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.bp} Open: {emojis.lbepic} EPIC, {emojis.lbedgy} EDGY, excess {emojis.lbomega} OMEGA, excess {emojis.lbgodly} GODLY'
            )
        elif 10 <= area_no <= 14:
            lootboxes = (
                f'{emojis.bp} Buy: {emojis.lbedgy} EDGY\n'
                f'{emojis.bp} Keep: {emojis.lbcommon} Common, {emojis.lbuncommon} Uncommon, {emojis.lbrare} Rare, {emojis.lbepic} EPIC for STT score\n'
                f'{emojis.bp} Keep: 1 {emojis.lbomega} OMEGA for {emojis.armoromega} OMEGA Armor\n'
                f'{emojis.bp} Keep: 15 {emojis.lbomega} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.bp} Keep: 1 {emojis.lbgodly} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.bp} Open: {emojis.lbedgy} EDGY, excess {emojis.lbomega} OMEGA, excess {emojis.lbgodly} GODLY'
            )
        elif area_no >= 15:
            lootboxes = (
                f'{emojis.bp} Keep: {emojis.lbcommon} Common, {emojis.lbuncommon} Uncommon, {emojis.lbrare} Rare, {emojis.lbepic} EPIC for STT score\n'
                f'{emojis.bp} Keep: 15 {emojis.lbomega} OMEGA for D15-2 (only if you plan to do it)\n'
                f'{emojis.bp} Keep: 1 {emojis.lbgodly} GODLY for D15-2 (only if you plan to do it)\n'
                f'{emojis.bp} Open: {emojis.lbedgy} EDGY, excess {emojis.lbomega} OMEGA, excess {emojis.lbgodly} GODLY'
            )            
    
    # Materials areas 3, 5 and 8
    if area_no == 5:
        materials = (
            f'{emojis.bp} 30+ {emojis.wolfskin} wolf skins\n'
            f'{emojis.bp} 30+ {emojis.zombieeye} zombie eyes\n'
            f'{emojis.bp} 30+ {emojis.unicornhorn} unicorn horns (after crafting)'
        )
        if user_tt < 5:
            materials = f'{materials}\n{emojis.bp} {mats_apple:,} {emojis.apple} apples'
    
    if (area_no == 3) and (1 <= user_tt <= 4):
        materials = (
            f'{emojis.bp} 20 {emojis.wolfskin} wolf skins\n'
            f'{emojis.bp} 20 {emojis.zombieeye} zombie eyes'
        )
        
        if not mats_fish == 0:
            if user_asc == 'ascended':
                materials = f'{materials}\n{emojis.bp} {mats_fish:,} {emojis.fish} normie fish (= {ceil(mats_fish/225):,} {emojis.ruby} rubies)'
            else:
                materials = f'{materials}\n{emojis.bp} {mats_fish:,} {emojis.fish} normie fish'
    
    if (area_no == 3) and (user_tt > 4):
        if not mats_fish == 0:
            if user_asc == 'ascended':
                materials = f'{emojis.bp} {mats_fish:,} {emojis.fish} normie fish (= {ceil(mats_fish/225):,} {emojis.ruby} rubies)'
            else:
                materials = f'{emojis.bp} {mats_fish:,} {emojis.fish} normie fish'
        
    if area_no == 8:
        materials = f'{emojis.bp} 30 {emojis.mermaidhair} mermaid hairs\n'
    # Trades
    trades = await global_data.design_field_trades(area_no, user_asc)
    
    # Trade rates
    traderates = await global_data.design_field_traderate(traderate_data)
    if not traderate_data_next == '':
        traderates_next = await global_data.design_field_traderate(traderate_data_next)
    
    # Note
    note = (
        f'{emojis.bp} To see the guide for another TT, use `{prefix}a{area_no} [tt]` or `{prefix}a{area_no} [tt] asc`\n'
        f'{emojis.bp} To change your personal TT settings, use `{prefix}setprogress`.'
    )
     
    # Title
    if user_asc == 'ascended':
        title = f'AREA {area_no}  •  TT {user_tt}, {user_asc.upper()}'
    else:
        title = f'AREA {area_no}  •  TT {user_tt}'
     
    # Embed
    embed = discord.Embed(
        color = global_data.color,
        title = title,
        description = description  
    )    
    embed.set_footer(text=footer)
    if not area_locked == '':
            embed.add_field(name='AREA LOCKED', value=area_locked, inline=False)
    embed.add_field(name='QUICK GUIDE', value=quick_guide, inline=False)
    if (area_no > 1) and (user_asc != 'ascended') and (new_cmd != ''):
        embed.add_field(name='NEW COMMANDS', value=f'{emojis.bp} {new_cmd}', inline=False)
    embed.add_field(name='BEST WORK COMMAND', value=work_cmd, inline=False)
    if not time_traveller_prepare == True:
        embed.add_field(name='LOOTBOXES', value=lootboxes, inline=False)
        embed.add_field(name=f'RECOMMENDED GEAR FOR D{dungeon_no}', value=f'{emojis.bp} {player_sword_emoji} {player_sword} {player_sword_enchant}\n'
                             f'{emojis.bp} {player_armor_emoji} {player_armor} {player_armor_enchant}', inline=False)
        embed.add_field(name=f'RECOMMENDED STATS FOR D{dungeon_no}', value=field_rec_stats, inline=False)
    if ((area_no == 3) and (user_tt > 0)) or (area_no in (5,8)):
        embed.add_field(name='MATERIALS TO FARM', value=materials, inline=False)
    if not time_traveller_prepare == True:
        embed.add_field(name='TRADES BEFORE LEAVING', value=trades, inline=False)
    embed.add_field(name=f'TRADE RATES A{area_no}', value=traderates, inline=True)
    if not (traderate_data_next == '') and not (time_traveller_prepare == True):
        embed.add_field(name=f'TRADE RATES A{area_no+1}', value=traderates_next, inline=True)
    embed.add_field(name='NOTE', value=note, inline=False)
    
    return embed