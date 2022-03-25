# titles.py


import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands

from content import titles


class TitlesCog(commands.Cog):
    """Cog with title/achievement commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_title = SlashCommandGroup(
        "title",
        "Title search commands",
    )

    @cmd_title.command(name='search', description='Look up titles / achievements')
    async def title_search(
        self,
        ctx: discord.ApplicationContext,
        search_string: Option(str, 'Achievement ID or part of the title / achievement'),
    ) -> None:
        """Command to search for a title/achievement"""
        await titles.command_title_search(ctx, search_string)


# Initialization
def setup(bot):
    bot.add_cog(TitlesCog(bot))