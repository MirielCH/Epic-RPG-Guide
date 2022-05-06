# links.py
"""Contains various commands with links"""

import discord
from discord.ext import commands

from resources import emojis, functions, settings, strings


# Links
LINK_EROS = 'https://discord.gg/w5dej5m'
LINK_SUPPORT_SERVER = 'https://discord.gg/v7WbhnhbgN'
LINK_VOTE = 'https://top.gg/bot/770199669141536768/vote'
LINK_WIKI = 'https://epic-rpg.fandom.com/wiki/EPIC_RPG_Wiki'


class LinksOldCog(commands.Cog):
    """Cog with link commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Commands
    @commands.command(aliases=('inv',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def invite(self, ctx: commands.Context) -> None:
        """Sends the invite link"""
        embed = discord.Embed(
            color = settings.EMBED_COLOR,
            title = 'NEED A GUIDE?',
            description = (
                f'I\'d be flattered to visit your server, **{ctx.author.name}**.\n'
                f'You can invite me [here]({strings.LINK_INVITE}).'
            )
        )
        embed.set_footer(text=await functions.default_footer(ctx.prefix))
        await ctx.send(embed=embed)

    @commands.command(aliases=('supportserver','server',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def support(self, ctx: commands.Context) -> None:
        """Link to the support server"""
        embed = discord.Embed(
            color = settings.EMBED_COLOR,
            title = 'NEED BOT SUPPORT?',
            description = f'You can visit the support server [here]({LINK_SUPPORT_SERVER}).'
        )
        embed.set_footer(text=await functions.default_footer(ctx.prefix))
        await ctx.send(embed=embed)

    @commands.command(aliases=('link','wiki',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def links(self, ctx: commands.Context) -> None:
        """Links to wiki, servers, top.gg and invite"""
        epic_rpg_guide = (
            f'{emojis.BP} [Support Server]({LINK_SUPPORT_SERVER})\n'
            f'{emojis.BP} [Bot Invite]({strings.LINK_INVITE})\n'
            f'{emojis.BP} [Vote]({LINK_VOTE})'
        )
        epic_rpg = (
            f'{emojis.BP} [Official Wiki]({LINK_WIKI})\n'
            f'{emojis.BP} [Official Server]({LINK_EROS})'
        )
        embed = discord.Embed(
            color = settings.EMBED_COLOR,
            title = 'SOME HELPFUL LINKS',
            description = 'There\'s a whole world out there.'
        )
        embed.set_footer(text=await functions.default_footer(ctx.prefix))
        embed.add_field(name='EPIC RPG GUIDE', value=epic_rpg_guide, inline=False)
        embed.add_field(name='EPIC RPG', value=epic_rpg, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def vote(self, ctx: commands.Context) -> None:
        """Link to the top.gg voting page"""
        embed = discord.Embed(
            color = settings.EMBED_COLOR,
            title = 'FEEL LIKE VOTING?',
            description = (
                f'That\'s nice of you, **{ctx.author.name}**, thanks!\n'
                f'You can vote for me [here]({LINK_VOTE}).'
                )
            )
        embed.set_footer(text=await functions.default_footer(ctx.prefix))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def donate(self, ctx: commands.Context) -> None:
        """Much love"""
        await ctx.send(
            f'Aw that\'s nice of you but this is a free bot, you know.\n'
            f'Thanks though :heart:'
        )


# Initialization
def setup(bot):
    bot.add_cog(LinksOldCog(bot))