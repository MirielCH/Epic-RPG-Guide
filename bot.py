# bot.py

from datetime import datetime
import sys
import traceback

import discord

import database
from resources import functions, settings, logs


startup_time = datetime.isoformat(datetime.utcnow().replace(microsecond=0), sep=' ')
functions.await_coroutine(database.update_setting('startup_time', startup_time))


intents = discord.Intents.none()
intents.guilds = True   # for on_guild_join(), bot.guilds and everything guild related
intents.messages = True   # for the calculators that read the game
intents.message_content = True   # for the calculators that read the game


if settings.DEBUG_MODE:
    bot = discord.AutoShardedBot(intents=intents, owner_id=settings.OWNER_ID, debug_guilds=settings.DEV_GUILDS)
else:
    bot = discord.AutoShardedBot(intents=intents, owner_id=settings.OWNER_ID)


@bot.event
async def on_error(event: str, *args, **kwargs) -> None:
    """Runs when an error outside a command appears.
    All errors get written to the database for further review.
    """
    if not settings.DEBUG_MODE: return
    if event == 'on_message':
        message, = args
        if message.channel.type.name == 'private': return
        embed = discord.Embed(title='An error occured')
        error = sys.exc_info()
        traceback_str = "".join(traceback.format_tb(error[2]))
        traceback_message = f'{error[1]}\n{traceback_str}'
        print(traceback_message)
        logs.logger.error(traceback_message)
        embed.add_field(name='Event', value=f'`{event}`', inline=False)
        embed.add_field(name='Error', value=f'```py\n{traceback_message[:1015]}```', inline=False)
        await database.log_error(f'Got an error in event {event}:\nError: {error[1]}\nTraceback: {traceback_str}')
        await message.channel.send(embed=embed)
    else:
        try:
            message, = args
        except:
            return
        embed = discord.Embed(title='An error occured')
        error = sys.exc_info()
        traceback_str = "".join(traceback.format_tb(error[2]))
        traceback_message = f'{error[1]}\n{traceback_str}'
        print(traceback_message)
        logs.logger.error(traceback_message)
        embed.add_field(name='Error', value=f'```py\n{traceback_message[:1015]}```', inline=False)
        await database.log_error(f'Got an error:\nError: {error[1]}\nTraceback: {traceback_str}')
        await message.channel.send(embed=embed)
        if event == 'on_reaction_add':
            reaction, user = args
            return
        elif event == 'on_command_error':
            ctx, error = args
            raise
        else:
            return


COG_EXTENSIONS = [
    'cogs.alchemy',
    'cogs.areas',
    'cogs.cache',
    'cogs.crafting',
    'cogs.dev',
    'cogs.duel',
    'cogs.dungeons',
    'cogs.enchanting',
    'cogs.events',
    'cogs.fun',
    'cogs.guild',
    'cogs.gambling',
    #'cogs.halloween',
    'cogs.horse',
    'cogs.main',
    'cogs.misc',
    'cogs.monsters',
    'cogs.pets',
    'cogs.professions',
    'cogs.settings',
    'cogs.timetravel',
    'cogs.titles',
    'cogs.trading',
    'cogs.ultraining',
    #'cogs.valentine',
    #'cogs.xmas',
]

if __name__ == '__main__':
    for extension in COG_EXTENSIONS:
        bot.load_extension(extension)

bot.run(settings.TOKEN)