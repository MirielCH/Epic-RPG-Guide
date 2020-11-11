# crafting.py

import discord
import global_data
import emojis
from operator import itemgetter


# List needed items for recipe
async def mats(items_data, amount, prefix):
    
    items_headers = items_data[0]
    
    for data_index, item in enumerate(items_data[1:]):
        item_name = item[2]            
        item_emoji = getattr(emojis, item[3])
    
        ingredients = []
    
        for item_index, value in enumerate(item[6:]):
            header_index = item_index+6
            if not value == 0:               
                if items_headers[header_index] == 'log':
                    ingredients.append([value, emojis.log, 'wooden log'])
                elif items_headers[header_index] == 'epiclog':
                    ingredients.append([value, emojis.logepic, 'EPIC log'])
                elif items_headers[header_index] == 'superlog':
                    ingredients.append([value, emojis.logsuper, 'SUPER log'])
                elif items_headers[header_index] == 'megalog':
                    ingredients.append([value, emojis.logmega, 'MEGA log'])
                elif items_headers[header_index] == 'hyperlog':
                    ingredients.append([value, emojis.loghyper, 'HYPER log'])
                elif items_headers[header_index] == 'ultralog':
                    ingredients.append([value, emojis.logultra, 'ULTRA log'])
                elif items_headers[header_index] == 'fish':
                    ingredients.append([value, emojis.fish, 'normie fish'])
                elif items_headers[header_index] == 'goldenfish':
                    ingredients.append([value, emojis.fishgolden, 'golden fish'])
                elif items_headers[header_index] == 'epicfish':
                    ingredients.append([value, emojis.fishepic, 'EPIC fish'])
                elif items_headers[header_index] == 'apple':
                    ingredients.append([value, emojis.apple, 'apple'])
                elif items_headers[header_index] == 'banana':
                    ingredients.append([value, emojis.banana, 'banana'])
                elif items_headers[header_index] == 'ruby':
                    ingredients.append([value, emojis.ruby, 'ruby'])
                elif items_headers[header_index] == 'wolfskin':
                    ingredients.append([value, emojis.wolfskin, 'wolf skin'])
                elif items_headers[header_index] == 'zombieeye':
                    ingredients.append([value, emojis.zombieeye, 'zombie eye'])
                elif items_headers[header_index] == 'unicornhorn':
                    ingredients.append([value, emojis.unicornhorn, 'unicorn horn'])
                elif items_headers[header_index] == 'mermaidhair':
                    ingredients.append([value, emojis.mermaidhair, 'mermaid hair'])
                elif items_headers[header_index] == 'chip':
                    ingredients.append([value, emojis.chip, 'chip'])
                elif items_headers[header_index] == 'dragonscale':
                    ingredients.append([value, emojis.dragonscale, 'dragon scale'])
                elif items_headers[header_index] == 'coin':
                    ingredients.append([value, emojis.coin, 'coin'])
                elif items_headers[header_index] == 'life':
                    ingredients.append([value, emojis.statlife, 'LIFE'])
                elif items_headers[header_index] == 'lifepotion':
                    ingredients.append([value, emojis.lifepotion, 'life potion'])
                elif items_headers[header_index] == 'cookies':
                    ingredients.append([value, emojis.arenacookie, 'arena cookie'])
                elif items_headers[header_index] == 'lbrare':
                    ingredients.append([value, emojis.lbrare, 'rare lootbox'])
                elif items_headers[header_index] == 'lbomega':
                    ingredients.append([value, emojis.lbomega, 'OMEGA lootbox'])
                elif items_headers[header_index] == 'armoredgy':
                    ingredients.append([value, emojis.armoredgy, 'EDGY Armor'])
                elif items_headers[header_index] == 'swordedgy':
                    ingredients.append([value, emojis.swordedgy, 'EDGY Sword'])
                elif items_headers[header_index] == 'armorultraedgy':
                    ingredients.append([value, emojis.armorultraedgy, 'ULTRA-EDGY Armor'])
                elif items_headers[header_index] == 'swordultraedgy':
                    ingredients.append([value, emojis.swordultraedgy, 'ULTRA-EDGY Sword'])
                elif items_headers[header_index] == 'armoromega':
                    ingredients.append([value, emojis.armoromega, 'OMEGA Armor'])
                elif items_headers[header_index] == 'swordomega':
                    ingredients.append([value, emojis.swordomega, 'OMEGA Sword'])
                elif items_headers[header_index] == 'armorultraomega':
                    ingredients.append([value, emojis.armoromega, 'ULTRA-OMEGA Armor'])
                elif items_headers[header_index] == 'swordultraomega':
                    ingredients.append([value, emojis.swordultraomega, 'ULTRA-OMEGA Sword'])
        
        if len(ingredients) == 1:
            ingredient = ingredients[0]
            if data_index == 0:
                submats = f'\n{amount:,} {item_emoji} `{item_name}`\n= {amount*ingredient[0]:,} {ingredient[1]} `{ingredient[2]}`'  # Initialisiere Aufschlüsselung der Materialien, falls benötigt.
                original_item_name = item_name # Speichere originalen Itemnamen, damit ich den für die erste Zeile am Schluss noch habe
                original_item_emoji = item_emoji # Speichere originales Emoji, damit ich das für die erste Zeile am Schluss noch habe
                if amount == 1:
                    mats = f'To craft {item_emoji} `{item_name}` you need {ingredient[0]} {ingredient[1]} `{ingredient[2]}`.'
                else:
                    mats = f'To craft {amount:,} {item_emoji} `{item_name}` you need {amount*ingredient[0]:,} {ingredient[1]} `{ingredient[2]}`.'
            else:
                ingredient_name = ingredient[2]
                if ingredient_name.find('log') != -1: # Falls das Item ein Log ist, berechne die Menge der Logs anhand des Index
                    subamount = (10**data_index) * amount
                    submats = f'{submats}\n= {ingredient[0]*subamount:,} {ingredient[1]} `{ingredient[2]}`'
                elif ingredient_name.find('fish') != -1: # Falls das Item ein Fisch ist, berechne die Menge der Logs anhand des Index
                    subamount = 100 * amount
                    submats = f'{submats}\n= {ingredient[0]*subamount:,} {ingredient[1]} `{ingredient[2]}`'
                    
                if data_index == (len(items_data)-2): # Falls es der letzte Durchlauf ist, stelle die finale Message zusammen (überschreibt die im allerersten Durchlauf erstellte, Items mit nur einem Record kommen gar nie hierhin)
                    if amount == 1:
                        mats = f'To craft {original_item_emoji} `{original_item_name}` you need {subamount*ingredient[0]:,} {ingredient[1]} `{ingredient[2]}`.\n{submats}'
                    else:
                        mats = f'To craft {amount:,} {original_item_emoji} `{original_item_name}` you need {subamount*ingredient[0]:,} {ingredient[1]} `{ingredient[2]}`.\n{submats}'         
        else:
            if amount == 1:
                mats = f'To craft {item_emoji} `{item_name}` you need:'
            else:
                mats = f'To craft {amount:,} {item_emoji} `{item_name}` you need:'
            for ingredient in ingredients:
                mats = f'{mats}\n{emojis.bp} {amount*ingredient[0]:,} {ingredient[1]} `{ingredient[2]}`'

    return mats

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

# Enchants
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