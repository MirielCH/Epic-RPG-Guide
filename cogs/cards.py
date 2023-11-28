# cards.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import cards
from resources import strings


class CardsCog(commands.Cog):
    """Cog with cards commands"""
    def __init__(self, bot):
        self.bot = bot

    # Commands
    cmd_cards = SlashCommandGroup("cards", "Cards guide")
    @cmd_cards.command(name='guide', description='Found a card? Here\'s what to do with it.')
    async def artifacts_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION,
                      choices=cards.TOPICS_CARDS, default=cards.TOPIC_OVERVIEW)
    ) -> None:
        """Cards guide"""
        await cards.command_cards_guide(ctx, topic)


# Initialization
def setup(bot):
    bot.add_cog(CardsCog(bot))