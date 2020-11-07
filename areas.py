# areas.py

import discord
import emojis
import global_data
import dungeons
import trading

# Create area embed
async def area(area_data, mats_data, traderate_data, traderate_data_next, user_settings, user_name, prefix):
    
    area_no = int(area_data[0])
    work_cmd_poor = area_data[1]
    work_cmd_rich = area_data[2]
    work_cmd_asc = area_data[3]
    new_cmd_1 = area_data[4]
    new_cmd_2 = area_data[5]
    new_cmd_3 = area_data[6]
    rich_threshold = area_data[7]
    upgrade_sword = area_data[8]
    upgrade_sword_enchant = area_data[9]
    upgrade_armor = area_data[10]
    upgrade_armor_enchant = area_data[11]
    area_description = area_data[12]
    dungeon_no = area_data[13]
    player_sword_emoji = area_data[14]
    player_armor_emoji = area_data[15]
    player_at = area_data[16]
    player_def = area_data[17]
    player_carry_def = area_data[18]
    player_life = area_data[19]
    life_boost = area_data[20]
    player_level = area_data[21]
    player_sword = area_data[22]
    player_sword_enchant = area_data[23]
    player_armor = area_data[24]
    player_armor_enchant = area_data[25]
    user_tt = int(user_settings[0])
    user_asc = user_settings[1]

    if not mats_data == '':
        mats_fish = mats_data[1] 
        mats_apple = mats_data[2]
        if not mats_fish == 0:
            try:
                mats_fish = f'{mats_fish:,}'.replace(',','\'')
            except:
                mats_fish = int(mats_fish)
            
        if not mats_apple == 0:
            try:
                mats_apple = f'{mats_apple:,}'.replace(',','\'')
            except:
                mats_apple = int(mats_apple)

    field_rec_stats_data = (player_at, player_def, player_carry_def, player_life, life_boost, player_level, dungeon_no)
    field_rec_stats = await dungeons.design_field_rec_stats(field_rec_stats_data)
    
    if ((area_no == 12) and (user_tt < 1)) or ((area_no == 13) and (user_tt < 3)) or ((area_no == 14) and (user_tt < 5)) or ((area_no == 15) and (user_tt < 10)):
        time_traveller_area_locked = True
    else:
        time_traveller_area_locked = False
    
    if ((area_no == 11) and (user_tt == 0)) or ((area_no == 12) and (1 <= user_tt <= 2)) or ((area_no == 13) and (3 <= user_tt <= 4)) or ((area_no == 14) and (5 <= user_tt <= 9)) or ((area_no == 15) and (10 <= user_tt <= 24)):
        time_traveller_prepare = True
    else:
        time_traveller_prepare = False
        
    # Footer
    if time_traveller_prepare == False:
        footer = f'Tip: Use {prefix}d{dungeon_no} for details about the next dungeon.'
    else:
        footer = f'Tip: To see the full page use {prefix}a{area_no} full.'
        
    # Description
    if len(user_settings) > 2:
        if user_settings[2] == 'override':
            description = f'This is the guide for **TT {user_tt}**, **{user_asc}**.\n**You are seeing TT 25 because you used the parameter** `full`.'
    else:
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
                quick_guide_enchant_sword = f'\n {emojis.bp} Enchant {player_sword_emoji} {player_sword} to [{player_sword_enchant}+]'
        player_sword_enchant = f'[{player_sword_enchant}]'
    
    if not player_armor_enchant == '':
        if upgrade_armor == 'true':
            quick_guide_enchant_armor = f' and enchant to [{player_armor_enchant}+]'
        else:
            if upgrade_armor_enchant == 'true':
                quick_guide_enchant_armor = f'\n {emojis.bp} Enchant {player_armor_emoji} {player_armor} to [{player_armor_enchant}+]'
        player_armor_enchant = f'[{player_armor_enchant}]'

    if time_traveller_prepare == True:
        quick_guide = f'{emojis.bp} {emojis.timetravel} Prepare for time travel (see `{prefix}tt{user_tt+1}`)'
    elif (1 <= area_no <= 4) and (user_tt == 0) :
        if not player_level == 0:
            quick_guide = f'{emojis.bp} Reach level {player_level}{quick_guide_sword}{quick_guide_enchant_sword}{quick_guide_armor}{quick_guide_enchant_armor}'
        else:
            quick_guide = f'{quick_guide_sword}{quick_guide_enchant_sword}{quick_guide_armor}{quick_guide_enchant_armor}'
    elif (area_no == 3) and (user_tt > 4):
        quick_guide = f'{emojis.bp} Farm the materials mentioned below\n{emojis.bp} Reach level {player_level}{quick_guide_sword}{quick_guide_enchant_sword}{quick_guide_armor}{quick_guide_enchant_armor}\n{emojis.bp} Buy {emojis.lbedgy} EDGY lootbox on cooldown'
    elif area_no in (5,8):
        if not player_level == 0:
            quick_guide = f'{emojis.bp} Farm the materials mentioned below\n{emojis.bp} Reach level {player_level}{quick_guide_sword}{quick_guide_enchant_sword}{quick_guide_armor}{quick_guide_enchant_armor}\n{emojis.bp} Buy {emojis.lbedgy} EDGY lootbox on cooldown'
        else:
            quick_guide = f'{emojis.bp} Farm the materials mentioned below\n{quick_guide_sword}{quick_guide_enchant_sword}{quick_guide_armor}{quick_guide_enchant_armor}\n{emojis.bp} Buy {emojis.lbedgy} EDGY lootbox on cooldown'
    elif area_no == 9:
        if not player_level == 0:
            quick_guide = f'{emojis.bp} Go back to previous areas if you are missing materials for crafting the armor (see `{prefix}drops`)\n{emojis.bp} Reach level {player_level}{quick_guide_sword}{quick_guide_enchant_sword}{quick_guide_armor}{quick_guide_enchant_armor}\n{emojis.bp} Buy {emojis.lbedgy} EDGY lootbox on cooldown'
        else:
            quick_guide = f'{emojis.bp} Go back to previous areas if you are missing materials for crafting the armor (see `{prefix}drops`)\n{quick_guide_sword}{quick_guide_enchant_sword}{quick_guide_armor}{quick_guide_enchant_armor}\n{emojis.bp} Buy {emojis.lbedgy} EDGY lootbox on cooldown'
    else:
        if not player_level == 0:
            if area_no == 3:
                quick_guide = f'{emojis.bp} Reach level {player_level}{quick_guide_sword}{quick_guide_enchant_sword}{quick_guide_armor}{quick_guide_enchant_armor}\n{emojis.bp} Buy {emojis.lbedgy} EDGY lootbox on cooldown'
            else:
                quick_guide = f'{emojis.bp} Reach level {player_level}{quick_guide_sword}{quick_guide_enchant_sword}{quick_guide_armor}{quick_guide_enchant_armor}\n{emojis.bp} Buy {emojis.lbedgy} EDGY lootbox on cooldown'
        else:
            quick_guide = f'{quick_guide_sword}{quick_guide_enchant_sword}{quick_guide_armor}{quick_guide_enchant_armor}\n{emojis.bp} Buy {emojis.lbedgy} EDGY lootboxes on cooldown'
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
    if 1 <= area_no <= 9:
        if user_asc == 'ascended':
            work_cmd = f'{emojis.bp} `ascended {work_cmd_asc}`'
        else:
            if rich_threshold == -1:
                work_cmd = f'{emojis.bp} `{work_cmd_poor}`'
            else:
                work_cmd = f'{emojis.bp} `{work_cmd_poor}` if you have less than {rich_threshold}m coins\n'\
                           f'{emojis.bp} `{work_cmd_rich}` if you have more than {rich_threshold}m coins'
    elif 10 <= area_no <= 11:
        if (area_no == 11) and (user_tt == 0):
            work_cmd = f'{emojis.bp} `drill` if you need coins'
        else:
            if user_asc == 'ascended':
                work_cmd = f'{emojis.bp} `ascended dynamite` if not in round down TT (see `{prefix}tt`)\n'\
                            f'{emojis.bp} `chainsaw` otherwise'
            else:
                if rich_threshold == -1:
                    work_cmd = f'{emojis.bp} `{work_cmd_poor}`'
                else:
                    work_cmd = f'{emojis.bp} `{work_cmd_poor}` if you have less than {rich_threshold}m coins\n'\
                                f'{emojis.bp} `{work_cmd_rich}` if you have more than {rich_threshold}m coins'
    elif 12 <= area_no <= 15:
        work_cmd = f'{emojis.bp} `chainsaw` if you need logs\n'\
                   f'{emojis.bp} `greenhouse` if you need apples or bananas\n'\
                   f'{emojis.bp} `dynamite` if you need coins'
    
    # Materials areas 3, 5 and 8
    if area_no == 5:
        materials = f'{emojis.bp} 30+ {emojis.wolfskin} wolf skins\n'\
                    f'{emojis.bp} 30+ {emojis.zombieeye} zombie eyes\n'\
                    f'{emojis.bp} 30+ {emojis.unicornhorn} unicorn horns (after crafting)'
        if user_tt < 5:
            materials = f'{materials}\n{emojis.bp} {mats_apple} {emojis.apple} apples'
    
    if (area_no == 3) and (user_tt > 4):
        materials = f'{emojis.bp} {mats_fish} {emojis.fish} normie fish'
        
    if area_no == 8:
        materials = f'{emojis.bp} 30 {emojis.mermaidhair} mermaid hairs\n'
    # Trades
    trades = await trading.design_field_trades(area_no)
    
    # Trade rates
    traderates = await trading.design_field_traderate(traderate_data)
    if not traderate_data_next == '':
        traderates_next = await trading.design_field_traderate(traderate_data_next)
            
    # Embed
    embed = discord.Embed(
        color = global_data.color,
        title = f'AREA {area_no}',
        description = description  
            
    )    
    embed.set_footer(text=footer)
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    if not area_locked == '':
            embed.add_field(name='AREA LOCKED', value=area_locked, inline=False)
    embed.add_field(name='QUICK GUIDE', value=quick_guide, inline=False)
    if (area_no > 1) and (user_asc != 'ascended') and (new_cmd != ''):
        embed.add_field(name='NEW COMMANDS', value=f'{emojis.bp} {new_cmd}', inline=False)
    embed.add_field(name='BEST WORK COMMAND', value=work_cmd, inline=False)
    if not time_traveller_prepare == True:
        embed.add_field(name=f'REC. MINIMUM GEAR FOR D{dungeon_no}', value=f'{emojis.bp} {player_sword_emoji} {player_sword} {player_sword_enchant}\n'
                             f'{emojis.bp} {player_armor_emoji} {player_armor} {player_armor_enchant}', inline=False)
        embed.add_field(name=f'RECOMMENDED STATS FOR D{dungeon_no}', value=field_rec_stats, inline=False)
    if ((area_no == 3) and (user_tt > 4)) or (area_no in (5,8)):
        embed.add_field(name='MATERIALS TO FARM', value=materials, inline=False)
    if not time_traveller_prepare == True:
        embed.add_field(name='TRADES BEFORE LEAVING', value=trades, inline=False)
    embed.add_field(name=f'TRADE RATES A{area_no}', value=traderates, inline=True)
    if not (traderate_data_next == '') and not (time_traveller_prepare == True):
        embed.add_field(name=f'TRADE RATES A{area_no+1}', value=traderates_next, inline=True)
    embed.add_field(name=f'NOTE', value=f'This is the guide for **TT {user_tt}**, **{user_asc}**.\nIf this is wrong, run `{prefix}setprogress`.', inline=False)
    
    
    
    
    return (thumbnail, embed)