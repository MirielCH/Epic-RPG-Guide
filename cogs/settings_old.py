# settings.py
"""Contains user and guild settings commands"""

from discord.ext import commands

import database
from resources import functions
from resources import strings


class SettingsOldCog(commands.Cog):
    """Cog user and guild settings commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Commands
    @commands.command(aliases=('setprefix',))
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(send_messages=True)
    async def prefix(self, ctx: commands.Context, *args: str) -> None:
        """Gets/sets new server prefix"""
        prefix = await database.get_prefix(ctx)
        message_syntax = (
            f'{strings.MSG_SYNTAX.format(syntax=f"{prefix}setprefix [prefix]")}\n\n'
            f'Tip: If you want to include a space, use "".\n'
            f'Example: `{prefix}setprefix "guide "`'
        )

        if args:
            if len(args) > 1:
                await ctx.send(message_syntax)
                return
            (new_prefix,) = args
            await database.set_prefix(ctx, new_prefix)
            await ctx.send(f'Prefix changed to `{await database.get_prefix(ctx)}`')
        else:
            await ctx.send(
                f'The prefix for this server is `{prefix}`\nTo change the prefix use '
                f'`{prefix}setprefix [prefix]`'
            )

    @commands.command(aliases=('me',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def settings(self, ctx: commands.Context) -> None:
        """Returns current user progress settings"""
        await functions.send_slash_migration_message(ctx, 'settings')

    @commands.command(aliases=('sp','setpr','setp',))
    @commands.bot_has_permissions(send_messages=True)
    async def setprogress(self, ctx: commands.Context, *args: str) -> None:
        """Sets user progress settings"""
        await functions.send_slash_migration_message(ctx, 'set progress')


# Initialization
def setup(bot):
    bot.add_cog(SettingsOldCog(bot))