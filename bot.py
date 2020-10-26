# bot.py
import os
import discord
import sqlite3

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# Reads the bot token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Open connection to the local database
erg_db = sqlite3.connect('erg_db.db')

# Set default prefix
default_prefix = '$'

bot = discord.Client()

# Check database for stored prefix, if none is found, the default prefix $ is used
def get_prefix(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM global_settings where guild_id=?', [message.guild.id,])
    a = cur.fetchone()
    
    if a:
        prefix = a[1]
    else:
        prefix = default_prefix
        
    return commands.when_mentioned_or(*prefix)(bot, message)

bot = commands.Bot(command_prefix=get_prefix)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Suppresses errors if a command is entered that the bot doesn't recognize
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

# Return or set the prefix
@bot.command()
async def prefix(ctx, new_prefix=None):
    if new_prefix:
        await ctx.send(f'Parameter detected')
    else:
        a = get_prefix(bot, ctx)
        await ctx.send(f'The prefix for this server is `{a[-1]}`')
    
bot.run(TOKEN)