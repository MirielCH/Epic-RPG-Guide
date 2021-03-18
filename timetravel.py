# timetravel.py

import discord
import global_data
import emojis

# Time travel
async def timetravel(prefix):

    where = (
        f'{emojis.bp} {emojis.timetravel} TT 0: Beat dungeon 10, reach area 11\n'
        f'{emojis.bp} {emojis.timetravel} TT 1-2: Beat dungeon 11, reach area 12\n'
        f'{emojis.bp} {emojis.timetravel} TT 3-4: Beat dungeon 12, reach area 13\n'
        f'{emojis.bp} {emojis.timetravel} TT 5-9: Beat dungeon 13, reach area 14\n'
        f'{emojis.bp} {emojis.timetravel} TT 10-24: Beat dungeon 14, reach area 15\n'
        f'{emojis.bp} {emojis.timetravel} TT 25+: Beat dungeon 15-1 (see `{prefix}stt` for details)\n'
    )
    
    keptitems = (
        f'{emojis.bp} Coins (this includes your bank account)\n'
        f'{emojis.bp} Epic Coins\n'
        f'{emojis.bp} Items bought from the epic shop\n'
        f'{emojis.bp} Arena cookies \n'
        f'{emojis.bp} Dragon essences\n'
        f'{emojis.bp} Event items (if an event is active)\n'
        f'{emojis.bp} Your horse\n'
        f'{emojis.bp} Your pets\n'
        f'{emojis.bp} Your marriage partner\n'
        f'{emojis.bp} Your guild\n'
        f'{emojis.bp} Profession levels\n'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = f'TIME TRAVEL (TT)',
        description = (
            f'Resets your character to level 1 / area 1 but unlocks new game features and increases XP and drop chances.\nTo time travel, use `rpg time travel` while meeting the requirements.\n'
            f'Warning: **You will lose everything except the items mentioned below**. So make sure you have done all you want to do. You can check what you should do before time traveling by looking up the TT you are going to travel to (e.g. `{prefix}tt1` if you are about to travel to TT 1).'
        )
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))

    embed.add_field(name=f'REQUIREMENTS FOR TIME TRAVEL', value=where, inline=False)
    embed.add_field(name=f'WHAT YOU KEEP', value=keptitems, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}mytt` : Details about your current TT\n{emojis.bp} `{prefix}tt1`-`{prefix}tt999` : Details about specific TTs and how to prepare\n{emojis.bp} `{prefix}stt` : Details about super time travel', inline=False)
            
    return embed

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
    
    bonus_xp = f'{bonus_xp:,g}'
    bonus_duel_xp = f'{bonus_duel_xp:,g}'
    bonus_drop_chance = f'{bonus_drop_chance:,g}'

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
              f'{emojis.bp} **{bonus_drop_chance} %** extra chance to get **monster drops** (see `{prefix}dropchance`)\n'\
              f'{emojis.bp} **{bonus_drop_chance} %** more **items** with work commands\n'\
              f'{emojis.bp} Higher chance to get +1 tier in `horse breed` and `pet fusion` (chance unknown)'
                  

    prep_tt1_to_2 =     f'{emojis.bp} If your horse is T6+: Get 30m coins\n'\
                        f'{emojis.bp} If your horse is <T6: Get 50m coins\n'\
                        f'{emojis.bp} If you need money: Use `drill` and sell mob drops\n'\
                        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'\
                        f'{emojis.bp} Level up professions (see `{prefix}prlevel`)\n'\
                        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'\
                        f'{emojis.bp} Don\'t forget to sell your armor and sword!'
    
    prep_tt3_to_4 =     f'{emojis.bp} If your horse is T6+: Get 50m coins\n'\
                        f'{emojis.bp} If your horse is <T6: Get 150m coins\n'\
                        f'{emojis.bp} If you need money: Use `dynamite` and sell mob drops\n'\
                        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'\
                        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'\
                        f'{emojis.bp} Note: If you want to level enchanter, you need 2-3 billion coins\n'\
                        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'\
                        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'\
                        f'{emojis.bp} Don\'t forget to sell your armor and sword!'
    
    prep_tt5_to_9 =     f'{emojis.bp} If your horse is T6+: Get 150m coins\n'\
                        f'{emojis.bp} If your horse is <T6: Get 350m coins\n'\
                        f'{emojis.bp} If you need money: Use `dynamite` and sell mob drops\n'\
                        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'\
                        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'\
                        f'{emojis.bp} Note: If you want to level enchanter, you need 2-3 billion coins\n'\
                        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'\
                        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'\
                        f'{emojis.bp} Don\'t forget to sell your armor and sword!'
    
    prep_tt10_to_24 =   f'{emojis.bp} If your horse is T6+: Get 350m coins\n'\
                        f'{emojis.bp} If your horse is <T6: Get 850m coins\n'\
                        f'{emojis.bp} If you need money: Use `dynamite` and sell mob drops\n'\
                        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'\
                        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'\
                        f'{emojis.bp} Note: If you want to level enchanter, you need 2-3 billion coins\n'\
                        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'\
                        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'\
                        f'{emojis.bp} Don\'t forget to sell your armor and sword!'

    prep_tt25 =         f'{emojis.bp} If your horse is T6+: Get 350m coins\n'\
                        f'{emojis.bp} If your horse is <T6: Get 850m coins\n'\
                        f'{emojis.bp} Note: You **need** a T6+ horse to do Dungeon 15\n'\
                        f'{emojis.bp} If you need money: Use `dynamite` and sell mob drops\n'\
                        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'\
                        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'\
                        f'{emojis.bp} Note: If you want to level enchanter, you need 2-3 billion coins\n'\
                        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'\
                        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'\
                        f'{emojis.bp} Don\'t forget to sell your armor and sword!'
    
    prep_stt =          f'{emojis.bp} Get 850m coins\n'\
                        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'\
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

    embed.add_field(name=f'UNLOCKS & BONUSES', value=unlocks, inline=False)
    if not (mytt == True) and not (tt_no == 0):
        if 1 <= tt_no <= 2:
            embed.add_field(name=f'WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt1_to_2, inline=False)
        elif 3 <= tt_no <= 4:
            embed.add_field(name=f'WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt3_to_4, inline=False)
        elif 5 <= tt_no <= 9:
            embed.add_field(name=f'WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt5_to_9, inline=False)
        elif 10 <= tt_no <= 24:
            embed.add_field(name=f'WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt10_to_24, inline=False)
        elif tt_no == 25:
            embed.add_field(name=f'WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt25, inline=False)
        else:
            embed.add_field(name=f'WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_stt, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}tt` : Time travel overview\n{emojis.bp} `{prefix}stt` : Details about super time travel\n{emojis.bp} `{prefix}dropchance` : Mob drop chance calculator', inline=False)
            
    return embed

# Super time travel
async def supertimetravel(prefix):

    requirements =      f'{emojis.bp} {emojis.timetravel} TT 25+\n'\
                        f'{emojis.bp} {emojis.timekey} TIME key (drops from the boss in dungeon 15-1)'
    
    starter_bonuses =   f'{emojis.bp} Start with +25 LIFE (50 score)\n'\
                        f'{emojis.bp} Start with a new Tier I pet (300 score)\n'\
                        f'{emojis.bp} Start with +50 AT (400 score)\n'\
                        f'{emojis.bp} Start with +50 DEF (400 score)\n'\
                        f'{emojis.bp} Start with 10 of each monster drop (400 score)\n'\
                        f'{emojis.bp} Start with an OMEGA lootbox (500 score)\n'\
                        f'{emojis.bp} Start with a new Tier III pet (1,500 score)\n'\
                        f'{emojis.bp} Start with 10 ULTRA logs (1,750 score)\n'\
                        f'{emojis.bp} Start in area 2 (2,000 score)\n'\
                        f'{emojis.bp} Start with a new Tier I pet with 1 skill (4,500 score)\n'\
                        f'{emojis.bp} Start in area 3 (4,500 score)\n'\
                        f'{emojis.bp} Start with a GODLY lootbox (6,500 score)'
                        
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

    embed.add_field(name=f'REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name=f'STARTER BONUSES', value=starter_bonuses, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Super time travel score calculation
async def supertimetravelscore(prefix):

    gear =      f'{emojis.bp} {emojis.swordultraomega}{emojis.armorultraomega} ULTRA-OMEGA set = 155.5 score'
    
    level =     f'{emojis.bp} 1 level = 1 score'
    
    lootboxes = f'{emojis.bp} 1 {emojis.lbcommon} common lootbox = 1 score\n'\
                f'{emojis.bp} 1 {emojis.lbuncommon} uncommon lootbox = 2 score\n'\
                f'{emojis.bp} 1 {emojis.lbrare} rare lootbox = 3 score\n'\
                f'{emojis.bp} 1 {emojis.lbepic} EPIC lootbox = 4 score\n'\
                f'{emojis.bp} 1 {emojis.lbedgy} EDGY lootbox = 5 score\n'\
                f'{emojis.bp} 1 {emojis.lbomega} OMEGA lootbox = 50 score\n'\
                f'{emojis.bp} 1 {emojis.lbgodly} GODLY lootbox = 500 score'
                        
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
        description =   f'The score points for the starter bonuses of super time travel are calculated based on your level, inventory and your gear.'
                      
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))

    embed.add_field(name=f'LEVEL', value=level, inline=False)
    embed.add_field(name=f'GEAR', value=gear, inline=False)
    embed.add_field(name=f'LOOTBOXES', value=lootboxes, inline=False)
    embed.add_field(name=f'MATERIALS', value=materials, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed