# guilds.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import guild
from resources import strings


class GuildCog(commands.Cog):
    """Cog with guild commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_guild = SlashCommandGroup("guild", "Guild commands")

    @cmd_guild.command(name='guide', description='All you need to know about guilds')
    async def guild_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION, choices=guild.TOPICS, default=guild.TOPIC_OVERVIEW),
    ) -> None:
        """Guild guides"""
        await guild.command_guild_guide(ctx, topic)


# Initialization
def setup(bot):
    bot.add_cog(GuildCog(bot))