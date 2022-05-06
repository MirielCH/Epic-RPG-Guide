# enchanting.py

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from content import enchanting


class EnchantingCog(commands.Cog):
    """Cog with enchanting commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_enchanting = SlashCommandGroup(
        "enchanting",
        "Enchanting commands",
    )

    @cmd_enchanting.command(name='guide', description='All enchants & how enchanting works')
    async def enchanting_guide(self, ctx: discord.ApplicationContext) -> None:
        """Enchanting guide"""
        await enchanting.command_enchanting_guide(ctx)


# Initialization
def setup(bot):
    bot.add_cog(EnchantingCog(bot))