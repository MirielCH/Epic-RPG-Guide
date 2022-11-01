# halloween.py
"""Contains all halloween guides"""

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import halloween
from resources import strings


class HalloweenCog(commands.Cog):
    """Cog with halloween commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_halloween = SlashCommandGroup("halloween", "Halloween event guide")

    @cmd_halloween.command(name='guide', description='Halloween guide. Spppoooookkyy!')
    async def halloween_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION, choices=halloween.TOPICS,
                      default=halloween.TOPIC_OVERVIEW),
    ) -> None:
        """Halloween guide"""
        await halloween.command_halloween_guide(ctx, topic)


# Initialization
def setup(bot):
    bot.add_cog(HalloweenCog(bot))
