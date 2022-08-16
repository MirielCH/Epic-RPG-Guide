# timetravel.py

from discord.ext import commands

from resources import functions


# time travel commands (cog)
class timetravelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "ttX" - Specific tt information
    tt_aliases = []
    for x in range(0,1000):
        tt_aliases.append(f'tt{x}')
        tt_aliases.append(f'timetravel{x}')

    @commands.command(aliases=(tt_aliases))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def timetravel_specific(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'time travel bonuses')

    @commands.command(name='tt',aliases=('timetravel',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def timetravel_guide(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'time travel guide')

    # Command "mytt" - Information about user's TT
    @commands.command(aliases=('mytimetravel',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def mytt(self, ctx):
        await functions.send_slash_migration_message(ctx, 'time travel bonuses')

    # Command "supertimetravel" - Information about super time travel
    @commands.command(aliases=('stt','supertt',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def supertimetravel(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'time travel guide')

    # Command "sttscore" - Returns super time travel score calculations
    @commands.command(aliases=('sttscore','superttscore','stts',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def supertimetravelscore(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'time travel guide')

    # Command "sttcalc" - Calculates STT score based in inventory and area
    @commands.command(aliases=('scorecalc','sttscorecalc','sttc','scalc','sc','superttcalc',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def sttcalc(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'time jump calculator')


# Initialization
def setup(bot):
    bot.add_cog(timetravelCog(bot))