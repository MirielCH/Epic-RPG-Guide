# crafting.py

import discord
import global_data
import emojis

# Trade rates of all areas
async def enchants():

    buffs = f'{emojis.bp} **Normie** - 5% buff\n'\
            f'{emojis.bp} **Good** - 15% buff\n'\
            f'{emojis.bp} **Great** - 25% buff\n'\
            f'{emojis.bp} **Mega** - 40% buff\n'\
            f'{emojis.bp} **Epic** - 60% buff\n'\
            f'{emojis.bp} **Hyper** - 70% buff\n'\
            f'{emojis.bp} **Ultimate** - 80% buff\n'\
            f'{emojis.bp} **Perfect** - 90% buff\n'\
            f'{emojis.bp} **EDGY** - 95% buff\n'\
            f'{emojis.bp} **ULTRA-EDGY** - 100% buff\n'\
            f'{emojis.bp} **OMEGA** - 125% buff, unlocked in {emojis.timetravel} TT 1\n'\
            f'{emojis.bp} **ULTRA-OMEGA** - 150% buff, unlocked in {emojis.timetravel} TT 3\n'\
            f'{emojis.bp} **GODLY** - 200% buff, unlocked in {emojis.timetravel} TT 5'
            
    commands = f'{emojis.bp} `enchant` - unlocked in area 2, costs 1k * area\n'\
               f'{emojis.bp} `refine` - unlocked in area 7, costs 10k * area\n'\
               f'{emojis.bp} `transmute` - unlocked in area 13, costs 100k * area\n'\
               f'{emojis.bp} `transcent` - unlocked in area 15, costs 1m * area'

    embed = discord.Embed(
        color = global_data.color,
        title = f'ENCHANTS',
        description = f'Enchants buff either AT or DEF (sword enchants buff AT, armor enchants buff DEF). Enchants buff your **overall** stats.\n'\
                      f'The chance to get better enchants can be increased by levelling up the enchanter profession and having a {emojis.horset9} T9 horse.\n'\
                      f'See the [Wiki](https://epic-rpg.fandom.com/wiki/Enchant) for **base** chance estimates.'
    )    
    embed.set_footer(text=global_data.footer)
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
    embed.add_field(name=f'POSSIBLE ENCHANTS', value=buffs, inline=False)
    embed.add_field(name=f'COMMAND TIERS', value=commands, inline=False)
            
    return (thumbnail, embed)