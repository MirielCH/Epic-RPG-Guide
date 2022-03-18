# bot.py

import sys
import traceback

import discord
from discord.ext import commands

import database
from resources import settings, logs


intents = discord.Intents.none()
intents.guilds = True   # for on_guild_join(), bot.guilds and everything guild related
intents.messages = True   # for the calculators that read the game
intents.message_content = True   # for the calculators that read the game


if settings.DEBUG_MODE:
    bot = commands.AutoShardedBot(command_prefix=database.get_all_prefixes, help_command=None,
                                  case_insensitive=True, intents=intents, owner_id=settings.OWNER_ID,
                                  debug_guilds=settings.DEV_GUILDS)
else:
    bot = commands.AutoShardedBot(command_prefix=database.get_all_prefixes, help_command=None,
                                  case_insensitive=True, intents=intents, owner_id=settings.OWNER_ID)


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
    'cogs.areas',
    'cogs.crafting',
    'cogs.dev',
    'cogs.dev_old',
    'cogs.dungeons',
    'cogs.enchanting',
    'cogs.events',
    'cogs.events_old',
    'cogs.fun',
    'cogs.guild',
    'cogs.guild_old',
    'cogs.gambling',
    'cogs.gambling_old',
    'cogs.horse',
    'cogs.horse_old',
    'cogs.links',
    'cogs.links_old',
    'cogs.main',
    'cogs.main_old',
    'cogs.misc',
    'cogs.monsters',
    'cogs.monsters_old',
    'cogs.pets',
    'cogs.professions',
    'cogs.professions_old',
    'cogs.settings',
    'cogs.timetravel',
    'cogs.titles',
    'cogs.titles_old',
    'cogs.trading',
]

if __name__ == '__main__':
    for extension in COG_EXTENSIONS:
        bot.load_extension(extension)

bot.run(settings.TOKEN)