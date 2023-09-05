# celebration.py
"""Contains all celebration guides"""

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from content import celebration


class CelebrationCog(commands.Cog):
    """Cog with valentine commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_cel = SlashCommandGroup("cel", "Celebration event guide")

    @cmd_cel.command(name='guide', description='Celebrate good times, come on!')
    async def celebration_guide(
        self,
        ctx: discord.ApplicationContext,
    ) -> None:
        """Valentine guide"""
        await celebration.command_celebration_guide(ctx)


# Initialization
def setup(bot):
    bot.add_cog(CelebrationCog(bot))