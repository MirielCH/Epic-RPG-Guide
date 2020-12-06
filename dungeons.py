# dungeons.py

import discord
import emojis
import global_data
from humanfriendly import format_timespan

# Create field "Recommended Stats"
async def design_field_rec_stats(field_rec_stats_data, short_version=False):
    
    player_at = field_rec_stats_data[0]
    player_def = field_rec_stats_data[1]
    player_carry_def = field_rec_stats_data[2]
    player_life = field_rec_stats_data[3]
    life_boost = field_rec_stats_data[4]
    player_level = field_rec_stats_data[5]
    dungeon_no = field_rec_stats_data[6]

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
        field_value =   f'{emojis.bp} {emojis.statat} **AT**: {player_at}\n'\
                        f'{emojis.bp} {emojis.statdef} **DEF**: {player_def} {player_carry_def}\n'\
                        f'{emojis.bp} {emojis.statlife} **LIFE**: {player_life} {life_boost}\n'\
                        f'{emojis.bp} {emojis.statlevel} **LEVEL**: {player_level}'
    else:
        field_value =   f'{emojis.statat} **AT**: {player_at}\n'\
                        f'{emojis.statdef} **DEF**: {player_def} {player_carry_def}\n'\
                        f'{emojis.statlife} **LIFE**: {player_life} {life_boost}\n'\
                        f'{emojis.statlevel} **LEVEL**: {player_level}\n{emojis.blank}'
    
    return field_value

# Create field "Recommended gear"
async def design_field_rec_gear(field_rec_gear_data):
    
    player_sword = field_rec_gear_data[0]
    player_sword_enchant = field_rec_gear_data[1]
    player_sword_emoji = getattr(emojis, field_rec_gear_data[2])
    player_armor = field_rec_gear_data[3]
    player_armor_enchant = field_rec_gear_data[4]
    player_armor_emoji = getattr(emojis, field_rec_gear_data[5])
    
    if not player_armor_enchant == '':
        player_armor_enchant = f'[{player_armor_enchant}]'
    
    if not player_sword_enchant == '':
        player_sword_enchant = f'[{player_sword_enchant}]'
    
    field_value =   f'{emojis.bp} {player_sword_emoji} {player_sword} {player_sword_enchant}\n'\
                    f'{emojis.bp} {player_armor_emoji} {player_armor} {player_armor_enchant}'
    
    return field_value

# Create field "Check dungeon stats"
async def design_field_check_stats(field_check_stats_data, user_data, prefix, short_version):
    
    user_at = user_data[0]
    user_def = user_data[1]
    user_life = user_data[2]
    
    player_at = field_check_stats_data[0]
    player_def = field_check_stats_data[1]
    player_carry_def = field_check_stats_data[2]
    player_life = field_check_stats_data[3]
    dungeon_no = field_check_stats_data[4]
    
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
        if not player_at == 0:
            if user_at < player_at:
                if user_def >= player_carry_def:
                    user_at_check_result = 'ignore'
                else:
                    user_at_check_result = 'fail'
            elif user_at >= player_at:
                user_at_check_result = 'pass'
        else:
            check_at = f'{emojis.checkignore} **AT**: -'
        
        if not player_def == 0:
            if user_def < player_def:
                user_def_check_result = 'fail'
            elif user_def >= player_def:
                user_def_check_result = 'pass'
        else:
            check_def = f'{emojis.checkignore} **DEF**: -'
    
        if not player_carry_def == 0:
            if user_def < player_carry_def:
                user_carry_def_check_result = 'fail'
            elif user_def >= player_carry_def:
                user_carry_def_check_result = 'pass'
        else:
            check_carry_def = f'{emojis.checkignore} **Carry DEF**: -'
            
        if not player_life == 0:
            if user_life < player_life:
                if user_def >= player_carry_def:
                        user_life_check_result = 'ignore'
                elif player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                else:
                    user_life_check_result = 'fail'
            elif user_life >= player_life:
                user_life_check_result = 'pass'
        else:
            check_life = f'{emojis.checkignore} **LIFE**: -'
    
    elif dungeon_no == 11:
        if user_at < player_at:
            user_at_check_result = 'fail'
        elif user_at >= player_at:
            user_at_check_result = 'pass'
        if user_life < player_life:
            if user_at_check_result == 'pass':
                if player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                elif (player_life - user_life) <= 200:
                    user_life_check_result = 'warn'
                else:
                    user_life_check_result = 'fail'
            else:
                if player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                else:
                    user_life_check_result = 'fail'
        elif user_life >= player_life:
            user_life_check_result = 'pass'
            
    elif dungeon_no == 12:
        if user_def < player_def:
            user_def_check_result = 'fail'
        elif user_def >= player_def:
            user_def_check_result = 'pass'
        if user_life < player_life:
            if player_life - user_life <= 10:
                user_life_check_result = 'passA'
            elif 11 <= (player_life - user_life) <= 25:
                user_life_check_result = 'passB'
            elif 26 <= (player_life - user_life) <= 50:
                user_life_check_result = 'passC'
            else:
                user_life_check_result = 'fail'
        elif user_life >= player_life:
            user_life_check_result = 'pass'
  
    elif dungeon_no == 13:
        if user_life < player_life:
            user_life_check_result = 'fail'
        else:
            user_life_check_result = 'pass'
  
    elif dungeon_no == 14:
        if user_def < player_def:
            user_def_check_result = 'fail'
        elif user_def >= player_def:
            user_def_check_result = 'pass'

    if user_at_check_result == 'pass':
        check_at = f'{emojis.checkok} **AT**: {player_at}'
    elif user_at_check_result == 'warn':
        check_at = f'{emojis.checkwarn} **AT**: {player_at}'
    elif user_at_check_result == 'fail':
        check_at = f'{emojis.checkfail} **AT**: {player_at}'
    elif user_at_check_result == 'ignore':
        check_at = f'{emojis.checkignore} **AT**: {player_at}'
    
    if user_def_check_result == 'pass':
        check_def = f'{emojis.checkok} **DEF**: {player_def}'
    elif user_def_check_result == 'warn':
        check_def = f'{emojis.checkwarn} **DEF**: {player_def}'
    elif user_def_check_result == 'fail':
        check_def = f'{emojis.checkfail} **DEF**: {player_def}'
    elif user_def_check_result == 'ignore':
        check_def = f'{emojis.checkignore} **DEF**: {player_def}'
    
    if user_carry_def_check_result == 'pass':
        check_carry_def = f'{emojis.checkok} **Carry DEF**: {player_carry_def}'
    elif user_carry_def_check_result == 'warn':
        check_carry_def = f'{emojis.checkwarn} **Carry DEF**: {player_carry_def}'
    elif user_carry_def_check_result == 'fail':
        check_carry_def = f'{emojis.checkfail} **Carry DEF**: {player_carry_def}'
    elif user_carry_def_check_result == 'ignore':
        check_carry_def = f'{emojis.checkignore} **Carry DEF**: {player_carry_def}'
        
    if user_life_check_result == 'pass':
        check_life = f'{emojis.checkok} **LIFE**: {player_life}'
    elif user_life_check_result == 'passA':
        check_life = f'{emojis.checkok} **LIFE**: {player_life} • {emojis.lifeboost}**A**'
    elif user_life_check_result == 'passB':
        check_life = f'{emojis.checkok} **LIFE**: {player_life} • {emojis.lifeboost}**B**'
    elif user_life_check_result == 'passC':
        check_life = f'{emojis.checkok} **LIFE**: {player_life} • {emojis.lifeboost}**C**'
    elif user_life_check_result == 'warn':
        check_life = f'{emojis.checkwarn} **LIFE**: {player_life}'
    elif user_life_check_result == 'fail':
        check_life = f'{emojis.checkfail} **LIFE**: {player_life}'
    elif user_life_check_result == 'ignore':
        check_life = f'{emojis.checkignore} **LIFE**: {player_life}'
    
    if short_version == True:
        bulletpoint = ''
    else:
        bulletpoint = f'{emojis.bp}'
    
    field_value = ''
    if not check_at == 'N/A':
        field_value =   f'{bulletpoint} {check_at}'
    if not check_def == 'N/A':
        field_value =   f'{field_value}\n{bulletpoint} {check_def}'
    if not check_carry_def == 'N/A':
        field_value =   f'{field_value}\n{bulletpoint} {check_carry_def}'
    if not check_life == 'N/A':
        field_value =   f'{field_value}\n{bulletpoint} {check_life}'
    field_value = field_value.strip()
    if field_value == '':
        field_value = f'{bulletpoint}Stats irrelevant'
    if short_version == True:
        field_value =   f'{field_value}\n{emojis.blank}'                        
    
    if short_version == False:
        user_stats_check_results = [['AT',user_at_check_result], ['DEF', user_def_check_result], ['LIFE', user_life_check_result]]
        player_stats_check = [player_at, player_def, player_life]
        
        if dungeon_no in (10,15):
            check_results = f'{emojis.bp} Stats are irrelevant for this dungeon'
            if dungeon_no == 10:
                check_results = f'{check_results}\n{emojis.bp} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
            elif dungeon_no == 15:
                check_results = f'{check_results}\n{emojis.bp} This dungeon has various requirements (see `{prefix}d{dungeon_no}`)'
        elif dungeon_no == 11:
            if user_at_check_result == 'fail':
                check_results = f'{emojis.bp} You are not yet ready for this dungeon\n'\
                                f'{emojis.bp} You should increase your **AT** to **{player_at}**'
                if user_life_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.bp} You should increase your **LIFE** to **{player_life}** or more'
            else:
                if user_life_check_result == 'warn':
                    check_results = f'{emojis.bp} Your **LIFE** is below recommendation (**{player_life}**)\n'\
                                    f'{emojis.bp} You can still attempt the dungeon though, maybe you get lucky!'
                elif user_life_check_result == 'fail':
                    check_results = f'{emojis.bp} You are not yet ready for this dungeon\n'\
                                    f'{emojis.bp} You should increase your **LIFE** to **{player_life}** or more'
                else:
                    check_results = f'{emojis.bp} Your stats are high enough for this dungeon\n'\
                                    f'{emojis.bp} Note that this dungeon is luck based, so you can still die'
                    if (user_life_check_result == 'passA'):
                        check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost A to reach recommended **LIFE**'
                    if (user_life_check_result == 'passB'):
                        check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost B to reach recommended **LIFE**'
                    if (user_life_check_result == 'passC'):
                        check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost C to reach recommended **LIFE**'
            check_results = f'{check_results}\n{emojis.bp} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
        elif dungeon_no == 12:
            if (user_def_check_result == 'fail') or (check_life == 'fail'):
                check_results = f'{emojis.bp} You are not yet ready for this dungeon'    
                if user_def_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.bp} You should increase your **DEF** to **{player_def}**'
                if user_life_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.bp} You should increase your **LIFE** to **{player_life}** or more'
            else:
                check_results = f'{emojis.bp} You are ready for this dungeon'
                if (user_life_check_result == 'passA'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost A to reach recommended **LIFE**'
                if (user_life_check_result == 'passB'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost B to reach recommended **LIFE**'
                if (user_life_check_result == 'passC'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost C to reach recommended **LIFE**'
                check_results = f'{check_results}\n{emojis.bp} Note that higher **LIFE** will still help in beating the dungeon'    
            check_results = f'{check_results}\n{emojis.bp} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
        elif dungeon_no == 13:
            if user_life_check_result == 'fail':
                check_results = f'{emojis.bp} You are not yet ready for this dungeon\n'\
                                f'{emojis.bp} You should increase your **LIFE** to **{player_life}** or more\n'\
                                f'{emojis.bp} The **LIFE** is for crafting the {emojis.swordomega} OMEGA Sword, not the dungeon\n'\
                                f'{emojis.bp} **Important**: This is **base LIFE**, before buying a {emojis.lifeboost} LIFE boost'
            else:
                check_results = f'{emojis.bp} Your stats are high enough for this dungeon'
            check_results = f'{check_results}\n{emojis.bp} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
                
        elif dungeon_no == 14:
            if user_def_check_result == 'fail':
                check_results = f'{emojis.bp} You are not yet ready for this dungeon\n'\
                                f'{emojis.bp} You should increase your **DEF** to **{player_def}**'
            else:
                check_results = f'{emojis.bp} Your stats are high enough for this dungeon'
                if (user_life_check_result == 'passA'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost A to reach recommended **LIFE**'
                if (user_life_check_result == 'passB'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost B to reach recommended **LIFE**'
                if (user_life_check_result == 'passC'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost C to reach recommended **LIFE**'
            check_results = f'{check_results}\n{emojis.bp} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
                
        else:
            if user_carry_def_check_result == 'pass':
                check_results = f'{emojis.bp} You are ready **and** can carry other players'
                for check in user_stats_check_results:
                    if (check[1] == 'ignore') or (check[1] == 'warn'):
                        check_results = f'{check_results}\n{emojis.bp} Your **{check[0]}** is low but can be ignored because of your DEF'
            elif (user_at_check_result == 'fail') or (user_def_check_result == 'fail') or (user_life_check_result == 'fail'):
                check_results = f'{emojis.bp} You are not yet ready for this dungeon'
                for x, check in enumerate(user_stats_check_results):
                    if check[1] == 'fail':
                        check_results = f'{check_results}\n{emojis.bp} You should increase your **{check[0]}** to **{player_stats_check[x]}**'
                check_results = f'{check_results}\n{emojis.bp} However, you can still do this dungeon if you get carried'
            elif (user_at_check_result == 'pass') and (user_def_check_result == 'pass') and ((user_life_check_result == 'pass') or (user_life_check_result == 'passA') or (user_life_check_result == 'passB') or (user_life_check_result == 'passC')):
                check_results = f'{emojis.bp} Your stats are high enough for this dungeon'
                if (user_life_check_result == 'passA'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost A to reach recommended **LIFE**'
                if (user_life_check_result == 'passB'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost B to reach recommended **LIFE**'
                if (user_life_check_result == 'passC'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost C to reach recommended **LIFE**'
            
    else:
        check_results = 'N/A'
        
    return (field_value, check_results)

# Create dungeon embed
async def dungeon(dungeon_data, prefix):
    
    dungeon_no = dungeon_data[0]
    dungeon_tt = dungeon_data[1]
    boss_name = dungeon_data[2]
    boss_emoji = getattr(emojis, dungeon_data[3])
    boss_at = dungeon_data[4]
    boss_life = dungeon_data[5]
    min_players = dungeon_data[6]
    max_players = dungeon_data[7]
    key_price = dungeon_data[8]
    player_at = dungeon_data[9]
    player_def = dungeon_data[10]
    player_carry_def = dungeon_data[11]
    player_life = dungeon_data[12]
    life_boost = dungeon_data[13]
    player_level = dungeon_data[14]
    player_sword = dungeon_data[15]
    player_sword_enchant = dungeon_data[16]
    player_armor = dungeon_data[17]
    player_armor_enchant = dungeon_data[18]
    time_limit = format_timespan(dungeon_data[19])
    player_sword_emoji = getattr(emojis, dungeon_data[20])
    player_armor_emoji = getattr(emojis, dungeon_data[21])
    img_dungeon = ''
    image_url = ''
    
    field_rec_stats_data = (player_at, player_def, player_carry_def, player_life, life_boost, player_level, dungeon_no)
    field_rec_stats = await design_field_rec_stats(field_rec_stats_data)
    
    field_rec_gear_data = (player_sword, player_sword_enchant, dungeon_data[20], player_armor, player_armor_enchant, dungeon_data[21])
    field_rec_gear = await design_field_rec_gear(field_rec_gear_data)
    
    if min_players == max_players:
        players = f'{emojis.bp} {min_players}'
    else:
        players = f'{emojis.bp} {min_players}-{max_players}'
        boss_life = f'{boss_life} per player'
    
    if boss_at == 0:
        boss_at = '-'
    else:
        boss_at = f'~{boss_at}'
    
    if not boss_life == 0:
        try:
            boss_life = f'{dungeon_data[5]:,}'
        except:
            boss_life = int(dungeon_data[5])
    else:
        boss_life = '-'
    
    if not key_price == 0:
        try:
            key_price = f'{dungeon_data[8]:,}'
        except:
            key_price = int(dungeon_data[8])
        key_price = f'{key_price} coins'
    else:
        key_price = f'You can only enter this dungeon with a {emojis.horset6} T6+ horse.'
    
    if 1 <= dungeon_no <= 9:
        embed_description = 'This is a simple stats based dungeon.'
        requirements = f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse'
        strategy = f'{emojis.bp} Use `stab` or `power`'
        strategy_name = 'STRATEGY'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1}'
    elif dungeon_no == 10:
        embed_description = f'This is a scripted strategy dungeon.'
        requirements = f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse\n'\
                       f'{emojis.bp} {player_sword_emoji} {player_sword}\n {emojis.bp} {player_armor_emoji} {player_armor}'
        strategy = f'{emojis.bp} The player that starts the dungeon gets the attacker role.\n'\
                  f'{emojis.bp} The other player gets the defender role.\n'\
                  f'{emojis.bp} Attacker command sequence:\n{emojis.blank} `charge edgy sword` x20\n{emojis.blank} `attack`\n'\
                  f'{emojis.bp} Defender command sequence:\n{emojis.blank} `weakness spell`\n{emojis.blank} `protect`\n{emojis.blank} `charge edgy armor` x4\n{emojis.blank} `protect` x2\n{emojis.blank} `invulnerability`\n{emojis.blank} `healing spell`\n{emojis.blank} `protect` x5\n'\
                  f'{emojis.bp} Note: The defender will die before the boss.'
        strategy_name = 'STRATEGY'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1}'
    elif dungeon_no == 11:
        embed_description = f'This is a randomized puzzle-based dungeon.'
        requirements = f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse\n'\
                       f'{emojis.bp} {player_sword_emoji} {player_sword}\n{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        strategy =  f'{emojis.bp} You can move left, right, up, down or pass\n'\
                    f'{emojis.bp} Your goal is to reach and hit the boss until it dies\n'\
                    f'{emojis.bp} Each point of AT you have does 1 damage to the boss\n'\
                    f'{emojis.bp} You can only attack if you stand right next to the boss\n'\
                    f'{emojis.bp} After you hit the boss, your position will reset\n'\
                    f'{emojis.bp} If you end up on a fireball, you take 100 damage\n'\
                    f'{emojis.bp} If you pass a turn, you take 10 damage\n'\
                    f'{emojis.bp} The board scrolls down one line with every move you make\n'\
                    f'{emojis.bp} You do **not** move down with the board\n'\
                    f'{emojis.bp} **The board moves first** when you make a move\n'\
                    f'{emojis.bp} Check the image below to see the movement behaviour\n'\
                    f'{emojis.bp} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Dungeon_11)'
        strategy_name = 'TIPS'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1}'
        img_dungeon = discord.File(global_data.dungeon11, filename='dungeon11.png')
        image_url = 'attachment://dungeon11.png'
        image_name = 'MOVEMENT BEHAVIOUR'
    elif dungeon_no == 12:
        embed_description = f'This is a randomized puzzle-based dungeon.'
        requirements = f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse\n'\
                       f'{emojis.bp} {player_armor_emoji} {player_armor}\n{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        strategy = f'{emojis.bp} https://epic-rpg.fandom.com/wiki/Dungeon_12'
        strategy_name = 'TIPS'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1}'
    elif dungeon_no == 13:
        embed_description = f'This is a trivia themed strategy dungeon.'
        requirements = f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse\n'\
                       f'{emojis.bp} {player_sword_emoji} {player_sword}\n{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        strategy =  f'{emojis.bp} You start in room 1, 2 or 3\n'\
                    f'{emojis.bp} Your goal is to reach the dragon\'s room\n'\
                    f'{emojis.bp} In each room you will be asked one question\n'\
                    f'{emojis.bp} Your answer determines your next room\n'\
                    f'{emojis.bp} Refer to the image below for a walkthrough\n'\
                    f'{emojis.bp} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Dungeon_13)'
        strategy_name = 'STRATEGY'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1}'
        img_dungeon = discord.File(global_data.dungeon13, filename='dungeon13.png')
        image_url = 'attachment://dungeon13.png'
        image_name = 'WALKTHROUGH'
    elif dungeon_no == 14:
        embed_description = f'This is a strategy dungeon.'
        requirements = f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse\n'\
                       f'{emojis.bp} {player_armor_emoji} {player_armor}\n{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        strategy = f'{emojis.bp} https://epic-rpg.fandom.com/wiki/Dungeon_14'
        strategy_name = 'STRATEGY'
        boss_life = f'2x {boss_life}'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1}'
    elif dungeon_no == 15:
        embed_description = f'This is a strategy dungeon.'
        requirements = f'{emojis.bp} {emojis.horset6} T6+ horse\n'\
                       f'{emojis.bp} {player_sword_emoji} {player_sword}\n {emojis.bp} {player_armor_emoji} {player_armor}\n'\
                       f'{emojis.bp} {emojis.petcat} T4+ cat pet\n{emojis.bp} {emojis.petdog} T4+ dog pet\n{emojis.bp} {emojis.petdragon} T4+ dragon pet\n'\
                       f'{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        strategy = f'{emojis.bp} https://epic-rpg.fandom.com/wiki/Dungeon_15'
        strategy_name = 'STRATEGY'
        rewards = f'{emojis.bp} {emojis.timekey} TIME key to unlock super time travel (see `{prefix}stt`)'
    else:
        embed_description = ''
        rewards = 'N/A'
        requirements = f'{emojis.bp} N/A'
        strategy = f'{emojis.bp} N/A'
        strategy_name = 'STRATEGY'
        
    embed = discord.Embed(
        color = global_data.color,
        title = f'DUNGEON {dungeon_no}',
        description = embed_description
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='BOSS', value=f'{emojis.bp} {boss_emoji} {boss_name}', inline=False)
    embed.add_field(name='PLAYERS', value=players, inline=False)
    embed.add_field(name='TIME LIMIT', value=f'{emojis.bp} {time_limit}', inline=False)
    embed.add_field(name='REWARDS', value=rewards, inline=False)
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='DUNGEON KEY PRICE', value=f'{emojis.bp} {key_price}', inline=False)
    embed.add_field(name='BOSS STATS', value=f'{emojis.bp} {emojis.statat} **AT**: {boss_at}\n'
                    f'{emojis.bp} {emojis.statlife} **LIFE**: {boss_life}', inline=False)
    embed.add_field(name='RECOMMENDED GEAR', value=field_rec_gear, inline=False)
    embed.add_field(name='RECOMMENDED STATS', value=field_rec_stats, inline=False)
    embed.add_field(name=strategy_name, value=strategy, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}dc{dungeon_no}` : Check if you\'re ready for this dungeon\n{emojis.bp} `{prefix}dg` : Recommended gear (all dungeons)\n{emojis.bp} `{prefix}ds` : Recommended stats (all dungeons)', inline=False)
    if not image_url == '':
        embed.set_image(url=image_url)
        embed.add_field(name=image_name, value=f'** **', inline=False)
    
    return (img_dungeon, embed)
    
# Recommended stats for all dungeons
async def dungeon_rec_stats(rec_stats_data, prefix):

    embed = discord.Embed(
        color = global_data.color,
        title = f'RECOMMENDED STATS FOR ALL DUNGEONS',
        description = f'\u200b'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    
    for dung_x in rec_stats_data:
        dungeon_no = dung_x[6]
        
        field_rec_stats = await design_field_rec_stats(dung_x, True)
        embed.add_field(name=f'DUNGEON {dungeon_no}', value=field_rec_stats, inline=True)
        
    embed.add_field(name='ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}d1`-`{prefix}d15` : Guide for dungeon 1~15\n{emojis.bp} `{prefix}dg` : Recommended gear (summary)', inline=False)
            
    return embed

# Recommended gear for all dungeons
async def dungeon_rec_gear(rec_gear_data, prefix, page):

    if page == 1:
        title_value = f'RECOMMENDED GEAR FOR DUNGEONS 1 TO 9'
        description_value = f'➜ See `{prefix}dg2` for dungeons 10 to 15.'
    elif page == 2:
        title_value = f'RECOMMENDED GEAR FOR DUNGEONS 10 TO 15'
        description_value = f'➜ See `{prefix}dg1` for dungeons 1 to 9.'
                    
    embed = discord.Embed(
        color = global_data.color,
        title = title_value,
        description = description_value
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    
    for dung_x in rec_gear_data:
        dungeon_no = dung_x[6]
        field_rec_gear = await design_field_rec_gear(dung_x)
        embed.add_field(name=f'DUNGEON {dungeon_no}', value=field_rec_gear, inline=False)
    
    embed.add_field(name='ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}d1`-`{prefix}d15` : Guide for dungeon 1~15\n{emojis.bp} `{prefix}ds` : Recommended stats (summary)', inline=False)
            
    return embed
    
# Stats check (all dungeons)
async def dungeon_check_stats(dungeon_check_data, user_stats, ctx):

    legend =    f'{emojis.bp} {emojis.checkok} : Stat is above recommendation\n'\
                f'{emojis.bp} {emojis.checkfail} : Stat is below recommendation\n'\
                f'{emojis.bp} {emojis.checkignore} : Stat is below rec. but you are above carry DEF\n'\
                f'{emojis.bp} {emojis.checkwarn} : Stat is below rec. but with a lot of luck it _might_ work\n'\
                f'{emojis.bp} {emojis.lifeboost} : LIFE boost you have to buy to reach recommendation'
    
    notes =     f'{emojis.bp} You can ignore this check for D1-D9 if you get carried\n'\
                f'{emojis.bp} This only checks stats, you may still need certain gear for D10+!\n'\
                f'{emojis.bp} Use `{ctx.prefix}dc1`-`{ctx.prefix}dc15` for individual checks with more details'
    
    embed = discord.Embed(
        color = global_data.color,
        title = f'DUNGEON STATS CHECK',
        description = f'**{ctx.author.name}**, here\'s your check for **{user_stats[0]} AT**, **{user_stats[1]} DEF** and **{user_stats[2]} LIFE.**'
    )    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    
    for dung_x in dungeon_check_data:
        dungeon_no = dung_x[4]
        dungeon_no = int(dungeon_no)
        
        field_check_stats = await design_field_check_stats(dung_x, user_stats, ctx.prefix, True)
        embed.add_field(name=f'DUNGEON {dungeon_no}', value=field_check_stats[0], inline=True)
    
    embed.add_field(name='LEGEND', value=legend, inline=False)
    embed.add_field(name='NOTE', value=notes, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=f'{emojis.bp} `{ctx.prefix}d1`-`{ctx.prefix}d15` : Guide for dungeon 1~15\n{emojis.bp} `{ctx.prefix}dg` : Recommended gear (summary)', inline=False)
            
    return embed

# Stats check (dungeon specific)
async def dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx):

    legend =    f'{emojis.bp} {emojis.checkok} : Stat is above recommendation\n'\
                f'{emojis.bp} {emojis.checkfail} : Stat is below recommendation\n'\
                f'{emojis.bp} {emojis.checkignore} : Stat is below rec. but you are above carry DEF\n'\
                f'{emojis.bp} {emojis.checkwarn} : Stat is below rec. but with a lot of luck it _might_ work\n'\
                f'{emojis.bp} {emojis.lifeboost} : LIFE boost you have to buy to reach recommendation'
    
    notes =     f'{emojis.bp} You can ignore this check for D1-D9 if you get carried\n'\
                f'{emojis.bp} This check does **not** take into account required gear for D10+!\n'\
                f'{emojis.bp} Use `{ctx.prefix}dc1`-`{ctx.prefix}dc15` for a few more details'
    
    dungeon_no = dungeon_check_data[4]
    
    embed = discord.Embed(
        color = global_data.color,
        title = f'DUNGEON {dungeon_no} STATS CHECK',
        description = f'**{ctx.author.name}**, here\'s your check for **{user_stats[0]} AT**, **{user_stats[1]} DEF** and **{user_stats[2]} LIFE.**'
    )    
    embed.set_footer(text=f'Tip: Use {ctx.prefix}dc to see a check of ALL dungeons.')
    
    field_check_stats = await design_field_check_stats(dungeon_check_data, user_stats, ctx.prefix, False)
    
    embed.add_field(name=f'CHECK RESULT', value=field_check_stats[0], inline=False)
    embed.add_field(name=f'DETAILS', value=field_check_stats[1], inline=False)
    #embed.add_field(name=f'LEGEND', value=legend, inline=False)
    #embed.add_field(name='ADDITIONAL GUIDES', value=f'{emojis.bp} `{ctx.prefix}dcheck` : Dungeon stats check for ALL dungeons\n{emojis.bp} `{ctx.prefix}d1`-`{ctx.prefix}d15` : Guide for dungeon 1~15\n{emojis.bp} `{ctx.prefix}dg` : Recommended gear (summary)', inline=False)
            
    return embed