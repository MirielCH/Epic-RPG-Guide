# pets.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import pets
import database
from resources import strings, views


TOPIC_ADVENTURES = 'Pet adventures'
TOPIC_CATCH = 'Catching pets'
TOPIC_FUSION = 'Fusing pets'
TOPIC_OVERVIEW = 'Overview'
TOPIC_SKILLS = 'Skills: Normal skills'
TOPIC_SKILLS_SPECIAL = 'Skills: Special skills'
TOPIC_SKILLS_UNIQUE = 'Skills: Unique skills'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_CATCH,
    TOPIC_FUSION,
    TOPIC_ADVENTURES,
    TOPIC_SKILLS,
    TOPIC_SKILLS_SPECIAL,
    TOPIC_SKILLS_UNIQUE,
]


class PetsCog(commands.Cog):
    """Cog with pet commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_pets = SlashCommandGroup("pets", "Pets commands")

    @cmd_pets.command(name='guide', description='All about pets')
    async def pets_guide(
        self,
        ctx: discord.ApplicationContext,
        topic: Option(str, strings.ARGUMENT_TOPIC_DESCRIPTION,
                           choices=TOPICS, default=TOPIC_OVERVIEW),
    ) -> None:
        """Professions guides"""
        topics_functions = {
            TOPIC_OVERVIEW: pets.embed_pets_overview,
            TOPIC_CATCH: pets.embed_pets_catch,
            TOPIC_FUSION: pets.embed_pets_fusion,
            TOPIC_ADVENTURES: pets.embed_pets_adventures,
            TOPIC_SKILLS: pets.embed_pets_skills_normal,
            TOPIC_SKILLS_SPECIAL: pets.embed_pets_skills_special,
            TOPIC_SKILLS_UNIQUE: pets.embed_pets_skills_unique,
        }
        view = views.TopicView(ctx, topics_functions, active_topic=topic)
        embed = await topics_functions[topic]()
        interaction = await ctx.respond(embed=embed, view=view)
        view.interaction = interaction
        await view.wait()
        await interaction.edit_original_message(view=None)

    @cmd_pets.command(name='fuse', description='Pet fusion recommendations for a target tier')
    async def pets_fuse(
        self,
        ctx: discord.ApplicationContext,
        pet_tier: Option(int, 'The pet tier you want to get', min_value=1, max_value=20),
        timetravel: Option(int, 'The TT you want a recommendation for. Uses your progress setting if empty.',
                           min_value=0, max_value=999, default=None),
    ) -> None:
        if timetravel is None:
            user: database.User = await database.get_user(ctx.author.id)
            timetravel = user.tt
        embed = await pets.embed_fuse(pet_tier, timetravel)
        await ctx.respond(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(PetsCog(bot))