# dev.py
"""Contains internal dev commands"""

import asyncio
import importlib
import sys

import discord
from discord.ext import commands

import database
from resources import emojis, functions, settings


class DevOldCog(commands.Cog):
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
    async def logs(self, ctx, base_log_amount: int) -> None:
        """Calculates how many logs it needs for a certain amount of epic logs"""
        item_amount = 100
        returned_percentage = 0.1
        level = 1
        base_log_amount_upper = 100_000_000_000
        base_log_amount_lower = 0
        while True:
            #base_log_amount = log_amount = (base_log_amount_lower + base_log_amount_upper) // 2
            log_amount = base_log_amount
            epic_log_amount = epic_log_amount_total = log_amount_total = 0
            while True:
                epic_log_amount, log_rest = divmod(log_amount, 25)
                epic_log_amount_total += epic_log_amount
                if level >= 100:
                    returned_amount = functions.round_school(epic_log_amount * 0.8 * 25 * returned_percentage)
                    if returned_amount == 0: returned_amount = 1
                    log_rest += returned_amount
                    log_amount_total += returned_amount
                log_amount = log_rest + epic_log_amount * 20
                log_amount_total += epic_log_amount * 20
                if log_amount < 25: break
            await ctx.send(f'{epic_log_amount_total:,}')
            return
            if (item_amount - 1) <= epic_log_amount_total <= (item_amount + 1):
                break
            elif epic_log_amount_total < item_amount:
                base_log_amount_lower = base_log_amount - 1
            elif epic_log_amount_total > item_amount:
                base_log_amount_upper = base_log_amount + 1




    @dev.command(aliases=('unload','reload',))
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def load(self, ctx: commands.Context, *args: str) -> None:
        """Loads/unloads cogs and reloads cogs or modules"""
        action = ctx.invoked_with
        message_syntax = f'The syntax is `{ctx.prefix}dev {action} [name(s)]`'
        if not args:
            await ctx.send(message_syntax)
            return
        args = [arg.lower() for arg in args]
        actions = []
        for mod_or_cog in args:
            name_found = False
            if not 'cogs.' in mod_or_cog:
                cog_name = f'cogs.{mod_or_cog}'
            try:
                if action == 'load':
                    cog_status = self.bot.load_extension(cog_name)
                elif action == 'reload':
                    cog_status = self.bot.reload_extension(cog_name)
                else:
                    if cog_name != 'cogs.dev':
                        cog_status = self.bot.unload_extension(cog_name)
                    else:
                        cog_status = 'dev-unload'
            except:
                cog_status = 'error'
            if cog_status is None:
                actions.append(f'+ Extension \'{cog_name}\' {action}ed.')
                name_found = True
            if not name_found:
                if action == 'reload':
                    for module_name in sys.modules.copy():
                        if mod_or_cog == module_name:
                            module = sys.modules.get(module_name)
                            if module is not None:
                                importlib.reload(module)
                                actions.append(f'+ Module \'{module_name}\' reloaded.')
                                name_found = True
            if not name_found:
                if action == 'reload':
                    actions.append(f'- No cog with the name \'{mod_or_cog}\' found or cog not loaded.')
                elif cog_status == 'dev-unload':
                    actions.append(f'- You can not unload \'cogs.dev\', dummy.')
                else:
                    actions.append(f'- No cog with the name \'{mod_or_cog}\' found or cog already {action}ed.')

        message = ''
        for action in actions:
            message = f'{message}\n{action}'
        await ctx.send(f'```diff\n{message}\n```')


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

    # Enable/disable commands
    @commands.command()
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def test(self, ctx):
        embed = discord.Embed(
            title='Will I ever get a godly lootbox?',
            description='I have no clue, but it\'s very nice talking to you. Are you single?',
            color=0xfe019a
        )
        file = discord.File(settings.IMG_CRYSTAL_BALL)
        #embed.set_thumbnail(url=f"attachment://{file.filename}")
        embed.set_author(name=f'{ctx.author.name}\'s question')
        """
        image_url = 'https://www.youtube.com/watch?v=gENVB6tjq_M'
        embed.set_image(url=image_url)
        """
        await ctx.send(embed=embed)

    @dev.command(name='migrate-users')
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def migrate_users(self, ctx: commands.Context) -> None:
        """Migrate user settings to new format
        Old: ascended / not ascended
        New: O / 1 (boolean)"""
        await ctx.send('Working...')
        ascended_over_25 = 0
        users = await database.get_all_users()
        for user in users:
            if user.tt >= 25:
                user.ascended = True
                ascended_over_25 += 1
            await user.update(ascended=user.ascended)
        await ctx.send(f'Updated {len(users):,} records, {ascended_over_25:,} of them where not ascended over TT 25.')

    @dev.command(name='sync-commands')
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def sync_commands(self, ctx: commands.Context) -> None:
        """Migrate user settings to new format
        Old: ascended / not ascended
        New: O / 1 (boolean)"""
        await self.bot.sync_commands()
        await ctx.send('Done')

    @dev.command()
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def fetch_members(self, ctx: commands.Context) -> None:
        guild = await self.bot.fetch_guild(830928381100556338)
        members = await guild.fetch_members(limit=10).flatten()
        await ctx.send(str(members))



# Initialization
def setup(bot):
    bot.add_cog(DevOldCog(bot))