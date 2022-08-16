# titles.py


from discord.ext import commands

from resources import functions


class TitlesOldCog(commands.Cog):
    """Cog with title/achievement commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=('titles','achievement','achievements','ach','t'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def title(self, ctx: commands.Context, *args: str) -> None:
        """Command to search for a title/achievement"""
        await functions.send_slash_migration_message(ctx, 'title search')


# Initialization
def setup(bot):
    bot.add_cog(TitlesOldCog(bot))