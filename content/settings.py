# settings.py
"""Contains user settings commands"""

import asyncio

import discord
from discord.ext import commands

import database
from resources import emojis, functions, settings, views


# --- Choices ---
CHOICE_ASCENDED = 'Ascended'
CHOICE_NOT_ASCENDED = 'Not ascended'

CHOICES_ASCENSION = [
    CHOICE_ASCENDED,
    CHOICE_NOT_ASCENDED,
]


# --- Commands ---
async def command_settings(ctx: discord.ApplicationContext) -> None:
    """Settings command"""
    user_settings = await database.get_user(ctx.author.id)
    view = views.SettingsUserView(ctx,user_settings, embed_user_settings)
    embed = await embed_user_settings(ctx, user_settings)
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()


async def command_set_progress(ctx: discord.ApplicationContext, timetravel: int, ascension: str) -> None:
    """Set progress command"""
    ascended = True if ascension == CHOICE_ASCENDED else False
    if timetravel >= 25 and not ascended:
        await ctx.respond(
            f'Invalid combination. You can\'t set yourself as not ascended if you are {emojis.TIME_TRAVEL} TT 25+.',
            ephemeral=True
        )
        return
    if timetravel == 0 and ascended:
        await ctx.respond(
            f'Invalid combination. You can\'t ascend in {emojis.TIME_TRAVEL} TT 0.',
            ephemeral=True
        )
        return
    user = await database.get_user(ctx.author.id)
    await user.update(tt=timetravel, ascended=ascended)
    if user.tt == timetravel and user.ascended == ascended:
        await ctx.respond(
            f'Alright **{ctx.author.name}**, your progress is now set to **TT {user.tt:,}**, '
            f'**{"ascended" if user.ascended else "not ascended"}**.'
        )
    else:
        await ctx.respond('Welp, something went wrong here.', ephemeral=True)


async def command_purge_data(bot: discord.Bot, ctx: discord.ApplicationContext) -> None:
    """Purge data command"""
    user_settings = await database.get_user(ctx.author.id)
    answer_aborted = f'**{ctx.author.global_name}**, phew, was worried there for a second.'
    answer = (
        f'{emojis.CHECK_WARN} **{ctx.author.global_name}**, this will purge all your data from Epic RPG Guide {emojis.CHECK_WARN}\n\n'
        f'You will of course be able to start using Epic RPG Guide again, but you will have to reregister.\n'
        f'Are you **SURE**?'
    )
    view = views.ConfirmCancelView(ctx)
    interaction = await ctx.respond(answer, view=view)
    view.interaction = interaction
    await view.wait()
    if view.value is None:
        await functions.edit_interaction(interaction, content=f'**{ctx.author.name}**, you didn\'t answer in time.',
                                         view=None)
    elif view.value == 'confirm':
        cur = database.ERG_DB.cursor()
        await functions.edit_interaction(
            interaction, content='Purging data...',
            view=None
        )
        cur.execute('DELETE FROM users WHERE user_id=?', (ctx.author.id,))
        await asyncio.sleep(1)
        await functions.edit_interaction(
            interaction,
            content=(
                f'{emojis.ENABLED} **{ctx.author.global_name}**, you are now gone and forgotton. '
                f'Thanks for using me!'
            ),
            view=None
        )   
    else:
        await functions.edit_interaction(
            interaction, content=answer_aborted, view=None
        )


# --- Embeds ---
async def embed_user_settings(ctx: commands.Context, user_settings: database.User) -> discord.Embed:
    """User settings embed

    Raises
    ------
    sqlite3.Error if something happened during the query.
    """
    ascended = 'Ascended' if user_settings.ascended else 'Not ascended'
    quick_trade = f'{emojis.ENABLED}`Enabled`' if user_settings.quick_trade_enabled else f'{emojis.DISABLED}`Disabled`'
    settings_field = (
        f'{emojis.BP} **Current TT**: `{user_settings.tt:,}`\n'
        f'{emojis.BP} **Ascension**: `{ascended}`\n'
    )
    settings_calculators = (
        f'{emojis.BP} **Quick trade calculator**: {quick_trade}\n'
        f'{emojis.DETAIL} _Can be used with `rpg i <area>`_\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'USER SETTINGS',
        description = (
            f'Hey there, **{ctx.author.name}**.\n'
            f'Use the menu below to change your settings!'
        )
    )
    embed.set_footer(text='Tip: You can also use "/set progress" to change progress settings.')
    embed.add_field(name='PROGRESS', value=settings_field, inline=False)
    embed.add_field(name='CALCULATORS', value=settings_calculators, inline=False)
    return embed