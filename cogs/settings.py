# settings.py
"""Contains user and guild settings commands"""

import asyncio

import discord
from discord.ext import commands

import database
import emojis
import global_data


class SettingsCog(commands.Cog):
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
            f'{global_data.MSG_SYNTAX.format(syntax=f"{prefix}setprefix [prefix]")}\n\n'
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
        embed = await embed_user_settings(ctx)
        await ctx.send(embed=embed)

    @commands.command(aliases=('sp','setpr','setp',))
    @commands.bot_has_permissions(send_messages=True)
    async def setprogress(self, ctx: commands.Context, *args: str) -> None:
        """Sets user progress settings"""
        def check(m):
            return (m.author == ctx.author) and (m.channel == ctx.channel)

        user_name = ctx.author.name

        async def set_progress(new_tt: int, new_ascended: str) -> None:
            """Sends new settings to the database"""
            await database.set_progress(ctx, new_tt, new_ascended)
            try:
                user_settings = await database.get_user_settings(ctx)
            except Exception as error:
                if isinstance(error, database.FirstTimeUser):
                    return
                else:
                    await ctx.send(global_data.MSG_ERROR)
                    return
            user_tt, user_ascended = user_settings
            await ctx.send(
                f'Alright **{user_name}**, your progress is now set to **TT {user_tt}**, '
                f'**{user_ascended}**.'
            )

        prefix = ctx.prefix
        invoked = ctx.invoked_with
        ascension = {
                    'ascended': 'ascended',
                    'asc': 'ascended',
                    'yes': 'ascended',
                    'y': 'ascended',
                    'no': 'not ascended',
                    'not': 'not ascended',
                    'n': 'not ascended'
                    }
        message_syntax = (
            f'The command syntax is `{prefix}{invoked} [0-999]` or `{prefix}{invoked} [0-999] asc` '
            f'if you\'re ascended.\n'
            f'You can also use `{prefix}{invoked}` and let me ask you.\n\n'
            f'Examples: `{prefix}{invoked} tt5`, `{prefix}{invoked} 8 asc`'
            )

        if args:
            args = [arg.lower() for arg in args]
            arg_tt, *arg_ascended = args
            try:
                new_tt = int(arg_tt.replace('tt',''))
            except:
                await ctx.send(message_syntax)
                return
            if not 0 <= new_tt <= 999:
                await ctx.send(message_syntax)
                return
            if arg_ascended:
                arg_ascended, *_ = arg_ascended
                new_ascended = ascension.get(arg_ascended, None)
                if new_ascended is None:
                    await ctx.send(message_syntax)
                    return
                if (new_ascended == 'ascended') and (new_tt == 0):
                    await ctx.send(f'**{user_name}**, you can not ascend in TT 0.')
                    return
            else:
                new_ascended = 'not ascended'
            await set_progress(new_tt, new_ascended)
            return
        try:
            await ctx.send(
                f'**{user_name}**, what **TT** are you currently in? '
                f'`[0-999]` (type `abort` to abort).'
            )
            answer_tt = await self.bot.wait_for('message', check=check, timeout=30)
            answer_tt = answer_tt.content.lower()
            if answer_tt in ('abort', 'cancel'):
                await ctx.send(global_data.MSG_ABORTING)
                return
            try:
                new_tt = int(answer_tt)
            except:
                await ctx.send(
                    f'**{user_name}**, you didn\'t answer with a valid number. Aborting.'
                )
                return
            if new_tt not in range(0, 1000):
                await ctx.send(
                    f'**{user_name}**, you didn\'t enter a number from 0 to 999. Aborting.'
                )
                return
            await ctx.send(
                f'**{user_name}**, are you **ascended**? `[yes/no]` '
                f'(type `abort` to abort)'
            )
            answer_ascended = await self.bot.wait_for('message', check=check, timeout=30)
            answer_ascended = answer_ascended.content.lower()
            if answer_ascended in ('abort', 'cancel'):
                await ctx.send(global_data.MSG_ABORTING)
                return
            new_ascended = ascension.get(answer_ascended, None)
            if new_ascended is None:
                await ctx.send(
                    f'**{user_name}**, you didn\'t answer with `yes` or `no`. '
                    f'Aborting.'
                )
                return
            await set_progress(new_tt, new_ascended)
            return
        except asyncio.TimeoutError as error:
            await ctx.send(
                f'**{user_name}**, you took too long to answer, RIP.\n\n'
                f'Tip: You can also use `{prefix}{invoked} [0-999]` or '
                f'`{prefix}{invoked} [0-999] asc` if you\'re ascended.'
            )
            return


# Initialization
def setup(bot):
    bot.add_cog(SettingsCog(bot))


# --- Embeds ---
async def embed_user_settings(ctx: commands.Context) -> discord.Embed:
    """User settings embed"""
    try:
        user_settings = await database.get_user_settings(ctx)
    except Exception as error:
        if isinstance(error, database.FirstTimeUser):
            return
        else:
            await ctx.send(global_data.MSG_ERROR)
            return
    user_tt, user_ascension = user_settings
    settings_field = (
        f'{emojis.BP} Current run: **TT {user_tt}**\n'
        f'{emojis.BP} Ascension: **{user_ascension.capitalize()}**'
    )
    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'USER SETTINGS',
        description = (
            f'Hey there, **{ctx.author.name}**.\n'
            f'These settings are used by some guides to tailor the information to your '
            f'current progress.'
        )
    )
    embed.set_footer(text=f'Tip: Use {ctx.prefix}setprogress to change your settings.')
    embed.add_field(name='YOUR CURRENT SETTINGS', value=settings_field, inline=False)
    return embed