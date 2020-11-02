# trading.py

import discord
import emojis
import global_data

# Trade for area X
async def design_field_trades(area_no):
    
    if int(area_no) in (1,2,4,6,12,13,14,15):
        field_value = f'{emojis.bp} None'
    elif int(area_no) == 3:
        field_value = f'{emojis.bp} Dismantle {emojis.banana} bananas\n'\
                      f'{emojis.bp} Dismantle **all** logs\n'\
                      f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.log} logs to {emojis.fish} fish'
    elif int(area_no) == 5:
        field_value = f'{emojis.bp} Dismantle **all** logs\n'\
                      f'{emojis.bp} Dismantle **all** fish\n'\
                      f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.fish} fish to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.log} logs to {emojis.apple} apples'
    elif int(area_no) == 7:
        field_value = f'{emojis.bp} Dismantle {emojis.banana} bananas\n'\
                      f'{emojis.bp} Dismantle {emojis.apple} to {emojis.log} logs'
    elif int(area_no) == 8:
        field_value = f'{emojis.bp} Dismantle {emojis.logmega} MEGA logs and below if crafter < 90\n'\
                      f'{emojis.bp} Dismantle {emojis.loghyper} HYPER logs and below if crafter 90+\n'\
                      f'{emojis.bp} Dismantle **all** fish\n'\
                      f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.fish} fish to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.log} logs to {emojis.apple} apples'
    elif int(area_no) == 9:
        field_value = f'{emojis.bp} Dismantle {emojis.logepic} EPIC logs if crafter < 90\n'\
                      f'{emojis.bp} Dismantle {emojis.logsuper} SUPER logs and below if crafter 90+\n'\
                      f'{emojis.bp} Dismantle {emojis.banana} bananas\n'\
                      f'{emojis.bp} Trade {emojis.ruby} rubies to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.apple} apples to {emojis.log} logs\n'\
                      f'{emojis.bp} Trade {emojis.log} logs to {emojis.fish} fish'
    elif int(area_no) == 10:
        field_value = f'{emojis.bp} Dismantle {emojis.banana} bananas\n'\
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

# Trades before leaving areas
async def trades(user_settings):
    
    embed = discord.Embed(
        color = 8983807,
        title = f'AREA TRADES',
        description = f'This page lists all trades you should do before leaving each area.\nAreas not listed here don\'t have any recommended trades.\nThe trades for area 11 depend on your user settings.'
    )    
    embed.set_footer(text=f'Tip: Use "traderates" to see the trade rates of all areas.')
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
    for x in range(1,16):
        if x not in (1,2,4,6,12,13,14,15):
            if x==11: 
                if user_settings[0]==0:
                    embed.add_field(name=f'AREA {x}', value=f'{emojis.bp} No trades because of {emojis.timetravel} time travel', inline=False)    
                else:
                    field_value = await get_area_trades(x)
                    embed.add_field(name=f'AREA {x}', value=field_value, inline=False)
            else:
                field_value = await get_area_trades(x)
                embed.add_field(name=f'AREA {x}', value=field_value, inline=False)
            
    
    return (thumbnail, embed)

# Trade rates of all areas
async def traderates(traderate_data):

    embed = discord.Embed(
        color = global_data.color,
        title = f'TRADE RATES',
        description = f'The trades available to you depend on your **highest unlocked** area.'
    )    
    embed.set_footer(text=f'Tip: Use "trades" to see the trades you should do in each area.')
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
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
                embed.add_field(name=f'AREA {area_x[0]}+', value=area_value, inline=True)
            else:
                embed.add_field(name=f'AREA {area_x[0]}', value=area_value, inline=True)
            
    return (thumbnail, embed)