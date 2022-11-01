# fun.py
"""Contains some silly and useless fun commands"""

import asyncio

import discord
from discord.embeds import EmptyEmbed

import database
from resources import emojis, functions, settings


# --- Commands ---
async def command_oracle(bot: discord.Bot, ctx: discord.ApplicationContext, question: str) -> None:
    """Ask the oracle (and get nonsense in return)"""
    if len(question) > 250:
        await ctx.respond('Can you stop with these overly long questions, Jesus Christ, for real.')
        return
    answer: database.OracleAnswer = await database.get_oracle_answer()
    embed = discord.Embed(
        title = question,
        description = answer.answer if answer.answer is not None else discord.Embed.Empty
    )
    if ctx.author.avatar is not None:
        icon_url = ctx.author.avatar.url
    else:
        icon_url = EmptyEmbed
    embed.set_author(icon_url=icon_url, name=f'{ctx.author.name} is consulting the oracle')
    if answer.image_url is not None:
        embed.set_image(url=answer.image_url)
    await ctx.respond(embed=embed)
    if answer.answer is not None and ctx.guild_id is not None:
        if 'y u ignore me' in answer.answer.lower():
            try:
                bot_message = await functions.wait_for_fun_message(bot, ctx)
            except asyncio.TimeoutError:
                return
            if bot_message is None: return
            await ctx.respond('Did you... seriously just try this :eyes:')


async def command_complain(ctx: discord.ApplicationContext, complaint: str) -> None:
    """Complain"""
    image, embed = await embed_complain(ctx, complaint)
    await ctx.respond(embed=embed, file=image)


# --- Embeds ---
async def embed_complain(ctx: discord.ApplicationContext, complaint: str) -> discord.Embed:
    """Complaint embed"""
    complaint = (
        f'{complaint}\n\n'
        f'**THIS IS UNACCEPTABLE!** {emojis.SAD_ANGRY}\n\n'
        f'**BRING ME THE MANAGER!** {emojis.PEPE_ANGRY_POLICE}\n\n'
        f'**I DEMAND MY MONEY BACK!** {emojis.PEPE_TABLESLAM}\n\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'{ctx.author.name} IS COMPLAINING'.upper(),
        description = complaint
    )
    image = discord.File(settings.IMG_CRANKY, filename='cranky.png')
    image_url = 'attachment://cranky.png'
    embed.set_thumbnail(url=image_url)
    return (image, embed)
