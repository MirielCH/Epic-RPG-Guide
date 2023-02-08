# valentine.py
"""Contains all valentine guides"""

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from content import valentine


class ValentineCog(commands.Cog):
    """Cog with valentine commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_valentine = SlashCommandGroup("valentine", "Valentine event guide")

    @cmd_valentine.command(name='guide', description='Love is in the aaaaaaiiiiirr')
    async def xmas_guide(
        self,
        ctx: discord.ApplicationContext,
    ) -> None:
        """Christmas guide"""
        await valentine.command_valentine_guide(ctx)


# Initialization
def setup(bot):
    bot.add_cog(ValentineCog(bot))
