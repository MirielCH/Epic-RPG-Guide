# misc.py

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import discord
import emojis
import global_data
import database

from discord.ext import commands

# Miscellaneous commands (cog)
class miscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Command "duels" - Returns all duelling weapons
    @commands.command(aliases=('duel','duelling','dueling','duelweapons','duelweapon',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def duels(self, ctx):
        embed = await embed_duels(ctx.prefix)
        await ctx.send(embed=embed)
    
    # Command "codes" - Redeemable codes
    @commands.command(aliases=('code',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def codes(self, ctx):
        codes = await database.get_codes(ctx)
        embed = await embed_codes(ctx.prefix, codes)
        await ctx.send(embed=embed)            
    
    # Command "coolness" - Coolness guide
    @commands.command(aliases=('cool',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def coolness(self, ctx):
        embed = await embed_coolness(ctx.prefix)
        await ctx.send(embed=embed)
        
    # Command "badges" - Badge guide
    @commands.command(aliases=('badge',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def badges(self, ctx):
        embed = await embed_badges(ctx.prefix)
        await ctx.send(embed=embed)
    
    # Command "calc" - Simple calculator
    @commands.command(aliases=('calculate','calculator',))
    @commands.bot_has_permissions(send_messages=True)
    async def calc(self, ctx, *args):

        def formatNumber(num):
            if num % 1 == 0:
                return int(num)
            else:
                return num

        if args:
            calculation = ''
            allowedchars = set('1234567890.-+/*%()')
            
            for arg in args:
                calculation = f'{calculation}{arg}'
            
            if set(calculation).issubset(allowedchars):
                if calculation.find('**') > -1:
                    await ctx.send(
                        f'Invalid characters. Please only use numbers and supported operators.\n'
                        f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
                    )
                    return
                else:
                    pass
            else:
                await ctx.send(
                    f'Invalid characters. Please only use numbers and supported operators.\n'
                    f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
                )
                return
                
            # Parse open the calculation, convert all numbers to float and store it as a list
            # This is necessary because Python has the annoying habit of allowing infinite integers which can completely lockup a system. Floats have overflow protection.
            pos = 1
            calculation_parsed = []
            number = ''
            last_char_was_operator = False # Not really accurate name, I only use it to check for *, % and /. Multiple + and - are allowed.
            last_char_was_number = False
            calculation_sliced = calculation
            try:
                while not pos == len(calculation)+1:
                    slice = calculation_sliced[0:1]
                    allowedcharacters = set('1234567890.-+/*%()')
                    if set(slice).issubset(allowedcharacters):
                        if slice.isnumeric():
                            if last_char_was_number == True:
                                number = f'{number}{slice}'
                            else:
                                number = slice
                                last_char_was_number = True
                            last_char_was_operator = False
                        else:
                            if slice == '.':
                                number = f'{number}{slice}'
                            else:
                                if not number == '':        
                                    calculation_parsed.append(float(number))
                                    number = ''
                                
                                if slice in ('*','%','/'):
                                    if last_char_was_operator == True:
                                        await ctx.send(
                                            f'Error while parsing your input. Please check your equation.\n'
                                            f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
                                        )
                                        return
                                    else:
                                        calculation_parsed.append(slice)
                                        last_char_was_operator = True
                                else:
                                    calculation_parsed.append(slice)
                                    last_char_was_operator = False
                                last_char_was_number = False
                    else:
                        await ctx.send(
                            f'Error while parsing your input. Please check your equation.\n'
                            f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
                        )
                        return

                    calculation_sliced = calculation_sliced[1:]
                    pos = pos+1
                else:
                    if not number=='':
                        calculation_parsed.append(float(number))
            except:
                await ctx.send(
                    f'Error while parsing your input. Please check your equation.\n'
                    f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
                )
                return
            
            # Reassemble and execute calculation
            calculation_reassembled = ''
            for slice in calculation_parsed:
                calculation_reassembled = f'{calculation_reassembled}{slice}'
            
            try:
                result = eval(calculation_reassembled)
                result = formatNumber(result)
                result = f'{result:,}'
                if not len(result) > 2000:
                    await ctx.send(result)
                    return
                else:
                    await ctx.send('Well. Whatever you calculated, the result is too long to display. GG.')
                    return
            except:
                await ctx.send(
                    f'Well, _that_ didn\'t calculate to anything useful.\n'
                    f'What were you trying to do there? :thinking:'
                )
                return
        else:
            await ctx.send(
                f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [calculation]`\n'
                f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
            )
            
    # Command "tip" - Returns a random tip
    @commands.command(aliases=('tips',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def tip(self, ctx, *args):
        
        if args:
            if len(args)==1:
                id = args[0]
                if id.isnumeric():
                    id = int(id)
                    tip = await database.get_tip(ctx, id)
                else:
                    tip = await database.get_tip(ctx)
            else:
                tip = await database.get_tip(ctx)
        else:
            tip = await database.get_tip(ctx)
        
        embed = discord.Embed(
            color = global_data.color,
            title = 'TIP',
            description = tip[0]
        )    
        
        await ctx.send(embed=embed)

# Initialization
def setup(bot):
    bot.add_cog(miscCog(bot))

                    

# --- Embeds ---
# Duels
async def embed_duels(prefix):

    weapons = (
        f'{emojis.bp} {emojis.duelat}{emojis.duelat} - **AT**\n'
        f'{emojis.bp} {emojis.dueldef}{emojis.dueldef} - **DEF**\n'
        f'{emojis.bp} {emojis.duellife}{emojis.duellife} - **LIFE**\n'
        f'{emojis.bp} {emojis.duellevel}{emojis.duellevel} - **LEVEL**\n'
        f'{emojis.bp} {emojis.duelcoins}{emojis.duelcoins} - **Coins** (incl. bank account)\n'
        f'{emojis.bp} {emojis.duelgear}{emojis.duelgear} - **Gear** (both sword and armor)\n'
        f'{emojis.bp} {emojis.duelenchants}{emojis.duelenchants} - **Enchants** (both sword and armor)'
    )
    
    randomness = (
        f'{emojis.bp} Every duel score gets multiplied by 0.75 ~ 1.25\n'
        f'{emojis.bp} Thus the duel outcome can be highly unexpected'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'DUELS',
        description = 'Winning a duel depends on the chosen weapon and some luck.'
    )
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='DUELLING WEAPONS', value=weapons, inline=False)
    embed.add_field(name='RANDOMNESS', value=randomness, inline=False)
    embed.add_field(name='TIP', value=f'{emojis.bp} Unless you are __very__ rich, don\'t choose coins.', inline=False)
            
    return embed

# Redeemable codes
async def embed_codes(prefix, codes):

    temporary_value = ''
    permanent_value = ''

    for code in codes:  
        temporary_code = code[2]
        if temporary_code == 'True':
            temporary_value = f'{temporary_value}\n{emojis.bp} `{code[0]}`{emojis.blank}{code[1]}'
        else:
            permanent_value = f'{permanent_value}\n{emojis.bp} `{code[0]}`{emojis.blank}{code[1]}'

    embed = discord.Embed(
        color = global_data.color,
        title = 'REDEEMABLE CODES',
        description = (
            f'Use these codes with `rpg code` to get some free goodies.\n'
            f'Every code can only be redeemed once.'
        )          
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    
    if not temporary_value == '':
        embed.add_field(name='TEMPORARY EVENT CODES', value=temporary_value, inline=False)
    embed.add_field(name='PERMANENT CODES', value=permanent_value, inline=False)
            
    return embed

# Coolness
async def embed_coolness(prefix):

    usage = (
        f'{emojis.bp} Unlocks cosmetic only profile badges (see `{prefix}badges`)\n'
        f'{emojis.bp} You need at least 1000 coolness for dungeon 15-2 (see `{prefix}d15-2`)'
    )
                
    req = f'{emojis.bp} Unlocks when you reach area 12 in {emojis.timetravel}TT 1'
                
    howtoget = (
        f'{emojis.bp} `ultraining` awards 2 coolness per stage (unlocked in A12)\n'
        f'{emojis.bp} Survive adventures with 1 HP\n'
        f'{emojis.bp} Open {emojis.lbomega} OMEGA and {emojis.lbgodly} GODLY lootboxes\n'
        f'{emojis.bp} Get {emojis.loghyper} HYPER or {emojis.logultra} ULTRA logs from work commands\n'
        f'{emojis.bp} Forge ULTRA-EDGY or higher gear\n'
        f'{emojis.bp} Ascend a pet\n'
        f'{emojis.bp} Do other \'cool\' actions that are currently unknown'
    )
                
    note = (
        f'{emojis.bp} You don\'t lose coolness when you time travel\n'
        f'{emojis.bp} You can get coolness in every area once it\'s unlocked\n'
        f'{emojis.bp} If you have 100+, you get less (except from `ultraining`)\n'
        f'{emojis.bp} You can check your coolness by using `ultraining p`\n'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'COOLNESS',
        description = 'Coolness is a stat you start collecting once you reach area 12.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='REQUIREMENTS', value=req, inline=False)
    embed.add_field(name='HOW TO GET COOLNESS', value=howtoget, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
            
    return embed

# Badges
async def embed_badges(prefix):

    badges = (
        f'{emojis.bp} {emojis.badge1} : Unlocked with 1 coolness\n'
        f'{emojis.bp} {emojis.badge100} : Unlocked with 100 coolness\n'
        f'{emojis.bp} {emojis.badge200} : Unlocked with 200 coolness\n'
        f'{emojis.bp} {emojis.badge500} : Unlocked with 500 coolness\n'
        f'{emojis.bp} {emojis.badge1000} : Unlocked with 1000 coolness\n'
        f'{emojis.bp} {emojis.badgea15} : Unlocked by reaching area 15 ({emojis.timetravel}TT 10)\n'
        f'{emojis.bp} {emojis.badgetop} : Unlocked by beating D15-2 and reaching the TOP\n'
        f'{emojis.bp} {emojis.badgeomega} : Unlock requirements unknown'
    )
                
    howtouse = (
        f'{emojis.bp} Use `rpg badge list` to get the ID of the badges you want\n'
        f'{emojis.bp} Use `rpg badge claim [ID]` to claim a badge\n'
        f'{emojis.bp} Use `rpg badge [ID]` to activate or deactivate a badge'
    )
                
    note = (
        f'{emojis.bp} You can have several badges active at the same time\n'
        f'{emojis.bp} You can only claim badges you have unlocked\n'
        f'{emojis.bp} If you don\'t know how to get coolness, see `{prefix}coolness`'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'BADGES',
        description = 'Badges are cosmetic only profile decorations.'      
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='AVAILABLE BADGES', value=badges, inline=False)
    embed.add_field(name='HOW TO USE', value=howtouse, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
            
    return embed