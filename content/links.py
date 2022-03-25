# links.py
"""Contains various commands with links"""

import discord

from resources import settings


# --- Commands ---
async def command_invite(ctx: discord.ApplicationContext) -> discord.Embed:
    """Invite command"""
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'NEED A GUIDE?',
        description = (
            f'I\'d be flattered to visit your server!\n'
            f'You can invite me [here]({settings.LINK_INVITE}).'
        )
    )
    await ctx.respond(embed=embed)


async def command_support(ctx: discord.ApplicationContext) -> discord.Embed:
    """Support command"""
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'NEED BOT SUPPORT?',
        description = f'You can visit the support server [here](https://discord.gg/v7WbhnhbgN).'
    )
    await ctx.respond(embed=embed)