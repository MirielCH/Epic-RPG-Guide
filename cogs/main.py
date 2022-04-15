# main.py
"""Contains the main events, error handling and the help and about commands"""

import aiohttp

import discord
from discord.commands import slash_command, Option
from discord.ext import commands, tasks

from content import main
import database
from resources import logs, settings, strings


class MainCog(commands.Cog):
    """Cog with events and help and about commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Tasks
    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        """Updates top.gg guild count"""
        if settings.DBL_TOKEN is None: return
        guilds = len(list(self.bot.guilds))
        guild_count = {'server_count':guilds}
        header = {'Authorization':settings.DBL_TOKEN}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://top.gg/api/bots/770199669141536768/stats',
                                        data=guild_count,headers=header) as request:
                    logs.logger.info(
                        f'Posted server count ({guilds}), status code: {request.status}'
                    )
        except Exception as error:
            logs.logger.error(f'Failed to post server count: {error}')

    # Events
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        """Runs when an error occurs and handles them accordingly.
        Interesting errors get written to the database for further review.
        """
        async def send_error() -> None:
            """Sends error message as embed"""
            embed = discord.Embed(title='An error occured')
            command_name = f'{ctx.command.full_parent_name} {ctx.command.name}'.strip()
            embed.add_field(name='Command', value=f'`{command_name}`', inline=False)
            embed.add_field(name='Error', value=f'```py\n{error}\n```', inline=False)
            await ctx.respond(embed=embed, ephemeral=True)

        error = getattr(error, 'original', error)
        if isinstance(error, commands.NoPrivateMessage):
            if ctx.guild_id is None:
                await ctx.respond(
                    f'I\'m sorry, this command is not available in DMs because it needs to be able to read EPIC RPG.\n\n'
                    f'Please use this command in a server channel where you also have access to EPIC RPG.',
                    ephemeral=True
                )
            else:
                await ctx.respond(
                    f'I\'m sorry, this command is not available in this server because it needs to be able to read EPIC RPG.\n\n'
                    f'To allow this, the server admin needs to reinvite me with the necessary permissions.\n'
                    f'To do that click [here]({settings.LINK_INVITE}).\n',
                    ephemeral=True
                )
        elif isinstance(error, (commands.MissingPermissions, commands.MissingRequiredArgument,
                                commands.TooManyArguments, commands.BadArgument)):
            await send_error()
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond(
                f'You can\'t use this command here, because I can\'t read EPIC RPG in this channel.\n'
                f'To enable this, I need to have a role and that role needs the permission `View Channel` / '
                f'`Read Messages` in this channel.',
                ephemeral=True
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(
                f'Yo hey, calm down, this is an oracle, not a spam box, wait another {error.retry_after:.1f}s, will ya.',
                ephemeral=True
            )
        else:
            await database.log_error(error, ctx)
            if settings.DEBUG_MODE or ctx.author.id == settings.OWNER_ID: await send_error()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Fires when bot has finished starting"""
        startup_info = f'{self.bot.user.name} has connected to Discord!'
        print(startup_info)
        logs.logger.info(startup_info)
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

    # Commands
    @slash_command(description='Main help command')
    async def help(self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION,
                           choices=main.TOPICS, default=main.TOPIC_GUIDES),
    ) -> None:
        """Main help command"""
        await main.command_help(ctx, topic)

    @slash_command(description='Some info and links about Epic RPG Guide')
    async def about(self, ctx: discord.ApplicationContext) -> None:
        """About command"""
        await main.command_about(self.bot, ctx)

# Initialization
def setup(bot):
    bot.add_cog(MainCog(bot))