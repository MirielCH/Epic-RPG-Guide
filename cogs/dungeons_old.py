# dungeons.py

import asyncio
from humanfriendly import format_timespan
from typing import Tuple

import discord
from discord.ext import commands

import database
from resources import emojis
from resources import settings
from resources import functions


# dungeon commands (cog)
class DungeonsOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Dungeons menu
    @commands.command(aliases=('dungeons',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def dungeonguide(self, ctx):
        embed = await embed_dungeons_menu(ctx)
        await ctx.send(embed=embed)

    # Dungeon guide, can be invoked with "dX", "d X", "dungeonX" and "dungeon X"
    dungeon_aliases = ['dungeon','dung','dung15-1','d15-1','dungeon15-1','dung15-2','d15-2','dungeon15-2','dung152',
                       'd152','dungeon152','dung151','d151','dungeon151','dtop','dfinal','dungtop','dungfinal',
                       'dungeontop','dungeonfinal','finalfight']
    for x in range(1,21):
        dungeon_aliases.append(f'd{x}')
        dungeon_aliases.append(f'dungeon{x}')
        dungeon_aliases.append(f'dung{x}')

    @commands.command(name='d',aliases=(dungeon_aliases))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True, attach_files=True)
    async def dungeon(self, ctx, *args):

        invoked = ctx.message.content
        invoked = invoked.lower()
        prefix = ctx.prefix
        prefix = prefix.lower()

        if args:
            if len(args)>2:
                if len(args)==3:
                    arg1 = args[0]
                    arg2 = args[1]
                    arg3 = args[2]
                    if arg1.isnumeric() and arg2.isnumeric() and arg3.isnumeric():
                        await ctx.send(f'Uhm, you may have confused this command with the command `{ctx.prefix}dc`.')
                        return
                else:
                    return
            elif len(args) == 2:
                arg = args[0]
                arg = arg.lower()
                if arg == 'gear':
                    page = args[1]
                    if page.isnumeric():
                        page = int(page)
                        if page in (1,2):
                            await self.dungeongear(ctx, page)
                            return
                    else:
                        await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d20`')
                else:
                    await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d20`')
            elif len(args) == 1:
                arg = args[0]
                arg = arg.lower().replace('-','').replace('top','21').replace('final','21')
                if arg.isnumeric():
                    dungeon_no = int(arg)
                    if dungeon_no == 151: dungeon_no = 15
                    if dungeon_no == 152: dungeon_no = 15.2
                    if 1 <= dungeon_no <= 21 or dungeon_no == 15.2:
                        dungeon_data = await database.get_dungeon(dungeon_no)
                        dungeon_embed = await embed_dungeon(ctx, dungeon_data)
                        if dungeon_embed[0] == '':
                            await ctx.send(embed=dungeon_embed[1])
                        else:
                            await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
                    else:
                        await ctx.send(f'There is no dungeon {arg}, lol.')
                else:
                    if arg == 'gear':
                        await self.dungeongear(ctx, '1')
                        return
                    elif arg == 'stats':
                        await self.dungeonstats(ctx)
                        return
                    else:
                        await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d20`')
        else:
            dungeon_no = (invoked.replace(f'{prefix}dungeons','').replace(f'{prefix}dungeon','')
                          .replace(f'{prefix}dung','').replace(f'{prefix}d','').replace('-','')
                          .replace('top','21').replace(f'{prefix}finalfight','21').replace(f'{prefix}final','21'))
            if dungeon_no.isnumeric():
                dungeon_no = int(dungeon_no)
                if dungeon_no == 151: dungeon_no = 15
                if dungeon_no == 152: dungeon_no = 15.2
                if 1 <= dungeon_no <= 21 or dungeon_no == 15.2:
                    dungeon_data = await database.get_dungeon(dungeon_no)
                    dungeon_embed = await embed_dungeon(ctx, dungeon_data)
                    if dungeon_embed[0] == '':
                        await ctx.send(embed=dungeon_embed[1])
                    else:
                        await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
                else:
                    await ctx.send(f'There is no dungeon {dungeon_no}, lol.')
            else:
                if dungeon_no == '':
                    await self.dungeonguide(ctx)
                    return
                else:
                    await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d20`')

    # Command "dungeonstats" - Returns recommended stats for all dungeons
    @commands.command(aliases=('dstats','ds',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeonstats(self, ctx):
        dungeons = await database.get_all_dungeons()
        embed = await embed_dungeon_rec_stats(ctx, dungeons)
        await ctx.send(embed=embed)

    # Command "dungeongear" - Returns recommended gear for all dungeons
    @commands.command(aliases=('dgear','dg','dg1','dg2','dg3'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeongear(self, ctx, *args):

        invoked = ctx.message.content
        invoked = invoked.lower()
        syntax = (
            f'The command syntax is `{ctx.prefix}{ctx.invoked_with}`, `{ctx.prefix}{ctx.invoked_with} [1-3]` '
            f'or `{ctx.prefix}dg1`-`{ctx.prefix}dg3`'
        )

        if args:
            if len(args)>1:
                await ctx.send(syntax)
                return
            elif len(args)==1:
                page = args[0]
                if page.isnumeric():
                    page = int(page)
                    if page in (1,2,3):
                        dungeons = await database.get_all_dungeons()
                        embed = await embed_dungeon_rec_gear(ctx, dungeons,page)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(syntax)
                        return
                else:
                    await ctx.send(syntax)
                    return
        else:
            page = (invoked.replace(f'{ctx.prefix}dungeongear','').replace(f'{ctx.prefix}dgear','')
                    .replace(f'{ctx.prefix}dg',''))
            if page.isnumeric():
                page = int(page)
                dungeons = await database.get_all_dungeons()
                embed = await embed_dungeon_rec_gear(ctx, dungeons, page)
                await ctx.send(embed=embed)
            else:
                if page == '':
                    dungeons = await database.get_all_dungeons()
                    embed = await embed_dungeon_rec_gear(ctx, dungeons, 1)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(syntax)
                    return

    # Command "dungeoncheck" - Checks user stats against recommended stats
    @commands.command(aliases=('dcheck','dungcheck','dc','check',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeoncheck(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s profile') > 1) or (embed_author.find(f'{ctx_author}\'s stats') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        try:
            dungeon_no = 0
            if len(args) == 0:
                explanation = (
                    f'This command shows you for which dungeons your stats are high enough.\n'
                    f'You have the following options:\n'
                    f'{emojis.BP} `{ctx.prefix}{ctx.invoked_with} auto` to let me read your stats.\n{emojis.BLANK} This works with default profiles (no background) and `rpg stats`.\n'
                    f'{emojis.BP} `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually'
                )
                await ctx.send(explanation)
            elif len(args) == 1:
                try:
                    arg = args[0]
                    arg = arg.lower()
                    if arg == 'auto':
                        await ctx.send(
                            f'**{ctx.author.name}**, please type:\n'
                            f'{emojis.BP} `rpg stats` if you are an EPIC RPG donor\n'
                            f'{emojis.BLANK} or\n'
                            f'{emojis.BP} `rpg p` if you are not\n'
                            f'{emojis.BLANK} or\n'
                            f'{emojis.BP} `abort` to abort\n\n'
                            f'Note: `rpg p` does **not** work with profile backgrounds.\n'
                            f'If you have a background and are not a donor, please use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.'
                        )
                        answer_user_profile = await self.bot.wait_for('message', check=check, timeout = 30)
                        answer = answer_user_profile.content
                        answer = answer.lower()
                        if (answer == 'rpg p') or (answer == 'rpg profile') or (answer == 'rpg stats'):
                            answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                            try:
                                profile = str(answer_bot_at.embeds[0].fields[1])
                            except:
                                try:
                                    profile = str(answer_bot_at.embeds[0].fields[0])
                                except:
                                    await ctx.send(
                                        f'Whelp, something went wrong here, sorry.\n'
                                        f'If you have a profile background, use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually.'
                                    )
                                    return
                            start_at = profile.find('**AT**') + 8
                            end_at = profile.find('<:', start_at) - 2
                            user_at = profile[start_at:end_at]
                            user_at = user_at.replace(',','')
                            start_def = profile.find('**DEF**') + 9
                            end_def = profile.find(':', start_def) - 2
                            user_def = profile[start_def:end_def]
                            user_def = user_def.replace(',','')
                            start_current_life = profile.find('**LIFE**') + 10
                            start_life = profile.find('/', start_current_life) + 1
                            end_life = profile.find('\',', start_life)
                            user_life = profile[start_life:end_life]
                            user_life = user_life.replace(',','')
                        elif (answer == 'abort') or (answer == 'cancel'):
                            await ctx.send('Aborting.')
                            return
                        else:
                            await ctx.send('Wrong input. Aborting.')
                            return
                        if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                            user_at = int(user_at)
                            user_def = int(user_def)
                            user_life = int(user_life)
                        else:
                            await ctx.send('Whelp, something went wrong here, sorry. Aborting.')
                            return
                        user_stats = [user_at, user_def, user_life]
                        if dungeon_no == 0:
                            dungeon_check_data = await database.get_dungeon_check_data(ctx)
                            embed = await embed_dungeon_check_stats(dungeon_check_data, user_stats, ctx)
                        else:
                            dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                            embed = await embed_dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(
                            f'The command syntax is:\n'
                            f'• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\n'
                            f'or\n'
                            f'•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.'
                        )
                        return
                except asyncio.TimeoutError as error:
                    await ctx.send(
                        f'**{ctx.author.name}**, couldn\'t find your profile, RIP.\n'
                        f'If you have a profile background: Use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.'
                    )
            elif len(args) == 3:
                user_at = args[0]
                user_def = args[1]
                user_life = args[2]
                if (user_at.find('-') != -1) or (user_def.find('-') != -1) or (user_life.find('-') != -1):
                    await ctx.send('Did you play backwards? Send a post card from area -5.')
                    return
                else:
                    if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                        user_at = int(args[0])
                        user_def = int(args[1])
                        user_life = int(args[2])
                        if (user_at == 0) or (user_def == 0) or (user_life == 0) or (user_at > 10000) or (user_def > 10000) or (user_life > 10000):
                            await ctx.send('NICE STATS. Not gonna buy it though.')
                            return
                        else:
                            dungeon_check_data = await database.get_dungeon_check_data(ctx)
                            user_stats = [user_at, user_def, user_life]
                            embed = await embed_dungeon_check_stats(dungeon_check_data, user_stats, ctx)
                            await ctx.send(embed=embed)
                    else:
                        await ctx.send('These stats look suspicious. Try actual numbers.')
            else:
                await ctx.send(
                    f'The command syntax is:\n'
                    f'• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\n'
                    f'or\n'
                    f'•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.'
                )
        except:
            raise

    # Command "dungeoncheckX" - Checks user stats against recommended stats of a specific dungeon
    dungeon_check_aliases = ['dcheck1','check1','dungcheck1','dc1','dcheck15-1','check15-1','dungcheck15-1','dc15-1','dcheck151','check151','dungcheck151','dc151','dcheck15-2','check15-2','dungcheck15-2','dc15-2','dcheck152','check152','dungcheck152','dc152',]
    for x in range(2,21):
        dungeon_check_aliases.append(f'dcheck{x}')
        dungeon_check_aliases.append(f'check{x}')
        dungeon_check_aliases.append(f'dungeoncheck{x}')
        dungeon_check_aliases.append(f'dungcheck{x}')
        dungeon_check_aliases.append(f'dc{x}')

    @commands.command(aliases=dungeon_check_aliases)
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeoncheck1(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s profile') > 1) or (embed_author.find(f'{ctx_author}\'s stats') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        try:
            invoked = ctx.invoked_with
            invoked = invoked.lower()

            dungeon_no = invoked.replace('dungeoncheck','').replace('dungcheck','').replace('dcheck','').replace('check','').replace('dc','').replace('-','')
            dungeon_no = int(dungeon_no)

            if dungeon_no in (10,15,151,152):
                user_stats = (0,0,0)
                if dungeon_no == 151:
                    dungeon_no = 15
                elif dungeon_no == 152:
                    dungeon_no = 15.2
                dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                embed = await embed_dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                await ctx.send(embed=embed)
            else:
                if len(args) == 0:
                    explanation = (
                        f'This command shows you if your stats are high enough for dungeon **{dungeon_no}**.\n'
                        f'You have the following options:\n'
                        f'{emojis.BP} `{ctx.prefix}{ctx.invoked_with} auto` to let me read your stats.\n'
                        f'{emojis.BLANK} This works with default profiles (no background) and `rpg stats`.\n'
                        f'{emojis.BP} `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually'
                    )
                    await ctx.send(explanation)
                elif len(args) == 1:
                    arg = args[0]
                    arg = arg.lower()
                    if arg == 'auto':
                        try:
                            await ctx.send(
                                f'**{ctx.author.name}**, please type:\n'
                                f'{emojis.BP} `rpg stats` if you are an EPIC RPG donor\n'
                                f'{emojis.BLANK} or\n'
                                f'{emojis.BP} `rpg p` if you are not\n'
                                f'{emojis.BLANK} or\n'
                                f'{emojis.BP} `abort` to abort\n\n'
                                f'Note: `rpg p` does **not** work with profile backgrounds.\n'
                                f'If you have a background and are not a donor, please use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.'
                            )
                            answer_user_at = await self.bot.wait_for('message', check=check, timeout = 30)
                            answer = answer_user_at.content
                            answer = answer.lower()
                            if (answer == 'rpg p') or (answer == 'rpg profile') or (answer == 'rpg stats'):
                                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                                try:
                                    profile = str(answer_bot_at.embeds[0].fields[1])
                                except:
                                    try:
                                        profile = str(answer_bot_at.embeds[0].fields[0])
                                    except:
                                        await ctx.send(
                                            f'Whelp, something went wrong here, sorry.\n'
                                            f'If you have a profile background, use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually.'
                                        )
                                        return
                                start_at = profile.find('**AT**') + 8
                                end_at = profile.find('<:', start_at) - 2
                                user_at = profile[start_at:end_at]
                                start_def = profile.find('**DEF**') + 9
                                end_def = profile.find(':', start_def) - 2
                                user_def = profile[start_def:end_def]
                                start_current_life = profile.find('**LIFE**') + 10
                                start_life = profile.find('/', start_current_life) + 1
                                end_life = profile.find('\',', start_life)
                                user_life = profile[start_life:end_life]
                            elif (answer == 'abort') or (answer == 'cancel'):
                                await ctx.send('Aborting.')
                                return
                            else:
                                await ctx.send('Wrong input. Aborting.')
                                return
                            if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                                user_at = int(user_at)
                                user_def = int(user_def)
                                user_life = int(user_life)
                            else:
                                await ctx.send('Whelp, something went wrong here, sorry. Aborting.')
                                return
                            dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                            user_stats = [user_at, user_def, user_life]
                            embed = await embed_dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                            await ctx.send(embed=embed)
                        except asyncio.TimeoutError as error:
                            await ctx.send(
                                f'**{ctx.author.name}**, couldn\'t find your profile, RIP.\n'
                                f'If you have a profile background: Use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.'
                            )
                    else:
                        await ctx.send(
                            f'The command syntax is:\n'
                            f'• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\n'
                            f'or\n'
                            f'•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.'
                        )
                        return
                elif len(args) == 3:
                    user_at = args[0]
                    user_def = args[1]
                    user_life = args[2]
                    if (user_at.find('-') != -1) or (user_def.find('-') != -1) or (user_life.find('-') != -1):
                        await ctx.send('Did you play backwards? Send a post card from area -5.')
                        return
                    else:
                        if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                            user_at = int(args[0])
                            user_def = int(args[1])
                            user_life = int(args[2])
                            if (user_at == 0) or (user_def == 0) or (user_life == 0) or (user_at > 10000) or (user_def > 10000) or (user_life > 10000):
                                await ctx.send('NICE STATS. Not gonna buy it though.')
                                return
                            else:
                                dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                                user_stats = [user_at, user_def, user_life]
                                embed = await embed_dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                                await ctx.send(embed=embed)
                        else:
                            await ctx.send('These stats look suspicious. Try actual numbers.')
                else:
                    await ctx.send(
                        f'The command syntax is:\n'
                        f'• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\n'
                        f'or\n'
                        f'•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.'
                    )
        except:
            raise

# Initialization
def setup(bot):
    bot.add_cog(DungeonsOldCog(bot))



# --- Redundancies ---
# Guides
guide_dungeon = '`{prefix}d1`-`{prefix}d20` : Guide for dungeon 1~20'
guide_check = '`{prefix}dc{dungeon_no}` : Check if you\'re ready for this dungeon'
guide_check_all = '`{prefix}dc1`-`{prefix}dc15` : Dungeon 1~15 stats check'
guide_gear = '`{prefix}dg` : Recommended gear (all dungeons)'
guide_stats = '`{prefix}ds` : Recommended stats (all dungeons)'



# --- Functions ---
# Create field "Check dungeon stats" for areas and dungeons
async def function_design_field_check_stats(field_check_stats_data, user_data, prefix, short_version):

    user_at = user_data[0]
    user_def = user_data[1]
    user_life = user_data[2]

    player_at = field_check_stats_data[0]
    player_def = field_check_stats_data[1]
    player_carry_def = field_check_stats_data[2]
    player_life = field_check_stats_data[3]
    dungeon_no = field_check_stats_data[4]

    if not dungeon_no == 15.2:
        dungeon_no = int(dungeon_no)

    check_at = 'N/A'
    check_def = 'N/A'
    check_carry_def = 'N/A'
    check_life = 'N/A'

    user_at_check_result = 'N/A'
    user_def_check_result = 'N/A'
    user_carry_def_check_result = 'N/A'
    user_life_check_result = 'N/A'

    check_results = ''

    if dungeon_no <= 9:
        if not player_at == 0:
            if user_at < player_at:
                if user_def >= player_carry_def:
                    user_at_check_result = 'ignore'
                else:
                    user_at_check_result = 'fail'
            elif user_at >= player_at:
                user_at_check_result = 'pass'
        else:
            check_at = f'{emojis.CHECK_IGNORE} **AT**: -'

        if not player_def == 0:
            if user_def < player_def:
                user_def_check_result = 'fail'
            elif user_def >= player_def:
                user_def_check_result = 'pass'
        else:
            check_def = f'{emojis.CHECK_IGNORE} **DEF**: -'

        if not player_carry_def == 0:
            if user_def < player_carry_def:
                user_carry_def_check_result = 'fail'
            elif user_def >= player_carry_def:
                user_carry_def_check_result = 'pass'
        else:
            check_carry_def = f'{emojis.CHECK_IGNORE} **Carry DEF**: -'

        if not player_life == 0:
            if user_life < player_life:
                if user_def >= player_carry_def:
                        user_life_check_result = 'ignore'
                elif player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                else:
                    user_life_check_result = 'fail'
            elif user_life >= player_life:
                user_life_check_result = 'pass'
        else:
            check_life = f'{emojis.CHECK_IGNORE} **LIFE**: -'

    elif dungeon_no == 11:
        if user_at < player_at:
            user_at_check_result = 'fail'
        elif user_at >= player_at:
            user_at_check_result = 'pass'
        if user_life < player_life:
            if user_at_check_result == 'pass':
                if player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                elif (player_life - user_life) <= 200:
                    user_life_check_result = 'warn'
                else:
                    user_life_check_result = 'fail'
            else:
                if player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                else:
                    user_life_check_result = 'fail'
        elif user_life >= player_life:
            user_life_check_result = 'pass'

    elif dungeon_no == 12:
        if user_def < player_def:
            user_def_check_result = 'fail'
        elif user_def >= player_def:
            user_def_check_result = 'pass'
        if user_life < player_life:
            if player_life - user_life <= 10:
                user_life_check_result = 'passA'
            elif 11 <= (player_life - user_life) <= 25:
                user_life_check_result = 'passB'
            elif 26 <= (player_life - user_life) <= 50:
                user_life_check_result = 'passC'
            else:
                user_life_check_result = 'fail'
        elif user_life >= player_life:
            user_life_check_result = 'pass'

    elif dungeon_no == 13:
        if user_life < player_life:
            user_life_check_result = 'fail'
        else:
            user_life_check_result = 'pass'

    elif dungeon_no == 14:
        if user_def < player_def:
            user_def_check_result = 'fail'
        elif user_def >= player_def:
            user_def_check_result = 'pass'
        if user_life < player_life:
            if player_life - user_life <= 10:
                user_life_check_result = 'passA'
            elif 11 <= (player_life - user_life) <= 25:
                user_life_check_result = 'passB'
            elif 26 <= (player_life - user_life) <= 50:
                user_life_check_result = 'passC'
            else:
                user_life_check_result = 'fail'
        elif user_life >= player_life:
            user_life_check_result = 'pass'

    if user_at_check_result == 'pass':
        check_at = f'{emojis.CHECK_OK} **AT**: {player_at}'
    elif user_at_check_result == 'warn':
        check_at = f'{emojis.CHECK_WARN} **AT**: {player_at}'
    elif user_at_check_result == 'fail':
        check_at = f'{emojis.CHECK_FAIL} **AT**: {player_at}'
    elif user_at_check_result == 'ignore':
        check_at = f'{emojis.CHECK_IGNORE} **AT**: {player_at}'

    if user_def_check_result == 'pass':
        check_def = f'{emojis.CHECK_OK} **DEF**: {player_def}'
    elif user_def_check_result == 'warn':
        check_def = f'{emojis.CHECK_WARN} **DEF**: {player_def}'
    elif user_def_check_result == 'fail':
        check_def = f'{emojis.CHECK_FAIL} **DEF**: {player_def}'
    elif user_def_check_result == 'ignore':
        check_def = f'{emojis.CHECK_IGNORE} **DEF**: {player_def}'

    if user_carry_def_check_result == 'pass':
        check_carry_def = f'{emojis.CHECK_OK} **Carry DEF**: {player_carry_def}'
    elif user_carry_def_check_result == 'warn':
        check_carry_def = f'{emojis.CHECK_WARN} **Carry DEF**: {player_carry_def}'
    elif user_carry_def_check_result == 'fail':
        check_carry_def = f'{emojis.CHECK_FAIL} **Carry DEF**: {player_carry_def}'
    elif user_carry_def_check_result == 'ignore':
        check_carry_def = f'{emojis.CHECK_IGNORE} **Carry DEF**: {player_carry_def}'

    if user_life_check_result == 'pass':
        check_life = f'{emojis.CHECK_OK} **LIFE**: {player_life}'
    elif user_life_check_result == 'passA':
        check_life = f'{emojis.CHECK_OK} **LIFE**: {player_life} • {emojis.LIFE_BOOST}**A**'
    elif user_life_check_result == 'passB':
        check_life = f'{emojis.CHECK_OK} **LIFE**: {player_life} • {emojis.LIFE_BOOST}**B**'
    elif user_life_check_result == 'passC':
        check_life = f'{emojis.CHECK_OK} **LIFE**: {player_life} • {emojis.LIFE_BOOST}**C**'
    elif user_life_check_result == 'warn':
        check_life = f'{emojis.CHECK_WARN} **LIFE**: {player_life}'
    elif user_life_check_result == 'fail':
        check_life = f'{emojis.CHECK_FAIL} **LIFE**: {player_life}'
    elif user_life_check_result == 'ignore':
        check_life = f'{emojis.CHECK_IGNORE} **LIFE**: {player_life}'

    if short_version == True:
        bulletpoint = ''
    else:
        bulletpoint = f'{emojis.BP}'

    field_value = ''
    if not check_at == 'N/A':
        field_value =   f'{bulletpoint} {check_at}'
    if not check_def == 'N/A':
        field_value =   f'{field_value}\n{bulletpoint} {check_def}'
    if not check_carry_def == 'N/A':
        field_value =   f'{field_value}\n{bulletpoint} {check_carry_def}'
    if not check_life == 'N/A':
        field_value =   f'{field_value}\n{bulletpoint} {check_life}'
    field_value = field_value.strip()
    if field_value == '':
        if dungeon_no <= 15.2:
            field_value = f'{bulletpoint} Stats irrelevant'
        else:
            field_value = f'{bulletpoint} Stats unknown'
    if short_version == True:
        field_value =   f'{field_value}\n{emojis.BLANK}'

    if short_version == False:
        user_stats_check_results = [['AT',user_at_check_result], ['DEF', user_def_check_result], ['LIFE', user_life_check_result]]
        player_stats_check = [player_at, player_def, player_life]

        if dungeon_no in (10,15,15.2):
            check_results = f'{emojis.BP} Stats are irrelevant for this dungeon'
            if dungeon_no == 10:
                check_results = f'{check_results}\n{emojis.BP} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
            elif dungeon_no in (15,15.2):
                dungeon_no = str(dungeon_no).replace('.','-')
                check_results = f'{check_results}\n{emojis.BP} This dungeon has various requirements (see `{prefix}d{dungeon_no}`)'
        elif dungeon_no == 11:
            if user_at_check_result == 'fail':
                check_results = (
                    f'{emojis.BP} You are not yet ready for this dungeon\n'
                    f'{emojis.BP} You should increase your **AT** to **{player_at}**'
                )
                if user_life_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.BP} You should increase your **LIFE** to **{player_life}** or more'
            else:
                if user_life_check_result == 'warn':
                    check_results = (
                        f'{emojis.BP} Your **LIFE** is below recommendation (**{player_life}**)\n'
                        f'{emojis.BP} You can still attempt the dungeon though, maybe you get lucky!'
                    )
                elif user_life_check_result == 'fail':
                    check_results = (
                        f'{emojis.BP} You are not yet ready for this dungeon\n'
                        f'{emojis.BP} You should increase your **LIFE** to **{player_life}** or more'
                    )
                else:
                    check_results = (
                        f'{emojis.BP} Your stats are high enough for this dungeon\n'
                        f'{emojis.BP} Note that this dungeon is luck based, so you can still die'
                    )
                    if (user_life_check_result == 'passA'):
                        check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost A to reach recommended **LIFE**'
                    if (user_life_check_result == 'passB'):
                        check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost B to reach recommended **LIFE**'
                    if (user_life_check_result == 'passC'):
                        check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost C to reach recommended **LIFE**'
            check_results = f'{check_results}\n{emojis.BP} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
        elif dungeon_no == 12:
            if (user_def_check_result == 'fail') or (check_life == 'fail'):
                check_results = f'{emojis.BP} You are not yet ready for this dungeon'
                if user_def_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.BP} You should increase your **DEF** to **{player_def}**'
                if user_life_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.BP} You should increase your **LIFE** to **{player_life}** or more'
            else:
                check_results = f'{emojis.BP} You are ready for this dungeon'
                if (user_life_check_result == 'passA'):
                    check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost A to reach recommended **LIFE**'
                if (user_life_check_result == 'passB'):
                    check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost B to reach recommended **LIFE**'
                if (user_life_check_result == 'passC'):
                    check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost C to reach recommended **LIFE**'
                check_results = f'{check_results}\n{emojis.BP} Note that higher **LIFE** will still help in beating the dungeon'
            check_results = f'{check_results}\n{emojis.BP} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
        elif dungeon_no == 13:
            if user_life_check_result == 'fail':
                check_results = (
                    f'{emojis.BP} You are not yet ready for this dungeon\n'
                    f'{emojis.BP} You should increase your **LIFE** to **{player_life}** or more\n'
                    f'{emojis.BP} The **LIFE** is for crafting the {emojis.SWORD_OMEGA} OMEGA Sword, not the dungeon\n'
                    f'{emojis.BP} **Important**: This is **base LIFE**, before buying a {emojis.LIFE_BOOST} LIFE boost'
                )
            else:
                check_results = f'{emojis.BP} Your stats are high enough for this dungeon'
            check_results = f'{check_results}\n{emojis.BP} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'

        elif dungeon_no == 14:
            if (user_def_check_result == 'fail') or user_life_check_result == 'fail':
                check_results = f'{emojis.BP} You are not yet ready for this dungeon'

                if user_def_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.BP} You should increase your **DEF** to **{player_def}**'
                if user_life_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.BP} You should increase your **LIFE** to **{player_life}** or more'
            else:
                check_results = f'{emojis.BP} Your stats are high enough for this dungeon'
                if (user_life_check_result == 'passA'):
                    check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost A to reach recommended **LIFE**'
                if (user_life_check_result == 'passB'):
                    check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost B to reach recommended **LIFE**'
                if (user_life_check_result == 'passC'):
                    check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost C to reach recommended **LIFE**'
            check_results = f'{check_results}\n{emojis.BP} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
        elif 16 <= dungeon_no <= 20:
            check_results = f'{emojis.BP} Stats for this dungeon are currently unknown'
        else:
            if user_carry_def_check_result == 'pass':
                check_results = f'{emojis.BP} You are ready **and** can carry other players'
                for check in user_stats_check_results:
                    if (check[1] == 'ignore') or (check[1] == 'warn'):
                        check_results = f'{check_results}\n{emojis.BP} Your **{check[0]}** is low but can be ignored because of your DEF'
            elif (user_at_check_result == 'fail') or (user_def_check_result == 'fail') or (user_life_check_result == 'fail'):
                check_results = f'{emojis.BP} You are not yet ready for this dungeon'
                for x, check in enumerate(user_stats_check_results):
                    if check[1] == 'fail':
                        check_results = f'{check_results}\n{emojis.BP} You should increase your **{check[0]}** to **{player_stats_check[x]}**'
                check_results = f'{check_results}\n{emojis.BP} However, you can still do this dungeon if you get carried'
            elif (user_at_check_result == 'pass') and (user_def_check_result == 'pass') and ((user_life_check_result == 'pass') or (user_life_check_result == 'passA') or (user_life_check_result == 'passB') or (user_life_check_result == 'passC')):
                check_results = f'{emojis.BP} Your stats are high enough for this dungeon'
                if (user_life_check_result == 'passA'):
                    check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost A to reach recommended **LIFE**'
                if (user_life_check_result == 'passB'):
                    check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost B to reach recommended **LIFE**'
                if (user_life_check_result == 'passC'):
                    check_results = f'{check_results}\n{emojis.BP} Note: You need a {emojis.LIFE_BOOST} LIFE boost C to reach recommended **LIFE**'

    else:
        check_results = 'N/A'

    return (field_value, check_results)



# --- Embeds ---
# Dungeons menu
async def embed_dungeons_menu(ctx):

    prefix = ctx.prefix

    dungeon_guide = (
        f'{emojis.BP} `{prefix}dungeon [#]` / `{prefix}d1`-`{prefix}d20` : Guide for dungeon 1~20\n'
        f'{emojis.BP} `{prefix}dgear` / `{prefix}dg` : Recommended gear (all dungeons)\n'
        f'{emojis.BP} `{prefix}dstats` / `{prefix}ds` : Recommended stats (all dungeons)'
    )

    statscheck = (
        f'{emojis.BP} `{prefix}dc1`-`{prefix}dc15` : Dungeon 1~15 stats check\n'
        f'{emojis.BP} `{prefix}dcheck` / `{prefix}dc` : Dungeon stats check (all dungeons)'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'DUNGEON GUIDES',
        description = f'Hey **{ctx.author.name}**, what do you want to know?'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='DUNGEONS', value=dungeon_guide, inline=False)
    embed.add_field(name='STATS CHECK', value=statscheck, inline=False)

    return embed


async def embed_dungeon(ctx: commands.Context, dungeon: database.Dungeon) -> Tuple[discord.File, discord.Embed]:
    """Creates dungeon guide embed"""
    prefix = ctx.prefix
    img_dungeon = image_url = image_name = None
    boss_life = time_limit = player_amount = key_price = description = requirements = strategy = tips = rewards = None
    notes = None

    if dungeon.boss_life is not None:
        boss_life = int(dungeon.boss_life) if dungeon.boss_life.is_integer() else dungeon.boss_life
    dungeon_no = dungeon.dungeon_no

    field_rec_stats = await functions.design_field_rec_stats(dungeon)
    field_rec_gear = await functions.design_field_rec_gear(dungeon)
    if field_rec_gear is None: field_rec_gear = f'{emojis.BP} None'

    # Time limit
    if dungeon.time_limit is not None:
        time_limit = format_timespan(dungeon.time_limit)
        if 1 <= dungeon_no <= 9:
            time_limit = f'{time_limit} per player'

    # Amount of players and boss stats
    player_amount = f'{emojis.BP} {dungeon.player_amount[0]}'
    if dungeon.player_amount[0] != dungeon.player_amount[1]:
        player_amount = f'{player_amount}-{dungeon.player_amount[1]}'
    if dungeon.player_amount in ((1,1),(2,2)):
        boss_life = '-' if boss_life is None else f'{boss_life:,}'
    else:
        boss_life = '-' if boss_life is None else f'{boss_life:,} per player'
    boss_at = '-' if dungeon.boss_at is None else f'~{dungeon.boss_at:,}'
    if 16 <= dungeon_no <= 21: boss_at = 'Unknown'
    if dungeon_no == 21: boss_life = 'Unknown'
    if dungeon_no == 14: boss_life = f'2x {boss_life}'

    # Key price
    if dungeon.key_price is not None:
        key_price = f'{dungeon.key_price:,} coins'
    else:
        if dungeon_no != 21:
            key_price = f'You can only enter this dungeon with a {emojis.HORSE_T6} T6+ horse'

    # Description
    description = dungeon.description
    if dungeon_no == 15:
        description = (
            f'{description}\n'
            f'To see part 2 of this dungeon, use `{prefix}d15-2`'
        )
    elif dungeon_no == 15.2:
        description = (
            f'{description}\n'
            f'To see part 1 of this dungeon, use `{prefix}d15-1`'
        )

    # Requirements
    if 1 <= dungeon_no <= 9:
        requirements = f'{emojis.BP} {emojis.DUNGEON_KEY_1} Dungeon key **OR** {emojis.HORSE_T6} T6+ horse'
    elif 10 <= dungeon_no <= 15.2:
        requirements = f'{emojis.BP} {emojis.DUNGEON_KEY_10} Dungeon key **OR** {emojis.HORSE_T6} T6+ horse'
    elif dungeon_no == 21:
        requirements = f'{emojis.BP} {emojis.HORSE_T9} T9+ horse (T10 **highly** recommended)'

    else:
        requirements = f'{emojis.BP} {emojis.HORSE_T6} T6+ horse'
    if dungeon_no in (10, 11, 13, 15, 15.2):
        requirements = f'{requirements}\n{emojis.BP} {dungeon.player_sword.emoji} {dungeon.player_sword.name}'
    if dungeon_no == 21:
        requirements = (
            f'{requirements}\n'
            f'{emojis.BP} {emojis.SWORD_GODLYCOOKIE} GODLY cookie (`eat` it to start the fight)'
        )
    if dungeon_no in (10, 12, 14, 15):
        requirements = f'{requirements}\n{emojis.BP} {dungeon.player_armor.emoji} {dungeon.player_armor.name}'
    if dungeon_no in (15, 15.2):
        requirements = (
            f'{requirements}\n'
            f'{emojis.BP} {emojis.PET_CAT} T5+ cat pet\n'
            f'{emojis.BP} {emojis.PET_DOG} T5+ dog pet\n'
            f'{emojis.BP} {emojis.PET_DRAGON} T5+ dragon pet'
        )
    if dungeon.tt is not None:
        if dungeon.tt != 0: requirements = f'{requirements}\n{emojis.BP} {emojis.TIME_TRAVEL} TT {dungeon.tt}+'
    if dungeon_no == 15.2:
        requirements = f'{requirements}\n{emojis.BP} {emojis.STAT_COOLNESS} 2,000+ coolness'

    # Strategy
    if 1 <= dungeon_no <= 9:
        strategy = f'{emojis.BP} Use `stab` or `power`'
    elif dungeon_no == 10:
         strategy = (
            f'{emojis.BP} The player that starts the dungeon gets the attacker role\n'
            f'{emojis.BP} The other player gets the defender role\n'
            f'{emojis.BP} Attacker command sequence:\n'
            f'{emojis.BLANK} `charge edgy sword` x20\n'
            f'{emojis.BLANK} `attack`\n'
            f'{emojis.BP} Defender command sequence:\n'
            f'{emojis.BLANK} `weakness spell`\n'
            f'{emojis.BLANK} `protect` x3\n'
            f'{emojis.BLANK} `charge edgy armor` x2\n'
            f'{emojis.BLANK} `protect`\n'
            f'{emojis.BLANK} `invulnerability`\n'
            f'{emojis.BLANK} `healing spell`\n'
            f'{emojis.BLANK} `protect` x7\n'
            f'{emojis.BP} Note: The defender will die before the boss does'
        )
    elif dungeon_no == 13:
        strategy = (
            f'{emojis.BP} You start in room 1, 2 or 3\n'
            f'{emojis.BP} Your goal is to reach the dragon\'s room\n'
            f'{emojis.BP} In each room you will be asked one question\n'
            f'{emojis.BP} Your answer determines your next room\n'
            f'{emojis.BP} Refer to the image below for a walkthrough\n'
            f'{emojis.BP} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Dungeon_13)'
        )
    elif dungeon_no == 14:
        strategy = f'{emojis.BP} https://epic-rpg.fandom.com/wiki/Dungeon_14'
    elif dungeon_no == 15:
        strategy = f'{emojis.BP} https://epic-rpg.fandom.com/wiki/Dungeon_15.1'
    elif dungeon_no == 15.2:
        strategy = f'{emojis.BP} https://epic-rpg.fandom.com/wiki/Dungeon_15.2'
    elif 16 <= dungeon_no <= 19:
        strategy = f'{emojis.BP} Use `power`'
    elif dungeon_no == 20:
        strategy = (
            f'{emojis.BP} Use `power` if you can survive the damage\n'
            f'{emojis.BP} Use `sacrifice` if you are about to die'
        )

    # Tips
    if dungeon_no == 11:
        tips = (
            f'{emojis.BP} You can move left, right, up, down or pass\n'
            f'{emojis.BP} Your goal is to reach and hit the boss until it dies\n'
            f'{emojis.BP} Each point of AT you have does 1 damage to the boss\n'
            f'{emojis.BP} You can only attack if you stand right next to the boss\n'
            f'{emojis.BP} After you hit the boss, your position will reset\n'
            f'{emojis.BP} If you end up on a fireball, you take 100 damage\n'
            f'{emojis.BP} If you pass a turn, you take 10 damage\n'
            f'{emojis.BP} The board scrolls down one line with every move you make\n'
            f'{emojis.BP} You do **not** move down with the board\n'
            f'{emojis.BP} **The board moves first** when you make a move\n'
            f'{emojis.BP} Check the image below to see the movement behaviour\n'
            f'{emojis.BP} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Dungeon_11)'
        )
    elif dungeon_no == 12:
        tips = f'{emojis.BP} https://epic-rpg.fandom.com/wiki/Dungeon_12'

    # Rewards
    if 1 <= dungeon_no <= 14:
        rewards = f'{emojis.BP} Unlocks area {dungeon_no + 1:g} (see `{prefix}a{dungeon_no + 1:g}`)'
    elif dungeon_no == 15:
        rewards = f'{emojis.BP} {emojis.TIME_KEY} TIME key to unlock super time travel (see `{prefix}stt`)'
    elif dungeon_no == 15.2:
        rewards = (
            f'{emojis.BP} Unlocks the TOP (see `{prefix}top`)\n'
            f'{emojis.BP} {emojis.TIME_DRAGON_ESSENCE} TIME dragon essence\n'
            f'{emojis.BLANK} Used to craft the {emojis.SWORD_GODLYCOOKIE} GODLY cookie (see `{prefix}dtop`)\n'
            f'{emojis.BLANK} Used in the `shop` to buy {emojis.EPIC_JUMP} EPIC jump (see `{prefix}a16`)\n'
        )
    elif 16 <= dungeon_no <= 20:
        if 16 <= dungeon_no <= 19:
            rewards = (
                f'{emojis.BP} {emojis.EPIC_JUMP} EPIC jump to move to area {dungeon_no + 1:g} (if unsealed)'
            )
        else:
            rewards = (
                f'{emojis.BP} {emojis.EPIC_JUMP} EPIC jump'
            )
        rewards = (
            f'{rewards}\n'
            f'{emojis.BLANK} Note: You can not have more than 1 in your inventory.\n'
            f'{emojis.BP} Unlocks the ability to get 1 additional {emojis.TIME_TRAVEL} TT every {21 - dungeon_no:g} TTs.\n'
            f'{emojis.BLANK} This reward is permanent.\n'
            f'{emojis.BP} Chance to get a {emojis.PET_VOIDOG} VOIDog pet\n'
        )
    elif dungeon_no == 21:
        rewards = (
            f'{emojis.BP} {emojis.EPIC_JUMP} EPIC jump to move to area 16 (if unsealed)\n'
            f'{emojis.BP} Unlocks the ability to buy {emojis.EPIC_JUMP} EPIC jumps in the `shop`.\n'
            f'{emojis.BLANK} This reward is permanent.'
        )

    # Notes
    if dungeon_no == 15.2:
        notes = (
            f'{emojis.BP} To enter this dungeon, you need to equip the {emojis.SWORD_GODLY} GODLY sword and start D15.\n'
            f'{emojis.BLANK} Once you beat part 1, part 2 will automatically start.\n'
        )
    elif 16 <= dungeon_no <= 20:
        notes = (
            f'{emojis.BP} Carrying is not possible in this dungeon\n'
            f'{emojis.BP} You can redo this dungeon as long as you are in area {dungeon_no:g}\n'
        )
    elif dungeon_no == 21:
        notes = (
            f'{emojis.BP} This fight does not need your dungeon cooldown\n'
        )

    # Images
    if dungeon_no == 11:
        img_dungeon = discord.File(settings.IMG_DUNGEON_11, filename='dungeon11.png')
        image_url = 'attachment://dungeon11.png'
        image_name = 'MOVEMENT BEHAVIOUR'
    elif dungeon_no == 13:
        img_dungeon = discord.File(settings.IMG_DUNGEON_13, filename='dungeon13.png')
        image_url = 'attachment://dungeon13.png'
        image_name = 'WALKTHROUGH'

    dungeon_no = 15.1 if dungeon.dungeon_no == 15 else dungeon.dungeon_no
    title = f'DUNGEON {f"{dungeon_no:g}".replace(".","-")}' if dungeon_no != 21 else 'EPIC NPC FIGHT'

    guides = (
        f'{emojis.BP} {guide_gear.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}'
    )
    if dungeon_no != 21:
        dungeon_no_check = f'{dungeon_no:g}' if dungeon_no != 15.2 else '15-2'
        guides = f'{emojis.BP} {guide_check.format(prefix=prefix,dungeon_no=dungeon_no_check)}\n{guides}'

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = title,
        description = description
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='BOSS', value=f'{emojis.BP} {dungeon.boss_emoji} {dungeon.boss_name}', inline=False)
    if player_amount is not None:
        embed.add_field(name='PLAYERS', value=player_amount, inline=False)
    if time_limit is not None:
        embed.add_field(name='TIME LIMIT', value=f'{emojis.BP} {time_limit}', inline=False)
    if rewards is not None:
        embed.add_field(name='REWARDS', value=rewards, inline=False)
    if requirements is not None:
        embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    if key_price is not None:
        embed.add_field(name='DUNGEON KEY PRICE', value=f'{emojis.BP} {key_price}', inline=False)
    embed.add_field(
        name='BOSS STATS',
        value=(
            f'{emojis.BP} {emojis.STAT_AT} **AT**: {boss_at}\n'
            f'{emojis.BP} {emojis.STAT_LIFE} **LIFE**: {boss_life}'
        ),
            inline=False
    )
    embed.add_field(name='RECOMMENDED GEAR', value=field_rec_gear, inline=True)
    embed.add_field(name='RECOMMENDED STATS', value=field_rec_stats, inline=True)
    if strategy is not None: embed.add_field(name='STRATEGY', value=strategy, inline=False)
    if tips is not None: embed.add_field(name='TIPS', value=tips, inline=False)
    if notes is not None: embed.add_field(name='NOTE', value=notes, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    if image_url is not None:
        embed.set_image(url=image_url)
        embed.add_field(name=image_name, value=f'** **', inline=False)

    return (img_dungeon, embed)


async def embed_dungeon_rec_stats(ctx: commands.Context, dungeons: Tuple[database.Dungeon]) -> discord.Embed:
    # Embed with recommended stats for all dungeons
    prefix = ctx.prefix
    guides = (
        f'{emojis.BP} {guide_check_all.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_gear.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'RECOMMENDED STATS FOR ALL DUNGEONS',
        description = f'\u200b'
    )

    embed.set_footer(text=await functions.default_footer(prefix))

    for dungeon in dungeons:
        dungeon_no = 15.1 if dungeon.dungeon_no == 15 else dungeon.dungeon_no
        field_name = f'DUNGEON {f"{dungeon_no:g}".replace(".","-")}' if dungeon_no != 21 else 'THE "FINAL" FIGHT'
        field_rec_stats = await functions.design_field_rec_stats(dungeon, True)
        embed.add_field(name=field_name, value=field_rec_stats, inline=True)

    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed


async def embed_dungeon_rec_gear(ctx: commands.Context, dungeons: Tuple[database.Dungeon], page: int) -> discord.Embed:
    """Embed with recommended gear for all dungeons"""
    prefix = ctx.prefix
    page_1 = f'➜ See `{prefix}dg1` for dungeons 1 to 9.'
    page_2 = f'➜ See `{prefix}dg2` for dungeons 10 to 15.'
    page_3 = f'➜ See `{prefix}dg3` for dungeons 16 to 20 and the EPIC NPC fight.'

    if page == 1:
        title_value = 'RECOMMENDED GEAR FOR DUNGEONS 1 TO 9'
        description_value = f'{page_2}\n{page_3}'
        listed_dungeons = dungeons[:9]
    elif page == 2:
        title_value = 'RECOMMENDED GEAR FOR DUNGEONS 10 TO 15'
        description_value = f'{page_1}\n{page_3}'
        listed_dungeons = dungeons[9:16]
    elif page == 3:
        title_value = 'RECOMMENDED GEAR FOR DUNGEONS 16 TO 20'
        description_value = f'{page_1}\n{page_2}'
        listed_dungeons = dungeons[16:]

    guides = (
        f'{emojis.BP} {guide_dungeon.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_check_all.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = title_value,
        description = description_value
    )

    embed.set_footer(text=await functions.default_footer(prefix))


    for dungeon in listed_dungeons:
        dungeon_no = 15.1 if dungeon.dungeon_no == 15 else dungeon.dungeon_no
        field_name = f'DUNGEON {f"{dungeon_no:g}".replace(".","-")}' if dungeon_no != 21 else 'THE "FINAL" FIGHT'
        field_rec_gear = await functions.design_field_rec_gear(dungeon)
        if field_rec_gear is None: field_rec_gear = f'{emojis.BP} None'
        embed.add_field(name=field_name, value=field_rec_gear, inline=False)

    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Stats check (all dungeons)
async def embed_dungeon_check_stats(dungeon_check_data, user_stats, ctx):

    prefix = ctx.prefix

    legend = (
        f'{emojis.BP} {emojis.CHECK_OK} : Stat is above recommendation\n'
        f'{emojis.BP} {emojis.CHECK_FAIL} : Stat is below recommendation\n'
        f'{emojis.BP} {emojis.CHECK_IGNORE} : Stat is below rec. but you are above carry DEF\n'
        f'{emojis.BP} {emojis.CHECK_WARN} : Stat is below rec. but with a lot of luck it _might_ work\n'
        f'{emojis.BP} {emojis.LIFE_BOOST} : LIFE boost you have to buy to reach recommendation'
    )

    notes = (
        f'{emojis.BP} You can ignore this check for D1-D9 if you get carried\n'
        f'{emojis.BP} You can **not** get carried in D16-D20, the boss gets stronger if someone dies!\n'
        f'{emojis.BP} This only checks stats, you may still need certain gear for D10+!\n'
        f'{emojis.BP} Use `{ctx.prefix}dc1`-`{ctx.prefix}dc20` for individual checks with more details'
    )

    guides = (
        f'{emojis.BP} {guide_gear.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'DUNGEON STATS CHECK',
        description = f'**{ctx.author.name}**, here\'s your check for **{user_stats[0]} AT**, **{user_stats[1]} DEF** and **{user_stats[2]} LIFE.**'
    )

    embed.set_footer(text=await functions.default_footer(ctx.prefix))

    for dung_x in dungeon_check_data:
        dungeon_no = dung_x[4]

        field_check_stats = await function_design_field_check_stats(dung_x, user_stats, ctx.prefix, True)
        embed.add_field(name=f'DUNGEON {dungeon_no:g}', value=field_check_stats[0], inline=True)

    embed.add_field(name='LEGEND', value=legend, inline=False)
    embed.add_field(name='NOTE', value=notes, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Stats check (dungeon specific)
async def embed_dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx):

    prefix = ctx.prefix

    legend = (
        f'{emojis.BP} {emojis.CHECK_OK} : Stat is above recommendation\n'
        f'{emojis.BP} {emojis.CHECK_FAIL} : Stat is below recommendation\n'
        f'{emojis.BP} {emojis.CHECK_IGNORE} : Stat is below rec. but you are above carry DEF\n'
        f'{emojis.BP} {emojis.CHECK_WARN} : Stat is below rec. but with a lot of luck it _might_ work\n'
        f'{emojis.BP} {emojis.LIFE_BOOST} : LIFE boost you have to buy to reach recommendation'
    )

    notes = (
        f'{emojis.BP} You can ignore this check for D1-D9 if you get carried\n'
        f'{emojis.BP} You can **not** get carried in D16-D20, the boss gets stronger if someone dies!\n'
        f'{emojis.BP} This check does **not** take into account required gear for D10+!\n'
        f'{emojis.BP} Use `{ctx.prefix}dc1`-`{ctx.prefix}dc15` for a few more details'
    )

    guides = (
        f'{emojis.BP} {guide_check_all.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_gear.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}'
    )

    dungeon_no = dungeon_check_data[4]

    if dungeon_no == 15:
        dungeon_no = '15-1'
    elif dungeon_no == 15.2:
        dungeon_no = '15-2'

    if isinstance(dungeon_no, float):
        dungeon_no = f'{dungeon_no:g}'

    embed_title = f'DUNGEON {dungeon_no} STATS CHECK'

    field_check_stats = await function_design_field_check_stats(dungeon_check_data, user_stats, prefix, False)

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = embed_title,
        description = f'**{ctx.author.name}**, here\'s your check for **{user_stats[0]} AT**, **{user_stats[1]} DEF** and **{user_stats[2]} LIFE.**'
    )

    embed.set_footer(text=await functions.default_footer(ctx.prefix))
    embed.add_field(name='CHECK RESULT', value=field_check_stats[0], inline=False)
    embed.add_field(name='DETAILS', value=field_check_stats[1], inline=False)
    #embed.add_field(name=f'LEGEND', value=legend, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed