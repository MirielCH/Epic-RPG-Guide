# celebration.py
"""Contains all celebration guides"""

import discord

from resources import emojis, settings, strings


# --- Commands ---
async def command_celebration_guide(ctx: discord.ApplicationContext) -> None:
    """Celebration guide command"""
    embed = await embed_celebration_guide()
    await ctx.respond(embed=embed)


# --- Embeds ---
async def embed_celebration_guide() -> discord.Embed:
    """Celebration guide embed"""
    activities = (
        f'{emojis.BP} Get {emojis.COIN_CELEBRATION} celebration coins in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} and fish commands\n'
        f'{emojis.BP} Kill the rare {emojis.PARTY_SLIME} party slime in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'to get more coins\n'
        f'{emojis.BP} Complete the `cel dailyquest` to get EVEN MORE coins (and an OP boost)\n'
        f'{emojis.BP} Increase your coins by with `cel multiply` '
        f'(`12`h cooldown)\n'
        f'{emojis.BP} Sacrifice some coins for a small reward with `cel sacrifice` '
        f'(`12`h cooldown)\n'
        f'{emojis.BP} Use `cel trade` between Sep 10 and Sep 17 to get a big reward '
        f'based on your total coin amount\n'
        f'{emojis.DETAIL} Use `cel trade` before Sep 10 to check possible rewards.\n'
    )
    tldr_guide = (
        f'{emojis.BP} Use `cel dailyquest` every day\n'
        f'{emojis.BP} Use `cel multiply` every `12` hours\n'
        f'{emojis.BP} Use `cel title` once you reach `1,000,000` '
        f'{emojis.COIN_CELEBRATION}\n'
        f'{emojis.BP} Use `cel trade` between Sep 10 and Sep 17 to get '
        f'your reward\n'
        f'{emojis.DETAIL} Try to be in A1-A5 when you claim your reward!\n'
    )
    bonuses = (
        f'{emojis.BP} All cooldowns except `daily` and `weekly` are reduced by `35`%'
    )
    titles = (
        f'{emojis.BP} **2,500,000** (use `cel title` at `1,000,000` '
        f'{emojis.COIN_CELEBRATION})\n'
        f'{emojis.DETAIL} Getting the title will **not** consume any coins!'
    )
    schedule = (
        f'{emojis.BP} Event started on September 4, 2023\n'
        f'{emojis.BP} Event ends on September 10, 2023, 23:55 UTC\n'
        f'{emojis.BP} Reward can be claimed until September 17, 23:55 UTC\n'
    )
    boost = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`80`% XP from all sources\n'
        f'{emojis.DETAIL2} +`80`% items from work commands\n'
        f'{emojis.DETAIL2} +`80`% coins from all sources except selling & miniboss\n'
        f'{emojis.DETAIL2} +`50`% lootbox drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.DETAIL2} +`50`% mob drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.DETAIL2} +`25`% item rarity from work commands\n'
        f'{emojis.DETAIL2} +`40` {emojis.STAT_AT} AT\n'
        f'{emojis.DETAIL2} +`40` {emojis.STAT_DEF} DEF\n'
        f'{emojis.DETAIL2} +`40` {emojis.STAT_LIFE} LIFE\n'
        f'{emojis.DETAIL} Automatically heals you if you take damage\n'
        f'{emojis.BP} **Duration**: `10`h\n'
    )
    chances = (
        f'{emojis.BP} 30% to get coins with `hunt`\n'
        f'{emojis.BP} 80% to get coins with `adventure`\n'
        f'{emojis.BP} 50% to get coins with `fish` commands\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'2,500,000 PLAYERS CELEBRATION 2023 {emojis.COIN_CELEBRATION}',
        description = 'There\'s a party goin\' on right here'
    )
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='TITLES', value=titles, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='IS THAT CELEBRATION BOOST ANY GOOD?', value=boost, inline=False)
    #embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed