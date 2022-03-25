# settings.py
"""Contains user settings commands"""

import asyncio

import discord
from discord.ext import commands

import database
from resources import emojis
from resources import settings
from resources import strings


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
    embed = await embed_user_settings(ctx)
    await ctx.respond(embed=embed)


async def command_set_progress(ctx: discord.ApplicationContext, timetravel: int, ascension: str) -> None:
    """Set progress command"""
    ascended = True if ascension == CHOICE_ASCENDED else False
    if timetravel > 25 and not ascended:
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
            f'Alright **{ctx.author.name}**, your progress is now set to **TT {user.tt}**, '
            f'**{"ascended" if user.ascended else "not ascended"}**.'
        )
    else:
        await ctx.respond('Welp, something went wrong here.', ephemeral=True)


# --- Embeds ---
async def embed_user_settings(ctx: commands.Context) -> discord.Embed:
    """User settings embed

    Raises
    ------
    sqlite3.Error if something happened during the query.
    """
    try:
        user = await database.get_user(ctx.author.id)
    except:
        raise
    settings_field = (
        f'{emojis.BP} Current run: **TT {user.tt}**\n'
        f'{emojis.BP} Ascension: **{"Ascended" if user.ascended else "Not ascended"}**'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
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