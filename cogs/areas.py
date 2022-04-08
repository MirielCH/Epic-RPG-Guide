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

    @cmd_area.command(name='guide', description='What to do and what you need in all areas')
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
        """Area guide"""
        await areas.command_area_guide(ctx, area_no, timetravel, ascension, length)

    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_area.command(name='check', description='Check how much damage you take in an area')
    async def area_check(
        self,
        ctx: discord.ApplicationContext,
        area_no: Option(int, 'The area you want to check for', name='area',
                        min_value=1, max_value=21, choices=strings.CHOICES_AREA),
        user_at: Option(int, 'Your AT. Reads from EPIC RPG if empty.', name='at', min_value=1, default=None),
        user_def: Option(int, 'Your DEF. Reads from EPIC RPG if empty.', name='def', min_value=1, default=None),
        user_life: Option(int, 'Your LIFE. Reads from EPIC RPG if empty.', name='life', min_value=100, default=None),
    ) -> None:
        """Area check"""
        await areas.command_area_check(self.bot, ctx, area_no, user_at, user_def, user_life)


# Initialization
def setup(bot):
    bot.add_cog(AreasCog(bot))