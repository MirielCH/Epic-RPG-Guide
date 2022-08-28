# trading.py

from discord.ext import commands

from resources import functions


# trading commands (cog)
class TradingOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "trades" - Returns recommended trades of one area or all areas
    trades_aliases = ['tr','trade','trtop','tradetop']
    for x in range(1,21):
        trades_aliases.append(f'tr{x}')
        trades_aliases.append(f'trades{x}')
        trades_aliases.append(f'trade{x}')

    @commands.command(aliases=trades_aliases)
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def trades(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'trade guide')

    # Command "traderates" - Returns trade rates of all areas
    @commands.command(aliases=('trr','rates','rate','traderate',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def traderates(self, ctx):
        await functions.send_slash_migration_message(ctx, 'trade rates')

    # Command "tradecalc" - Calculates the trades up to A10
    @commands.command(aliases=('trc',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def tradecalc(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'trade calculator')


# Initialization
def setup(bot):
    bot.add_cog(TradingOldCog(bot))