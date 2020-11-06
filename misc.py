# misc.py

import discord
import global_data
import emojis

# Monster drops
async def drops(prefix):

    items = f'Area: 1~2\nSource: {emojis.mobwolf}\nValue: 5\'000\n'\
            f'{emojis.bp} {emojis.zombieeye} **Zombie Eye** - {emojis.mobzombie} Zombie in areas **3~4**\n'\
            f'{emojis.bp} {emojis.unicornhorn} **Unicorn Horn** - {emojis.mobunicorn} Unicorn in areas **5~6**\n'\
            f'{emojis.bp} {emojis.mermaidhair} **Mermaid Hair** - {emojis.mobmermaid} Mermaid in areas **7~8**\n'\
            f'{emojis.bp} {emojis.chip} **Chip** - {emojis.mobkillerrobot} Killer Robot in areas **9~10**\n'\
            f'{emojis.bp} Area: 11~14\n{emojis.bp} Source: {emojis.mobbabydragon}{emojis.mobteendragon}{emojis.mobadultdragon}\n{emojis.bp} Value: 250\'000 coins'

    embed = discord.Embed(
        color = global_data.color,
        title = f'MONSTER DROPS',
        description = f'These items drop when using `hunt`, `hunt together` or when opening lootboxes.\n{emojis.blank}'
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
    embed.add_field(name=f'DROP CHANCE', value=f'{emojis.bp} All items have a 2% base drop chance\n{emojis.bp} The drop chance increases by ~25% every time you time travel\n{emojis.blank}', inline=False)    
            
    return (thumbnail, embed)

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

# Time travel
async def timetravel(prefix):

    keptitems = f'{emojis.bp} Coins (this includes your bank account)\n'\
                f'{emojis.bp} Epic Coins\n'\
                f'{emojis.bp} Items bought from the epic shop\n'\
                f'{emojis.bp} Arena cookies \n'\
                f'{emojis.bp} Event items (if an event is active)\n'\
                f'{emojis.bp} Lottery tickets\n'\
                f'{emojis.bp} Your horse\n'\
                f'{emojis.bp} Your pets\n'\
                f'{emojis.bp} Your marriage partner\n'\
                f'{emojis.bp} Your guild\n'\
                f'{emojis.bp} Profession levels\n'

    embed = discord.Embed(
        color = global_data.color,
        title = f'TIME TRAVEL',
        description = f'Resets your character to level 1 / area 1 but unlocks new game features and increases XP and drop chances.\n'\
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'WHAT YOU KEEP', value=keptitems, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}mytt` : Details about your next TT and how to prepare\n{emojis.bp} `{prefix}tt[1-999]` : Details about specific TTs and how to prepare\n{emojis.bp} `{prefix}stt` : Details about super time travel', inline=False)
            
    return (thumbnail, embed)

# Time travel X
async def timetravel_specific(tt_data, prefix, mytt=False):

    tt_no = int(tt_data[0])
    unlock_dungeon = int(tt_data[1])
    unlock_area = int(tt_data[2])
    unlock_enchant = tt_data[3]
    unlock_title = tt_data[4]
    unlock_misc = tt_data[5]
    
    bonus_xp = (99+tt_no)*tt_no/2
    bonus_duel_xp = (99+tt_no)*tt_no/4
    bonus_drop_chance = (49+tt_no)*tt_no/2
    
    bonus_xp = f'{bonus_xp:,}'.replace(',','\'').replace('.0','')
    bonus_duel_xp = f'{bonus_duel_xp:,}'.replace(',','\'').replace('.0','')
    bonus_drop_chance = f'{bonus_drop_chance:,}'.replace(',','\'').replace('.0','')

    if mytt == True:
        embed_description = f'This is your current TT according to your settings.\n If this is wrong, run `{prefix}setprogress`.'
    else:
        embed_description = f'Allons-y !'

    unlocks = ''
    
    if not unlock_misc == '':
        unlocks = f'{emojis.bp} Unlocks **{unlock_misc}**\n'
    
    if not unlock_dungeon == 0:
        unlocks = f'{unlocks}{emojis.bp} Unlocks **dungeon {unlock_dungeon}**\n'
    
    if not unlock_area == 0:
        unlocks = f'{unlocks}{emojis.bp} Unlocks **area {unlock_area}**\n'
    
    if not unlock_enchant == '':
        unlocks = f'{unlocks}{emojis.bp} Unlocks the **{unlock_enchant}** enchant\n'
        
    if not unlock_title == '':
        unlocks = f'{unlocks}{emojis.bp} Unlocks the title **{unlock_title}**\n'
        
    unlocks = f"{unlocks}{emojis.bp} **{bonus_xp} %** increased **XP** from everything except duels\n"\
              f'{emojis.bp} **{bonus_duel_xp} %** increased XP from **duels**\n'\
              f'{emojis.bp} **{bonus_drop_chance} %** extra chance to get **monster drops**\n'\
              f'{emojis.bp} **{bonus_drop_chance} %** more **items** with work commands'
                  

    preparations = f'{emojis.bp} If your horse is T6+: Have 30m coins\n'\
                   f'{emojis.bp} If your horse is <T6: Have 50m coins\n'\
                   f'{emojis.bp} Level up professions if necessary (see `{prefix}prlevel`)\n'\
                   f'{emojis.bp} Sell your leftover materials (if any)\n'\
                   f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'\
                   f'{emojis.bp} Don\'t forget to sell your armor and sword!'

    embed = discord.Embed(
        color = global_data.color,
        title = f'TIME TRAVEL {tt_no}',
        description = embed_description
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'UNLOCKS & BONUSES', value=unlocks, inline=False)
    embed.add_field(name=f'WHAT TO DO BEFORE YOU TIME TRAVEL', value=preparations, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}tt` : Time travel overview\n{emojis.bp} `{prefix}stt` : Details about super time travel', inline=False)
            
    return (thumbnail, embed)

# Super time travel
async def supertimetravel(prefix):

    starter_bonuses =   f'{emojis.bp} {emojis.statlife} Start with +25 LIFE (50 score)\n'\
                        f'{emojis.bp} {emojis.statat} Start with +50 AT (400 score)\n'\
                        f'{emojis.bp} {emojis.statdef} Start with +50 DEF (400 score)\n'\
                        f'{emojis.bp} {emojis.wolfskin} Start with 10 of each monster drop (400 score)\n'\
                        f'{emojis.bp} :two: Start in area 2 (750 score)\n'\
                        f'{emojis.bp} {emojis.lbomega} Start with an OMEGA lootbox (800 score)\n'\
                        f'{emojis.bp} :three: Start in area 3 (1500 score)\n'\
                        f'{emojis.bp} {emojis.logultra} Start with 10 ULTRA logs (2250 score)\n'\
                        f'{emojis.bp} {emojis.lbgodly} Start with a GODLY lootbox (6500 score)'

    requirements =  f'{emojis.bp} {emojis.timetravel} TT 25+\n'\
                    f'{emojis.bp} {emojis.timekey} TIME key (drops from the boss in dungeon 15)\n'\

    embed = discord.Embed(
        color = global_data.color,
        title = f'SUPER TIME TRAVEL',
        description =   f'Super time travel is unlocked once you reach {emojis.timetravel} TT 25. From this point onward have to use `super time travel` to reach the next TT.\n'\
                        f'Super time travel lets you choose a starter bonus. You can (and have to) choose **1** bonus.\n'\
                        f'These bonuses cost score points which are calculated based on your leftover materials and your level.'
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'STARTER BONUSES', value=starter_bonuses, inline=False)
    embed.add_field(name=f'REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}tt` : Time travel overview\n{emojis.bp} `{prefix}mytt` : Details about your next TT and how to prepare\n{emojis.bp} `{prefix}tt[1-999]` : Details about specific TTs and how to prepare', inline=False)
            
    return (thumbnail, embed)