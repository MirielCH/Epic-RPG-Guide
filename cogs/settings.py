# settings.py
"""Contains user settings commands"""

import discord
from discord.commands import SlashCommandGroup, slash_command, Option
from discord.ext import commands

from content import settings as settings_content
from resources import settings


# --- Autocomplete functions ---
async def ascension_choice(ctx: discord.AutocompleteContext):
    """Returns a list of possible ascension states"""
    if ctx.options['timetravel'] < 25:
        return settings_content.CHOICES_ASCENSION
    else:
        return [settings_content.CHOICE_ASCENDED,]


class SettingsCog(commands.Cog):
    """Cog user settings commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Commands
    @slash_command(description='Shows your current settings')
    async def cmd_settings(self, ctx: discord.ApplicationContext) -> None:
        """Returns current user progress settings"""
        await settings.command_settings(ctx)

    cmd_set = SlashCommandGroup("set", "Commands that change settings")
    @cmd_set.command(name='progress', description='Set your progress to get the correct guides')
    async def set_progress(
        self,
        ctx: discord.ApplicationContext,
        timetravel: Option(int, 'Your current TT', min_value=0, max_value=999),
        ascension: Option(str, 'Your current ascension', autocomplete=ascension_choice)
    ) -> None:
        """Sets user progress settings"""
        await settings_content.command_set_progress(ctx, timetravel, ascension)


# Initialization
def setup(bot):
    bot.add_cog(SettingsCog(bot))