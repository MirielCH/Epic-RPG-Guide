# horse.py

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import discord
import asyncio
import emojis
import global_data
import database

from discord.ext import commands

# horse commands (cog)
class horseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    horse_aliases = (
        'horses',
        'htier','horsestier','horsetiers','horsestiers',
        'htype','horsestype','horsetypes','horsestypes',
        'hbreed','hbreeding','breed','breeding','horsebreeding','horsesbreed','horsesbreeding','breedhorse','breedhorses','breedinghorse','breedingshorses'
    )
    
    # Command "horse"
    @commands.command(aliases=horse_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def horse(self, ctx, *args):
        invoked = ctx.invoked_with
        invoked = invoked.lower()
        if args:
            if len(args)>1:
                return
            elif len(args)==1:
                arg = args[0]
                if arg.find('tier') > -1:
                    embed = await embed_horses_tiers(ctx.prefix)
                    await ctx.send(embed=embed)
                elif arg.find('type') > -1:
                    embed = await embed_horses_types(ctx.prefix)
                    await ctx.send(embed=embed)
                elif arg.find('breed') > -1:
                    embed = await embed_horses_breeding(ctx.prefix)
                    await ctx.send(embed=embed)
                elif arg.find('calc') > -1:
                    x = await self.horsecalc(ctx)
                    return
                else:
                    embed = await embed_horses_overview(ctx.prefix)
                    await ctx.send(embed=embed)
            else:
                embed = await embed_horses_overview(ctx.prefix)
                await ctx.send(embed=embed)
        else:
            if invoked.find('tier') > -1:
                embed = await embed_horses_tiers(ctx.prefix)
                await ctx.send(embed=embed)
            elif invoked.find('type') > -1:
                embed = await embed_horses_types(ctx.prefix)
                await ctx.send(embed=embed)
            elif invoked.find('breed') > -1:
                embed = await embed_horses_breeding(ctx.prefix)
                await ctx.send(embed=embed)
            else:
                embed = await embed_horses_overview(ctx.prefix)
                await ctx.send(embed=embed)

    # Command "horsecalc" - Calculates the horse stats bonuses
    @commands.command(aliases=('hcalc',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def horsecalc(self, ctx, *args):
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if embed_author.find(f'{ctx_author}\'s horse') > 1:
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False
            
            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed
        
        if args:
            if len(args) == 2:
                horse_tier = args[0]
                horse_tier = horse_tier.lower().replace('t','')
                horse_level = args[1]
                horse_level = horse_level.lower().replace('l','')
                
                if horse_tier.isnumeric():
                    horse_tier = int(horse_tier)
                    if horse_level.isnumeric():
                        horse_level = int(horse_level)
                        if not horse_level >= 1:
                            await ctx.send(f'`{horse_level}` is not a valid horse level for a T{horse_tier} horse.\nThe level needs to be 1 or higher.')
                            return
                    else:
                        await ctx.send(f'`{args[1]}` doesn\'t look like a valid horse level to me :thinking:')
                        return
                    if not 1 <= horse_tier <= 9:
                            await ctx.send(f'`{horse_tier}` is not a valid horse tier.')
                            return
                else:
                    await ctx.send(f'`{args[0]}` doesn\'t look like a valid horse tier to me :thinking:')
                    return
                
                horse_emoji = getattr(emojis, f'horset{horse_tier}')
                
                horse_data = await database.get_horse_data(ctx, horse_tier)
                
                def_bonus = float(horse_data[1])
                strong_bonus = float(horse_data[2])
                tank_bonus = float(horse_data[3])
                special_bonus = float(horse_data[4])
                golden_bonus = float(horse_data[5])
                
                await ctx.send(
                    f'Stat bonuses for a {horse_emoji} **T{horse_tier} L{horse_level}** horse:\n'
                    f'{emojis.bp} DEFENDER: {def_bonus*horse_level:,g} % extra DEF\n'
                    f'{emojis.bp} STRONG: {strong_bonus*horse_level:,g} % extra AT\n'
                    f'{emojis.bp} TANK: {tank_bonus*horse_level:,g} % extra LIFE\n'
                    f'{emojis.bp} SPECIAL: {special_bonus*horse_level:,g} % extra coins and XP from the epic quest\n'
                    f'{emojis.bp} GOLDEN: {golden_bonus*horse_level:,g} % extra coins from `rpg hunt` and `rpg adventure`\n'
                ) 
            else:
                await ctx.send(
                    f'The command syntax is `{ctx.prefix}horsecalc [tier] [level]`\n'
                    f'You can also omit all parameters to use your horse tier and level for the calculation.\n\n'
                    f'Examples: `{ctx.prefix}horsecalc 6 25` or `{ctx.prefix}horsecalc t7 l30` or `{ctx.prefix}horsecalc 6 25`'
                )
        else:
            try:
                await ctx.send(f'**{ctx.author.name}**, please type `rpg horse` (or `abort` to abort)')
                answer_user_horse = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_horse.content
                answer = answer.lower()
                if (answer == 'rpg horse'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        horse_stats = str(answer_bot_at.embeds[0].fields[0])
                        
                        start_level = horse_stats.find('Horse Level -') + 14
                        end_level = start_level + 2
                        horse_level = horse_stats[start_level:end_level]
                        horse_level = horse_level.strip()
                        horse_level = int(horse_level)
                        
                        horse_chance = 0
                        horse_tier = 0
                        horse_emoji = ''
                    except:
                        await ctx.send(f'Whelp, something went wrong here, sorry.')
                        return
                    
                    if horse_stats.find('Tier - III') > 1:
                        horse_chance = 1
                        horse_tier = 3
                    elif horse_stats.find('Tier - II') > 1:
                        horse_chance = 1
                        horse_tier = 2
                    elif horse_stats.find('Tier - VIII') > 1:
                        horse_chance = 1.5
                        horse_tier = 8
                    elif horse_stats.find('Tier - VII') > 1:
                        horse_chance = 1.2
                        horse_tier = 7
                    elif horse_stats.find('Tier - VI') > 1:
                        horse_chance = 1
                        horse_tier = 6
                    elif horse_stats.find('Tier - V') > 1:
                        horse_chance = 1
                        horse_tier = 5
                    elif horse_stats.find('Tier - IV') > 1:
                        horse_chance = 1
                        horse_tier = 4
                    elif horse_stats.find('Tier - IX') > 1:
                        horse_chance = 2
                        horse_tier = 9
                    elif horse_stats.find('Tier - I') > 1:
                        horse_chance = 1    
                        horse_tier = 1
                    else:
                        await ctx.send(f'Whelp, something went wrong here, sorry.')
                        return
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send(f'Aborting.')
                    return
                else:
                    await ctx.send(f'Wrong input. Aborting.')
                    return
                
                horse_emoji = getattr(emojis, f'horset{horse_tier}')
                
                horse_data = await database.get_horse_data(ctx, horse_tier)
                
                def_bonus = float(horse_data[1])
                strong_bonus = float(horse_data[2])
                tank_bonus = float(horse_data[3])
                special_bonus = float(horse_data[4])
                golden_bonus = float(horse_data[5])
                
                await ctx.send(
                    f'Stat bonuses for a {horse_emoji} **T{horse_tier} L{horse_level}** horse:\n'
                    f'{emojis.bp} DEFENDER: {def_bonus*horse_level:,g} % extra DEF\n'
                    f'{emojis.bp} STRONG: {strong_bonus*horse_level:,g} % extra AT\n'
                    f'{emojis.bp} TANK: {tank_bonus*horse_level:,g} % extra LIFE\n'
                    f'{emojis.bp} SPECIAL: {special_bonus*horse_level:,g} % extra coins and XP from the epic quest\n'
                    f'{emojis.bp} GOLDEN: {golden_bonus*horse_level:,g} % extra coins from `rpg hunt` and `rpg adventure`\n\n'
                    f'Tip: You can use `{ctx.prefix}horsecalc [tier] [level]` to check the stats bonuses for any horse tier and level.'
                ) 
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your horse information, RIP.')

# Initialization
def setup(bot):
    bot.add_cog(horseCog(bot))



# --- Redundancies ---
# Guides
guide_overview = '`{prefix}horse` : Horse overview'
guide_breed = '`{prefix}horse breed` : Details about horse breeding'
guide_calc = '`{prefix}horse calc` : Horse stats bonus calculator'
guide_tier = '`{prefix}horse tier` : Details about horse tiers'
guide_type = '`{prefix}horse type` : Details about horse types'

                    

# --- Embeds ---
# Horse overview
async def embed_horses_overview(prefix):

    tier = (
        f'{emojis.bp} Tiers range from I to IX (1 to 9) (see `{prefix}horse tier`)\n'
        f'{emojis.bp} Every tier unlocks new bonuses\n'
        f'{emojis.bp} Mainly increased by breeding with other horses (see `{prefix}horse breed`)\n'
        f'{emojis.bp} Small chance of increasing in horse races (see `{prefix}event race`)'
    )
            
    level = (
        f'{emojis.bp} Levels range from 1 to ([tier] * 10) + [lootboxer bonus]\n'
        f'{emojis.bp} Example: A T7 horse with lootboxer at 102 has a max level of 72\n'
        f'{emojis.bp} Leveling up increases the horse type bonus (see the [Wiki](https://epic-rpg.fandom.com/wiki/Horse#Horse_Types_and_Boosts))\n'
        f'{emojis.bp} Increased by using `horse training` which costs coins\n'
        f'{emojis.bp} Training cost is reduced by leveling up lootboxer (see `{prefix}pr`)'
    )
            
    type = (
        f'{emojis.bp} There are 5 different types (see `{prefix}horse type`)\n'
        f'{emojis.bp} 4 of the types increase a player stat, 1 unlocks the epic quest\n'
        f'{emojis.bp} The exact bonus the type gives is dependent on the level\n'
        f'{emojis.bp} Randomly changes when breeding unless you have a {emojis.horsetoken} horse token in your inventory'
    )

    guides = (
        f'{emojis.bp} {guide_breed.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_calc.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_tier.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_type.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'HORSES',
        description = 'Horses have tiers, levels and types which all give certain important bonuses.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='TIER', value=tier, inline=False)
    embed.add_field(name='LEVEL', value=level, inline=False)
    embed.add_field(name='TYPE', value=type, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Horse tiers
async def embed_horses_tiers(prefix):

    tier1 = f'{emojis.bp} No bonuses'
            
    tier2 = f'{emojis.bp} 5% more coins when using `daily` and `weekly`'
    
    tier3 = f'{emojis.bp} 10% more coins when using `daily` and `weekly`'
            
    tier4 = (
        f'{emojis.bp} Unlocks immortality in `hunt` and `adventure`\n'
        f'{emojis.bp} 20% more coins when using `daily` and `weekly`'
    )
            
    tier5 = (
        f'{emojis.bp} Unlocks horse racing\n'
        f'{emojis.bp} 20% buff to lootbox drop chance\n'
        f'{emojis.bp} 30% more coins when using `daily` and `weekly`'
    )

    tier6 = (
        f'{emojis.bp} Unlocks free access to dungeons without dungeon keys\n'
        f'{emojis.bp} 50% buff to lootbox drop chance\n'
        f'{emojis.bp} 45% more coins when using `daily` and `weekly`'
    )
            
    tier7 = (
        f'{emojis.bp} 20% buff to monster drops drop chance\n'
        f'{emojis.bp} 100% buff to lootbox drop chance\n'
        f'{emojis.bp} 60% more coins when using `daily` and `weekly`'
    )
            
    tier8 = (
        f'{emojis.bp} Unlocks higher chance to get better enchants (% unknown)\n'
        f'{emojis.bp} 50% buff to monster drops drop chance\n'
        f'{emojis.bp} 200% buff to lootbox drop chance\n'
        f'{emojis.bp} 80% more coins when using `daily` and `weekly`'
    )
            
    tier9 = (
        f'{emojis.bp} Unlocks higher chance to find pets with `training` (10%)\n'
        f'{emojis.bp} 100% buff to monster drops drop chance\n'
        f'{emojis.bp} 400% buff to lootbox drop chance\n'
        f'{emojis.bp} 100% more coins when using `daily` and `weekly`'
    )
            
    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_breed.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_calc.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_type.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'HORSE TIERS',
        description = (
            f'Every horse tier unlocks additional bonuses.\n'
            f'Note: Every tier only lists the changes to the previous tier. You don\'t lose any unlocks when tiering up.'
        )
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'TIER I {emojis.horset1}', value=tier1, inline=False)
    embed.add_field(name=f'TIER II {emojis.horset2}', value=tier2, inline=False)
    embed.add_field(name=f'TIER III {emojis.horset3}', value=tier3, inline=False)
    embed.add_field(name=f'TIER IV {emojis.horset4}', value=tier4, inline=False)
    embed.add_field(name=f'TIER V {emojis.horset5}', value=tier5, inline=False)
    embed.add_field(name=f'TIER VI {emojis.horset6}', value=tier6, inline=False)
    embed.add_field(name=f'TIER VII {emojis.horset7}', value=tier7, inline=False)
    embed.add_field(name=f'TIER VIII {emojis.horset8}', value=tier8, inline=False)
    embed.add_field(name=f'TIER IX {emojis.horset9}', value=tier9, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Horse types
async def embed_horses_types(prefix):

    defender = (
        f'{emojis.bp} Increases overall DEF\n'
        f'{emojis.bp} The higher the horse level, the higher the DEF bonus\n'
        f'{emojis.bp} 23.75 % chance to get this type when breeding'
    )
    
    strong = (
        f'{emojis.bp} Increases overall AT\n'
        f'{emojis.bp} The higher the horse level, the higher the AT bonus\n'
        f'{emojis.bp} 23.75 % chance to get this type when breeding'
    )
    
    tank = (
        f'{emojis.bp} Increases overall LIFE\n'
        f'{emojis.bp} The higher the horse level, the higher the LIFE bonus\n'
        f'{emojis.bp} 23.75 % chance to get this type when breeding'
    )
                
    golden = (
        f'{emojis.bp} Increases the amount of coins from `hunt` and `adventure`\n'
        f'{emojis.bp} The higher the horse level, the higher the coin bonus\n'
        f'{emojis.bp} 23.75 % chance to get this type when breeding'
    )
                
    special = (
        f'{emojis.bp} Unlocks the epic quest which gives more coins and XP than the regular quest\n'
        f'{emojis.bp} The higher the horse level, the more coins and XP the epic quest gives\n'
        f'{emojis.bp} 5 % chance to get this type when breeding'
    )
    
    besttype = (
        f'{emojis.bp} If you are in {emojis.timetravel} TT 0-2: SPECIAL\n'
        f'{emojis.bp} If you are in {emojis.timetravel} TT 3+: DEFENDER (if T6 L30+)'
    )
                
    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_breed.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_calc.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_tier.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'HORSE TYPES',
        description = (
            f'Each horse type has its unique bonuses.\n'
            f'The best type for you depends on your current TT and your horse tier and level.'
        )
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='DEFENDER', value=defender, inline=False)
    embed.add_field(name='STRONG', value=strong, inline=False)
    embed.add_field(name='TANK', value=tank, inline=False)
    embed.add_field(name='GOLDEN', value=golden, inline=False)
    embed.add_field(name='SPECIAL', value=special, inline=False)
    embed.add_field(name='WHICH TYPE TO CHOOSE', value=besttype, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Horse breeding
async def embed_horses_breeding(prefix):

    howto = (
        f'{emojis.bp} Use `horse breeding [@player]`\n'
        f'{emojis.bp} You can only breed with a horse of the **same** tier\n'
        f'{emojis.bp} Ideally breed with a horse of the same level'
    )
    
    whereto = f'{emojis.bp} You can find players in the [official EPIC RPG server](https://discord.gg/w5dej5m)'

    tier = (
        f'{emojis.bp} You have a chance to get +1 tier\n'
        f'{emojis.bp} The chance to tier up gets lower the higher your tier is\n'
        f'{emojis.bp} If one horse tiers up, the other one isn\'t guaranteed to do so too'
    )
                
    level = (
        f'{emojis.bp} The new horses will have an average of both horse\'s levels\n'
        f'{emojis.bp} Example: L20 horse + L24 horse = L22 horses\n'
        f'{emojis.bp} Example: L20 horse + L23 horse = L21 **or** L22 horses'
    )
                
    type = (
        f'{emojis.bp} Breeding changes your horse type randomly\n'
        f'{emojis.bp} You can keep your type by buying a {emojis.horsetoken} horse token\n'
        f'{emojis.bp} Note: Each breeding consumes 1 {emojis.horsetoken} horse token'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_calc.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_tier.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_type.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'HORSE BREEDING',
        description = 'You need to breed to increase your horse tier and/or get a different type.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='HOW TO BREED', value=howto, inline=False)
    embed.add_field(name='WHERE TO BREED', value=whereto, inline=False)
    embed.add_field(name='IMPACT ON TIER', value=tier, inline=False)
    embed.add_field(name='IMPACT ON LEVEL', value=level, inline=False)
    embed.add_field(name='IMPACT ON TYPE', value=type, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed