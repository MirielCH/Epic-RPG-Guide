# easter.py

import discord

from content import events
from resources import emojis, settings, functions, strings, views


# --- Topics ---
TOPIC_BUNNY = 'Bunny event'
TOPIC_BUNNY_BOSS = 'Bunny boss event'
TOPIC_OVERVIEW = 'Overview'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_BUNNY,
    TOPIC_BUNNY_BOSS,
]


async def easter_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Easter guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_overview,
        TOPIC_BUNNY: embed_event_bunny,
        TOPIC_BUNNY_BOSS: embed_event_bunnyboss,
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
        f'{emojis.BP} Get {emojis.EASTER_EGG} easter eggs in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} and all fish command tiers\n'
        f'{emojis.BP} Tame bunnies in the new random **bunny event** (see topic `Bunny event`)\n'
        f'{emojis.BP} Defeat the {emojis.EASTER_BUNNY_BOSS} **bunny boss** to get {emojis.EASTER_EGG_GOLDEN} '
        f'golden eggs (see topic `Bunny boss event`)\n'
        f'{emojis.BP} Complete the **quest** to get the {emojis.PET_GOLDEN_BUNNY} golden bunny pet '
        f'(see {emojis.EPIC_RPG_LOGO}`/easter quest`)\n'
        f'{emojis.BP} Gamble all your eggs away with {emojis.EPIC_RPG_LOGO_SMALL}`/easter slots`'
    )
    bonuses = (
        f'{emojis.BP} Dungeon/Miniboss cooldown is lowered to 6h'
    )
    whattodo = (
        f'{emojis.BP} Craft 5 {emojis.EASTER_RAINBOW_CARROT} rainbow carrots first to increase bunny event spawns\n'
        f'{emojis.BP} Craft a {emojis.EASTER_SPAWNER} boss spawner whenever you have a {emojis.EASTER_BUNNY} bunny '
        f'and enough eggs to buy the instant spawn to spawn the {emojis.EASTER_BUNNY_BOSS} bunny boss\n'
        f'{emojis.BP} Get at least 10 {emojis.EASTER_EGG_GOLDEN} golden eggs to complete the quest\n'
        f'{emojis.BP} Craft {emojis.POTION_SLEEPY} sleepy potions with leftover {emojis.EASTER_EGG_GOLDEN} golden eggs\n'
        f'{emojis.BP} Spend leftover {emojis.EASTER_EGG} easter eggs in the shop '
        f'({emojis.EPIC_RPG_LOGO_SMALL}`/easter shop`)'
    )
    schedule = (
        f'{emojis.BP} Event started on April 3, 2021\n'
        f'{emojis.BP} Event ended on April 17, 2021, 23:55 UTC\n'
        f'{emojis.BP} Items will vanish on April 22, 2021, 23:55 UTC'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'EASTER EVENT 2022 {emojis.EASTER_EGG}',
        description = 'Hope you like eggs.'
    )
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='WHAT TO DO', value=whattodo, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed


async def embed_event_bunny() -> discord.Embed:
    """Embed with bunny event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'and work commands (0.75 % chance)'
    )
    answers = (
        f'{emojis.BP} The bunny has a {emojis.PET_HAPPINESS} happiness and :carrot: hunger stat\n'
        f'{emojis.BP} You click on the buttons below to influence these stats\n'
        f'{emojis.BP} 1 `feed` decreases hunger by 18-22\n'
        f'{emojis.BP} 1 `pat` increases happiness by 8-12\n'
        f'{emojis.BP} If happiness is 85+ higher than hunger, catch chance is 100%\n'
        f'{emojis.BP} You can only use up to 6 actions\n'
        f'{emojis.BP} Less actions = 15 {emojis.EASTER_EGG} easter eggs for every command not used'
    )
    rewards = (
        f'{emojis.BP} {emojis.EASTER_BUNNY} Bunny (used in crafting {emojis.EASTER_SPAWNER} boss spawners)\n'
        f'{emojis.BP} {emojis.PET_GOLDEN_BUNNY} Fake golden bunny. Gifts you a {emojis.EASTER_SPAWNER} boss spawner '
        f'every day.'
    )
    note =(
        f'{emojis.BP} You can increase the chance of this event by crafting {emojis.EASTER_RAINBOW_CARROT} '
        f'rainbow carrots\n'
        f'{emojis.BP} You can craft up to 5 carrots which gives you a 3 % spawn chance'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EASTER: BUNNY EVENT',
        description = 'This is a random personal event in which a bunny appears for you to tame.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO TAME THE BUNNY', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_bunnyboss() -> discord.Embed:
    """Embed with bunny boss event"""
    trigger = (
        f'{emojis.BP} Craft a {emojis.EASTER_SPAWNER} boss spawner\n'
        f'{emojis.BP} Use `egg use boss spawner` or `egg buy instant spawn`\n'
        f'{emojis.BP} If you don\'t buy an instant spawn, this will use your dungeon cooldown'
    )
    answers = (
        f'{emojis.BP} `fight` or `defend`\n'
        f'{emojis.BP} Look at the boss stats to decide what to choose'
    )
    rewards = (
        f'{emojis.BP} 1-2 {emojis.EASTER_EGG_GOLDEN} golden eggs\n'
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
        title = 'EASTER: BUNNY BOSS EVENT',
        description = 'This is a multiplayer event in which you fight a bunny boss.'
    )
    embed.add_field(name='HOW TO START', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed