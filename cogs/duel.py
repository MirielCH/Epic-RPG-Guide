# duel.py
"""Contains duel commands"""

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from resources import emojis, settings, strings


class DuelCog(commands.Cog):
    """Cog with silly and useless fun commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_duel = SlashCommandGroup("duel", "Duel commands")

    # Commands
    @cmd_duel.command(name='weapons', description='What every weapon does in duels')
    async def duel_weapons(self, ctx: discord.ApplicationContext) -> None:
        """Duel weapons"""
        embed = await embed_duel_weapons()
        await ctx.respond(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(DuelCog(bot))


# --- Embeds ---
async def embed_duel_weapons() -> discord.Embed:
    """Embed duel weapons"""
    weapons = (
        f'{emojis.BP} {emojis.DUEL_AT}{emojis.DUEL_AT} - **AT**\n'
        f'{emojis.BP} {emojis.DUEL_DEF}{emojis.DUEL_DEF} - **DEF**\n'
        f'{emojis.BP} {emojis.DUEL_LIFE}{emojis.DUEL_LIFE} - **LIFE**\n'
        f'{emojis.BP} {emojis.DUEL_LEVEL}{emojis.DUEL_LEVEL} - **LEVEL**\n'
        f'{emojis.BP} {emojis.DUEL_COINS}{emojis.DUEL_COINS} - **Coins** (incl. bank account)\n'
        f'{emojis.BP} {emojis.DUEL_GEAR}{emojis.DUEL_GEAR} - **Gear** (both sword and armor)\n'
        f'{emojis.BP} {emojis.DUEL_ENCHANTS}{emojis.DUEL_ENCHANTS} - **Enchants** (both sword and armor)'
    )
    randomness = (
        f'{emojis.BP} Every duel score gets multiplied by 0.75 ~ 1.25\n'
        f'{emojis.BP} Thus the duel outcome can be highly unexpected'
    )
    note = (
        f'{emojis.BP} Unless you are really rich, don\'t choose coins/cards.\n'
        f'{emojis.BP} If you don\'t choose a weapon, your opponent will automatically win.\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'DUELS',
        description = 'Winning a duel depends on the chosen weapon and some luck.'
    )
    embed.set_footer(text=strings.DEFAULT_FOOTER)
    embed.add_field(name='DUELLING WEAPONS', value=weapons, inline=False)
    embed.add_field(name='RANDOMNESS', value=randomness, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed