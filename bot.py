# bot.py
import os
import discord
import sqlite3

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound
#from discord.ext.commands import MissingPermissions

# Reads the bot token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Open connection to the local database
erg_db = sqlite3.connect('erg_db.db')

# Set default prefix
default_prefix = '$'

bot = discord.Client()

# Check database for stored prefix, if none is found, the default prefix $ is used
def get_prefix_all(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM global_settings where guild_id=?', [message.guild.id,])
    a = cur.fetchone()
    
    if a:
        prefix = a[1]
    else:
        prefix = default_prefix
        
    return commands.when_mentioned_or(*prefix)(bot, message)

def get_prefix(bot, message):
    cur=erg_db.cursor()
    cur.execute('SELECT * FROM global_settings where guild_id=?', [message.guild.id,])
    a = cur.fetchone()
    
    if a:
        prefix = a[1]
    else:
        prefix = default_prefix
        
    return prefix

bot = commands.Bot(command_prefix=get_prefix_all)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Suppresses errors if a command is entered that the bot doesn't recognize
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, (commands.MissingPermissions)):
        await ctx.send(f'Sorry, you are not allowed to use that command.')
    raise error

# Set new prefix (if user has "manage server" permission)
@bot.command()
@commands.has_permissions(manage_guild=True)
async def setprefix(ctx, *new_prefix):
    if new_prefix:
        if len(new_prefix)>1:
            await ctx.send('Too many arguments.\nCommand syntax: `setprefix [prefix]`')
        else:
            await ctx.send(f'Prefix changed to `{new_prefix[0]}`')
    else:
        a = get_prefix(bot, ctx)
        await ctx.send(f'Command syntax: `setprefix [prefix]`')
        
@bot.command()
async def prefix(ctx, *args):
    await ctx.send(f'The prefix for this server is `{get_prefix(bot, ctx)}`\nTo change the prefix use `setprefix [prefix]`')
    
bot.run(TOKEN)