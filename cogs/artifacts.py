# artifacts.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import artifacts
import database
from resources import functions, strings


ALL_ITEMS = functions.await_coroutine(database.get_all_items())


class ArtifactsCog(commands.Cog):
    """Cog with artifacts commands"""
    def __init__(self, bot):
        self.bot = bot

    # Commands
    cmd_alchemy = SlashCommandGroup("artifacts", "Artifacts guide")
    @cmd_alchemy.command(name='guide', description='Artifacts? Sounds fancy!')
    async def artifacts_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION,
                      choices=artifacts.TOPICS_ARTIFACTS, default=artifacts.TOPIC_OVERVIEW)
    ) -> None:
        """Artifacts guide"""
        await artifacts.command_artifacts_guide(ctx, topic)


# Initialization
def setup(bot):
    bot.add_cog(ArtifactsCog(bot))
