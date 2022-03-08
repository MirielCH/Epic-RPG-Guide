# titles.py


from typing import Tuple

import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages

import database
from resources import emojis, settings, views


class TitlesCog(commands.Cog):
    """Cog with title/achievement commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_title = SlashCommandGroup(
        "title",
        "Title search commands",
    )

    @cmd_title.command(name='search', description='Look up titles / achievements')
    async def professions_guide(
        self,
        ctx: discord.ApplicationContext,
        search_string: Option(str, 'Achievement ID or part of the title / achievement'),
    ) -> None:
        """Command to search for a title/achievement"""
        if len(search_string) < 3 and not search_string.isnumeric() and search_string != 'no': # There is a title called "no"
            await ctx.respond('The search query needs to be at least 3 characters long.')
            return
        if len(search_string) > 200:
            await ctx.respond('Really.')
            return
        try:
            titles = await database.get_titles(ctx, search_string)
        except database.NoDataFound:
            await ctx.respond('I didn\'t find any titles with that search query, sorry. Try searching for something else.')
            return
        embeds = []
        chunk_amount = 0
        for chunk in range(0, len(titles), 6):
            titles_chunk = titles[chunk:chunk+6]
            chunk_amount += 1
            embed = await embed_titles(len(titles), titles_chunk)
            embeds.append(embed)
        if len(embeds) > 1:
            view = views.PaginatorView(ctx, embeds)
            interaction = await ctx.respond(embed=embeds[0], view=view)
            view.interaction = interaction
            await view.wait()
            await interaction.edit_original_message(view=None)
        else:
            await ctx.respond(embed=embed)

        """paginator = pages.Paginator(
                pages=embeds,
                timeout=settings.INTERACTION_TIMEOUT,
                custom_buttons=views.PAGINATOR_BUTTONS,
                use_default_buttons=False
            )
            await paginator.respond(ctx.interaction, ephemeral=False)
            await paginator.wait()
            paginator.clear_items()

        Returns:
            _type_: _description_
        """


# Initialization
def setup(bot):
    bot.add_cog(TitlesCog(bot))


# --- Embeds ---
async def embed_titles(amount_found: int, titles: Tuple[database.Title]) -> discord.Embed:
    """Embed with all search results

    Arguments
    ---------
    search_string: String that user searched for
    pages: current page, max page (max. 9 titles per page)
    amount_found: total amount of titles found in the database
    """
    description = f'Your search returned **{amount_found}** results.'

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
            field_value = f'{field_value}\n{emojis.BP} **Tip**: {title.tip}'
        if title.requires_id is not None:
            field_value = (
                f'{field_value}\n'
                f'{emojis.BP} **Note**: Requires completion of achievement `{title.requires_id}` first.'
            )
        embed.add_field(name=title.title, value=field_value, inline=False)

    return embed