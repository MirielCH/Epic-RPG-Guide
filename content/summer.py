# summer.py
"""Contains all summer event guides"""

import discord

from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_BOOSTS = 'Boosts'
TOPIC_COLOR_TOURNAMENT = 'Color tournament'
TOPIC_SURF = 'Surfing'
TOPIC_SUNGLASSES = 'Sunglasses artifact'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_BOOSTS,
    TOPIC_COLOR_TOURNAMENT,
    TOPIC_SURF,
    TOPIC_SUNGLASSES,
]

# --- Commands ---
async def command_summer_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Summer event guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_overview,
        TOPIC_BOOSTS: embed_boosts,
        TOPIC_COLOR_TOURNAMENT: embed_color_tournament,
        TOPIC_SURF: embed_surf,
        TOPIC_SUNGLASSES: embed_sunglasses,
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
async def embed_overview() -> discord.Embed:
    """Summer guide overview embed"""
    activities = (
        f'{emojis.BP} Get {emojis.SMR_COCONUT} coconuts and {emojis.SMR_LOG_PALM}{emojis.SMR_LOG_PALM_MEGA} palm logs with chop and fish commands\n'
        f'{emojis.BP} Complete daily and weekly {strings.SLASH_COMMANDS_EPIC_RPG["smr tasks"]}\n'
        f'{emojis.BP} Complete the {strings.SLASH_COMMANDS_EPIC_RPG["smr quest"]} to get a {emojis.PET_TURTLE} turtle pet\n'
        f'{emojis.BP} Find the {emojis.ARTIFACT_SUNGLASSES} sunglasses artifact (see topic `Sunglasses artifact`)\n'
        f'{emojis.BP} Go surfing with {strings.SLASH_COMMANDS_EPIC_RPG["smr surf"]} (see topic `Surfing`)\n'
        f'{emojis.DETAIL} This event command has a `4`h cooldown\n'
        f'{emojis.BP} Join the weekly color tournament (see topic `Color tournament`)\n'
        f'{emojis.BP} Kill the rare {emojis.SMR_SLIME} summer slime in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'to get extra coconuts and a free drink\n'
        f'{emojis.BP} Join the world boss fight to unlock codes (see {strings.SLASH_COMMANDS_EPIC_RPG["smr wb"]})\n'
        f'{emojis.BP} Buy various rewards in the {strings.SLASH_COMMANDS_EPIC_RPG["smr shop"]}\n'
    )
    bonuses = (
        f'{emojis.BP} Work commands are reduced by `50`%\n'
    )
    titles = (
        f'{emojis.BP} **SumMEGA** (bought in the {strings.SLASH_COMMANDS_EPIC_RPG["smr shop"]})\n'
        f'{emojis.BP} **BEACH KING** (unlocked by winning the color tournament)\n'
    )
    schedule = (
        f'{emojis.BP} Event started on July 10, 2025\n'
        f'{emojis.BP} Event ended on July 28, 2025, 23:55 UTC\n'
        f'{emojis.BP} Love tokens and coins can be used until August 4, 23:55 UTC\n'
    )
    tldr_guide = (
        f'{emojis.BP} Complete daily and weekly {strings.SLASH_COMMANDS_EPIC_RPG["smr tasks"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["smr craft"]} a surfboard of your choosing\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["smr surf"]} on cooldown\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["smr drink"]} at least one drink each week to join the color tournament\n'
        f'{emojis.BP} Complete the {strings.SLASH_COMMANDS_EPIC_RPG["smr quest"]} to unlock the '
        f'{emojis.PET_TURTLE} turtle pet\n'
        f'{emojis.BP} Use your coins for whatever you want in {strings.SLASH_COMMANDS_EPIC_RPG["love shop"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SUMMER EVENT 2025 {emojis.SMR_DRINK_BLUE}',
        description = 'Don\'t mind me, just working on my tan.'
    )
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='TITLES', value=titles, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed


async def embed_boosts() -> discord.Embed:
    """Embed with summer boosts guide"""
    boost_summer = ( # Verified
        f'{emojis.BP} **Source**: Bought in the {strings.SLASH_COMMANDS_EPIC_RPG["smr shop"]} for 50 {emojis.SMR_COCONUT_CHOPPED}\n'
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`40`% items from work commands\n'
        f'{emojis.DETAIL2} +`40`% item rarity from work commands\n'
        f'{emojis.DETAIL2} +`25`% XP from all sources\n'
        f'{emojis.DETAIL} +`15`% profession XP\n'
        f'{emojis.BP} **Duration**: `4`h\n'
    )
    boost_drink_blue = ( # Verified
        f'{emojis.BP} **Source**: Crafted with {strings.SLASH_COMMANDS_EPIC_RPG["smr craft"]}\n'
        f'{emojis.BP} **Recipe**: `3` {emojis.SMR_COCONUT_CHOPPED} + `2` {emojis.FISH}\n'
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL} +`30`% summer event item drop chance\n'
        f'{emojis.BP} **Duration**: `2`h\n'
    )
    boost_drink_green = ( # Verified
        f'{emojis.BP} **Source**: Crafted with {strings.SLASH_COMMANDS_EPIC_RPG["smr craft"]}\n'
        f'{emojis.BP} **Recipe**: `3` {emojis.SMR_COCONUT_CHOPPED} + `1` {emojis.FISH_EPIC} + `1` {emojis.CHIP}\n'
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`25`% items from work commands\n'
        f'{emojis.BP} **Duration**: `2`h\n'
    )
    boost_drink_pink = ( # Verified
        f'{emojis.BP} **Source**: Crafted with {strings.SLASH_COMMANDS_EPIC_RPG["smr craft"]}\n'
        f'{emojis.BP} **Recipe**: `3` {emojis.SMR_COCONUT_CHOPPED} + `1` {emojis.LB_EDGY}\n'
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`20`% lootbox drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} **Duration**: `2`h\n'
    )
    boost_drink_yellow = ( # Verified
        f'{emojis.BP} **Source**: Crafted with {strings.SLASH_COMMANDS_EPIC_RPG["smr craft"]}\n'
        f'{emojis.BP} **Recipe**: `3` {emojis.SMR_COCONUT_CHOPPED} + `1` {emojis.EPIC_SEED} + `3` {emojis.BANANA} '
        f'`1` {emojis.LOTTERY_TICKET}\n'
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`50`% XP from all sources\n'
        f'{emojis.DETAIL} +`50`% coins from all sources except selling & miniboss\n'
        f'{emojis.BP} **Duration**: `2`h\n'
    )
    boost_chopped_coconut = (
        f'{emojis.BP} **Source**: Crafted with {strings.SLASH_COMMANDS_EPIC_RPG["smr craft"]}\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.SMR_COCONUT}\n'
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`5` {emojis.STAT_LIFE} LIFE\n'
        f'{emojis.DETAIL2} +`5`% XP from all sources\n'
        f'{emojis.DETAIL} +`5`% coins from all sources except selling & miniboss\n'
        f'{emojis.BP} **Duration**: `2`m\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SUMMER EVENT BOOSTS {emojis.SMR_DRINK_BLUE}{emojis.SMR_DRINK_GREEN}{emojis.SMR_DRINK_PINK}{emojis.SMR_DRINK_YELLOW}',
        description = 'It\'s five o\'clock somewhere.'
    )
    embed.add_field(name=f'SUMMER BOOST {emojis.SMR_COCONUT}', value=boost_summer, inline=False)
    embed.add_field(name=f'BLUE DRINK {emojis.SMR_DRINK_BLUE}', value=boost_drink_blue, inline=False)
    embed.add_field(name=f'GREEN DRINK {emojis.SMR_DRINK_GREEN}', value=boost_drink_green, inline=False)
    embed.add_field(name=f'PINK DRINK {emojis.SMR_DRINK_PINK}', value=boost_drink_pink, inline=False)
    embed.add_field(name=f'YELLOW DRINK {emojis.SMR_DRINK_YELLOW}', value=boost_drink_yellow, inline=False)
    embed.add_field(name=f'CHOPPED COCONUT {emojis.SMR_COCONUT_CHOPPED}', value=boost_chopped_coconut, inline=False)
    return embed


async def embed_color_tournament() -> discord.Embed:
    """Big arena event"""
    overview = (
        f'{emojis.BP} Every week, you can join the blue, green, pink or yellow team\n'
        f'{emojis.BP} The team with the least slip offs in {strings.SLASH_COMMANDS_EPIC_RPG["smr surf"]} wins\n'
        f'{emojis.BP} The amount of players in the teams does **not** impact the ability to win\n'
    )
    schedule = f'{emojis.BP} Runs between Saturday 00:01 UTC and Sunday 23:59 UTC'
    command = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["smr drink"]} a {emojis.SMR_DRINK_BLUE} blue, {emojis.SMR_DRINK_GREEN} '
        f'green, {emojis.SMR_DRINK_PINK} pink or {emojis.SMR_DRINK_YELLOW} yellow drink between '
        f'Monday 00:01 UTC and Friday 23:59 UTC\n'
        f'{emojis.BP} The **first** drink you drink in that timeframe determines your team.\n'
        f'{emojis.BP} You can not change teams.'
    )
    rewards = (
        f'{emojis.BP} `10` {emojis.SMR_LOG_PALM_MEGA} MEGA palm logs and the **BEACH KING** title for the winning team\n'
        f'{emojis.BP} `5` {emojis.SMR_LOG_PALM_MEGA} MEGA palm logs for the other teams\n'
    )
    team_bonuses = (
        f'{emojis.BP} Being in a team gives you a buff until the tournament resets\n'
        f'{emojis.BP} **Blue** team: Crafted items in {strings.SLASH_COMMANDS_EPIC_RPG["smr craft"]} are doubled\n'
        f'{emojis.BP} **Green** team: Rewards from {strings.SLASH_COMMANDS_EPIC_RPG["smr surf"]} are doubled\n'
        f'{emojis.BP} **Pink** team: Items in the {strings.SLASH_COMMANDS_EPIC_RPG["smr shop"]} are `30`% cheaper\n'
        f'{emojis.BP} **Yellow** team: Rewards from {strings.SLASH_COMMANDS_EPIC_RPG["smr tasks"]} are doubled\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'COLOR TOURNAMENT',
        description = 'This is a global event which runs weekly.'
    )
    embed.add_field(name='OVERVIEW', value=overview, inline=False)
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=command, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='TEAM BONUSES', value=team_bonuses, inline=False)
    return embed


async def embed_surf() -> discord.Embed:
    """Surf embed"""
    overview = (
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["smr surf"]} to start surfing\n'
        f'{emojis.BP} Every surf event has `3` rounds\n'
        f'{emojis.BP} Every round you will encounter `2` random choices\n'
        f'{emojis.BP} Depending on your choice and luck, you can either slip off your board or continue to the next round\n'
        f'{emojis.BP} You can craft a surfboard to increase your chances (see below)\n'
        f'{emojis.BP} You can surf every `4`h\n'
    )
    rewards = (
        f'{emojis.BP} You get a reward for every round you stay on the board\n'
        f'{emojis.DETAIL} The amount depends on the risk you took (see below)\n'
        f'{emojis.BP} Staying on the board for all `3` rounds gives you an additional `1` {emojis.SMR_LOG_PALM_MEGA} MEGA palm log\n'
        f'{emojis.BP} If you slip off the board and have the {emojis.ARTIFACT_SUNGLASSES} '
        f'sunglasses artifact, you get a compensation reward.\n'
    )
    answers = (
        f'{emojis.BP} The command differentiates between **logical**, **defensive**, **initiative** and **creative** answers\n'
        f'{emojis.BP} **Logical** answer: **Very low** risk to slip off the board\n'
        f'{emojis.BP} **Defensive** answer: **Low** risk to slip off the board\n'
        f'{emojis.BP} **Initative** answer: **High** risk to slip off the board\n'
        f'{emojis.BP} **Creative** answer: **Very high** risk to slip off the board\n'
        f'{emojis.BP} The higher the risk, the higher the rewards!\n'
    )
    surfboards = (
        f'{emojis.BP} {emojis.SMR_SURFBOARD_GREEN} Green surfboard: `+20`% success chance in logical answers\n'
        f'{emojis.BP} {emojis.SMR_SURFBOARD_BLUE} Blue surfboard: `+20`% success chance in defensive answers\n'
        f'{emojis.BP} {emojis.SMR_SURFBOARD_YELLOW} Yellow surfboard: `+20`% success chance in initiative answers\n'
        f'{emojis.BP} {emojis.SMR_SURFBOARD_PINK} Pink surfboard: `+20`% success chance in creative answers\n'
        f'{emojis.BP} {emojis.SMR_SURFBOARD_MEGA} MEGA surfboard: `+15`% success chance in **all** answers\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'SURFING',
        description = 'C\'mon man, it\'s just water moving around... how hard can it be?'
    )
    embed.add_field(name='OVERVIEW', value=overview, inline=False)
    embed.add_field(name='REWARDS', value=rewards, inline=False)
    embed.add_field(name='ANSWERS', value=answers, inline=False)
    embed.add_field(name='SURFBOARDS', value=surfboards, inline=False)
    return embed


async def embed_sunglasses() -> discord.Embed:
    """Sunglasses artifact embed"""
    effects = (
        f'{emojis.BP} Adds a compensation reward when you slip off in {strings.SLASH_COMMANDS_EPIC_RPG["smr surf"]}\n'
        f'{emojis.BP} Adds a `5`% chance to trigger a 2 minute boost when using {strings.SLASH_COMMANDS_EPIC_RPG["heal"]}\n'
        f'{emojis.DETAIL} The boost includes `5` LIFE, `5`% mob drop chance and `5`% profession XP\n'
    )
    parts = (
        f'{emojis.BP} {emojis.ARTIFACT_SUNGLASSES_PART_A} `Part A` • Reward for not slipping off in all 3 rounds of '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["smr surf"]}\n'
        f'{emojis.BP} {emojis.ARTIFACT_SUNGLASSES_PART_B} `Part B` • Drops from drinking {emojis.SMR_DRINK_BLUE}'
        f'{emojis.SMR_DRINK_GREEN}{emojis.SMR_DRINK_PINK}{emojis.SMR_DRINK_YELLOW} drinks with '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["smr drink"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'SUNGLASSES {emojis.ARTIFACT_SUNGLASSES}',
        description = 'This artifact is only available during the summer event!',
    )
    embed.add_field(name='EFFECT', value=effects, inline=False)
    embed.add_field(name='ARTIFACT PARTS', value=parts, inline=False)
    return embed