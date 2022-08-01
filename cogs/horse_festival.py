# horse_festival.py
"""Contains all horse festival guides"""

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import horse_festival
from resources import strings


class HorseFestivalCog(commands.Cog):
    """Cog with horse commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_horse_festival = SlashCommandGroup("hf", "Horse festival commands")

    @cmd_horse_festival.command(name='guide', description='Horse festival guide. Neigh!')
    async def horse_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION, choices=horse_festival.TOPICS,
                      default=horse_festival.TOPIC_OVERVIEW),
    ) -> None:
        """Horse festival guide"""
        await horse_festival.command_horse_festival_guide(ctx, topic)


# Initialization
def setup(bot):
    bot.add_cog(HorseFestivalCog(bot))
