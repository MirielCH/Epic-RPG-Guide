# trading.py

import discord
import emojis
import global_data
from operator import itemgetter

# Trade for area X
async def design_field_trades(area_no):
    
    if int(area_no) in (1,2,4,6,12,13,14,15):
        field_value = f'{emojis.bp} None'
    elif int(area_no) == 3:
        field_value = f'{emojis.bp} Dismantle {emojis.fruitbanana} bananas\n'\
                      f'{emojis.bp} Dismantle {emojis.logultra} ULTRA logs and below\n'\
                      f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.log} logs to {emojis.fish} fish'
    elif int(area_no) == 5:
        field_value = f'{emojis.bp} Dismantle {emojis.logultra} ULTRA logs and below\n'\
                      f'{emojis.bp} Dismantle {emojis.fishepic} EPIC fish and below\n'\
                      f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.fish} fish to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.log} logs to {emojis.apple} apples'
    elif int(area_no) == 7:
        field_value = f'{emojis.bp} Dismantle {emojis.fruitbanana} bananas\n'\
                      f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs'
    elif int(area_no) == 8:
        field_value = f'{emojis.bp} If crafter <90: Dismantle {emojis.logmega} MEGA logs and below\n'\
                      f'{emojis.bp} If crafter 90+: Dismantle {emojis.loghyper} HYPER logs and below\n'\
                      f'{emojis.bp} Dismantle {emojis.fishepic} EPIC fish and below\n'\
                      f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.fish} fish to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.log} logs to {emojis.apple} apples'
    elif int(area_no) == 9:
        field_value = f'{emojis.bp} If crafter <90: Dismantle {emojis.logepic} EPIC logs\n'\
                      f'{emojis.bp} If crafter 90+: Dismantle {emojis.logsuper} SUPER logs and below\n'\
                      f'{emojis.bp} Dismantle {emojis.fruitbanana} bananas\n'\
                      f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.log} logs to {emojis.fish} fish'
    elif int(area_no) == 10:
        field_value = f'{emojis.bp} Dismantle {emojis.fruitbanana} bananas\n'\
                      f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs'
    elif int(area_no) == 11:
        field_value = f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs'
    else:
        field_value = f'{emojis.bp} N/A'

    return (field_value)

# Create field "trade rates" for area
async def design_field_traderate(traderate_data):
        
    field_value = f'{emojis.bp} 1 {emojis.fish} ⇄ {emojis.log} {traderate_data[1]}'
    if not traderate_data[2] == 0:
        field_value = f'{field_value}\n{emojis.bp} 1 {emojis.apple} ⇄ {emojis.log} {traderate_data[2]}'
        if not traderate_data[3] == 0:
            field_value = f'{field_value}\n{emojis.bp} 1 {emojis.ruby} ⇄ {emojis.log} {traderate_data[3]}'
            
    return (field_value)

# Trades before leaving all areas
async def trades(user_settings, prefix):
    
    embed = discord.Embed(
        color = 8983807,
        title = f'AREA TRADES',
        description = f'This page lists all trades you should do before leaving each area.\nAreas not listed here don\'t have any recommended trades.\nEverything that isn\'t mentioned can be ignored.'
    )    
    embed.set_footer(text=f'Tip: Use {prefix}tr1-{prefix}tr15 to see the trades of a specific area only.')
    
    for x in range(1,16):
        if x not in (1,2,4,6,12,13,14,15):
            if x==11: 
                if user_settings[0]==0:
                    embed.add_field(name=f'AREA {x}', value=f'{emojis.bp} No trades because of {emojis.timetravel} time travel', inline=False)    
                else:
                    field_value = await design_field_trades(x)
                    embed.add_field(name=f'AREA {x}', value=field_value, inline=False)
            else:
                field_value = await design_field_trades(x)
                embed.add_field(name=f'AREA {x}', value=field_value, inline=False)
            
    
    return embed

# Trades before leaving area X
async def trades_area_specific(user_settings, area_no, prefix):
    
    if area_no==11: 
        if user_settings[0]==0:
            description = f'{emojis.bp} No trades because of {emojis.timetravel} time travel'
        else:
            description = await design_field_trades(area_no)
    else:
        description = await design_field_trades(area_no)
    
    embed = discord.Embed(
        color = 8983807,
        title = f'TRADES BEFORE LEAVING AREA {area_no}',
        description = description
    )    
    embed.set_footer(text=f'Tip: Use {prefix}tr to see the trades of ALL areas.')
    
    return embed

# Trade rates of all areas
async def traderates(traderate_data, prefix):

    embed = discord.Embed(
        color = global_data.color,
        title = f'TRADE RATES',
        description = f'The trades available to you depend on your **highest unlocked** area.\n{emojis.blank}'
    )    
    embed.set_footer(text=f'Tip: Use {prefix}tr to see the trades you should do in each area.')
    
    area_limit = 0
    for area_x in traderate_data:
        area_limit = area_limit + 1
        if area_limit < 13:
            area_value = f'1 {emojis.fish} ⇄ {emojis.log} {area_x[1]}'
            if not area_x[2] == 0:
                area_value = f'{area_value}\n1 {emojis.apple} ⇄ {emojis.log} {area_x[2]}'
            if not area_x[3] == 0:
                area_value = f'{area_value}\n1 {emojis.ruby} ⇄ {emojis.log} {area_x[3]}'
            
            if area_limit == 12:
                embed.add_field(name=f'AREA {area_x[0]}+', value=f'{area_value}\n{emojis.blank}', inline=True)
            else:
                embed.add_field(name=f'AREA {area_x[0]}', value=f'{area_value}\n{emojis.blank}', inline=True)
            
    return embed

# Mats calculator (aX mats > all area mats after trading)
async def matscalc(traderate_data, areamats, prefix):

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
            break
        fish_rate = area[1]
        fish_rate_next = area_next[1]
        apple_rate = area[2]
        apple_rate_next = area_next[2]
        ruby_rate = area[3]
        ruby_rate_next = area_next[3]
        
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
        
        if (fish_rate_change == 1) and (apple_rate_change == 1) and (ruby_rate_change == 1):
            best_change_index = 3
        else:
            all_changes = [fish_rate_change, apple_rate_change, ruby_rate_change]
            best_change = max(all_changes)
            best_change_index = all_changes.index(best_change)
        
        areas_best_changes.append([area_no, best_change_index, fish_rate, apple_rate, ruby_rate])
    
    # Get the amount of logs in each future area
    trade_amount = current_amount
    areas_log_amounts = []
    for best_change in areas_best_changes[original_area-1:]:
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
            areas_log_amounts.append([trade_area, trade_amount, current_mat])

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
    
        areas_log_amounts.append([trade_area+1, trade_amount, current_mat])
    
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
            areas_log_amounts.append([trade_area-1, trade_amount, original_mat])
    
    areas_log_amounts = sorted(areas_log_amounts, key=itemgetter(0))
    
    embed = discord.Embed(
        color = global_data.color,
        title = f'TRADE CALCULATOR',
        description = f'If you have **{original_amount:,}** {original_emoji} in **area {original_area}** and follow all the trades correctly, this amounts to the following:'
        )    
        
    embed.set_footer(text=await global_data.default_footer(prefix))
    
    for area in areas_log_amounts[:12]:
        area_no = area[0]
        area_logs = int(area[1])
        area_mat = area[2]
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
        
        if area_no == 12:
            area_name = f'AREA {area_no}+'
        else:
            area_name = f'AREA {area_no}'
        
        embed.add_field(name=area_name, value=area_mats, inline=True)                   

    return embed