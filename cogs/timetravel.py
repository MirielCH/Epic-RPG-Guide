# timetravel.py

import discord
from discord.commands import SlashCommandGroup, Option, OptionChoice
from discord.ext import commands

from content import timetravel as timetravel_content
from resources import functions, strings


class TimeTravelCog(commands.Cog):
    """Cog with timetravel commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_tt = SlashCommandGroup("timetravel", "Timetravel commands")
    cmd_stt = SlashCommandGroup("stt", "Super timetravel commands")
    cmd_score = cmd_stt.create_subgroup("score", "Subcommand of the super timetravel command")

    @cmd_tt.command(name='guide', description='All you need to know about time travels and super time travels')
    async def timetravel_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION,
                           choices=timetravel_content.TOPICS, default=timetravel_content.TOPIC_TT),
    ) -> None:
        """Time travel guide"""
        await timetravel_content.command_timetravel_guide(ctx, topic)

    @cmd_tt.command(name='details', description='Unlocks & bonuses of a certain TT and how to prepare for it')
    async def timetravel_details(
        self,
        ctx: discord.ApplicationContext,
        timetravel: Option(int, 'The TT you want to look up. Shows your current TT if empty.',
                           min_value=1, max_value=1000, default=None),
    ) -> None:
        """Time travel details"""
        await timetravel_content.command_timetravel_details(ctx, timetravel=timetravel)

    @cmd_score.command(name='calculator', description='Calculates the theoretical score of your inventory')
    async def stt_score_calculator(
        self,
        ctx: discord.ApplicationContext,
        area_no: Option(int, 'Your current area', min_value=1, max_value=21, autocomplete=functions.area_choice),
    ) -> None:
        await timetravel_content.command_stt_score_calculator(self.bot, ctx, area_no)


# Initialization
def setup(bot):
    bot.add_cog(TimeTravelCog(bot))