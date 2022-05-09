# fun.py
"""Contains some silly and useless fun commands"""

import asyncio
from cgitb import text
import discord

import database
from resources import functions


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
    embed.set_author(icon_url=ctx.author.avatar.url, name=f'{ctx.author.name} is consulting the oracle')
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