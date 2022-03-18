# links.py
"""Contains various commands with links"""

import discord
from discord.commands import slash_command
from discord.ext import commands

from resources import settings


class LinksCog(commands.Cog):
    """Cog with link commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description='Invite the bot to your server')
    async def invite(self, ctx: discord.ApplicationContext) -> None:
        """Invite link"""
        embed = discord.Embed(
            color = settings.EMBED_COLOR,
            title = 'NEED A GUIDE?',
            description = (
                f'I\'d be flattered to visit your server, **{ctx.author.name}**.\n'
                f'You can invite me [here]({settings.LINK_INVITE}).'
            )
        )
        await ctx.respond(embed=embed)

    @slash_command(description='Visit the support server')
    async def support(self, ctx: discord.ApplicationContext) -> None:
        """Link to the support server"""
        embed = discord.Embed(
            color = settings.EMBED_COLOR,
            title = 'NEED BOT SUPPORT?',
            description = f'You can visit the support server [here](https://discord.gg/v7WbhnhbgN).'
        )
        await ctx.respond(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(LinksCog(bot))