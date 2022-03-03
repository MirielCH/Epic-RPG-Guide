# bot.py

import discord
from discord.ext import commands

import database
from resources import settings


intents = discord.Intents.none()
intents.guilds = True   # for on_guild_join(), bot.guilds and everything guild related
intents.messages = True   # for the calculators that read the game


bot = commands.AutoShardedBot(command_prefix=database.get_all_prefixes, help_command=None,
                              case_insensitive=True, intents=intents)


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
    'cogs.misc',
    'cogs.monsters',
    'cogs.pets',
    'cogs.professions',
    'cogs.settings',
    'cogs.timetravel',
    'cogs.titles',
    'cogs.trading',
    ]
if __name__ == '__main__':
    for extension in COG_EXTENSIONS:
        bot.load_extension(extension)

bot.run(settings.TOKEN)