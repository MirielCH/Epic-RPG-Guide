# ultraining.py
"""Contains ultraining commands"""

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import ultraining


class UltrainingCog(commands.Cog):
    """Cog with silly and useless fun commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_ultraining = SlashCommandGroup("ultraining", "Ultraining guide and calculator")
    cmd_stats = cmd_ultraining.create_subgroup("stats", "Ultraining guide and calculator")

    # Commands
    @cmd_ultraining.command(name='guide', description='All about ultraining')
    async def ultraining_guide(self, ctx: discord.ApplicationContext) -> None:
        """Ultraining guide"""
        await ultraining.command_ultraining_guide(ctx)

    @cmd_stats.command(name='calculator', description='Calculates the stats for an ultraining stage')
    async def ultraining_stats_calculator(
        self,
        ctx: discord.ApplicationContext,
        stage: Option(int, 'The ultraining stage you want to calculate the stats for',
                      min_value=1, max_value=63_096)
        ) -> None:
        """Ultraining stats calculator"""
        await ultraining.command_ultraining_stats_calculator(ctx, stage)


# Initialization
def setup(bot):
    bot.add_cog(UltrainingCog(bot))