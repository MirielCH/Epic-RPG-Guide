# areas.py

from discord.ext import commands

from resources import functions


# area commands (cog)
class AreasOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    area_aliases = ['area','areas','top','thetop','atop','areatop']
    for x in range(1,21):
        area_aliases.append(f'a{x}')
        area_aliases.append(f'area{x}')

    @commands.command(name='a',aliases=(area_aliases))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def area(self, ctx: commands.Context, *args: str) -> None:
        """Command for areas, can be invoked with "aX", "a X", "areaX" and "area X".
        Optional parameters for TT and ascension
        """
        invoked = ctx.invoked_with.lower()
        prefix = ctx.prefix.lower()
        area_no = arg_tt = None
        arg_asc = False


# Initialization
def setup(bot):
<<<<<<< HEAD
    bot.add_cog(AreasOldCog(bot))