# gambling.py

from discord.ext import commands

from resources import functions


# gambling commands (cog)
class GamblingOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Trading menu
    @commands.command(aliases=('gamble','gambling',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def gamblingguide(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'gambling guide')

    # Command "blackjack"
    @commands.command(aliases=('bj',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def blackjack(self, ctx):
        await functions.send_slash_migration_message(ctx, 'gambling guide')

    # Command "coinflip"
    @commands.command(aliases=('cf',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def coinflip(self, ctx):
        await functions.send_slash_migration_message(ctx, 'gambling guide')

    # Command "cups"
    @commands.command(aliases=('cup',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def cups(self, ctx):
        await functions.send_slash_migration_message(ctx, 'gambling guide')

    # Command "dice"
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def dice(self, ctx):
        await functions.send_slash_migration_message(ctx, 'gambling guide')

    # Command "bigdice"
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def bigdice(self, ctx):
        await functions.send_slash_migration_message(ctx, 'gambling guide')

    # Command "multidice"
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def multidice(self, ctx):
        await functions.send_slash_migration_message(ctx, 'gambling guide')

    # Command "slots"
    @commands.command(aliases=('slot',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def slots(self, ctx):
        await functions.send_slash_migration_message(ctx, 'gambling guide')

    # Command "wheels"
    @commands.command(aliases=('wheels',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def wheel(self, ctx):
        await functions.send_slash_migration_message(ctx, 'gambling guide')


# Initialization
def setup(bot):
    bot.add_cog(GamblingOldCog(bot))