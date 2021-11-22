# main.py
"""Contains the main events, error handling and the help and about commands"""

import aiohttp
from datetime import datetime
from typing import Tuple

import discord
from discord.ext import commands, tasks

import database
import emojis
import global_data


class MainCog(commands.Cog):
    """Cog with events and help and about commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Tasks
    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        """Updates top.gg guild count"""
        try:
            if global_data.DBL_TOKEN != 'none':
                guilds = len(list(self.bot.guilds))
                guild_count = {'server_count':guilds}
                header = {'Authorization':global_data.DBL_TOKEN}
                async with aiohttp.ClientSession() as session:
                    async with session.post('https://top.gg/api/bots/770199669141536768/stats',
                                            data=guild_count,headers=header) as request:
                        global_data.logger.info(
                            f'Posted server count ({guilds}), status code: {request.status}'
                            )
        except Exception as error:
            global_data.logger.error(f'Failed to post server count: {error}')


    # Commands
    @commands.command(name='help',aliases=('guide','g','h',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def main_help(self, ctx: commands.Context):
        """Main help command"""
        prefix = await database.get_prefix(ctx)
        embed = await embed_main_help(ctx)
        await ctx.send(embed=embed)

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

        if isinstance(error, (commands.CommandNotFound, database.FirstTimeUser, commands.NotOwner)):
            return
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'Command `{ctx.command.qualified_name}` is temporarily disabled.')
        elif isinstance(error, (commands.MissingPermissions, commands.MissingRequiredArgument,
                                commands.TooManyArguments, commands.BadArgument)):
            await send_error()
        elif isinstance(error, commands.BotMissingPermissions):
            if 'send_messages' in error.missing_perms:
                return
            if 'embed_links' in error.missing_perms:
                await ctx.send(error)
            else:
                await send_error()
        else:
            await database.log_error(ctx, error)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Fires when bot has finished starting"""
        #DiscordComponents(bot)

        startup_info = f'{self.bot.user.name} has connected to Discord!'
        print(startup_info)
        global_data.logger.info(startup_info)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                                 name='your questions'))
        if not self.update_stats.is_running(): await self.update_stats.start()

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Sends welcome message on guild join"""
        try:
            prefix = await database.get_prefix(self.bot, guild, True)
            welcome_message = (
                f'Hello **{guild.name}**! I\'m here to provide some guidance!\n\n'
                f'To get a list of all topics, type `{prefix}guide` (or `{prefix}g` for short).\n'
                f'If you don\'t like this prefix, use `{prefix}setprefix` to change it.\n\n'
                f'Tip: If you ever forget the prefix, simply ping me with a command.\n\n'
            )
            await guild.system_channel.send(welcome_message)
        except:
            return


# Initialization
def setup(bot):
    bot.add_cog(MainCog(bot))


# --- Embeds ---
async def embed_main_help(ctx: commands.Context) -> discord.Embed:
    """Main menu embed"""
    prefix = ctx.prefix
    seasonal_event = f'{emojis.BP} `{prefix}halloween` / `{prefix}hal` : Halloween guide\n'
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
        f'{emojis.BP} `{prefix}tip` : A handy dandy random tip'
    )
    botlinks = (
        f'{emojis.BP} `{prefix}invite` : Invite me to your server\n'
        f'{emojis.BP} `{prefix}support` : Visit the support server\n'
        f'{emojis.BP} `{prefix}links` : EPIC RPG wiki & support'
    )
    settings = (
        f'{emojis.BP} `{prefix}settings` / `{prefix}me` : Check your user settings\n'
        f'{emojis.BP} `{prefix}setprogress` / `{prefix}sp` : Change your user settings\n'
        f'{emojis.BP} `{prefix}prefix` : Check/set the prefix'
    )
    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'EPIC RPG GUIDE',
        description = f'Hey **{ctx.author.name}**, what do you want to know?'
    )
    embed.set_footer(text='Note: This is not an official guide bot.')
    #embed.add_field(name=f'HALLOWEEN 2021 {emojis.HAL_PUMPKIN}', value=seasonal_event, inline=False)
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
    embed.add_field(name='SETTINGS', value=settings, inline=False)
    return embed


async def embed_about(bot: commands.Bot, ctx: commands.Context, api_latency: datetime) -> discord.Embed:
    """Bot info embed"""
    user_count, *_ = await database.get_user_number(ctx)
    closed_shards = 0
    for shard_id in bot.shards:
        shard = bot.get_shard(shard_id)
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
        f'{emojis.BP} All the math geniuses in the support server'
    )
    privacy = (
        f'{emojis.BP} You can find this bot\'s privacy policy [here]'
        f'(https://docs.google.com/document/d/1CStt8k902m5s5CUb2RyPTTN-dmb-N2FAONfxzm7eAio/edit?usp=sharing).\n'
    )
    embed = discord.Embed(color = global_data.EMBED_COLOR, title = 'ABOUT EPIC RPG GUIDE')
    embed.add_field(name='BOT STATS', value=general, inline=False)
    embed.add_field(name='CURRENT SHARD', value=current_shard_status, inline=False)
    embed.add_field(name='CREATOR', value=creator, inline=False)
    embed.add_field(name='SPECIAL THANKS TO', value=thanks, inline=False)
    embed.add_field(name='PRIVACY POLICY', value=privacy, inline=False)
    return embed