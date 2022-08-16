# monsters.py

import asyncio
from typing import Tuple

import discord
from discord.ext import commands
# from discord_components import Button, ButtonStyle, InteractionType

from resources import functions


# monsters commands (cog)
class MonstersOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Mobs list
    @commands.command(aliases=('monster','monsters','mob','monsterlist','monsterslist','moblist','mobslist',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def mobs(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'area guide')

    # Daily mob lookup
    @commands.command(aliases=('mobdaily','daily',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def dailymob(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'monster search')


# Initialization
def setup(bot):
    bot.add_cog(MonstersOldCog(bot))