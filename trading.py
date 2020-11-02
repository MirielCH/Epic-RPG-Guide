# trading.py

import discord
import emojis
import global_data

# Trade for area X
async def get_area_trades(area_no):
    
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
async def traderates(trading_data):
    
    try:
        area1_data = trading_data[0]
        area2_data = trading_data[1]
        area3_data = trading_data[2]
        area4_data = trading_data[3]
        area5_data = trading_data[4]
        area6_data = trading_data[5]
        area7_data = trading_data[6]
        area8_data = trading_data[7]
        area9_data = trading_data[8]
        area10_data = trading_data[9]
        area11_data = trading_data[10]
        area12_data = trading_data[11]
        area13_data = trading_data[12]
        area14_data = trading_data[13]
        area15_data = trading_data[14]
    except:
        print('Error parsing trading data')
        return
        
    area1 = f'1 {emojis.fish} ⇄ {emojis.log} {area1_data[1]}\n'\
            f'{emojis.blank}' 
    
    area2 = area1
    
    area3 = f'1 {emojis.fish} ⇄ {emojis.log} {area3_data[1]}\n'\
            f'1 {emojis.apple} ⇄ {emojis.log} {area3_data[2]}\n'\
            f'{emojis.blank}'
            
    area4 = f'1 {emojis.fish} ⇄ {emojis.log} {area4_data[1]}\n'\
            f'1 {emojis.apple} ⇄ {emojis.log} {area4_data[2]}\n'\
            f'{emojis.blank}'
    
    area5 = f'1 {emojis.fish} ⇄ {emojis.log} {area5_data[1]}\n'\
            f'1 {emojis.apple} ⇄ {emojis.log} {area5_data[2]}\n'\
            f'1 {emojis.ruby} ⇄ {emojis.log} {area5_data[3]}\n'\
            f'{emojis.blank}'
            
    area6 = f'1 {emojis.fish} ⇄ {emojis.log} {area6_data[1]}\n'\
            f'1 {emojis.apple} ⇄ {emojis.log} {area6_data[2]}\n'\
            f'1 {emojis.ruby} ⇄ {emojis.log} {area6_data[3]}\n'\
            f'{emojis.blank}'
    
    area7 = area6
            
    area8 = f'1 {emojis.fish} ⇄ {emojis.log} {area8_data[1]}\n'\
            f'1 {emojis.apple} ⇄ {emojis.log} {area8_data[2]}\n'\
            f'1 {emojis.ruby} ⇄ {emojis.log} {area8_data[3]}\n'\
            f'{emojis.blank}'
    
    area9 = f'1 {emojis.fish} ⇄ {emojis.log} {area9_data[1]}\n'\
            f'1 {emojis.apple} ⇄ {emojis.log} {area9_data[2]}\n'\
            f'1 {emojis.ruby} ⇄ {emojis.log} {area9_data[3]}\n'\
            f'{emojis.blank}'
            
    area10 = f'1 {emojis.fish} ⇄ {emojis.log} {area10_data[1]}\n'\
             f'1 {emojis.apple} ⇄ {emojis.log} {area10_data[2]}\n'\
             f'1 {emojis.ruby} ⇄ {emojis.log} {area10_data[3]}\n'\
             f'{emojis.blank}'
             
    area11 = f'1 {emojis.fish} ⇄ {emojis.log} {area11_data[1]}\n'\
             f'1 {emojis.apple} ⇄ {emojis.log} {area11_data[2]}\n'\
             f'1 {emojis.ruby} ⇄ {emojis.log} {area11_data[3]}\n'\
             f'{emojis.blank}'

    area12 = f'1 {emojis.fish} ⇄ {emojis.log} {area12_data[1]}\n'\
             f'1 {emojis.apple} ⇄ {emojis.log} {area12_data[2]}\n'\
             f'1 {emojis.ruby} ⇄ {emojis.log} {area12_data[3]}\n'\
             f'{emojis.blank}'

    areas = [area1,area2,area3,area4,area5,area6,area7,area8,area9,area10,area11,area12,]

    embed = discord.Embed(
        color = global_data.color,
        title = f'TRADE RATES OF ALL AREAS',
        description = f'The trades available to you depend on your **highest unlocked** area.'
    )    
    embed.set_footer(text=f'Tip: Use "trades" to see the trades you should do in each area.')
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
    for index, area in enumerate(areas, start=1):
        if index < 12:
            embed.add_field(name=f'AREA {index}', value=area, inline=True)
        else:
            embed.add_field(name=f'AREA {index}+', value=area, inline=True)
            
    return (thumbnail, embed)