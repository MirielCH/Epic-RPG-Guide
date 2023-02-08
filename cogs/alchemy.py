# alchemy.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import alchemy
import database
from resources import functions, strings


ALL_ITEMS = functions.await_coroutine(database.get_all_items())


class AlchemyCog(commands.Cog):
    """Cog with alchemy commands"""
    def __init__(self, bot):
        self.bot = bot

    # Commands
    cmd_alchemy = SlashCommandGroup("alchemy", "Alchemy guide")
    @cmd_alchemy.command(name='guide', description='Potions? Potions!')
    async def alchemy_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION,
                      choices=alchemy.TOPICS_ALCHEMY, default=alchemy.TOPIC_OVERVIEW)
    ) -> None:
        """Alchemy guide"""
        await alchemy.command_alchemy_guide(ctx, topic)


# Initialization
def setup(bot):
    bot.add_cog(AlchemyCog(bot))
