# events.py

import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup

from content import events


# --- Autocomplete functions ---
async def event_type_filter(ctx: discord.AutocompleteContext):
    """Returns a list of matching monsters from ALL_MONSTER_NAMES"""
    picked_type = ctx.options['type']
    if picked_type == 'Personal':
        FILTERED_LIST = events.EVENTS_PERSONAL
    elif picked_type == 'Multiplayer':
        FILTERED_LIST = events.EVENTS_MULTIPLAYER
    elif picked_type == 'Global':
        FILTERED_LIST = events.EVENTS_GLOBAL
    else:
        FILTERED_LIST = events.EVENTS_ALL
    return [event for event in FILTERED_LIST if ctx.value.lower() in event.lower()]


class EventsCog(commands.Cog):
    """Cog with event commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_event = SlashCommandGroup(
        "event",
        "Event guide commands",
    )

    @cmd_event.command(name='guide', description='Guide for all personal, multiplayer and global events')
    async def event_guide(self,
        ctx: discord.ApplicationContext,
        type: Option(str, 'Type of the event.', choices=events.EVENT_TYPES),
        event: Option(str, 'Name of the event.', autocomplete=event_type_filter),
    ) -> None:
        """Event guides"""
        await events.command_event_guide(ctx, event)


# Initialization
def setup(bot):
    bot.add_cog(EventsCog(bot))
