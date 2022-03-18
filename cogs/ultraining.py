# ultraining.py
"""Contains ultraining commands"""

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from resources import emojis, settings, strings


class UltrainingCog(commands.Cog):
    """Cog with silly and useless fun commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_ultraining = SlashCommandGroup("ultraining", "Ultraining commands")

    # Commands
    @cmd_ultraining.command(name='guide', description='All about ultraining')
    async def ultraining_guide(self, ctx: discord.ApplicationContext) -> None:
        """Ultraining guide"""
        embed = await embed_ultraining_guide()
        await ctx.respond(embed=embed)

    @cmd_ultraining.command(name='calculator', description='Calculates the EPIC NPC damage in ultraining')
    async def ultraining_calculator(
        self,
        ctx: discord.ApplicationContext,
        stage: Option(int, 'The ultraining stage you want to calculate the damage of',
                      min_value=1, max_value=63_096)
        ) -> None:
        """Ultraining stage calculator"""
        npc_at_base = 5 * (stage ** 1.25)
        npc_def_base = 6 * (stage ** 1.25)
        answer = (
            f'Estimated EPIC NPC stats at stage **{stage:,}**:\n'
            f'{emojis.STAT_AT} AT: **{round(npc_at_base * 0.9):,} - {round(npc_at_base * 1.1):,}**\n'
            f'{emojis.STAT_DEF} DEF: **{round(npc_def_base * 0.9):,} - {round(npc_def_base * 1.1):,}**\n'
        )
        await ctx.respond(answer)


# Initialization
def setup(bot):
    bot.add_cog(UltrainingCog(bot))


# --- Embeds ---
async def embed_ultraining_guide():
    """Ultraining guide"""
    how_it_works = (
        f'{emojis.BP} The EPIC NPC appears with stats depending on the stage\n'
        f'{emojis.BP} You have to choose between `ATTACK`, `BLOCK` and `ATTLOCK`\n'
        f'{emojis.BP} You win or lose depending on your stats vs the EPIC NPC\'s stats\n'
        f'{emojis.BP} If you win, the stage increases by +1 the next time\n'
        f'{emojis.BP} Stages never reset\n'
        f'{emojis.BP} You can use `rpg ultr p` to check your progress\n'
    )
    which_command = (
        f'{emojis.BP} The exact impact of the chosen answer is unknown\n'
        f'{emojis.BP} However, it seems that it doesn\'t matter at all\n'
    )
    when = (
        f'{emojis.BP} It is recommended to wait until {emojis.TIME_TRAVEL} TT 25+\n'
    )
    preparation = (
        f'{emojis.BP} Get VOID enchants\n'
        f'{emojis.BP} Get a MAGIC horse\n'
        f'{emojis.BP} Craft as many {emojis.FOOD_APPLE_JUICE} apple juice and {emojis.FOOD_ORANGE_JUICE} orange juice '
        f'you need to reach your desired stage\n'
        f'{emojis.BP} Duel on cooldown to increase your level\n'
    )
    rewards = (
        f'{emojis.BP} 2 {emojis.STAT_COOLNESS} coolness per win\n'
        f'{emojis.BP} XP (depends on your TT and your area)\n'
        f'{emojis.BP} Note: You can **not** get pets in ultraining\n'
    )
    calculators = (
        f'{emojis.BP} `/ultraining calculator`: Calculate EPIC NPC damage in ultraining\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ULTRAINING',
        description = (
            f'Ultraining is a higher tier of training that is unlocked in area 12. It rewards coolness in addition to XP.\n'
            f'It is the main source of coolness which you need for dungeon 15-2.'
        )
    )
    embed.set_footer(text=strings.DEFAULT_FOOTER)
    embed.add_field(name='HOW IT WORKS', value=how_it_works, inline=False)
    embed.add_field(name='ATTACK, BLOCK OR ATTLOCK?', value=which_command, inline=False)
    embed.add_field(name='WHEN TO DO ULTRAINING', value=when, inline=False)
    embed.add_field(name='PREPARING FOR ULTRAINING', value=preparation, inline=False)
    embed.add_field(name='REWARDS', value=rewards, inline=False)
    embed.add_field(name='CALCULATOR', value=calculators, inline=False)
    return embed