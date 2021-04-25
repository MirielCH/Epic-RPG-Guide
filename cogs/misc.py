# misc.py

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import discord
import emojis
import global_data
import database
import asyncio

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

    # Command "farm" - Farming guide
    @commands.command(aliases=('farming',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def farm(self, ctx):
        embed = await embed_farm(ctx.prefix)
        await ctx.send(embed=embed)
    
    # Command "calc" - Simple calculator
    @commands.command(aliases=('calculate','calculator',))
    @commands.bot_has_permissions(send_messages=True)
    async def calc(self, ctx, *args):

        def formatNumber(num):
            if num % 1 == 0:
                return int(num)
            else:
                return round(num,5)

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
        
    # Command "coincap" - Calculate the coin cap
    @commands.command(aliases=('coin',))
    @commands.bot_has_permissions(send_messages=True, external_emojis=True)
    async def coincap(self, ctx, *args):
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
            
        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s profile') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False
            
            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed
        
        prefix = ctx.prefix
        
        error_syntax = (
            f'The command syntax is `{prefix}coincap [tt] [area]`\n'
            f'You can also use `{prefix}coincap` and let me read your profile.\n'
            f'Examples: `{prefix}coincap tt5 a12`, `{prefix}coincap 8 10`'
        )
        
        user_tt = None
        user_area = None
        
        if args:
            if args[0].lower() == 'cap':
                args = list(args)
                args.pop(0)
            if len(args) > 0:
                arg1 = args[0]
                arg1 = arg1.lower()
                arg1 = arg1.replace('tt','')
                if arg1.isnumeric():
                    user_tt = int(arg1)
                    if 0 <= user_tt <= 999:
                        if len(args) > 1:
                            arg2 = args[1]
                            arg2 = arg2.lower()
                            arg2 = arg2.replace('a','')
                            if arg1.isnumeric():
                                try:
                                    user_area = int(arg2)
                                except:
                                    await ctx.send(error_syntax)
                                    return
                                if 1 <= user_area <= 15:
                                    if ((user_area == 12) and (user_tt < 1)) or ((user_area == 13) and (user_tt < 3)) or ((user_area == 14) and (user_tt < 5)) or ((user_area == 15) and (user_tt < 10)):
                                        await ctx.send(f'You can not reach area {user_area} in TT {user_tt}.')
                                        return
                                else:
                                    await ctx.send('Sure, send me a postcard from that totally legit area.')
                                    return
                            else:
                                await ctx.send(error_syntax)
                                return
                        else:
                            await ctx.send(error_syntax)
                            return
                    else:
                        await ctx.send(f'Uuuuhhhhhh..... you sure about that time travel count?')
                        return
                else:
                    await ctx.send(error_syntax)
                    return
        
        if user_tt == None:
            try:
                await ctx.send(
                    f'**{ctx.author.name}**, please type `rpg p` (or `abort` to abort).\n\n'
                    f'Note: This does **not** work with profile backgrounds.\n'
                    f'Please remove your background or use `{ctx.prefix}coincap [tt] [max area]` instead.'
                )
                answer_user_at = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_at.content
                answer = answer.lower()
                if (answer == 'rpg p') or (answer == 'rpg profile') or (answer == 'rpg stats'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        profile = str(answer_bot_at.embeds[0].fields[0])
                    except:
                        try:
                            profile = str(answer_bot_at.embeds[0].fields[0])
                        except:
                            await ctx.send(
                                f'Whelp, something went wrong here, sorry.\n'
                                f'If you have a profile background, remove it or use `{ctx.prefix}coincap [tt] [max area]` instead.'
                            )
                            return
                        
                    start_area = profile.find('(Max:') + 6
                    end_area = profile.find(')', start_area)
                    user_area = profile[start_area:end_area]
                    user_area = int(user_area)
                    if profile.find('Time travels') > -1:
                        start_tt = profile.find('Time travels**') + 16
                        end_tt = profile.find('\',', start_tt)
                        user_tt = profile[start_tt:end_tt]
                        user_tt = int(user_tt)
                    else:
                        user_tt = 0
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return
                                
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profile, RIP.')
                return
        
        coin_cap = round(pow(user_tt,2.5)*10000000000+(user_area*2500000))
        await ctx.send(
            f'**{ctx.author.name}**, the coin cap for **TT {user_tt}**, **area {user_area}** is **{coin_cap:,}** {emojis.coin} coins.\n'
            f'You can not receive coins from other players or boosted minibosses that exceed this cap.'
        )

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
        f'{emojis.bp} You need at least 2,000 coolness for dungeon 15-2 (see `{prefix}d15-2`)'
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

# Farming
async def embed_farm(prefix):

    planting_normal = (
        f'{emojis.bp} Use `rpg farm` to plant {emojis.seed} seeds. Buy seeds in the shop for 2,000 coins.\n'
        f'{emojis.bp} This gives you XP and either {emojis.bread} bread, {emojis.carrot} carrots or {emojis.potato} potatoes\n'
        f'{emojis.bp} You have a 4% chance to receive special seeds (see below)\n'
        f'{emojis.bp} The cooldown of the command is 10m (donor reduction applies)'
    )
    
    planting_special = (
        f'{emojis.bp} There are three special seeds: {emojis.seedbread} bread, {emojis.seedcarrot} carrot and {emojis.seedpotato} potato seed\n'
        f'{emojis.bp} You can plant them with `rpg farm [type]` (e.g. `rpg farm carrot`)\n'
        f'{emojis.bp} The crop will be the same type (e.g. a {emojis.seedcarrot} carrot seed gives you {emojis.carrot} carrots)\n'
        f'{emojis.bp} You have a 65% chance to get 1 seed and a 10% chance to get 2 seeds back'
    )
                
    usage_bread = (
        f'{emojis.bp} {emojis.swordhair} `Hair Sword` ➜ 7 {emojis.mermaidhair} + **220** {emojis.bread}\n'
        f'{emojis.bp} {emojis.armorelectronical} `Electronical Armor` ➜ 12 {emojis.chip} + 1 {emojis.loghyper} + **180** {emojis.bread}\n'
        f'{emojis.bp} {emojis.foodcarrotbread} `Carrot Bread` (+1 Level) ➜ **1** {emojis.bread} + 160 {emojis.carrot}\n'
        f'{emojis.bp} 1 STT score per **20** {emojis.bread}\n'
        f'{emojis.bp} Can be sold for 3,000 coins and 3 merchant XP\n'
        f'{emojis.bp} Heals the player and gives a temporary +5 LIFE when eaten (`rpg eat bread`)'
    )
    
    usage_carrot = (
        f'{emojis.bp} {emojis.foodcarrotbread} `Carrot Bread` (+1 Level) ➜ 1 {emojis.bread} + **160** {emojis.carrot}\n'
        f'{emojis.bp} {emojis.foodorangejuice} `Orange Juice` (+3 AT, +3 DEF) ➜ **320** {emojis.carrot}\n'
        f'{emojis.bp} {emojis.foodcarrotato} `Carrotato Chips` (+25 random profession XP) ➜ 80 {emojis.potato} + **80** {emojis.carrot}\n'
        f'{emojis.bp} 1 STT score per **25** {emojis.carrot}\n'
        f'{emojis.bp} Can be sold for 2,500 coins and 3 merchant XP\n'
        f'{emojis.bp} Can be used to change the horse name with `rpg horse feed`'
    )
    
    usage_potato = (
        f'{emojis.bp} {emojis.swordruby} `Ruby Sword` ➜ 4 {emojis.ruby} + 1 {emojis.logmega} + **36** {emojis.potato}\n'
        f'{emojis.bp} {emojis.armorruby} `Ruby Armor` ➜ 7 {emojis.ruby} + 4 {emojis.unicornhorn} + **120** {emojis.potato} + 2 {emojis.logmega}\n'
        f'{emojis.bp} {emojis.swordelectronical} `Electronical Sword` ➜ 8 {emojis.chip} + 1 {emojis.logmega} + **140** {emojis.potato}\n'
        f'{emojis.bp} {emojis.foodcarrotato} `Carrotato Chips` (+25 random profession XP) ➜ **80** {emojis.potato} + 80 {emojis.carrot}\n'
        f'{emojis.bp} 1 STT score per **30** {emojis.potato}\n'
        f'{emojis.bp} Can be sold for 2,000 coins and 3 merchant XP'
    )
           
    what_to_plant = (
        f'{emojis.bp} If you want to cook food for levels or stats: {emojis.carrot} carrots\n'
        f'{emojis.bp} If you want to get more coins or a higher STT score: {emojis.bread} bread\n'
        f'{emojis.bp} If you want to flex potatoes for some reason: {emojis.potato} potatoes'
    )
                
    note = (
        f'{emojis.bp} Farming is unlocked in area 4.\n'
        f'{emojis.bp} The command can be used in area 1+ when ascended.\n'
        f'{emojis.bp} The amount of items you gain increases with your TT'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'FARMING',
        description = f'It ain\'t much, but it\'s honest work.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='PLANTING NORMAL SEEDS', value=planting_normal, inline=False)
    embed.add_field(name='PLANTING SPECIAL SEEDS', value=planting_special, inline=False)
    embed.add_field(name='BREAD USAGE', value=usage_bread, inline=False)
    embed.add_field(name='CARROT USAGE', value=usage_carrot, inline=False)
    embed.add_field(name='POTATO USAGE', value=usage_potato, inline=False)
    embed.add_field(name='WHAT TO FARM?', value=what_to_plant, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
            
    return embed