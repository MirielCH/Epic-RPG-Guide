# fun.py
"""Contains some silly and useless fun commands"""

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from content import fun


class FunCog(commands.Cog):
    """Cog with silly and useless fun commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_ask = SlashCommandGroup("ask", "Just a silly fun command")
    cmd_the = cmd_ask.create_subgroup("the", "Subcommand of the ask command")

    # Commands
    @commands.cooldown(1, 5, commands.BucketType.user)
    @cmd_the.command(description='Ask the oracle any yes/no question! Just don\'t expect a useful answer.')
    async def oracle(self, ctx: discord.ApplicationContext, question: str) -> None:
        """Ask the oracle (and get nonsense in return)"""
        await fun.command_oracle(ctx, question)


# Initialization
def setup(bot):
    bot.add_cog(FunCog(bot))