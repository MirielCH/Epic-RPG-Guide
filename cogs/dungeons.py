# dungeons.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import areas, dungeons
from resources import strings


class DungeonsCog(commands.Cog):
    """Cog with dungeon commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_dungeon = SlashCommandGroup("dungeon", "Dungeon guides and ready check")

    @cmd_dungeon.command(name='guide', description='How to prepare for and beat the dungeons')
    async def dungeon_guide(
        self,
        ctx: discord.ApplicationContext,
        dungeon_no: Option(float, 'The dungeon you want a guide for', name='dungeon',
                        min_value=1, max_value=21, choices=strings.CHOICES_DUNGEON),
    ) -> None:
        """Dungeon guide"""
        await dungeons.command_dungeon_guide(ctx, dungeon_no, areas.command_area_guide)

    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_dungeon.command(name='check', description='Check how you will manage in a dungeon')
    async def dungeon_check(
        self,
        ctx: discord.ApplicationContext,
        dungeon_no: Option(float, 'The dungeon you want to check for', name='dungeon',
                           min_value=1, max_value=21, choices=strings.CHOICES_DUNGEON),
        user_at: Option(int, 'Your AT. Reads from EPIC RPG if empty.', name='at', min_value=1, default=None),
        user_def: Option(int, 'Your DEF. Reads from EPIC RPG if empty.', name='def', min_value=1, default=None),
        user_life: Option(int, 'Your LIFE. Reads from EPIC RPG if empty.', name='life', min_value=100, default=None),
    ) -> None:
        """Dungeon check"""
        await dungeons.command_dungeon_check(self.bot, ctx, dungeon_no, areas.command_area_check, user_at, user_def, user_life)


# Initialization
def setup(bot):
    bot.add_cog(DungeonsCog(bot))
