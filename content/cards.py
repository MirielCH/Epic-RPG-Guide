# cards.py

import discord

from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_CARDS_SOURCES = 'Sources'

TOPICS_CARDS = [
    TOPIC_OVERVIEW,
    TOPIC_CARDS_SOURCES,
]


# --- Commands ---
async def command_cards_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Cards command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_cards_overview,
        TOPIC_CARDS_SOURCES: embed_cards_sources,
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
async def embed_cards_overview() -> discord.Embed:
    """Artifacts guide overview"""
    overview = (
        f'{emojis.BP} Cards are rare drops which can be turned into playing cards\n'
        f'{emojis.BP} There are 8 card tiers: {emojis.CARD_COMMON}{emojis.CARD_UNCOMMON}{emojis.CARD_RARE}{emojis.CARD_EPIC}'
        f'{emojis.CARD_OMEGA}{emojis.CARD_GODLY}{emojis.CARD_VOID}{emojis.CARD_ETERNAL}\n'
        f'{emojis.BP} Cards can drop from {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}, '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["farm"]} and work commands (see `Sources`)\n'
        f'{emojis.BP} The cards drop rate is **not** affected by TT and hardmode (or anything else)'
    )
    slotting_cards = (
        f'{emojis.BP} Once you have 3 cards of the **same tier**, you can use {strings.SLASH_COMMANDS_EPIC_RPG["cards slots"]} '
        f'to turn these into a random **playing** card\n'
        f'{emojis.BP} Slotting cards will only give you playing cards you don\'t have yet\n'
    )
    playing_cards = (
        f'{emojis.BP} There are 52 playing cards in total\n'
        f'{emojis.BP} Playing cards will be used with the upcoming {strings.SLASH_COMMANDS_EPIC_RPG["cards hand"]} command\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["cards deck"]} to see your current playing cards\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CARDS GUIDE',
        description = 'What are those monsters even doing with cards?'
    )
    embed.add_field(name='WHAT ARE CARDS?', value=overview, inline=False)
    embed.add_field(name='SLOTTING CARDS', value=slotting_cards, inline=False)
    embed.add_field(name='PLAYING CARDS', value=playing_cards, inline=False)
    return embed


async def embed_cards_sources() -> discord.Embed:
    """Cards sources guide"""
    monsters = (
        f'{emojis.BP} Areas 1-3: {emojis.CARD_COMMON} common\n'
        f'{emojis.BP} Areas 4-5 : {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.BP} Areas 6-8 : {emojis.CARD_RARE} rare\n'
        f'{emojis.BP} Areas 9-10 : {emojis.CARD_EPIC} EPIC\n'
        f'{emojis.BP} Areas 11-13 : {emojis.CARD_OMEGA} OMEGA\n'
        f'{emojis.BP} Areas 14-15 : {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.BP} Areas 16-19 : {emojis.CARD_VOID} VOID\n'
        f'{emojis.BP} Area 20 : {emojis.CARD_ETERNAL} ETERNAL\n'
    )
    chop_commands = (
        f'{emojis.BP} {emojis.LOG} wooden logs: {emojis.CARD_COMMON} common\n'
        f'{emojis.BP} {emojis.LOG_EPIC} EPIC logs: {emojis.CARD_COMMON} common\n'
        f'{emojis.BP} {emojis.LOG_SUPER} SUPER logs: {emojis.CARD_COMMON} common\n'
        f'{emojis.BP} {emojis.LOG_MEGA} MEGA logs: {emojis.CARD_RARE} rare\n'
        f'{emojis.BP} {emojis.LOG_HYPER} HYPER logs: {emojis.CARD_RARE} rare\n'
        f'{emojis.BP} {emojis.LOG_ULTRA} ULTRA logs: {emojis.CARD_RARE} rare\n'
        f'{emojis.BP} {emojis.LOG_ULTIMATE} ULTIMATE logs: {emojis.CARD_ETERNAL} ETERNAL\n'
    )
    fish_commands = (
        f'{emojis.BP} {emojis.FISH} normie fish: {emojis.CARD_COMMON} common\n'
        f'{emojis.BP} {emojis.FISH_GOLDEN} golden fish: {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.BP} {emojis.FISH_EPIC} EPIC fish: {emojis.CARD_RARE} rare\n'
        f'{emojis.BP} {emojis.FISH_SUPER} SUPER fish: {emojis.CARD_ETERNAL} ETERNAL\n'
    )
    pickup_commands = (
        f'{emojis.BP} {emojis.APPLE} apples: {emojis.CARD_COMMON} common\n'
        f'{emojis.BP} {emojis.BANANA} bananas: {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.BP} {emojis.WATERMELON} watermelon: {emojis.CARD_ETERNAL} ETERNAL\n'
    )
    mine_commands = (
        f'{emojis.BP} {emojis.COIN} coins: {emojis.CARD_COMMON} common\n'
        f'{emojis.BP} {emojis.RUBY} rubies: {emojis.CARD_UNCOMMON} uncommon\n'
    )
    farm_command = (
        f'{emojis.BP} {emojis.POTATO} potatoes: {emojis.CARD_EPIC} EPIC\n'
        f'{emojis.BP} {emojis.BREAD} bread: {emojis.CARD_EPIC} EPIC\n'
        f'{emojis.BP} {emojis.CARROT} carrots: {emojis.CARD_EPIC} EPIC\n'
    )
    note = (
        f'{emojis.BP} Every monster or material can drop exactly **once**\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["cards info"]} to track your drops so far\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["area guide"]} to see all monsters in an area\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["monster search"]} to look up monsters by name\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CARD SOURCES',
    )
    embed.add_field(name='MONSTERS', value=monsters, inline=False)
    embed.add_field(name='CHOP WORK COMMANDS', value=chop_commands, inline=False)
    embed.add_field(name='FISH WORK COMMANDS', value=fish_commands, inline=False)
    embed.add_field(name='PICKUP WORK COMMANDS', value=pickup_commands, inline=False)
    embed.add_field(name='MINE WORK COMMANDS', value=mine_commands, inline=False)
    embed.add_field(name='FARM COMMAND', value=farm_command, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed