# alchemy.py

import discord

from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_ARTIFACTS_SOURCE_SUMMARY = 'Source summary'
TOPIC_ARTIFACTS_BUNNY_MASK = 'Bunny mask'
TOPIC_ARTIFACTS_CHOCOLATE_BOX = 'Chocolate box'
TOPIC_ARTIFACTS_CLAUS_BELT = 'Claus belt'
TOPIC_ARTIFACTS_COIN_RING = 'Coin ring'
TOPIC_ARTIFACTS_CLAUS_BELT = 'Claus belt'
TOPIC_ARTIFACTS_COWBOY_BOOTS = 'Cowboy boots'
TOPIC_ARTIFACTS_GOLDEN_PAN = 'Golden pan'
TOPIC_ARTIFACTS_MASTER_KEY = 'Master key'
TOPIC_ARTIFACTS_POCKET_WATCH = 'Pocket watch'
TOPIC_ARTIFACTS_SHINY_PICKAXE = 'Shiny pickaxe'
TOPIC_ARTIFACTS_SUNGLASSES = 'Sunglasses'
TOPIC_ARTIFACTS_TOP_HAT = 'Top hat'
TOPIC_ARTIFACTS_VAMPIRE_TEETH = 'Vampire teeth'
TOPIC_ARTIFACTS_VOID_TOME = 'Void tome'

TOPICS_ARTIFACTS = [
    TOPIC_OVERVIEW,
    TOPIC_ARTIFACTS_SOURCE_SUMMARY,
    TOPIC_ARTIFACTS_BUNNY_MASK,
    TOPIC_ARTIFACTS_CHOCOLATE_BOX,
    TOPIC_ARTIFACTS_CLAUS_BELT,
    TOPIC_ARTIFACTS_COIN_RING,
    TOPIC_ARTIFACTS_COWBOY_BOOTS,
    TOPIC_ARTIFACTS_GOLDEN_PAN,
    TOPIC_ARTIFACTS_MASTER_KEY,
    TOPIC_ARTIFACTS_POCKET_WATCH,
    TOPIC_ARTIFACTS_SHINY_PICKAXE,
    TOPIC_ARTIFACTS_SUNGLASSES,
    TOPIC_ARTIFACTS_TOP_HAT,
    TOPIC_ARTIFACTS_VAMPIRE_TEETH,
    TOPIC_ARTIFACTS_VOID_TOME,
]


# --- Commands ---
async def command_artifacts_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Artifacts command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_artifacts_overview,
        TOPIC_ARTIFACTS_SOURCE_SUMMARY: embed_artifacts_source_summary,
        TOPIC_ARTIFACTS_BUNNY_MASK: embed_artifacts_bunny_mask,
        TOPIC_ARTIFACTS_CHOCOLATE_BOX: embed_artifacts_chocolate_box,
        TOPIC_ARTIFACTS_CLAUS_BELT: embed_artifacts_claus_belt,
        TOPIC_ARTIFACTS_COIN_RING: embed_artifacts_coin_ring,
        TOPIC_ARTIFACTS_COWBOY_BOOTS: embed_artifacts_cowboy_boots,
        TOPIC_ARTIFACTS_GOLDEN_PAN: embed_artifacts_golden_pan,
        TOPIC_ARTIFACTS_MASTER_KEY: embed_artifacts_master_key,
        TOPIC_ARTIFACTS_POCKET_WATCH: embed_artifacts_pocket_watch,
        TOPIC_ARTIFACTS_SHINY_PICKAXE: embed_artifacts_shiny_pickaxe,
        TOPIC_ARTIFACTS_SUNGLASSES: embed_artifacts_sunglasses,
        TOPIC_ARTIFACTS_TOP_HAT: embed_artifacts_top_hat,
        TOPIC_ARTIFACTS_VAMPIRE_TEETH: embed_artifacts_vampire_teeth,
        TOPIC_ARTIFACTS_VOID_TOME: embed_artifacts_void_tome,
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
        f'{emojis.DETAIL} Artifact parts start dropping in {emojis.TIME_TRAVEL} TT `1+`\n'
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


async def embed_artifacts_chocolate_box() -> discord.Embed:
    """Chocolate box guide"""
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


async def embed_artifacts_cowboy_boots() -> discord.Embed:
    """Cowboy boots guide"""
    effects = (
        f'{emojis.BP} Increases your luck in {strings.SLASH_COMMANDS_EPIC_RPG["hf megarace"]}\n'
        f'{emojis.BP} Increases your horse\'s chance to gain epicness when breeding by `5`%\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_COWBOY_BOOTS_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["hf lightspeed"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_COWBOY_BOOTS_PART_B} `Part B` • Drops from starting {strings.SLASH_COMMANDS_EPIC_RPG["hf megarace"]}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'COWBOY BOOTS {emojis.ARTIFACT_COWBOY_BOOTS}',
        description = 'This artifact is only available during the horse festival event!',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed


async def embed_artifacts_golden_pan() -> discord.Embed:
    """Golden pan guide"""
    effects = (
        f'{emojis.BP} Lets you keep a percentage of cooked stats when time traveling\n'
        f'{emojis.DETAIL} The percentage increases with time travels\n'
        f'{emojis.BP} Increases the cooking item cap to `1.5b`\n'
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


async def embed_artifacts_shiny_pickaxe() -> discord.Embed:
    """Shiny pickaxe guide"""
    effects = (
        f'{emojis.BP} Increases the drop amount with `mine` commands by `x2.5`\n'
        f'{emojis.BP} Increases the chance to get a ruby dragon event when using `mine` commands by `x10`\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_SHINY_PICKAXE_PART_A} `Part A` • Reward from the {emojis.MOB_GOLDEN_WOLF} golden wolf '
        f'hunt event in areas 1~2\n'
        f'{emojis.BP} {emojis.ARTIFACT_SHINY_PICKAXE_PART_B} `Part B` • Reward from the {emojis.MOB_RUBY_ZOMBIE} ruby zombie '
        f'hunt event in areas 3~4\n'
        f'{emojis.BP} {emojis.ARTIFACT_SHINY_PICKAXE_PART_C} `Part C` • Reward from the {emojis.MOB_DIAMOND_UNICORN} diamond '
        f'unicorn hunt event in areas 5~6\n'
        f'{emojis.BP} {emojis.ARTIFACT_SHINY_PICKAXE_PART_D} `Part D` • Reward from the {emojis.MOB_EMERALD_MERMAID} emerald mermaid '
        f'hunt event in areas 7~8\n'
        f'{emojis.BP} {emojis.ARTIFACT_SHINY_PICKAXE_PART_E} `Part E` • Reward from the {emojis.MOB_SAPPHIRE_KILLER_ROBOT} sapphire '
        f'killer robot hunt event in areas 9~10\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SHINY PICKAXE {emojis.ARTIFACT_SHINY_PICKAXE}',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed


async def embed_artifacts_sunglasses() -> discord.Embed:
    """Sunglasses artifact embed"""
    effects = (
        f'{emojis.BP} Adds compensation reward when slipping off in {strings.SLASH_COMMANDS_EPIC_RPG["smr surf"]}\n'
        f'{emojis.BP} Sometimes increases amount healed by {strings.SLASH_COMMANDS_EPIC_RPG["heal"]}\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_SUNGLASSES_PART_A} `Part A` • Reward for not slipping off in any round in '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["smr surf"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_SUNGLASSES_PART_B} `Part B` • Drops from drinking {emojis.SMR_DRINK_BLUE}'
        f'{emojis.SMR_DRINK_GREEN}{emojis.SMR_DRINK_PINK}{emojis.SMR_DRINK_YELLOW} drinks with '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["smr drink"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SUNGLASSES {emojis.ARTIFACT_SUNGLASSES}',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
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


async def embed_artifacts_bunny_mask() -> discord.Embed:
    """Bunny mask artifact embed"""
    effects = (
        f'{emojis.BP} You get 1 round egg back after summoning the {strings.SLASH_COMMANDS_EPIC_RPG["egg god"]}\n'
        f'{emojis.BP} Increases chance to encounter pets in {strings.SLASH_COMMANDS_EPIC_RPG["training"]} by `10`%\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_BUNNY_MASK_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["egg eat"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_BUNNY_MASK_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["egg slots"]}\n'
        f'{emojis.BP} {emojis.BLANK} `Part C` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["egg god"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'BUNNY MASK {emojis.ARTIFACT_BUNNY_MASK}',
        description = 'This artifact is only available during the easter event!',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed


async def embed_artifacts_void_tome() -> discord.Embed:
    """Void tome artifact embed"""
    effects = (
        f'{emojis.BP} Reduces the price of the {emojis.EPIC_JUMP} EPIC jump to `1` {emojis.TIME_DRAGON_ESSENCE} TIME dragon essence\n'
        f'{emojis.BP} Increases the VOID contribution rewards by `1.2x`\n'
        f'{emojis.BP} Gives you a {emojis.VOIDICE} VOIDice every time you time travel\n'
        f'{emojis.DETAIL} Using the item will reward you with `0`~`5` {emojis.TIME_TRAVEL} time travels\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_VOID_TOME_PART_A} `Part A` • Drops from beating dungeon 16\n'
        f'{emojis.BP} {emojis.ARTIFACT_VOID_TOME_PART_B} `Part B` • Drops from beating dungeon 17\n'
        f'{emojis.BP} {emojis.ARTIFACT_VOID_TOME_PART_C} `Part C` • Drops from beating dungeon 18\n'
        f'{emojis.BP} {emojis.ARTIFACT_VOID_TOME_PART_D} `Part D` • Drops from beating dungeon 19\n'
        f'{emojis.BP} {emojis.ARTIFACT_VOID_TOME_PART_E} `Part E` • Drops from beating dungeon 20\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'VOID TOME {emojis.ARTIFACT_VOID_TOME}',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed


async def embed_artifacts_source_summary() -> discord.Embed:
    """Artifacts sources"""
    bunny_mask = (
        f'{emojis.ARTIFACT_BUNNY_MASK_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["egg eat"]}\n'
        f'{emojis.ARTIFACT_BUNNY_MASK_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["egg slots"]}\n'
        f'{emojis.BLANK} `Part C` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["egg god"]}\n'
    )
    chocolate_box = (
        f'{emojis.ARTIFACT_CHOCOLATE_BOX_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["love share"]}\n'
        f'{emojis.ARTIFACT_CHOCOLATE_BOX_PART_B} `Part B` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["love slots"]}\n'
        f'{emojis.ARTIFACT_CHOCOLATE_BOX_PART_C} `Part C` • Drops from buying items in the '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["love shop"]}\n'
    )
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
    cowboy_boots = (
        f'{emojis.ARTIFACT_COWBOY_BOOTS_PART_A} `Part A` • Drops from {strings.SLASH_COMMANDS_EPIC_RPG["hf lightspeed"]}\n'
        f'{emojis.ARTIFACT_COWBOY_BOOTS_PART_B} `Part B` • Drops from starting {strings.SLASH_COMMANDS_EPIC_RPG["hf megarace"]} '
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
    shiny_pickaxe = (
        f'{emojis.ARTIFACT_SHINY_PICKAXE_PART_A} `Part A` • Reward from the {emojis.MOB_GOLDEN_WOLF} golden wolf '
        f'hunt event in areas 1~2\n'
        f'{emojis.ARTIFACT_SHINY_PICKAXE_PART_B} `Part B` • Reward from the {emojis.MOB_RUBY_ZOMBIE} ruby zombie '
        f'hunt event in areas 3~4\n'
        f'{emojis.ARTIFACT_SHINY_PICKAXE_PART_C} `Part C` • Reward from the {emojis.MOB_DIAMOND_UNICORN} diamond '
        f'unicorn hunt event in areas 5~6\n'
        f'{emojis.ARTIFACT_SHINY_PICKAXE_PART_D} `Part D` • Reward from the {emojis.MOB_EMERALD_MERMAID} emerald mermaid '
        f'hunt event in areas 7~8\n'
        f'{emojis.ARTIFACT_SHINY_PICKAXE_PART_E} `Part E` • Reward from the {emojis.MOB_SAPPHIRE_KILLER_ROBOT} sapphire '
        f'killer robot hunt event in areas 9~10\n'
    )
    sunglasses = (
        f'{emojis.ARTIFACT_SUNGLASSES_PART_A} `Part A` • Reward for not slipping off in any round in '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["smr surf"]}\n'
        f'{emojis.ARTIFACT_SUNGLASSES_PART_B} `Part B` • Drops from drinking {emojis.SMR_DRINK_BLUE}'
        f'{emojis.SMR_DRINK_GREEN}{emojis.SMR_DRINK_PINK}{emojis.SMR_DRINK_YELLOW} drinks with '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["smr drink"]}\n'
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
    void_tome = (
        f'{emojis.ARTIFACT_VOID_TOME_PART_A} `Part A` • Drops from beating dungeon 16\n'
        f'{emojis.ARTIFACT_VOID_TOME_PART_B} `Part B` • Drops from beating dungeon 17\n'
        f'{emojis.ARTIFACT_VOID_TOME_PART_C} `Part C` • Drops from beating dungeon 18\n'
        f'{emojis.ARTIFACT_VOID_TOME_PART_D} `Part D` • Drops from beating dungeon 19\n'
        f'{emojis.ARTIFACT_VOID_TOME_PART_E} `Part E` • Drops from beating dungeon 20\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ARTIFACT SOURCES',
    )
    embed.add_field(name=f'BUNNY MASK {emojis.ARTIFACT_BUNNY_MASK}', value=bunny_mask, inline=False)
    embed.add_field(name=f'CHOCOLATE BOX {emojis.ARTIFACT_CHOCOLATE_BOX}', value=chocolate_box, inline=False)
    embed.add_field(name=f'CLAUS BELT {emojis.ARTIFACT_CLAUS_BELT}', value=claus_belt, inline=False)
    embed.add_field(name=f'COIN RING {emojis.ARTIFACT_COIN_RING}', value=coin_ring, inline=False)
    embed.add_field(name=f'COWBOY BOOTS {emojis.ARTIFACT_COWBOY_BOOTS}', value=cowboy_boots, inline=False)
    embed.add_field(name=f'GOLDEN PAN {emojis.ARTIFACT_GOLDEN_PAN}', value=golden_pan, inline=False)
    embed.add_field(name=f'MASTER KEY {emojis.ARTIFACT_MASTER_KEY}', value=master_key, inline=False)
    embed.add_field(name=f'POCKET WATCH {emojis.ARTIFACT_POCKET_WATCH}', value=pocket_watch, inline=False)
    embed.add_field(name=f'SHINY PICKAXE {emojis.ARTIFACT_SHINY_PICKAXE}', value=shiny_pickaxe, inline=False)
    embed.add_field(name=f'SUNGLASSES {emojis.ARTIFACT_SUNGLASSES}', value=sunglasses, inline=False)
    embed.add_field(name=f'TOP HAT {emojis.ARTIFACT_TOP_HAT}', value=top_hat, inline=False)
    embed.add_field(name=f'VAMPIRE TEETH {emojis.ARTIFACT_VAMPIRE_TEETH}', value=vampire_teeth, inline=False)
    embed.add_field(name=f'VOID TOME {emojis.ARTIFACT_VOID_TOME}', value=void_tome, inline=False)
    return embed