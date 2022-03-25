# main.py
"""Contains the main events, error handling and the help and about commands"""

from datetime import datetime

import discord
from discord.ext import commands

import database
from resources import emojis, settings, views


# --- Topics ---
TOPIC_GUIDES = 'Guides'
TOPIC_CALCULATORS = 'Calculators'

TOPICS = [
    TOPIC_GUIDES,
    TOPIC_CALCULATORS,
]


# --- Commands ---
async def command_help(ctx: discord.ApplicationContext, topic: str) -> None:
    """Help command"""
    topics_functions = {
        TOPIC_GUIDES: embed_help_guides,
        TOPIC_CALCULATORS: embed_help_calculators,
    }
    view = views.TopicView(ctx, topics_functions, active_topic=topic)
    embed = await topics_functions[topic]()
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    await interaction.edit_original_message(view=None)


async def command_about(bot: discord.Bot, ctx: discord.ApplicationContext) -> None:
    """About command"""
    start_time = datetime.utcnow()
    interaction = await ctx.respond('Testing API latency...')
    end_time = datetime.utcnow()
    api_latency = end_time - start_time
    embed = await embed_about(bot, ctx, api_latency)
    await interaction.edit_original_message(content=None, embed=embed)


# --- Embeds ---
async def embed_help_guides() -> discord.Embed:
    """Main menu embed"""
    seasonal_event = f'{emojis.BP} `/valentine guide` : Valentine event guide\n'
    guides = (
        #f'{emojis.BP} `/area guide`\n'
        f'{emojis.BP} `/beginner guide`\n'
        f'{emojis.BP} `/coolness guide`\n'
        #f'{emojis.BP} `/dungeon guide`\n'
        f'{emojis.BP} `/enchanting guide`\n'
        f'{emojis.BP} `/event guide`\n'
        f'{emojis.BP} `/farming guide`\n'
        f'{emojis.BP} `/gambling guide`\n'
        f'{emojis.BP} `/guild guide`\n'
        f'{emojis.BP} `/horse guide`\n'
        f'{emojis.BP} `/pet guide`\n'
        f'{emojis.BP} `/profession guide`\n'
        f'{emojis.BP} `/timetravel guide`\n'
        f'{emojis.BP} `/timetravel details`\n'
        f'{emojis.BP} `/ultraining guide`\n'
    )
    trade_rates = (
        f'{emojis.BP} `/trade rates` : Overview of all trade rates\n'
    )
    monsters = (
        f'{emojis.BP} `/monster drops` : Monster drops and where to find them\n'
        f'{emojis.BP} `/monster search` : Look up monsters or the daily monster\n'
    )
    achievements = f'{emojis.BP} `/title search` : Look up titles / achievements\n'
    misc = (
        f'{emojis.BP} `/ask the oracle` : A very useless command\n'
        f'{emojis.BP} `/badges` : All badges and how to get them\n'
        f'{emojis.BP} `/codes` : All current redeemable codes\n'
        f'{emojis.BP} `/duel weapons` : What every weapon does in duels\n'
        f'{emojis.BP} `/tip` : A handy dandy random tip\n'
    )
    botlinks = (
        f'{emojis.BP} `/invite` : Invite Epic RPG Guide to your server\n'
        f'{emojis.BP} `/support` : Visit the support server\n'
    )
    field_settings = (
        f'{emojis.BP} `/settings` : View your current settings\n'
        f'{emojis.BP} `/set progress` : Set your progress to get fitting guides\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EPIC RPG GUIDE: ALL GUIDES',
    )
    embed.set_footer(text='Note: This is not an official guide bot.')
    #embed.add_field(name=f'VALENTINE EVENT 2022 {emojis.COIN_LOVE}', value=seasonal_event, inline=False)
    embed.add_field(name='GUIDES', value=guides, inline=False)
    embed.add_field(name='ACHIEVEMENTS / TITLES', value=achievements, inline=False)
    embed.add_field(name='MONSTERS', value=monsters, inline=False)
    #embed.add_field(name='TRADE RATES', value=trade_rates, inline=False)
    embed.add_field(name='MISC', value=misc, inline=False)
    embed.add_field(name='LINKS', value=botlinks, inline=False)
    embed.add_field(name='SETTINGS', value=field_settings, inline=False)
    return embed


async def embed_help_calculators() -> discord.Embed:
    """Main menu embed"""
    checks = (
        f'{emojis.BP} `/area check` : Check if you\'re ready for an area\n'
        f'{emojis.BP} `/dungeon check` : Check if you\'re ready for a dungeon\n'
    )
    coincap = (
        f'{emojis.BP} `/coincap calculator` : Calculate the coin cap for a TT/area\n'
    )
    crafting = (
        f'{emojis.BP} `/craft` : Recipes mats calculator\n'
        f'{emojis.BP} `/dismantle` : Dismantling calculator\n'
        f'{emojis.BP} `/inventory calculator` : Convert your inventory into one material\n'
    )
    timetravel = (
        f'{emojis.BP} `/stt score calculator` : Calculate the STT score of your inventory\n'
    )
    horse = (
        f'{emojis.BP} `/horse boost calculator` : Calculate horse boosts\n'
        f'{emojis.BP} `/horse training calculator` : Calculate horse training cost\n'
    )
    pet = (
        f'{emojis.BP} `/pet fuse` : See the recommended tiers for a pet fusion\n'
    )
    drop_chance = f'{emojis.BP} `/dropchance calculator` : Calculate your monster drop chance\n'
    trading = f'{emojis.BP} `/trade calculator` : Calculate materials after trading'
    professions = f'{emojis.BP} `/profession calculator` : Calculate what you need to level professions'
    ultraining = f'{emojis.BP} `/ultraining calculator` : Calculate EPIC NPC damage in ultraining'
    misc = (
        f'{emojis.BP} `/calculator` : A basic calculator\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EPIC RPG GUIDE: CALCULATORS',
    )
    embed.set_footer(text='Note: This is not an official guide bot.')
    embed.add_field(name='COIN CAP', value=coincap, inline=False)
    embed.add_field(name='CRAFTING', value=crafting, inline=False)
    #embed.add_field(name='DAMAGE CHECKS', value=checks, inline=False)
    embed.add_field(name='DROP CHANCE', value=drop_chance, inline=False)
    embed.add_field(name='HORSE', value=horse, inline=False)
    embed.add_field(name='PETS', value=pet, inline=False)
    embed.add_field(name='PROFESSIONS', value=professions, inline=False)
    embed.add_field(name='TIME TRAVEL', value=timetravel, inline=False)
    #embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='ULTRAINING', value=ultraining, inline=False)
    embed.add_field(name='MISC', value=misc, inline=False)
    return embed


async def embed_about(bot: commands.Bot, ctx: discord.ApplicationContext, api_latency: datetime) -> discord.Embed:
    """Bot info embed"""
    user_count = await database.get_user_count()
    closed_shards = 0
    for shard in bot.shards.values():
        if shard is not None:
            if shard.is_closed(): closed_shards += 1
        else:
            closed_shards += 1
    general = (
        f'{emojis.BP} {len(bot.guilds):,} servers\n'
        f'{emojis.BP} {user_count:,} users\n'
        f'{emojis.BP} {len(bot.shards):,} shards ({closed_shards:,} shards offline)\n'
        f'{emojis.BP} {round(bot.latency * 1000):,} ms average bot latency\n'
    )
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
    privacy = (
        f'{emojis.BP} You can find this bot\'s privacy policy [here]'
        f'(https://docs.google.com/document/d/1CStt8k902m5s5CUb2RyPTTN-dmb-N2FAONfxzm7eAio/edit?usp=sharing).\n'
    )
    embed = discord.Embed(color = settings.EMBED_COLOR, title = 'ABOUT EPIC RPG GUIDE')
    embed.add_field(name='BOT STATS', value=general, inline=False)
    embed.add_field(name='CURRENT SHARD', value=current_shard_status, inline=False)
    embed.add_field(name='CREATOR', value=creator, inline=False)
    embed.add_field(name='SPECIAL THANKS TO', value=thanks, inline=False)
    embed.add_field(name='PRIVACY POLICY', value=privacy, inline=False)
    return embed