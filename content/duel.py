# duel.py
"""Contains duel commands"""

import asyncio
from math import floor

import discord

import database
from resources import emojis, functions, settings, strings


CHOICES_DONOR = [
    'Non-donor',
    'Donor',
]

# --- Commands ---
async def command_duel_weapons(ctx: discord.ApplicationContext) -> None:
    """Command duel weapons"""
    embed = await embed_duel_weapons()
    await ctx.respond(embed=embed)


"""
async def command_duel_rewards_calculator(bot: discord.Bot, ctx: discord.ApplicationContext, level: int, donor: str,
                                          timetravel: int, guild_bonus: int) -> None:
    #Duel rewards calculator.

    #Revive this when the formulae work.
    #- coin formula is at least somewhat close but still too inaccurate.
    #- XP formula is not even in the same ballpark.
    #- Level formula makes no sense whatsoever because the level scaling is not included.

    donor_multi = 2 if donor == 'Donor' else 1
    if guild_bonus is None:
        content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                          command=strings.SLASH_COMMANDS_EPIC_RPG[f"guild stats"])
        bot_message_task = asyncio.ensure_future(functions.wait_for_guild_message(bot, ctx))
        try:
            bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
        except asyncio.TimeoutError:
            await ctx.respond(
                strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='guild'),
                ephemeral=True
            )
            return
        if bot_message is None: return
        guild_bonus = (
            await functions.extract_duel_bonus_from_guild_embed(ctx, bot_message)
        )
    if timetravel is None:
        user: database.User = await database.get_user(ctx.author.id)
        timetravel = user.tt

    tt_bonus = (99 + timetravel) * timetravel / 4
    reward_coin = (125 / 6 * level ** 2) * (1 + guild_bonus / 100) * donor_multi
    reward_xp = (((125 / 20 * level ** 2) * (1 + guild_bonus / 100)) + (1 + tt_bonus)) * donor_multi
    reward_levels = (0.05 * (1 + guild_bonus / 100) + (1 + tt_bonus / 100)) * donor_multi
    description = (
        f'{emojis.BP} Player level: **{level:,}**\n'
        f'{emojis.BP} TT: {emojis.TIME_TRAVEL} **{timetravel}**\n'
        f'{emojis.BP} Guild duel bonus: **{guild_bonus} %**\n'
        f'{emojis.BP} Donor state: **{donor}**\n'
    )
    rewards = (
        f'{emojis.BP} ~**{floor(reward_coin):,}** {emojis.COIN}\n'
        f'{emojis.BP} ~**{floor(reward_xp):,}** XP\n'
    )
    note = (
        f'{emojis.BP} These are approximations. The actual results might vary slightly.'
    )
    embed = discord.Embed(title='DUEL REWARDS CALCULATOR', description=description)
    embed.add_field(name='REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    await ctx.respond(embed=embed)
"""

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
    embed.add_field(name='DUELLING WEAPONS', value=weapons, inline=False)
    embed.add_field(name='RANDOMNESS', value=randomness, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed