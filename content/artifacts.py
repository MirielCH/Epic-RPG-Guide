# alchemy.py

import discord

from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_ARTIFACTS_SOURCE_SUMMARY = 'Source summary'
TOPIC_ARTIFACTS_CLAUS_BELT = 'Claus belt'
TOPIC_ARTIFACTS_COIN_RING = 'Coin ring'
TOPIC_ARTIFACTS_GOLDEN_PAN = 'Golden pan'
TOPIC_ARTIFACTS_MASTER_KEY = 'Master key'
TOPIC_ARTIFACTS_POCKET_WATCH = 'Pocket watch'
TOPIC_ARTIFACTS_TOP_HAT = 'Top hat'
TOPIC_ARTIFACTS_VAMPIRE_TEETH = 'Vampire teeth'

TOPICS_ARTIFACTS = [
    TOPIC_OVERVIEW,
    TOPIC_ARTIFACTS_SOURCE_SUMMARY,
    TOPIC_ARTIFACTS_CLAUS_BELT,
    TOPIC_ARTIFACTS_COIN_RING,
    TOPIC_ARTIFACTS_GOLDEN_PAN,
    TOPIC_ARTIFACTS_MASTER_KEY,
    TOPIC_ARTIFACTS_POCKET_WATCH,
    TOPIC_ARTIFACTS_VAMPIRE_TEETH,
    TOPIC_ARTIFACTS_TOP_HAT,
]


# --- Commands ---
async def command_artifacts_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Artifacts command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_artifacts_overview,
        TOPIC_ARTIFACTS_SOURCE_SUMMARY: embed_artifacts_source_summary,
        TOPIC_ARTIFACTS_CLAUS_BELT: embed_artifacts_claus_belt,
        TOPIC_ARTIFACTS_COIN_RING: embed_artifacts_coin_ring,
        TOPIC_ARTIFACTS_GOLDEN_PAN: embed_artifacts_golden_pan,
        TOPIC_ARTIFACTS_MASTER_KEY: embed_artifacts_master_key,
        TOPIC_ARTIFACTS_POCKET_WATCH: embed_artifacts_pocket_watch,
        TOPIC_ARTIFACTS_TOP_HAT: embed_artifacts_top_hat,
        TOPIC_ARTIFACTS_VAMPIRE_TEETH: embed_artifacts_vampire_teeth,
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
async def embed_artifacts_overview() -> discord.Embed:
    """Artifacts guide overview"""
    overview = (
        f'{emojis.BP} Artifacts are rare items that unlock unique benefits\n'
        f'{emojis.DETAIL} These benefits are permanent!\n'
        f'{emojis.BP} Finished artifacts show up on your profile\n'
    )
    how_to_get = (
        f'{emojis.BP} To craft an artifact, you need to find all its parts (see topics below)\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["artifacts"]} to see the status of your artifacts\n'
        f'{emojis.BP} The chance to get artifacts parts increases with your time travel\n'
        f'{emojis.DETAIL} Check {strings.SLASH_COMMANDS_GUIDE["time travel bonuses"]} to see the numbers\n'
        f'{emojis.BP} Once you get all parts of an artifact, you can {strings.SLASH_COMMANDS_EPIC_RPG["craft"]} it\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ARTIFACTS GUIDE',
        description = 'Want artifacts? Pray to RNGesus. That is all.'
    )
    embed.add_field(name='WHAT ARE ARTIFACTS?', value=overview, inline=False)
    embed.add_field(name='HOW TO GET THEM', value=how_to_get, inline=False)
    return embed


async def embed_artifacts_top_hat() -> discord.Embed:
    """Top hat guide"""
    effects = (
        f'{emojis.BP} Increases the inventory item cap to `25b` per item\n'
        f'{emojis.BP} Unlocks a random daily trade in {strings.SLASH_COMMANDS_EPIC_RPG["trade list"]}\n'
        f'{emojis.DETAIL2} The daily trade is not affected by area changes\n'
        f'{emojis.DETAIL2} The current daily trade is random for each player\n'
        f'{emojis.DETAIL} The daily trade amount is limited and increases with time travels\n'
    )
    possible_trades = (
        f'{emojis.BP} 1 {emojis.LOG} ➜ 4 {emojis.FISH}\n'
        f'{emojis.BP} 1 {emojis.LOG} ➜ 2 {emojis.APPLE}\n'
        f'{emojis.BP} 25 {emojis.LOG} ➜ 1 {emojis.RUBY}\n'
        f'{emojis.BP} 1 {emojis.FISH} ➜ 12 {emojis.LOG}\n'
        f'{emojis.BP} 1 {emojis.APPLE} ➜ 50 {emojis.LOG}\n'
        f'{emojis.BP} 1 {emojis.RUBY} ➜ 1,000 {emojis.LOG}\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_TOP_HAT_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'in areas 3, 5 and TOP\n'
        f'{emojis.BP} {emojis.ARTIFACT_TOP_HAT_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'in areas 3, 5 and TOP\n'
        f'{emojis.BP} {emojis.ARTIFACT_TOP_HAT_PART_C} `Part C` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["trade items"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'TOP HAT {emojis.ARTIFACT_TOP_HAT}',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='POSSIBLE DAILY TRADES', value=possible_trades, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed


async def embed_artifacts_claus_belt() -> discord.Embed:
    """Claus belt artifact embed"""
    effects = (
        f'{emojis.BP} Increases chances to get better presents from {strings.SLASH_COMMANDS_EPIC_RPG["xmas chimney"]}\n'
        f'{emojis.BP} Doubles rewards from {strings.SLASH_COMMANDS_EPIC_RPG["xmas chimney"]}\n'
        f'{emojis.BP} Halves the chance to get stuck in {strings.SLASH_COMMANDS_EPIC_RPG["xmas chimney"]}\n'
        f'{emojis.BP} Increases lootbox drop chance by `5`%\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_CLAUS_BELT_PART_A} `Part A` • Drops from beating the area 0 dungeon\n'
        f'{emojis.BP} {emojis.ARTIFACT_CLAUS_BELT_PART_B} `Part B` • Drops from opening presents\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'CLAUS BELT {emojis.ARTIFACT_CLAUS_BELT}',
        description = 'This artifact is only available during the christmas event!',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed


async def embed_artifacts_coin_ring() -> discord.Embed:
    """Coin ring guide"""
    effects = (
        f'{emojis.BP} Upgrades your bank with a chance to get double drops\n'
        f'{emojis.DETAIL2} Affects drops in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} and '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.DETAIL} This is applied **after** the T10 horse drop chance boost\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_COIN_RING_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["sell"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_COIN_RING_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["slots"]} '
        f'(wins only, more coins = higher chance)\n'
        f'{emojis.BP} {emojis.ARTIFACT_COIN_RING_PART_C} `Part C` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["buy"]} '
        f'(lootboxes only)\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'COIN RING {emojis.ARTIFACT_COIN_RING}',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed


async def embed_artifacts_golden_pan() -> discord.Embed:
    """Golden pan guide"""
    effects = (
        f'{emojis.BP} Lets you keep a percentage of cooked stats when time traveling\n'
        f'{emojis.DETAIL} The percentage increases with time travels\n'
        f'{emojis.BP} Increases the cooking item cap to `1m` per command\n'
        f'{emojis.BP} Grants the ability to brew potions already active\n'
        f'{emojis.DETAIL} This will refresh their duration, not add time\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_GOLDEN_PAN_PART_A} `Part A` • Drops from level ups (except from cooking)\n'
        f'{emojis.BP} {emojis.ARTIFACT_GOLDEN_PAN_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["cook"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'GOLDEN PAN {emojis.ARTIFACT_GOLDEN_PAN}',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed


async def embed_artifacts_master_key() -> discord.Embed:
    """Master key guide"""
    effects = (
        f'{emojis.BP} Skips 1 single player dungeon (11-14) each time travel\n'
        f'{emojis.DETAIL2} The skipped dungeon randomly changes when time traveling\n'
        f'{emojis.DETAIL} Check {strings.SLASH_COMMANDS_EPIC_RPG["artifacts"]} to see your skipped dungeon\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_MASTER_KEY_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["dungeon"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_MASTER_KEY_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'in areas 11-15\n'
        f'{emojis.BP} {emojis.ARTIFACT_MASTER_KEY_PART_C} `Part C` • Drops from enchant commands\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'MASTER KEY {emojis.ARTIFACT_MASTER_KEY}',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed


async def embed_artifacts_pocket_watch() -> discord.Embed:
    """Pocket watch guide"""
    effects = (
        f'{emojis.BP} Doubles the duration of all boosts\n'
        f'{emojis.BP} Unlocks a personal cooldown reduction\n'
        f'{emojis.DETAIL2} Increases with time travels (up to `5`%)\n'
        f'{emojis.DETAIL} Your current reduction is shown in {strings.SLASH_COMMANDS_EPIC_RPG["artifacts"]}\n'
    )
    affected_commands = (
        f'{emojis.BP} `adventure`\n'
        f'{emojis.BP} `arena`\n'
        f'{emojis.BP} `dungeon` / `miniboss`\n'
        f'{emojis.BP} `farm`\n'
        f'{emojis.BP} `horse breed`\n'
        f'{emojis.BP} `hunt`\n'
        f'{emojis.BP} `quest` / `epic quest`\n'
        f'{emojis.BP} `training`\n'
        f'{emojis.BP} `chop`, `fish`, `pickup` and `mine` commands\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_POCKET_WATCH_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["pets claim"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_POCKET_WATCH_PART_B} `Part B` • Drops from time travels and time capsules\n'
        f'{emojis.BP} {emojis.ARTIFACT_POCKET_WATCH_PART_C} `Part C` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["forge"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_POCKET_WATCH_PART_D} `Part D` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["weekly"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_POCKET_WATCH_PART_E} `Part E` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'in the TOP\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'POCKET WATCH {emojis.ARTIFACT_POCKET_WATCH}',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='AFFECTED COMMANDS', value=affected_commands, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed

async def embed_artifacts_vampire_teeth() -> discord.Embed:
    """Vampire teeth guide"""
    effects = (
        f'{emojis.BP} Increases rewards from {strings.SLASH_COMMANDS_EPIC_RPG["hal boo"]}\n'
        f'{emojis.BP} Increases monster drop chance by `5`%\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_VAMPIRE_TEETH_PART_A} `Part A` • Drops from the {emojis.HAL_BOSS} pumpkin bat '
        f'(scroll boss)\n'
        f'{emojis.BP} {emojis.ARTIFACT_VAMPIRE_TEETH_PART_B} `Part B` • Drops from '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["hal boo"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_VAMPIRE_TEETH_PART_C} `Part C` • Drops from joining a '
        f'{emojis.HAL_SLEEPYNT_JACK_O_LANTERN} sleepyn\'t jack-o-lantern miniboss\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'VAMPIRE TEETH {emojis.ARTIFACT_VAMPIRE_TEETH}',
        description = 'This artifact is only available during the halloween event!',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed


async def embed_artifacts_source_summary() -> discord.Embed:
    """Artifacts sources"""
    claus_belt = (
        f'{emojis.ARTIFACT_CLAUS_BELT_PART_A} `Part A` • Drops from beating the area 0 dungeon\n'
        f'{emojis.ARTIFACT_CLAUS_BELT_PART_B} `Part B` • Drops from opening presents\n'
    )
    coin_ring = (
        f'{emojis.ARTIFACT_COIN_RING_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["sell"]}\n'
        f'{emojis.ARTIFACT_COIN_RING_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["slots"]} '
        f'(wins only, more coins = higher chance)\n'
        f'{emojis.ARTIFACT_COIN_RING_PART_C} `Part C` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["buy"]} '
        f'(lootboxes only)\n'
    )
    golden_pan = (
        f'{emojis.ARTIFACT_GOLDEN_PAN_PART_A} `Part A` • Drops from level ups (except from cooking)\n'
        f'{emojis.ARTIFACT_GOLDEN_PAN_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["cook"]}\n'
    )
    master_key = (
        f'{emojis.ARTIFACT_MASTER_KEY_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["dungeon"]}\n'
        f'{emojis.ARTIFACT_MASTER_KEY_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'in areas 11-15\n'
        f'{emojis.ARTIFACT_MASTER_KEY_PART_C} `Part C` • Drops from enchant commands\n'
    )
    pocket_watch = (
        f'{emojis.ARTIFACT_POCKET_WATCH_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["pets claim"]}\n'
        f'{emojis.ARTIFACT_POCKET_WATCH_PART_B} `Part B` • Drops from time travels and time capsules\n'
        f'{emojis.ARTIFACT_POCKET_WATCH_PART_C} `Part C` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["forge"]}\n'
        f'{emojis.ARTIFACT_POCKET_WATCH_PART_D} `Part D` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["weekly"]}\n'
        f'{emojis.ARTIFACT_POCKET_WATCH_PART_E} `Part E` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'in the TOP\n'
    )
    top_hat = (
        f'{emojis.ARTIFACT_TOP_HAT_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'in areas 3, 5 and TOP\n'
        f'{emojis.ARTIFACT_TOP_HAT_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'in areas 3, 5 and TOP\n'
        f'{emojis.ARTIFACT_TOP_HAT_PART_C} `Part C` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["trade items"]}\n'
    )
    vampire_teeth = (
        f'{emojis.ARTIFACT_VAMPIRE_TEETH_PART_A} `Part A` • Drops from the {emojis.HAL_BOSS} pumpkin bat (scroll boss)\n'
        f'{emojis.ARTIFACT_VAMPIRE_TEETH_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["hal boo"]}\n'
        f'{emojis.ARTIFACT_VAMPIRE_TEETH_PART_C} `Part C` • Drops from joining a {emojis.HAL_SLEEPYNT_JACK_O_LANTERN} '
        f'sleepyn\'t jack-o-lantern miniboss\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ARTIFACT SOURCES',
    )
    embed.add_field(name=f'CLAUS BELT {emojis.ARTIFACT_CLAUS_BELT}', value=claus_belt, inline=False)
    embed.add_field(name=f'COIN RING {emojis.ARTIFACT_COIN_RING}', value=coin_ring, inline=False)
    embed.add_field(name=f'GOLDEN PAN {emojis.ARTIFACT_GOLDEN_PAN}', value=golden_pan, inline=False)
    embed.add_field(name=f'MASTER KEY {emojis.ARTIFACT_MASTER_KEY}', value=master_key, inline=False)
    embed.add_field(name=f'POCKET WATCH {emojis.ARTIFACT_POCKET_WATCH}', value=pocket_watch, inline=False)
    embed.add_field(name=f'TOP HAT {emojis.ARTIFACT_TOP_HAT}', value=top_hat, inline=False)
    embed.add_field(name=f'VAMPIRE TEETH {emojis.ARTIFACT_VAMPIRE_TEETH}', value=vampire_teeth, inline=False)
    return embed