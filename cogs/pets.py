# pets.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import pets
from resources import strings


class PetsCog(commands.Cog):
    """Cog with pet commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_pet = SlashCommandGroup("pet", "Pet commands")

    @cmd_pet.command(name='guide', description='All about pets')
    async def pet_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION,
                           choices=pets.TOPICS, default=pets.TOPIC_OVERVIEW),
    ) -> None:
        """Professions guides"""
        await pets.command_pet_guide(ctx, topic)

    @cmd_pet.command(name='fuse', description='Pet fusion recommendations for a target tier')
    async def pet_fuse(
        self,
        ctx: discord.ApplicationContext,
        pet_tier: Option(int, 'The pet tier you want to get', min_value=1, max_value=20),
        timetravel: Option(int, 'The TT you want a recommendation for. Uses your progress setting if empty.',
                           min_value=0, max_value=999, default=None),
    ) -> None:
        """Pet fuse recommendations"""
        await pets.command_pet_fuse(ctx, pet_tier, timetravel=timetravel)


# Initialization
def setup(bot):
    bot.add_cog(PetsCog(bot))