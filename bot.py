# bot.py

import sys
import traceback

import discord
from discord.ext import commands

import database
from resources import settings


intents = discord.Intents.none()
intents.guilds = True   # for on_guild_join(), bot.guilds and everything guild related
intents.messages = True   # for the calculators that read the game
intents.message_content = True   # for EPIC RPG reading and message commands


if settings.DEBUG_MODE:
    bot = commands.AutoShardedBot(command_prefix=database.get_all_prefixes, help_command=None,
                                  case_insensitive=True, intents=intents, owner_id=settings.OWNER_ID,
                                  debug_guilds=settings.DEV_GUILDS)
else:
    bot = commands.AutoShardedBot(command_prefix=database.get_all_prefixes, help_command=None,
                                  case_insensitive=True, intents=intents, owner_id=settings.OWNER_ID)


@bot.event
async def on_error(event: str, message: discord.Message) -> None:
    """Runs when an error outside a command appears.
    All errors get written to the database for further review.
    """
    if not settings.DEBUG_MODE: return
    if message.channel.type.name == 'private': return
    embed = discord.Embed(title='An error occured')
    error = sys.exc_info()
    traceback_str = "".join(traceback.format_tb(error[2]))
    traceback_message = f'{error[1]}\n{traceback_str}'
    embed.add_field(name='Event', value=f'`{event}`', inline=False)
    embed.add_field(name='Error', value=f'```py\n{traceback_message[:1015]}```', inline=False)
    await database.log_error(f'Got an error in event {event}:\nError: {error[1]}\nTraceback: {traceback_str}')
    await message.channel.send(embed=embed)

COG_EXTENSIONS = [
    'cogs.areas',
    'cogs.crafting',
    'cogs.dev',
    'cogs.dungeons',
    'cogs.events',
    'cogs.fun',
    'cogs.guilds',
    'cogs.gambling',
    'cogs.horse',
    'cogs.links',
    'cogs.main',
    'cogs.main_old',
    'cogs.misc',
    'cogs.monsters',
    'cogs.pets',
    'cogs.professions',
    'cogs.professions_old',
    'cogs.settings',
    'cogs.timetravel',
    'cogs.titles',
    'cogs.trading',
    ]
if __name__ == '__main__':
    for extension in COG_EXTENSIONS:
        bot.load_extension(extension)

bot.run(settings.TOKEN)