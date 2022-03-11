# monsters.py

import asyncio
from typing import Tuple

import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup

import database
from resources import emojis, functions, settings, strings, views


ALL_MONSTERS = functions.await_coroutine(database.get_all_monsters())
ALL_MONSTER_NAMES = [monster.name for monster in ALL_MONSTERS]


# --- Functions ---
async def monster_searcher(ctx: discord.AutocompleteContext):
    """Returns a list of matching monsters from ALL_MONSTER_NAMES"""
    return [monster for monster in ALL_MONSTER_NAMES if ctx.value.lower() in monster.lower()]


class MonstersCog(commands.Cog):
    """Cog with monster commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_monster = SlashCommandGroup(
        "monster",
        "Monster search commands",
    )

    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_monster.command(name='search', description='Looks up monsters by name')
    async def monster_search(self,
        ctx: discord.ApplicationContext,
        name: Option(str, 'Name or part of the name of the monster(s). Looks up the daily mob if empty.',
                     autocomplete=monster_searcher, default=None),
    ) -> None:
        """Command to search for a monster"""
        if name is None:
            bot_message_task = asyncio.ensure_future(functions.wait_for_world_message(self.bot, ctx))
            try:
                bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, 'rpg world')
            except asyncio.TimeoutError:
                await ctx.respond(strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='profession'))
                return
            if bot_message is None: return
            name = await functions.extract_monster_name_from_world_embed(ctx, bot_message)
        if len(name) < 3:
            await ctx.respond('The search query needs to be at least 3 characters long.')
            return
        if len(name) > 200:
            await ctx.respond('Really.')
            return
        try:
            monsters = await database.get_monsters(name)
        except database.NoDataFound:
            await ctx.respond('I didn\'t find any monsters with that search query, sorry. Try searching for something else.')
            return
        embeds = []
        chunk_amount = 0
        for chunk in range(0, len(monsters), 6):
            monsters_chunk = monsters[chunk:chunk+6]
            chunk_amount += 1
            embed = await embed_monsters(len(monsters), monsters_chunk)
            embeds.append(embed)
        if len(embeds) > 1:
            view = views.PaginatorView(ctx, embeds)
            interaction = await ctx.respond(embed=embeds[0], view=view)
            view.interaction = interaction
            await view.wait()
            await interaction.edit_original_message(view=None)
        else:
            await ctx.respond(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(MonstersCog(bot))


# --- Redundancies ---
# Guides
guide_mobs_all = '`{prefix}mobs` : List of all monsters'
guide_mobs_area = '`{prefix}mobs [area]` : List of monsters in area [area]'
guide_mob_daily = '`{prefix}dailymob` : Where to find the daily monster'


# --- Embeds ---
async def embed_monsters(amount_found: int, monsters: Tuple[database.Monster]):
    """Monster search results"""

    description = f'Your search returned **{amount_found}** results.'

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MONSTER SEARCH',
        description = description
    )

    monster = type(database.Monster)
    for monster in monsters:
        if monster.areas[0] == monster.areas[1]:
            field_value = f'{emojis.BP} Found in area **{monster.areas[0]}** with `{monster.activity}`'
        else:
            field_value = f'{emojis.BP} Found in areas **{monster.areas[0]}~{monster.areas[1]}** with `{monster.activity}`'
        if monster.drop_name is not None:
            field_value = f'{field_value}\n{emojis.BP} Drops {monster.drop_emoji} {monster.drop_name}'
        embed.add_field(name=f'{monster.name.upper()} {monster.emoji}', value=field_value, inline=False)

    return embed