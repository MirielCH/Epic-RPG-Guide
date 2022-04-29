# timetravel.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import timetravel as timetravel_content
from resources import strings


class TimeTravelCog(commands.Cog):
    """Cog with timetravel commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_time = SlashCommandGroup("time", "Time travel commands")
    cmd_travel = cmd_time.create_subgroup("travel", "Time travel sub commands")
    cmd_jump = cmd_time.create_subgroup("jump", "Time jump sub commands")

    @cmd_travel.command(name='guide', description='All you need to know about time travels and super time travels')
    async def timetravel_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION,
                           choices=timetravel_content.TOPICS, default=timetravel_content.TOPIC_TT),
    ) -> None:
        """Time travel guide"""
        await timetravel_content.command_time_travel_guide(ctx, topic)

    @cmd_travel.command(name='bonuses', description='Unlocks & bonuses of a certain time travel and how to prepare for it')
    async def timetravel_bonuses(
        self,
        ctx: discord.ApplicationContext,
        timetravel: Option(int, 'The TT you want to look up. Shows your current TT if empty.',
                           min_value=0, max_value=1000, default=None),
    ) -> None:
        """Time travel details"""
        await timetravel_content.command_time_travel_bonuses(ctx, timetravel=timetravel)

    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_jump.command(name='calculator', description='Calculates the theoretical time jump score of your inventory')
    async def tj_score_calculator(
        self,
        ctx: discord.ApplicationContext,
        area_no: Option(int, 'Your current area', min_value=1, max_value=21, choices=strings.CHOICES_AREA),
    ) -> None:
        await timetravel_content.command_tj_score_calculator(self.bot, ctx, area_no)


# Initialization
def setup(bot):
    bot.add_cog(TimeTravelCog(bot))