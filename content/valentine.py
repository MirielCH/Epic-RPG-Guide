# valentine.py
"""Contains all valentine guides"""

import discord

from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_CHOCOLATE_BOX = 'Chocolate box artifact'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_CHOCOLATE_BOX,
]

# --- Commands ---
async def command_valentine_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Valentine guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_valentine_guide,
        TOPIC_CHOCOLATE_BOX: embed_chocolate_box,
    }
    view = views.TopicView(ctx, topics_functions, active_topic=topic)
    embed = await topics_functions[topic]()
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    try:
        await functions.edit_interaction(interaction, view=None)
    except discord.errors.NotFound:
        pass


# --- Embeds ---
async def embed_valentine_guide() -> discord.Embed:
    """Valentine guide embed"""
    activities = (
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["love share"]} to get {emojis.COIN_LOVE} love coins\n'
        f'{emojis.BP} Complete the {strings.SLASH_COMMANDS_EPIC_RPG["love quest"]} to get a '
        f'{emojis.PET_PINK_FISH} pink fish pet\n'
        f'{emojis.BP} Find the {emojis.ARTIFACT_CHOCOLATE_BOX} chocolate box artifact (see topic `Chocolate box`)\n'
        f'{emojis.BP} Kill the rare {emojis.MOB_PINK_WOLF} pink wolf in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'to get extra coins\n'
        f'{emojis.BP} Buy various rewards in the {strings.SLASH_COMMANDS_EPIC_RPG["love shop"]}\n'
        f'{emojis.BP} Gamble all your love coins away with {strings.SLASH_COMMANDS_EPIC_RPG["love slots"]}\n'
    )
    bonuses = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} cooldown is reduced by 25%\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} cooldown is reduced by 10% (**only if you are married**)\n'
    )
    love_tokens = (
        f'{emojis.BP} Love tokens are basically lootboxes with a special way of opening\n'
        f'{emojis.BP} To open these, use {strings.SLASH_COMMANDS_EPIC_RPG["love share"]} with a player '
        f'**who also has one**\n'
        f'{emojis.BP} If you **don\'t** want to open your token, use {strings.SLASH_COMMANDS_EPIC_RPG["love share"]} '
        f'`action: notokens`.\n'
        f'{emojis.DETAIL} Text version: `rpg love share @player notokens`.\n'
        f'{emojis.BP} You can only get these by completing the quest\n'
        f'{emojis.BP} Contains `15` {emojis.EPIC_COIN}, `80` {emojis.ARENA_COOKIE}, `6` {emojis.LB_EDGY}, `2` {emojis.LB_RARE}, '
        f'and resets `arena`, `dungeon` and `horse`\n'
    )
    love_share = (
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["love share"]} to ping another player\n'
        f'{emojis.BP} You need at least 1 {emojis.LIFE_POTION} life potion in your inventory\n'
        f'{emojis.BP} This command has the same cooldown as {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
    )
    titles = (
        f'{emojis.BP} **Wood you be my valentine?** (bought in {strings.SLASH_COMMANDS_EPIC_RPG["love shop"]})\n'
        f'{emojis.BP} **lovely fren** (Achievement #211)\n'
        f'{emojis.BP} **Heart broken** (Achievement #212)\n'
    )
    schedule = (
        f'{emojis.BP} Event started on February 9, 2024\n'
        f'{emojis.BP} Event ended on February 22, 2024, 23:55 UTC\n'
        f'{emojis.BP} Love tokens and coins can be used until February 29, 23:55 UTC\n'
    )
    tldr_guide = (
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["love share"]} after every hunt '
        f'to get {emojis.COIN_LOVE} love coins\n'
        f'{emojis.BP} Complete the {strings.SLASH_COMMANDS_EPIC_RPG["love quest"]} to unlock the '
        f'{emojis.PET_PINK_FISH} pink fish pet\n'
        f'{emojis.BP} Use your coins for whatever you want in {strings.SLASH_COMMANDS_EPIC_RPG["love shop"]}\n'
    )
    boost = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL} +`15`% XP from all sources\n'
        f'{emojis.DETAIL} +`10`% items from work commands\n'
        f'{emojis.DETAIL} +`5`% profession XP\n'
        f'{emojis.DETAIL} +`100` {emojis.STAT_LIFE} LIFE\n'
        f'{emojis.BP} **Duration**: `1`h\n'
    )
    chances = (
        f'{emojis.BP} `0.5`% to find the {emojis.MOB_PINK_WOLF} pink wolf in `hunt`\n'
        f'{emojis.BP} The chance is increased to `1`% if the world buff from the shop is active\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'VALENTINE EVENT 2024 {emojis.COIN_LOVE}',
        description = 'Voulez-vous trinquer avec moi, ce soir ?'
    )
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='TITLES', value=titles, inline=False)
    embed.add_field(name='HOW LOVE SHARING WORKS', value=love_share, inline=False)
    embed.add_field(name=f'WHAT TO DO WITH {emojis.TOKEN_LOVE} LOVE TOKENS', value=love_tokens, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='OK, BUT WHAT DOES THE VALENTINE BOOST DO?', value=boost, inline=False)
    #embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed


async def embed_chocolate_box() -> discord.Embed:
    """Chocolate box artifact embed"""
    effects = (
        f'{emojis.BP} Doubles rewards from {strings.SLASH_COMMANDS_EPIC_RPG["love share"]}\n'
        f'{emojis.BP} Reduces {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} cooldown by `2`%\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_CHOCOLATE_BOX_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["love share"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_CHOCOLATE_BOX_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["love slots"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_CHOCOLATE_BOX_PART_C} `Part C` • Drops from buying items in the '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["love shop"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'CHOCOLATE BOX {emojis.ARTIFACT_CHOCOLATE_BOX}',
        description = 'This artifact is only available during the valentine event!',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed