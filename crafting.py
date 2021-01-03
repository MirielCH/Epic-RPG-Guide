# crafting.py

import discord
import global_data
import emojis
from operator import itemgetter


# Aufschlüsseln von Subamounts
async def get_submats(items_data, amount, ingredient, dismantle=False):
        
    item1 = ''
    item2 = ''
    item3 = ''
    item4 = ''
    item5 = ''
    breakdown = ''
    ingredient_name = ingredient[0]
    ingredient_emoji = ingredient[1]
    
    breakdown = f'> {amount:,} {ingredient_emoji}'                
    
    mats_ultralog = ['ULTRA log','HYPER log', 'MEGA log', 'SUPER log', 'EPIC log',]
    mats_hyperlog = ['HYPER log','MEGA log', 'SUPER log', 'EPIC log',]
    mats_megalog = ['MEGA log','SUPER log', 'EPIC log',]
    mats_superlog = ['SUPER log','EPIC log',]
    mats_epiclog = ['EPIC log',]
    mats_epicfish = ['EPIC fish','golden fish',]
    mats_goldenfish = ['golden fish',]
    mats_banana = ['banana',]
    mats_all = [mats_ultralog, mats_hyperlog, mats_megalog, mats_superlog, mats_epiclog, mats_epicfish, mats_goldenfish, mats_banana,]
    
    items_subitems = {
        'ULTRA log': 'HYPER log',
        'HYPER log': 'MEGA log',
        'MEGA log': 'SUPER log',
        'SUPER log': 'EPIC log',
        'EPIC log': 'wooden log',
        'EPIC fish': 'golden fish',
        'golden fish': 'normie fish',
        'banana': 'apple'
    }
    
    subitems_emojis = {
        'HYPER log': emojis.loghyper,
        'MEGA log': emojis.logmega,
        'SUPER log': emojis.logsuper,
        'EPIC log': emojis.logepic,
        'wooden log': emojis.log,
        'golden fish': emojis.fishgolden,
        'normie fish': emojis.fish,
        'apple': emojis.apple
    }
    
    last_item_amount = 0
    
    for mats_item in mats_all:
        if ingredient_name == mats_item[0]:
            last_item_amount = amount
            for data_index, item in enumerate(items_data[1:]):
                item_name = item[2]
                if item_name in mats_item:
                    subitem_name = items_subitems[item_name]
                    subitem_emoji = subitems_emojis[subitem_name]
                    item_filtered = list(dict.fromkeys(item))
                    item_filtered = list(filter(lambda num: num != 0, item_filtered))
                    item_amount = item_filtered[4]
                    if dismantle == True:
                        subitem_amount = item_amount*last_item_amount*0.8
                        try:
                            subitem_amount = int(subitem_amount)
                        except:
                            pass
                    else:
                        subitem_amount = item_amount*last_item_amount
                    last_item_amount = subitem_amount
                    breakdown = f'{breakdown} ➜ {subitem_amount:,} {subitem_emoji}'
    
    return (breakdown, last_item_amount)
            

# List needed items for recipe
async def mats(items_data, amount, prefix):
    
    items_headers = items_data[0]
    
    item_crafted = items_data[1]
    item_crafted_name = item_crafted[2]
    item_crafted_emoji = getattr(emojis, item_crafted[3])
    
    ingredients = []

    for item_index, value in enumerate(item_crafted[6:]):
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
                ingredients.append([value, emojis.fruitbanana, 'banana'])
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
        
    breakdown_logs = ''
    breakdown_fish = ''
    breakdown_banana = ''
    
    breakdown_list_logs = ['EPIC log', 'SUPER log', 'MEGA log', 'HYPER log', 'ULTRA log', ]
    breakdown_list_fish = ['EPIC fish', 'golden fish',]
    
    ingredient_submats_logs = ['',0]
    ingredient_submats_fish = ['',0]
    ingredient_submats_banana = ['',0]
    ingredient_submats = ''
    mats = ''
    total_logs = 0
    total_fish = 0
    total_apple = 0
    mats_total_logs = ''
    mats_total_fish = ''
    mats_total_apple = ''
    
    if (len(ingredients) == 1) or (item_crafted_name in breakdown_list_logs) or (item_crafted_name in breakdown_list_fish) or (item_crafted_name == 'banana'):
        ingredient = ingredients[0]
        ingredient_amount = ingredient[0]*amount
        ingredient_emoji = ingredient[1]
        ingredient_name = ingredient[2]
        
        if ingredient_name == 'wooden log':
            total_logs = total_logs+ingredient_amount
        elif ingredient_name == 'normie fish':
            total_fish = total_fish+ingredient_amount
        elif ingredient_name == 'apple':
            total_apple = total_apple+ingredient_amount
        
        if ingredient_name in breakdown_list_logs:
            ingredient_submats_logs = await get_submats(items_data, ingredient_amount, (ingredient_name, ingredient_emoji,))
            total_logs = total_logs+ingredient_submats_logs[1]
        elif ingredient_name in breakdown_list_fish:
            ingredient_submats_fish = await get_submats(items_data, ingredient_amount, (ingredient_name, ingredient_emoji,))
            total_fish = total_fish+ingredient_submats_fish[1]
        elif ingredient_name == 'banana':
            ingredient_submats_banana = await get_submats(items_data, ingredient_amount, (ingredient_name, ingredient_emoji,))
            total_apple = total_apple+ingredient_submats_banana[1]
        
        ingredient_submats = f'{ingredient_submats_logs[0]}{ingredient_submats_fish[0]}{ingredient_submats_banana[0]}'
        
        if amount == 1:
            mats = f'To craft {item_crafted_emoji} `{item_crafted_name}` you need {ingredient_amount:,} {ingredient_emoji} `{ingredient_name}`.'
        else:
            mats = f'To craft {amount:,} {item_crafted_emoji} `{item_crafted_name}` you need {ingredient_amount:,} {ingredient_emoji} `{ingredient_name}`.'
            
    else:
        if amount == 1:
            mats = f'To craft {item_crafted_emoji} `{item_crafted_name}` you need:'
        else:
            mats = f'To craft {amount:,} {item_crafted_emoji} `{item_crafted_name}` you need:'
        
        for ingredient in ingredients:
            ingredient_amount = ingredient[0]*amount
            ingredient_emoji = ingredient[1]
            ingredient_name = ingredient[2]
            
            if ingredient_name == 'wooden log':
                total_logs = total_logs+ingredient_amount
            elif ingredient_name == 'normie fish':
                total_fish = total_fish+ingredient_amount
            elif ingredient_name == 'apple':
                total_apple = total_apple+ingredient_amount
            
            mats = f'{mats}\n> {ingredient_amount} {ingredient_emoji} `{ingredient_name}`'
    
            if ingredient_name in breakdown_list_logs:
                ingredient_submats_logs = await get_submats(items_data, ingredient_amount, (ingredient_name, ingredient_emoji,))
                total_logs = total_logs+ingredient_submats_logs[1]
                ingredient_submats = f'{ingredient_submats}\n  {ingredient_submats_logs[0]}'
            elif ingredient_name in breakdown_list_fish:
                ingredient_submats_fish = await get_submats(items_data, ingredient_amount, (ingredient_name, ingredient_emoji,))
                total_fish = total_fish+ingredient_submats_fish[1]
                ingredient_submats = f'{ingredient_submats}\n  {ingredient_submats_fish[0]}'
            elif ingredient_name == 'banana':
                ingredient_submats_banana = await get_submats(items_data, ingredient_amount, (ingredient_name, ingredient_emoji,))
                total_apple = total_apple+ingredient_submats_banana[1]
                ingredient_submats = f'{ingredient_submats}\n  {ingredient_submats_banana[0]}'
        
    if not total_logs == 0:    
        mats_total_logs = f'\n> {total_logs:,} {emojis.log} `wooden log`'
    if not total_fish == 0:    
        mats_total_fish = f'\n> {total_fish:,} {emojis.fish} `normie fish`'    
    if not total_apple == 0:    
        mats_total_apple = f'\n> {total_apple:,} {emojis.apple} `apple`'
    
    if not ingredient_submats == '':
        ingredient_submats = ingredient_submats.strip()
        mats = f'{mats}\n\n**Ingredients breakdown**\n{ingredient_submats}'
    
    if not (total_logs == 0) or not (total_fish == 0) or not (total_apple == 0):
        mats = f'{mats}\n\n**Base materials total**{mats_total_logs}{mats_total_fish}{mats_total_apple}'

    return mats

# Dismantle items
async def dismantle(items_data, amount, prefix):
    
    items_headers = items_data[0]
    
    item_crafted = items_data[1]
    item_crafted_name = item_crafted[2]
    item_crafted_emoji = getattr(emojis, item_crafted[3])
    
    ingredients = []

    for item_index, value in enumerate(item_crafted[6:]):
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
            elif items_headers[header_index] == 'fish':
                ingredients.append([value, emojis.fish, 'normie fish'])
            elif items_headers[header_index] == 'goldenfish':
                ingredients.append([value, emojis.fishgolden, 'golden fish'])
            elif items_headers[header_index] == 'apple':
                ingredients.append([value, emojis.apple, 'apple'])
        
    breakdown_logs = ''
    breakdown_fish = ''
    breakdown_banana = ''
    
    breakdown_list_logs = ['EPIC log', 'SUPER log', 'MEGA log', 'HYPER log', 'ULTRA log', ]
    breakdown_list_fish = ['EPIC fish', 'golden fish',]
    
    ingredient_submats_logs = ['',0]
    ingredient_submats_fish = ['',0]
    ingredient_submats_banana = ['',0]
    ingredient_submats = ''
    mats = ''
    total_logs = 0
    total_fish = 0
    total_apple = 0
    mats_total_logs = ''
    mats_total_fish = ''
    mats_total_apple = ''
    
    if (len(ingredients) == 1) or (item_crafted_name in breakdown_list_logs) or (item_crafted_name in breakdown_list_fish) or (item_crafted_name == 'banana'):
        ingredient = ingredients[0]
        ingredient_amount = ingredient[0]*amount*0.8
        try:
            ingredient_amount = int(ingredient_amount)
        except:
            pass
        ingredient_emoji = ingredient[1]
        ingredient_name = ingredient[2]
        
        if ingredient_name in breakdown_list_logs:
            ingredient_submats_logs = await get_submats(items_data, ingredient_amount, (ingredient_name, ingredient_emoji,), True)
            total_logs = total_logs+ingredient_submats_logs[1]
        elif ingredient_name in breakdown_list_fish:
            ingredient_submats_fish = await get_submats(items_data, ingredient_amount, (ingredient_name, ingredient_emoji,), True)
            total_fish = total_fish+ingredient_submats_fish[1]
        elif ingredient_name == 'banana':
            ingredient_submats_banana = await get_submats(items_data, ingredient_amount, (ingredient_name, ingredient_emoji,), True)
            total_apple = total_apple+ingredient_submats_banana[1]
        
        ingredient_submats = f'{ingredient_submats_logs[0]}{ingredient_submats_fish[0]}{ingredient_submats_banana[0]}'
        
        if amount == 1:
            mats = f'By dismantling {item_crafted_emoji} `{item_crafted_name}` you get {ingredient_amount:,} {ingredient_emoji} `{ingredient_name}`.'
        else:
            mats = f'By dismantling {amount:,} {item_crafted_emoji} `{item_crafted_name}` you get {ingredient_amount:,} {ingredient_emoji} `{ingredient_name}`.'
        
    if not total_logs == 0:    
        mats_total_logs = f'\n> {total_logs:,} {emojis.log} `wooden log`'
    if not total_fish == 0:    
        mats_total_fish = f'\n> {total_fish:,} {emojis.fish} `normie fish`'    
    if not total_apple == 0:    
        mats_total_apple = f'\n> {total_apple:,} {emojis.apple} `apple`'
    
    if not ingredient_submats == '':
        ingredient_submats = ingredient_submats.strip()
        mats = f'{mats}\n\n**Full breakdown**\n{ingredient_submats}'

    return mats

# Monster drops
async def drops(prefix):

    items =     f'Area: 1~2\nSource: {emojis.mobwolf}\nValue: 5\'000\n'\
                f'{emojis.bp} {emojis.zombieeye} **Zombie Eye** - {emojis.mobzombie} Zombie in areas **3~4**\n'\
                f'{emojis.bp} {emojis.unicornhorn} **Unicorn Horn** - {emojis.mobunicorn} Unicorn in areas **5~6**\n'\
                f'{emojis.bp} {emojis.mermaidhair} **Mermaid Hair** - {emojis.mobmermaid} Mermaid in areas **7~8**\n'\
                f'{emojis.bp} {emojis.chip} **Chip** - {emojis.mobkillerrobot} Killer Robot in areas **9~10**\n'\
                f'{emojis.bp} Area: 11~14\n{emojis.bp} Source: {emojis.mobbabydragon}{emojis.mobteendragon}{emojis.mobadultdragon}\n{emojis.bp} Value: 250\'000 coins'

    chance =    f'{emojis.bp} The chance to encounter a mob that drops items is 50 %\n'\
                f'{emojis.bp} These mobs have a base chance of 4 % to drop an item\n'\
                f'{emojis.bp} Thus you have a total base drop chance of 2 % when hunting\n'\
                f'{emojis.bp} Every {emojis.timetravel} time travel increases the drop chance by ~25%\n'\
                f'{emojis.bp} A {emojis.horset7} T7 horse increases the drop chance by 20%\n'\
                f'{emojis.bp} A {emojis.horset8} T8 horse increases the drop chance by 50%\n'\
                f'{emojis.bp} A {emojis.horset9} T9 horse increases the drop chance by 100%\n'\
                f'{emojis.bp} To calculate your current drop chance, use `{prefix}dropchance`\n{emojis.blank}'

    embed = discord.Embed(
        color = global_data.color,
        title = f'MONSTER DROPS',
        description =   f'These items drop when using `hunt`, `hunt together` or when opening lootboxes.\n'\
                        f'You can go back to previous areas with `rpg area`.\n{emojis.blank}'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))

    embed.add_field(name=f'WOLF SKIN {emojis.wolfskin}', value=f'{emojis.bp} Areas: 1~2\n{emojis.bp} Source: {emojis.mobwolf}\n{emojis.bp} Value: 500\n{emojis.blank}', inline=True)
    embed.add_field(name=f'ZOMBIE EYE {emojis.zombieeye}', value=f'{emojis.bp} Areas: 3~4\n{emojis.bp} Source: {emojis.mobzombie}\n{emojis.bp} Value: 2\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'UNICORN HORN {emojis.unicornhorn}', value=f'{emojis.bp} Areas: 5~6\n{emojis.bp} Source: {emojis.mobunicorn}\n{emojis.bp} Value: 7\'500\n{emojis.blank}', inline=True)
    embed.add_field(name=f'MERMAID HAIR {emojis.mermaidhair}', value=f'{emojis.bp} Areas: 7~8\n{emojis.bp} Source: {emojis.mobmermaid}\n{emojis.bp} Value: 30\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'CHIP {emojis.chip}', value=f'{emojis.bp} Areas: 9~10\n{emojis.bp} Source: {emojis.mobkillerrobot}\n{emojis.bp} Value: 100\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'DRAGON SCALE {emojis.dragonscale}', value=f'{emojis.bp} Areas: 11~14\n{emojis.bp} Source: {emojis.mobbabydragon}{emojis.mobteendragon}{emojis.mobadultdragon}\n{emojis.bp} Value: 250\'000\n{emojis.blank}', inline=True)
    embed.add_field(name=f'DROP CHANCE', value=chance, inline=False)    
            
    return embed

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
    
    embed.add_field(name=f'POSSIBLE ENCHANTS', value=buffs, inline=False)
    embed.add_field(name=f'COMMAND TIERS', value=commands, inline=False)
            
    return embed