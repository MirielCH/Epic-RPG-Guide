# timetravel.py

import discord
import global_data
import emojis

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
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}mytt` : Details about your current TT\n{emojis.bp} `{prefix}tt1`-`{prefix}tt999` : Details about specific TTs and how to prepare\n{emojis.bp} `{prefix}stt` : Details about super time travel', inline=False)
            
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
              f'{emojis.bp} **{bonus_duel_xp} %** increased **XP** from **duels**\n'\
              f'{emojis.bp} **{bonus_drop_chance} %** extra chance to get **monster drops**\n'\
              f'{emojis.bp} **{bonus_drop_chance} %** more **items** with work commands'
                  

    prep_tt1 =          f'{emojis.bp} If your horse is T6+: get 30m coins\n'\
                        f'{emojis.bp} If your horse is <T6: get 50m coins\n'\
                        f'{emojis.bp} If you need money: Use `drill` and sell mob drops\n'\
                        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'\
                        f'{emojis.bp} Level up professions (see `{prefix}prlevel`)\n'\
                        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'\
                        f'{emojis.bp} Don\'t forget to sell your armor and sword!'
    
    prep_tt2_to_25 =    f'{emojis.bp} If your horse is T6+: get 30m coins\n'\
                        f'{emojis.bp} If your horse is <T6: get 50m coins\n'\
                        f'{emojis.bp} If you need money: Use `dynamite` and sell mob drops\n'\
                        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'\
                        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'\
                        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'\
                        f'{emojis.bp} Don\'t forget to sell your armor and sword!'
                   
    prep_stt =          f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'\
                        f'{emojis.bp} If you need a higher score: Trade to {emojis.ruby} rubies (see `{prefix}sttscore`)\n'\
                        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'\
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
    if not (mytt == True) and not (tt_no == 0):
        if tt_no == 1:
            embed.add_field(name=f'WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt1, inline=False)
        elif 2 <= tt_no <= 25:
            embed.add_field(name=f'WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt2_to_25, inline=False)
        else:
            embed.add_field(name=f'WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_stt, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}tt` : Time travel overview\n{emojis.bp} `{prefix}stt` : Details about super time travel', inline=False)
            
    return (thumbnail, embed)

# Super time travel
async def supertimetravel(prefix):

    requirements =      f'{emojis.bp} {emojis.timetravel} TT 25+\n'\
                        f'{emojis.bp} {emojis.timekey} TIME key (drops from the boss in dungeon 15)'
    
    starter_bonuses =   f'{emojis.bp} {emojis.statlife} Start with +25 LIFE (50 score)\n'\
                        f'{emojis.bp} {emojis.statat} Start with +50 AT (400 score)\n'\
                        f'{emojis.bp} {emojis.statdef} Start with +50 DEF (400 score)\n'\
                        f'{emojis.bp} {emojis.wolfskin} Start with 10 of each monster drop (400 score)\n'\
                        f'{emojis.bp} :two: Start in area 2 (750 score)\n'\
                        f'{emojis.bp} {emojis.lbomega} Start with an OMEGA lootbox (800 score)\n'\
                        f'{emojis.bp} :three: Start in area 3 (1500 score)\n'\
                        f'{emojis.bp} {emojis.logultra} Start with 10 ULTRA logs (2250 score)\n'\
                        f'{emojis.bp} {emojis.lbgodly} Start with a GODLY lootbox (6500 score)'
                        
    guides =            f'{emojis.bp} `{prefix}tt` : Time travel overview\n'\
                        f'{emojis.bp} `{prefix}mytt` : Details about your current TT\n'\
                        f'{emojis.bp} `{prefix}tt1`-`{prefix}tt999` : Details about specific TTs and how to prepare'

    embed = discord.Embed(
        color = global_data.color,
        title = f'SUPER TIME TRAVEL',
        description =   f'Super time travel is unlocked once you reach {emojis.timetravel} TT 25. From this point onward you have to use `super time travel` to reach the next TT.\n'\
                        f'Super time travel lets you choose a starter bonus. You can (and have to) choose **1** bonus.\n'\
                        f'These bonuses cost score points which are calculated based on your inventory and your gear (see `{prefix}sttscore`).'
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name=f'STARTER BONUSES', value=starter_bonuses, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=guides, inline=False)
            
    return (thumbnail, embed)

# Super time travel score calculation
async def supertimetravelscore(prefix):

    gear =      f'{emojis.bp} {emojis.swordultraomega}{emojis.armorultraomega} ULTRA-OMEGA set = 355.5 score'
    
    lootboxes = f'{emojis.bp} 1 {emojis.lbcommon} common lootbox = 10 score\n'\
                f'{emojis.bp} 1 {emojis.lbuncommon} uncommon lootbox = 20 score\n'\
                f'{emojis.bp} 1 {emojis.lbrare} rare lootbox = 30 score\n'\
                f'{emojis.bp} 1 {emojis.lbepic} EPIC lootbox = 40 score\n'\
                f'{emojis.bp} 1 {emojis.lbedgy} EDGY lootbox = 50 score\n'\
                f'{emojis.bp} 1 {emojis.lbomega} OMEGA lootbox = 60 score\n'\
                f'{emojis.bp} 1 {emojis.lbgodly} GODLY lootbox = 60 score'
                        
    materials = f'{emojis.bp} 25 {emojis.ruby} rubies = 1 score\n'\
                f'{emojis.bp} 20 {emojis.wolfskin} wolf skins = 1 score\n'\
                f'{emojis.bp} 9 {emojis.zombieeye} zombie eyes = 1 score\n'\
                f'{emojis.bp} 7 {emojis.unicornhorn} unicorn horns = 1 score\n'\
                f'{emojis.bp} 5 {emojis.mermaidhair} mermaid hairs = 1 score\n'\
                f'{emojis.bp} 4 {emojis.chip} chips = 1 score\n'\
                f'{emojis.bp} 2 {emojis.dragonscale} dragon scales = 1 score\n'\
                        
                        
    guides =    f'{emojis.bp} `{prefix}tt` : Time travel overview\n'\
                f'{emojis.bp} `{prefix}mytt` : Details about your current TT\n'\
                f'{emojis.bp} `{prefix}tt1`-`{prefix}tt999` : Details about specific TTs and how to prepare\n'\
                f'{emojis.bp} `{prefix}stt` : Super time travel'

    embed = discord.Embed(
        color = global_data.color,
        title = f'SUPER TIME TRAVEL SCORE CALCULATION',
        description =   f'The score points for the starter bonuses of super time travel are calculated based on your inventory and your gear.'
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'GEAR', value=gear, inline=False)
    embed.add_field(name=f'LOOTBOXES', value=lootboxes, inline=False)
    embed.add_field(name=f'MATERIALS', value=materials, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=guides, inline=False)
            
    return (thumbnail, embed)