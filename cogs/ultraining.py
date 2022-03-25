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

    cmd_ultraining = SlashCommandGroup("ultraining", "Ultraining commands")

    # Commands
    @cmd_ultraining.command(name='guide', description='All about ultraining')
    async def ultraining_guide(self, ctx: discord.ApplicationContext) -> None:
        """Ultraining guide"""
        await ultraining.command_ultraining_guide(ctx)

    @cmd_ultraining.command(name='calculator', description='Calculates the EPIC NPC damage in ultraining')
    async def ultraining_calculator(
        self,
        ctx: discord.ApplicationContext,
        stage: Option(int, 'The ultraining stage you want to calculate the damage of',
                      min_value=1, max_value=63_096)
        ) -> None:
        """Ultraining stage calculator"""
        await ultraining.command_ultraining_calculator(ctx, stage)


# Initialization
def setup(bot):
    bot.add_cog(UltrainingCog(bot))