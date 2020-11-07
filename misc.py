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