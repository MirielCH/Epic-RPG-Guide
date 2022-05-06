# horse.py
"""Contains all horse related guides and calculators"""

import asyncio

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import horse
from resources import strings


class HorseCog(commands.Cog):
    """Cog with horse commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_horse = SlashCommandGroup("horse", "Horse commands")
    cmd_boost = cmd_horse.create_subgroup("boost", "Boost subcommand of the horse command")
    cmd_training = cmd_horse.create_subgroup("training", "Training subcommand of the horse command")

    @cmd_horse.command(name='guide', description='All you need to know about horses')
    async def horse_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION, choices=horse.TOPICS, default=horse.TOPIC_OVERVIEW),
    ) -> None:
        """Horse guides"""
        await horse.command_horse_guide(ctx, topic)

    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_boost.command(name='calculator', description='Calculates the horse boost for all types')
    async def horse_boost_calculator(
        self,
        ctx: discord.ApplicationContext,
        horse_tier: Option(int, 'The horse tier you want to calculate for. Reads from EPIC RPG if empty.',
                           min_value=1, max_value=10, default=None),
        horse_level: Option(int, 'The horse level you want to calculate for. Reads from EPIC RPG if empty.',
                            min_value=1, max_value=140, default=None),
    ) -> None:
        """Horse boost calculator"""
        await horse.command_boost_calculator(self.bot, ctx, horse_tier=horse_tier, horse_level=horse_level)

    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_training.command(name='calculator', description='Calculates the horse training cost')
    async def horse_training_calculator(
        self,
        ctx: discord.ApplicationContext,
        horse_tier: Option(int, 'The horse tier you want to calculate for. Reads from EPIC RPG if empty.',
                           min_value=1, max_value=10, default=None),
        from_level: Option(int, 'The horse level you want to calculate from. Reads from EPIC RPG if empty.',
                           min_value=1, max_value=139, default=None),
        to_level: Option(int, 'The horse level you want to calculate to. Uses the max possible level if empty.',
                         min_value=1, max_value=140, default=None),
        lootboxer_level: Option(int, 'Level of your lootboxer profession. Reads from EPIC RPG if empty.',
                                min_value=1, max_value=140, default=None),
    ) -> None:
        """Horse training calculator"""
        await horse.command_horse_training_calculator(self.bot, ctx, horse_tier=horse_tier, from_level=from_level,
                                                      to_level=to_level, lootboxer_level=lootboxer_level)


# Initialization
def setup(bot):
    bot.add_cog(HorseCog(bot))
