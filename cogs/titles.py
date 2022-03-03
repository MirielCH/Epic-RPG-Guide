# titles.py


from typing import Tuple

import discord
from discord.ext import commands

import database
from resources import emojis
from resources import settings


class TitlesCog(commands.Cog):
    """Cog with title/achievement commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=('titles','achievement','achievements','ach','t'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def title(self, ctx: commands.Context, *args: str) -> None:
        """Command to search for a title/achievement"""
        prefix = ctx.prefix
        syntax = (
            f'The command syntax is `{prefix}{ctx.invoked_with} [search query]`. The search query can either be part '
            f'of the title, part of the achievement name or the ID of the title/achievement.\n'
            f'Examples:\n'
            f'{emojis.BP} `{prefix}{ctx.invoked_with} cool`\n'
            f'{emojis.BP} `{prefix}{ctx.invoked_with} survive waves`\n'
            f'{emojis.BP} `{prefix}{ctx.invoked_with} 199`'
        )
        if not args:
            await ctx.send(syntax)
            return
        args = [arg.lower() for arg in args]
        search_string = " ".join(args)
        if len(search_string) < 3 and not search_string.isnumeric() and search_string != 'no': # There is a title called "no"
            await ctx.send('The search query needs to be at least 3 characters long.')
            return
        if len(search_string) > 200:
            await ctx.send('Really.')
            return
        try:
            titles = await database.get_titles(ctx, search_string)
        except database.NoDataFound:
            await ctx.send('I didn\'t find any titles with that search query, sorry. Try searching for something else.')
            return
        embed = await embed_titles(prefix, search_string, titles)
        await ctx.send(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(TitlesCog(bot))


# --- Embeds ---
async def embed_titles(prefix: str, search_string: str, titles: Tuple[database.Title]) -> discord.Embed:
    """Embed with all search results"""
    amount_found = len(titles)
    description = f'Your search returned **{amount_found}** results.'
    if amount_found > 9:
        description = (
            f'{description}\nThe first 9 results are shown below. To narrow down your search, please specify a less '
            f'general query.'
        )


    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TITLE SEARCH',
        description = description
    )

    title = type(database.Title)
    for title in titles[:9]:
        ach_or_req = 'Achievement' if title.source == 'Achievement' else 'Requirement'
        if title.source != 'Achievement':
            field_value = f'{emojis.BP} **Source**: {title.source}'
        else:
            field_value = f'{emojis.BP} **ID**: `{title.achievement_id}`'
        field_value = f'{field_value}\n{emojis.BP} **{ach_or_req}**: {title.requirements}'
        if title.command is not None: field_value = f'{field_value}\n{emojis.BP} **Command**: `{title.command}`'
        if title.tip is not None:
            tip = title.tip.format(prefix=prefix) if '{prefix}' in title.tip else title.tip
            field_value = f'{field_value}\n{emojis.BP} **Tip**: {tip}'
        if title.requires_id is not None:
            field_value = (
                f'{field_value}\n'
                f'{emojis.BP} **Note**: Requires completion of achievement `{title.requires_id}` first.'
            )
        embed.add_field(name=title.title, value=field_value, inline=False)
    if amount_found > 9:
        embed.set_footer(text=f'Note: This is only the first 9 of {amount_found} results. Please narrow your search.')

    return embed