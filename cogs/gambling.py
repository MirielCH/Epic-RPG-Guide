# gambling.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import gambling
from resources import strings


class GamblingCog(commands.Cog):
    """Cog with gambling commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_gambling = SlashCommandGroup("gambling", "Gambling guides")

    @cmd_gambling.command(name='guide', description='Gambling guide')
    async def gambling_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION, choices=gambling.TOPICS),
    ) -> None:
        """Gambling guides"""
        await gambling.command_gambling_guide(ctx, topic)


# Initialization
def setup(bot):
    bot.add_cog(GamblingCog(bot))
