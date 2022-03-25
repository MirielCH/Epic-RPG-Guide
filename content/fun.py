# fun.py
"""Contains some silly and useless fun commands"""

import discord

import database


# --- Commands ---
async def command_oracle(ctx: discord.ApplicationContext, question: str) -> None:
    """Ask the oracle (and get nonsense in return)"""
    if len(question) > 250:
        await ctx.respond('Can you stop with these overly long questions, keep it brief, will ya?')
        return
    answer: database.OracleAnswer = await database.get_oracle_answer()
    embed = discord.Embed(
        title = question,
        description = answer.answer if answer.answer is not None else discord.Embed.Empty
    )
    if answer.image_url is not None:
        embed.set_image(url=answer.image_url)
    await ctx.respond(embed=embed)