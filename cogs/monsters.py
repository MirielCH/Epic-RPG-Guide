# monsters.py

import asyncio
from typing import Tuple

import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup

import database
from resources import emojis, functions, settings, strings, views


ALL_MONSTERS = functions.await_coroutine(database.get_all_monsters())


# --- Functions ---
async def monster_searcher(ctx: discord.AutocompleteContext):
    """Returns a list of matching monsters from ALL_MONSTER_NAMES"""
    return [monster.name for monster in ALL_MONSTERS if ctx.value.lower() in monster.name.lower()]


class MonstersCog(commands.Cog):
    """Cog with monster commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_monster = SlashCommandGroup(
        "monster",
        "Monster search commands",
    )

    @cmd_monster.command(name='drops', description='Monster drops and where to find them')
    async def professions_guide(self, ctx: discord.ApplicationContext) -> None:
        """Monster drops"""
        embed = await embed_monster_drops()
        await ctx.respond(embed=embed)

    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_monster.command(name='search', description='Look up monsters by name')
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


async def embed_monster_drops() -> discord.Embed:
    """Monster drops"""
    wolfskin = (
        f'{emojis.BP} Areas: 1~2\n'
        f'{emojis.BP} Source: {emojis.MOB_WOLF}\n'
        f'{emojis.BP} Value: 500\n'
        f'{emojis.BLANK}'
    )
    zombieeye = (
        f'{emojis.BP} Areas: 3~4\n'
        f'{emojis.BP} Source: {emojis.MOB_ZOMBIE}\n'
        f'{emojis.BP} Value: 2,000\n'
        f'{emojis.BLANK}'
    )
    unicornhorn = (
        f'{emojis.BP} Areas: 5~6\n'
        f'{emojis.BP} Source: {emojis.MOB_UNICORN}\n'
        f'{emojis.BP} Value: 7,500\n'
        f'{emojis.BLANK}'
    )
    mermaidhair = (
        f'{emojis.BP} Areas: 7~8\n'
        f'{emojis.BP} Source: {emojis.MOB_MERMAID}\n'
        f'{emojis.BP} Value: 30,000\n'
        f'{emojis.BLANK}'
    )
    chip = (
        f'{emojis.BP} Areas: 9~10\n'
        f'{emojis.BP} Source: {emojis.MOB_KILLER_ROBOT}\n'
        f'{emojis.BP} Value: 100,000\n'
        f'{emojis.BLANK}'
    )
    dragonscale = (
        f'{emojis.BP} Areas: 11~15\n'
        f'{emojis.BP} Source: {emojis.MOB_BABY_DRAGON}{emojis.MOB_TEEN_DRAGON}{emojis.MOB_ADULT_DRAGON}{emojis.MOB_OLD_DRAGON}\n'
        f'{emojis.BP} Value: 250,000\n'
        f'{emojis.BLANK}'
    )
    dark_energy = (
        f'{emojis.BP} Areas: 16~20\n'
        f'{emojis.BP} Source: {emojis.MOB_VOID_SHARD}{emojis.MOB_ABYSS_BUG}{emojis.MOB_CORRUPTED_UNICORN}'
        f'{emojis.MOB_NEUTRON_STAR}{emojis.MOB_TIME_ALTERATION}\n'
        f'{emojis.BP} Value: 5,000,000\n'
        f'{emojis.BLANK}'
    )
    chance = (
        f'{emojis.BP} The chance to encounter a mob that drops items is 50 %\n'
        f'{emojis.BP} These mobs have a base chance of 4 % to drop an item\n'
        f'{emojis.BP} Thus you have a total base drop chance of 2 % when hunting\n'
        f'{emojis.BP} Every {emojis.TIME_TRAVEL} time travel increases the drop chance by ~25%\n'
        f'{emojis.BP} A {emojis.HORSE_T7} T7 horse increases the drop chance by 20%\n'
        f'{emojis.BP} A {emojis.HORSE_T8} T8 horse increases the drop chance by 50%\n'
        f'{emojis.BP} A {emojis.HORSE_T9} T9 horse increases the drop chance by 100%\n'
        f'{emojis.BP} A {emojis.HORSE_T10} T10 horse increases the drop chance by 200%\n'
        f'{emojis.BP} To see your drop chance, use `/dropchance calculator`\n{emojis.BLANK}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MONSTER DROPS',
        description = (
            f'These items drop when using `hunt`, `hunt together` or when opening lootboxes.\n'
            f'You can go back to previous areas with `rpg area`.\n'
            f'{emojis.BLANK}'
        )
    )
    embed.set_footer(text=strings.DEFAULT_FOOTER)
    embed.add_field(name=f'WOLF SKIN {emojis.WOLF_SKIN}', value=wolfskin, inline=True)
    embed.add_field(name=f'ZOMBIE EYE {emojis.ZOMBIE_EYE}', value=zombieeye, inline=True)
    embed.add_field(name=f'UNICORN HORN {emojis.UNICORN_HORN}', value=unicornhorn, inline=True)
    embed.add_field(name=f'MERMAID HAIR {emojis.MERMAID_HAIR}', value=mermaidhair, inline=True)
    embed.add_field(name=f'CHIP {emojis.CHIP}', value=chip, inline=True)
    embed.add_field(name=f'DRAGON SCALE {emojis.DRAGON_SCALE}', value=dragonscale, inline=True)
    embed.add_field(name=f'DARK ENERGY {emojis.DARK_ENERGY}', value=dark_energy, inline=True)
    embed.add_field(name='DROP CHANCE', value=chance, inline=False)
    return embed