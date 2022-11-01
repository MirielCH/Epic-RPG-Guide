# fun.py
"""Contains some silly and useless fun commands"""

import discord
from discord.commands import slash_command, Option, SlashCommandGroup
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
        await fun.command_oracle(self.bot, ctx, question)

    @slash_command(description='Complain about something because yes')
    async def complain(
        self,
        ctx: discord.ApplicationContext,
        complaint: Option(str, 'Your complaint', max_length=1000),
    ) -> None:
        """Complain"""
        await fun.command_complain(ctx, complaint)


# Initialization
def setup(bot):
    bot.add_cog(FunCog(bot))