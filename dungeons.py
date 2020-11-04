# dungeons.py

import discord
import emojis
import global_data
from humanfriendly import format_timespan

# Create field "Recommended Stats"
async def design_field_rec_stats(field_rec_stats_data):
    
    player_at = field_rec_stats_data[0]
    player_def = field_rec_stats_data[1]
    player_carry_def = field_rec_stats_data[2]
    player_life = field_rec_stats_data[3]
    life_boost = field_rec_stats_data[4]
    player_level = field_rec_stats_data[5]
    dungeon_no = field_rec_stats_data[6]
    
    if life_boost == 'true':
        if dungeon_no < 11:
            life_boost = '(buy boost if necessary)'
        else:
            life_boost = '(buy boost and cook food if necessary)'
    else:
        life_boost = ''
    
    if not player_carry_def == 0:
        player_carry_def = f'({player_carry_def}+ to carry)'
    else:
        player_carry_def = ''
        
    if player_at == 0:
        player_at = '-'
    
    if player_def == 0:
        player_def = '-'
        
    if player_life == 0:
        player_life = '-'
    
    if player_level == 0:
        player_level = '-'
    
    field_name = 'REC. MINIMUM STATS'
    field_value = f'{emojis.bp} {emojis.statat} **AT**: {player_at}\n'\
    f'{emojis.bp} {emojis.statdef} **DEF**: {player_def} {player_carry_def}\n'\
    f'{emojis.bp} {emojis.statlife} **LIFE**: {player_life} {life_boost}\n'\
    f'{emojis.bp} {emojis.statlevel} **LEVEL**: {player_level}'
    
    return (field_name, field_value)

# Create dungeon embed
async def dungeon(dungeon_data):
    
    dungeon_no = dungeon_data[0]
    dungeon_tt = dungeon_data[1]
    boss_name = dungeon_data[2]
    boss_emoji = dungeon_data[3]
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
    player_sword_emoji = dungeon_data[20]
    player_armor_emoji = dungeon_data[21]
    
    field_rec_stats_data = (player_at, player_def, player_carry_def, player_life, life_boost, player_level, dungeon_no)
    field_rec_stats = await design_field_rec_stats(field_rec_stats_data)
    
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
            boss_life = f'{dungeon_data[5]:,}'.replace(',','\'')
        except:
            boss_life = int(dungeon_data[5])
    else:
        boss_life = '-'
    
    if not key_price == 0:
        try:
            key_price = f'{dungeon_data[8]:,}'.replace(',','\'')
        except:
            key_price = int(dungeon_data[8])
        key_price = f'{key_price} coins'
    else:
        key_price = f'You can only enter this dungeon with a {emojis.horset6} T6+ horse.'
    
    if not player_armor_enchant == '':
        player_armor_enchant = f'[{player_armor_enchant}]'
    
    if not player_sword_enchant == '':
        player_sword_enchant = f'[{player_sword_enchant}]'
    
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
        strategy = f'{emojis.bp} https://epic-rpg.fandom.com/wiki/Dungeon_11'
        strategy_name = 'TIPS'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1}'
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
        strategy = f'{emojis.bp} https://epic-rpg.fandom.com/wiki/Dungeon_13'
        strategy_name = 'STRATEGY'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1}'
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
        rewards = f'{emojis.bp} {emojis.timekey} TIME key to unlock SUPER time travel'
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
    embed.set_footer(text=global_data.footer)
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='BOSS', value=f'{emojis.bp} {boss_emoji} {boss_name}', inline=False)
    embed.add_field(name='PLAYERS', value=players, inline=False)
    embed.add_field(name='TIME LIMIT', value=f'{emojis.bp} {time_limit}', inline=False)
    embed.add_field(name='REWARDS', value=rewards, inline=False)
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='DUNGEON KEY PRICE', value=f'{emojis.bp} {key_price}', inline=False)
    embed.add_field(name='BOSS STATS', value=f'{emojis.bp} {emojis.statat} **AT**: {boss_at}\n'
                    f'{emojis.bp} {emojis.statlife} **LIFE**: {boss_life}', inline=False)
    embed.add_field(name='REC. MINIMUM GEAR', value=f'{emojis.bp} {player_sword_emoji} {player_sword} {player_sword_enchant}\n'
                    f'{emojis.bp} {player_armor_emoji} {player_armor} {player_armor_enchant}', inline=False)
    embed.add_field(name=field_rec_stats[0], value=field_rec_stats[1], inline=False)
    embed.add_field(name=strategy_name, value=strategy, inline=False)
    
    return (thumbnail, embed)
        
    