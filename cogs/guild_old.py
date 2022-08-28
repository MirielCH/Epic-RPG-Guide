# guilds.py

from discord.ext import commands

from resources import functions


# Guild commands (cog)
class GuildOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guild_aliases = (
        'guilds',
        'stealth',
        'energy',
        'guildstealth',
        'guildenergy',
        'guildreward',
        'guildrewards',
        'guildweekly',
        'guildcmd',
        'guildcommand',
        'guildcommands',
        'guildstat',
        'guildstats',
        'guildshop',
        'omegahorsetoken',
        'omegatoken',
        'guildomegatoken',
        'guildomegahorsetoken',
        'guildhorsetoken',
        'cookierain',
        'guildcookierain',
        'guildrain',
        'guildbuff',
        'guildbuy',
        'guildlevel',
        'guildlvl',
        'guildprogress',
        'magicchair',
        'guildtask',
        'guildtasks',
    )

    # Command "guild"
    @commands.command(aliases=guild_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def guild(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'guild guide')


# Initialization
def setup(bot):
    bot.add_cog(GuildOldCog(bot))