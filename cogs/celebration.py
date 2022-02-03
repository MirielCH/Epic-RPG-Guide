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
        f'{emojis.BP} Kill the rare party slime in `hunt` to get more coins\n'
        f'{emojis.BP} Complete the daily quest to get EVEN MORE coins\n'
        f'{emojis.BP} Increase your coins by 5% with `rpg cel multiply` (12h cooldown)\n'
        f'{emojis.BP} Unlock the title **500,000** title with `rpg cel title` at 250,000 coins\n'
        f'{emojis.BLANK} This does **not** use up the coins\n'
        f'{emojis.BP} Get a big reward at the end of the event based on coins you gathered\n'
    )
    bonuses = (
        f'{emojis.BP} All cooldowns except `daily` and `weekly` are reduced by 25%'
    )
    schedule = (
        f'{emojis.BP} Event started on February 1, 2022\n'
        f'{emojis.BP} Event ends on February 5, 2022, 23:55 UTC\n'
        f'{emojis.BP} Reward can be claimed until February 7, 2022, 23:55 UTC\n'
    )
    tldr_guide = (
        f'{emojis.BP} Complete the daily quest every day (`rpg cel dailyquest`)\n'
        f'{emojis.BP} Multiply your celebration coins every 12h (`rpg cel multiply`)\n'
        f'{emojis.BP} Get the event title with `rpg cel title` once you reach 250,000 coins\n'
        f'{emojis.BP} Use `rpg cel trade` to get your reward after February 5\n'
        f'{emojis.BLANK} Tip: Try to be in A1-A5 when you get the reward\n'
    )
    chances = (
        f'{emojis.BP} 30% to get coins with `hunt`\n'
        f'{emojis.BP} 80% to get coins with `adventure`\n'
        f'{emojis.BP} 50% to get coins with `fish` commands\n'
    )
    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = f'500K CELEBRATION EVENT 2022 {emojis.COIN_CELEBRATION}',
        description = 'Yo hey, may I interest you in a godly lootbox?'
    )
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed