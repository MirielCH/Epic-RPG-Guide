# main.py
"""Contains the main events, error handling and the help and about commands"""

from datetime import datetime
import sys
from typing import Optional, Tuple
from humanfriendly import format_timespan
import psutil

import discord
from discord.ext import commands

import database
from resources import components, emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_GUIDES = 'Guides'
TOPIC_CALCULATORS = 'Calculators'

TOPICS = [
    TOPIC_GUIDES,
    TOPIC_CALCULATORS,
]


# --- Views ---
class HelpView(discord.ui.View):
    """View with a topic select and link buttons.
    Also needs the interaction of the response with the view, so do TopicView.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    topics: Topics to select from - dict (description: function). The functions need to return an embed and have one
    argument (context)
    active_topic: Currently chosen topic

    Returns
    -------
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: discord.ApplicationContext, topics: dict, active_topic: str,
                 placeholder: Optional[str] = 'Choose topic ...',
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.topics = topics
        self.active_topic = active_topic
        self.placeholder = placeholder
        self.add_item(components.TopicSelect(self.topics, self.active_topic, self.placeholder, row=0))
        self.add_item(discord.ui.Button(label="Invite", style=discord.ButtonStyle.link, url=strings.LINK_INVITE, row=1))
        self.add_item(discord.ui.Button(label="Support", style=discord.ButtonStyle.link, url=strings.LINK_SUPPORT, row=1))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
        #    await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
         #   return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class LinksView(discord.ui.View):
    """View with link buttons."""
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Invite", style=discord.ButtonStyle.link, url=strings.LINK_INVITE))
        self.add_item(discord.ui.Button(label="Support", style=discord.ButtonStyle.link, url=strings.LINK_SUPPORT))
        self.add_item(discord.ui.Button(label="Vote", style=discord.ButtonStyle.link, url=strings.LINK_VOTE))


# --- Commands ---
async def command_help(ctx: discord.ApplicationContext, topic: str) -> None:
    """Help command"""
    topics_functions = {
        TOPIC_GUIDES: embed_help_guides,
        TOPIC_CALCULATORS: embed_help_calculators,
    }
    view = HelpView(ctx, topics_functions, active_topic=topic)
    embed = await topics_functions[topic]()
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    try:
        await functions.edit_interaction(interaction, view=None)
    except discord.errors.NotFound:
        pass


async def command_about(bot: discord.Bot, ctx: discord.ApplicationContext) -> None:
    """About command"""
    start_time = datetime.utcnow()
    interaction = await ctx.respond('Testing API latency...')
    end_time = datetime.utcnow()
    api_latency = end_time - start_time
    image, embed = await embed_about(bot, ctx, api_latency)
    view = LinksView()
    await functions.edit_interaction(interaction, content=None, file=image, embed=embed, view=view)


# --- Embeds ---
async def embed_help_guides() -> discord.Embed:
    """Main menu embed"""
    seasonal_event = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["halloween guide"]}\n'
    )
    guides = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["alchemy guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["area guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["artifacts guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["beginner guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["cards guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["coolness guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["dungeon guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["enchanting guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["event guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["farming guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["gambling guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["guild guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["horse guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["pets guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["professions guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["time jump score"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["time travel guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["time travel bonuses"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["trade guide"]}\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["ultraining guide"]}\n'
    )
    trade_rates = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["trade rates"]} : Overview of all trade rates\n'
    )
    monsters = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["monster drops"]} : Monster drops and where to find them\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["monster search"]} : Look up monsters or the daily monster\n'
    )
    achievements = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["achievement search"]} : Look up titles / achievements\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["title search"]} : Look up titles / achievements\n'
    )
    misc = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["ask the oracle"]} : A very useful command\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["badges"]} : All badges and how to get them\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["codes"]} : All current redeemable codes\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["complain"]} : Sometimes you just gotta vent\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["duel weapons"]} : What every weapon does in duels\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["tip"]} : A handy dandy random tip\n'
    )
    field_settings = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["settings"]} : View your current settings\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["set progress"]} : Set your progress to get fitting guides\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EPIC RPG GUIDES',
    )
    embed.set_footer(text='Note: This is not an official bot.')
    embed.add_field(name=f'HALLOWEEN GUIDE {emojis.HAL_PUMPKIN}', value=seasonal_event, inline=False)
    embed.add_field(name='GUIDES', value=guides, inline=False)
    embed.add_field(name='ACHIEVEMENTS / TITLES', value=achievements, inline=False)
    embed.add_field(name='MONSTERS', value=monsters, inline=False)
    embed.add_field(name='TRADE RATES', value=trade_rates, inline=False)
    embed.add_field(name='MISC', value=misc, inline=False)
    embed.add_field(name='SETTINGS', value=field_settings, inline=False)
    return embed


async def embed_help_calculators() -> discord.Embed:
    """Main menu embed"""
    checks = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["area check"]} : Check if you\'re ready for an area\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["dungeon check"]} : Check if you\'re ready for a dungeon\n'
    )
    coincap = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["coin cap calculator"]} : Calculate the coin cap for a TT/area\n'
    )
    crafting = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["crafting calculator"]} : Recipes mats calculator\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["dismantling calculator"]} : Dismantling calculator\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["inventory calculator"]} : Convert your inventory into one material\n'
    )
    timetravel = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["time jump calculator"]} : Calculate the time jump score of your inventory\n'
    )
    horse = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["horse boost calculator"]} : Calculate horse boosts\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["horse training calculator"]} : Calculate horse training cost\n'
    )
    pet = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["pets fuse"]} : See the recommended tiers for a pet fusion\n'
    )
    drop_chance = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["drop chance calculator"]} : Calculate your monster drop chance\n'
    )
    trading = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["trade calculator"]} : Calculate materials after trading\n'
        f'{emojis.BP} `rpg i <area>` : Quickly calculate trades for your current inventory\n'
        f'{emojis.DETAIL} _This calculator can be toggled in {strings.SLASH_COMMANDS_GUIDE["settings"]}_'
    )
    professions = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["professions calculator"]} : Calculate what you need to level professions'
    )
    ultraining = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["ultraining stats calculator"]} : Calculate stats for an ultraining stage'
    )
    misc = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_GUIDE["calculator"]} : A basic calculator\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EPIC RPG CALCULATORS',
    )
    embed.set_footer(text='Note: This is not an official bot.')
    embed.add_field(name='COIN CAP', value=coincap, inline=False)
    embed.add_field(name='CRAFTING', value=crafting, inline=False)
    embed.add_field(name='DAMAGE CHECKS', value=checks, inline=False)
    embed.add_field(name='DROP CHANCE', value=drop_chance, inline=False)
    embed.add_field(name='HORSE', value=horse, inline=False)
    embed.add_field(name='PETS', value=pet, inline=False)
    embed.add_field(name='PROFESSIONS', value=professions, inline=False)
    embed.add_field(name='TIME TRAVEL', value=timetravel, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='ULTRAINING', value=ultraining, inline=False)
    embed.add_field(name='MISC', value=misc, inline=False)
    return embed


async def embed_about(
    bot: commands.Bot, ctx: discord.ApplicationContext, api_latency: datetime
) -> Tuple[discord.File, discord.Embed]:
    """Bot info embed"""
    user_count = await database.get_user_count()
    closed_shards = 0
    for shard in bot.shards.values():
        if shard is not None:
            if shard.is_closed(): closed_shards += 1
        else:
            closed_shards += 1
    settings_db = await database.get_settings()
    uptime = datetime.utcnow().replace(microsecond=0) - datetime.fromisoformat(settings_db['startup_time'])
    general = (
        f'{emojis.BP} {len(bot.guilds):,} servers\n'
        f'{emojis.BP} {user_count:,} users\n'
        f'{emojis.BP} {len(bot.shards):,} shards ({closed_shards:,} shards offline)\n'
        f'{emojis.BP} {round(bot.latency * 1000):,} ms average bot latency\n'
        f'{emojis.BP} Online for {format_timespan(uptime)}'
    )
    if ctx.guild is not None:
        current_shard = bot.get_shard(ctx.guild.shard_id)
        bot_latency = f'{round(current_shard.latency * 1000):,} ms' if current_shard is not None else 'N/A'
        current_shard_status = (
            f'{emojis.BP} Shard: {ctx.guild.shard_id + 1} of {len(bot.shards):,}\n'
            f'{emojis.BP} Bot latency: {bot_latency}\n'
            f'{emojis.BP} API latency: {round(api_latency.total_seconds() * 1000):,} ms'
        )
    creator = f'{emojis.BP} Miriel#0001'
    thanks = (
        f'{emojis.BP} FlyingPanda#0328\n'
        f'{emojis.BP} Hakiobo#6097\n'
        f'{emojis.BP} r5#2253\n'
        f'{emojis.BP} Everyone contributing one way or the other'
    )
    documents = (
        f'{emojis.BP} [Privacy Policy](https://erg.zoneseven.ch/privacy.html)\n'
        f'{emojis.BP} [Terms of Service](https://erg.zoneseven.ch/terms.html)\n'
    )
    dev_stuff = (
        f'{emojis.BP} Language: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n'
        f'{emojis.BP} Library: Pycord {discord.__version__}\n'
        f'{emojis.BP} System CPU usage: {psutil.cpu_percent()}%\n'
        f'{emojis.BP} System RAM usage: {psutil.virtual_memory()[2]}%\n'
    )
    img_raspi = discord.File(settings.IMG_RASPI, filename='raspi.png')
    image_url = 'attachment://raspi.png'
    embed = discord.Embed(color = settings.EMBED_COLOR, title = 'ABOUT EPIC RPG GUIDE')
    embed.add_field(name='BOT STATS', value=general, inline=False)
    if ctx.guild is not None:
        embed.add_field(name='CURRENT SHARD', value=current_shard_status, inline=False)
    embed.add_field(name='CREATOR', value=creator, inline=False)
    embed.add_field(name='SPECIAL THANKS TO', value=thanks, inline=False)
    embed.add_field(name='PRIVACY POLICY & TOS', value=documents, inline=False)
    embed.add_field(name='DEV STUFF', value=dev_stuff, inline=False)
    embed.add_field(name='PROUDLY HOSTED ON THIS RASPBERRY PI 4', value=f'** **', inline=False)
    embed.set_image(url=image_url)
    return (img_raspi, embed)