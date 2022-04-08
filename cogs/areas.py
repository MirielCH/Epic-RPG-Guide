# areas.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import areas
from resources import strings


class AreasCog(commands.Cog):
    """Cog with area commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_area = SlashCommandGroup("area", "Area commands")

    @cmd_area.command(name='guide', description='Guide for certain areas')
    async def area_guide(
        self,
        ctx: discord.ApplicationContext,
        area_no: Option(int, 'The area you want a guide for', name='area',
                        min_value=1, max_value=21, choices=strings.CHOICES_AREA),
        length: Option(str, 'The guide length you want to see. Short only shows the most important points.',
                      choices=strings.CHOICES_AREA_GUIDES),
        timetravel: Option(int, 'The TT you want to see the guide for. Uses your progress setting if empty.',
                           min_value=0, max_value=999, default=None),
        ascension: Option(str, 'The ascension you want to see the guide for. Uses your progress setting if empty.',
                           choices=strings.CHOICES_ASCENSION, default=None),

    ) -> None:
        """Dropchance calculator"""
        await areas.command_area_guide(ctx, area_no, timetravel, ascension, length)


# Initialization
def setup(bot):
    bot.add_cog(AreasCog(bot))