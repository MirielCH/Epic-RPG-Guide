# misc.py

from discord.ext import commands

from resources import functions


# Miscellaneous commands (cog)
class MiscOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "duels" - Returns all duelling weapons
    @commands.command(aliases=('duel','duelling','dueling','duelweapons','duelweapon',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def duels(self, ctx):
        await functions.send_slash_migration_message(ctx, 'duel weapons')

    # Command "codes" - Redeemable codes
    @commands.command(aliases=('code',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def codes(self, ctx):
        await functions.send_slash_migration_message(ctx, 'codes')

    # Command "coolness" - Coolness guide
    @commands.command(aliases=('cool',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def coolness(self, ctx):
        await functions.send_slash_migration_message(ctx, 'coolness guide')

    # Command "badges" - Badge guide
    @commands.command(aliases=('badge',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def badges(self, ctx):
        await functions.send_slash_migration_message(ctx, 'badges')

    # Command "farm" - Farming guide
    @commands.command(aliases=('farming',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def farm(self, ctx):
        await functions.send_slash_migration_message(ctx, 'farming guide')

    # Command "start" - Starter guide
    @commands.command(aliases=('starting','startguide','starterguide','startingguide'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def start(self, ctx):
        await functions.send_slash_migration_message(ctx, 'beginner guide')

    @commands.command(aliases=('ultr',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def ultraining(self, ctx: commands.Context, *args: str) -> None:
        """Ultraining guide"""
        await functions.send_slash_migration_message(ctx, 'ultraining guide')

    @commands.command(aliases=('ucalc','ultrcalc','ultrainingcalc','stage'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def uc(self, ctx: commands.Context, *args: str) -> None:
        """Ultraining stage calculator"""
        await functions.send_slash_migration_message(ctx, 'ultraining stats calculator')

    # Command "calc" - Simple calculator
    @commands.command(aliases=('calculate','calculator','math'))
    @commands.bot_has_permissions(send_messages=True)
    async def calc(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'calculator')

    # Command "tip" - Returns a random tip
    @commands.command(aliases=('tips',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def tip(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'tip')

    # Command "coincap" - Calculate the coin cap
    @commands.command(aliases=('coin',))
    @commands.bot_has_permissions(send_messages=True, external_emojis=True)
    async def coincap(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'coin cap calculator')


# Initialization
def setup(bot):
    bot.add_cog(MiscOldCog(bot))