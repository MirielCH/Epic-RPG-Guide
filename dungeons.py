# dungeons.py

import discord
import sqlite3
import emojis
import global_data

# Create field "Recommended Stats"
async def design_field_rec_stats(field_rec_stats_data):
    
    if field_rec_stats_data[4] == 'true':
        life_boost = '(buy LIFE boost if necessary)'
    else:
        life_boost = ''
    
    field_name = 'RECOMMENDED STATS'
    field_value = f'{emojis.bp} {emojis.statat} **AT**: {field_rec_stats_data[0]}\n'\
    f'{emojis.bp} {emojis.statdef} **DEF**: {field_rec_stats_data[1]} ({field_rec_stats_data[2]}+ to carry)\n'\
    f'{emojis.bp} {emojis.statlife} **LIFE**: {field_rec_stats_data[3]} {life_boost}\n'\
    f'{emojis.bp} {emojis.statlevel} **LEVEL**: {field_rec_stats_data[5]}'
    
    return (field_name, field_value)

# Create dungeon embed
async def dungeon(dungeon_data, footer):
    
    if dungeon_data[6] == dungeon_data[7]:
        players = f'{emojis.bp} {dungeon_data[6]}'
    else:
        players = f'{emojis.bp} {dungeon_data[6]}-{dungeon_data[7]}'
    
    if 1 <= dungeon_data[0] <= 9:
        requirements = f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse'
        tactics = 'Use `stab` or `power`'
        
    key_price = "{:,}".format(dungeon_data[8]).replace(',','\'')
    boss_life = "{:,}".format(dungeon_data[5]).replace(',','\'')
    
    field_rec_stats_data = (dungeon_data[9], dungeon_data[10], dungeon_data[11], dungeon_data[12], dungeon_data[13], dungeon_data[14])
    field_rec_stats = await design_field_rec_stats(field_rec_stats_data)
    
    embed = discord.Embed(
        color = 8983807,
        title = f'DUNGEON {dungeon_data[0]}'
    )    
    embed.set_footer(text=footer)
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    embed.add_field(name='BOSS', value=f'{emojis.bp} {dungeon_data[3]} {dungeon_data[2]}', inline=False)
    embed.add_field(name='PLAYERS', value=players, inline=False)
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='DUNGEON KEY PRICE', value=f'{emojis.bp} {key_price} coins', inline=False)
    embed.add_field(name='BOSS STATS', value=f'{emojis.bp} {emojis.statat} **AT**: {dungeon_data[4]}\n'
                    f'{emojis.bp} {emojis.statlife} **LIFE**: {boss_life} per player', inline=False)
    embed.add_field(name='RECOMMENDED GEAR', value=f'{emojis.bp} {dungeon_data[19]} **{dungeon_data[15]}** [{dungeon_data[16]}]\n'
                    f'{emojis.bp} {dungeon_data[20]} **{dungeon_data[17]}** [{dungeon_data[18]}]', inline=False)
    embed.add_field(name=field_rec_stats[0], value=field_rec_stats[1], inline=False)
    embed.add_field(name='TACTICS', value=f'{emojis.bp} {tactics}', inline=False)
    
    dungeon_embed = embed
    
    return (thumbnail, dungeon_embed)
        
    