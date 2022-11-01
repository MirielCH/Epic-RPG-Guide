# easter.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import easter
from resources import strings


class EasterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    cmd_easter = SlashCommandGroup("easter", "Easter event guide")

    @cmd_easter.command(name='guide', description='Eggs! Eggs everywhere!')
    async def easter_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION,
                      choices=easter.TOPICS, default=easter.TOPIC_OVERVIEW),
    ) -> None:
        """Easter guide"""
        await easter.command_easter_guide(ctx, topic)


# Initialization
def setup(bot):
    bot.add_cog(EasterCog(bot))
