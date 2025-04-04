# easter.py

import discord

from content import events
from resources import emojis, settings, functions, strings, views


# --- Topics ---
TOPIC_BUNNY = 'Bunny event'
TOPIC_BUNNY_BOSS = 'Bunny boss event'
TOPIC_OVERVIEW = 'Overview'
TOPIC_BUNNY_MASK = 'Bunny mask artifact'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_BUNNY,
    TOPIC_BUNNY_BOSS,
    TOPIC_BUNNY_MASK,
]


async def command_easter_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Easter guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_overview,
        TOPIC_BUNNY: embed_event_bunny,
        TOPIC_BUNNY_BOSS: embed_event_bunnyboss,
        TOPIC_BUNNY_MASK: embed_bunny_mask,
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
    """Embed with easter guide"""
    activities = (
        f'{emojis.BP} Get {emojis.EASTER_EGG} easter eggs in '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'and all fish command tiers\n'
        f'{emojis.BP} Get {emojis.EASTER_EGG_ROUND} round eggs in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.BP} Complete daily and weekly {strings.SLASH_COMMANDS_EPIC_RPG["egg tasks"]}\n'
        f'{emojis.BP} Defeat the {emojis.EASTER_BUNNY_BOSS} **bunny boss** to get {emojis.EASTER_EGG_GOLDEN} '
        f'golden eggs\n'
        f'{emojis.DETAIL} See topic `Bunny boss event` for details.\n'
        f'{emojis.BP} Summon the {emojis.EASTER_BUNNY_GOD} **bunny god** with {strings.SLASH_COMMANDS_EPIC_RPG["egg god"]} '
        f'to make powerful wishes\n'
        f'{emojis.BP} Find the {emojis.ARTIFACT_BUNNY_MASK} bunny mask artifact (see topic `Bunny mask`)\n'
        f'{emojis.BP} Complete the {strings.SLASH_COMMANDS_EPIC_RPG["egg quest"]} to get the '
        f'{emojis.PET_GOLDEN_BUNNY} golden bunny pet\n'
        f'{emojis.BP} Gamble all your eggs away with {strings.SLASH_COMMANDS_EPIC_RPG["egg slots"]}'
    )
    bonuses = (
        f'{emojis.BP} Dungeon/Miniboss cooldown is reduced by `33`%'
    )
    tldr_guide = (
        f'{emojis.BP} Complete your {strings.SLASH_COMMANDS_EPIC_RPG["egg tasks"]}\n'
        f'{emojis.BP} Craft up to `30` {emojis.EASTER_RAINBOW_CARROT} rainbow carrots to increase bunny event spawns\n'
        f'{emojis.BP} Craft a {emojis.EASTER_SPAWNER} boss spawner whenever you have a {emojis.EASTER_BUNNY} bunny '
        f'and enough eggs to buy the instant spawn to spawn the {emojis.EASTER_BUNNY_BOSS} bunny boss\n'
        f'{emojis.BP} Summon the {emojis.EASTER_BUNNY_GOD} bunny god whenever you have '
        f'`7` {emojis.EASTER_EGG_ROUND} round eggs\n'
        f'{emojis.BP} Get at least `10` {emojis.EASTER_EGG_GOLDEN} golden eggs to complete the quest\n'
        f'{emojis.BP} Throw all {emojis.EASTER_EGG_PINK} pink eggs you get at the worldboss with '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["egg wb"]} `action: throw`\n'
        f'{emojis.BP} Empty the {strings.SLASH_COMMANDS_EPIC_RPG["egg shop"]}\n'
    )
    titles = (
        f'{emojis.BP} **Eggspert player** (bought in {strings.SLASH_COMMANDS_EPIC_RPG["egg shop"]})\n'
        f'{emojis.BP} **this is the best title** (Reward from the {strings.SLASH_COMMANDS_EPIC_RPG["egg quest"]})\n'
        f'{emojis.BP} **egg** (Achievement #213)\n'
        f'{emojis.BP} **Egg slayer** (Achievement #214)\n'
        f'{emojis.BP} **jumping fren** (Achievement #215)\n'
    )
    boost_easter = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`40` {emojis.STAT_DEF} DEF\n'
        f'{emojis.DETAIL2} +`40`% items from {strings.SLASH_COMMANDS_EPIC_RPG["farm"]}\n'
        f'{emojis.DETAIL2} +`15`% XP from all sources\n'
        f'{emojis.DETAIL} -`10`% pet adventure time if pet returns while boost is active\n'
        f'{emojis.BP} **Duration**: `1`h\n'
    )
    boost_egg_blessing = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`60`% XP from all sources\n'
        f'{emojis.DETAIL2} +`60`% coins from all sources except selling & miniboss\n'
        f'{emojis.DETAIL2} +`35`% lootbox drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.DETAIL2} +`35`% mob drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.DETAIL2} +`35`% easter event item drop chance\n'
        f'{emojis.DETAIL2} +`30`% items from work commands\n'
        f'{emojis.DETAIL2} +`10`% enchanting luck\n'
        f'{emojis.DETAIL2} +`20` {emojis.STAT_AT} AT\n'
        f'{emojis.DETAIL2} +`20` {emojis.STAT_DEF} DEF\n'
        f'{emojis.DETAIL2} +`20` {emojis.STAT_LIFE} LIFE\n'
        f'{emojis.DETAIL} Automatically heals you if you take damage\n'
        f'{emojis.BP} **Duration**: `30`d\n'
    )
    chocolate_bunny = (
        f'{emojis.BP} It\'s a Swiss chocolate delicacy, you should try it\n'
        f'{emojis.BP} It spawns a {emojis.PET_GOLDEN_BUNNY} fake golden bunny which you can try to catch\n'
        f'{emojis.DETAIL} See topic `Bunny event` for details.\n'
    )
    schedule = (
        f'{emojis.BP} Event started on March 25, 2024\n'
        f'{emojis.BP} Event will end on April 14, 2024, 23:55 UTC\n'
        f'{emojis.BP} Items will vanish on April 21, 2024, 23:55 UTC'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'EASTER EVENT 2024 {emojis.EASTER_EGG_ROUND}',
        description = 'These are some weird eggs'
    )
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='TITLES', value=titles, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='OK, BUT WHAT DOES THE EASTER BOOST DO?', value=boost_easter, inline=False)
    embed.add_field(name='EGG BLESSING IS BETTER THO, RIGHT?', value=boost_egg_blessing, inline=False)
    embed.add_field(
        name=f'...AND WTH IS A {emojis.EASTER_CHOCOLATE_BUNNY} CHOCOLATE BUNNY?',
        value=chocolate_bunny,
        inline=False
    )
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed


async def embed_event_bunny() -> discord.Embed:
    """Embed with bunny event"""
    tldr = (
        f'{emojis.BP} It\'s a pet. Tame it.\n'
    )
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'and work commands'
    )
    answers = (
        f'{emojis.BP} The bunny has a {emojis.PET_HAPPINESS} happiness and :carrot: hunger stat\n'
        f'{emojis.BP} You click on the buttons below to influence these stats\n'
        f'{emojis.BP} `1` `feed` decreases hunger by `18`-`22`\n'
        f'{emojis.BP} `1` `pat` increases happiness by `8`-`12`\n'
        f'{emojis.BP} If happiness is `85`+ higher than hunger, catch chance is `100`%\n'
        f'{emojis.BP} You can only use up to `6` actions\n'
        f'{emojis.BP} Less actions = `15` {emojis.EASTER_EGG} easter eggs for every command not used'
    )
    rewards = (
        f'{emojis.BP} {emojis.EASTER_BUNNY} Bunny (used in crafting {emojis.EASTER_SPAWNER} boss spawners)\n'
        f'{emojis.BP} {emojis.PET_GOLDEN_BUNNY} Fake golden bunny. Gifts you a {emojis.EASTER_SPAWNER} boss spawner '
        f'every day.'
    )
    note =(
        f'{emojis.BP} You can increase the chance of this event by crafting {emojis.EASTER_RAINBOW_CARROT} '
        f'rainbow carrots\n'
        f'{emojis.DETAIL} You can craft up to `30` carrots'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'EASTER: BUNNY EVENT {emojis.EASTER_BUNNY}',
        description = 'This is a random personal event in which a bunny appears for you to tame.'
    )
    embed.add_field(name='TL;DR', value=tldr, inline=False)
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO TAME THE BUNNY', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_bunnyboss() -> discord.Embed:
    """Embed with bunny boss event"""
    trigger = (
        f'{emojis.BP} Craft a {emojis.EASTER_SPAWNER} boss spawner\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["egg use"]} `item: boss spawner` or '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["egg buy"]} `item: instant spawn`\n'
        f'{emojis.DETAIL} If you don\'t buy an instant spawn, this will use your dungeon cooldown!'
    )
    answers = (
        f'{emojis.BP} `fight` or `defend`\n'
        f'{emojis.BP} Look at the boss stats to decide what to choose'
    )
    rewards = (
        f'{emojis.BP} `1`-`2` {emojis.EASTER_EGG_GOLDEN} golden eggs\n'
        f'{emojis.BP} {emojis.EASTER_EGG} Easter eggs\n'
        f'{emojis.BP} {emojis.ARENA_COOKIE} Arena cookies\n'
        f'{emojis.BP} {emojis.EPIC_COIN} EPIC coins\n'
        f'{emojis.BP} {emojis.EASTER_LOOTBOX} Easter lootboxes\n'
        f'{emojis.BP} The participants have a chance to get a few {emojis.EASTER_EGG} easter eggs and '
        f'{emojis.ARENA_COOKIE} cookies'
    )
    note = (
        f'{emojis.BP} {events.events_multiplayer}\n'
        f'{emojis.BP} {events.events_player_no.format(no=15)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'EASTER: BUNNY BOSS EVENT {emojis.EASTER_BUNNY_BOSS}',
        description = 'This is a multiplayer event in which you fight a bunny boss.'
    )
    embed.add_field(name='HOW TO START', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_bunny_mask() -> discord.Embed:
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