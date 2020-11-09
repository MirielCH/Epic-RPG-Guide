# crafting.py

import discord
import global_data
import emojis

# Monster drops
async def drops(prefix):

    items =     f'Area: 1~2\nSource: {emojis.mobwolf}\nValue: 5\'000\n'\
                f'{emojis.bp} {emojis.zombieeye} **Zombie Eye** - {emojis.mobzombie} Zombie in areas **3~4**\n'\
                f'{emojis.bp} {emojis.unicornhorn} **Unicorn Horn** - {emojis.mobunicorn} Unicorn in areas **5~6**\n'\
                f'{emojis.bp} {emojis.mermaidhair} **Mermaid Hair** - {emojis.mobmermaid} Mermaid in areas **7~8**\n'\
                f'{emojis.bp} {emojis.chip} **Chip** - {emojis.mobkillerrobot} Killer Robot in areas **9~10**\n'\
                f'{emojis.bp} Area: 11~14\n{emojis.bp} Source: {emojis.mobbabydragon}{emojis.mobteendragon}{emojis.mobadultdragon}\n{emojis.bp} Value: 250\'000 coins'

    chance =    f'{emojis.bp} All items have a 2% base drop chance\n'\
                f'{emojis.bp} Every {emojis.timetravel} time travel increases the drop chance by ~25%\n'\
                f'{emojis.bp} A {emojis.horset7} T7+ horse increases the drop chance by 20%\n{emojis.blank}'

    embed = discord.Embed(
        color = global_data.color,
        title = f'MONSTER DROPS',
        description =   f'These items drop when using `hunt`, `hunt together` or when opening lootboxes.\n'\
                        f'You can go back to previous areas with `rpg area`.\n{emojis.blank}'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'WOLF SKIN {emojis.wolfskin}', value=f'{emojis.bp} Areas: 1~2\n{emojis.bp} Source: {emojis.mobwolf}\n{emojis.bp} Value: 500\n{emojis.blank}', inline=True)
    embed.add_field(name=f'ZOMBIE EYE {emojis.zombieeye}', value=f'{emojis.bp} Areas: 3~4\n{emojis.bp} Source: {emojis.mobzombie}\n{emojis.bp} Value: 2\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'UNICORN HORN {emojis.unicornhorn}', value=f'{emojis.bp} Areas: 5~6\n{emojis.bp} Source: {emojis.mobunicorn}\n{emojis.bp} Value: 7\'500\n{emojis.blank}', inline=True)
    embed.add_field(name=f'MERMAID HAIR {emojis.mermaidhair}', value=f'{emojis.bp} Areas: 7~8\n{emojis.bp} Source: {emojis.mobmermaid}\n{emojis.bp} Value: 30\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'CHIP {emojis.chip}', value=f'{emojis.bp} Areas: 9~10\n{emojis.bp} Source: {emojis.mobkillerrobot}\n{emojis.bp} Value: 100\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'DRAGON SCALE {emojis.dragonscale}', value=f'{emojis.bp} Areas: 11~14\n{emojis.bp} Source: {emojis.mobbabydragon}{emojis.mobteendragon}{emojis.mobadultdragon}\n{emojis.bp} Value: 250\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'DROP CHANCE', value=chance, inline=False)    
            
    return (thumbnail, embed)

# Trade rates of all areas
async def enchants(prefix):

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
               f'{emojis.bp} `transcend` - unlocked in area 15, costs 1m * area'

    embed = discord.Embed(
        color = global_data.color,
        title = f'ENCHANTS',
        description = f'Enchants buff either AT or DEF (sword enchants buff AT, armor enchants buff DEF). Enchants buff your **overall** stats.\n'\
                      f'The chance to get better enchants can be increased by leveling up the enchanter profession and having a {emojis.horset9} T9 horse.\n'\
                      f'See the [Wiki](https://epic-rpg.fandom.com/wiki/Enchant) for **base** chance estimates.'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
    embed.add_field(name=f'POSSIBLE ENCHANTS', value=buffs, inline=False)
    embed.add_field(name=f'COMMAND TIERS', value=commands, inline=False)
            
    return (thumbnail, embed)