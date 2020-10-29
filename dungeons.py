# dungeons.py

import discord
import sqlite3
import emojis
import global_data

# Create field "Recommended Stats"
async def design_field_rec_stats(field_rec_stats_data):
    
    player_at = field_rec_stats_data[0]
    player_def = field_rec_stats_data[1]
    player_carry_def = field_rec_stats_data[2]
    player_life = field_rec_stats_data[3]
    life_boost = field_rec_stats_data[4]
    player_level = field_rec_stats_data[5]
    
    if life_boost == 'true':
        life_boost = '(buy LIFE boost if necessary)'
    else:
        life_boost = ''
    
    field_name = 'RECOMMENDED STATS'
    field_value = f'{emojis.bp} {emojis.statat} **AT**: {player_at}\n'\
    f'{emojis.bp} {emojis.statdef} **DEF**: {player_def} ({player_carry_def}+ to carry)\n'\
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
    boss_life = "{:,}".format(dungeon_data[5]).replace(',','\'')
    min_players = dungeon_data[6]
    max_players = dungeon_data[7]
    key_price = "{:,}".format(dungeon_data[8]).replace(',','\'')
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
    player_sword_emoji = dungeon_data[19]
    player_armor_emoji = dungeon_data[20]
    
    field_rec_stats_data = (player_at, player_def, player_carry_def, player_life, life_boost, player_level)
    field_rec_stats = await design_field_rec_stats(field_rec_stats_data)
    
    if min_players == max_players:
        players = f'{emojis.bp} {min_players}'
    else:
        players = f'{emojis.bp} {min_players}-{max_players}'
    
    if 1 <= dungeon_no <= 9:
        requirements = f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse'
        tactics = 'Use `stab` or `power`'
        
    embed = discord.Embed(
        color = 8983807,
        title = f'DUNGEON {dungeon_no}'
    )    
    embed.set_footer(text=global_data.footer)
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='BOSS', value=f'{emojis.bp} {boss_emoji} {boss_name}', inline=False)
    embed.add_field(name='PLAYERS', value=players, inline=False)
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='DUNGEON KEY PRICE', value=f'{emojis.bp} {key_price} coins', inline=False)
    embed.add_field(name='BOSS STATS', value=f'{emojis.bp} {emojis.statat} **AT**: {boss_at}\n'
                    f'{emojis.bp} {emojis.statlife} **LIFE**: {boss_life} per player', inline=False)
    embed.add_field(name='RECOMMENDED GEAR', value=f'{emojis.bp} {player_sword_emoji} **{player_sword}** [{player_sword_enchant}]\n'
                    f'{emojis.bp} {player_armor_emoji} **{player_armor}** [{player_armor_enchant}]', inline=False)
    embed.add_field(name=field_rec_stats[0], value=field_rec_stats[1], inline=False)
    embed.add_field(name='TACTICS', value=f'{emojis.bp} {tactics}', inline=False)
    
    return (thumbnail, embed)
        
    