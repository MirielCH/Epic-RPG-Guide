# horse.py
"""Contains all horse related guides and calculators"""

import asyncio
from math import floor

import discord
from discord.ext import commands

import database
from resources import emojis
from resources import settings
from resources import functions, strings


# Error messages
MSG_INVALID_HORSE_TIER = '**{user}**, this is not a valid horse tier.'
MSG_INVALID_HORSE_LEVEL = '**{user}**, this is not a valid horse level.'
MSG_INVALID_HORSE_TARGET_LEVEL = '**{user}**, this is not a valid horse target level.'
MSG_INVALID_LOOTBOXER_LEVEL = '**{user}**, this is not a valid lootboxer level.'
MSG_HORSE_TIER_RANGE = '**{user}**, the horse tier needs to be between 1 and 10.'
MSG_HORSE_LEVEL_RANGE_1 = '**{user}**, the horse level needs to be between 1 and 140.'
MSG_HORSE_LEVEL_RANGE_2 = '**{user}**, the horse level needs to be between 2 and 140.'
MSG_LOOTBOXER_LEVEL_RANGE = '**{user}**, the lootboxer level needs to be between 1 and 150.'
MSG_HORSE_LEVEL_MIN_1 = '**{user}**, the horse level needs to be 1 or higher.'
MSG_HORSE_LEVEL_ALREADY_MAX = (
    '**{user}**, your horse is already at max level. You can\'t level up any further until you increase your '
    'lootboxer profession.'
)
MSG_HORSE_LEVEL_ALREADY_TARGET = '**{user}**, your horse is already at the target level.'
MSG_HORSE_LEVEL_OVER_TARGET = (
    '**{user}**, sorry mate, but training your horse to level **down** is not exactly an option right now.'
)
MSG_HORSE_LEVEL_MAX_POSSIBLE = (
    'With a {horse_emoji} **T{horse_tier}** horse and lootboxer **L{lootboxer_level}**, your max horse '
    'level is **L{horse_max_level}**.'
)


# Additional guides
GUIDE_OVERVIEW = '`{prefix}horse` : Horse overview'
GUIDE_BREED = '`{prefix}horse breed` : Details about horse breeding'
GUIDE_TIER = '`{prefix}horse tier` : Details about horse tiers'
GUIDE_TYPE = '`{prefix}horse type` : Details about horse types'
CALC_HTC = '`{prefix}htc` : Coins you need for your next horse levels'
CALC_HTCTOTAL = '`{prefix}htctotal [level]` : Total coins you need to reach `[level]`'
CALC_TYPE = '`{prefix}hc` : Horse stats bonus calculator'


class HorseOldCog(commands.Cog):
    """Cog with horse commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    horse_aliases = (
        'horses',
        'htier',
        'horsestier',
        'horsetiers',
        'horsestiers',
        'htype',
        'horsestype',
        'horsetypes',
        'horsestypes',
        'hbreed',
        'hbreeding',
        'breed',
        'breeding',
        'horsebreeding',
        'horsesbreed',
        'horsesbreeding',
        'breedhorse',
        'breedhorses',
        'breedinghorse',
        'breedingshorses'
    )

    @commands.command(aliases=horse_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def horse(self, ctx: commands.Context, *args: str) -> None:
        """Horse main command"""
        prefix = ctx.prefix
        if args:
            args = [arg.lower() for arg in args]
            command, *_ = args
        else:
            command = ctx.invoked_with.lower()
        if 'tier' in command:
            embed = await embed_horses_tiers(prefix)
        elif 'type' in command:
            embed = await embed_horses_types(prefix)
        elif 'breed' in command:
            embed = await embed_horses_breeding(prefix)
        elif 'calc' in command:
            if args: del args[0]
            await self.horsecalc(ctx, *args)
            return
        else:
            embed = await embed_horses_overview(prefix)
        await ctx.send(embed=embed)

    @commands.command(aliases=('hcalc','hc'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def horsecalc(self, ctx: commands.Context, *args: str) -> None:
        """Calculates the horse stat bonuses"""
        user_name = ctx.author.name
        def check(m):
            return (m.author == ctx.author) and (m.channel == ctx.channel)

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = functions.format_string(str(user_name))
                embed_author = functions.format_string(str(m.embeds[0].author))
                if f'{ctx_author}\'s horse' in embed_author:
                    correct_embed = True
            except:
                pass
            return (m.author.id == settings.EPIC_RPG_ID) and (m.channel == ctx.channel) and correct_embed

        prefix = ctx.prefix
        message_syntax = (
            f'{strings.MSG_SYNTAX.format(syntax=f"{prefix}horsecalc [tier] [level]")}\n\n'
            'You can also omit all parameters to use your horse tier and level for the calculation.\n'
            f'Examples: `{prefix}horsecalc 6 25` or `{prefix}horsecalc t7 l30` or `{prefix}horsecalc`'
        )
        if args:
            if len(args) != 2:
                await ctx.send(message_syntax)
                return
            args = [arg.lower() for arg in args]
            horse_tier, horse_level = args
            try:
                horse_tier = int(horse_tier.replace('t',''))
            except:
                await ctx.send(f'{MSG_INVALID_HORSE_TIER.format(user=user_name)}\n\n{message_syntax}')
                return
            try:
                horse_level = int(horse_level.replace('l',''))
            except:
                await ctx.send(f'{MSG_INVALID_HORSE_LEVEL.format(user=user_name)}\n\n{message_syntax}')
                return
            if not 1 <= horse_level <= 140:
                await ctx.send(f'{MSG_HORSE_LEVEL_RANGE_1.format(user=user_name)}\n\n{message_syntax}')
                return
            if not 1 <= horse_tier <= 10:
                await ctx.send(f'{MSG_HORSE_TIER_RANGE.format(user=user_name)}\n\n{message_syntax}')
                return
        else:
            try:
                await ctx.send(strings.MSG_WAIT_FOR_INPUT.format(user=user_name, command='rpg horse'))
                answer_user_horse = await self.bot.wait_for('message', check=check, timeout=30)
                answer = answer_user_horse.content.lower()
                if answer == 'rpg horse':
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                elif answer in ('abort', 'cancel'):
                    await ctx.send(strings.MSG_ABORTING)
                    return
                else:
                    await ctx.send(strings.MSG_WRONG_INPUT)
                    return
            except asyncio.TimeoutError as error:
                await ctx.send(strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=user_name, information='horse'))
                return
            try:
                horse_stats = str(answer_bot_at.embeds[0].fields[0])
                start_level = horse_stats.find('Horse Level** -') + 16
                end_level = start_level + 3
                horse_level = int(horse_stats[start_level:end_level].replace('\\','').strip())
            except:
                await ctx.send(strings.MSG_ERROR)
                return
            if 'Tier** - III' in horse_stats:
                horse_chance = 1
                horse_tier = 3
            elif 'Tier** - II' in horse_stats:
                horse_chance = 1
                horse_tier = 2
            elif 'Tier** - VIII' in horse_stats:
                horse_chance = 1.5
                horse_tier = 8
            elif 'Tier** - VII' in horse_stats:
                horse_chance = 1.2
                horse_tier = 7
            elif 'Tier** - VI' in horse_stats:
                horse_chance = 1
                horse_tier = 6
            elif 'Tier** - V' in horse_stats:
                horse_chance = 1
                horse_tier = 5
            elif 'Tier** - IV' in horse_stats:
                horse_chance = 1
                horse_tier = 4
            elif 'Tier** - IX' in horse_stats:
                horse_chance = 2
                horse_tier = 9
            elif 'Tier** - I' in horse_stats:
                horse_chance = 1
                horse_tier = 1
            elif 'Tier** - X' in horse_stats:
                horse_chance = 3
                horse_tier = 10
            else:
                await ctx.send(strings.MSG_ERROR)
                return
        horse_emoji = getattr(emojis, f'HORSE_T{horse_tier}')
        try:
            horse_data = await database.get_horse_data(ctx, horse_tier)
        except Exception as error:
            await ctx.send(strings.MSG_ERROR)
            return
        def_bonus = horse_data['def_level_bonus']
        festive_bonus = horse_data['festive_level_bonus']
        golden_bonus = horse_data['golden_level_bonus']
        magic_bonus = horse_data['magic_level_bonus']
        special_bonus = horse_data['special_level_bonus']
        strong_bonus = horse_data['strong_level_bonus']
        super_special_bonus = horse_data['super_special_level_bonus']
        tank_bonus = horse_data['tank_level_bonus']
        await ctx.send(
            f'Stat bonuses for a {horse_emoji} **T{horse_tier} L{horse_level}** horse:\n'
            f'{emojis.BP} **DEFENDER**: {def_bonus * horse_level:,g}% extra DEF\n'
            f'{emojis.BP} **FESTIVE**: {festive_bonus * horse_level:,g}% extra chance to spawn random events\n'
            f'{emojis.BP} **GOLDEN**: {golden_bonus * horse_level:,g}% extra coins from `rpg hunt` and `rpg adventure`\n'
            f'{emojis.BP} **MAGIC**: {magic_bonus * horse_level:,g}% increased enchantment efficiency\n'
            f'{emojis.BP} **SPECIAL**: {special_bonus * horse_level:,g}% extra coins and XP from the epic quest\n'
            #f'{emojis.BP} {emojis.HAL_PUMPKIN} **SPOOKY**: {strong_bonus * horse_level * 1.25:,g}% extra chance to find pumpkins and 5% extra '
            #f'chance to find bat slimes\n'
            f'{emojis.BP} **STRONG**: {strong_bonus * horse_level:,g}% extra AT\n'
            f'{emojis.BP} **SUPER SPECIAL**: {super_special_bonus * horse_level:,g}% extra coins and XP from the epic '
            f'quest\n'
            f'{emojis.BP} **TANK**: {tank_bonus * horse_level:,g}% extra LIFE\n'
        )

    @commands.command(aliases=('horsetraincalc','horsetrainingcalc','horsetraining','htraincalc',
                               'htrainingcalc','htcalc'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def htc(self, ctx: commands.Context, *args: str) -> None:
        """Horse training cost calculator"""
        user_name = ctx.author.name
        def check(m):
            return (m.author == ctx.author) and (m.channel == ctx.channel)

        def epic_rpg_check_horse(m):
            correct_embed = False
            try:
                ctx_author = functions.format_string(str(user_name))
                embed_author = functions.format_string(str(m.embeds[0].author))
                if f'{ctx_author}\'s horse' in embed_author:
                    correct_embed = True
            except:
                pass
            return (m.author.id == settings.EPIC_RPG_ID) and (m.channel == ctx.channel) and correct_embed

        def epic_rpg_check_professions(m):
            correct_embed = False
            try:
                ctx_author = functions.format_string(str(user_name))
                embed_author = functions.format_string(str(m.embeds[0].author))
                if f'{ctx_author}\'s professions' in embed_author:
                    correct_embed = True
            except:
                pass
            return (m.author.id == settings.EPIC_RPG_ID) and (m.channel == ctx.channel) and correct_embed

        prefix = ctx.prefix
        message_syntax = (
            f'{strings.MSG_SYNTAX.format(syntax=f"{prefix}htc [horse tier] [horse level] [lootboxer level]")}\n\n'
            f'Or just use `{prefix}htc` and let me ask you.\n'
            f'Examples: `{prefix}htc t5 l35 l75` or `{prefix}htc 4 18 48`'
        )
        horse_tier = 0
        horse_level = 0
        lootboxer_level = 0
        if args:
            args = [arg.lower() for arg in args]
            arg, *_ = args
            if arg == 'total':
                del args[0]
                await self.htctotal(ctx, *args)
                return
            if len(args) < 2:
                await ctx.send(message_syntax)
                return
            horse_tier, horse_level, *args_rest = args
            try:
                horse_tier = int(horse_tier.replace('t',''))
            except:
                await ctx.send(f'{MSG_INVALID_HORSE_TIER.format(user=user_name)}\n\n{message_syntax}')
                return
            try:
                horse_level = int(horse_level.replace('l',''))
            except:
                await ctx.send(f'{MSG_INVALID_HORSE_LEVEL.format(user=user_name)}\n\n{message_syntax}')
                return
            if not 1 <= horse_tier <= 10:
                await ctx.send(
                    f'{MSG_HORSE_TIER_RANGE.format(user=user_name)}\n\n{message_syntax}'
                )
                return
            if not 1 <= horse_level <= 140:
                await ctx.send(
                    f'{MSG_HORSE_LEVEL_RANGE_1.format(user=user_name)}\n\n{message_syntax}'
                )
                return
            if len(args) > 2:
                lootboxer_level, *_ = args_rest
                try:
                    lootboxer_level = int(lootboxer_level.replace('l',''))
                except:
                    await ctx.send(f'{MSG_INVALID_LOOTBOXER_LEVEL.format(user=user_name)}\n\n{message_syntax}')
                    return
                if not 1 <= lootboxer_level <= 150:
                    await ctx.send(f'{MSG_LOOTBOXER_LEVEL_RANGE.format(user=user_name)}\n\n{message_syntax}')
                    return

        if (horse_tier == 0) or (horse_level == 0):
            try:
                await ctx.send(strings.MSG_WAIT_FOR_INPUT.format(user=user_name, command='rpg horse'))
                answer_horse = await self.bot.wait_for('message', check=check, timeout=30)
                answer = answer_horse.content.lower()
                if answer == 'rpg horse':
                    answer_bot_horse = await self.bot.wait_for('message', check=epic_rpg_check_horse, timeout=5)
                elif answer in ('abort', 'cancel'):
                    await ctx.send(strings.MSG_ABORTING)
                    return
                else:
                    await ctx.send(strings.MSG_WRONG_INPUT)
                    return
            except asyncio.TimeoutError as error:
                await ctx.send(strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=user_name, information='horse'))
                return
            try:
                horse_stats = str(answer_bot_horse.embeds[0].fields[0])
                start_level = horse_stats.find('Horse Level** -') + 16
                end_level = start_level + 3
                horse_level = int(horse_stats[start_level:end_level].replace('\\','').replace('(','').strip())
            except:
                await ctx.send(strings.MSG_ERROR)
                return
            if 'Tier** - III' in horse_stats:
                horse_tier = 3
            elif 'Tier** - II' in horse_stats:
                horse_tier = 2
            elif 'Tier** - VIII' in horse_stats:
                horse_tier = 8
            elif 'Tier** - VII' in horse_stats:
                horse_tier = 7
            elif 'Tier** - VI' in horse_stats:
                horse_tier = 6
            elif 'Tier** - V' in horse_stats:
                horse_tier = 5
            elif 'Tier** - IV' in horse_stats:
                horse_tier = 4
            elif 'Tier** - IX' in horse_stats:
                horse_tier = 9
            elif 'Tier** - I' in horse_stats:
                horse_tier = 1
            elif 'Tier** - X' in horse_stats:
                horse_tier = 10
            else:
                await ctx.send(strings.MSG_ERROR)
                return

        if lootboxer_level == 0:
            try:
                await ctx.send(strings.MSG_WAIT_FOR_INPUT.format(user=user_name, command='rpg pr'))
                answer_user_pr = await self.bot.wait_for('message', check=check, timeout=30)
                answer = answer_user_pr.content.lower()
                if answer in ('rpg pr', 'rpg profession', 'rpg professions'):
                    answer_bot_pr = await self.bot.wait_for('message', check=epic_rpg_check_professions, timeout=5)
                elif answer in ('abort', 'cancel'):
                    await ctx.send(strings.MSG_ABORTING)
                    return
                else:
                    await ctx.send(strings.MSG_WRONG_INPUT)
                    return
            except asyncio.TimeoutError as error:
                await ctx.send(strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=user_name, information='profession'))
                return
            try:
                professions = str(answer_bot_pr.embeds[0].fields[2])
                start_level = professions.find('Lootboxer Lv ') + 13
                end_level = professions.find(' |', start_level)
                lootboxer_level = int(professions[start_level:end_level])
            except:
                await ctx.send(strings.MSG_ERROR)
                return

        horse_emoji = getattr(emojis, f'HORSE_T{horse_tier}')
        if lootboxer_level > 100:
            horse_max_level = 10 * horse_tier + (lootboxer_level - 100)
        else:
            horse_max_level = 10 * horse_tier
        if horse_max_level < horse_level:
            horse_level_max_possible = MSG_HORSE_LEVEL_MAX_POSSIBLE.format(
                horse_emoji=horse_emoji, horse_tier=horse_tier, lootboxer_level=lootboxer_level,
                horse_max_level=horse_max_level
            )
            await ctx.send(
                f'{MSG_INVALID_HORSE_LEVEL.format(user=user_name)}\n'
                f'{horse_level_max_possible}'
            )
            return
        if (horse_max_level - horse_level) >= 11:
            horse_level_range = horse_level + 11
        else:
            horse_level_range = horse_level + (horse_max_level-horse_level)
        if horse_level == horse_max_level:
            await ctx.send(MSG_HORSE_LEVEL_ALREADY_MAX.format(user=user_name))
            return
        output = (
                f'For a {horse_emoji} **T{horse_tier} L{horse_level}** horse with lootboxer level **{lootboxer_level}** '
                f'the horse training costs for your next levels are as follows:'
            )
        for level in range(horse_level, horse_level_range):
            level_cost = floor(
                (level ** 4) * ((level ** 2) + (210 * level) + 2200) * (500 - (lootboxer_level**1.2)) / 100000
            )
            output = f'{output}\n{emojis.BP} Level {level} to {level+1}: **{level_cost:,}** coins'
        await ctx.send(output)

    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def htctotal(self, ctx: commands.Context, *args: str) -> None:
        """Calculate total horse training costs up to a level"""
        user_name = ctx.author.name

        def check(m):
            return (m.author == ctx.author) and (m.channel == ctx.channel)

        def epic_rpg_check_horse(m):
            correct_embed = False
            try:
                ctx_author = functions.format_string(str(user_name))
                embed_author = functions.format_string(str(m.embeds[0].author))
                if f'{ctx_author}\'s horse' in embed_author:
                    correct_embed = True
            except:
                pass
            return (m.author.id == settings.EPIC_RPG_ID) and (m.channel == ctx.channel) and correct_embed

        def epic_rpg_check_professions(m):
            correct_embed = False
            try:
                ctx_author = functions.format_string(str(user_name))
                embed_author = functions.format_string(str(m.embeds[0].author))
                if f'{ctx_author}\'s professions' in embed_author:
                    correct_embed = True
            except:
                pass
            return (m.author.id == settings.EPIC_RPG_ID) and (m.channel == ctx.channel) and correct_embed

        prefix = ctx.prefix
        horse_target_level = 0
        message_syntax = (
            f'{strings.MSG_SYNTAX.format(syntax=f"{prefix}htctotal [horse target level]")}\n\n'
            f'Or just use `{prefix}htctotal` to calculate up to your current max horse level.\n'
            f'Examples: `{prefix}htctotal l80` or `{prefix}htctotal 65`'
        )
        if args:
            horse_target_level, *_ = args
            try:
                horse_target_level = int(horse_target_level.lower().replace('l',''))
            except:
                await ctx.send(f'{MSG_INVALID_HORSE_LEVEL.format(user=user_name)}\n\n{message_syntax}')
                return
            if not 2 <= horse_target_level <= 140:
                await ctx.send(f'{MSG_HORSE_LEVEL_RANGE_2.format(user=user_name)}\n\n{message_syntax}')
                return
        try:
            await ctx.send(strings.MSG_WAIT_FOR_INPUT.format(user=user_name, command='rpg horse'))
            answer_user_horse = await self.bot.wait_for('message', check=check, timeout=30)
            answer = answer_user_horse.content.lower()
            if answer == 'rpg horse':
                answer_bot_horse = await self.bot.wait_for('message', check=epic_rpg_check_horse, timeout=5)
            elif answer in ('abort', 'cancel'):
                await ctx.send(strings.MSG_ABORTING)
                return
            else:
                await ctx.send(strings.MSG_WRONG_INPUT)
                return
        except asyncio.TimeoutError as error:
            await ctx.send(strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=user_name, information='horse'))
            return
        try:
            horse_stats = str(answer_bot_horse.embeds[0].fields[0])
            start_level = horse_stats.find('Horse Level** -') + 16
            end_level = start_level + 3
            horse_level = int(horse_stats[start_level:end_level].replace('\\','').replace('(','').strip())
        except:
            await ctx.send(strings.MSG_ERROR)
            return
        if 'Tier** - III' in horse_stats:
            horse_tier = 3
        elif 'Tier** - II' in horse_stats:
            horse_tier = 2
        elif 'Tier** - VIII' in horse_stats:
            horse_tier = 8
        elif 'Tier** - VII' in horse_stats:
            horse_tier = 7
        elif 'Tier** - VI' in horse_stats:
            horse_tier = 6
        elif 'Tier** - V' in horse_stats:
            horse_tier = 5
        elif 'Tier** - IV' in horse_stats:
            horse_tier = 4
        elif 'Tier** - IX' in horse_stats:
            horse_tier = 9
        elif 'Tier** - I' in horse_stats:
            horse_tier = 1
        elif 'Tier** - X' in horse_stats:
            horse_tier = 10
        else:
            await ctx.send(strings.MSG_ERROR)
            return

        try:
            await ctx.send(strings.MSG_WAIT_FOR_INPUT.format(user=user_name, command='rpg pr'))
            answer_user_pr = await self.bot.wait_for('message', check=check, timeout=30)
            answer = answer_user_pr.content.lower()
            if answer in ('rpg pr', 'rpg profession', 'rpg professions'):
                answer_bot_pr = await self.bot.wait_for('message', check=epic_rpg_check_professions, timeout=5)
            elif answer in ('abort', 'cancel'):
                await ctx.send(strings.MSG_ABORTING)
                return
            else:
                await ctx.send(strings.MSG_WRONG_INPUT)
                return
        except asyncio.TimeoutError as error:
            await ctx.send(strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=user_name, information='profession'))
            return
        try:
            professions = str(answer_bot_pr.embeds[0].fields[2])
            start_level = professions.find('Lootboxer Lv ') + 13
            end_level = professions.find(' |', start_level)
            lootboxer_level = int(professions[start_level:end_level])
        except:
            await ctx.send(strings.MSG_ERROR)
            return

        horse_emoji = getattr(emojis, f'HORSE_T{horse_tier}')
        if lootboxer_level > 100:
            horse_max_level = 10 * horse_tier + (lootboxer_level - 100)
        else:
            horse_max_level = 10 * horse_tier
        if horse_target_level == 0: horse_target_level = horse_max_level
        if horse_target_level > horse_max_level:
            horse_level_max_possible = MSG_HORSE_LEVEL_MAX_POSSIBLE.format(
                horse_emoji=horse_emoji, horse_tier=horse_tier, lootboxer_level=lootboxer_level,
                horse_max_level=horse_max_level
            )
            await ctx.send(
                f'{MSG_INVALID_HORSE_TARGET_LEVEL.format(user=user_name)} '
                f'{horse_level_max_possible}'
            )
            return
        if horse_target_level < horse_level:
            await ctx.send(MSG_HORSE_LEVEL_OVER_TARGET.format(user=user_name))
            return
        if horse_max_level == horse_level:
            await ctx.send(MSG_HORSE_LEVEL_ALREADY_MAX.format(user=user_name))
            return
        if horse_target_level == horse_level:
            await ctx.send(MSG_HORSE_LEVEL_ALREADY_TARGET.format(user=user_name))
            return
        level_cost_total = 0
        for level in range(horse_level, horse_target_level):
            level_cost = floor(
                (level ** 4) * ((level ** 2) + (210 * level) + 2200) * (500 - (lootboxer_level ** 1.2)) / 100000
            )
            level_cost_total = level_cost_total + level_cost
        await ctx.send(
            f'Leveling a {horse_emoji} **T{horse_tier} L{horse_level}** horse to **L{horse_target_level}** '
            f'with lootboxer level **{lootboxer_level}** costs **{level_cost_total:,}** coins. Phew.'
        )

    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def htcmanual(self, ctx: commands.Context, *args: str) -> None:
        """Calculate total horse training cost with manually specified values"""
        def check(m):
            return (m.author == ctx.author) and (m.channel == ctx.channel)

        prefix = ctx.prefix
        target_level = 0
        message_syntax = (
            strings.MSG_SYNTAX.format(
                syntax=f"{prefix}htcmanual [horse tier] [horse current level] [horse target level] [lootboxer level]"
            )
        )
        user_name = ctx.author.name
        if len(args) != 4:
            await ctx.send(message_syntax)
            return
        args = [arg.lower() for arg in args]
        horse_tier, current_level, target_level, lootboxer_level = args
        try:
            horse_tier = int(horse_tier.replace('t',''))
        except:
            await ctx.send(f'{MSG_INVALID_HORSE_TIER.format(user=user_name)}\n\n{message_syntax}')
            return
        try:
            current_level = int(current_level.replace('l',''))
        except:
            await ctx.send(f'{MSG_INVALID_HORSE_LEVEL.format(user=user_name)}\n\n{message_syntax}')
            return
        try:
            target_level = int(target_level.replace('l',''))
        except:
            await ctx.send(f'{MSG_INVALID_HORSE_TARGET_LEVEL.format(user=user_name)}\n\n{message_syntax}')
            return
        try:
            lootboxer_level = int(lootboxer_level.replace('l',''))
        except:
            await ctx.send(f'{MSG_INVALID_LOOTBOXER_LEVEL.format(user=user_name)}\n\n{message_syntax}')
            return
        if not 1 <= horse_tier <= 10:
            await ctx.send(f'{MSG_HORSE_TIER_RANGE.format(user=user_name)}\n\n{message_syntax}')
            return
        if not (2 <= target_level <= 140) or not (2 <= current_level <= 140):
            await ctx.send(f'{MSG_HORSE_LEVEL_RANGE_2.format(user=user_name)}\n\n{message_syntax}')
            return
        if not 1 <= lootboxer_level <= 150:
            await ctx.send(f'{MSG_LOOTBOXER_LEVEL_RANGE.format(user=user_name)}\n\n{message_syntax}')
            return

        horse_emoji = getattr(emojis, f'HORSE_T{horse_tier}')
        if lootboxer_level > 100:
            horse_max_level = 10 * horse_tier + (lootboxer_level - 100)
        else:
            horse_max_level = 10 * horse_tier
        if target_level == 0: target_level = horse_max_level
        if target_level > horse_max_level:
            horse_level_max_possible = MSG_HORSE_LEVEL_MAX_POSSIBLE.format(
                horse_emoji=horse_emoji, horse_tier=horse_tier, lootboxer_level=lootboxer_level,
                horse_max_level=horse_max_level
            )
            await ctx.send(
                f'{MSG_INVALID_HORSE_TARGET_LEVEL.format(user=user_name)} '
                f'{horse_level_max_possible}'
            )
            return
        if target_level < current_level:
            await ctx.send(MSG_HORSE_LEVEL_OVER_TARGET.format(user=user_name))
            return
        if horse_max_level == current_level:
            await ctx.send(MSG_HORSE_LEVEL_ALREADY_MAX.format(user=user_name))
            return
        if target_level == current_level:
            await ctx.send(MSG_HORSE_LEVEL_ALREADY_TARGET.format(user=user_name))
            return
        level_cost_total = 0
        for level in range(current_level, target_level):
            level_cost = floor(
                (level ** 4) * ((level ** 2) + (210 * level) + 2200) * (500 - (lootboxer_level ** 1.2)) / 100000
            )
            level_cost_total = level_cost_total + level_cost

        await ctx.send(
            f'Leveling a {horse_emoji} **T{horse_tier} L{current_level}** horse to **L{target_level}** with '
            f'lootboxer level **{lootboxer_level}** costs **{level_cost_total:,}** coins. Phew.'
        )

# Initialization
def setup(bot):
    bot.add_cog(HorseOldCog(bot))


# --- Embeds ---
async def embed_horses_overview(prefix: str) -> discord.Embed:
    """Horse overview embed"""
    horse_tier = (
        f'{emojis.BP} Tiers range from I to X (1 to 10) (see `{prefix}horse tier`)\n'
        f'{emojis.BP} Every tier unlocks new bonuses\n'
        f'{emojis.BP} Mainly increased by breeding with other horses (see `{prefix}horse breed`)\n'
        f'{emojis.BP} Small chance of increasing in horse races (see `{prefix}event race`)'
    )
    horse_level = (
        f'{emojis.BP} Levels range from 1 to ([tier] * 10) + [lootboxer bonus]\n'
        f'{emojis.BP} Example: A T7 horse with lootboxer at 102 has a max level of 72\n'
        f'{emojis.BP} Leveling up increases the horse type bonus (see the [Wiki]'
        f'(https://epic-rpg.fandom.com/wiki/Horse#Horse_Types_and_Boosts))\n'
        f'{emojis.BP} Increased by using `horse training` which costs coins\n'
        f'{emojis.BP} Training cost is reduced by leveling up lootboxer (see `{prefix}pr`)'
    )
    horse_type = (
        f'{emojis.BP} There are 8 different types (see `{prefix}horse type`)\n'
        f'{emojis.BP} The exact bonus the type gives is dependent on the level\n'
        f'{emojis.BP} Randomly changes when breeding unless you have a {emojis.HORSE_TOKEN} horse token in your '
        f'inventory'
    )
    calculators = (
        f'{emojis.BP} {CALC_TYPE.format(prefix=prefix)}\n'
        f'{emojis.BP} {CALC_HTC.format(prefix=prefix)}\n'
        f'{emojis.BP} {CALC_HTCTOTAL.format(prefix=prefix)}'
    )
    guides = (
        f'{emojis.BP} {GUIDE_BREED.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_TIER.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_TYPE.format(prefix=prefix)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSES',
        description = 'Horses have tiers, levels and types which all give certain important bonuses.'
    )
    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='TIER', value=horse_tier, inline=False)
    embed.add_field(name='LEVEL', value=horse_level, inline=False)
    embed.add_field(name='TYPE', value=horse_type, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    return embed


async def embed_horses_tiers(prefix: str) -> discord.Embed:
    """Horse tiers embed"""

    buff_lootbox = '{increase}% buff to lootbox drop chance'
    buff_monsters = '{increase}% buff to monster drops drop chance'
    buff_coins = '{increase}% more coins when using `daily` and `weekly`'
    buff_pets = '{increase}% higher chance to find pets with `training` ({total}%)'

    tier1 = f'{emojis.BP} No bonuses'
    tier2 = f'{emojis.BP} {buff_coins.format(increase=5)}'
    tier3 = f'{emojis.BP} {buff_coins.format(increase=10)}'
    tier4 = (
        f'{emojis.BP} Unlocks immortality in `hunt` and `adventure`\n'
        f'{emojis.BP} {buff_coins.format(increase=20)}'
    )
    tier5 = (
        f'{emojis.BP} Unlocks horse racing\n'
        f'{emojis.BP} {buff_lootbox.format(increase=20)}\n'
        f'{emojis.BP} {buff_coins.format(increase=30)}'
    )
    tier6 = (
        f'{emojis.BP} Unlocks free access to dungeons without dungeon keys\n'
        f'{emojis.BP} {buff_lootbox.format(increase=50)}\n'
        f'{emojis.BP} {buff_coins.format(increase=45)}'
    )
    tier7 = (
        f'{emojis.BP} {buff_monsters.format(increase=20)}\n'
        f'{emojis.BP} {buff_lootbox.format(increase=100)}\n'
        f'{emojis.BP} {buff_coins.format(increase=60)}'
    )
    tier8 = (
        f'{emojis.BP} Unlocks higher chance to get better enchants (% unknown)\n'
        f'{emojis.BP} {buff_monsters.format(increase=50)}\n'
        f'{emojis.BP} {buff_lootbox.format(increase=200)}\n'
        f'{emojis.BP} {buff_coins.format(increase=80)}'
    )
    tier9 = (
        f'{emojis.BP} {buff_pets.format(increase=150, total=10)}\n'
        f'{emojis.BP} {buff_monsters.format(increase=100)}\n'
        f'{emojis.BP} {buff_lootbox.format(increase=400)}\n'
        f'{emojis.BP} {buff_coins.format(increase=100)}\n'
    )
    tier10 = (
        #f'{emojis.BP} **You need to be {emojis.TIME_TRAVEL} TT50+ to unlock this tier**\n'
        f'{emojis.BP} Unlocks 2 extra badge slots\n'
        f'{emojis.BP} Adds a chance for another drop after each drop (mob drops and lootboxes)\n'
        f'{emojis.BLANK} The chance is believed to be around 20-35%, depending on the item\n'
        f'{emojis.BLANK} The better the item, the lower the chance\n'
        f'{emojis.BP} {buff_pets.format(increase=400, total=20)}\n'
        f'{emojis.BP} {buff_monsters.format(increase=200)}\n'
        f'{emojis.BP} {buff_lootbox.format(increase=650)}\n'
        f'{emojis.BP} {buff_coins.format(increase=200)}\n'
    )
    guides = (
        f'{emojis.BP} {GUIDE_OVERVIEW.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_BREED.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_TYPE.format(prefix=prefix)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSE TIERS',
        description = (
            f'Every horse tier unlocks additional bonuses.\n'
            f'Note: Every tier only lists the unlocks for this tier. You don\'t lose any previous unlocks when '
            f'tiering up.'
        )
    )
    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name=f'TIER I {emojis.HORSE_T1}', value=tier1, inline=False)
    embed.add_field(name=f'TIER II {emojis.HORSE_T2}', value=tier2, inline=False)
    embed.add_field(name=f'TIER III {emojis.HORSE_T3}', value=tier3, inline=False)
    embed.add_field(name=f'TIER IV {emojis.HORSE_T4}', value=tier4, inline=False)
    embed.add_field(name=f'TIER V {emojis.HORSE_T5}', value=tier5, inline=False)
    embed.add_field(name=f'TIER VI {emojis.HORSE_T6}', value=tier6, inline=False)
    embed.add_field(name=f'TIER VII {emojis.HORSE_T7}', value=tier7, inline=False)
    embed.add_field(name=f'TIER VIII {emojis.HORSE_T8}', value=tier8, inline=False)
    embed.add_field(name=f'TIER IX {emojis.HORSE_T9}', value=tier9, inline=False)
    embed.add_field(name=f'TIER X {emojis.HORSE_T10}', value=tier10, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    return embed


async def embed_horses_types(prefix: str) -> discord.Embed:
    """Horse types embed"""
    defender = (
        f'{emojis.BP} Increases overall DEF\n'
        f'{emojis.BP} The higher the horse level, the higher the DEF bonus\n'
        f'{emojis.BP} This type is better than MAGIC if you use EDGY or lower enchants\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    strong = (
        f'{emojis.BP} Increases overall AT\n'
        f'{emojis.BP} The higher the horse level, the higher the AT bonus\n'
        f'{emojis.BP} This type is better than MAGIC if you use EDGY or lower enchants\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    tank = (
        f'{emojis.BP} Increases overall LIFE\n'
        f'{emojis.BP} The higher the horse level, the higher the LIFE bonus\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    golden = (
        f'{emojis.BP} Increases the amount of coins from `hunt` and `adventure`\n'
        f'{emojis.BP} The higher the horse level, the higher the coin bonus\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    special = (
        f'{emojis.BP} Unlocks the epic quest which gives more coins and XP than the regular quest\n'
        f'{emojis.BP} You can do up to 15 waves in the epic quest\n'
        f'{emojis.BP} The higher the horse level, the more coins and XP the epic quest gives\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    super_special = (
        f'{emojis.BP} Unlocks the epic quest which gives more coins and XP than the regular quest\n'
        f'{emojis.BP} You can do up to 100 waves in the epic quest\n'
        f'{emojis.BP} The higher the horse level, the more coins and XP the epic quest gives\n'
        f'{emojis.BP} The coin and XP bonus is 50% higher than SPECIAL\n'
        f'{emojis.BP} **You only have a chance getting this type when breeding two SPECIAL horses**\n'
        f'{emojis.BP} As with every type change, you need to breed **without** a horse token\n'
    )
    magic = (
        f'{emojis.BP} Increases the effectiveness of enchantments\n'
        f'{emojis.BP} The higher the horse level, the higher the increase\n'
        f'{emojis.BP} This type is better than DEFENDER / STRONG if you use ULTRA-EDGY or higher enchants\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    festive = (
        f'{emojis.BP} Increases the chance to trigger a random event when using commands\n'
        f'{emojis.BP} The higher the horse level, the higher the increase\n'
        #f'{emojis.BP} ?% chance to get this type when breeding'
    )
    spooky = (
        f'{emojis.BP} Increases the chance to find pumpkins and spawn bat slimes\n'
        f'{emojis.BP} The higher the horse level, the higher the pumpkin chance\n'
        f'{emojis.BP} The bat slime spawn chance increase is always 5%\n'
        f'{emojis.BP} To get this type, craft and use a {emojis.HAL_CANDY_FISH} candy fish'
    )
    besttype = (
        f'{emojis.BP} SPECIAL or SUPER SPECIAL if you are in {emojis.TIME_TRAVEL} TT 0-1\n'
        f'{emojis.BP} DEFENDER if you are {emojis.TIME_TRAVEL} TT 2+, not ascended\n'
        f'{emojis.BP} MAGIC if you are {emojis.TIME_TRAVEL} TT 2+, ascended\n'
    )
    calculators = (
        f'{emojis.BP} {CALC_TYPE.format(prefix=prefix)}\n'
    )
    guides = (
        f'{emojis.BP} {GUIDE_OVERVIEW.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_BREED.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_TIER.format(prefix=prefix)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSE TYPES',
        description = (
            f'Each horse type has its unique bonuses.\n'
            f'The best type for you depends on your current TT and your horse tier and level.'
        )
    )
    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='DEFENDER', value=defender, inline=False)
    embed.add_field(name='FESTIVE', value=festive, inline=False)
    embed.add_field(name='GOLDEN', value=golden, inline=False)
    embed.add_field(name='MAGIC', value=magic, inline=False)
    embed.add_field(name='SPECIAL', value=special, inline=False)
    #embed.add_field(name=f'SPOOKY {emojis.HAL_PUMPKIN}', value=spooky, inline=False)
    embed.add_field(name='STRONG', value=strong, inline=False)
    embed.add_field(name='SUPER SPECIAL', value=super_special, inline=False)
    embed.add_field(name='TANK', value=tank, inline=False)
    embed.add_field(name='WHICH TYPE TO CHOOSE', value=besttype, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    return embed


async def embed_horses_breeding(prefix: str) -> discord.Embed:
    """Horse breeding embed"""
    howto = (
        f'{emojis.BP} Use `horse breeding [@player]`\n'
        f'{emojis.BP} You can only breed with a horse of the **same** tier\n'
        f'{emojis.BP} Ideally breed with a horse of the same level'
    )
    whereto = f'{emojis.BP} You can find players in the [official EPIC RPG server](https://discord.gg/w5dej5m)'
    horse_tier = (
        f'{emojis.BP} You have a chance to get +1 tier\n'
        f'{emojis.BP} The chance to tier up gets lower the higher your tier is\n'
        f'{emojis.BP} If one horse tiers up, the other one isn\'t guaranteed to do so too'
    )
    fail_count = (
        f'{emojis.BP} Everytime you don\'t tier up, you increase your fail count by 1\n'
        f'{emojis.BP} After a certain amount of fails, you will unlock an increased tier up chance\n'
        f'{emojis.BP} If you still don\'t tier up, you will unlock a guaranteed tier up at some point\n'
        f'{emojis.BP} The exact fail count needed depends on the horse tier\n'
        f'{emojis.BP} A {emojis.GODLY_HORSE_TOKEN} GODLY horse token increases the fail count by 50\n'
        f'{emojis.BP} This token can be earned in certain seasonal events\n'
    )
    chances = (
        f'{emojis.BP} T1 ➜ T2: 100% chance\n'
        f'{emojis.BP} T2 ➜ T3: 60% chance (guaranteed after 2 attempts)\n'
        f'{emojis.BP} T3 ➜ T4: 30% chance (guaranteed after 4 attempts)\n'
        f'{emojis.BP} T4 ➜ T5: 15% chance (guaranteed after 8 attempts)\n'
        f'{emojis.BP} T5 ➜ T6: 5% chance (guaranteed after 24 attempts)\n'
        f'{emojis.BP} T6 ➜ T7: 2% chance (guaranteed after 60 attempts)\n'
        f'{emojis.BP} T7 ➜ T8: 1% chance (guaranteed after 120 attempts)\n'
        f'{emojis.BP} T8 ➜ T9: chance unknown (guaranteed after 360 attempts)\n'
        f'{emojis.BP} T9 ➜ T10: chance & attempts unknown\n'
    )
    horse_level = (
        f'{emojis.BP} The new horses will have an average of both horse\'s levels\n'
        f'{emojis.BP} Example: L20 horse + L24 horse = L22 horses\n'
        f'{emojis.BP} Example: L20 horse + L23 horse = L21 **or** L22 horses'
    )
    horse_type = (
        f'{emojis.BP} Breeding changes your horse type randomly\n'
        f'{emojis.BP} You can keep your type by buying a {emojis.HORSE_TOKEN} horse token\n'
        f'{emojis.BP} Note: Each breeding consumes 1 {emojis.HORSE_TOKEN} horse token'
    )
    calculators = (
        f'{emojis.BP} {CALC_TYPE.format(prefix=prefix)}\n'
        f'{emojis.BP} {CALC_HTC.format(prefix=prefix)}\n'
        f'{emojis.BP} {CALC_HTCTOTAL.format(prefix=prefix)}'
    )
    guides = (
        f'{emojis.BP} {GUIDE_OVERVIEW.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_TIER.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_TYPE.format(prefix=prefix)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSE BREEDING',
        description = 'You need to breed to increase your horse tier and/or get a different type.'
    )
    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='HOW TO BREED', value=howto, inline=False)
    embed.add_field(name='WHERE TO BREED', value=whereto, inline=False)
    embed.add_field(name='IMPACT ON TIER', value=horse_tier, inline=False)
    embed.add_field(name='IMPACT ON LEVEL', value=horse_level, inline=False)
    embed.add_field(name='IMPACT ON TYPE', value=horse_type, inline=False)
    embed.add_field(name='TIER UP FAIL COUNT', value=fail_count, inline=False)
    embed.add_field(name='CHANCE TO TIER UP', value=chances, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    return embed