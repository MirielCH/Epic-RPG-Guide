# timetravel.py

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
from operator import itemgetter
from math import floor

# time travel commands (cog)
class timetravelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Command "ttX" - Specific tt information
    tt_aliases = ['timetravel',]
    for x in range(1,1000):
        tt_aliases.append(f'tt{x}')    
        tt_aliases.append(f'timetravel{x}') 

    @commands.command(name='tt',aliases=(tt_aliases))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def timetravel_specific(self, ctx, *args):
        
        invoked = ctx.message.content
        invoked = invoked.lower()
        
        if args:
            if len(args) > 1:
                await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [1-999]` or `{ctx.prefix}tt1`-`{ctx.prefix}tt999`')
                return       
            else:
                tt_no = args[0]
                if tt_no.isnumeric():
                    tt_no = int(tt_no)
                    if 1 <= tt_no <= 999:
                        if 1 <= tt_no <= 25:
                            tt_data = await database.get_tt_unlocks(ctx, tt_no)
                        else:
                            tt_data = (tt_no, 0, 0, '', '', '')
                    else:
                        await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [1-999]` or `{ctx.prefix}tt1`-`{ctx.prefix}tt999`')
                        return
                        
                    embed = await embed_timetravel_specific(tt_data, ctx.prefix)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [1-999]` or `{ctx.prefix}tt1`-`{ctx.prefix}tt999`')
        else:
            tt_no = invoked.replace(f'{ctx.prefix}timetravel','').replace(f'{ctx.prefix}tt','')
            
            if tt_no == '':
                embed = await embed_timetravel_overview(ctx.prefix)
                await ctx.send(embed=embed)
            else:
                if tt_no.isnumeric():
                    tt_no = int(tt_no)
                    if 1 <= tt_no <= 999:
                        if 1 <= tt_no <= 25:
                            tt_data = await database.get_tt_unlocks(ctx, int(tt_no))
                        else:
                            tt_data = (tt_no, 0, 0, '', '', '')
                        embed = await embed_timetravel_specific(tt_data, ctx.prefix)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [1-999]` or `{ctx.prefix}tt1`-`{ctx.prefix}tt999`')
                        return
                else:
                    await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [1-999]` or `{ctx.prefix}tt1`-`{ctx.prefix}tt999`')
                    return
                
    # Command "tt1000" - Because they will try
    @commands.command(aliases=('timetravel1000',))
    @commands.bot_has_permissions(send_messages=True)
    async def tt1000(self, ctx):
        
        await ctx.send('https://tenor.com/view/doctor-who-snap-tardis-david-tennant-gif-17590283')

    # Command "mytt" - Information about user's TT
    @commands.command(aliases=('mytimetravel',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def mytt(self, ctx):
        
        user_settings = await database.get_settings(ctx)
        if user_settings == None:
            await database.first_time_user(self.bot, ctx)
            return
        my_tt = int(user_settings[0])
        
        if 1 <= my_tt <= 25:    
            tt_data = await database.get_tt_unlocks(ctx, int(my_tt))
        else:
            tt_data = (my_tt,0,0,'','','')
        embed = await embed_timetravel_specific(tt_data, ctx.prefix, True)
        await ctx.send(embed=embed)
                
    # Command "supertimetravel" - Information about super time travel
    @commands.command(aliases=('stt','supertt',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def supertimetravel(self, ctx, *args):
        
        if args:
            arg = args[0]
            if arg == 'score':
                await self.supertimetravelscore(ctx)
                return
            elif arg == 'calc':
                if len(args) > 1:
                    await self.sttcalc(ctx, args[1])
                else:
                    await self.sttcalc(ctx)
                return
            else:
                embed = await embed_stt(ctx.prefix)
        else:
            embed = await embed_stt(ctx.prefix)
        
        await ctx.send(embed=embed)
        
    # Command "sttscore" - Returns super time travel score calculations
    @commands.command(aliases=('sttscore','superttscore','stts',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def supertimetravelscore(self, ctx, *args):
        if args:
            arg = args[0]
            if arg == 'calc':
                if len(args) > 1:
                    await self.sttcalc(ctx, args[1])
                else:
                    await self.sttcalc(ctx)
                return
            else:
                embed = await embed_stt_score(ctx.prefix)
        else:        
            embed = await embed_stt_score(ctx.prefix)
        
        await ctx.send(embed=embed)
        
    # Command "sttcalc" - Calculates STT score based in inventory and area
    @commands.command(aliases=('scorecalc','sttscorecalc','sttc','scalc','sc','superttcalc',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def sttcalc(self, ctx, *args):
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s inventory') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False
            
            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed
        
        error_syntax = (
            f'The command syntax is `{ctx.prefix}scorecalc [current max area]`\n'
            f'Example: `{ctx.prefix}scorecalc a5`'
        )
        
        if args:
            if len(args) == 1:
                area = args[0]
                area = area.lower()
                if area.find('top') > -1:
                    area = 16
                else:
                    area = area.lower().replace('a','')
                    if area.isnumeric():
                        area = int(area)
                        if not 1 <= area <= 16:
                            await ctx.send(f'There is no area {area}.')
                            return
                    else:
                        await ctx.send(f'There is no area {area}.')
                        return
            else:
                await ctx.send(error_syntax)
                return
        else:
            await ctx.send(error_syntax)
            return
        
        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg i` (or `abort` to abort)')
            answer_user_enchanter = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_user_enchanter.content
            answer = answer.lower()
            if answer in ('rpg i','rpg inventory','rpg inv',):
                answer_bot_inv = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    inventory = str(answer_bot_inv.embeds[0].fields).lower()
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                fish = await global_data.inventory_get(inventory, 'normie fish')
                fishgolden = await global_data.inventory_get(inventory, 'golden fish')
                fishepic = await global_data.inventory_get(inventory, 'epic fish')
                log = await global_data.inventory_get(inventory, 'wooden log')
                logepic = await global_data.inventory_get(inventory, 'epic log')
                logsuper = await global_data.inventory_get(inventory, 'super log')
                logmega = await global_data.inventory_get(inventory, 'mega log')
                loghyper = await global_data.inventory_get(inventory, 'hyper log')
                logultra = await global_data.inventory_get(inventory, 'ultra log')
                apple = await global_data.inventory_get(inventory, 'apple')
                banana = await global_data.inventory_get(inventory, 'banana')
                ruby = await global_data.inventory_get(inventory, 'ruby')
                wolfskin = await global_data.inventory_get(inventory, 'wolf skin')
                zombieeye = await global_data.inventory_get(inventory, 'zombie eye')
                unicornhorn = await global_data.inventory_get(inventory, 'unicorn horn')
                mermaidhair = await global_data.inventory_get(inventory, 'mermaid hair')
                chip = await global_data.inventory_get(inventory, 'chip')
                dragonscale = await global_data.inventory_get(inventory, 'dragon scale')
                lbcommon = await global_data.inventory_get(inventory, 'common lootbox')
                lbuncommon = await global_data.inventory_get(inventory, 'uncommon lootbox')
                lbrare = await global_data.inventory_get(inventory, 'rare lootbox')
                lbepic = await global_data.inventory_get(inventory, 'epic lootbox')
                lbedgy = await global_data.inventory_get(inventory, 'edgy lootbox')
                lbomega = await global_data.inventory_get(inventory, 'omega lootbox')
                lbgodly = await global_data.inventory_get(inventory, 'godly lootbox')
                lifepotion = await global_data.inventory_get(inventory, 'life potion')
                potato = await global_data.inventory_get(inventory, 'potato')
                carrot = await global_data.inventory_get(inventory, 'carrot')
                bread = await global_data.inventory_get(inventory, 'bread')
                seed = await global_data.inventory_get(inventory, 'seed')
            elif (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send('Wrong input. Aborting.')
                return
            # Do stuff
            pass
        except asyncio.TimeoutError as error:
            await ctx.send(f'**{ctx.author.name}**, couldn\'t find your inventory, RIP.')
            return
            
        traderate_data = await database.get_traderate_data(ctx, 'all')
        
        loghyper = loghyper + (logultra * 8)
        logmega = logmega + (loghyper * 8)
        logsuper = logsuper + (logmega * 8)
        logepic = logepic + (logsuper * 8)
        log = log + (logepic * 20)
        fishgolden = fishgolden + (fishepic * 80)
        fish = fish + (fishgolden * 12)
        apple = apple + (banana * 12)

        current_area = area
        original_area = area
        areas_best_changes = []
        
        # Get the amount of logs for the current area
        current_area_rates = traderate_data[current_area-1]
        current_fish_rate = current_area_rates[1]
        current_apple_rate = current_area_rates[2]
        current_ruby_rate = current_area_rates[3]
        log = log + (fish * current_fish_rate)
        if not current_apple_rate == 0:
            log = log + (apple * current_apple_rate)
            apple = 0
        if not current_ruby_rate == 0:
            log = log + (ruby * current_ruby_rate)
            ruby = 0
        
        # Calculate the best trade rate for all areas
        for area in traderate_data:
            area_no = area[0]
            area_no_next = area_no + 1
            if not area_no_next == len(traderate_data)+1:
                area_next = traderate_data[area_no_next-1]
            else:
                area_next = None
            
            fish_rate = area[1]
            apple_rate = area[2]
            ruby_rate = area[3]
            if not area_next == None:
                fish_rate_next = area_next[1]
                apple_rate_next = area_next[2]
                ruby_rate_next = area_next[3]
            
            if not area_next == None:
                if not fish_rate == 0:
                    fish_rate_change = fish_rate_next / fish_rate
                else:
                    fish_rate_change = 0
                if not apple_rate == 0:
                    apple_rate_change = apple_rate_next / apple_rate
                else:
                    apple_rate_change = 0
                if not ruby_rate == 0:
                    ruby_rate_change = ruby_rate_next / ruby_rate
                else:
                    ruby_rate_change = 0
            else:
                fish_rate_change = 1
                apple_rate_change = 1
                ruby_rate_change = 1
            
            if (fish_rate_change <= 1) and (apple_rate_change <= 1) and (ruby_rate_change <= 1):
                best_change_index = 3
            else:
                all_changes = [fish_rate_change, apple_rate_change, ruby_rate_change]
                best_change = max(all_changes)
                best_change_index = all_changes.index(best_change)
            
            areas_best_changes.append([area_no, best_change_index, fish_rate, apple_rate, ruby_rate])
            
            if area_next == None:
                break
        
        # Get the amount of logs in each area
        areas_log_amounts = []
        trade_fish_rate_next = None
        trade_apple_rate_next = None
        trade_ruby_rate_next = None
        for best_change in areas_best_changes[original_area-1:]:
            trade_area = best_change[0]
            trade_best_change = best_change[1]
            trade_fish_rate = best_change[2]
            trade_apple_rate = best_change[3]
            trade_ruby_rate = best_change[4]
            if not trade_area == len(areas_best_changes):
                next_area = areas_best_changes[trade_area]
                trade_fish_rate_next = next_area[2]
                trade_apple_rate_next = next_area[3]
                trade_ruby_rate_next = next_area[4]

            if not (trade_apple_rate_next == 0) and not (apple == 0):
                log = log + (apple * trade_apple_rate_next)
                apple = 0
            if not (trade_ruby_rate_next == 0) and not (ruby == 0):
                log = log + (ruby * trade_ruby_rate_next)
                ruby = 0
                
            if trade_area == original_area:
                areas_log_amounts.append([trade_area, log, trade_ruby_rate])
                
            if trade_best_change == 0:
                log = log / trade_fish_rate
                log = log * trade_fish_rate_next
            elif trade_best_change == 1:
                log = log / trade_apple_rate
                log = log * trade_apple_rate_next
            elif trade_best_change == 2:
                log = log / trade_ruby_rate
                log = log * trade_ruby_rate_next
        
            if not trade_area == len(areas_best_changes):
                areas_log_amounts.append([trade_area+1, log, trade_ruby_rate_next])
        

        a15 = areas_log_amounts[len(areas_log_amounts)-2]
        a16 = areas_log_amounts[len(areas_log_amounts)-1]
        log_a15 = a15[1]
        ruby_rate_a15 = a15[2]
        ruby_a15 = floor(log_a15 / ruby_rate_a15)
        log_a16 = a16[1]
        ruby_rate_a16 = a16[2]
        ruby_a16 = floor(log_a16 / ruby_rate_a16)
        
        score_lootboxes = round((lbcommon*0.05)+(lbuncommon*0.1)+(lbrare*0.15)+(lbepic*0.2)+(lbedgy*0.25)+(lbomega*2.5)+(lbgodly*25),2)
        score_mobdrops = round((wolfskin/20)+floor(zombieeye/9)+floor(unicornhorn/7)+floor(mermaidhair/5)+floor(chip/4)+floor(dragonscale/2),2)
        score_farm_items = floor((bread/20)+(carrot/25)+(potato/30)+(seed/2500))
        score_ruby_a15 = floor(ruby_a15/25)
        score_ruby_a16 = floor(ruby_a16/25)
        score_lifepotions = floor(lifepotion/500000)
        if score_lifepotions > 20:
            score_lifepotions = 20
        if score_lifepotions == 0 and lifepotion > 0:
            score_lifepotions = 1
            
        if original_area == 16:
            message_area = 'The TOP'
        else:
            message_area = original_area
        
        if a15[0] == 15:
            message_a15 = (
                f'**Area 15**\n'
                f'{emojis.bp} {score_lootboxes:,} lootbox score\n'
                f'{emojis.bp} {score_mobdrops:,} mob drop score\n'
                f'{emojis.bp} ~{score_farm_items:,} farm items score ({bread:,} bread, {carrot:,} carrots, {potato:,} potatoes, {seed:,} seeds)\n'
                f'{emojis.bp} ~{score_ruby_a15+score_lifepotions:,} materials score ({ruby_a15:,} rubies, {lifepotion:,} life potions)\n'
                f'{emojis.bp} ~**{score_lootboxes+score_mobdrops+score_farm_items+score_ruby_a15+score_lifepotions:,} total score**\n\n'
            )
        else:
            message_a15 = ''
        
        await ctx.send(
            f'**{ctx.author.name}**, this is the theoretical STT score for your inventory, calculated up to area 15 / the TOP.\n'
            f'The material calculation assumes that your **current** max area is **{message_area}** and that you trade **all** of your materials to rubies.\n'
            f'Note that this score does not include gear, levels and stats. This is only your inventory.\n\n'
            f'{message_a15}'
            f'**The TOP**\n'
            f'{emojis.bp} {score_lootboxes:,} lootbox score\n'
            f'{emojis.bp} {score_mobdrops:,} mob drop score\n'
            f'{emojis.bp} ~{score_farm_items:,} farm items score ({bread:,} bread, {carrot:,} carrots, {potato:,} potatoes, {seed:,} seeds)\n'
            f'{emojis.bp} ~{score_ruby_a16+score_lifepotions:,} materials score ({ruby_a16:,} rubies, {lifepotion:,} life potions)\n'
            f'{emojis.bp} ~**{score_lootboxes+score_mobdrops+score_farm_items+score_ruby_a16+score_lifepotions:,} total score**'
        )

# Initialization
def setup(bot):
    bot.add_cog(timetravelCog(bot))



# --- Redundancies ---
# Guides
guide_overview = '`{prefix}tt` : Time travel overview'
guide_mytt = '`{prefix}mytt` : Details about your current TT'
guide_tt_specific = '`{prefix}tt1`-`{prefix}tt999` : Details about specific TTs and how to prepare'
guide_stt = '`{prefix}stt` : Details about super time travel'
guide_stt_score = '`{prefix}sttscore` : Details about STT score'
guide_stt_score_calc = '`{prefix}scorecalc` / `{prefix}sc` : STT score calculator'

                    

# --- Embeds ---
# Time travel overview
async def embed_timetravel_overview(prefix):

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
        f'{emojis.bp} TIME dragon essences\n'
        f'{emojis.bp} OMEGA horse tokens\n'
        f'{emojis.bp} Event items (if an event is active)\n'
        f'{emojis.bp} Your horse\n'
        f'{emojis.bp} Your pets\n'
        f'{emojis.bp} Your marriage partner\n'
        f'{emojis.bp} Your guild\n'
        f'{emojis.bp} Profession levels\n'
    )
    
    guides = (
        f'{emojis.bp} {guide_mytt.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_tt_specific.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stt.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'TIME TRAVEL (TT)',
        description = (
            f'Resets your character to level 1 / area 1 but unlocks new game features and increases XP and drop chances.\n'
            f'To time travel, use `rpg time travel` while meeting the requirements.\n'
            f'Warning: **You will lose everything except the items mentioned below**. So make sure you have done all you want to do. You can check what you should do before time traveling by looking up the TT you are going to travel to (e.g. `{prefix}tt1` if you are about to travel to TT 1).'
        )
                      
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='REQUIREMENTS FOR TIME TRAVEL', value=where, inline=False)
    embed.add_field(name='WHAT YOU KEEP', value=keptitems, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Time travel guide for specific area
async def embed_timetravel_specific(tt_data, prefix, mytt=False):

    tt_no = int(tt_data[0])
    unlock_dungeon = int(tt_data[1])
    unlock_area = int(tt_data[2])
    unlock_enchant = tt_data[3]
    unlock_title = tt_data[4]
    unlock_misc = tt_data[5]
    
    bonus_xp = (99+tt_no)*tt_no/2
    bonus_duel_xp = (99+tt_no)*tt_no/4
    bonus_drop_chance = (49+tt_no)*tt_no/2
    dynamite_rubies = 1+(bonus_drop_chance / 100)
    rubies = round(dynamite_rubies)
    
    bonus_xp = f'{bonus_xp:,g}'
    bonus_duel_xp = f'{bonus_duel_xp:,g}'
    bonus_drop_chance = f'{bonus_drop_chance:,g}'

    if mytt == True:
        embed_description = (
            f'This is your current TT according to your settings.\n'
            f'If this is wrong, run `{prefix}setprogress`.'
        )
    else:
        embed_description = 'Allons-y !'

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
        
    unlocks = (
        f"{unlocks}{emojis.bp} **{bonus_xp} %** increased **XP** from everything except duels\n"
        f'{emojis.bp} **{bonus_duel_xp} %** increased **XP** from **duels**\n'
        f'{emojis.bp} **{bonus_drop_chance} %** extra chance to get **monster drops** (see `{prefix}dropchance`)\n'
        f'{emojis.bp} **{bonus_drop_chance} %** more **items** with work commands (**{rubies}** {emojis.ruby} rubies with `dynamite`)\n'
        f'{emojis.bp} Higher chance to get +1 tier in `horse breed` and `pet fusion` (chance unknown)'
    )
                  

    prep_tt1_to_2 = (
        f'{emojis.bp} If your horse is T6+: Get 30m coins\n'
        f'{emojis.bp} If your horse is <T6: Get 50m coins\n'
        f'{emojis.bp} If you need money: Do boosted minibosses, use `drill` and sell mob drops\n'
        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'
        f'{emojis.bp} Level up professions (see `{prefix}prlevel`)\n'
        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'
        f'{emojis.bp} Don\'t forget to sell your armor and sword!'
    )
    
    prep_tt3_to_4 = (
        f'{emojis.bp} If your horse is T6+: Get 50m coins\n'
        f'{emojis.bp} If your horse is <T6: Get 150m coins\n'
        f'{emojis.bp} If you need money: Do boosted minibosses, use `dynamite` and sell mob drops\n'
        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'
        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'
        f'{emojis.bp} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'
        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'
        f'{emojis.bp} Don\'t forget to sell your armor and sword!'
    )
    
    prep_tt5_to_9 = (
        f'{emojis.bp} If your horse is T6+: Get 150m coins\n'
        f'{emojis.bp} If your horse is <T6: Get 350m coins\n'
        f'{emojis.bp} If you need money: Do boosted minibosses, use `dynamite` and sell mob drops\n'
        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'
        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'
        f'{emojis.bp} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'
        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'
        f'{emojis.bp} Don\'t forget to sell your armor and sword!'
    )
    
    prep_tt10_to_24 = (
        f'{emojis.bp} If your horse is T6+: Get 350m coins\n'
        f'{emojis.bp} If your horse is <T6: Get 850m coins\n'
        f'{emojis.bp} If you need money: Do boosted minibosses, use `dynamite` and sell mob drops\n'
        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'
        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'
        f'{emojis.bp} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'
        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'
        f'{emojis.bp} Don\'t forget to sell your armor and sword!\n'
        f'{emojis.bp} Tip: Claim the {emojis.badgea15} area 15 badge if you haven\'t yet (`rpg badge claim 6`)\n'
    )

    prep_tt25 = (
        f'{emojis.bp} If your horse is T6+: Get 350m coins\n'
        f'{emojis.bp} If your horse is <T6: Get 850m coins\n'
        f'{emojis.bp} Note: You **need** a T6+ horse to do Dungeon 15\n'
        f'{emojis.bp} If you need money: Do boosted minibosses, use `dynamite` and sell mob drops\n'
        f'{emojis.bp} If you need money and are impatient: sell {emojis.apple} apples\n'
        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'
        f'{emojis.bp} Note: If you want to level enchanter, you need 2-3 billion coins\n'
        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'
        f'{emojis.bp} Sell everything else **except** the items listed in `{prefix}tt`\n'
        f'{emojis.bp} Don\'t forget to sell your armor and sword!'
    )
    
    prep_stt = (
        f'{emojis.bp} Get 850m coins\n'
        f'{emojis.bp} Level up professions if not done (see `{prefix}prlevel`)\n'
        f'{emojis.bp} If you need a higher score: Trade to {emojis.ruby} rubies (see `{prefix}sttscore`)\n'
        f'{emojis.bp} If you have materials left: Trade to {emojis.apple} apples and sell\n'
        f'{emojis.bp} Sell everything you don\'t need for your desired score (see `{prefix}sttscore)`\n'
        f'{emojis.bp} Do not sell items listed in `{prefix}tt`'
    )
    
    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_mytt.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stt.format(prefix=prefix)}'
    )               

    embed = discord.Embed(
        color = global_data.color,
        title = f'TIME TRAVEL {tt_no}',
        description = embed_description        
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='UNLOCKS & BONUSES', value=unlocks, inline=False)
    if not (mytt == True) and not (tt_no == 0):
        if 1 <= tt_no <= 2:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt1_to_2, inline=False)
        elif 3 <= tt_no <= 4:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt3_to_4, inline=False)
        elif 5 <= tt_no <= 9:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt5_to_9, inline=False)
        elif 10 <= tt_no <= 24:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt10_to_24, inline=False)
        elif tt_no == 25:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_tt25, inline=False)
        else:
            embed.add_field(name='WHAT TO DO BEFORE YOU TIME TRAVEL', value=prep_stt, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Super time travel
async def embed_stt(prefix):

    requirements = (
        f'{emojis.bp} {emojis.timetravel} TT 25+\n'
        f'{emojis.bp} {emojis.timekey} TIME key (drops from the boss in dungeon 15-1)'
    )
    
    starter_bonuses = (
        f'{emojis.bp} Start with +25 LIFE (50 score)\n'
        f'{emojis.bp} Start with a new Tier I pet (300 score)\n'
        f'{emojis.bp} Start with +50 AT (400 score)\n'
        f'{emojis.bp} Start with +50 DEF (400 score)\n'
        f'{emojis.bp} Start with 35 of each monster drop (400 score)\n'
        f'{emojis.bp} Start with an OMEGA lootbox (500 score)\n'
        f'{emojis.bp} Start with a new Tier III pet (1,500 score)\n'
        f'{emojis.bp} Start with 10 ULTRA logs (1,750 score)\n'
        f'{emojis.bp} Start in area 2 (2,000 score)\n'
        f'{emojis.bp} Start with a new Tier I pet with 1 skill (4,500 score)\n'
        f'{emojis.bp} Start in area 3 (4,500 score)\n'
        f'{emojis.bp} Start with a GODLY lootbox (6,500 score)'
    )
                        
    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_mytt.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_tt_specific.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stt_score.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stt_score_calc.format(prefix=prefix)}'
    ) 

    embed = discord.Embed(
        color = global_data.color,
        title = 'SUPER TIME TRAVEL',
        description = (
            f'Super time travel is unlocked once you reach {emojis.timetravel} TT 25. From this point onward you have to use `super time travel` to reach the next TT.\n'
            f'Super time travel lets you choose a starter bonus. You can (and have to) choose **1** bonus.\n'
            f'These bonuses cost score points which are calculated based on your inventory and your gear (see `{prefix}sttscore`).'
        )
                      
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='STARTER BONUSES', value=starter_bonuses, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Super time travel score guide
async def embed_stt_score(prefix):

    base = (
        f'{emojis.bp} If you are level 200, have the ULTRA-OMEGA set and your inventory is empty, you have 355.5 score'
    )

    gear = (
        f'{emojis.bp} {emojis.swordultraomega} ULTRA-OMEGA sword = ~74 score\n'
        f'{emojis.bp} {emojis.armorultraomega} ULTRA-OMEGA armor = ~87 score'
    )
    
    level = (
        f'{emojis.bp} 1 level = 0.5 score\n'
        f'{emojis.bp} 1 {emojis.statdef} DEF + 1 {emojis.statat} AT + 5 {emojis.statlife} HP = 0.4 score'
    )
    
    lootboxes = (
        f'{emojis.bp} 1 {emojis.lbcommon} common lootbox = 0.05 score\n'
        f'{emojis.bp} 1 {emojis.lbuncommon} uncommon lootbox = 0.1 score\n'
        f'{emojis.bp} 1 {emojis.lbrare} rare lootbox = 0.15 score\n'
        f'{emojis.bp} 1 {emojis.lbepic} EPIC lootbox = 0.2 score\n'
        f'{emojis.bp} 1 {emojis.lbedgy} EDGY lootbox = 0.25 score\n'
        f'{emojis.bp} 1 {emojis.lbomega} OMEGA lootbox = 2.5 score\n'
        f'{emojis.bp} 1 {emojis.lbgodly} GODLY lootbox = 25 score'
    )
                        
    materials = (
        f'{emojis.bp} 30 {emojis.potato} potatoes = 1 score\n'
        f'{emojis.bp} 25 {emojis.ruby} rubies = 1 score\n'
        f'{emojis.bp} 25 {emojis.carrot} carrots = 1 score\n'
        f'{emojis.bp} 20 {emojis.bread} bread = 1 score\n'
        f'{emojis.bp} 2500 {emojis.seed} seed = 1 score\n'
        f'{emojis.bp} **Take farm items score with a grain of salt for now**'
    )    
        
    mobdrops = (
        f'{emojis.bp} 20 {emojis.wolfskin} wolf skins = 1 score\n'
        f'{emojis.bp} 10 {emojis.zombieeye} zombie eyes = 1 score\n'
        f'{emojis.bp} 7 {emojis.unicornhorn} unicorn horns = 1 score\n'
        f'{emojis.bp} 5 {emojis.mermaidhair} mermaid hairs = 1 score\n'
        f'{emojis.bp} 4 {emojis.chip} chips = 1 score\n'
        f'{emojis.bp} 2 {emojis.dragonscale} dragon scales = 1 score'
    )
                                           
    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_mytt.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_tt_specific.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stt.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stt_score_calc.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'SUPER TIME TRAVEL SCORE',
        description = (
            f'The score points for the starter bonuses of super time travel are calculated based on your level, inventory and your gear.\n'
            f'You can calculate the score of your inventory with `{prefix}scorecalc`.'
        )
    )    

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='BASE SCORE', value=base, inline=False)
    embed.add_field(name='LEVEL & STATS', value=level, inline=False)
    embed.add_field(name='GEAR', value=gear, inline=False)
    embed.add_field(name='LOOTBOXES', value=lootboxes, inline=False)
    embed.add_field(name='MATERIALS', value=materials, inline=False)
    embed.add_field(name='MOB DROPS', value=mobdrops, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed