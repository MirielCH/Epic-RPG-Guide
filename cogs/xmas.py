# xmas.py
"""Contains all christmas guides"""

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import xmas
from resources import strings


class ChristmasCog(commands.Cog):
    """Cog with christmas commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_xmas = SlashCommandGroup("xmas", "Christmas event guide")

    @cmd_xmas.command(name='guide', description='Christmas guide. Ho ho ho!')
    async def xmas_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION, choices=xmas.TOPICS,
                      default=xmas.TOPIC_OVERVIEW),
    ) -> None:
        """Christmas guide"""
        await xmas.command_xmas_guide(ctx, topic)

    @cmd_xmas.command(name='items', description='All christmas items explained')
    async def xmas_items(
        self,
        ctx: discord.ApplicationContext,
        item: Option(str, 'The item you want to read about', choices=xmas.ITEMS),
    ) -> None:
        """Christmas items guide"""
        await xmas.command_xmas_items(ctx, item)


# Initialization
def setup(bot):
    bot.add_cog(ChristmasCog(bot))
