# horse.py
"""Contains all horse related guides and calculators"""

from discord.ext import commands

from resources import functions


class HorseOldCog(commands.Cog):
    """Cog with horse commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    horse_aliases = (
        'horses',
        'htier',
        'horsestier',
        'horsetiers',
        'horsestiers',
        'htype',
        'horsestype',
        'horsetypes',
        'horsestypes',
        'hbreed',
        'hbreeding',
        'breed',
        'breeding',
        'horsebreeding',
        'horsesbreed',
        'horsesbreeding',
        'breedhorse',
        'breedhorses',
        'breedinghorse',
        'breedingshorses'
    )

    @commands.command(aliases=horse_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def horse(self, ctx: commands.Context, *args: str) -> None:
        """Horse main command"""
        await functions.send_slash_migration_message(ctx, 'horse guide')

    @commands.command(aliases=('hcalc','hc'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def horsecalc(self, ctx: commands.Context, *args: str) -> None:
        """Calculates the horse stat bonuses"""
        await functions.send_slash_migration_message(ctx, 'horse boost calculator')

    @commands.command(aliases=('horsetraincalc','horsetrainingcalc','horsetraining','htraincalc',
                               'htrainingcalc','htcalc'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def htc(self, ctx: commands.Context, *args: str) -> None:
        """Horse training cost calculator"""
        await functions.send_slash_migration_message(ctx, 'horse training calculator')

    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def htctotal(self, ctx: commands.Context, *args: str) -> None:
        """Calculate total horse training costs up to a level"""
        await functions.send_slash_migration_message(ctx, 'horse training calculator')

    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def htcmanual(self, ctx: commands.Context, *args: str) -> None:
        """Calculate total horse training cost with manually specified values"""
        await functions.send_slash_migration_message(ctx, 'horse training calculator')


# Initialization
def setup(bot):
    bot.add_cog(HorseOldCog(bot))