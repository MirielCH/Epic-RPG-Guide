# horses.py

import discord
import emojis
import global_data

# Horses overview
async def horses(prefix):

    tier =  f'{emojis.bp} Tiers range from I to IX (1 to 9) (see `{prefix}htier`)\n'\
            f'{emojis.bp} Every tier unlocks new bonuses\n'\
            f'{emojis.bp} Mainly increased by breeding with other horses (see `{prefix}hbreed`)'\
            f'{emojis.bp} __Very__ small chance of increasing in horse races'
            
    level = f'{emojis.bp} Levels range from 1 to (tier * 10)\n'\
            f'{emojis.bp} Leveling up increases the horse type bonus (see the [Wiki](https://epic-rpg.fandom.com/wiki/Horse#Horse_Types_and_Boosts))\n'\
            f'{emojis.bp} Increased by using `horse training` which costs coins\n'\
            f'{emojis.bp} Training cost is reduced by leveling up lootboxer (see `{prefix}pr`)'
            
    type =  f'{emojis.bp} There are 5 different types (see `{prefix}htype`)\n'\
            f'{emojis.bp} 4 of the types increase a player stat, 1 unlocks the epic quest\n'\
            f'{emojis.bp} The exact bonus the type gives is dependent on the level\n'\
            f'{emojis.bp} Randomly changes when breeding unless you have a {emojis.horsetoken} horse token in your inventory'

    embed = discord.Embed(
        color = global_data.color,
        title = f'HORSES',
        description =   f'Horses have tiers, levels and types which all give certain important bonuses.'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'TIER', value=tier, inline=False)
    embed.add_field(name=f'LEVEL', value=level, inline=False)
    embed.add_field(name=f'TYPE', value=type, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}htier` : Details about horse tiers\n{emojis.bp} `{prefix}htype` : Details about horse types\n{emojis.bp} `{prefix}hbreed` : Details about horse breeding', inline=False)
            
    return (thumbnail, embed)

# Horse tiers
async def horsetiers(prefix):

    tier1 = f'{emojis.bp} No bonuses'
            
    tier2 = f'{emojis.bp} 5% more coins when using`daily` and `weekly`'
    
    tier3 = f'{emojis.bp} 10% more coins when using`daily` and `weekly`'
            
    tier4 = f'{emojis.bp} Unlocks immortality in `hunt` and `adventure`\n'\
            f'{emojis.bp} 20% more coins when using `daily` and `weekly`'
            
    tier5 = f'{emojis.bp} Unlocks horse racing\n'\
            f'{emojis.bp} 20% buff to lootbox drop chance\n'\
            f'{emojis.bp} 30% more coins when using `daily` and `weekly`'

    tier6 = f'{emojis.bp} Unlocks free access to dungeons without dungeon keys\n'\
            f'{emojis.bp} 50% buff to lootbox drop chance\n'\
            f'{emojis.bp} 45% more coins when using `daily` and `weekly`'
            
    tier7 = f'{emojis.bp} 20% buff to monster drops drop chance\n'\
            f'{emojis.bp} 100% buff to lootbox drop chance\n'\
            f'{emojis.bp} 60% more coins when using `daily` and `weekly`'
            
    tier8 = f'{emojis.bp} Unlocks higher chance to get better enchants (% unknown)\n'\
            f'{emojis.bp} 50% buff to monster drops drop chance\n'\
            f'{emojis.bp} 200% buff to lootbox drop chance\n'\
            f'{emojis.bp} 80% more coins when using `daily` and `weekly`'
            
    tier9 = f'{emojis.bp} Unlocks higher chance to find pets with `training` (10%)\n'\
            f'{emojis.bp} 100% buff to monster drops drop chance\n'\
            f'{emojis.bp} 400% buff to lootbox drop chance\n'\
            f'{emojis.bp} 100% more coins when using `daily` and `weekly`'

    embed = discord.Embed(
        color = global_data.color,
        title = f'HORSE TIERS',
        description =   f'Every horse tier unlocks additional bonuses.\n'\
                        f'Note: Every tier only lists the changes to the previous tier. You don\'t lose any unlocks when tiering up.'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'TIER I {emojis.horset1}', value=tier1, inline=False)
    embed.add_field(name=f'TIER II {emojis.horset2}', value=tier2, inline=False)
    embed.add_field(name=f'TIER III {emojis.horset3}', value=tier3, inline=False)
    embed.add_field(name=f'TIER IV {emojis.horset4}', value=tier4, inline=False)
    embed.add_field(name=f'TIER V {emojis.horset5}', value=tier5, inline=False)
    embed.add_field(name=f'TIER VI {emojis.horset6}', value=tier6, inline=False)
    embed.add_field(name=f'TIER VII {emojis.horset7}', value=tier7, inline=False)
    embed.add_field(name=f'TIER VIII {emojis.horset8}', value=tier8, inline=False)
    embed.add_field(name=f'TIER IX {emojis.horset9}', value=tier9, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}horse` : Horse overview\n{emojis.bp} `{prefix}htype` : Details about horse types\n{emojis.bp} `{prefix}hbreed` : Details about horse breeding', inline=False)
            
    return (thumbnail, embed)

# Horse types
async def horsetypes(prefix):

    defender =  f'{emojis.bp} Increases overall DEF\n'\
                f'{emojis.bp} The higher the horse level, the higher the DEF bonus\n'\
                f'{emojis.bp} 23.75 % chance to get this type when breeding'
    
    strong =    f'{emojis.bp} Increases overall AT\n'\
                f'{emojis.bp} The higher the horse level, the higher the AT bonus\n'\
                f'{emojis.bp} 23.75 % chance to get this type when breeding'
    
    tank =      f'{emojis.bp} Increases overall LIFE\n'\
                f'{emojis.bp} The higher the horse level, the higher the LIFE bonus\n'\
                f'{emojis.bp} 23.75 % chance to get this type when breeding'
                
    golden =    f'{emojis.bp} Increases the amount of coins from `hunt` and `adventure`\n'\
                f'{emojis.bp} The higher the horse level, the higher the coin bonus\n'\
                f'{emojis.bp} 23.75 % chance to get this type when breeding'
                
    special =   f'{emojis.bp} Unlocks the epic quest which gives more coins and XP than the regular quest\n'\
                f'{emojis.bp} The higher the horse level, the more coins and XP the epic quest gives\n'\
                f'{emojis.bp} 5 % chance to get this type when breeding'
    
    besttype =  f'{emojis.bp} If you are in {emojis.timetravel} TT 0-2: SPECIAL\n'\
                f'{emojis.bp} If you are in {emojis.timetravel} TT 3-19: DEFENDER (horse should be T6 L30+)\n'\
                f'{emojis.bp} If you are in {emojis.timetravel} TT 20+: TANK (horse should be T8 L80+)'

    embed = discord.Embed(
        color = global_data.color,
        title = f'HORSE TYPES',
        description =   f'Each horse type has its unique bonuses.\n'\
                        f'The best type for you depends on your current TT and your horse tier and level.'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'DEFENDER', value=defender, inline=False)
    embed.add_field(name=f'STRONG', value=strong, inline=False)
    embed.add_field(name=f'TANK', value=tank, inline=False)
    embed.add_field(name=f'GOLDEN', value=golden, inline=False)
    embed.add_field(name=f'SPECIAL', value=special, inline=False)
    embed.add_field(name=f'WHICH TYPE TO CHOOSE', value=besttype, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}horse` : Horse overview\n{emojis.bp} `{prefix}htier` : Details about horse tiers\n{emojis.bp} `{prefix}hbreed` : Details about horse breeding', inline=False)
            
    return (thumbnail, embed)

# Horse breeding
async def horsebreeding(prefix):

    howto =     f'{emojis.bp} Use `horse breeding [@player]`\n'\
                f'{emojis.bp} **Always** breed with a horse of the same tier\n'\
                f'{emojis.bp} Ideally breed with a horse of the same level'
    
    whereto =   f'{emojis.bp} You can find players in the [official EPIC RPG server](https://discord.gg/w5dej5m)'

    tier =      f'{emojis.bp} If you breed with same or higher tier, you may get +1 tier\n'\
                f'{emojis.bp} **If you breed with lower tier, you may tier down!**\n'\
                f'{emojis.bp} The chance to tier up gets lower the higher your tier is\n'\
                f'{emojis.bp} If one horse tiers up, the other one isn\'t guaranteed to do so too'
                
    level =     f'{emojis.bp} The new horses will have an average of both horse\'s levels\n'\
                f'{emojis.bp} Example: L20 horse + L24 horse = L22 horses'
                
    type =      f'{emojis.bp} Breeding changes your horse type randomly\n'\
                f'{emojis.bp} You can keep your type by buying a {emojis.horsetoken} horse token\n'\
                f'{emojis.bp} Note: Each breeding consumes 1 {emojis.horsetoken} horse token'

    embed = discord.Embed(
        color = global_data.color,
        title = f'HORSE BREEDING',
        description =   f'You need to breed to increase your horse tier and/or get a different type.'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'HOW TO BREED', value=howto, inline=False)
    embed.add_field(name=f'WHERE TO BREED', value=whereto, inline=False)
    embed.add_field(name=f'IMPACT ON TIER', value=tier, inline=False)
    embed.add_field(name=f'IMPACT ON LEVEL', value=level, inline=False)
    embed.add_field(name=f'IMPACT ON TYPE', value=type, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=f'{emojis.bp} `{prefix}horse` : Horse overview\n{emojis.bp} `{prefix}htier` : Details about horse tiers\n{emojis.bp} `{prefix}htype` : Details about horse types', inline=False)
            
    return (thumbnail, embed)