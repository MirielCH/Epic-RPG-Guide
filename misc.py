# misc.py

import discord
import global_data
import emojis

# Duels
async def duels(prefix):

    weapons = f'{emojis.bp} {emojis.duelat}{emojis.duelat} - **AT**\n'\
              f'{emojis.bp} {emojis.dueldef}{emojis.dueldef} - **DEF**\n'\
              f'{emojis.bp} {emojis.duellife}{emojis.duellife} - **LIFE**\n'\
              f'{emojis.bp} {emojis.duellevel}{emojis.duellevel} - **LEVEL**\n'\
              f'{emojis.bp} {emojis.duelcoins}{emojis.duelcoins} - **Coins** (incl. bank account)\n'\
              f'{emojis.bp} {emojis.duelgear}{emojis.duelgear} - **Gear** (both sword and armor)\n'\
              f'{emojis.bp} {emojis.duelenchants}{emojis.duelenchants} - **Enchants** (both sword and armor)'

    embed = discord.Embed(
        color = global_data.color,
        title = f'DUELS',
        description = f'Winning a duel depends on the chosen weapon and some luck.'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'DUELLING WEAPONS', value=weapons, inline=False)
    embed.add_field(name=f'TIP', value=f'{emojis.bp} Unless you are __very__ rich, don\'t choose coins.', inline=False)
            
    return (thumbnail, embed)

# Redeemable codes
async def codes(prefix):

    all_codes = f'{emojis.bp} `code` {emojis.blank} 20 {emojis.log}, 10 {emojis.fish}, 5\'000 {emojis.coin}\n'\
                f'{emojis.bp} `epic` {emojis.blank} 1 {emojis.epiccoin}\n'\
                f'{emojis.bp} `epicrpg` 10 {emojis.arenacookie}, 15\'000 {emojis.coin}\n'\
                f'{emojis.bp} `lmao` {emojis.blank} 2 {emojis.logepic}, 50\'000 {emojis.coin}'

    embed = discord.Embed(
        color = global_data.color,
        title = f'REDEEMABLE CODES',
        description =   f'Use these codes with `rpg code` to get some free goodies.\n'\
                        f'Every code can only be redeemed once.'
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'CODES', value=all_codes, inline=False)
            
    return (thumbnail, embed)

# Coolness
async def coolness(prefix):

    usage =     f'{emojis.bp} Unlocks cosmetic only profile badges (see `{prefix}badges`)\n'\
                f'{emojis.bp} An unknown amount will be required for part 2 of D15'
                
    req =       f'{emojis.bp} Unlocks when you reach area 12 in {emojis.timetravel}TT 1'
                
    howtoget =  f'{emojis.bp} `ultraining` awards 2 coolness per stage (unlocked in A12)\n'\
                f'{emojis.bp} Survive adventures with 1 HP\n'\
                f'{emojis.bp} Open {emojis.lbomega} OMEGA and {emojis.lbgodly} GODLY lootboxes\n'\
                f'{emojis.bp} Get {emojis.loghyper} HYPER or {emojis.logultra} ULTRA logs from work commands\n'\
                f'{emojis.bp} Forge ULTRA-EDGY or higher gear\n'\
                f'{emojis.bp} Do other \'cool\' actions that are currently unknown'
                
    note =      f'{emojis.bp} You don\'t lose coolness when you time travel\n'\
                f'{emojis.bp} You can get coolness in every area once it\'s unlocked\n'\
                f'{emojis.bp} If you have 100+, you get less (except from `ultraining`)\n'\
                f'{emojis.bp} You can only see your coolness by doing `ultraining`\n'\

    embed = discord.Embed(
        color = global_data.color,
        title = f'COOLNESS',
        description =   f'Coolness is a stat you start collecting after you reach area 12.\n'\
                        f'It has currently no use (yet) apart from cosmetic profile badges.'
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'USAGE', value=usage, inline=False)
    embed.add_field(name=f'REQUIREMENTS', value=req, inline=False)
    embed.add_field(name=f'HOW TO GET COOLNESS', value=howtoget, inline=False)
    embed.add_field(name=f'NOTE', value=note, inline=False)
            
    return (thumbnail, embed)

# Badges
async def badges(prefix):

    badges =    f'{emojis.bp} {emojis.badge1} : Unlocked with 1 coolness\n'\
                f'{emojis.bp} {emojis.badge100} : Unlocked with 100 coolness\n'\
                f'{emojis.bp} {emojis.badge200} : Unlocked with 200 coolness\n'\
                f'{emojis.bp} {emojis.badge500} : Unlocked with 500 coolness\n'\
                f'{emojis.bp} {emojis.badge1000} : Unlocked with 1000 coolness\n'\
                f'{emojis.bp} {emojis.badgea15} : Unlocked by reaching area 15 ({emojis.timetravel}TT 10)\n'\
                f'{emojis.bp} {emojis.badgeomega} : Currently unknown and unavailable'
                
    howtouse =  f'{emojis.bp} Use `rpg badge list` to get the ID of the badges you want\n'\
                f'{emojis.bp} Use `rpg badge claim [ID]` to claim a badge\n'\
                f'{emojis.bp} Use `rpg badge [ID]` to activate or deactivate a badge'
                
    note =      f'{emojis.bp} You can have several badges active at the same time\n'\
                f'{emojis.bp} You can only claim badges you have unlocked\n'\
                f'{emojis.bp} If you don\'t know how to get coolness, see `{prefix}coolness`'

    embed = discord.Embed(
        color = global_data.color,
        title = f'BADGES',
        description =   f'Badges are cosmetic only profile decorations.'
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'AVAILABLE BADGES', value=badges, inline=False)
    embed.add_field(name=f'HOW TO USE', value=howtouse, inline=False)
    embed.add_field(name=f'NOTE', value=note, inline=False)
            
    return (thumbnail, embed)