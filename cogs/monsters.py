# monsters.py

import asyncio
from typing import Tuple

import discord
from discord.ext import commands
# from discord_components import Button, ButtonStyle, InteractionType

import database
import emojis
import global_data


# monsters commands (cog)
class monstersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Mobs list
    @commands.command(aliases=('monster','monsters','mob','monsterlist','monsterslist','moblist','mobslist',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def mobs(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        prefix = ctx.prefix
        error_area = f'This is not a valid area. The syntax is `{prefix}mobs [area]`. The area has to be between 1 and 20.'
        info_top = (
            f'The TOP does not have its own monsters.\n'
            f'Instead the EPIC NPC poses as a random monster which can be any monster from areas 1~15.'
        )
        error_syntax = ( #Temporary solution because buttons use a shit ton of cpu for some reason
            f'This command shows all mobs in an area.\n'
            f'The syntax is `{prefix}mobs [area]`. The area has to be between 1 and 20.'
        )

        if args:
            area_no = args[0].lower().replace('a','')
            if area_no.isnumeric():
                try:
                    area_no = int(area_no)
                except:
                    await ctx.send(error_area)
                    return
                if not 1 <= area_no <= 20:
                    await ctx.send(error_area)
                    return
            else:
                if 'top' in area_no:
                    await ctx.send(info_top)
                    return
                else:
                    await ctx.send(error_area)
                    return
        else:
            await ctx.send(error_syntax)
            return
            # area = 1

        monsters = await database.get_monster_by_area(area_no, area_no)
        embed = await embed_mobs(ctx, monsters, area_no)
        await ctx.send(embed=embed)

    # Daily mob lookup
    @commands.command(aliases=('mobdaily','daily',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def dailymob(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                if (str(m.embeds[0].fields).find('Daily monster') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg world` (or `abort` to abort)')
            answer_message = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_message.content
            answer = answer.lower()
            if answer == 'rpg world':
                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    embed_world = str(answer_bot_at.embeds[0].fields)
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                end_daily = embed_world.find('**\\nThis monster')
                start_daily = embed_world.rfind('**',0,end_daily) + 2
                daily_mob = embed_world[start_daily:end_daily]
            elif answer in ('abort','cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send(f'Wrong input. Aborting.')
                return

            try:
                monster: database.Monster = await database.get_monster_by_name(daily_mob)
            except database.NoDataFound:
                await ctx.send(f'Couldn\'t find the mob **{daily_mob}**, sorry.')
                return
            if monster.areas[0] == monster.areas[1]:
                await ctx.send(
                    f'{monster.emoji} **{monster.name}** can be found in **area {monster.areas[0]}** '
                    f'by using `rpg {monster.activity}`.'
                )
            else:
                await ctx.send(
                    f'{monster.emoji} **{monster.name}** can be found in **areas {monster.areas[0]}-{monster.areas[1]}** '
                    f'by using `rpg {monster.activity}`.'
                )
        except asyncio.TimeoutError:
            await ctx.send(f'**{ctx.author.name}**, couldn\'t find the daily monster, RIP.')
            return

# Initialization
def setup(bot):
    bot.add_cog(monstersCog(bot))



# --- Redundancies ---
# Guides
guide_mobs_all = '`{prefix}mobs` : List of all monsters'
guide_mobs_area = '`{prefix}mobs [area]` : List of monsters in area [area]'
guide_mob_daily = '`{prefix}dailymob` : Where to find the daily monster'



# --- Embeds ---
async def embed_mobs(ctx: commands.Context, monsters: Tuple[database.Monster], area_no: int):
    """Mobs list"""
    prefix = ctx.prefix
    guides = (
        #f'{emojis.BP} {guide_mobs_all.format(prefix=prefix)}\n'
        #f'{emojis.BP} {guide_mobs_area.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_mob_daily.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = f'MONSTERS IN AREA {area_no}'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))

    field_monsters_hunt = field_monsters_adv = ''
    for monster in monsters:
        if monster.activity == 'hunt':
            field_monsters_hunt = f'{field_monsters_hunt}\n{emojis.BP} {monster.emoji} {monster.name}'
            if monster.drop_emoji is not None:
                field_monsters_hunt = f'{field_monsters_hunt} (drops {monster.drop_emoji})'
        elif monster.activity == 'adventure':
            field_monsters_adv = f'{field_monsters_adv}\n{emojis.BP} {monster.emoji} {monster.name}'

    if field_monsters_hunt != '':
        embed.add_field(name='HUNT', value=field_monsters_hunt, inline=False)
    if field_monsters_adv != '':
        embed.add_field(name='ADVENTURE', value=field_monsters_adv, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed