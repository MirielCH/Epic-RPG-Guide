# crafting.py

from discord.ext import commands

from resources import functions


# crafting commands (cog)
class craftingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "enchants"
    @commands.command(aliases=('enchant','e','enchanting',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def enchants(self, ctx):
        await functions.send_slash_migration_message(ctx, 'enchanting guide')

    # Command "drops" - Returns all monster drops and where to get them
    @commands.command(aliases=('drop','mobdrop','mobdrops','mobsdrop','mobsdrops','monsterdrop','monsterdrops',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def drops(self, ctx):
        await functions.send_slash_migration_message(ctx, 'monster drops')


    # Command "dropchance" - Calculate current drop chance
    @commands.command(aliases=('dropcalc','droprate',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def dropchance(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'drop chance calculator')

    @commands.command(aliases=('cook','forge',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def craft(self, ctx: commands.Context, *args: str) -> None:
        """Calculates mats you need when crafting items"""
        await functions.send_slash_migration_message(ctx, 'crafting calculator')

    @commands.command(aliases=('dm',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def dismantle(self, ctx: commands.Context, *args: str) -> None:
        """Calculates mats you get when dismantling items"""
        await functions.send_slash_migration_message(ctx, 'dismantling calculator')

    # Command "invcalc" - Calculates amount of items craftable with current inventory
    @commands.command(aliases=('ic','invc','icalc','inventoryc','inventorycalc',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def invcalc(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'inventory calculator')


# Initialization
def setup(bot):
    bot.add_cog(craftingCog(bot))