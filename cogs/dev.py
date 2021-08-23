# dev.py
"""Contains internal dev commands"""

import asyncio
import importlib

import discord
from discord.ext import commands

import database
import emojis
import global_data


class DevCog(commands.Cog):
    """Cog with internal dev commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Commands
    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def dev(self, ctx: commands.Context, *args: str) -> None:
        """Dev command group, lists all dev commands"""
        subcommands = ''
        for command in self.bot.walk_commands():
            if isinstance(command, commands.Group):
                if command.qualified_name == 'dev':
                    for subcommand in command.walk_commands():
                        if subcommand.parents[0] == command:
                            aliases = f'`{subcommand.qualified_name}`'
                            for alias in subcommand.aliases:
                                aliases = f'{aliases}, `{alias}`'
                            subcommands = f'{subcommands}{emojis.BP} {aliases}\n'
        await ctx.send(
            f'Available dev commands:\n'
            f'{subcommands}'
        )

    @dev.command()
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def reload(self, ctx: commands.Context, *args: str) -> None:
        """Reloads modules and cogs"""
        if args:
            args = [arg.lower() for arg in args]
            arg, *_ = args
            actions = []
            if arg in ('lib','libs','modules','module'):
                importlib.reload(database)
                actions.append(f'Module \'database\' reloaded.')
                importlib.reload(emojis)
                actions.append(f'Module \'emojis\' reloaded.')
                importlib.reload(global_data)
                actions.append(f'Module \'global_data\' reloaded.')
            else:
                for arg in args:
                    cog_name = f'cogs.{arg}'
                    try:
                        result = self.bot.reload_extension(cog_name)
                        if result is None:
                            actions.append(f'Extension \'{cog_name}\' reloaded.')
                        else:
                            actions.append(f'{cog_name}: {result}')
                    except Exception as error:
                        actions.append(f'{cog_name}: {error}')
            message = ''
            for action in actions:
                message = f'{message}\n{action}'
            await ctx.send(message)
        else:
            await ctx.send('Uhm, what.')

    @dev.command()
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def shutdown(self, ctx: commands.Context) -> None:
        """Shuts down the bot (noisily)"""
        def check(m):
            return (m.author == ctx.author) and (m.channel == ctx.channel)

        user_name = ctx.author.name
        await ctx.send(
            f'**{user_name}**, are you **SURE**?\n'
            f'I have a wife {user_name}. A family. I have two kids, you know? '
            f'The youngest one has asthma but he\'s fighting it like a champ. I love them so much.\n'
            f'Do you really want to do this, {user_name}? Do you? `[yes/no]`'
            )
        try:
            answer = await self.bot.wait_for('message', check=check, timeout=30)
            if answer.content.lower() in ('yes','y'):
                await ctx.send(
                    f'Goodbye world.\n'
                    f'Goodbye my loved ones.\n'
                    f'Goodbye cruel {user_name}.\n'
                    f'Shutting down.'
                )
                await self.bot.close()
            else:
                await ctx.send(
                    'Oh thank god, thank you so much, I was really afraid there for a second. Bless you.'
                )
        except asyncio.TimeoutError as error:
            await ctx.send('Oh thank god, he forgot to answer.')

    # Enable/disable commands
    @dev.command(aliases=('disable',))
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def enable(self, ctx, *args):
        action = ctx.invoked_with
        if args:
            command = ''
            for arg in args:
                command = f'{command} {arg}'
            command = self.bot.get_command(command)
            if command is None:
                await ctx.send('No command with that name found.')
            elif ctx.command == command:
                await ctx.send(f'You can not {action} this command.')
            else:
                if action == 'enable':
                    command.enabled = True
                else:
                    command.enabled = False
                await ctx.send(f'Command {command.qualified_name} {action}d.')
        else:
            await ctx.send(f'The syntax is `{ctx.prefix}{ctx.command} [command]`')

# Initialization
def setup(bot):
    bot.add_cog(DevCog(bot))