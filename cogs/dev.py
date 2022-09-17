# dev.py
"""Contains internal dev commands"""

import importlib
import sys

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from resources import functions, settings, views


class DevCog(commands.Cog):
    """Cog with internal dev commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    dev = SlashCommandGroup(
        "dev",
        "Development commands",
        guild_ids=settings.DEV_GUILDS,
        default_member_permissions=discord.Permissions(administrator=True)
    )

    # Commands
    @dev.command()
    @commands.is_owner()
    async def reload(
        self,
        ctx: discord.ApplicationContext,
        modules: Option(str, 'Cogs or modules to reload'),
    ) -> None:
        """Reloads cogs or modules"""
        modules = modules.split(' ')
        actions = []
        for module in modules:
            name_found = False
            cog_name = f'cogs.{module}' if not 'cogs.' in module else module
            try:
                cog_status = self.bot.reload_extension(cog_name)
            except:
                cog_status = 'Error'
            if cog_status is None:
                actions.append(f'+ Extension \'{cog_name}\' reloaded.')
                name_found = True
            if not name_found:
                for module_name in sys.modules.copy():
                    if module == module_name:
                        module = sys.modules.get(module_name)
                        if module is not None:
                            importlib.reload(module)
                            actions.append(f'+ Module \'{module_name}\' reloaded.')
                            name_found = True
            if not name_found:
                actions.append(f'- No loaded cog or module with the name \'{module}\' found.')

        message = ''
        for action in actions:
            message = f'{message}\n{action}'
        await ctx.respond(f'```diff\n{message}\n```')

    @dev.command()
    @commands.is_owner()
    async def shutdown(self, ctx: discord.ApplicationContext):
        """Shuts down the bot"""
        view = views.ConfirmCancelView(ctx)
        interaction = await ctx.respond(f'**{ctx.author.name}**, are you **SURE**?', view=view)
        view.interaction = interaction
        await view.wait()
        if view.value is None:
            await functions.edit_interaction(interaction, content=f'**{ctx.author.name}**, you didn\'t answer in time.',
                                             view=None)
        elif view.value == 'confirm':
            await functions.edit_interaction(interaction, content='Shutting down.', view=None)
            await self.bot.close()
        else:
            await functions.edit_interaction(interaction, content='Shutdown aborted.', view=None)

    @dev.command(name='sync-commands')
    @commands.is_owner()
    async def sync_commands(self, ctx: discord.ApplicationContext) -> None:
        """Manually sync commands"""
        await ctx.defer()
        if settings.DEBUG_MODE:
            #await self.bot.sync_commands(commands=[], guild_ids=settings.DEV_GUILDS)
            await self.bot.sync_commands(guild_ids=settings.DEV_GUILDS, force=True)
        else:
            #await self.bot.sync_commands(commands=[], force=False)
            await self.bot.sync_commands(force=True)
        await ctx.respond('Done')

    @dev.command(name='test')
    @commands.is_owner()
    async def test_command(self, ctx: discord.ApplicationContext) -> None:
        """Manually sync commands"""
        test = functions.format_string(None)
        pass


# Initialization
def setup(bot):
    bot.add_cog(DevCog(bot))