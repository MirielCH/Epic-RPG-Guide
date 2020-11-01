# trading.py

import discord
import emojis
import global_data

# Trades for area X
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

# Command "trades"
async def trades():
    embed = discord.Embed(
        color = 8983807,
        title = f'AREA TRADES',
        description = 'This page lists all trades you should do before leaving each area.'
    )    
    embed.set_footer(text=f'Tip: Use "traderates" to see the trade rates of all areas')
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')
    
    for x in range(1,16):
        field_value = await get_area_trades(x)
        embed.add_field(name=f'AREA {x}', value=field_value, inline=False)
    
    return (thumbnail, embed)