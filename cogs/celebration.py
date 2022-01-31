# celebration.py

import discord
from discord.ext import commands

import emojis
import global_data


# Celebration commands (cog)
class CelebrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "hal"
    @commands.command(aliases=('cel',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def celebration(self, ctx: commands.Context) -> None:
        """Celebration"""
        embed = await embed_celebration_overview(ctx.prefix)
        await ctx.send(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(CelebrationCog(bot))


# --- Embeds ---
async def embed_celebration_overview(prefix: str) -> discord.Embed:
    """Celebration overview embed"""
    activities = (
        f'{emojis.BP} Get {emojis.COIN_CELEBRATION} celebration coins in `hunt`, `adventure` and `fish` commands\n'
        f'{emojis.BP} Kill the rare celebration slime in `hunt` to get more coins\n'
        f'{emojis.BP} Complete the daily quest to get EVEN MORE coins\n'
        f'{emojis.BP} Increase your coins by 5% with `rpg cel multiply` (12h cooldown)\n'
        f'{emojis.BP} Get a big reward at the end of the event based on coins you gathered\n'
    )
    bonuses = (
        f'{emojis.BP} All cooldowns are reduced by 25%'
    )
    schedule = (
        f'{emojis.BP} Event started on October 18, 2021\n'
        f'{emojis.BP} Event ends on November 14, 2021, 23:55 UTC\n'
    )
    tldr_guide = (
        f'{emojis.BP} Complete the daily quest every day (`rpg cel dailyquest`)\n'
        f'{emojis.BP} Multiply your celebration coins every 12h (`rpg cel multiply`)\n'
        f'{emojis.BP} Use `rpg cel trade` to preview the rewards\n'
    )
    chances = (
        f'{emojis.BP} 20% to get coins with `hunt` (~ 50 {emojis.COIN_CELEBRATION})\n'
        f'{emojis.BP} 60% to get coins with `adventure` (~ 220 {emojis.COIN_CELEBRATION})\n'
        f'{emojis.BP} 35% to get coins with `fish` commands (~ 130 {emojis.COIN_CELEBRATION})\n'
        f'{emojis.BP} 0.25% to find the celebration slime in `hunt` (2,000 {emojis.COIN_CELEBRATION})\n'
    ) # 2020 values, unclear if still accurate
    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = f'500K CELEBRATION EVENT 2022 {emojis.COIN_CELEBRATION}',
        description = 'Yo hey, may I interest you in a godly lootbox?'
    )
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    # embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed