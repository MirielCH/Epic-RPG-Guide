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
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
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
    await functions.edit_interaction(interaction, view=None)


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
    seasonal_event = f'{emojis.BP} {emojis.LOGO}`/valentine guide` : Valentine event guide\n'
    guides = (
        f'{emojis.BP} {emojis.LOGO}`/area guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/beginner guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/coolness guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/dungeon guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/enchanting guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/event guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/farming guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/gambling guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/guild guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/horse guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/pet guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/profession guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/time-travel guide`\n'
        f'{emojis.BP} {emojis.LOGO}`/time-travel details`\n'
        f'{emojis.BP} {emojis.LOGO}`/ultraining guide`\n'
    )
    trade_rates = (
        f'{emojis.BP} {emojis.LOGO}`/trade rates` : Overview of all trade rates\n'
    )
    monsters = (
        f'{emojis.BP} {emojis.LOGO}`/monster drops` : Monster drops and where to find them\n'
        f'{emojis.BP} {emojis.LOGO}`/monster search` : Look up monsters or the daily monster\n'
    )
    achievements = f'{emojis.BP} {emojis.LOGO}`/title search` : Look up titles / achievements\n'
    misc = (
        f'{emojis.BP} {emojis.LOGO}`/ask the oracle` : A very useless command\n'
        f'{emojis.BP} {emojis.LOGO}`/badges` : All badges and how to get them\n'
        f'{emojis.BP} {emojis.LOGO}`/codes` : All current redeemable codes\n'
        f'{emojis.BP} {emojis.LOGO}`/duel weapons` : What every weapon does in duels\n'
        f'{emojis.BP} {emojis.LOGO}`/tip` : A handy dandy random tip\n'
    )
    field_settings = (
        f'{emojis.BP} {emojis.LOGO}`/settings` : View your current settings\n'
        f'{emojis.BP} {emojis.LOGO}`/set progress` : Set your progress to get fitting guides\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EPIC RPG GUIDES',
    )
    embed.set_footer(text='Note: This is not an official bot.')
    #embed.add_field(name=f'VALENTINE EVENT 2022 {emojis.COIN_LOVE}', value=seasonal_event, inline=False)
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
        f'{emojis.BP} {emojis.LOGO}`/area check` : Check if you\'re ready for an area\n'
        f'{emojis.BP} {emojis.LOGO}`/dungeon check` : Check if you\'re ready for a dungeon\n'
    )
    coincap = (
        f'{emojis.BP} {emojis.LOGO}`/coin-cap calculator` : Calculate the coin cap for a TT/area\n'
    )
    crafting = (
        f'{emojis.BP} {emojis.LOGO}`/crafting calculator` : Recipes mats calculator\n'
        f'{emojis.BP} {emojis.LOGO}`/dismantling calculator` : Dismantling calculator\n'
        f'{emojis.BP} {emojis.LOGO}`/inventory calculator` : Convert your inventory into one material\n'
    )
    timetravel = (
        f'{emojis.BP} {emojis.LOGO}`/time-jump score calculator` : Calculate the time jump score of your inventory\n'
    )
    horse = (
        f'{emojis.BP} {emojis.LOGO}`/horse boost calculator` : Calculate horse boosts\n'
        f'{emojis.BP} {emojis.LOGO}`/horse training calculator` : Calculate horse training cost\n'
    )
    pet = (
        f'{emojis.BP} {emojis.LOGO}`/pet fuse` : See the recommended tiers for a pet fusion\n'
    )
    drop_chance = f'{emojis.BP} {emojis.LOGO}`/dropchance calculator` : Calculate your monster drop chance\n'
    trading = f'{emojis.BP} {emojis.LOGO}`/trade calculator` : Calculate materials after trading'
    professions = f'{emojis.BP} {emojis.LOGO}`/profession calculator` : Calculate what you need to level professions'
    ultraining = f'{emojis.BP} {emojis.LOGO}`/ultraining stats calculator` : Calculate stats for an ultraining stage'
    misc = (
        f'{emojis.BP} {emojis.LOGO}`/calculator` : A basic calculator\n'
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
        f'{emojis.BP} r5#2253\n'
        f'{emojis.BP} All the math geniuses in the support server'
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