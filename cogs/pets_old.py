# pets.py

import discord
from discord.ext import commands

from resources import functions


# pets commands (cog)
class PetsOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pets_aliases = (
        'pet',
        'petcatch','petscatch','petscatching','petcatching','catchpet','catchpets','catchingpet','catchingpets',
        'petfind','petsfind','petfinding','petsfinding','findpet','findingpet','findpets','findingpets',
        'petsfusion','fusion','petfusing','petsfusing','fusing','fusepet','fusepets','fusingpet','fusingpets',
        'petsskills','petskill','skill','skills','petsskill',
        'petsspecial','petsspecialskill','petsspecialskills','petspecial','petspecialskill','petspecialskills','petskillspecial','petskillsspecial','petsskillspecial','petsskillsspecial',
        'petsadv','petsadventures','petadv','petadventure','petadventures'
    )

    # Command "pets"
    @commands.command(aliases=pets_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def pets(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'pets guide')

    # Command "Fuse" - Recommendations for pet tiers in fusions
    @commands.command(aliases=('petfuse',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def fuse(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'pets fuse')


# Initialization
def setup(bot):
    bot.add_cog(PetsOldCog(bot))