# anniversary.py

import discord
from discord.ext import commands

from resources import emojis
from resources import functions, settings


class AnniversaryCog(commands.Cog):
    """Cog with anniversary commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=('anni',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def anniversary(self, ctx: commands.Context) -> None:
        """Anniversary"""
        embed = await embed_anniversary_overview(ctx.prefix)
        await ctx.send(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(AnniversaryCog(bot))


# --- Embeds ---
async def embed_anniversary_overview(prefix: str) -> discord.Embed:
    """Anniversary overview embed"""
    activities = (
        f'{emojis.BP} Duel other players to get {emojis.LB_ANNIVERSARY} anniversary lootboxes\n'
        f'{emojis.DETAIL} You do **not** lose these lootboxes when TTing\n'
    )
    bonuses = (
        f'{emojis.BP} Command cooldowns except `vote`, `guild`, `daily`, `weekly` are reduced by 50%\n'
        f'{emojis.DETAIL} This lowers by 10% per day of the event\n'
    )
    lb_content = (
        f'{emojis.BP} 1 {emojis.PET_HAMSTER} hamster pet (max 1 in the event)\n'
        f'{emojis.DETAIL} The chance to get the pet increases each time you don\'t get it\n'
        f'{emojis.BP} 1 {emojis.LB_GODLY} GODLY lootbox\n'
        f'{emojis.BP} 1 {emojis.LB_OMEGA} OMEGA lootbox\n'
        f'{emojis.BP} 3 or 5 {emojis.LB_EDGY} EDGY lootboxes\n'
        f'{emojis.BP} 350 {emojis.ARENA_COOKIE} arena cookies\n'
        f'{emojis.BP} 15 {emojis.EPIC_COIN} EPIC coins\n'
        f'{emojis.BP} 1 {emojis.STAT_COOLNESS} coolness\n'
    )
    schedule = (
        f'{emojis.BP} Event started on March 15, 2022\n'
        f'{emojis.BP} Event ends on March 20, 2022, 18:00 UTC\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'ANNIVERSARY EVENT 2022 {emojis.LB_ANNIVERSARY}',
        description = '[It\'s...](https://www.youtube.com/watch?v=SFkdcQgNJHo)'
    )
    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='POSSIBLE LOOTBOX CONTENT', value=lb_content, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed