# main.py
"""Contains the main events, error handling and the help and about commands"""

from datetime import datetime
from typing import List

import discord
from discord.ext import commands

import database
from resources import emojis
from resources import settings, strings


class MainOldCog(commands.Cog):
    """Cog with events and help and about commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Commands
    @commands.command(name='help',aliases=('guide','g','h',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def main_help(self, ctx: commands.Context):
        """Main help command"""
        embeds = await embed_main_help(ctx)
        await ctx.send(embeds=embeds)

    @commands.command(aliases=('statistic','statistics,','devstat','ping','devstats','info','stats','privacy'))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def about(self, ctx: commands.Context):
        """Shows some bot info"""
        start_time = datetime.utcnow()
        message = await ctx.send('Testing API latency...')
        end_time = datetime.utcnow()
        api_latency = end_time - start_time
        embed = await embed_about(self.bot, ctx, api_latency)
        await message.edit(content=None, embed=embed)

    # Events
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        """Runs when an error occurs and handles them accordingly.
        Interesting errors get written to the database for further review.
        """
        async def send_error() -> None:
            """Sends error message as embed"""
            embed = discord.Embed(title='An error occured')
            embed.add_field(name='Command', value=f'`{ctx.command.qualified_name}`', inline=False)
            embed.add_field(name='Error', value=f'```\n{error}\n```', inline=False)
            await ctx.send(embed=embed)

        error = getattr(error, 'original', error)
        if isinstance(error, (commands.CommandNotFound, commands.NotOwner, database.DirectMessageError)):
            return
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'Command `{ctx.command.qualified_name}` is temporarily disabled.')
        elif isinstance(error, (commands.MissingPermissions, commands.MissingRequiredArgument,
                                commands.TooManyArguments, commands.BadArgument)):
            await send_error()
        elif isinstance(error, commands.BotMissingPermissions):
            if 'send_messages' in error.missing_permissions:
                return
            if 'embed_links' in error.missing_permissions:
                await ctx.send(error)
            else:
                await send_error()
        elif isinstance(error, database.FirstTimeUser):
            await ctx.send(
                f'Hey there, **{ctx.author.name}**. Looks like we haven\'t met before.\n'
                f'I have set your progress to **TT 0**, **not ascended**.\n\n'
                f'** --> Please use `{ctx.prefix}{ctx.invoked_with}` again to use the bot.**\n\n'
                f'• If you don\'t know what this means, you probably haven\'t time traveled yet and are in TT 0. '
                f'Check out `{ctx.prefix}tt` for some details.\n'
                f'• If you are in a higher TT, please use `{ctx.prefix}setprogress` (or `{ctx.prefix}sp`) '
                f'to change your settings.\n\n'
                f'These settings are used by some guides (like the area guides) to only show you what is relevant '
                f'to your current progress.'
            )
        else:
            await database.log_error(error, ctx)
            if settings.DEBUG_MODE or ctx.author.id == settings.OWNER_ID: await send_error()


# Initialization
def setup(bot):
    bot.add_cog(MainOldCog(bot))


# --- Embeds ---
async def embed_main_help(ctx: commands.Context) -> List[discord.Embed]:
    """Main menu embed"""
    prefix = ctx.prefix
    seasonal_event = f'{emojis.BP} `{prefix}easter` / `{prefix}egg` : Easter event guide\n'
    progress = (
        f'{emojis.BP} `{prefix}start` : Starter guide for new players\n'
        f'{emojis.BP} `{prefix}areas` / `{prefix}a` : Area guides overview\n'
        f'{emojis.BP} `{prefix}dungeons` / `{prefix}d` : Dungeon guides overview\n'
        f'{emojis.BP} `{prefix}timetravel` / `{prefix}tt` : Time travel guide\n'
        f'{emojis.BP} `{prefix}coolness` : Everything known about {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} `{prefix}ultraining` / `{prefix}ultr` : Ultraining guide\n'
    )
    crafting = (
        f'{emojis.BP} `{prefix}craft` : Recipes mats calculator\n'
        f'{emojis.BP} `{prefix}dismantle` / `{prefix}dm` : Dismantling calculator\n'
        f'{emojis.BP} `{prefix}invcalc` / `{prefix}ic` : Inventory calculator\n'
        f'{emojis.BP} `{prefix}drops` : Monster drops\n'
        f'{emojis.BP} `{prefix}enchants` / `{prefix}e` : Enchants'
    )
    animals = (
        f'{emojis.BP} `{prefix}horse` : Horse guide\n'
        f'{emojis.BP} `{prefix}pet` : Pets guide\n'
    )
    trading = f'{emojis.BP} `{prefix}trading` : Trading guides overview'
    professions_value = f'{emojis.BP} `{prefix}professions` / `{prefix}pr` : Professions guide'
    guild_overview = f'{emojis.BP} `{prefix}guild` : Guild guide'
    event_overview = f'{emojis.BP} `{prefix}events` : Event guides overview'
    monsters = (
        f'{emojis.BP} `{prefix}mobs [area]` : List of all monsters in area [area]\n'
        f'{emojis.BP} `{prefix}dailymob` : Where to find the daily monster'
    )
    gambling_overview = f'{emojis.BP} `{prefix}gambling` : Gambling guides overview'
    misc = (
        f'{emojis.BP} `{prefix}calc` : A basic calculator\n'
        f'{emojis.BP} `{prefix}codes` : Redeemable codes\n'
        f'{emojis.BP} `{prefix}duel` : Duelling weapons\n'
        f'{emojis.BP} `{prefix}farm` : Farming guide\n'
        f'{emojis.BP} `{prefix}returning` : Returning event guide\n'
        f'{emojis.BP} `{prefix}tip` : A handy dandy random tip\n'
        f'{emojis.BP} `{prefix}title` / `{prefix}t`  : Titles / Achievements\n'
    )
    botlinks = (
        f'{emojis.BP} `{prefix}invite` : Invite me to your server\n'
        f'{emojis.BP} `{prefix}support` : Visit the support server\n'
        f'{emojis.BP} `{prefix}links` : EPIC RPG wiki & support'
    )
    field_settings = (
        f'{emojis.BP} `{prefix}settings` / `{prefix}me` : Check your user settings\n'
        f'{emojis.BP} `{prefix}setprogress` / `{prefix}sp` : Change your user settings\n'
        f'{emojis.BP} `{prefix}prefix` : Check/set the prefix'
    )
    field_slash_info = (
        f'Yo, hey, I now support slash commands! Use {strings.SLASH_COMMANDS_GUIDE["help"]} to check it out.\n'
        f'If you can\'t see of any of my slash commands, click [here]({strings.LINK_INVITE}) to reinvite me with '
        f'the proper permissions.\n'
        f'Note that new or improved features will be slash only.'
    )
    embed_slash = discord.Embed(
        color = settings.EMBED_COLOR,
        title='SLASH COMMANDS ARE HERE!',
        description=field_slash_info
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EPIC RPG GUIDE',
        description = f'Hey **{ctx.author.name}**, what do you want to know?'
    )
    embed.set_footer(text='Note: This is not an official guide bot.')
    #embed.add_field(name=f'EASTER EVENT 2022 {emojis.EASTER_EGG}', value=seasonal_event, inline=False)
    embed.add_field(name='PROGRESS', value=progress, inline=False)
    embed.add_field(name='CRAFTING', value=crafting, inline=False)
    embed.add_field(name='HORSE & PETS', value=animals, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='PROFESSIONS', value=professions_value, inline=False)
    embed.add_field(name='GUILD', value=guild_overview, inline=False)
    embed.add_field(name='EVENTS', value=event_overview, inline=False)
    embed.add_field(name='MONSTERS', value=monsters, inline=False)
    embed.add_field(name='GAMBLING', value=gambling_overview, inline=False)
    embed.add_field(name='MISC', value=misc, inline=False)
    embed.add_field(name='LINKS', value=botlinks, inline=False)
    embed.add_field(name='SETTINGS', value=field_settings, inline=False)
    return [embed_slash, embed]


async def embed_about(bot: commands.Bot, ctx: commands.Context, api_latency: datetime) -> discord.Embed:
    """Bot info embed"""
    user_count, *_ = await database.get_user_number(ctx)
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
        f'{emojis.BP} {round(bot.latency * 1000):,} ms average latency'
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
    documents = (
        f'{emojis.BP} [Privacy Policy](https://erg.zoneseven.ch/privacy.html)\n'
        f'{emojis.BP} [Terms of Service](https://erg.zoneseven.ch/terms.html)\n'
    )
    embed = discord.Embed(color = settings.EMBED_COLOR, title = 'ABOUT EPIC RPG GUIDE')
    embed.add_field(name='BOT STATS', value=general, inline=False)
    embed.add_field(name='CURRENT SHARD', value=current_shard_status, inline=False)
    embed.add_field(name='CREATOR', value=creator, inline=False)
    embed.add_field(name='SPECIAL THANKS TO', value=thanks, inline=False)
    embed.add_field(name='PRIVACY POLICY & TOS', value=documents, inline=False)
    return embed