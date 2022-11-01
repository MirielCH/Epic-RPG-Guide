# duel.py
"""Contains duel commands"""

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import duel


class DuelCog(commands.Cog):
    """Cog with duel commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_duel = SlashCommandGroup("duel", "Duel weapons guide")

    # Commands
    @cmd_duel.command(name='weapons', description='What every weapon does in duels')
    async def duel_weapons(self, ctx: discord.ApplicationContext) -> None:
        """Duel weapons"""
        await duel.command_duel_weapons(ctx)

    """
    cmd_rewards = cmd_duel.create_subgroup("rewards", "Duel rewards subcommands")
    @cmd_rewards.command(name='calculator', description='Calculate the rewards you get from a duel')
    async def duel_rewards_calculator(
        self,
        ctx: discord.ApplicationContext,
        level: Option(int, 'The lower player level in the duel.',
                           min_value=1, max_value=999_999_999),
        donor: Option(str, 'The donor status you want to calculate for.', choices=duel.CHOICES_DONOR),
        timetravel: Option(int, 'The TT you want to calculate for. Uses your progress setting if empty.',
                           min_value=0, max_value=999, default=None),
        guild_bonus: Option(int, 'The guild bonus you want to calculate with. Reads from EPIC RPG if empty.',
                            min_value=0, max_value=999_999, default=None),
    ) -> None:
        # Duel rewards calculator
        # Revive this when the formulae work.
        # - coin formula is at least somewhat close but still too inaccurate.
        # - XP formula is not even in the same ballpark.
        # - Level formula makes no sense whatsoever because the level scaling is not included.
        await duel.command_duel_rewards_calculator(self.bot, ctx, level, donor, timetravel, guild_bonus)
    """

# Initialization
def setup(bot):
    bot.add_cog(DuelCog(bot))