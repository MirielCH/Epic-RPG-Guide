# fun.py
"""Contains some silly and useless fun commands"""

import discord
from discord.ext import commands

import global_data


class FunCog(commands.Cog):
    """Cog with silly and useless fun commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Commands
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def panda(self, ctx: commands.Context) -> None:
        """Because Panda is awesome"""
        await ctx.send('All hail Panda! :panda_face:')

    @commands.command(aliases=('shutup','shutit','shutup!','shutit!'))
    @commands.bot_has_permissions(send_messages=True)
    async def shut(self, ctx: commands.Context, *args: str) -> None:
        """Sometimes you just have to say it"""
        if ctx.invoked_with.lower() == 'shut':
            if args:
                args = [arg.lower() for arg in args]
                arg, *_ = args
                if arg in ('up','it','up!','it!'):
                    await ctx.send('No.')
        else:
            await ctx.send('No.')

    @commands.command(aliases=('bad!','trash','trash!','badbot','trashbot','badbot!','trashbot!','delete',))
    @commands.bot_has_permissions(send_messages=True)
    async def bad(self, ctx: commands.Context, *args: str) -> None:
        """Sad"""
        if ctx.invoked_with.lower() in ('bad','trash',):
            if args:
                args = [arg.lower() for arg in args]
                arg, *_ = args
                if arg in ('bot','bot!'):
                    await ctx.send('https://tenor.com/view/sad-pikachu-crying-pokemon-gif-16694846')
        else:
            await ctx.send('https://tenor.com/view/sad-pikachu-crying-pokemon-gif-16694846')

    @commands.command(aliases=('nice','great','amazing','useful','best','goodbot','bestbot',
                               'greatbot','nicebot',))
    @commands.bot_has_permissions(send_messages=True)
    async def good(self, ctx: commands.Context, *args: str) -> None:
        """Yay!"""
        if ctx.invoked_with.lower() in ('good','great','nice','best','useful','amazing'):
            if args:
                args = [arg.lower() for arg in args]
                arg, *_ = args
                if arg in ('bot','bot!'):
                    await ctx.send('https://tenor.com/view/raquita-gif-9201609')
        else:
            await ctx.send('https://tenor.com/view/raquita-gif-9201609')

    @commands.command(aliases=('thank','thanks!','ty','thx'))
    @commands.bot_has_permissions(send_messages=True)
    async def thanks(self, ctx: commands.Context, *args: str) -> None:
        """You're very welcome"""
        if ctx.invoked_with.lower() == 'thank':
            if args:
                args = [arg.lower() for arg in args]
                arg, *_ = args
                if arg in ('you', 'you!'):
                    await ctx.send('You\'re welcome! :heart:')
        else:
            await ctx.send('You\'re welcome! :heart:')

    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def brandon(self, ctx: commands.Context) -> None:
        """Only three people will get this"""
        embed = discord.Embed(
            color = global_data.EMBED_COLOR,
            title = 'WHAT TO DO WITH BRANDON',
            description = 'Don\'t even _think_ about dismantling him. You monster.'
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def complain(self, ctx: commands.Context) -> None:
        """Complain"""
        await ctx.send('No u')

    @commands.command()
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def hey(self, ctx: commands.Context) -> None:
        """Hey ho"""
        await ctx.send('Hey hey. Oh it\'s you, Miri! Yes I\'m online, thanks for asking. NOW LEAVE ME ALONE.')


# Initialization
def setup(bot):
    bot.add_cog(FunCog(bot))