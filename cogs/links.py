# links.py
"""Contains various commands with links"""

import discord
from discord.commands import slash_command
from discord.ext import commands

from content import links


class LinksCog(commands.Cog):
    """Cog with link commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description='Invite the bot to your server')
    async def invite(self, ctx: discord.ApplicationContext) -> None:
        """Invite link"""
        await links.command_invite(ctx)

    @slash_command(description='Visit the support server')
    async def support(self, ctx: discord.ApplicationContext) -> None:
        """Link to the support server"""
        await links.command_support(ctx)


# Initialization
def setup(bot):
    bot.add_cog(LinksCog(bot))