# links.py
"""Contains various commands with links"""

from discord.ext import commands

from resources import functions


# Links
LINK_EROS = 'https://discord.gg/w5dej5m'
LINK_SUPPORT_SERVER = 'https://discord.gg/v7WbhnhbgN'
LINK_VOTE = 'https://top.gg/bot/770199669141536768/vote'
LINK_WIKI = 'https://epic-rpg.fandom.com/wiki/EPIC_RPG_Wiki'


class LinksOldCog(commands.Cog):
    """Cog with link commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Commands
    @commands.command(aliases=('inv',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def invite(self, ctx: commands.Context) -> None:
        """Sends the invite link"""
        await functions.send_slash_migration_message(ctx, 'help')

    @commands.command(aliases=('supportserver','server',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def support(self, ctx: commands.Context) -> None:
        """Link to the support server"""
        await functions.send_slash_migration_message(ctx, 'help')

    @commands.command(aliases=('link','wiki',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def links(self, ctx: commands.Context) -> None:
        """Links to wiki, servers, top.gg and invite"""
        await functions.send_slash_migration_message(ctx, 'about')

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def donate(self, ctx: commands.Context) -> None:
        """Much love"""
        await ctx.send(
            f'Aw that\'s nice of you but this is a free bot, you know.\n'
            f'Thanks though :heart:'
        )


# Initialization
def setup(bot):
    bot.add_cog(LinksOldCog(bot))