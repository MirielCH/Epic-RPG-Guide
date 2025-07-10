# summer.py
"""Contains all summer guides"""

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import summer
from resources import strings


class SummerCog(commands.Cog):
    """Cog with summer event commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_summer = SlashCommandGroup("summer", "Summer event guide")

    @cmd_summer.command(name='guide', description='Sun, fun, and lots of stuff to do')
    async def summer_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION, choices=summer.TOPICS,
                      default=summer.TOPIC_OVERVIEW),
    ) -> None:
        """Summer guide"""
        await summer.command_summer_guide(ctx, topic)


# Initialization
def setup(bot):
    bot.add_cog(SummerCog(bot))