# professions.py

import discord
import global_data
import emojis

# Professions overview
async def professions_overview(prefix):
    
    worker =    f'{emojis.bp} Increases the chance to get a better item with work commands\n'\
                f'{emojis.bp} Chance increases up to 50 % at level 100'
                
    crafter =   f'{emojis.bp} Increases the chance to get 10% materials back when crafting\n'\
                f'{emojis.bp} Chance increases up to 90 % at level 100'
                
    lootboxer = f'{emojis.bp} Increases the bank XP bonus\n'\
                f'{emojis.bp} Decreases the cost of horse training\n'\
                f'{emojis.bp} Horse training gets up to 50 % cheaper at level 100\n'\
                f'{emojis.bp} Exact buff of bank bonus unknown'
                
    merchant =  f'{emojis.bp} Increases the amount of coins you get when selling items\n'\
                f'{emojis.bp} You get up to 4.929395x more coins at level 100'
                
    enchanter = f'{emojis.bp} Increases the chance to get a better enchant when enchanting\n'\
                f'{emojis.bp} Exact chance increase unknown'
    
    embed = discord.Embed(
        color = global_data.color,
        title = f'PROFESSIONS',
        description =   f'There are 5 professions you can increase to get increasing bonuses.\n'\
                        f'Each profession has 100 levels.\n'\
                        f'If you get all professions to level 100, you can ascend (see `{prefix}asc`).'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
    embed.add_field(name=f'WORKER {emojis.prworker}', value=worker, inline=False)
    embed.add_field(name=f'CRAFTER {emojis.prcrafter}', value=crafter, inline=False)
    embed.add_field(name=f'LOOTBOXER {emojis.prlootboxer}', value=lootboxer, inline=False)
    embed.add_field(name=f'MERCHANT {emojis.prmerchant}', value=merchant, inline=False)
    embed.add_field(name=f'ENCHANTER {emojis.prenchanter}', value=enchanter, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}prlevel` : How and when to level up your professions\n{emojis.bp} `{prefix}asc` : Details about ascension', inline=False)
            
    return (thumbnail, embed)


# Professions levelling guide
async def professions_levelling(prefix):
    
    crafter =   f'{emojis.bp} This is the first profession you should level up\n'\
                f'{emojis.bp} Level **before time travelling** with leftover materials\n'\
                f'{emojis.bp} Trade everything to {emojis.log} logs and craft/dismantle {emojis.logepic} EPIC logs\n'\
                f'{emojis.bp} Craft in batches of 500, dismantle in batches of 1000\n'\
                f'{emojis.bp} Once you reach level 90, switch to levelling merchant'
    
    merchant =  f'{emojis.bp} This is the second profession you should level up\n'\
                f'{emojis.bp} Level **before time travelling** with leftover materials\n'\
                f'{emojis.bp} Trade everything to {emojis.log} logs\n'\
                f'{emojis.bp} For each level look up `pr merchant` and calculate the XP you need for the next level\n'\
                f'{emojis.bp} Take 5x the XP amount and sell as many {emojis.log} logs\n'\
                f'{emojis.bp} Once you reach level 90, wait until lootboxer and worker are catching up'
                
    lootboxer = f'{emojis.bp} Levels up automatically when opening lootboxes\n'\
                f'{emojis.bp} Better lootboxes give more XP\n'\
                f'{emojis.bp} To maximize XP gain, buy {emojis.lbedgy} EDGY lootboxes on cooldown\n'\
                    
    worker =    f'{emojis.bp} Levels up automatically when using work commands\n'\
                f'{emojis.bp} Higher tier work commands give more XP'
                
    enchanter = f'{emojis.bp} This is the last profession you should level up because of costs\n'\
                f'{emojis.bp} Level **before time travelling** using `transmute`\n'\
                f'{emojis.bp} XP gain is based on the quality of the enchant you get\n'\
                f'{emojis.bp} You should have around 2 billion coins\n'\
                f'{emojis.bp} A {emojis.horset8} T8 horse is helpful'
    
    embed = discord.Embed(
        color = global_data.color,
        title = f'LEVELLING UP PROFESSIONS',
        description =   f'Don\'t stress about it too much, it usually takes around 10 time travels to reach ascension.\n'\
                        f'For detailed XP calculations check out the [Wiki](https://epic-rpg.fandom.com/wiki/Professions)'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
    embed.add_field(name=f'CRAFTER {emojis.prcrafter}', value=crafter, inline=False)
    embed.add_field(name=f'MERCHANT {emojis.prmerchant}', value=merchant, inline=False)
    embed.add_field(name=f'LOOTBOXER {emojis.prlootboxer}', value=lootboxer, inline=False)
    embed.add_field(name=f'WORKER {emojis.prworker}', value=worker, inline=False)
    embed.add_field(name=f'ENCHANTER {emojis.prenchanter}', value=enchanter, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}pr` : Professions overview\n{emojis.bp} `{prefix}asc` : Details about ascension', inline=False)
            
    return (thumbnail, embed)