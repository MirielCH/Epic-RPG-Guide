# monsters.py

import asyncio
from typing import Optional, Tuple

import discord

import database
from resources import emojis, functions, settings, strings, views


ALL_MONSTERS = functions.await_coroutine(database.get_all_monsters())


# --- Commands ---
async def command_monster_drops(ctx: discord.ApplicationContext) -> None:
    """Monster drop command"""
    embed = await embed_monster_drops()
    await ctx.respond(embed=embed)


async def command_monster_search(bot: discord.Bot, ctx: discord.ApplicationContext, name: Optional[str] = None) -> None:
    """Monster search command"""
    if name is not None:
        if len(name) < 3:
            await ctx.respond(strings.MSG_SEARCH_QUERY_TOO_SHORT, ephemeral=True)
            return
        if len(name) > 200:
            await ctx.respond(strings.MSG_INPUT_TOO_LONG, ephemeral=True)
            return
        try:
            monsters = await database.get_monsters(name)
        except database.NoDataFound:
            await ctx.respond(
                'I didn\'t find any monsters with that search query, sorry. Try searching for something else.',
                ephemeral=True
            )
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
            try:
                await functions.edit_interaction(interaction, view=None)
            except discord.errors.NotFound:
                pass
        else:
            await ctx.respond(embed=embed)

    if name is None:
        monster = await database.get_daily_monster(name)
        if monster is None:
            bot_message_task = asyncio.ensure_future(functions.wait_for_world_message(bot, ctx))
            try:
                content = strings.MSG_WAIT_FOR_INPUT_SLASH.format(user=ctx.author.name,
                                                                  command=strings.SLASH_COMMANDS_EPIC_RPG["world"])
                bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, content)
            except asyncio.TimeoutError:
                await ctx.respond(
                    strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='world'),
                    ephemeral=True
                )
                return
            if bot_message is None: return
            name = await functions.extract_monster_name_from_world_embed(ctx, bot_message)
            try:
                monster = await database.get_monster_by_name(name)
            except database.NoDataFound:
                await ctx.respond(
                    f'I didn\'t find a monster with that name, sorry. This ain\'t intended, so please report this to the '
                    f'support server if convenient.',
                    ephemeral=True
                )
                return
            await monster.set_daily()
        embed = await embed_daily_monster(monster)
        await ctx.respond(embed=embed)


# --- Embeds ---
async def embed_monsters(amount_found: int, monsters: Tuple[database.Monster]):
    """Monster search results"""
    description = f'Your search returned **{amount_found}** results.'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MONSTER SEARCH',
        description = description
    )
    embed.set_footer(text='Use "/monster drops" to see all monster drops at once')
    monster = type(database.Monster)
    for monster in monsters:
        if monster.areas[0] == monster.areas[1]:
            field_value = (
                f'{emojis.BP} Found in area **{monster.areas[0]}** with '
                f'{strings.SLASH_COMMANDS_EPIC_RPG[monster.activity]}'
            )
        else:
            field_value = (
                f'{emojis.BP} Found in areas **{monster.areas[0]}~{monster.areas[1]}** with '
                f'{strings.SLASH_COMMANDS_EPIC_RPG[monster.activity]}'
            )
        if monster.drop_name is not None:
            field_value = f'{field_value}\n{emojis.BP} Drops {monster.drop_emoji} {monster.drop_name}'
        embed.add_field(name=f'{monster.name.upper()} {monster.emoji}', value=field_value, inline=False)
    return embed


async def embed_daily_monster(monster: database.Monster):
    """Daily monster search result"""
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'DAILY MONSTER SEARCH',
    )
    if monster.areas[0] == monster.areas[1]:
        field_value = (
            f'{emojis.BP} Found in area **{monster.areas[0]}** with '
            f'{strings.SLASH_COMMANDS_EPIC_RPG[monster.activity]}'
        )
    else:
        field_value = (
            f'{emojis.BP} Found in areas **{monster.areas[0]}~{monster.areas[1]}** with '
            f'{strings.SLASH_COMMANDS_EPIC_RPG[monster.activity]}'
        )
    if monster.drop_name is not None:
        field_value = f'{field_value}\n{emojis.BP} Drops {monster.drop_emoji} {monster.drop_name}'
    embed.add_field(name=f'{monster.name.upper()} {monster.emoji}', value=field_value, inline=False)
    return embed


async def embed_monster_drops() -> discord.Embed:
    """Monster drops"""
    wolfskin = (
        f'{emojis.BP} Areas: 1~2\n'
        f'{emojis.BP} Source: {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.BP} Monster: {emojis.MOB_WOLF}\n'
        f'{emojis.BP} Value: 500\n'
        f'{emojis.BLANK}'
    )
    zombieeye = (
        f'{emojis.BP} Areas: 3~4\n'
        f'{emojis.BP} Source: {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.BP} Monster: {emojis.MOB_ZOMBIE}\n'
        f'{emojis.BP} Value: 2,000\n'
        f'{emojis.BLANK}'
    )
    unicornhorn = (
        f'{emojis.BP} Areas: 5~6\n'
        f'{emojis.BP} Source: {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.BP} Monster: {emojis.MOB_UNICORN}\n'
        f'{emojis.BP} Value: 7,500\n'
        f'{emojis.BLANK}'
    )
    mermaidhair = (
        f'{emojis.BP} Areas: 7~8\n'
        f'{emojis.BP} Source: {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.BP} Monster: {emojis.MOB_MERMAID}\n'
        f'{emojis.BP} Value: 30,000\n'
        f'{emojis.BLANK}'
    )
    chip = (
        f'{emojis.BP} Areas: 9~10\n'
        f'{emojis.BP} Source: {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.BP} Monster: {emojis.MOB_KILLER_ROBOT}\n'
        f'{emojis.BP} Value: 100,000\n'
        f'{emojis.BLANK}'
    )
    dragonscale = (
        f'{emojis.BP} Areas: 11~15\n'
        f'{emojis.BP} Source: {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.BP} Monsters: {emojis.MOB_BABY_DRAGON}{emojis.MOB_TEEN_DRAGON}{emojis.MOB_ADULT_DRAGON}{emojis.MOB_OLD_DRAGON}\n'
        f'{emojis.BP} Value: 250,000\n'
        f'{emojis.BLANK}'
    )
    dark_energy = (
        f'{emojis.BP} Areas: 16~20\n'
        f'{emojis.BP} Source: {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.BP} Monsters: All monsters\n'
        f'{emojis.BP} Value: 5,000,000\n'
        f'{emojis.BLANK}'
    )
    epic_berry = (
        f'{emojis.BP} Areas: All areas\n'
        f'{emojis.BP} Source: {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} Monsters: All monsters\n'
        f'{emojis.BP} Value: Can\'t be sold\n'
        f'{emojis.BLANK}'
    )
    chance = (
        f'{emojis.BP} The drop chance depends on the following:\n'
        f'{emojis.DETAIL} Your horse tier\n'
        f'{emojis.DETAIL} Your time travel count\n'
        f'{emojis.DETAIL} The command mode (`hardmode` increases drop chance)\n'
        f'{emojis.DETAIL} World buffs in {strings.SLASH_COMMANDS_EPIC_RPG["world"]}\n'
        f'{emojis.BP} To see the your drop chance, use {strings.SLASH_COMMANDS_GUIDE["drop chance calculator"]}\n'
        f'{emojis.BLANK}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MONSTER DROPS',
        description = (
            f'These items can drop when using certain commands.\n'
            f'You can move to other areas with {strings.SLASH_COMMANDS_EPIC_RPG["area"]}.\n'
            f'{emojis.BLANK}'
        )
    )
    embed.set_footer(text='Use "/monster search" to look up specific monsters')
    embed.add_field(name=f'WOLF SKIN {emojis.WOLF_SKIN}', value=wolfskin, inline=True)
    embed.add_field(name=f'ZOMBIE EYE {emojis.ZOMBIE_EYE}', value=zombieeye, inline=True)
    embed.add_field(name=f'UNICORN HORN {emojis.UNICORN_HORN}', value=unicornhorn, inline=True)
    embed.add_field(name=f'MERMAID HAIR {emojis.MERMAID_HAIR}', value=mermaidhair, inline=True)
    embed.add_field(name=f'CHIP {emojis.CHIP}', value=chip, inline=True)
    embed.add_field(name=f'DRAGON SCALE {emojis.DRAGON_SCALE}', value=dragonscale, inline=True)
    embed.add_field(name=f'DARK ENERGY {emojis.DARK_ENERGY}', value=dark_energy, inline=True)
    embed.add_field(name=f'EPIC BERRY {emojis.EPIC_BERRY}', value=epic_berry, inline=True)
    embed.add_field(name='DROP CHANCE', value=chance, inline=False)
    return embed