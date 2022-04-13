# enchanting.py

import discord

from resources import emojis, settings


# --- Commands ---
async def command_enchanting_guide(ctx: discord.ApplicationContext) -> None:
    """Enchanting guide command"""
    embed = await embed_enchanting()
    await ctx.respond(embed=embed)


# --- Embeds ---
async def embed_enchanting() -> discord.Embed:
    """Enchanting"""
    buffs = (
        f'{emojis.BP} **Normie** - 5% buff\n'
        f'{emojis.BP} **Good** - 15% buff\n'
        f'{emojis.BP} **Great** - 25% buff\n'
        f'{emojis.BP} **Mega** - 40% buff\n'
        f'{emojis.BP} **Epic** - 60% buff\n'
        f'{emojis.BP} **Hyper** - 70% buff\n'
        f'{emojis.BP} **Ultimate** - 80% buff\n'
        f'{emojis.BP} **Perfect** - 90% buff\n'
        f'{emojis.BP} **EDGY** - 95% buff\n'
        f'{emojis.BP} **ULTRA-EDGY** - 100% buff\n'
        f'{emojis.BP} **OMEGA** - 125% buff, unlocked in {emojis.TIME_TRAVEL} TT 1\n'
        f'{emojis.BP} **ULTRA-OMEGA** - 150% buff, unlocked in {emojis.TIME_TRAVEL} TT 3\n'
        f'{emojis.BP} **GODLY** - 200% buff, unlocked in {emojis.TIME_TRAVEL} TT 5\n'
        f'{emojis.BP} **VOID** - 300% buff, unlocked in {emojis.TIME_TRAVEL} TT 15\n'
    )
    commands_tiers = (
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/enchant`: area 2+, rolls `1 * TT multiplier` enchants\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/refine`: area 7+, rolls `10 * TT multiplier` enchants\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/transmute`: area 13+, rolls `100 * TT multiplier` enchants\n'
        f'{emojis.BP} {emojis.EPIC_RPG_LOGO_SMALL}`/transcend`: area 15+, rolls `1,000 * TT multiplier` enchants'
    )
    how_enchanting_works = (
        f'{emojis.BP} Each command rolls a certain amount of enchants\n'
        f'{emojis.BP} The resulting enchant is the highest enchant that got rolled\n'
        f'{emojis.BP} Higher command tiers increase the amount of rolls\n'
    )
    enchant_cost = (
        f'{emojis.BP} The enchant cost is `1k * amount of rolls * area * TT multiplier`\n'
    )
    multiplier = (
        f'{emojis.BP} The multiplier increases the amount of rolls of all command tiers\n'
        f'{emojis.BP} The multiplier increases with {emojis.TIME_TRAVEL} TT\n'
        f'{emojis.BP} More rolls also means higher cost!\n'
        f'{emojis.BP} You can check your current multiplier with `rpg time travel`\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ENCHANTING GUIDE',
        description = (
            f'Enchants buff either AT or DEF (sword enchants buff AT, armor enchants buff DEF). Enchants buff your **overall** stats.\n'
            f'The chance to get better enchants can be increased by leveling up the enchanter profession and having a {emojis.HORSE_T8} T8+ horse.\n'
            f'See the [Wiki](https://epic-rpg.fandom.com/wiki/Enchant) for **base** chance estimates.'
        )
    )
    embed.add_field(name='POSSIBLE ENCHANTS', value=buffs, inline=False)
    embed.add_field(name='HOW ENCHANTING WORKS', value=how_enchanting_works, inline=False)
    embed.add_field(name='COMMAND TIERS', value=commands_tiers, inline=False)
    embed.add_field(name='ENCHANT COST', value=enchant_cost, inline=False)
    embed.add_field(name='TT MULTIPLIER', value=multiplier, inline=False)
    return embed

