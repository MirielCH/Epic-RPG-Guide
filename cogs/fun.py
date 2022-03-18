# fun.py
"""Contains some silly and useless fun commands"""

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

import database


class FunCog(commands.Cog):
    """Cog with silly and useless fun commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_ask = SlashCommandGroup("ask", "Just a silly fun command")
    cmd_the = cmd_ask.create_subgroup("the", "Subcommand of the ask command")

    # Commands
    @commands.cooldown(1, 5, commands.BucketType.user)
    @cmd_the.command(description='Ask the oracle any yes/no question! Just don\'t expect a useful answer.')
    async def oracle(self, ctx: discord.ApplicationContext, question: str) -> None:
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


# Initialization
def setup(bot):
    bot.add_cog(FunCog(bot))