# trading.py

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import discord
import emojis
import global_data
import database
import asyncio
from operator import itemgetter

from discord.ext import commands

# trading commands (cog)
class tradingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Trading menu
    @commands.command(aliases=('trading',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def tradingguide(self, ctx):
        embed = await embed_trading_menu(ctx)
        await ctx.send(embed=embed)
    
    # Command "trades" - Returns recommended trades of one area or all areas
    trades_aliases = ['tr','trade',]
    for x in range(1,16):
        trades_aliases.append(f'tr{x}')    
        trades_aliases.append(f'trades{x}') 
        trades_aliases.append(f'trade{x}')

    @commands.command(aliases=trades_aliases)
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def trades(self, ctx, *args):
        
        user_settings = await database.get_settings(ctx)
        if user_settings == None:
            await database.first_time_user(self.bot, ctx)
            return
        
        invoked = ctx.message.content
        invoked = invoked.lower()
        prefix = ctx.prefix
        prefix = prefix.lower()
        
        if args:
            if len(args)>1:
                await ctx.send(
                    f'The command syntax is `{prefix}trade [#]` or `{prefix}tr1`-`{prefix}tr15`\n'
                    f'Or you can use `{prefix}trade` to see the trades of all areas.'
                )
                return
            elif len(args)==1:
                area_no = args[0]
                if area_no.isnumeric():
                    area_no = int(area_no)
                    if 1 <= area_no <= 15:
                        embed = await embed_trades_area_specific(user_settings, area_no, ctx.prefix)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f'There is no area {area_no}, lol.')
                        return
                else:
                    await ctx.send(
                        f'The command syntax is `{prefix}{ctx.invoked_with} [#]` or `{prefix}tr1`-`{prefix}tr15`\n'
                        f'Or you can use `{prefix}trade` to see the trades of all areas.'
                    )
                    return
            else:
                await ctx.send(
                    f'The command syntax is `{prefix}{ctx.invoked_with} [#]` or `{prefix}tr1`-`{prefix}tr15`\n'
                    f'Or you can use `{prefix}trade` to see the trades of all areas.'
                )
                return
        else:
            area_no = invoked.replace(f'{prefix}trades','').replace(f'{prefix}trade','').replace(f'{prefix}tr','')
            if area_no.isnumeric():
                area_no = int(area_no)
                if 1 <= area_no <= 15:
                    embed = await embed_trades_area_specific(user_settings, area_no, ctx.prefix)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'There is no area {area_no}, lol.')
                    return       
            else:
                if area_no == '':             
                    embed = await embed_trades_all_areas(user_settings, ctx.prefix)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(
                        f'The command syntax is `{prefix}trade [#]` or `{prefix}tr1`-`{prefix}tr15`\n'
                        f'Or you can use `{prefix}trade` to see the trades of all areas.'
                    )
    
    # Command "traderates" - Returns trade rates of all areas
    @commands.command(aliases=('trr','rates','rate','traderate',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def traderates(self, ctx):
        traderate_data = await database.get_traderate_data(ctx, 'all')
        embed = await embed_traderates(traderate_data, ctx.prefix)
        await ctx.send(embed=embed)
    
    # Command "tradecalc" - Calculates the trades up to A10
    @commands.command(aliases=('trc',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def tradecalc(self, ctx, *args):
        
        if len(args) >= 3:
            area = args[0]
            amount = None
            mat = ''
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
                    await ctx.send(
                        f'The command syntax is:\n'
                        f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} [area] [amount] [material]`\n'
                        f'{emojis.blank} or\n'
                        f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} [area] [material] [amount]`.\n\n'
                        f'Example: `{ctx.prefix}{ctx.invoked_with} a3 60k fish`'
                    )
                    return
            for arg in args[1:]:
                argument = arg
                argument = argument.replace('k','000').replace('m','000000')
                if argument.isnumeric():
                    amount = argument
                else:
                    mat = f'{mat}{argument}'
                    original_argument = f'{mat} {argument}'
            
            if amount:   
                if not amount.isnumeric():
                    await ctx.send(f'Couldn\'t find a valid amount. :eyes:')
                    return
                try:
                    amount = int(amount)
                except:
                    await ctx.send('Are you trying to break me or something? :thinking:')
                    return
                if amount > 100000000000:
                    await ctx.send('Are you trying to break me or something? :thinking:')
                    return
            else:
                await ctx.send(f'Couldn\'t find a valid amount. :eyes:')
                return

            mat = mat.lower()        
            aliases = {
                'f': 'fish',
                'fishes': 'fish',
                'normie fish': 'fish',
                'l': 'log',
                'logs': 'log',
                'wooden log': 'log',
                'wooden logs': 'log',
                'a': 'apple',
                'apples': 'apple',
                'r': 'ruby',
                'rubies': 'ruby',
                'rubys': 'ruby'
            }
            if mat in aliases:
                mat = aliases[mat]   
            if not mat in ('fish','log','ruby','apple'):
                await ctx.send(f'`{mat}` is not a valid material. The supported materials are (wooden) logs, (normie) fish, apples and rubies.')
                return
            
            if mat == 'fish':
                mat_output = f'{emojis.fish} fish'
            elif mat == 'log':
                mat_output = f'{emojis.log} wooden logs'
            elif mat == 'apple':
                mat_output = f'{emojis.apple} apples'
            elif mat == 'ruby':
                mat_output = f'{emojis.ruby} rubies'
            
            traderate_data = await database.get_traderate_data(ctx, 'all')
            embed = await embed_tradecalc(traderate_data, (area,mat,amount), ctx.prefix)
            await ctx.send(embed=embed)
        
        else:
            await ctx.send(
                f'The command syntax is:\n'
                f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} [area] [amount] [material]`\n'
                f'{emojis.blank} or\n'
                f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} [area] [material] [amount]`.\n\n'
                f'Example: `{ctx.prefix}{ctx.invoked_with} a3 60k fish`'
            )
    
# Initialization
def setup(bot):
    bot.add_cog(tradingCog(bot))



# --- Redundancies ---
# Guides
guide_trades_all = '`{prefix}tr` : Trades (all areas)'
guide_trades_specific = '`{prefix}tr1`-`{prefix}tr15` : Trades in area 1~15'
guide_traderates = '`{prefix}trr` : Trade rates'
guide_tradecalc = '`{prefix}trc`  : Trade calculator'



# --- Embeds ---
# Trading menu
async def embed_trading_menu(ctx):
    
    prefix = ctx.prefix
                    
    trading = (
        f'{emojis.bp} `{prefix}trades [#]` / `{prefix}tr1`-`{prefix}tr15` : Trades in area 1~15\n'
        f'{emojis.bp} `{prefix}trades` / `{prefix}tr` : Trades (all areas)\n'
        f'{emojis.bp} `{prefix}traderates` / `{prefix}trr` : Trade rates\n'
        f'{emojis.bp} `{prefix}tradecalc` / `{prefix}trc` : Trade calculator'
    )
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'TRADING GUIDES',
        description = f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='TRADING', value=trading, inline=False)
    
    return embed

# Trades before leaving area X
async def embed_trades_area_specific(user_settings, area_no, prefix):
    
    if area_no==11: 
        if user_settings[0]==0:
            description = f'{emojis.bp} No trades because of {emojis.timetravel} time travel'
        else:
            description = await global_data.design_field_trades(area_no, user_settings[1])
    else:
        description = await global_data.design_field_trades(area_no, user_settings[1])
    
    guides = (
        f'{emojis.bp} {guide_trades_all.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_traderates.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_tradecalc.format(prefix=prefix)}'
    )
    
    embed = discord.Embed(
        color = 8983807,
        title = f'TRADES BEFORE LEAVING AREA {area_no}',
        description = description
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    
    return embed


# Trades before leaving all areas
async def embed_trades_all_areas(user_settings, prefix):
    
    guides = (
        f'{emojis.bp} {guide_trades_specific.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_traderates.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_tradecalc.format(prefix=prefix)}'
    )
    
    embed = discord.Embed(
        color = 8983807,
        title = 'AREA TRADES',
        description = (
            f'This page lists all trades you should do before leaving each area.\n'
            f'Areas not listed here don\'t have any recommended trades.\n'
            f'Everything that isn\'t mentioned can be ignored.'
        )
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    
    for x in range(1,16):
        if x not in (1,2,4,6,12,13,14):
            if x==11:
                if user_settings[0]==0:
                    embed.add_field(name=f'AREA {x}', value=f'{emojis.bp} No trades because of {emojis.timetravel} time travel', inline=False)    
                else:
                    field_value = await global_data.design_field_trades(x, user_settings[1])
                    embed.add_field(name=f'AREA {x}', value=field_value, inline=False)
            elif x==15:
                if user_settings[0]<25:
                    embed.add_field(name=f'AREA {x}', value=f'{emojis.bp} No trades because of {emojis.timetravel} time travel', inline=False)    
                else:
                    field_value = await global_data.design_field_trades(x, user_settings[1])
                    embed.add_field(name=f'AREA {x}', value=field_value, inline=False)
            else:
                field_value = await global_data.design_field_trades(x, user_settings[1])
                embed.add_field(name=f'AREA {x}', value=field_value, inline=False)
    
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    
    return embed

# Trade rates of all areas
async def embed_traderates(traderate_data, prefix):

    guides = (
        f'{emojis.bp} {guide_trades_specific.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_trades_all.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_tradecalc.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'TRADE RATES',
        description = f'The trades available to you depend on your **highest unlocked** area.\n{emojis.blank}'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    
    previous_area = [0,0,0,0]
    actual_areas = []
    for area_x in traderate_data:
        if not (area_x[1] == previous_area[1]) or not (area_x[2] == previous_area[2]) or not (area_x[3] == previous_area[3]):
            actual_areas.append(list(area_x))
        previous_area = area_x
    
    counter = 0
    for index, area_x in enumerate(actual_areas):
        counter = counter + 1
        if not area_x[0] == counter:
            actual_areas[index-1][0] = f'{actual_areas[index-1][0]}-{area_x[0]-1}'
        counter = area_x[0]
                
    for area_x in actual_areas:
        area_value = f'1 {emojis.fish} ⇄ {emojis.log} {area_x[1]}'
        if not area_x[2] == 0:
            area_value = f'{area_value}\n1 {emojis.apple} ⇄ {emojis.log} {area_x[2]}'
        if not area_x[3] == 0:
            area_value = f'{area_value}\n1 {emojis.ruby} ⇄ {emojis.log} {area_x[3]}'
        
        if area_x[0] == 16:
            embed.add_field(name='THE TOP', value=f'{area_value}\n{emojis.blank}', inline=True)
        else:
            embed.add_field(name=f'AREA {area_x[0]}', value=f'{area_value}\n{emojis.blank}', inline=True)
    
    if len(actual_areas) % 3 == 2:
        embed.add_field(name=f'{emojis.blank}', value=f'{emojis.blank}', inline=True)
        
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Trade calculator (aX mats > all area mats after trading)
async def embed_tradecalc(traderate_data, areamats, prefix):

    current_area = areamats[0]
    original_area = current_area
    current_mat = areamats[1]
    original_mat = current_mat
    current_amount = areamats[2]
    original_amount = current_amount
    trade_breakdown = ''
    last_area_trade = ''
    last_area_amount = current_amount
    areas_best_changes = []
    
    # Get the amount of logs for the current area
    current_area_rates = traderate_data[current_area-1]
    current_fish_rate = current_area_rates[1]
    current_apple_rate = current_area_rates[2]
    current_ruby_rate = current_area_rates[3]
    if current_mat == 'fish':
        current_amount = current_amount * current_fish_rate
        current_mat = 'log'
        original_mat = 'log'
        original_emoji = emojis.fish
    elif current_mat == 'apple':
        original_emoji = emojis.apple
        if not current_apple_rate == 0:
            current_amount = current_amount * current_apple_rate
            current_mat = 'log'
            original_mat = 'log'
        else:
            original_mat = 'apple'
    elif current_mat == 'ruby':
        original_emoji = emojis.ruby
        if not current_ruby_rate == 0:
            current_amount = current_amount * current_ruby_rate
            current_mat = 'log'
            original_mat = 'log'
        else:
            original_mat = 'ruby'
    else:
        original_emoji = emojis.log
        
    
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
        
        if (fish_rate_change <= 1) and (apple_rate_change <= 1) and (ruby_rate_change <= 1):
            best_change_index = 3
        else:
            all_changes = [fish_rate_change, apple_rate_change, ruby_rate_change]
            best_change = max(all_changes)
            best_change_index = all_changes.index(best_change)
        
        areas_best_changes.append([area_no, best_change_index, fish_rate, apple_rate, ruby_rate])
    
        if area_next == None:
            break
    
    # Get the amount of logs in each future area
    trade_amount = current_amount
    areas_log_amounts = []
    
    if original_area-1 == len(areas_best_changes)-1:
        best_change = areas_best_changes[original_area-1]
        trade_area = best_change[0]
        trade_best_change = best_change[1]
        trade_fish_rate = best_change[2]
        trade_apple_rate = best_change[3]
        trade_ruby_rate = best_change[4]
        areas_log_amounts.append([trade_area, trade_amount, current_mat,'0'])
    else:
        for best_change in areas_best_changes[original_area-1:len(areas_best_changes)-1]:
            trade_area = best_change[0]
            trade_best_change = best_change[1]
            trade_fish_rate = best_change[2]
            trade_apple_rate = best_change[3]
            trade_ruby_rate = best_change[4]
            if not trade_area+1 > len(areas_best_changes):
                next_area = areas_best_changes[trade_area]
                trade_fish_rate_next = next_area[2]
                trade_apple_rate_next = next_area[3]
                trade_ruby_rate_next = next_area[4]

            if trade_area == original_area:
                areas_log_amounts.append([trade_area, trade_amount, current_mat,'0'])

            if not current_mat == 'log':
                if current_mat == 'apple':
                    if not trade_apple_rate_next == 0:
                        trade_amount = trade_amount * trade_apple_rate_next
                        current_mat = 'log'
                elif current_mat == 'ruby':
                    if not trade_ruby_rate_next == 0:
                        trade_amount = trade_amount * trade_ruby_rate_next
                        current_mat = 'log'
            
            if current_mat == 'log':
                if trade_best_change == 0:
                    trade_amount = trade_amount / trade_fish_rate
                    trade_amount = trade_amount * trade_fish_rate_next
                elif trade_best_change == 1:
                    trade_amount = trade_amount / trade_apple_rate
                    trade_amount = trade_amount * trade_apple_rate_next
                elif trade_best_change == 2:
                    trade_amount = trade_amount / trade_ruby_rate
                    trade_amount = trade_amount * trade_ruby_rate_next
        
            areas_log_amounts.append([trade_area+1, trade_amount, current_mat,'0'])
    
    # Get the amount of logs in each past area
    trade_amount = current_amount
    past_areas_best_changes = list(reversed(areas_best_changes[:original_area]))
    for index, best_change in enumerate(past_areas_best_changes):
        trade_area = best_change[0]
        trade_fish_rate = best_change[2]
        trade_apple_rate = best_change[3]
        trade_ruby_rate = best_change[4]
        if not trade_area == 1:
            past_area = past_areas_best_changes[index+1]
            trade_best_change = past_area[1]
            trade_fish_rate_past = past_area[2]
            trade_apple_rate_past = past_area[3]
            trade_ruby_rate_past = past_area[4]
        else:
            trade_best_change = 0
            trade_fish_rate_past = trade_fish_rate
            trade_apple_rate_past = trade_apple_rate
            trade_ruby_rate_past = trade_ruby_rate

        if original_mat == 'log':
            if trade_best_change == 0:
                trade_amount = trade_amount / trade_fish_rate
                trade_amount = trade_amount * trade_fish_rate_past
            elif trade_best_change == 1:
                trade_amount = trade_amount / trade_apple_rate
                trade_amount = trade_amount * trade_apple_rate_past
            elif trade_best_change == 2:
                trade_amount = trade_amount / trade_ruby_rate
                trade_amount = trade_amount * trade_ruby_rate_past
        
        if not trade_area == 1:
            areas_log_amounts.append([trade_area-1, trade_amount, original_mat,'0'])
    
    areas_log_amounts = sorted(areas_log_amounts, key=itemgetter(0))
    
    guides = (
        f'{emojis.bp} {guide_trades_specific.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_trades_all.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_traderates.format(prefix=prefix)}'
    )
    
    if original_area == 16:
        area_name_description = 'The TOP'
    else:
        area_name_description = f'Area {original_area}'
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'TRADE CALCULATOR',
        description = f'If you have **{original_amount:,}** {original_emoji} in **{area_name_description}** and follow all the trades correctly, this amounts to the following:'
        )    
        
    embed.set_footer(text=await global_data.default_footer(prefix))
    
    previous_area = [0,0,]
    previous_area_trade_rates = [0,0,0,0]
    actual_areas = []
    for area_x in areas_log_amounts:
        area_trade_rates = traderate_data[area_x[0]-1]
        if not area_x == 1:
            previous_area_trade_rates = traderate_data[area_x[0]-2]
        if not (area_trade_rates[1] == previous_area_trade_rates[1]) or not (area_trade_rates[2] == previous_area_trade_rates[2]) or not (area_trade_rates[3] == previous_area_trade_rates[3]):
            actual_areas.append(list(area_x))
        previous_area = area_x
    
    counter = 0
    for index, area_x in enumerate(actual_areas):
        counter = counter + 1
        if not area_x[0] == counter:
            actual_areas[index-1][3] = f'{actual_areas[index-1][0]}-{area_x[0]-1}'

        actual_areas[index][3] = f'{area_x[0]}'
        counter = area_x[0]
    
    for area in actual_areas:
        area_no = area[0]
        area_logs = int(area[1])
        area_mat = area[2]
        area_name = area[3]
        area_trade_rates = traderate_data[area_no-1]
        area_fish_rate = area_trade_rates[1]
        area_apple_rate = area_trade_rates[2]
        area_ruby_rate = area_trade_rates[3]

        area_mats = ''
        if area_mat == 'log':
            area_fish = int(area_logs / area_fish_rate)
            try:
                area_apple = int(area_logs / area_apple_rate)
            except:
                area_apple = 0
            try:
                area_ruby = int(area_logs / area_ruby_rate)
            except:
                area_ruby = 0
                
            if area_no == 10:
                area_mats = f'{emojis.bp} **{area_logs:,}** {emojis.log}'
            else:
                area_mats = f'{emojis.bp} {area_logs:,} {emojis.log}'
            
            if area_no in (3, 9):
                area_mats = f'{area_mats}\n{emojis.bp} **{area_fish:,}** {emojis.fish}'
            else:
                area_mats = f'{area_mats}\n{emojis.bp} {area_fish:,} {emojis.fish}'
                
            if area_no in (5, 8):
                area_mats = f'{area_mats}\n{emojis.bp} **{area_apple:,}** {emojis.apple}'
            else:
                if not area_apple == 0:    
                    area_mats = f'{area_mats}\n{emojis.bp} {area_apple:,} {emojis.apple}'
                    
            if not area_ruby == 0:
                area_mats = f'{area_mats}\n{emojis.bp} {area_ruby:,} {emojis.ruby}'
        else:
            if area_no >= original_area:
                if area_mat == 'apple':
                    area_mats = f'{emojis.bp} {area_logs:,} {emojis.apple}'
                elif area_mat == 'ruby':
                    area_mats = f'{emojis.bp} {area_logs:,} {emojis.ruby}'
            else:
                area_mats = f'{emojis.bp} N/A'
        
        if area_name == '16':
            area_name = 'THE TOP'
        else:
            area_name = f'AREA {area_name}'
        
        embed.add_field(name=area_name, value=area_mats, inline=True)
    
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)            

    return embed