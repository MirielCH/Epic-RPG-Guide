# professions.py

from discord.ext import commands

from resources import functions


# profession commands (cog)
class ProfessionsOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pr_aliases = (
        'pr','professions','prof','profs',
        'ascension','asc','prasc','prascension','ascended','ascend','prascend','prascended',
        'prlevel','prlvl','professionslevel','professionslevels','professionlevels','professionsleveling','professionleveling','prlevels','prleveling','proflevel','proflevels','profslevel','profslevels',
        'worker','enchanter','crafter','lootboxer','merchant','prworker','prenchanter','prcrafter','prlootboxer','prmerchant'
    )

    # Command "professions"
    @commands.command(aliases=pr_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def profession(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'professions guide')

    # Command "prc" - Info about crafting
    @commands.command(aliases=('prctotal',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prc(self, ctx):
        await functions.send_slash_migration_message(ctx, 'professions calculator')

    # Command "pre" - Calculate ice cream to craft
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, external_emojis=True)
    async def pre(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'professions calculator')

    # Command "prl" - Calculate lootboxes to craft
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def prl(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'professions calculator')

    # Command "prm" - Calculate logs to sell
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prm(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'professions calculator')

    # Command "prw" - Calculate pickaxes to craft
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, external_emojis=True)
    async def prw(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'professions calculator')

    # Command "pretotal" - Calculate total ice cream to craft until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def pretotal(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'professions calculator')

    # Command "prltotal" - Calculate total lootboxes to craft until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prltotal(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'professions calculator')

    # Command "prmtotal" - Calculate total logs to sell until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prmtotal(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'professions calculator')

    # Command "prwtotal" - Calculate total pickaxes to craft until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prwtotal(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'professions calculator')


# Initialization
def setup(bot):
    bot.add_cog(ProfessionsOldCog(bot))