# main.py
"""Contains the main events, error handling and the help and about commands"""

import discord
from discord.ext import commands

import database
from resources import functions, settings, strings


class MainOldCog(commands.Cog):
    """Cog with events and help and about commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Commands
    @commands.command(name='help',aliases=('guide','g','h',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def main_help(self, ctx: commands.Context):
        """Main help command"""
        await functions.send_slash_migration_message(ctx, 'help')

    @commands.command(aliases=('statistic','statistics,','devstat','ping','devstats','info','stats','privacy'))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def about(self, ctx: commands.Context):
        """Shows some bot info"""
        await functions.send_slash_migration_message(ctx, 'about')

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
                f'Please use {strings.SLASH_COMMANDS_GUIDE["help"]} to see the commands of the bot.\n\n'
                f'• If you don\'t know what TT means, you probably haven\'t time traveled yet and are in TT 0. '
                f'Check out {strings.SLASH_COMMANDS_GUIDE["time travel guide"]} for some details.\n'
                f'• If you are in a higher TT, please use {strings.SLASH_COMMANDS_GUIDE["set progress"]}'
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