# monsters.py

import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup

from content import monsters


# --- Autocomplete functions ---
async def monster_searcher(ctx: discord.AutocompleteContext):
    """Returns a list of matching monsters from ALL_MONSTER_NAMES"""
    return [monster.name for monster in monsters.ALL_MONSTERS if ctx.value.lower() in monster.name.lower()]


class MonstersCog(commands.Cog):
    """Cog with monster commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_monster = SlashCommandGroup(
        "monster",
        "Monster drops and search",
    )

    @cmd_monster.command(name='drops', description='Monster drops and where to find them')
    async def monster_drops(self, ctx: discord.ApplicationContext) -> None:
        """Monster drops"""
        await monsters.command_monster_drops(ctx)

    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_monster.command(name='search', description='Look up monsters')
    async def monster_search(self,
        ctx: discord.ApplicationContext,
        name: Option(str, 'Name of the monster(s). Looks up the daily monster if empty.',
                     autocomplete=monster_searcher, default=None, max_length=100),
    ) -> None:
        """Command to search for a monster"""
        await monsters.command_monster_search(self.bot, ctx, name)


# Initialization
def setup(bot):
    bot.add_cog(MonstersCog(bot))