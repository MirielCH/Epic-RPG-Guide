# duel.py
"""Contains duel commands"""

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from content import duel


class DuelCog(commands.Cog):
    """Cog with duel commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_duel = SlashCommandGroup("duel", "Duel commands")

    # Commands
    @cmd_duel.command(name='weapons', description='What every weapon does in duels')
    async def duel_weapons(self, ctx: discord.ApplicationContext) -> None:
        """Duel weapons"""
        await duel.command_duel_weapons(ctx)


# Initialization
def setup(bot):
    bot.add_cog(DuelCog(bot))