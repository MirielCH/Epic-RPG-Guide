# professions.py

import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands

from content import professions
from resources import strings


class ProfessionsCog(commands.Cog):
    """Cog with profession commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_profession = SlashCommandGroup("profession", "Profession commands")

    @cmd_profession.command(name='guide', description='All you need to know about professions')
    async def professions_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION,
                      choices=professions.TOPICS, default=professions.TOPIC_OVERVIEW),
    ) -> None:
        """Profession guide"""
        await professions.command_profession_guide(ctx, topic)


    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_profession.command(name='calculator', description='Calculates what you need to level up your professions')
    async def profession_calculator(
        self,
        ctx: discord.ApplicationContext,
        profession: Option(str, 'The profession you want to calculate for. Reads from EPIC RPG if empty.',
                           choices=strings.PROFESSIONS, default=None),
        from_level: Option(int, 'The profession level you want to calculate from. Reads from EPIC RPG if empty.',
                           min_value = 1, max_value = 200, default=None),
        to_level: Option(int, 'The profession level you want to calculate a total for. Uses 100 if empty.',
                         min_value = 2, max_value = 200, default=100),
    ) -> None:
        """Profession calculator"""
        await professions.command_profession_calculator(self.bot, ctx, profession=profession, from_level=from_level,
                                                        to_level=to_level)


# Initialization
def setup(bot):
    bot.add_cog(ProfessionsCog(bot))