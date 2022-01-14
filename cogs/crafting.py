# crafting.py

import asyncio

import discord
from discord.ext import commands

import database
import emojis
import global_data


# crafting commands (cog)
class craftingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "enchants"
    @commands.command(aliases=('enchant','e','enchanting',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def enchants(self, ctx):
        embed = await embed_enchants(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "drops" - Returns all monster drops and where to get them
    @commands.command(aliases=('drop','mobdrop','mobdrops','mobsdrop','mobsdrops','monsterdrop','monsterdrops',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def drops(self, ctx):
        embed = await embed_drops(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "dropchance" - Calculate current drop chance
    @commands.command(aliases=('dropcalc','droprate',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def dropchance(self, ctx, *args):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if embed_author.find(f'{ctx_author}\'s horse') > 1:
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if args:
            if len(args) == 2:
                user_tt, horse_tier = args
                user_tt = user_tt.lower().replace('tt','')
                horse_tier = horse_tier.lower().replace('t','')

                if user_tt.isnumeric():
                    user_tt = int(user_tt)
                    if horse_tier.isnumeric():
                        horse_tier = int(horse_tier)
                        if not 1 <= horse_tier <= 10:
                            await ctx.send(f'`{horse_tier}` is not a valid horse tier.\nPlease enter a tier between 1 and 10.')
                            return
                    else:
                        await ctx.send(f'`{args[1]}` doesn\'t look like a valid horse tier to me :thinking:')
                        return
                    if not 0 <= user_tt <= 999:
                            await ctx.send(f'`{user_tt}` is not a valid TT.\nPlease enter a TT between 0 and 999.')
                            return
                else:
                    await ctx.send(f'`{args[0]}` doesn\'t look like a valid TT to me :thinking:')
                    return

                tt_chance = (49+user_tt)*user_tt/2/100

                horse_tier_chance = {
                    1: 1,
                    2: 1,
                    3: 1,
                    4: 1,
                    5: 1,
                    6: 1,
                    7: 1.2,
                    8: 1.5,
                    9: 2,
                    10: 3
                }

                horse_chance = horse_tier_chance[horse_tier]
                drop_chance = 4*(1+tt_chance)*horse_chance
                drop_chance_worldbuff = 4*(1+tt_chance)*horse_chance*1.2
                drop_chance_daily = 4*(1+tt_chance)*horse_chance*1.1
                drop_chance_worldbuff_daily = 4*(1+tt_chance)*horse_chance*1.3
                drop_chance = round(drop_chance,1)
                drop_chance_worldbuff = round(drop_chance_worldbuff,1)
                drop_chance_daily = round(drop_chance_daily,1)
                drop_chance_worldbuff_daily = round(drop_chance_worldbuff_daily,1)

                if drop_chance >= 100: drop_chance = 100
                if drop_chance_worldbuff >= 100: drop_chance_worldbuff = 100
                if drop_chance_daily >= 100: drop_chance_daily = 100
                if drop_chance_worldbuff_daily >= 100: drop_chance_worldbuff_daily = 100

                hunt_drop_chance = drop_chance/2
                hunt_drop_chance_worldbuff = drop_chance_worldbuff/2
                hunt_drop_chance_daily = drop_chance_daily/2
                hunt_drop_chance_worldbuff_daily = drop_chance_worldbuff_daily/2
                hunt_drop_chance = round(hunt_drop_chance,2)
                hunt_drop_chance_worldbuff = round(hunt_drop_chance_worldbuff,2)

                horse_emoji = getattr(emojis, f'HORSE_T{horse_tier}')

                await ctx.send(
                    f'**{ctx.author.name}**, you are currently in {emojis.TIME_TRAVEL} **TT {user_tt}** and have a {horse_emoji} **T{horse_tier}** horse.\n\n'
                    f'**Your drop chance**\n'
                    f'{emojis.BP} Base drop chance: **__{drop_chance:g} %__**.\n'
                    f'{emojis.BP} Active world buff: **__{drop_chance_worldbuff:g} %__**.\n'
                    f'{emojis.BP} Mob is daily monster: **__{drop_chance_daily:g} %__**.\n'
                    f'{emojis.BP} Active world buff _and_ mob is daily monster: **__{drop_chance_worldbuff_daily:g} %__**.\n\n'
                    f'**Total drop chance while hunting**\n'
                    f'{emojis.BP} The chance to encounter a mob that drops items is 50 %, so the total chance of getting a mob drop when using `rpg hunt` is **half** of the values above.\n\n'
                    f'**Drop chance in hardmode**\n'
                    f'{emojis.BP} If you are using `rpg hunt hardmode`, the drop chance is increased further. The exact increase is unknown, it is currently believed to be around 70 to 75 %.'
                )

            else:
                await ctx.send(f'The command syntax is `{ctx.prefix}dropchance [tt] [horse tier]`\nYou can also omit all parameters to use your current TT and horse tier for the calculation.\n\nExamples: `{ctx.prefix}dropchance 25 7` or `{ctx.prefix}dropchance tt7 t5` or `{ctx.prefix}dropchance`')
        else:
            try:
                try:
                    user_settings = await database.get_user_settings(ctx)
                except Exception as error:
                    if isinstance(error, database.FirstTimeUser):
                        return
                    else:
                        await ctx.send(global_data.MSG_ERROR)
                        return
                user_tt, _ = user_settings
                tt_chance = (49 + user_tt) * user_tt / 2 / 100

                await ctx.send(f'**{ctx.author.name}**, please type `rpg horse` (or `abort` to abort)')
                answer_user_merchant = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_merchant.content
                answer = answer.lower()
                if answer == 'rpg horse':
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        horse_stats = str(answer_bot_at.embeds[0].fields[0])
                        horse_chance = 0
                        horse_tier = 0
                        horse_emoji = ''
                    except:
                        await ctx.send(global_data.MSG_ERROR)
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
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                elif answer in ('abort','cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return

                if horse_chance != 0 and horse_tier != 0:
                    drop_chance = 4*(1+tt_chance)*horse_chance
                    drop_chance_worldbuff = 4*(1+tt_chance)*horse_chance*1.2
                    drop_chance_daily = 4*(1+tt_chance)*horse_chance*1.1
                    drop_chance_worldbuff_daily = 4*(1+tt_chance)*horse_chance*1.3
                    drop_chance = round(drop_chance,1)
                    drop_chance_worldbuff = round(drop_chance_worldbuff,1)
                    drop_chance_daily = round(drop_chance_daily,1)
                    drop_chance_worldbuff_daily = round(drop_chance_worldbuff_daily,1)

                    if drop_chance >= 100: drop_chance = 100
                    if drop_chance_worldbuff >= 100: drop_chance_worldbuff = 100
                    if drop_chance_daily >= 100: drop_chance_daily = 100
                    if drop_chance_worldbuff_daily >= 100: drop_chance_worldbuff_daily = 100

                    hunt_drop_chance = drop_chance/2
                    hunt_drop_chance_worldbuff = drop_chance_worldbuff/2
                    hunt_drop_chance_daily = drop_chance_daily/2
                    hunt_drop_chance_worldbuff_daily = drop_chance_worldbuff_daily/2
                    hunt_drop_chance = round(hunt_drop_chance,2)
                    hunt_drop_chance_worldbuff = round(hunt_drop_chance_worldbuff,2)

                    horse_emoji = getattr(emojis, f'HORSE_T{horse_tier}')

                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return

                await ctx.send(
                    f'**{ctx.author.name}**, you are currently in {emojis.TIME_TRAVEL} **TT {user_tt}** and have a {horse_emoji} **T{horse_tier}** horse.\n\n'
                    f'**Your drop chance**\n'
                    f'{emojis.BP} Base drop chance: **__{drop_chance:g} %__**.\n'
                    f'{emojis.BP} Active world buff: **__{drop_chance_worldbuff:g} %__**.\n'
                    f'{emojis.BP} Mob is daily monster: **__{drop_chance_daily:g} %__**.\n'
                    f'{emojis.BP} Active world buff _and_ mob is daily monster: **__{drop_chance_worldbuff_daily:g} %__**.\n\n'
                    f'**Total drop chance while hunting**\n'
                    f'{emojis.BP} The chance to encounter a mob that drops items is 50 %, so the total chance of getting a mob drop when using `rpg hunt` is **half** of the values above.\n\n'
                    f'**Drop chance in hardmode**\n'
                    f'{emojis.BP} If you are using `rpg hunt hardmode`, the drop chance is increased further. The exact increase is unknown, it is currently believed to be around 70 to 75 %.\n\n'
                    f'**Note**\n'
                    f'If your TT is wrong, use `{ctx.prefix}setprogress` to update your user settings.\n\n'
                    f'Tip: You can use `{ctx.prefix}dropchance [tt] [horse tier]` to check the drop chance for any TT and horse.'
                )

            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your horse information, RIP.')

    @commands.command(aliases=('cook','forge',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def craft(self, ctx: commands.Context, *args: str) -> None:
        """Calculates mats you need when crafting items"""
        msg_syntax = (
            f'The command syntax is `{ctx.prefix}craft [amount] [item]` or `{ctx.prefix}craft [item] [amount]`\n'
            f'You can omit the amount if you want to see the materials for one item only.'
        )
        if not args:
            await ctx.send(msg_syntax)
            return
        itemname = ''
        amount = 1
        for arg in args:
            if not arg.lstrip('-').replace('.','').replace(',','').replace('\'','').isnumeric():
                itemname = f'{itemname} {arg}'
                itemname = itemname.strip()
                itemname = itemname.lower()
            else:
                try:
                    amount = int(arg.replace('.','').replace(',',''))
                except:
                    await ctx.send(f'Are you trying to break me or something? :thinking:')
                    return
                if amount <= 0:
                    await ctx.send(f'You wanna do _what_? Craft **{arg}** items?? Have some :bread: instead.')
                    return
                if amount >= 100_000_000_000:
                    await ctx.send(f'Are you trying to break me or something? :thinking:')
                    return

        if itemname == '':
            await ctx.send(msg_syntax)
            return

        itemname_replaced = (
            itemname.replace('logs','log')
            .replace('ultra edgy','ultra-edgy')
            .replace('ultra omega','ultra-omega')
            .replace('uo ','ultra-omega ')
            .replace('creatures','creature')
            .replace('salads','salad')
            .replace('juices','juice')
            .replace('cookies','cookie')
            .replace('pickaxes','pickaxe')
            .replace('lootboxes','lootbox')
            .replace(' lb',' lootbox')
            .replace('sandwiches','sandwich')
            .replace('apples','apple')
            .replace('oranges','orange')
        )
        if itemname_replaced in global_data.item_aliases:
            itemname_replaced = global_data.item_aliases[itemname_replaced]

        if itemname_replaced in ('ultimate log', 'super fish', 'watermelon'):
            await ctx.send(':shushing_face:')
            return
        try:
            item: database.Item = await database.get_item(ctx, itemname_replaced)
        except database.NoDataFound:
            await ctx.send(f'Uhm, I don\'t know a recipe to craft `{itemname}`, sorry.')
            return

        if item.item_type in ('sword', 'armor') and amount > 1:
            await ctx.send(f'You can only craft 1 {item.emoji} `{item.name}`.')
            return
        if not item.ingredients:
            await ctx.send(f'{item.emoji} `{item.name}` is not craftable.')
            return

        breakdown_totals = await get_item_breakdown(ctx, item, amount)

        if amount == 1:
            message = f'To craft {item.emoji} `{item.name}` you need:'
        else:
            message = f'To craft {amount:,} {item.emoji} `{item.name}` you need:'
        for ingredient in item.ingredients:
            ingredient_item: database.Item = await database.get_item(ctx, ingredient.name)
            message = f'{message}\n> {ingredient.amount * amount:,} {ingredient_item.emoji} `{ingredient_item.name}`'

        if breakdown_totals != '':
            message = f'{message}\n\n{breakdown_totals}'

        await ctx.send(message)

    @commands.command(aliases=('dm',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def dismantle(self, ctx: commands.Context, *args: str) -> None:
        """Calculates mats you get when dismantling items"""
        msg_syntax = (
            f'The command syntax is `{ctx.prefix}dismantle [amount] [item]` or `{ctx.prefix}dismantle [item] [amount]`\n'
            f'You can omit the amount if you want to see the materials for one item only.'
        )
        if not args:
            await ctx.send(msg_syntax)
            return
        itemname = ''
        amount = 1
        args = [arg.lower() for arg in args]
        for arg in args:
            if not arg.lstrip('-').replace('.','').replace(',','').replace('\'','').isnumeric():
                itemname = f'{itemname} {arg}'.strip()
            else:
                try:
                    amount = int(arg.replace('.','').replace(',',''))
                except:
                    await ctx.send(f'Are you trying to break me or something? :thinking:')
                    return
                if amount <= 0:
                    await ctx.send(f'You wanna do _what_? Dismantle **{arg}** items?? Have some :bread: instead.')
                    return
                if amount >= 100_000_000_000:
                    await ctx.send(f'Are you trying to break me or something? :thinking:')
                    return

        if itemname == '':
            await ctx.send(msg_syntax)
            return

        if itemname == 'brandon':
            await ctx.send('I WILL NEVER ALLOW THAT. YOU MONSTER.')
            return

        if itemname in global_data.item_aliases:
            itemname = global_data.item_aliases[itemname]

        if itemname in ('ultimate log', 'super fish', 'watermelon'):
            await ctx.send(':shushing_face:')
            return
        try:
            item: database.Item = await database.get_item(ctx, itemname)
        except database.NoDataFound:
            await ctx.send(f'Uhm, I don\'t know an item called `{itemname}`, sorry.')
            return
        if not item.dismanteable:
            await ctx.send(f'{item.emoji} `{item.name}` can not be dismantled.')
            return

        breakdown_totals = await get_item_breakdown(ctx, item, amount, dismantle=True)

        if amount == 1:
            message = f'By dismantling {item.emoji} `{item.name}` you get:'
        else:
            message = f'By dismantling {amount:,} {item.emoji} `{item.name}` you get:'
        for ingredient in item.ingredients:
            ingredient_item: database.Item = await database.get_item(ctx, ingredient.name)
            message = f'{message}\n> {int(ingredient.amount * amount * 0.8):,} {ingredient_item.emoji} `{ingredient_item.name}`'

        if breakdown_totals != '':
            message = f'{message}\n\n{breakdown_totals}'

        await ctx.send(message)

    # Command "invcalc" - Calculates amount of items craftable with current inventory
    @commands.command(aliases=('ic','invc','icalc','inventoryc','inventorycalc',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def invcalc(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s inventory') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        prefix = ctx.prefix

        error_syntax = (
            f'The command syntax is `{ctx.prefix}invcalc [current max area] [material]`\n'
            f'Example: `{ctx.prefix}invcalc a5 apple`'
        )

        items = [
            'log',
            'epic log',
            'super log',
            'mega log',
            'hyper log',
            'ultra log',
            'ruby',
            'apple',
            'banana',
            'fish',
            'golden fish',
            'epic fish'
        ]

        if args:
            if len(args) >= 2:
                area = args[0].lower()
                args = list(args)
                args.pop(0)
                item = ''
                for arg in args:
                    item = f'{item} {arg}'
                item = item.strip()
                if area.find('top') > -1:
                    area = 16
                else:
                    area = area.lower().replace('a','')
                    if area.isnumeric():
                        area = int(area)
                        if not 1 <= area <= 16:
                            await ctx.send(f'There is no area {area}.')
                            return
                    else:
                        await ctx.send(f'There is no area {area}.')
                        return
                original_item = item
                if item in global_data.item_aliases:
                    item = global_data.item_aliases[item]

                if not item in items:
                    await ctx.send(f'This command does not support an item called `{original_item}`, sorry.')
                    return
            else:
                await ctx.send(error_syntax)
                return
        else:
            await ctx.send(
                f'This command converts your inventory into a single material.\n\n'
                f'{error_syntax}'
            )
            return

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg i` (or `abort` to abort)')
            answer_user_enchanter = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_user_enchanter.content
            answer = answer.lower()
            if answer in ('rpg i','rpg inventory','rpg inv',):
                answer_bot_inv = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    inventory = str(answer_bot_inv.embeds[0].fields).lower()
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                fish = await global_data.inventory_get(inventory, 'normie fish')
                fishgolden = await global_data.inventory_get(inventory, 'golden fish')
                fishepic = await global_data.inventory_get(inventory, 'epic fish')
                log = await global_data.inventory_get(inventory, 'wooden log')
                logepic = await global_data.inventory_get(inventory, 'epic log')
                logsuper = await global_data.inventory_get(inventory, 'super log')
                logmega = await global_data.inventory_get(inventory, 'mega log')
                loghyper = await global_data.inventory_get(inventory, 'hyper log')
                logultra = await global_data.inventory_get(inventory, 'ultra log')
                apple = await global_data.inventory_get(inventory, 'apple')
                banana = await global_data.inventory_get(inventory, 'banana')
                ruby = await global_data.inventory_get(inventory, 'ruby')
                potato = await global_data.inventory_get(inventory, 'potato')
                carrot = await global_data.inventory_get(inventory, 'carrot')
                bread = await global_data.inventory_get(inventory, 'bread')
                cookie = await global_data.inventory_get(inventory, 'arena cookie')
                wolfskin = await global_data.inventory_get(inventory, 'wolf skin')
                zombieeye = await global_data.inventory_get(inventory, 'zombie eye')
                unicornhorn = await global_data.inventory_get(inventory, 'unicorn horn')
                mermaidhair = await global_data.inventory_get(inventory, 'mermaid hair')
                chip = await global_data.inventory_get(inventory, 'chip')
                dragonscale = await global_data.inventory_get(inventory, 'dragon scale')
            elif (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send('Wrong input. Aborting.')
                return
        except asyncio.TimeoutError as error:
            await ctx.send(f'**{ctx.author.name}**, couldn\'t find your inventory, RIP.')
            return

        traderate_data = await database.get_traderate_data(ctx, area)
        fish_rate = traderate_data[1]
        apple_rate = traderate_data[2]
        ruby_rate = traderate_data[3]

        # Calculate logs
        if item == 'log':
            loghyper_calc = loghyper + (logultra * 8)
            logmega_calc = logmega + (loghyper_calc * 8)
            logsuper_calc = logsuper + (logmega_calc * 8)
            logepic_calc = logepic + (logsuper_calc * 8)
            log_calc = log + (logepic_calc * 20)
            fishgolden_calc = fishgolden + (fishepic * 80)
            fish_calc = fish + (fishgolden_calc * 12)
            apple_calc = apple + (banana * 12)
            log_calc = log_calc + (fish_calc * fish_rate)

            if area in (1,2):
                log_calc = log_calc + (apple_calc * 3)
                log_calc = log_calc + (ruby * 450)
            elif area in (3,4):
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * 450)
            else:
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * ruby_rate)

            result_value = log_calc
            result_item = f'{emojis.LOG} wooden logs'

        # Calculate epic logs
        if item == 'epic log':
            loghyper_calc = loghyper + (logultra * 8)
            logmega_calc = logmega + (loghyper_calc * 8)
            logsuper_calc = logsuper + (logmega_calc * 8)
            fishgolden_calc = fishgolden + (fishepic * 80)
            fish_calc = fish + (fishgolden_calc * 12)
            apple_calc = apple + (banana * 12)
            log_calc = log + (fish_calc * fish_rate)

            if area in (1,2):
                log_calc = log_calc + (apple_calc * 3)
                log_calc = log_calc + (ruby * 450)
            elif area in (3,4):
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * 450)
            else:
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * ruby_rate)

            logepic_calc = logepic + (logsuper_calc * 8) + log_calc // 25

            result_value = logepic_calc
            result_item = f'{emojis.LOG_EPIC} EPIC logs'

        # Calculate super logs
        if item == 'super log':
            loghyper_calc = loghyper + (logultra * 8)
            logmega_calc = logmega + (loghyper_calc * 8)
            fishgolden_calc = fishgolden + (fishepic * 80)
            fish_calc = fish + (fishgolden_calc * 12)
            apple_calc = apple + (banana * 12)
            log_calc = log + (fish_calc * fish_rate)

            if area in (1,2):
                log_calc = log_calc + (apple_calc * 3)
                log_calc = log_calc + (ruby * 450)
            elif area in (3,4):
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * 450)
            else:
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * ruby_rate)

            logepic_calc = logepic + log_calc // 25
            logsuper_calc = logsuper + (logmega_calc * 8) + (logepic_calc // 10)

            result_value = logsuper_calc
            result_item = f'{emojis.LOG_SUPER} SUPER logs'

        # Calculate mega logs
        if item == 'mega log':
            loghyper_calc = loghyper + (logultra * 8)
            fishgolden_calc = fishgolden + (fishepic * 80)
            fish_calc = fish + (fishgolden_calc * 12)
            apple_calc = apple + (banana * 12)
            log_calc = log + (fish_calc * fish_rate)

            if area in (1,2):
                log_calc = log_calc + (apple_calc * 3)
                log_calc = log_calc + (ruby * 450)
            elif area in (3,4):
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * 450)
            else:
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * ruby_rate)

            logepic_calc = logepic + log_calc // 25
            logsuper_calc = logsuper + (logepic_calc // 10)
            logmega_calc = logmega + (loghyper_calc * 8) + (logsuper_calc // 10)

            result_value = logmega_calc
            result_item = f'{emojis.LOG_MEGA} MEGA logs'

        # Calculate hyper logs
        if item == 'hyper log':
            fishgolden_calc = fishgolden + (fishepic * 80)
            fish_calc = fish + (fishgolden_calc * 12)
            apple_calc = apple + (banana * 12)
            log_calc = log + (fish_calc * fish_rate)

            if area in (1,2):
                log_calc = log_calc + (apple_calc * 3)
                log_calc = log_calc + (ruby * 450)
            elif area in (3,4):
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * 450)
            else:
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * ruby_rate)

            logepic_calc = logepic + log_calc // 25
            logsuper_calc = logsuper + (logepic_calc // 10)
            logmega_calc = logmega + (logsuper_calc // 10)
            loghyper_calc = loghyper + (logultra * 8) + (logmega_calc // 10)

            result_value = loghyper_calc
            result_item = f'{emojis.LOG_HYPER} HYPER logs'

        # Calculate ultra logs
        if item == 'ultra log':
            fishgolden_calc = fishgolden + (fishepic * 80)
            fish_calc = fish + (fishgolden_calc * 12)
            apple_calc = apple + (banana * 12)
            log_calc = log + (fish_calc * fish_rate)

            if area in (1,2):
                log_calc = log_calc + (apple_calc * 3)
                log_calc = log_calc + (ruby * 450)
            elif area in (3,4):
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * 450)
            else:
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * ruby_rate)

            logepic_calc = logepic + log_calc // 25
            logsuper_calc = logsuper + (logepic_calc // 10)
            logmega_calc = logmega + (logsuper_calc // 10)
            loghyper_calc = loghyper + (logmega_calc // 10)
            logultra_calc = logultra + (loghyper_calc // 10)

            result_value = logultra_calc
            result_item = f'{emojis.LOG_ULTRA} ULTRA logs'

        # Calculate normie fish
        if item == 'fish':
            fishgolden_calc = fishgolden + (fishepic * 80)
            fish_calc = fish + (fishgolden_calc * 12)
            loghyper_calc = loghyper + (logultra * 8)
            logmega_calc = logmega + (loghyper_calc * 8)
            logsuper_calc = logsuper + (logmega_calc * 8)
            logepic_calc = logepic + (logsuper_calc * 8)
            log_calc = log + (logepic_calc * 20)
            apple_calc = apple + (banana * 12)

            if area in (1,2):
                log_calc = log_calc + (apple_calc * 3)
                fish_calc = fish_calc + (ruby * 225)
            elif area in (3,4):
                log_calc = log_calc + (apple_calc * apple_rate)
                fish_calc = fish_calc + (ruby * 225)
            else:
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * ruby_rate)

            fish_calc = fish_calc + (log_calc // fish_rate)

            result_value = fish_calc
            result_item = f'{emojis.FISH} normie fish'

        # Calculate golden fish
        if item == 'golden fish':
            loghyper_calc = loghyper + (logultra * 8)
            logmega_calc = logmega + (loghyper_calc * 8)
            logsuper_calc = logsuper + (logmega_calc * 8)
            logepic_calc = logepic + (logsuper_calc * 8)
            log_calc = log + (logepic_calc * 20)
            apple_calc = apple + (banana * 12)

            if area in (1,2):
                log_calc = log_calc + (apple_calc * 3)
                fish_calc = fish + (ruby * 225)
            elif area in (3,4):
                log_calc = log_calc + (apple_calc * apple_rate)
                fish_calc = fish + (ruby * 225)
            else:
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * ruby_rate)
                fish_calc = fish

            fish_calc = fish_calc + (log_calc // fish_rate)
            fishgolden_calc = fishgolden + (fishepic * 80) + (fish_calc // 15)

            result_value = fishgolden_calc
            result_item = f'{emojis.FISH_GOLDEN} golden fish'

        # Calculate epic fish
        if item == 'epic fish':
            loghyper_calc = loghyper + (logultra * 8)
            logmega_calc = logmega + (loghyper_calc * 8)
            logsuper_calc = logsuper + (logmega_calc * 8)
            logepic_calc = logepic + (logsuper_calc * 8)
            log_calc = log + (logepic_calc * 20)
            apple_calc = apple + (banana * 12)

            if area in (1,2):
                log_calc = log_calc + (apple_calc * 3)
                fish_calc = fish + (ruby * 225)
            elif area in (3,4):
                log_calc = log_calc + (apple_calc * apple_rate)
                fish_calc = fish + (ruby * 225)
            else:
                fish_calc = fish
                log_calc = log_calc + (apple_calc * apple_rate)
                log_calc = log_calc + (ruby * ruby_rate)

            fish_calc = fish_calc + (log_calc // fish_rate)
            fishgolden_calc = fishgolden + (fish_calc // 15)
            fishepic_calc = fishepic + (fishgolden_calc // 100)

            result_value = fishepic_calc
            result_item = f'{emojis.FISH_EPIC} EPIC fish'

        # Calculate apples
        if item == 'apple':
            loghyper_calc = loghyper + (logultra * 8)
            logmega_calc = logmega + (loghyper_calc * 8)
            logsuper_calc = logsuper + (logmega_calc * 8)
            logepic_calc = logepic + (logsuper_calc * 8)
            log_calc = log + (logepic_calc * 20)
            apple_calc = apple + (banana * 12)
            fishgolden_calc = fishgolden + (fishepic * 80)
            fish_calc = fish + (fishgolden_calc * 12)
            log_calc = log_calc + (fish_calc * fish_rate)

            if area in (1,2,3,4):
                log_calc = log_calc + (ruby * 225)
            else:
                log_calc = log_calc + (ruby * ruby_rate)

            if area in (1,2):
                apple_calc = apple_calc + (log_calc // 3)
            else:
                apple_calc = apple_calc + (log_calc // apple_rate)

            result_value = apple_calc
            result_item = f'{emojis.APPLE} apples'

        # Calculate bananas
        if item == 'banana':
            loghyper_calc = loghyper + (logultra * 8)
            logmega_calc = logmega + (loghyper_calc * 8)
            logsuper_calc = logsuper + (logmega_calc * 8)
            logepic_calc = logepic + (logsuper_calc * 8)
            log_calc = log + (logepic_calc * 20)
            fishgolden_calc = fishgolden + (fishepic * 80)
            fish_calc = fish + (fishgolden_calc * 12)
            log_calc = log_calc + (fish_calc * fish_rate)

            if area in (1,2,3,4):
                log_calc = log_calc + (ruby * 225)
            else:
                log_calc = log_calc + (ruby * ruby_rate)

            if area in (1,2):
                apple_calc = apple + (log_calc // 3)
            else:
                apple_calc = apple + (log_calc // apple_rate)

            banana_calc = banana + (apple_calc // 15)

            result_value = banana_calc
            result_item = f'{emojis.BANANA} bananas'

        # Calculate rubies
        if item == 'ruby':
            loghyper_calc = loghyper + (logultra * 8)
            logmega_calc = logmega + (loghyper_calc * 8)
            logsuper_calc = logsuper + (logmega_calc * 8)
            logepic_calc = logepic + (logsuper_calc * 8)
            log_calc = log + (logepic_calc * 20)
            apple_calc = apple + (banana * 12)
            fishgolden_calc = fishgolden + (fishepic * 80)
            fish_calc = fish + (fishgolden_calc * 12)
            log_calc = log_calc + (fish_calc * fish_rate)

            if area in (1,2):
                log_calc = log_calc + (apple_calc * 3)
            else:
                log_calc = log_calc + (apple_calc * apple_rate)

            if area in (1,2,3,4):
                ruby_calc = ruby + (log_calc // 450)
            else:
                ruby_calc = ruby + (log_calc // ruby_rate)

            result_value = ruby_calc
            result_item = f'{emojis.RUBY} rubies'



        if area in (1,2):
            await ctx.send(
                f'**{ctx.author.name}**, your inventory (assuming you are in area **{area}** now) equals **{result_value:,}** {result_item}.\n\n'
                f'Note that apples and rubies were included in the calculation but can not be traded in this area.'
            )
        elif area in (3,4):
            await ctx.send(
                f'**{ctx.author.name}**, your inventory (assuming you are in area **{area}** now) equals **{result_value:,}** {result_item}.\n\n'
                f'Note that rubies were included in the calculation but can not be traded in this area.'
            )
        else:
            await ctx.send(f'**{ctx.author.name}**, your inventory (assuming you are in area **{area}** now) equals **{result_value:,}** {result_item}.')

# Initialization
def setup(bot):
    bot.add_cog(craftingCog(bot))


# --- Functions ---
async def get_item_breakdown(ctx: commands.Context, item: database.Item, amount: int, dismantle: bool = False) -> str:
    """Generate item breakdown"""
    log_total = fish_total = apple_total = 0
    breakdown = ''
    multiplier = 0.8 if dismantle else 1
    base_totals = {}

    for ingredient in item.ingredients:
        ingredient_item: database.Item = await database.get_item(ctx, ingredient.name)
        if ingredient.name == 'wooden log':
            log_total += ingredient.amount * amount * multiplier
        elif ingredient.name == 'normie fish':
            fish_total += ingredient.amount * amount * multiplier
        elif ingredient.name == 'apple':
            apple_total += ingredient.amount * amount * multiplier
        if not ingredient_item.ingredients:
            if ingredient_item.item_type not in ('log', 'fish', 'fruit'):
                base_totals[ingredient.name] = (ingredient.amount, ingredient_item.emoji)
            continue
        if ingredient_item.item_type not in ('log', 'fish', 'fruit'): continue
        current_ingredient = ingredient
        current_breakdown = ''
        current_amount = amount
        while True:
            current_amount = current_amount * current_ingredient.amount * multiplier
            if current_ingredient.name == 'wooden log':
                log_total += current_amount
            elif current_ingredient.name == 'normie fish':
                fish_total += current_amount
            elif current_ingredient.name == 'apple':
                apple_total += current_amount
            sub_item: database.Item = await database.get_item(ctx, current_ingredient.name)
            if current_breakdown == '':
                current_breakdown = f'> {int(current_amount):,} {sub_item.emoji}'
            else:
                current_breakdown = f'{current_breakdown} ➜ {int(current_amount):,} {sub_item.emoji}'
            if not sub_item.ingredients:
                breakdown = f'{breakdown}\n{current_breakdown}'
                break
            current_ingredient = sub_item.ingredients[0] # If he ever makes more sub ingredients, this will break

    message = ''
    if '➜' in breakdown:
        if dismantle:
            message = f'**Full breakdown**\n{breakdown.strip()}'
            return message.strip()
        message = f'**Ingredients breakdown**\n{breakdown.strip()}'
        message = f'**Full breakdown**\n{breakdown.strip()}'
        message = f'{message}\n\n**Base materials total**'
        message = message.strip()
        if (log_total > 0 or fish_total > 0 or apple_total > 0) and not dismantle:
            if apple_total > 0: base_totals['apple'] = (apple_total, emojis.APPLE)
            if fish_total > 0: base_totals['normie fish'] = (fish_total, emojis.FISH)
            if log_total > 0: base_totals['wooden log'] = (log_total, emojis.LOG)
        for name, amount_emoji in sorted(base_totals.items(), key=lambda item: item[1][0]):
            message = f'{message}\n> {amount_emoji[0]:,} {amount_emoji[1]} `{name}`'

    return message.strip()


# --- Embeds ---
# Enchants
async def embed_enchants(prefix):

    buffs = (
        f'{emojis.BP} **Normie** - 5% buff\n'
        f'{emojis.BP} **Good** - 15% buff\n'
        f'{emojis.BP} **Great** - 25% buff\n'
        f'{emojis.BP} **Mega** - 40% buff\n'
        f'{emojis.BP} **Epic** - 60% buff\n'
        f'{emojis.BP} **Hyper** - 70% buff\n'
        f'{emojis.BP} **Ultimate** - 80% buff\n'
        f'{emojis.BP} **Perfect** - 90% buff\n'
        f'{emojis.BP} **EDGY** - 95% buff\n'
        f'{emojis.BP} **ULTRA-EDGY** - 100% buff\n'
        f'{emojis.BP} **OMEGA** - 125% buff, unlocked in {emojis.TIME_TRAVEL} TT 1\n'
        f'{emojis.BP} **ULTRA-OMEGA** - 150% buff, unlocked in {emojis.TIME_TRAVEL} TT 3\n'
        f'{emojis.BP} **GODLY** - 200% buff, unlocked in {emojis.TIME_TRAVEL} TT 5'
    )

    commands_tiers = (
        f'{emojis.BP} `enchant` - area 2+, rolls `1 * TT multiplier` enchants\n'
        f'{emojis.BP} `refine` - area 7+, rolls `10 * TT multiplier` enchants\n'
        f'{emojis.BP} `transmute` - area 13+, rolls `100 * TT multiplier` enchants\n'
        f'{emojis.BP} `transcend` - area 15+, rolls `1,000 * TT multiplier` enchants'
    )

    how_enchanting_works = (
        f'{emojis.BP} Each command rolls a certain amount of enchants\n'
        f'{emojis.BP} The resulting enchant is the highest enchant that got rolled\n'
        f'{emojis.BP} Higher command tiers increase the amount of rolls\n'
    )

    enchant_cost = (
        f'{emojis.BP} The enchant cost is `1k * amount of rolls * area * TT multiplier`\n'
    )

    multiplier = (
        f'{emojis.BP} The multiplier increases the amount of rolls of all command tiers\n'
        f'{emojis.BP} The multiplier increases with {emojis.TIME_TRAVEL} TT\n'
        f'{emojis.BP} More rolls also means higher cost!\n'
        f'{emojis.BP} You can check your current multiplier with `rpg time travel`\n'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'ENCHANTS',
        description = (
            f'Enchants buff either AT or DEF (sword enchants buff AT, armor enchants buff DEF). Enchants buff your **overall** stats.\n'
            f'The chance to get better enchants can be increased by leveling up the enchanter profession and having a {emojis.HORSE_T8} T8+ horse.\n'
            f'See the [Wiki](https://epic-rpg.fandom.com/wiki/Enchant) for **base** chance estimates.'
        )
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='POSSIBLE ENCHANTS', value=buffs, inline=False)
    embed.add_field(name='HOW ENCHANTING WORKS', value=how_enchanting_works, inline=False)
    embed.add_field(name='COMMAND TIERS', value=commands_tiers, inline=False)
    embed.add_field(name='ENCHANT COST', value=enchant_cost, inline=False)
    embed.add_field(name='TT MULTIPLIER', value=multiplier, inline=False)
    return embed

# Monster drops
async def embed_drops(prefix):

    wolfskin = (
        f'{emojis.BP} Areas: 1~2\n'
        f'{emojis.BP} Source: {emojis.MOB_WOLF}\n'
        f'{emojis.BP} Value: 500\n'
        f'{emojis.BLANK}'
    )

    zombieeye = (
        f'{emojis.BP} Areas: 3~4\n'
        f'{emojis.BP} Source: {emojis.MOB_ZOMBIE}\n'
        f'{emojis.BP} Value: 2\'000\n'
        f'{emojis.BLANK}'
    )

    unicornhorn = (
        f'{emojis.BP} Areas: 5~6\n'
        f'{emojis.BP} Source: {emojis.MOB_UNICORN}\n'
        f'{emojis.BP} Value: 7\'500\n'
        f'{emojis.BLANK}'
    )

    mermaidhair = (
        f'{emojis.BP} Areas: 7~8\n'
        f'{emojis.BP} Source: {emojis.MOB_MERMAID}\n'
        f'{emojis.BP} Value: 30\'000\n'
        f'{emojis.BLANK}'
    )

    chip = (
        f'{emojis.BP} Areas: 9~10\n'
        f'{emojis.BP} Source: {emojis.MOB_KILLER_ROBOT}\n'
        f'{emojis.BP} Value: 100\'000\n'
        f'{emojis.BLANK}'
    )

    dragonscale = (
        f'{emojis.BP} Areas: 11~15\n'
        f'{emojis.BP} Source: {emojis.MOB_BABY_DRAGON}{emojis.MOB_TEEN_DRAGON}{emojis.MOB_ADULT_DRAGON}{emojis.MOB_OLD_DRAGON}\n'
        f'{emojis.BP} Value: 250\'000\n'
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
        f'{emojis.BP} To calculate your current drop chance, use `{prefix}dropchance`\n{emojis.BLANK}'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'MONSTER DROPS',
        description = (
            f'These items drop when using `hunt`, `hunt together` or when opening lootboxes.\n'
            f'You can go back to previous areas with `rpg area`.\n'
            f'{emojis.BLANK}'
        )
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'WOLF SKIN {emojis.WOLF_SKIN}', value=wolfskin, inline=True)
    embed.add_field(name=f'ZOMBIE EYE {emojis.ZOMBIE_EYE}', value=zombieeye, inline=True)
    embed.add_field(name=f'UNICORN HORN {emojis.UNICORN_HORN}', value=unicornhorn, inline=True)
    embed.add_field(name=f'MERMAID HAIR {emojis.MERMAID_HAIR}', value=mermaidhair, inline=True)
    embed.add_field(name=f'CHIP {emojis.CHIP}', value=chip, inline=True)
    embed.add_field(name=f'DRAGON SCALE {emojis.DRAGON_SCALE}', value=dragonscale, inline=True)
    embed.add_field(name='DROP CHANCE', value=chance, inline=False)

    return embed

