# trading.py

import discord
import emojis
import global_data

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
                      f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs\n'\
                      f'{emojis.bp} Ignore logs and fish'
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
                      f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs\n'\
                      f'{emojis.bp} Ignore logs and fish'
    elif int(area_no) == 11:
        field_value = f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'\
                      f'{emojis.bp} Ignore logs, fish and fruits'
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
        description = f'This page lists all trades you should do before leaving each area.\nAreas not listed here don\'t have any recommended trades.\nThe trades for area 11 depend on your user settings.'
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

# Mats calculator (aX mats > a10 logs)
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
    
    
    for index, area in enumerate(traderate_data[original_area-1:]):
        current_trade = ''
        current_area = area[0]
        current_fish_rate = area[1]
        current_apple_rate = area[2]
        current_ruby_rate = area[3]
        
        if current_mat == 'fish':
            current_amount = current_amount * current_fish_rate
            current_mat = 'log'
        elif (current_mat == 'apple') and not (current_apple_rate == 0):
            current_amount = current_amount * current_apple_rate
            current_mat = 'log'
        elif (current_mat == 'ruby') and not (current_ruby_rate == 0):
            current_amount = current_amount * current_ruby_rate
            current_mat = 'log'
  
        if not index == (len(traderate_data)-original_area):
            next_area = traderate_data[current_area]
            next_fish_rate = next_area[1]
            next_apple_rate = next_area[2]
            next_ruby_rate = next_area[3]
            if not current_fish_rate == 0:
                fish_rate_change = next_fish_rate / current_fish_rate
            else:
                fish_rate_change = 0
            if not current_apple_rate == 0:
                apple_rate_change = next_apple_rate / current_apple_rate
            else:
                apple_rate_change = 0
            if not current_ruby_rate == 0:
                ruby_rate_change = next_ruby_rate / current_ruby_rate
            else:
                ruby_rate_change = 0
            if ((current_mat == 'ruby') and (current_ruby_rate  == 0)) or ((current_mat == 'apple') and (current_apple_rate  == 0)):
                trade_breakdown = f'{trade_breakdown}\n{emojis.bp} Area {current_area}: No trade available'
            elif (fish_rate_change in (0,1)) and (apple_rate_change in (0,1)) and (ruby_rate_change in (0,1)):
                trade_breakdown = f'{trade_breakdown}\n{emojis.bp} Area {current_area}: {last_area_amount:,} {last_area_trade}'
            else:
                all_changes = [fish_rate_change, apple_rate_change, ruby_rate_change]
                best_change = max(all_changes)
                best_change_index = all_changes.index(best_change)
                
                if (best_change <= 1) and ((apple_rate_change < 1) or (fish_rate_change < 1) or (ruby_rate_change < 1)):
                    trade_breakdown = f'{trade_breakdown}\n{emojis.bp} Area {current_area}: {current_amount:,} {emojis.log} logs'
                else:
                    if best_change_index == 0:
                        current_amount = int(current_amount / current_fish_rate)
                        current_mat = 'fish'
                        current_trade = f'{emojis.fish} fish'
                    elif best_change_index == 1:
                        current_amount = int(current_amount / current_apple_rate)
                        current_mat = 'apple'
                        current_trade = f'{emojis.apple} apples'
                    elif best_change_index == 2:
                        current_amount = int(current_amount / current_ruby_rate)
                        current_mat = 'ruby'
                        current_trade = f'{emojis.ruby} rubies'
            
                    trade_breakdown = f'{trade_breakdown}\n{emojis.bp} Area {current_area}: {current_amount:,} {current_trade}'
                    last_area_trade = current_trade
                    last_area_amount = current_amount
        else:
            trade_breakdown =   f'{trade_breakdown}\n{emojis.bp} Area {current_area}+: {current_amount:,} {emojis.log} logs'
    """    
    for index, area in reversed(enumerate(traderate_data[0:original_area])):
        current_trade = ''
        current_area = area[0]
        current_fish_rate = area[1]
        current_apple_rate = area[2]
        current_ruby_rate = area[3]
        
        if current_mat == 'fish':
            current_amount = current_amount * current_fish_rate
            current_mat = 'log'
        elif (current_mat == 'apple') and not (current_apple_rate == 0):
            current_amount = current_amount * current_apple_rate
            current_mat = 'log'
        elif (current_mat == 'ruby') and not (current_ruby_rate == 0):
            current_amount = current_amount * current_ruby_rate
            current_mat = 'log'
  
        if not index == 0:
            last_area = traderate_data[index-1]
            last_fish_rate = last_area[1]
            last_apple_rate = last_area[2]
            last_ruby_rate = last_area[3]
            if not last_fish_rate == 0:
                fish_rate_change = current_fish_rate / last_fish_rate
            else:
                fish_rate_change = 0
            if not last_apple_rate == 0:
                apple_rate_change = current_apple_rate / last_apple_rate
            else:
                apple_rate_change = 0
            if not last_ruby_rate == 0:
                ruby_rate_change = current_ruby_rate / last_ruby_rate
            else:
                ruby_rate_change = 0
            if ((current_mat == 'ruby') and (current_ruby_rate  == 0)) or ((current_mat == 'apple') and (current_apple_rate  == 0)):
                trade_breakdown_past = f'{trade_breakdown_past}\n{emojis.bp} Area {current_area}: No trade available.'
            elif (fish_rate_change in (0,1)) and (apple_rate_change in (0,1)) and (ruby_rate_change in (0,1)):
                trade_breakdown_past = f'{trade_breakdown_past}\n{emojis.bp} Area {current_area}: No trade necessary.'
            else:
                all_changes = [fish_rate_change, apple_rate_change, ruby_rate_change]
                best_change = max(all_changes)
                best_change_index = all_changes.index(best_change)
                
                if (best_change <= 1) and ((apple_rate_change < 1) or (fish_rate_change < 1) or (ruby_rate_change < 1)):
                    trade_breakdown = f'{trade_breakdown}\n{emojis.bp} Area {current_area}: {current_amount:,} {emojis.log} logs'
                else:
                    if best_change_index == 0:
                        current_amount = int(current_amount / current_fish_rate)
                        current_mat = 'fish'
                        current_trade = f'{emojis.fish} fish'
                    elif best_change_index == 1:
                        current_amount = int(current_amount / current_apple_rate)
                        current_mat = 'apple'
                        current_trade = f'{emojis.apple} apples'
                    elif best_change_index == 2:
                        current_amount = int(current_amount / current_ruby_rate)
                        current_mat = 'ruby'
                        current_trade = f'{emojis.ruby} rubies'
            
                    trade_breakdown = f'{trade_breakdown}\n{emojis.bp} Area {current_area}: {current_amount:,} {current_trade}'
                    last_area_trade = current_trade
                    last_area_amount = current_amount
            
                trade_breakdown_past = f'{trade_breakdown_past}\n{emojis.bp} Area {current_area}: Trade to {current_amount:,} {current_trade}.'
        else:
            trade_breakdown_past =   f'{trade_breakdown_past}\n{emojis.bp} Area {current_area}: Trade to {current_amount:,} {emojis.log} logs.\n'\
                                f'{emojis.bp} Area 11+: No useful trades anymore.'
    """                            
    trade_breakdown = trade_breakdown.strip()        

    return trade_breakdown