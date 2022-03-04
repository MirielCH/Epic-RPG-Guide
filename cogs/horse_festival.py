# horse_festival.py

import discord
from discord.ext import commands

from resources import emojis
from resources import settings
from resources import functions


# easter event commands (cog)
class FestivalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "hf"
    @commands.command(aliases=('festival','horsefestival',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def hf(self, ctx: commands.Context, *args: str) -> None:
        """Horse festival overview"""
        embed = await embed_festival_overview(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "megarace"
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def megarace(self, ctx: commands.Context, *args: str) -> None:
        """Megarace guide"""
        embed = await embed_megarace(ctx.prefix)
        await ctx.send(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(FestivalCog(bot))


# --- Embeds ---
async def embed_festival_overview(prefix: str) -> discord.Embed:
    """Horse festival overview embed"""
    activities = (
        f'{emojis.BP} Get 25 {emojis.HORSESHOE} horseshoes each day in `hunt`, `adventure` and all fish command tiers\n'
        f'{emojis.BP} Get {emojis.HORSESHOE} horseshoes and {emojis.HORSESHOE_GOLDEN} golden horseshoes in the daily '
        f'and weekly **tasks** (see `rpg hf tasks`)\n'
        f'{emojis.BP} Play in the weekly **megarace** to get rewards (see `{prefix}megarace`)\n'
        f'{emojis.BP} Complete the event **quest** to get the {emojis.PET_PONY} pony pet (see `rpg hf quest`)\n'
        f'{emojis.BP} Buy stuff in the event shop (see `rpg hf shop`)\n'
    )
    bonuses = (
        f'{emojis.BP} Horse breed cooldown is reduced by 25%'
    )
    whattodo = (
        f'{emojis.BP} Do megarace whenever a stage is available\n'
        f'{emojis.BP} Complete tasks until you have 525 {emojis.HORSESHOE} and 8 {emojis.HORSESHOE_GOLDEN}\n'
        f'{emojis.BP} Melt 21 {emojis.STEEL} and 4 {emojis.GOLD} and craft the {emojis.HORSE_ARMOR} horse armor. '
        f'This will increase your luck in the megarace.\n'
        f'{emojis.BP} Complete the event quest and get showered in stuff'
    )
    schedule = (
        f'{emojis.BP} Event started on August 23, 2021\n'
        f'{emojis.BP} Event ended on September 12, 2021, 23:55 UTC\n'
        f'{emojis.BP} Items will vanish on September 19, 2021, with the exception of the {emojis.GODLY_HORSE_TOKEN} '
        f'GODLY horse token which you can use whenever you want'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'HORSE FESTIVAL EVENT 2021 {emojis.HORSE_T10}',
        description = 'Neigh.'
    )
    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='WHAT TO DO FIRST', value=whattodo, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)

    return embed


async def embed_megarace(prefix: str) -> discord.Embed:
    """Megarace embed"""
    spreadsheet = 'https://docs.google.com/spreadsheets/d/1Q9_Pon8RMdVGfdnFAdx3F5d_XeLd-ud7PZWezgXHCzM/edit#gid=0'
    overview = (
        f'{emojis.BP} Use `rpg hf megarace start` to start a stage\n'
        f'{emojis.BP} Every megarace has 9 stages and resets weekly\n'
        f'{emojis.BP} Every stage you will encounter 3 random events and have to choose what to do\n'
        f'{emojis.BP} The cooldown of the next stage depends on your answers\n'
    )
    best_answers_1 = (
        f'{emojis.BP} Ancient Racer: **C**\n'
        f'{emojis.BP} Annoying Racer: **B** (**C** for gamblers)\n'
        f'{emojis.BP} Asteroid: **A** (**C** for gamblers)\n'
        f'{emojis.BP} Black Hole: **C** (**A** for gamblers)\n'
        f'{emojis.BP} Bottleneck: **C**\n'
        f'{emojis.BP} Cliff: **B**\n'
        f'{emojis.BP} Cooldown: **A**\n'
        f'{emojis.BP} Dinosaur: **B**\n'
        f'{emojis.BP} EPIC Guards: **A** (**C** for gamblers)\n'
        f'{emojis.BP} Injured Racers: **C**\n'
        f'{emojis.BP} Legendary Boss: **C**\n'
        f'{emojis.BP} Many Horses: **B**\n'
    )
    best_answers_2 = (
        f'{emojis.BP} Mountains: **C** (**A** for gamblers)\n'
        f'{emojis.BP} Mysterious Racer: All answers are the same\n'
        f'{emojis.BP} Nothing: **C** (**A** for gamblers)\n'
        f'{emojis.BP} Party: **B** (**A** for gamblers)\n'
        f'{emojis.BP} Plane: **B**\n'
        f'{emojis.BP} Rainy: **A** (**C** for gamblers)\n'
        f'{emojis.BP} Sandstorm: **B** (**A** for gamblers)\n'
        f'{emojis.BP} Sleepy: **A** (**B** for gamblers)\n'
        f'{emojis.BP} Snowy: **C**\n'
        f'{emojis.BP} Team: **B**\n'
        f'{emojis.BP} The EPIC NPC: **C**\n'
        f'{emojis.BP} World Border: **A**\n'
        f'{emojis.BP} Zombie Horde: **B** (**C** for gamblers)\n'
    )

    note = (
        f'{emojis.BP} The answers for gamblers are better **if** you get lucky, otherwise they are worse\n'
        f'{emojis.BP} If you want to choose those, get a {emojis.HORSE_ARMOR} horse armor first\n'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MEGARACE',
        description = 'Hgien.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='OVERVIEW', value=overview, inline=False)
    embed.add_field(name='SHORTEST ANSWERS (1)', value=best_answers_1, inline=False)
    embed.add_field(name='SHORTEST ANSWERS (2)', value=best_answers_2, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed