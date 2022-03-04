# bot.py

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