# xmas.py

import discord
import emojis
import global_data

# Christmas overview
async def xmas_overview(prefix):

    tree =      f'{emojis.bp} You can decorate a christmas tree\n'\
                f'{emojis.bp} The full tree requires the base, ? ornaments and the star\n'\
                f'{emojis.bp} The base is crafted with 20 {emojis.log} wooden logs\n'\
                f'{emojis.bp} The ornaments are ?\n'\
                f'{emojis.bp} To craft the star you need all 5 pieces which you get by completing all 5 quests\n'\
                f'{emojis.bp} If you manage to decorate the full tree before Dec 25th you will get a surprise'
                
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

    embed.add_field(name=f'AVAILABLE BADGES', value=badges, inline=False)
    embed.add_field(name=f'HOW TO USE', value=howtouse, inline=False)
    embed.add_field(name=f'NOTE', value=note, inline=False)
            
    return embed

# Christmas items
async def xmas_presents(prefix):

    presents =  f'{emojis.bp} EPIC present\n'\
                f'{emojis.bp} MEGA present\n'\
                f'{emojis.bp} ULTRA present\n'\
                f'{emojis.bp} OMEGA present\n'\
                f'{emojis.bp} GODLY present\n'\
                
    howtoget =  f'{emojis.bp} You get presents from the following commands:\n'\
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

    embed.add_field(name=f'AVAILABLE BADGES', value=badges, inline=False)
    embed.add_field(name=f'HOW TO USE', value=howtouse, inline=False)
    embed.add_field(name=f'NOTE', value=note, inline=False)
            
    return embed