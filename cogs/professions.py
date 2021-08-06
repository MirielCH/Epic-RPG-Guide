# professions.py

import asyncio
from math import ceil

import discord
from discord.ext import commands

import database
import emojis
import global_data


# profession commands (cog)
class professionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pr_aliases = (
        'pr','professions','prof','profs',
        'ascension','asc','prasc','prascension','ascended','ascend','prascend','prascended',
        'prlevel','prlvl','professionslevel','professionslevels','professionlevels','professionsleveling','professionleveling','prlevels','prleveling','proflevel','proflevels','profslevel','profslevels',
        'worker','enchanter','crafter','lootboxer','merchant','prworker','prenchanter','prcrafter','prlootboxer','prmerchant'
    )

    # Command "professions"
    @commands.command(aliases=pr_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def profession(self, ctx, *args):

        invoked = ctx.invoked_with
        invoked = invoked.lower()

        if args:
            arg = args[0]

            if arg.find('level') > -1:
                embed = await embed_professions_leveling(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('asc') > -1:
                embed = await embed_ascension(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('work') > -1:
                embed = await embed_professions_worker(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('craft') > -1:
                embed = await embed_professions_crafter(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('enchant') > -1:
                embed = await embed_professions_enchanter(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('merchant') > -1:
                embed = await embed_professions_merchant(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('lootbox') > -1:
                embed = await embed_professions_lootboxer(ctx.prefix)
                await ctx.send(embed=embed)
            else:
                embed = await embed_professions_overview(ctx.prefix)
                await ctx.send(embed=embed)
        else:
            if (invoked.find('level') > -1) or (invoked.find('lvl') > -1):
                embed = await embed_professions_leveling(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('asc') > -1):
                embed = await embed_ascension(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('work') > -1):
                embed = await embed_professions_worker(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('craft') > -1):
                embed = await embed_professions_crafter(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('enchant') > -1):
                embed = await embed_professions_enchanter(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('merchant') > -1):
                embed = await embed_professions_merchant(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('lootbox') > -1):
                embed = await embed_professions_lootboxer(ctx.prefix)
                await ctx.send(embed=embed)
            else:
                embed = await embed_professions_overview(ctx.prefix)
                await ctx.send(embed=embed)

    # Command "prc" - Info about crafting
    @commands.command(aliases=('prctotal',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prc(self, ctx):

        await ctx.send(
            f'To level up crafter, repeatedly craft {emojis.logepic} EPIC logs in batches of 500.\n'
            f'See `{ctx.prefix}pr level` for more information.'
        )

    # Command "pre" - Calculate ice cream to craft
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, external_emojis=True)
    async def pre(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Enchanter') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if args:
            arg = args[0]
            if arg == 'total':
                if len(args) == 2:
                    arg2 = args[1]
                    await self.pretotal(ctx, arg2)
                    return
                else:
                    await self.pretotal(ctx)
                    return

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg pr enchanter` (or `abort` to abort)')
            answer_user_enchanter = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_user_enchanter.content
            answer = answer.lower()
            if answer in ('rpg pr enchanter','rpg profession enchanter', 'rpg professions enchanter'):
                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    pr_worker = str(answer_bot_at.embeds[0].fields[0])
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                start_level = pr_worker.find('**Level**') + 11
                end_level = pr_worker.find('(', start_level) - 1
                if end_level == -2:
                    end_level = pr_worker.find('\\n', start_level)
                pr_level = pr_worker[start_level:end_level]
                start_current_xp = pr_worker.find('**XP**') + 8
                end_current_xp = pr_worker.find('/', start_current_xp)
                pr_current_xp = pr_worker[start_current_xp:end_current_xp]
                pr_current_xp = pr_current_xp.replace(',','')
                start_needed_xp = pr_worker.find('/', start_current_xp) + 1
                end_needed_xp = pr_worker.find(f'\'', start_needed_xp)
                pr_needed_xp = pr_worker[start_needed_xp:end_needed_xp]
                pr_needed_xp = pr_needed_xp.replace(',','')
            elif (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send('Wrong input. Aborting.')
                return
            if pr_level.isnumeric():
                pr_level = int(pr_level)
                if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    ice_cream = ceil(xp / 100)
                    ice_cream_wb = ceil(xp / 110)
                    xp_rest = 100 - (xp % 100)
                    xp_rest_wb = 110 - (xp % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0

                    levelrange = []

                    if pr_level >= 99:
                        enchanter_levels = []
                    elif pr_level + 7 > 100:
                        levelrange = [pr_level+2, 100,]
                        enchanter_levels = await database.get_profession_levels(ctx,'enchanter',levelrange)
                    else:
                        levelrange = [pr_level+2, pr_level+7,]
                        enchanter_levels = await database.get_profession_levels(ctx,'enchanter',levelrange)

                    output = (
                        f'You need to cook the following amounts of {emojis.foodfruiticecream} fruit ice cream:\n'
                        f'{emojis.bp} Level {pr_level} to {pr_level+1}: **{ice_cream:,}** (if world buff: **{ice_cream_wb:,}**)'
                    )

                    for enchanter_level in enchanter_levels:
                        enchanter_level_no = enchanter_level[0]
                        enchanter_level_xp = enchanter_level[1]
                        actual_xp = enchanter_level_xp - xp_rest
                        actual_xp_wb = enchanter_level_xp - xp_rest_wb
                        ice_cream = ceil(actual_xp / 100)
                        ice_cream_wb = ceil(actual_xp_wb / 110)
                        xp_rest = 100 - (actual_xp % 100)
                        xp_rest_wb = 110 - (actual_xp_wb % 110)
                        if xp_rest == 100:
                            xp_rest = 0
                        if xp_rest_wb == 110:
                            xp_rest_wb = 0
                        output = f'{output}\n{emojis.bp} Level {enchanter_level_no-1} to {enchanter_level_no}: **{ice_cream:,}** (if world buff: **{ice_cream_wb:,}**)'

                    await ctx.send(f'{output}\n\nUse `{ctx.prefix}craft [amount] ice cream` to see what materials you need to craft fruit ice cream.')
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            else:
                await ctx.send('Whelp, something went wrong here, sorry.')
                return
        except asyncio.TimeoutError as error:
                    await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')

    # Command "prl" - Calculate lootboxes to craft
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def prl(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Lootboxer') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if args:
            arg = args[0]
            if arg == 'total':
                if len(args) == 2:
                    arg2 = args[1]
                    await self.prltotal(ctx, arg2)
                    return
                else:
                    await self.prltotal(ctx)
                    return

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg pr lootboxer` (or `abort` to abort)')
            answer_user_lootboxer = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_user_lootboxer.content
            answer = answer.lower()
            if answer in ('rpg pr lootboxer','rpg profession lootboxer', 'rpg professions lootboxer'):
                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    pr_lootboxer = str(answer_bot_at.embeds[0].fields[0])
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                start_level = pr_lootboxer.find('**Level**') + 11
                end_level = pr_lootboxer.find('(', start_level) - 1
                if end_level == -2:
                    end_level = pr_lootboxer.find('\\n', start_level)
                pr_level = pr_lootboxer[start_level:end_level]
                start_current_xp = pr_lootboxer.find('**XP**') + 8
                end_current_xp = pr_lootboxer.find('/', start_current_xp)
                pr_current_xp = pr_lootboxer[start_current_xp:end_current_xp]
                pr_current_xp = pr_current_xp.replace(',','')
                start_needed_xp = pr_lootboxer.find('/', start_current_xp) + 1
                end_needed_xp = pr_lootboxer.find(f'\'', start_needed_xp)
                pr_needed_xp = pr_lootboxer[start_needed_xp:end_needed_xp]
                pr_needed_xp = pr_needed_xp.replace(',','')
            elif (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send('Wrong input. Aborting.')
                return
            if pr_level.isnumeric():
                pr_level = int(pr_level)
                if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                    pr_level = int(pr_level)
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    lootboxes = ceil(xp / 100)
                    lootboxes_wb = ceil(xp / 110)
                    xp_rest = 100 - (xp % 100)
                    xp_rest_wb = 110 - (xp % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0

                    levelrange = []

                    if pr_level >= 99:
                        worker_levels = []
                    elif pr_level + 7 > 100:
                        levelrange = [pr_level+2, 100,]
                        worker_levels = await database.get_profession_levels(ctx,'lootboxer',levelrange)
                    else:
                        levelrange = [pr_level+2, pr_level+7,]
                        worker_levels = await database.get_profession_levels(ctx,'lootboxer',levelrange)

                    output = (
                        f'You need to cook the following amounts of {emojis.foodfilledlootbox} filled lootboxes:\n'\
                        f'{emojis.bp} Level {pr_level} to {pr_level+1}: **{lootboxes:,}** (if world buff: **{lootboxes_wb:,}**)'
                    )

                    for worker_level in worker_levels:
                        worker_level_no = worker_level[0]
                        worker_level_xp = worker_level[1]
                        actual_xp = worker_level_xp - xp_rest
                        actual_xp_wb = worker_level_xp - xp_rest_wb
                        lootboxes = ceil(actual_xp / 100)
                        lootboxes_wb = ceil(actual_xp_wb / 110)
                        xp_rest = 100 - (actual_xp % 100)
                        xp_rest_wb = 110 - (actual_xp_wb % 110)
                        if xp_rest == 100:
                            xp_rest = 0
                        if xp_rest_wb == 110:
                            xp_rest_wb = 0
                        output = f'{output}\n{emojis.bp} Level {worker_level_no-1} to {worker_level_no}: **{lootboxes:,}** (if world buff: **{lootboxes_wb:,}**)'

                    await ctx.send(f'{output}\n\nUse `{ctx.prefix}craft [amount] lootboxes` to see what materials you need to craft filled lootboxes.')
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            else:
                await ctx.send('Whelp, something went wrong here, sorry.')
                return
        except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')

    # Command "prm" - Calculate logs to sell
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prm(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s professions') > 1) and (str(m.embeds[0].fields[0]).find('Merchant') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if args:
            arg = args[0]
            if arg == 'total':
                if len(args) == 2:
                    arg2 = args[1]
                    await self.prmtotal(ctx, arg2)
                    return
                else:
                    await self.prmtotal(ctx)
                    return

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg pr merchant` (or `abort` to abort)')
            answer_user_merchant = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_user_merchant.content
            answer = answer.lower()
            if answer in ('rpg pr merchant','rpg profession merchant', 'rpg professions merchant'):
                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    pr_merchant = str(answer_bot_at.embeds[0].fields[0])
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                start_level = pr_merchant.find('**Level**') + 11
                end_level = pr_merchant.find('(', start_level) - 1
                if end_level == -2:
                        end_level = pr_merchant.find('\\n', start_level)
                pr_level = pr_merchant[start_level:end_level]
                start_current_xp = pr_merchant.find('**XP**') + 8
                end_current_xp = pr_merchant.find('/', start_current_xp)
                pr_current_xp = pr_merchant[start_current_xp:end_current_xp]
                pr_current_xp = pr_current_xp.replace(',','')
                start_needed_xp = pr_merchant.find('/', start_current_xp) + 1
                end_needed_xp = pr_merchant.find(f'\'', start_needed_xp)
                pr_needed_xp = pr_merchant[start_needed_xp:end_needed_xp]
                pr_needed_xp = pr_needed_xp.replace(',','')
            elif (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send('Wrong input. Aborting.')
                return
            if pr_level.isnumeric():
                pr_level = int(pr_level)
                if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                    pr_level = int(pr_level)
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    logs = xp * 5
                    logs_wb = 5 * ceil((logs/1.1) / 5)

                    levelrange = []

                    if pr_level >= 99:
                        merchant_levels = []
                    elif pr_level + 7 > 100:
                        levelrange = [pr_level+2, 100,]
                        merchant_levels = await database.get_profession_levels(ctx,'merchant',levelrange)
                    else:
                        levelrange = [pr_level+2, pr_level+7,]
                        merchant_levels = await database.get_profession_levels(ctx,'merchant',levelrange)

                    output = f'You need to sell the following amounts of {emojis.log} wooden logs:\n'\
                            f'{emojis.bp} Level {pr_level} to {pr_level+1}: **{logs:,}** (if world buff: **{logs_wb:,}**)'

                    for merchant_level in merchant_levels:
                        merchant_level_no = merchant_level[0]
                        merchant_level_xp = merchant_level[1]
                        logs = merchant_level_xp*5
                        logs_wb = 5 * ceil((logs/1.1) / 5)
                        output = f'{output}\n{emojis.bp} Level {merchant_level_no-1} to {merchant_level_no}: **{logs:,}** (if world buff: **{logs_wb:,}**)'

                    await ctx.send(output)
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            else:
                await ctx.send('Whelp, something went wrong here, sorry.')
                return
        except asyncio.TimeoutError as error:
            await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')

    # Command "prw" - Calculate pickaxes to craft
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, external_emojis=True)
    async def prw(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Worker') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if args:
            arg = args[0]
            if arg == 'total':
                if len(args) == 2:
                    arg2 = args[1]
                    await self.prwtotal(ctx, arg2)
                    return
                else:
                    await self.prwtotal(ctx)
                    return

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg pr worker` (or `abort` to abort)')
            answer_user_worker = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_user_worker.content
            answer = answer.lower()
            if answer in ('rpg pr worker','rpg profession worker', 'rpg professions worker'):
                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    pr_worker = str(answer_bot_at.embeds[0].fields[0])
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                start_level = pr_worker.find('**Level**') + 11
                end_level = pr_worker.find('(', start_level) - 1
                if end_level == -2:
                        end_level = pr_worker.find('\\n', start_level)
                pr_level = pr_worker[start_level:end_level]
                start_current_xp = pr_worker.find('**XP**') + 8
                end_current_xp = pr_worker.find('/', start_current_xp)
                pr_current_xp = pr_worker[start_current_xp:end_current_xp]
                pr_current_xp = pr_current_xp.replace(',','')
                start_needed_xp = pr_worker.find('/', start_current_xp) + 1
                end_needed_xp = pr_worker.find(f'\'', start_needed_xp)
                pr_needed_xp = pr_worker[start_needed_xp:end_needed_xp]
                pr_needed_xp = pr_needed_xp.replace(',','')
            elif (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send('Wrong input. Aborting.')
                return
            if pr_level.isnumeric():
                pr_level = int(pr_level)
                if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                    pr_level = int(pr_level)
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    pickaxes = ceil(xp / 100)
                    pickaxes_wb = ceil(xp / 110)
                    xp_rest = 100 - (xp % 100)
                    xp_rest_wb = 110 - (xp % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0

                    levelrange = []

                    if pr_level >= 99:
                        worker_levels = []
                    elif pr_level + 7 > 100:
                        levelrange = [pr_level+2, 100,]
                        worker_levels = await database.get_profession_levels(ctx,'worker',levelrange)
                    else:
                        levelrange = [pr_level+2, pr_level+7,]
                        worker_levels = await database.get_profession_levels(ctx,'worker',levelrange)

                    output = (
                        f'You need to cook the following amounts of {emojis.foodbananapickaxe} banana pickaxes:\n'
                        f'{emojis.bp} Level {pr_level} to {pr_level+1}: **{pickaxes:,}** (if world buff: **{pickaxes_wb:,}**)'
                    )

                    for worker_level in worker_levels:
                        worker_level_no = worker_level[0]
                        worker_level_xp = worker_level[1]
                        actual_xp = worker_level_xp - xp_rest
                        actual_xp_wb = worker_level_xp - xp_rest_wb
                        pickaxes = ceil(actual_xp / 100)
                        pickaxes_wb = ceil(actual_xp_wb / 110)
                        xp_rest = 100 - (actual_xp % 100)
                        xp_rest_wb = 110 - (actual_xp_wb % 110)
                        if xp_rest == 100:
                            xp_rest = 0
                        if xp_rest_wb == 110:
                            xp_rest_wb = 0

                        output = f'{output}\n{emojis.bp} Level {worker_level_no-1} to {worker_level_no}: **{pickaxes:,}** (if world buff: **{pickaxes_wb:,}**)'

                    await ctx.send(f'{output}\n\nUse `{ctx.prefix}craft [amount] pickaxe` to see what materials you need to craft banana pickaxes.')
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            else:
                await ctx.send('Whelp, something went wrong here, sorry.')
                return
        except asyncio.TimeoutError as error:
            await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')

    # Command "pretotal" - Calculate total ice cream to craft until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def pretotal(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Enchanter') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if len(args) == 0:
            try:
                await ctx.send(f'**{ctx.author.name}**, please type `rpg pr enchanter` (or `abort` to abort)')
                answer_user_enchanter = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_enchanter.content
                answer = answer.lower()
                if answer in ('rpg pr enchanter','rpg profession enchanter', 'rpg professions enchanter'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        pr_enchanter = str(answer_bot_at.embeds[0].fields[0])
                    except:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    start_level = pr_enchanter.find('**Level**') + 11
                    end_level = pr_enchanter.find('(', start_level) - 1
                    if end_level == -2:
                        end_level = pr_enchanter.find('\\n', start_level)
                    pr_level = pr_enchanter[start_level:end_level]
                    start_current_xp = pr_enchanter.find('**XP**') + 8
                    end_current_xp = pr_enchanter.find('/', start_current_xp)
                    pr_current_xp = pr_enchanter[start_current_xp:end_current_xp]
                    pr_current_xp = pr_current_xp.replace(',','')
                    start_needed_xp = pr_enchanter.find('/', start_current_xp) + 1
                    end_needed_xp = pr_enchanter.find(f'\'', start_needed_xp)
                    pr_needed_xp = pr_enchanter[start_needed_xp:end_needed_xp]
                    pr_needed_xp = pr_needed_xp.replace(',','')
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return
                if pr_level.isnumeric():
                    pr_level = int(pr_level)
                    if not pr_level >= 100:
                        if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                            pr_level = int(pr_level)
                            pr_current_xp = int(pr_current_xp)
                            pr_needed_xp = int(pr_needed_xp)
                            xp = pr_needed_xp - pr_current_xp
                            ice_cream = ceil(xp / 100)
                            ice_cream_wb = ceil(xp / 110)
                            xp_rest = 100 - (xp % 100)
                            xp_rest_wb = 110 - (xp % 110)
                            if xp_rest == 100:
                                xp_rest = 0
                            if xp_rest_wb == 110:
                                xp_rest_wb = 0
                            ice_cream_total = ice_cream
                            ice_cream_total_wb = ice_cream_wb

                            levelrange = []

                            if pr_level == 99:
                                enchanter_levels = []
                            else:
                                levelrange = [pr_level+2, 100,]
                                enchanter_levels = await database.get_profession_levels(ctx,'enchanter',levelrange)

                            for enchanter_level in enchanter_levels:
                                enchanter_level_xp = enchanter_level[1]
                                actual_xp = enchanter_level_xp - xp_rest
                                actual_xp_wb = enchanter_level_xp - xp_rest_wb
                                ice_cream = ceil(actual_xp / 100)
                                ice_cream_wb = ceil(actual_xp_wb / 110)
                                ice_cream_total = ice_cream_total + ice_cream
                                ice_cream_total_wb = ice_cream_total_wb + ice_cream_wb
                                xp_rest = 100 - (actual_xp % 100)
                                xp_rest_wb = 110 - (actual_xp_wb % 110)
                                if xp_rest == 100:
                                    xp_rest = 0
                                if xp_rest_wb == 110:
                                    xp_rest_wb = 0

                            await ctx.send(
                                f'You need to cook the following amount of {emojis.foodfruiticecream} fruit ice cream to reach level 100:\n'
                                f'{emojis.bp} **{ice_cream_total:,}** without world buff\n'
                                f'{emojis.bp} **{ice_cream_total_wb:,}** with world buff\n\n'
                                f'Use `{ctx.prefix}craft [amount] ice cream` to see how much you need for that.'
                            )
                        else:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                    else:
                        await ctx.send(
                                f'Sorry, this command can only calculate up to level 100.\n'
                                f'You can use `{ctx.prefix}pre` to calculate the ice cream needed to reach the next level though.'
                            )
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                return

        elif len(args) == 1:
            arg = args[0]

            if arg.replace('-','').isnumeric():
                try:
                    level = int(arg)
                except:
                    await ctx.send(
                        f'`{arg}` is not a valid target level. Please enter the level you want me to calculate to.\n'
                        f'Example: `{ctx.prefix}pretotal 80`. If you want me to calculate to level 100, you can omit the level.'
                    )
                    return

                if level < 2:
                    await ctx.send('You want to reach level what now?')
                    return
                elif level > 100:
                    await ctx.send(
                                f'Sorry, this command can only calculate up to level 100.\n'
                                f'You can use `{ctx.prefix}pre` to calculate the ice cream needed to reach the next level though.'
                            )
                    return

                try:
                    await ctx.send(f'**{ctx.author.name}**, please type `rpg pr enchanter` (or `abort` to abort)')
                    answer_user_enchanter = await self.bot.wait_for('message', check=check, timeout = 30)
                    answer = answer_user_enchanter.content
                    answer = answer.lower()
                    if answer in ('rpg pr enchanter','rpg profession enchanter', 'rpg professions enchanter'):
                        answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                        try:
                            pr_enchanter = str(answer_bot_at.embeds[0].fields[0])
                        except:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                        start_level = pr_enchanter.find('**Level**') + 11
                        end_level = pr_enchanter.find('(', start_level) - 1
                        if end_level == -2:
                            end_level = pr_enchanter.find('\\n', start_level)
                        pr_level = pr_enchanter[start_level:end_level]
                        start_current_xp = pr_enchanter.find('**XP**') + 8
                        end_current_xp = pr_enchanter.find('/', start_current_xp)
                        pr_current_xp = pr_enchanter[start_current_xp:end_current_xp]
                        pr_current_xp = pr_current_xp.replace(',','')
                        start_needed_xp = pr_enchanter.find('/', start_current_xp) + 1
                        end_needed_xp = pr_enchanter.find(f'\'', start_needed_xp)
                        pr_needed_xp = pr_enchanter[start_needed_xp:end_needed_xp]
                        pr_needed_xp = pr_needed_xp.replace(',','')
                    elif (answer_user_enchanter.content == 'abort') or (answer_user_enchanter.content == 'cancel'):
                        await ctx.send(f'Aborting.')
                        return
                    else:
                        await ctx.send(f'Wrong input. Aborting.')
                        return

                    if pr_level.isnumeric():
                        pr_level = int(pr_level)
                        if not pr_level >= 100:
                            if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                                pr_level = int(pr_level)
                                pr_current_xp = int(pr_current_xp)
                                pr_needed_xp = int(pr_needed_xp)
                                xp = pr_needed_xp - pr_current_xp
                                ice_cream = ceil(xp / 100)
                                ice_cream_wb = ceil(xp / 110)
                                xp_rest = 100 - (xp % 100)
                                xp_rest_wb = 110 - (xp % 110)
                                if xp_rest == 100:
                                    xp_rest = 0
                                if xp_rest_wb == 110:
                                    xp_rest_wb = 0
                                ice_cream_total = ice_cream
                                ice_cream_total_wb = ice_cream_wb

                                if pr_level >= level:
                                    await ctx.send(f'So.\nYou are level {pr_level} and you want to get to level {level}.\n{emojis.waitwhat}')
                                    return

                                levelrange = []

                                if (level - pr_level) == 1:
                                    enchanter_levels = []
                                else:
                                    levelrange = [pr_level+2, level,]
                                    enchanter_levels = await database.get_profession_levels(ctx,'enchanter',levelrange)

                                for enchanter_level in enchanter_levels:
                                    enchanter_level_xp = enchanter_level[1]
                                    actual_xp = enchanter_level_xp - xp_rest
                                    actual_xp_wb = enchanter_level_xp - xp_rest_wb
                                    ice_cream = ceil(actual_xp / 100)
                                    ice_cream_wb = ceil(actual_xp_wb / 110)
                                    ice_cream_total = ice_cream_total + ice_cream
                                    ice_cream_total_wb = ice_cream_total_wb + ice_cream_wb
                                    xp_rest = 100 - (actual_xp % 100)
                                    xp_rest_wb = 110 - (actual_xp_wb % 110)
                                    if xp_rest == 100:
                                        xp_rest = 0
                                    if xp_rest_wb == 110:
                                        xp_rest_wb = 0

                                await ctx.send(
                                    f'You need to cook the following amount of {emojis.foodfruiticecream} fruit ice cream to reach level {level}:\n'
                                    f'{emojis.bp} **{ice_cream_total:,}** without world buff\n'
                                    f'{emojis.bp} **{ice_cream_total_wb:,}** with world buff\n\n'
                                    f'Use `{ctx.prefix}craft [amount] ice cream` to see how much you need for that.'
                                )
                            else:
                                await ctx.send('Whelp, something went wrong here, sorry.')
                                return
                        else:
                            await ctx.send(
                                f'Sorry, this command can only calculate up to level 100.\n'
                                f'You can use `{ctx.prefix}pre` to calculate the ice cream needed to reach the next level though.'
                            )
                    else:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                except asyncio.TimeoutError as error:
                    await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                    return
            else:
                await ctx.send('Sir, that is not a valid number.')
                return

        else:
            await ctx.send(f'The command syntax is `{ctx.prefix}pretotal [level]`.\nIf you omit the level, I will calculate the ice cream you need to reach level 100.')
            return

    # Command "prltotal" - Calculate total lootboxes to craft until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prltotal(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Lootboxer') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if len(args) == 0:
            try:
                await ctx.send(f'**{ctx.author.name}**, please type `rpg pr lootboxer` (or `abort` to abort)')
                answer_user_lootboxer = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_lootboxer.content
                answer = answer.lower()
                if answer in ('rpg pr lootboxer','rpg profession lootboxer', 'rpg professions lootboxer'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        pr_lootboxer = str(answer_bot_at.embeds[0].fields[0])
                    except:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    start_level = pr_lootboxer.find('**Level**') + 11
                    end_level = pr_lootboxer.find('(', start_level) - 1
                    if end_level == -2:
                        end_level = pr_lootboxer.find('\\n', start_level)
                    pr_level = pr_lootboxer[start_level:end_level]
                    start_current_xp = pr_lootboxer.find('**XP**') + 8
                    end_current_xp = pr_lootboxer.find('/', start_current_xp)
                    pr_current_xp = pr_lootboxer[start_current_xp:end_current_xp]
                    pr_current_xp = pr_current_xp.replace(',','')
                    start_needed_xp = pr_lootboxer.find('/', start_current_xp) + 1
                    end_needed_xp = pr_lootboxer.find(f'\'', start_needed_xp)
                    pr_needed_xp = pr_lootboxer[start_needed_xp:end_needed_xp]
                    pr_needed_xp = pr_needed_xp.replace(',','')
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return
                if pr_level.isnumeric():
                    pr_level = int(pr_level)
                    if not pr_level >= 100:
                        if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                            pr_level = int(pr_level)
                            pr_current_xp = int(pr_current_xp)
                            pr_needed_xp = int(pr_needed_xp)
                            xp = pr_needed_xp - pr_current_xp
                            lootboxes = ceil(xp / 100)
                            lootboxes_wb = ceil(xp / 110)
                            xp_rest = 100 - (xp % 100)
                            xp_rest_wb = 110 - (xp % 110)
                            if xp_rest == 100:
                                xp_rest = 0
                            if xp_rest_wb == 110:
                                xp_rest_wb = 0
                            lootboxes_total = lootboxes
                            lootboxes_total_wb = lootboxes_wb

                            levelrange = []

                            if pr_level == 99:
                                lootboxer_levels = []
                            else:
                                levelrange = [pr_level+2, 100,]
                                lootboxer_levels = await database.get_profession_levels(ctx,'lootboxer',levelrange)

                            for lootboxer_level in lootboxer_levels:
                                lootboxer_level_xp = lootboxer_level[1]
                                actual_xp = lootboxer_level_xp - xp_rest
                                actual_xp_wb = lootboxer_level_xp - xp_rest_wb
                                lootboxes = ceil(actual_xp / 100)
                                lootboxes_wb = ceil(actual_xp_wb / 110)
                                lootboxes_total = lootboxes_total + lootboxes
                                lootboxes_total_wb = lootboxes_total_wb + lootboxes_wb
                                xp_rest = 100 - (actual_xp % 100)
                                xp_rest_wb = 110 - (actual_xp_wb % 110)
                                if xp_rest == 100:
                                    xp_rest = 0
                                if xp_rest_wb == 110:
                                    xp_rest_wb = 0

                            await ctx.send(
                                f'You need to cook the following amount of {emojis.foodfilledlootbox} filled lootboxes to reach level 100:\n'
                                f'{emojis.bp} **{lootboxes_total:,}** without world buff\n'
                                f'{emojis.bp} **{lootboxes_total_wb:,}** with world buff\n\n'
                                f'Use `{ctx.prefix}craft [amount] lootboxes` to see how much you need for that.'
                            )
                        else:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                    else:
                        await ctx.send(
                            f'Sorry, this command can only calculate up to level 100.\n'
                            f'You can use `{ctx.prefix}prl` to calculate the lootboxes needed to reach the next level though.'
                        )
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                return

        elif len(args) == 1:
            arg = args[0]

            if arg.replace('-','').isnumeric():
                try:
                    level = int(arg)
                except:
                    await ctx.send(
                        f'`{arg}` is not a valid target level. Please enter the level you want me to calculate to.\n'
                        f'Example: `{ctx.prefix}prltotal 80`. If you want me to calculate to level 100, you can omit the level.'
                    )
                    return

                if level < 2:
                    await ctx.send('You want to reach level what now?')
                    return
                elif level > 100:
                    await ctx.send(
                        f'Sorry, this command can only calculate up to level 100.\n'
                        f'You can use `{ctx.prefix}prl` to calculate the lootboxes needed to reach the next level though.'
                    )
                    return

                try:
                    await ctx.send(f'**{ctx.author.name}**, please type `rpg pr lootboxer` (or `abort` to abort)')
                    answer_user_lootboxer = await self.bot.wait_for('message', check=check, timeout = 30)
                    answer = answer_user_lootboxer.content
                    answer = answer.lower()
                    if answer in ('rpg pr lootboxer','rpg profession lootboxer', 'rpg professions lootboxer'):
                        answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                        try:
                            pr_lootboxer = str(answer_bot_at.embeds[0].fields[0])
                        except:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                        start_level = pr_lootboxer.find('**Level**') + 11
                        end_level = pr_lootboxer.find('(', start_level) - 1
                        if end_level == -2:
                            end_level = pr_lootboxer.find('\\n', start_level)
                        pr_level = pr_lootboxer[start_level:end_level]
                        start_current_xp = pr_lootboxer.find('**XP**') + 8
                        end_current_xp = pr_lootboxer.find('/', start_current_xp)
                        pr_current_xp = pr_lootboxer[start_current_xp:end_current_xp]
                        pr_current_xp = pr_current_xp.replace(',','')
                        start_needed_xp = pr_lootboxer.find('/', start_current_xp) + 1
                        end_needed_xp = pr_lootboxer.find(f'\'', start_needed_xp)
                        pr_needed_xp = pr_lootboxer[start_needed_xp:end_needed_xp]
                        pr_needed_xp = pr_needed_xp.replace(',','')
                    elif (answer_user_lootboxer.content == 'abort') or (answer_user_lootboxer.content == 'cancel'):
                        await ctx.send('Aborting.')
                        return
                    else:
                        await ctx.send('Wrong input. Aborting.')
                        return

                    if pr_level.isnumeric():
                        pr_level = int(pr_level)
                        if not pr_level >= 100:
                            if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                                pr_level = int(pr_level)
                                pr_current_xp = int(pr_current_xp)
                                pr_needed_xp = int(pr_needed_xp)
                                xp = pr_needed_xp - pr_current_xp
                                lootboxes = ceil(xp / 100)
                                lootboxes_wb = ceil(xp / 110)
                                xp_rest = 100 - (xp % 100)
                                xp_rest_wb = 110 - (xp % 110)
                                if xp_rest == 100:
                                    xp_rest = 0
                                if xp_rest_wb == 110:
                                    xp_rest_wb = 0
                                lootboxes_total = lootboxes
                                lootboxes_total_wb = lootboxes_wb

                                if pr_level >= level:
                                    await ctx.send(f'So.\nYou are level {pr_level} and you want to get to level {level}.\n{emojis.waitwhat}')
                                    return

                                levelrange = []

                                if (level - pr_level) == 1:
                                    lootboxer_levels = []
                                else:
                                    levelrange = [pr_level+2, level,]
                                    lootboxer_levels = await database.get_profession_levels(ctx,'lootboxer',levelrange)

                                for lootboxer_level in lootboxer_levels:
                                    lootboxer_level_xp = lootboxer_level[1]
                                    actual_xp = lootboxer_level_xp - xp_rest
                                    actual_xp_wb = lootboxer_level_xp - xp_rest_wb
                                    lootboxes = ceil(actual_xp / 100)
                                    lootboxes_wb = ceil(actual_xp_wb / 110)
                                    lootboxes_total = lootboxes_total + lootboxes
                                    lootboxes_total_wb = lootboxes_total_wb + lootboxes_wb
                                    xp_rest = 100 - (actual_xp % 100)
                                    xp_rest_wb = 110 - (actual_xp_wb % 110)
                                    if xp_rest == 100:
                                        xp_rest = 0
                                    if xp_rest_wb == 110:
                                        xp_rest_wb = 0

                                await ctx.send(
                                    f'You need to cook the following amount of {emojis.foodfilledlootbox} filled lootboxes to reach level {level}:\n'
                                    f'{emojis.bp} **{lootboxes_total:,}** without world buff\n'
                                    f'{emojis.bp} **{lootboxes_total_wb:,}** with world buff\n\n'
                                    f'Use `{ctx.prefix}craft [amount] lootboxes` to see how much you need for that.'
                                )
                            else:
                                await ctx.send('Whelp, something went wrong here, sorry.')
                                return
                        else:
                            await ctx.send(
                                f'Sorry, this command can only calculate up to level 100.\n'
                                f'You can use `{ctx.prefix}prl` to calculate the lootboxes needed to reach the next level though.'
                            )
                    else:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                except asyncio.TimeoutError as error:
                    await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                    return
            else:
                await ctx.send('Sir, that is not a valid number.')
                return

        else:
            await ctx.send(f'The command syntax is `{ctx.prefix}prltotal [level]`.\nIf you omit the level, I will calculate the filled lootboxes you need to reach level 100.')
            return

    # Command "prmtotal" - Calculate total logs to sell until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prmtotal(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Merchant') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if len(args) == 0:
            try:
                await ctx.send(f'**{ctx.author.name}**, please type `rpg pr merchant` (or `abort` to abort)')
                answer_user_merchant = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_merchant.content
                answer = answer.lower()
                if answer in ('rpg pr merchant','rpg profession merchant', 'rpg professions merchant'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        pr_merchant = str(answer_bot_at.embeds[0].fields[0])
                    except:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    start_level = pr_merchant.find('**Level**') + 11
                    end_level = pr_merchant.find('(', start_level) - 1
                    if end_level == -2:
                        end_level = pr_merchant.find('\\n', start_level)
                    pr_level = pr_merchant[start_level:end_level]
                    start_current_xp = pr_merchant.find('**XP**') + 8
                    end_current_xp = pr_merchant.find('/', start_current_xp)
                    pr_current_xp = pr_merchant[start_current_xp:end_current_xp]
                    pr_current_xp = pr_current_xp.replace(',','')
                    start_needed_xp = pr_merchant.find('/', start_current_xp) + 1
                    end_needed_xp = pr_merchant.find(f'\'', start_needed_xp)
                    pr_needed_xp = pr_merchant[start_needed_xp:end_needed_xp]
                    pr_needed_xp = pr_needed_xp.replace(',','')
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return
                if pr_level.isnumeric():
                    pr_level = int(pr_level)
                    if not pr_level >= 100:
                        if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                            pr_current_xp = int(pr_current_xp)
                            pr_needed_xp = int(pr_needed_xp)
                            xp = pr_needed_xp - pr_current_xp
                            logs_total = xp * 5

                            levelrange = []

                            if pr_level == 99:
                                merchant_levels = []
                            else:
                                levelrange = [pr_level+2, 100,]
                                merchant_levels = await database.get_profession_levels(ctx,'merchant',levelrange)

                            for merchant_level in merchant_levels:
                                logs_total = logs_total + (merchant_level[1] * 5)

                            logs_total_wb = 5 * ceil((logs_total/1.1) / 5)

                            await ctx.send(
                                f'You need to sell the following amount of {emojis.log} wooden logs to reach level 100:\n'
                                f'{emojis.bp} ~**{logs_total:,}** without world buff\n'
                                f'{emojis.bp} ~**{logs_total_wb:,}** with world buff'
                            )
                        else:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                    else:
                        await ctx.send(
                            f'Sorry, this command can only calculate up to level 100.\n'
                            f'You can use `{ctx.prefix}prm` to calculate the logs needed to reach the next level though.'
                        )
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                return

        elif len(args) == 1:
            arg = args[0]

            if arg.replace('-','').isnumeric():
                try:
                    level = int(arg)
                except:
                    await ctx.send(
                        f'`{arg}` is not a valid target level. Please enter the level you want me to calculate to.\n'
                        f'Example: `{ctx.prefix}prmtotal 80`. If you want me to calculate to level 100, you can omit the level.'
                    )
                    return

                if level < 2:
                    await ctx.send('You want to reach level what now?')
                    return
                elif level > 100:
                    await ctx.send(
                        f'Sorry, this command can only calculate up to level 100.\n'
                        f'You can use `{ctx.prefix}prm` to calculate the logs needed to reach the next level though.'
                    )
                    return

                try:
                    await ctx.send(f'**{ctx.author.name}**, please type `rpg pr merchant` (or `abort` to abort)')
                    answer_user_merchant = await self.bot.wait_for('message', check=check, timeout = 30)
                    answer = answer_user_merchant.content
                    answer = answer.lower()
                    if answer in ('rpg pr merchant','rpg profession merchant', 'rpg professions merchant'):
                        answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                        try:
                            pr_merchant = str(answer_bot_at.embeds[0].fields[0])
                        except:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                        start_level = pr_merchant.find('**Level**') + 11
                        end_level = pr_merchant.find('(', start_level) - 1
                        if end_level == -2:
                            end_level = pr_merchant.find('\\n', start_level)
                        pr_level = pr_merchant[start_level:end_level]
                        start_current_xp = pr_merchant.find('**XP**') + 8
                        end_current_xp = pr_merchant.find('/', start_current_xp)
                        pr_current_xp = pr_merchant[start_current_xp:end_current_xp]
                        pr_current_xp = pr_current_xp.replace(',','')
                        start_needed_xp = pr_merchant.find('/', start_current_xp) + 1
                        end_needed_xp = pr_merchant.find(f'\'', start_needed_xp)
                        pr_needed_xp = pr_merchant[start_needed_xp:end_needed_xp]
                        pr_needed_xp = pr_needed_xp.replace(',','')
                    elif (answer_user_merchant.content == 'abort') or (answer_user_merchant.content == 'cancel'):
                        await ctx.send('Aborting.')
                        return
                    else:
                        await ctx.send('Wrong input. Aborting.')
                        return

                    if pr_level.isnumeric():
                        pr_level = int(pr_level)
                        if not pr_level >= 100:
                            if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                                pr_level = int(pr_level)
                                pr_current_xp = int(pr_current_xp)
                                pr_needed_xp = int(pr_needed_xp)
                                xp = pr_needed_xp - pr_current_xp
                                logs_total = xp * 5

                                if pr_level >= level:
                                    await ctx.send(f'So.\nYou are level {pr_level} and you want to get to level {level}.\n{emojis.waitwhat}')
                                    return

                                levelrange = []

                                if (level - pr_level) == 1:
                                    merchant_levels = []
                                else:
                                    levelrange = [pr_level+2, level,]
                                    merchant_levels = await database.get_profession_levels(ctx,'merchant',levelrange)

                                for merchant_level in merchant_levels:
                                    logs_total = logs_total + (merchant_level[1] * 5)

                                logs_total_wb = 5 * ceil((logs_total/1.1) / 5)

                                await ctx.send(
                                    f'You need to sell the following amount of {emojis.log} wooden logs to reach level {level}:\n'
                                    f'{emojis.bp} ~**{logs_total:,}** without world buff\n'
                                    f'{emojis.bp} ~**{logs_total_wb:,}** with world buff'
                                )
                            else:
                                await ctx.send(f'Whelp, something went wrong here, sorry.')
                                return
                        else:
                            await ctx.send(
                                f'Sorry, this command can only calculate up to level 100.\n'
                                f'You can use `{ctx.prefix}prm` to calculate the logs needed to reach the next level though.'
                            )
                    else:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                except asyncio.TimeoutError as error:
                    await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                    return
            else:
                await ctx.send('Sir, that is not a valid number.')
                return

        else:
            await ctx.send(
                f'The command syntax is `{ctx.prefix}prmtotal [level]`.\n'
                f'If you omit the level, I will calculate the logs you need to reach level 100.'
            )
            return

    # Command "prwtotal" - Calculate total pickaxes to craft until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prwtotal(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Worker') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if len(args) == 0:
            try:
                await ctx.send(f'**{ctx.author.name}**, please type `rpg pr worker` (or `abort` to abort)')
                answer_user_worker = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_worker.content
                answer = answer.lower()
                if answer in ('rpg pr worker','rpg profession worker', 'rpg professions worker'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        pr_worker = str(answer_bot_at.embeds[0].fields[0])
                    except:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    start_level = pr_worker.find('**Level**') + 11
                    end_level = pr_worker.find('(', start_level) - 1
                    if end_level == -2:
                        end_level = pr_worker.find('\\n', start_level)
                    pr_level = pr_worker[start_level:end_level]
                    start_current_xp = pr_worker.find('**XP**') + 8
                    end_current_xp = pr_worker.find('/', start_current_xp)
                    pr_current_xp = pr_worker[start_current_xp:end_current_xp]
                    pr_current_xp = pr_current_xp.replace(',','')
                    start_needed_xp = pr_worker.find('/', start_current_xp) + 1
                    end_needed_xp = pr_worker.find(f'\'', start_needed_xp)
                    pr_needed_xp = pr_worker[start_needed_xp:end_needed_xp]
                    pr_needed_xp = pr_needed_xp.replace(',','')
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return
                if pr_level.isnumeric():
                    pr_level = int(pr_level)
                    if not pr_level >= 100:
                        if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                            pr_level = int(pr_level)
                            pr_current_xp = int(pr_current_xp)
                            pr_needed_xp = int(pr_needed_xp)
                            xp = pr_needed_xp - pr_current_xp
                            pickaxes = ceil(xp / 100)
                            pickaxes_wb = ceil(xp / 110)
                            xp_rest = 100 - (xp % 100)
                            xp_rest_wb = 110 - (xp % 110)
                            if xp_rest == 100:
                                xp_rest = 0
                            if xp_rest_wb == 110:
                                xp_rest_wb = 0
                            pickaxes_total = pickaxes
                            pickaxes_total_wb = pickaxes_wb

                            levelrange = []

                            if pr_level == 99:
                                worker_levels = []
                            else:
                                levelrange = [pr_level+2, 100,]
                                worker_levels = await database.get_profession_levels(ctx,'worker',levelrange)

                            for worker_level in worker_levels:
                                worker_level_xp = worker_level[1]
                                actual_xp = worker_level_xp - xp_rest
                                actual_xp_wb = worker_level_xp - xp_rest_wb
                                pickaxes = ceil(actual_xp / 100)
                                pickaxes_wb = ceil(actual_xp_wb / 110)
                                pickaxes_total = pickaxes_total + pickaxes
                                pickaxes_total_wb = pickaxes_total_wb + pickaxes_wb
                                xp_rest = 100 - (actual_xp % 100)
                                xp_rest_wb = 110 - (actual_xp_wb % 110)
                                if xp_rest == 100:
                                    xp_rest = 0
                                if xp_rest_wb == 110:
                                    xp_rest_wb = 0

                            await ctx.send(
                                f'You need to cook the following amount of {emojis.foodbananapickaxe} banana pickaxes to reach level 100:\n'
                                f'{emojis.bp} **{pickaxes_total:,}** without world buff\n'
                                f'{emojis.bp} **{pickaxes_total_wb:,}** with world buff\n\n'
                                f'Use `{ctx.prefix}craft [amount] pickaxes` to see how much you need for that.'
                            )
                        else:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                    else:
                        await ctx.send(
                            f'Sorry, this command can only calculate up to level 100.\n'
                            f'You can use `{ctx.prefix}prw` to calculate the pickaes needed to reach the next level though.'
                        )
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                return

        elif len(args) == 1:
            arg = args[0]

            if arg.replace('-','').isnumeric():
                try:
                    level = int(arg)
                except:
                    await ctx.send(
                        f'`{arg}` is not a valid target level. Please enter the level you want me to calculate to.\n'
                        f'Example: `{ctx.prefix}prwtotal 80`. If you want me to calculate to level 100, you can omit the level.'
                    )
                    return

                if level < 2:
                    await ctx.send('You want to reach level what now?')
                    return
                elif level > 100:
                    await ctx.send(
                        f'Sorry, this command can only calculate up to level 100.\n'
                        f'You can use `{ctx.prefix}prw` to calculate the pickaxes needed to reach the next level though.'
                    )
                    return

                try:
                    await ctx.send(f'**{ctx.author.name}**, please type `rpg pr worker` (or `abort` to abort)')
                    answer_user_worker = await self.bot.wait_for('message', check=check, timeout = 30)
                    answer = answer_user_worker.content
                    answer = answer.lower()
                    if answer in ('rpg pr worker','rpg profession worker', 'rpg professions worker'):
                        answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                        try:
                            pr_worker = str(answer_bot_at.embeds[0].fields[0])
                        except:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                        start_level = pr_worker.find('**Level**') + 11
                        end_level = pr_worker.find('(', start_level) - 1
                        if end_level == -2:
                            end_level = pr_worker.find('\\n', start_level)
                        pr_level = pr_worker[start_level:end_level]
                        start_current_xp = pr_worker.find('**XP**') + 8
                        end_current_xp = pr_worker.find('/', start_current_xp)
                        pr_current_xp = pr_worker[start_current_xp:end_current_xp]
                        pr_current_xp = pr_current_xp.replace(',','')
                        start_needed_xp = pr_worker.find('/', start_current_xp) + 1
                        end_needed_xp = pr_worker.find(f'\'', start_needed_xp)
                        pr_needed_xp = pr_worker[start_needed_xp:end_needed_xp]
                        pr_needed_xp = pr_needed_xp.replace(',','')
                    elif (answer_user_worker.content == 'abort') or (answer_user_worker.content == 'cancel'):
                        await ctx.send('Aborting.')
                        return
                    else:
                        await ctx.send('Wrong input. Aborting.')
                        return

                    if pr_level.isnumeric():
                        pr_level = int(pr_level)
                        if not pr_level >= 100:
                            if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                                pr_level = int(pr_level)
                                pr_current_xp = int(pr_current_xp)
                                pr_needed_xp = int(pr_needed_xp)
                                xp = pr_needed_xp - pr_current_xp
                                pickaxes = ceil(xp / 100)
                                pickaxes_wb = ceil(xp / 110)
                                xp_rest = 100 - (xp % 100)
                                xp_rest_wb = 110 - (xp % 110)
                                if xp_rest == 100:
                                    xp_rest = 0
                                if xp_rest_wb == 110:
                                    xp_rest_wb = 0
                                pickaxes_total = pickaxes
                                pickaxes_total_wb = pickaxes_wb

                                if pr_level >= level:
                                    await ctx.send(f'So.\nYou are level {pr_level} and you want to get to level {level}.\n{emojis.waitwhat}')
                                    return

                                levelrange = []

                                if (level - pr_level) == 1:
                                    worker_levels = []
                                else:
                                    levelrange = [pr_level+2, level,]
                                    worker_levels = await database.get_profession_levels(ctx,'worker',levelrange)

                                for worker_level in worker_levels:
                                    worker_level_xp = worker_level[1]
                                    actual_xp = worker_level_xp - xp_rest
                                    actual_xp_wb = worker_level_xp - xp_rest_wb
                                    pickaxes = ceil(actual_xp / 100)
                                    pickaxes_wb = ceil(actual_xp_wb / 110)
                                    pickaxes_total = pickaxes_total + pickaxes
                                    pickaxes_total_wb = pickaxes_total_wb + pickaxes_wb
                                    xp_rest = 100 - (actual_xp % 100)
                                    xp_rest_wb = 110 - (actual_xp_wb % 110)
                                    if xp_rest == 100:
                                        xp_rest = 0
                                    if xp_rest_wb == 110:
                                        xp_rest_wb = 0

                                await ctx.send(
                                    f'You need to cook the following amount of {emojis.foodbananapickaxe} banana pickaxes to reach level {level}:\n'
                                    f'{emojis.bp} **{pickaxes_total:,}** without world buff\n'
                                    f'{emojis.bp} **{pickaxes_total_wb:,}** with world buff\n\n'
                                    f'Use `{ctx.prefix}craft [amount] pickaxes` to see how much you need for that.'
                                )
                            else:
                                await ctx.send('Whelp, something went wrong here, sorry.')
                                return
                        else:
                            await ctx.send(
                                f'Sorry, this command can only calculate up to level 100.\n'
                                f'You can use `{ctx.prefix}prw` to calculate the pickaxes needed to reach the next level though.'
                            )
                    else:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                except asyncio.TimeoutError as error:
                    await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                    return
            else:
                await ctx.send('Sir, that is not a valid number.')
                return
        else:
            await ctx.send(f'The command syntax is `{ctx.prefix}prwtotal [level]`.\nIf you omit the level, I will calculate the banana pickaxes you need to reach level 100.')
            return


# Initialization
def setup(bot):
    bot.add_cog(professionsCog(bot))



# --- Redundancies ---
# Guides
guide_overview = '`{prefix}pr` : Professions overview'
guide_ascension = '`{prefix}pr ascension` : Details about ascension'
guide_crafter = '`{prefix}pr crafter` : Details about crafter'
guide_enchanter = '`{prefix}pr enchanter` : Details about enchanter'
guide_level = '`{prefix}pr level` : How and when to level up your professions'
guide_lootboxer = '`{prefix}pr lootboxer` : Details about lootboxer'
guide_merchant = '`{prefix}pr merchant` : Details about merchant'
guide_worker = '`{prefix}pr worker` : Details about worker'

# Calculators
calc_pre = '`{prefix}pre` : Ice cream you need to cook for your next enchanter levels'
calc_prl = '`{prefix}prl` : Lootboxes you need to cook for your next lootboxer levels'
calc_prm = '`{prefix}prm` : Logs you need to sell for your next merchant levels'
calc_prw = '`{prefix}prw` : Pickaxes you need to cook for your next worker levels'
calc_pretotal = '`{prefix}pretotal [level]` : Total ice cream you need to reach `[level]`'
calc_prltotal = '`{prefix}prltotal [level]` : Total lootboxes you need to reach `[level]`'
calc_prmtotal = '`{prefix}prmtotal [level]` : Total logs you need to reach `[level]`'
calc_prwtotal = '`{prefix}prwtotal [level]` : Total pickaxes you need to reach `[level]`'



# --- Embeds ---
# Professions overview
async def embed_professions_overview(prefix):

    worker = (
        f'{emojis.bp} Increases the chance to get better items with work commands\n'
        f'{emojis.bp} Level 101+: Adds a chance to find other items with work commands\n'
        f'{emojis.bp} For more details see `{prefix}pr worker`'
    )

    crafter = (
        f'{emojis.bp} Increases the chance to get 10% materials back when crafting\n'
        f'{emojis.bp} Level 101+: Increases the percentage of items returned\n'
        f'{emojis.bp} For more details see `{prefix}pr crafter`'
    )

    lootboxer = (
        f'{emojis.bp} Increases the bank XP bonus\n'
        f'{emojis.bp} Decreases the cost of horse training\n'
        f'{emojis.bp} Level 101+: Increases the maximum level of your horse\n'
        f'{emojis.bp} For more details see `{prefix}pr lootboxer`'
    )

    merchant = (
        f'{emojis.bp} Increases the amount of coins you get when selling items\n'
        f'{emojis.bp} Level 101+: Adds a chance to get {emojis.dragonscale} dragon scales when selling mob drops\n'
        f'{emojis.bp} For more details see `{prefix}pr merchant`'
    )

    enchanter = (
        f'{emojis.bp} Increases the chance to get a better enchant when enchanting\n'\
        f'{emojis.bp} Level 101+: Adds a chance to win the price of the enchant instead of spending it\n'
        f'{emojis.bp} For more details see `{prefix}pr enchanter`'
    )

    guides = (
        f'{emojis.bp} {guide_ascension.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_crafter.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_enchanter.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_level.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_lootboxer.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_merchant.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_worker.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'PROFESSIONS',
        description = (
            f'There are 5 professions you can increase to get increasing bonuses.\n'
            f'Each profession has a bonus that caps at level 100. You can level further but it will take much longer and the bonuses for levels 101+ are different.\n'
            f'If you get all professions to level 100, you can ascend (see `{prefix}pr ascension`).'
        )
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'WORKER {emojis.prworker}', value=worker, inline=False)
    embed.add_field(name=f'CRAFTER {emojis.prcrafter}', value=crafter, inline=False)
    embed.add_field(name=f'LOOTBOXER {emojis.prlootboxer}', value=lootboxer, inline=False)
    embed.add_field(name=f'MERCHANT {emojis.prmerchant}', value=merchant, inline=False)
    embed.add_field(name=f'ENCHANTER {emojis.prenchanter}', value=enchanter, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Professions leveling guide
async def embed_professions_leveling(prefix):

    crafter = (
        f'{emojis.bp} This is the first profession you should level up\n'
        f'{emojis.bp} Level **before time traveling** with leftover materials\n'
        f'{emojis.bp} Trade everything to {emojis.log} logs and craft/dismantle {emojis.logepic} EPIC logs\n'
        f'{emojis.bp} Craft in batches of 500 or 1000 (you can dismantle all at once)\n'
        f'{emojis.bp} Once you reach level 90, switch to leveling merchant'
    )

    merchant = (
        f'{emojis.bp} This is the second profession you should level up\n'
        f'{emojis.bp} Level **before time traveling** with leftover materials\n'
        f'{emojis.bp} Trade everything to {emojis.log} logs\n'
        f'{emojis.bp} For each level look up `rpg pr merchant` and calculate the XP you need for the next level\n'
        f'{emojis.bp} Take 5x the XP amount and sell as many {emojis.log} logs\n'
        f'{emojis.bp} Tip: You can quickly calculate logs to sell with `{prefix}prm`\n'
        f'{emojis.bp} Once you reach level 90, focus on lootboxer and worker'
    )

    lootboxer = (
        f'{emojis.bp} Level up by opening lootboxes\n'
        f'{emojis.bp} Better lootboxes give more XP (see `{prefix}pr lootboxer`)\n'
        f'{emojis.bp} It should not be necessary to cook {emojis.foodfilledlootbox} filled lootboxes anymore\n'
        f'{emojis.bp} Use `hunt hardmode` whenever you have access (unlocks in A13)'
    )

    worker = (
        f'{emojis.bp} Level up by using work commands or cooking {emojis.foodbananapickaxe} banana pickaxes\n'
        f'{emojis.bp} Higher tier work commands give more XP (see `{prefix}pr worker`)\n'
        f'{emojis.bp} Try to keep the level at about the same as lootboxer\n'
        f'{emojis.bp} If lower than lootboxer, consider cooking {emojis.foodbananapickaxe} banana pickaxes\n'
        f'{emojis.bp} Tip: You can quickly calculate the pickaxes you need with `{prefix}prw`'
    )

    enchanter = (
        f'{emojis.bp} This is the last profession you should level up because of costs\n'
        f'{emojis.bp} Level before time traveling using `transmute` or `transcend`\n'
        f'{emojis.bp} XP gain is based on the quality of the enchant you get (see `{prefix}pr enchanter`)\n'
        f'{emojis.bp} Costs around 3 billion coins without {emojis.horset8} T8+ horse\n'
        f'{emojis.bp} Costs around 2 billion coins with {emojis.horset8} T8+ horse'
    )

    calculators = (
        f'{emojis.bp} {calc_pre.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_prl.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_prm.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_prw.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_pretotal.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_prltotal.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_prmtotal.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_prwtotal.format(prefix=prefix)}'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_ascension.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_crafter.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_enchanter.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_level.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_lootboxer.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_merchant.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_worker.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'LEVELING UP PROFESSIONS',
        description = (
            f'This guide shows you how to level up professions to reach ascension (level 100).\n'
            f'Do not overfarm to get ascended as early as possible. It wastes a lot of time you could spend time traveling. TT give high bonuses and ascension makes more sense if you already have access to all commands up to area 15.\n'
            f'Thus, unless you can reach ascension easily, always time travel again instead of staying and farming.'
        )
    )
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'1. CRAFTER {emojis.prcrafter}', value=crafter, inline=False)
    embed.add_field(name=f'2. MERCHANT {emojis.prmerchant}', value=merchant, inline=False)
    embed.add_field(name=f'3. WORKER {emojis.prworker}', value=worker, inline=False)
    embed.add_field(name=f'4. LOOTBOXER {emojis.prlootboxer}', value=lootboxer, inline=False)
    embed.add_field(name=f'5. ENCHANTER {emojis.prenchanter}', value=enchanter, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Crafter guide
async def embed_professions_crafter(prefix):

    base_bonus = (
        f'{emojis.bp} Increases the chance to get 10% materials back when crafting\n'
        f'{emojis.bp} The chance at level 100 is 80%'
    )

    level_101 =(
        f'{emojis.bp} Increases the percentage of items returned\n'
        f'{emojis.bp} The percentage increases logarithmically'
    )

    how_to_get_xp = (
        f'{emojis.bp} Craft and dismantle\n'
        f'{emojis.bp} ~~Cook {emojis.foodheavyapple} heavy apples (100 XP each)~~ (don\'t do that)'
    )

    xp_gain = (
        f'{emojis.bp} A detailed list of all material and gear XP is available in the [Wiki](https://epic-rpg.fandom.com/wiki/Professions#Crafter)'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'CRAFTER PROFESSION'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Enchanter guide
async def embed_professions_enchanter(prefix):

    base_bonus = (
        f'{emojis.bp} Increases the chance to get a better enchant when enchanting\n'
        f'{emojis.bp} The exact chance increase is unknown'
    )

    level_101 =(
        f'{emojis.bp} Adds a chance to win the price of the enchant instead of spending it\n'
        f'{emojis.bp} The chance is 2% at level 101 and increases by 2% for every level'
    )

    how_to_get_xp = (
        f'{emojis.bp} Use enchanting commands\n'
        f'{emojis.bp} The XP formula is [command multiplier] * [enchantment xp]\n'
        f'{emojis.bp} Example: If you enchant **Ultimate** with `transmute`, you get 600 (100*6) XP\n'
        f'{emojis.bp} ~~Cook {emojis.foodfruiticecream} fruit ice cream (100 XP each)~~ (don\'t do that)'
    )

    xp_gain = (
        f'{emojis.bp} **Normie**: 0 XP\n'
        f'{emojis.bp} **Good**: 1 XP\n'
        f'{emojis.bp} **Great**: 2 XP\n'
        f'{emojis.bp} **Mega**: 3 XP\n'
        f'{emojis.bp} **Epic**: 4 XP\n'
        f'{emojis.bp} **Hyper**: 5 XP\n'
        f'{emojis.bp} **Ultimate**: 6 XP\n'
        f'{emojis.bp} **Perfect**: 7 XP\n'
        f'{emojis.bp} **EDGY**: 8 XP\n'
        f'{emojis.bp} **ULTRA-EDGY**: 9 XP\n'
        f'{emojis.bp} **OMEGA**: 10 XP\n'
        f'{emojis.bp} **ULTRA-OMEGA**: 11 XP\n'
        f'{emojis.bp} **GODLY**: 12 XP'
    )

    command_multipliers = (
        f'{emojis.bp} `enchant`: 1\n'
        f'{emojis.bp} `refine`: 10\n'
        f'{emojis.bp} `transmute`: 100\n'
        f'{emojis.bp} `transcend`: 1000'
    )

    calculators = (
        f'{emojis.bp} {calc_pre.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_pretotal.format(prefix=prefix)}'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'ENCHANTER PROFESSION'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='COMMAND MULTIPLIERS', value=command_multipliers, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Lootboxer guide
async def embed_professions_lootboxer(prefix):

    base_bonus = (
        f'{emojis.bp} Increases the bank XP bonus\n'
        f'{emojis.bp} Decreases the cost of horse training\n'
        f'{emojis.bp} Horse training is 50 % cheaper at level 100\n'\
        f'{emojis.bp} The exact buff of the bank bonus unknown'
    )

    level_101 =(
        f'{emojis.bp} Increases the maximum level of your horse\n'
        f'{emojis.bp} The level increases by 1 per level after 100'
    )

    how_to_get_xp = (
        f'{emojis.bp} Open lootboxes\n'
        f'{emojis.bp} ~~Cook {emojis.foodfilledlootbox} filled lootboxes (100 XP each)~~ (don\'t do that)\n'
    )

    xp_gain = (
        f'{emojis.bp} {emojis.lbcommon} common lootbox: 4 XP\n'
        f'{emojis.bp} {emojis.lbuncommon} uncommon lootbox: 9 XP\n'
        f'{emojis.bp} {emojis.lbrare} rare lootbox: 17 XP\n'
        f'{emojis.bp} {emojis.lbepic} EPIC lootbox: 30 XP\n'
        f'{emojis.bp} {emojis.lbedgy} EDGY lootbox: 65 XP\n'
        f'{emojis.bp} {emojis.lbomega} OMEGA lootbox: 800 XP\n'
        f'{emojis.bp} {emojis.lbgodly} GODLY lootbox: 15004 XP'
    )

    calculators = (
        f'{emojis.bp} {calc_prl.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_prltotal.format(prefix=prefix)}'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'LOOTBOXER PROFESSION'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Merchant guide
async def embed_professions_merchant(prefix):

    base_bonus = (
        f'{emojis.bp} Increases the amount of coins you get when selling items\n'
        f'{emojis.bp} You get 4.929395x more coins at level 100'
    )

    level_101 =(
        f'{emojis.bp} Adds a chance to get {emojis.dragonscale} dragon scales when selling mob drops\n'
        f'{emojis.bp} The exact chance increase is unknown'
    )

    how_to_get_xp = (
        f'{emojis.bp} Sell materials\n'
        f'{emojis.bp} Note that you don\'t get any XP when selling gear and other items\n'
        f'{emojis.bp} ~~Cook {emojis.foodcoinsandwich} coin sandwich (100 XP each)~~ (**DON\'T DO THAT**)\n'
    )

    xp_gain = (
        f'{emojis.bp} A detailed list of XP per amount sold is available in the [Wiki](https://epic-rpg.fandom.com/wiki/Professions#Merchant)'
    )

    calculators = (
        f'{emojis.bp} {calc_prm.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_prmtotal.format(prefix=prefix)}'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'MERCHANT PROFESSION'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Worker guide
async def embed_professions_worker(prefix):

    base_bonus = (
        f'{emojis.bp} Increases the chance to get a better item with work commands\n'
        f'{emojis.bp} The chance increase is 50% at level 100'
    )

    level_101 =(
        f'{emojis.bp} Adds an increasing chance to find other items with top tier work commands\n'
        f'{emojis.bp} The chance is 4% at level 101 and increases by 4% for every level\n'
        f'{emojis.bp} `bigboat` gets a chance to drop {emojis.fruitbanana} bananas\n'
        f'{emojis.bp} `chainsaw` gets a chance to drop {emojis.fish} normie fish\n'
        f'{emojis.bp} `dynamite` gets a chance to drop {emojis.logsuper} SUPER logs\n'
        f'{emojis.bp} `greenhouse` gets a chance to drop {emojis.ruby} rubies'
    )

    how_to_get_xp = (
        f'{emojis.bp} Use work commands\n'
        f'{emojis.bp} Cook {emojis.foodbananapickaxe} banana pickaxes (100 XP each)\n'
    )

    xp_gain = (
        f'{emojis.bp} `chop` / `fish` / `pickup` / `mine`: 4 XP\n'
        f'{emojis.bp} `axe` / `ladder` / `pickaxe`: 8 XP\n'
        f'{emojis.bp} `net`: 9 XP\n'
        f'{emojis.bp} `bowsaw` / `tractor` / `drill`: 12 XP\n'
        f'{emojis.bp} `boat`: 13 XP\n'
        f'{emojis.bp} `chainsaw`: 16 XP\n'
        f'{emojis.bp} `greenhouse` / `dynamite`: 17 XP\n'
        f'{emojis.bp} `bigboat`: 18 XP'
    )

    calculators = (
        f'{emojis.bp} {calc_prw.format(prefix=prefix)}\n'
        f'{emojis.bp} {calc_prwtotal.format(prefix=prefix)}'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'WORKER PROFESSION'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Ascension
async def embed_ascension(prefix):

    requirements = (
        f'{emojis.bp} All 5 professions at level 100+ (see `{prefix}pr level`)\n'
        f'{emojis.bp} {emojis.timetravel} TT 1+'
    )

    benefits =(
        f'{emojis.bp} Get more materials by using high tier work commands early\n'
        f'{emojis.bp} Get more XP by using `hunt hardmode` and `adventure hardmode` early\n'
        f'{emojis.bp} Get higher enchants easier by using `transcend` and `transmute` early\n'
        f'{emojis.bp} {emojis.ruby} rubies and {emojis.fruitbanana} bananas are obtainable in area 1+'
    )

    notes = (
        f'{emojis.bp} The syntax is `rpg ascended [command]`\n'
        f'{emojis.bp} Trade rates are still area locked\n'
        f'{emojis.bp} Higher tier logs and fish remain area locked. Use `rpg h [material]` to see the area they unlock in.'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'ASCENSION',
        description = (
            f'Ascension allows you to use **all** game commands you ever unlocked in **every** area.\n'
            f'This makes it much easier to get XP, materials and high enchants early.'
        )
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='BENEFITS', value=benefits, inline=False)
    embed.add_field(name='NOTES', value=notes, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed