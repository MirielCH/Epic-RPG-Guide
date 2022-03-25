# misc.py

import asyncio

import discord
from discord.commands import slash_command, SlashCommandGroup, Option
from discord.ext import commands

from content import misc
import database
from resources import functions, strings


class MiscCog(commands.Cog):
    """Cog with miscellanous commands"""
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @slash_command(description='All current redeemable codes')
    async def codes(self, ctx: discord.ApplicationContext) -> None:
        """Codes"""
        await misc.command_codes(ctx)

    @slash_command(description='All badges and how to unlock them')
    async def badges(self, ctx: discord.ApplicationContext) -> None:
        """Badges"""
        await misc.command_badges(ctx)

    cmd_coolness = SlashCommandGroup("coolness", "Coolness commands")
    @cmd_coolness.command(name='guide', description='How to get coolness')
    async def coolness_guide(self, ctx: discord.ApplicationContext) -> None:
        """Coolness guide"""
        await misc.command_coolness_guide(ctx)

    cmd_farming = SlashCommandGroup("farming", "Farming commands")
    @cmd_farming.command(name='guide', description='How farming works and what do with crops')
    async def farming_guide(self, ctx: discord.ApplicationContext) -> None:
        """Farming guide"""
        await misc.command_farming_guide(ctx)

    cmd_beginner = SlashCommandGroup("beginner", "Beginner commands")
    @cmd_beginner.command(name='guide', description='How to start in the game')
    async def beginner_guide(self, ctx: discord.ApplicationContext) -> None:
        """Beginner guide"""
        await misc.embed_beginner_guide(ctx)

    @slash_command(description='A handy dandy random tip')
    async def tip(
        self,
        ctx: discord.ApplicationContext,
        id: Option(int, 'ID of a specific tip. Returns a random tip if empty.', min_value=1,
                   max_value=1000, default=None)
        ) -> None:
        """Tip"""
        await misc.command_tip(ctx, id)

    @slash_command(description='A basic calculator for your mathematical needs')
    async def calculator(
        self,
        ctx: discord.ApplicationContext,
        calculation: Option(str, 'The calculation you want solved')
        ) -> None:
        """Basic calculator"""
        await misc.command_calculator(ctx, calculation)

    cmd_coincap = SlashCommandGroup("coincap", "Coincap commands")
    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_coincap.command(name='calculator', description='Calculate the coin cap for a TT/area')
    async def coincap_calculator(
        self,
        ctx: discord.ApplicationContext,
        timetravel: Option(int, 'The TT you want to calculate for. Reads from EPIC RPG if empty.',
                           min_value=1, max_value=999, default=None),
        area_no: Option(int, 'The area you want to calculate for. Reads from EPIC RPG if empty.', name='area',
                        min_value=1, max_value=20, default=None),
    ) -> None:
        await misc.command_coincap_calculator(self.bot, ctx, timetravel=timetravel, area_no=area_no)


# Initialization
def setup(bot):
    bot.add_cog(MiscCog(bot))