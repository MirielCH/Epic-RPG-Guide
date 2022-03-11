# misc.py

import asyncio
from decimal import Decimal, ROUND_HALF_UP

import discord
from discord.ext import commands

import database
from resources import emojis
from resources import settings
from resources import functions


# Miscellaneous commands (cog)
class miscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "duels" - Returns all duelling weapons
    @commands.command(aliases=('duel','duelling','dueling','duelweapons','duelweapon',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def duels(self, ctx):
        embed = await embed_duels(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "codes" - Redeemable codes
    @commands.command(aliases=('code',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def codes(self, ctx):
        codes = await database.get_codes(ctx)
        embed = await embed_codes(ctx.prefix, codes)
        await ctx.send(embed=embed)

    # Command "coolness" - Coolness guide
    @commands.command(aliases=('cool',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def coolness(self, ctx):
        embed = await embed_coolness(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "badges" - Badge guide
    @commands.command(aliases=('badge',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def badges(self, ctx):
        embed = await embed_badges(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "farm" - Farming guide
    @commands.command(aliases=('farming',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def farm(self, ctx):
        embed = await embed_farm(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "start" - Starter guide
    @commands.command(aliases=('starting','startguide','starterguide','startingguide'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def start(self, ctx):
        embed = await embed_start(ctx.prefix)
        await ctx.send(embed=embed)

    @commands.command(aliases=('ultr',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def ultraining(self, ctx: commands.Context, *args: str) -> None:
        """Ultraining guide"""
        embed = await embed_ultraining(ctx.prefix)
        await ctx.send(embed=embed)

    @commands.command(aliases=('ucalc','ultrcalc','ultrainingcalc','stage'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def uc(self, ctx: commands.Context, *args: str) -> None:
        """Ultraining stage calculator"""
        prefix = ctx.prefix
        message_syntax = f'The command syntax is `{prefix}uc [stage]`\nExample: `{prefix}uc 150`'
        if not args:
            await ctx.send(f'This command calculates EPIC NPC stats in a certain ultraining stage.\n{message_syntax}')
            return

        arg, *_ = args
        try:
            stage = int(arg)
        except:
            await ctx.send(f'Invalid stage. The stage has to be a number.\n\n{message_syntax}')
            return
        if stage < 1:
            await ctx.send(f'Why do people always try {emojis.SUS}')
            return
        if stage > 63_096:
            await ctx.send(f'The current maximum possible stage is 63,096 which equals 100% EPIC NPC strength.')
            return
        npc_at_base = 5 * (stage ** 1.25)
        npc_def_base = 6 * (stage ** 1.25)

        answer = (
            f'Estimated EPIC NPC stats at stage **{stage:,}**:\n'
            f'{emojis.STAT_AT} AT: **{round(npc_at_base * 0.9):,} - {round(npc_at_base * 1.1):,}**\n'
            f'{emojis.STAT_DEF} DEF: **{round(npc_def_base * 0.9):,} - {round(npc_def_base * 1.1):,}**\n'
        )
        await ctx.send(answer)

    # Command "calc" - Simple calculator
    @commands.command(aliases=('calculate','calculator','math'))
    @commands.bot_has_permissions(send_messages=True)
    async def calc(self, ctx, *args):
        def formatNumber(num):
            if num % 1 == 0:
                return int(num)
            else:
                num = num.quantize(Decimal('1.1234567890'), rounding=ROUND_HALF_UP)
                return num

        if args:
            calculation = ''
            allowedchars = set('1234567890.-+/*%()')

            for arg in args:
                calculation = f'{calculation}{arg}'

            if set(calculation).issubset(allowedchars):
                if '**' in calculation:
                    await ctx.send(
                        f'Invalid characters. Please only use numbers and supported operators.\n'
                        f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
                    )
                    return
            else:
                await ctx.send(
                    f'Invalid characters. Please only use numbers and supported operators.\n'
                    f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
                )
                return

            # Parse open the calculation, convert all numbers to float and store it as a list
            # This is necessary because Python has the annoying habit of allowing infinite integers which can completely lockup a system. Floats have overflow protection.
            pos = 1
            calculation_parsed = []
            number = ''
            last_char_was_operator = False # Not really accurate name, I only use it to check for *, % and /. Multiple + and - are allowed.
            last_char_was_number = False
            calculation_sliced = calculation
            try:
                while pos != len(calculation) + 1:
                    slice = calculation_sliced[0:1]
                    allowedcharacters = set('1234567890.-+/*%()')
                    if set(slice).issubset(allowedcharacters):
                        if slice.isnumeric():
                            if last_char_was_number:
                                number = f'{number}{slice}'
                            else:
                                number = slice
                                last_char_was_number = True
                            last_char_was_operator = False
                        else:
                            if slice == '.':
                                if number == '':
                                    number = f'0{slice}'
                                    last_char_was_number = True
                                else:
                                    number = f'{number}{slice}'
                            else:
                                if number != '':
                                    calculation_parsed.append(Decimal(float(number)))
                                    number = ''

                                if slice in ('*','%','/'):
                                    if last_char_was_operator == True:
                                        await ctx.send(
                                            f'Error while parsing your input. Please check your equation.\n'
                                            f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
                                        )
                                        return
                                    else:
                                        calculation_parsed.append(slice)
                                        last_char_was_operator = True
                                else:
                                    calculation_parsed.append(slice)
                                    last_char_was_operator = False
                                last_char_was_number = False
                    else:
                        await ctx.send(
                            f'Error while parsing your input. Please check your equation.\n'
                            f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
                        )
                        return

                    calculation_sliced = calculation_sliced[1:]
                    pos += 1
                else:
                    if number != '':
                        calculation_parsed.append(Decimal(float(number)))
            except:
                await ctx.send(
                    f'Error while parsing your input. Please check your equation.\n'
                    f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
                )
                return

            # Reassemble and execute calculation
            calculation_reassembled = ''
            for slice in calculation_parsed:
                calculation_reassembled = f'{calculation_reassembled}{slice}'

            try:
                result = eval(calculation_reassembled)
                result = Decimal(eval(calculation_reassembled))
                result = formatNumber(result)
                if isinstance(result, int):
                    result = f'{result:,}'
                else:
                    result = f'{result:,}'.rstrip('0').rstrip('.')
                if not len(result) > 2000:
                    await ctx.send(result)
                    return
                else:
                    await ctx.send('Well. Whatever you calculated, the result is too long to display. GG.')
                    return
            except:
                await ctx.send(
                    f'Well, _that_ didn\'t calculate to anything useful.\n'
                    f'What were you trying to do there? :thinking:'
                )
                return
        else:
            await ctx.send(
                f'The command syntax is `{ctx.prefix}{ctx.invoked_with} [calculation]`\n'
                f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
            )

    # Command "tip" - Returns a random tip
    @commands.command(aliases=('tips',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def tip(self, ctx, *args):

        if args:
            if len(args)==1:
                id = args[0]
                if id.isnumeric():
                    id = int(id)
                    tip = await database.get_tip(ctx, id)
                else:
                    tip = await database.get_tip(ctx)
            else:
                tip = await database.get_tip(ctx)
        else:
            tip = await database.get_tip(ctx)

        embed = discord.Embed(
            color = settings.EMBED_COLOR,
            title = 'TIP',
            description = tip[0]
        )

        await ctx.send(embed=embed)

    # Command "coincap" - Calculate the coin cap
    @commands.command(aliases=('coin',))
    @commands.bot_has_permissions(send_messages=True, external_emojis=True)
    async def coincap(self, ctx, *args):

        """
        await ctx.send(
                f'**{ctx.author.name}**, this command is disabled because the known formula was confirmed to be wrong.\n'
                f'The correct formula is currently unkown.'
            )
        """

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s profile') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        prefix = ctx.prefix

        error_syntax = (
            f'The command syntax is `{prefix}coincap [tt] [max area]`\n'
            f'You can also use `{prefix}coincap` and let me read your profile.\n'
            f'Examples: `{prefix}coincap tt5 a5`, `{prefix}coincap 8 2`'
        )

        user_tt = None
        user_area = None

        if args:
            if args[0].lower() == 'cap':
                args = list(args)
                args.pop(0)
            if len(args) != 2:
                await ctx.send(error_syntax)
                return
            arg1 = args[0].lower().replace('tt','')
            arg2 = args[1].lower().replace('a','')
            if not arg1.isnumeric() or not arg2.isnumeric():
                await ctx.send(error_syntax)
                return
            user_tt = int(arg1)
            area_no = int(arg2)
            if not 0 <= user_tt <= 999:
                await ctx.send(f'Uuuuhhhhhh..... you sure about that time travel count?\n\n{error_syntax}')
                return
            if not 1 <= area_no <= 20:
                await ctx.send(f'What area is that supposed to be?\n\n{error_syntax}')
                return

        if user_tt is None:
            try:
                await ctx.send(
                    f'**{ctx.author.name}**, please type `rpg p` (or `abort` to abort).\n\n'
                    f'Note: This does **not** work with profile backgrounds.\n'
                    f'Please remove your background or use `{ctx.prefix}coincap [tt] [max area]` instead.'
                )
                answer_user_at = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_at.content
                answer = answer.lower()
                if (answer == 'rpg p') or (answer == 'rpg profile') or (answer == 'rpg stats'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        profile = str(answer_bot_at.embeds[0].fields[0])
                    except:
                        try:
                            profile = str(answer_bot_at.embeds[0].fields[0])
                        except:
                            await ctx.send(
                                f'Whelp, something went wrong here, sorry.\n'
                                f'If you have a profile background, remove it or use '
                                f'`{ctx.prefix}coincap [tt] [max area]` instead.'
                            )
                            return
                    start_area = profile.find('(Max:') + 6
                    end_area = profile.find(')', start_area)
                    user_area = profile[start_area:end_area]
                    area_no = int(user_area)
                    if profile.find('Time travels') > -1:
                        start_tt = profile.find('Time travels**') + 16
                        end_tt = profile.find('\',', start_tt)
                        user_tt = profile[start_tt:end_tt]
                        user_tt = int(user_tt)
                    else:
                        user_tt = 0
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profile, RIP.')
                return
        coin_cap = pow(user_tt, 4) * 500_000_000 + pow(area_no, 2) * 100_000
        if area_no == 1: coin_cap += 1
        await ctx.send(
            f'**{ctx.author.name}**, the coin cap for **TT {user_tt}**, **area {area_no}** is '
            f'**{coin_cap:,}** {emojis.COIN} coins.\n'
            f'You can not receive coins with `give`, `multidice` or `miniboss` if you would exceed this cap.'
        )

# Initialization
def setup(bot):
    bot.add_cog(miscCog(bot))



# --- Embeds ---
# Duels
async def embed_duels(prefix):

    weapons = (
        f'{emojis.BP} {emojis.DUEL_AT}{emojis.DUEL_AT} - **AT**\n'
        f'{emojis.BP} {emojis.DUEL_DEF}{emojis.DUEL_DEF} - **DEF**\n'
        f'{emojis.BP} {emojis.DUEL_LIFE}{emojis.DUEL_LIFE} - **LIFE**\n'
        f'{emojis.BP} {emojis.DUEL_LEVEL}{emojis.DUEL_LEVEL} - **LEVEL**\n'
        f'{emojis.BP} {emojis.DUEL_COINS}{emojis.DUEL_COINS} - **Coins** (incl. bank account)\n'
        f'{emojis.BP} {emojis.DUEL_GEAR}{emojis.DUEL_GEAR} - **Gear** (both sword and armor)\n'
        f'{emojis.BP} {emojis.DUEL_ENCHANTS}{emojis.DUEL_ENCHANTS} - **Enchants** (both sword and armor)'
    )

    randomness = (
        f'{emojis.BP} Every duel score gets multiplied by 0.75 ~ 1.25\n'
        f'{emojis.BP} Thus the duel outcome can be highly unexpected'
    )

    note = (
        f'{emojis.BP} Unless you are really rich, don\'t choose coins/cards.\n'
        f'{emojis.BP} If you don\'t choose a weapon, your opponent will automatically win.\n'
    )


    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'DUELS',
        description = 'Winning a duel depends on the chosen weapon and some luck.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='DUELLING WEAPONS', value=weapons, inline=False)
    embed.add_field(name='RANDOMNESS', value=randomness, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Redeemable codes
async def embed_codes(prefix, codes):

    temporary_value = ''
    temporary_value_2 = ''
    permanent_value = ''
    second_event_field = False

    for code in codes:
        temporary_code = code[2]
        if temporary_code == 'True':
            if second_event_field:
                temporary_value_2 = f'{temporary_value_2}\n{emojis.BP} `{code[0]}`{emojis.BLANK}{code[1]}'
            else:
                temporary_value_check = f'{temporary_value}\n{emojis.BP} `{code[0]}`{emojis.BLANK}{code[1]}'
                if len(temporary_value_check) > 1024:
                    temporary_value_2 = f'{emojis.BP} `{code[0]}`{emojis.BLANK}{code[1]}'
                    second_event_field = True
                else:
                    temporary_value = f'{temporary_value}\n{emojis.BP} `{code[0]}`{emojis.BLANK}{code[1]}'
        else:
            permanent_value = f'{permanent_value}\n{emojis.BP} `{code[0]}`{emojis.BLANK}{code[1]}'

    if permanent_value == '': permanent_value = f'{emojis.BP} No codes currently known'

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'REDEEMABLE CODES',
        description = (
            f'Use these codes with `rpg code` to get some free goodies.\n'
            f'Every code can only be redeemed once.'
        )
    )

    embed.set_footer(text=await functions.default_footer(prefix))

    if not temporary_value == '':
        embed.add_field(name='EVENT CODES', value=temporary_value, inline=False)
    if second_event_field:
        embed.add_field(name='MORE EVENT CODES', value=temporary_value_2, inline=False)
    embed.add_field(name='PERMANENT CODES', value=permanent_value, inline=False)

    return embed

# Coolness
async def embed_coolness(prefix):

    usage = (
        f'{emojis.BP} Unlocks cosmetic only profile badges (see `{prefix}badges`)\n'
        f'{emojis.BP} You need at least 2,000 coolness for dungeon 15-2 (see `{prefix}d15-2`)'
    )

    req = f'{emojis.BP} Unlocks when you reach area 12 in {emojis.TIME_TRAVEL}TT 1'

    howtoget = (
        f'{emojis.BP} `ultraining` awards 2 coolness per stage (see `{prefix}ultr`)\n'
        f'{emojis.BP} Do an adventure with full HP and survive with 1 HP\n'
        f'{emojis.BP} Open {emojis.LB_OMEGA} OMEGA and {emojis.LB_GODLY} GODLY lootboxes\n'
        f'{emojis.BP} Get {emojis.LOG_HYPER} HYPER or {emojis.LOG_ULTRA} ULTRA logs from work commands\n'
        f'{emojis.BP} Forge ULTRA-EDGY or higher gear\n'
        f'{emojis.BP} Ascend a pet\n'
        f'{emojis.BP} Do other \'cool\' actions that are currently unknown'
    )

    note = (
        f'{emojis.BP} You don\'t lose coolness when you time travel\n'
        f'{emojis.BP} You can get coolness in every area once it\'s unlocked\n'
        f'{emojis.BP} If you have 100+, you get less (except from `ultraining`)\n'
        f'{emojis.BP} You can check your coolness by using `ultraining p`\n'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'COOLNESS {emojis.STAT_COOLNESS}',
        description = 'Coolness is a stat you start collecting once you reach area 12.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='REQUIREMENTS', value=req, inline=False)
    embed.add_field(name='HOW TO GET COOLNESS', value=howtoget, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Badges
async def embed_badges(prefix):

    badges_coolness = (
        f'{emojis.BP} {emojis.BADGE_C1} : Unlocked with 1 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C100} : Unlocked with 100 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C200} : Unlocked with 200 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C500} : Unlocked with 500 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C1000} : Unlocked with 1,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C2000} : Unlocked with 2,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C5000} : Unlocked with 5,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C10000} : Unlocked with 10,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C20000} : Unlocked with 20,000 {emojis.STAT_COOLNESS} coolness\n'
    )

    badges_achievements = (
        f'{emojis.BP} {emojis.BADGE_A10} : Unlocked with 10 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A25} : Unlocked with 25 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A75} : Unlocked with 75 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A125} : Unlocked with 125 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A175} : Unlocked with 175 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A225} : Unlocked with 225 achievements\n'
    )

    badges_other = (
        f'{emojis.BP} {emojis.BADGE_AREA15} : Unlocked by reaching area 15 ({emojis.TIME_TRAVEL} TT 10)\n'
        f'{emojis.BP} {emojis.BADGE_TOP} : Unlocked by beating D15-2 and reaching the TOP\n'
        f'{emojis.BP} {emojis.BADGE_EPIC_NPC} : Unlocked by beating the "final" dungeon in the TOP\n'
        f'{emojis.BP} {emojis.BADGE_OMEGA} : Unlock requirements unknown\n'
        f'{emojis.BP} {emojis.BADGE_GODLY} : Unlock requirements unknown\n'
    )

    howtouse = (
        f'{emojis.BP} Use `rpg badge list` to get the ID of the badges you want\n'
        f'{emojis.BP} Use `rpg badge claim [ID]` to claim a badge\n'
        f'{emojis.BP} Use `rpg badge select [ID]` to activate or deactivate a badge'
    )

    note = (
        f'{emojis.BP} You can have 3 badges active (5 with a {emojis.HORSE_T10} T10 horse)\n'
        f'{emojis.BP} You can only claim badges you have unlocked\n'
        f'{emojis.BP} If you don\'t know how to get coolness, see `{prefix}coolness`'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'BADGES',
        description = 'Badges are cosmetic only profile decorations.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='ACHIEVEMENT BADGES', value=badges_achievements, inline=False)
    embed.add_field(name='COOLNESS BADGES', value=badges_coolness, inline=False)
    embed.add_field(name='OTHER BADGES', value=badges_other, inline=False)
    embed.add_field(name='HOW TO USE', value=howtouse, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Farming
async def embed_farm(prefix):

    planting_normal = (
        f'{emojis.BP} Use `rpg farm` to plant {emojis.SEED} seeds. Buy seeds in the shop for 4,000 coins.\n'
        f'{emojis.BP} This gives you XP and either {emojis.BREAD} bread, {emojis.CARROT} carrots or {emojis.POTATO} potatoes\n'
        f'{emojis.BP} You have a 4% chance to receive special seeds (see below)\n'
        f'{emojis.BP} The cooldown of the command is 10m (donor reduction applies)'
    )

    planting_special = (
        f'{emojis.BP} There are three special seeds: {emojis.SEED_BREAD} bread, {emojis.SEED_CARROT} carrot and {emojis.SEED_POTATO} potato seed\n'
        f'{emojis.BP} You can plant them with `rpg farm [type]` (e.g. `rpg farm carrot`)\n'
        f'{emojis.BP} The crop will be the same type (e.g. a {emojis.SEED_CARROT} carrot seed gives you {emojis.CARROT} carrots)\n'
        f'{emojis.BP} You have a 65% chance to get 1 seed and a 10% chance to get 2 seeds back'
    )

    usage_bread = (
        f'{emojis.BP} {emojis.SWORD_HAIR} `Hair Sword` ➜ 4 {emojis.MERMAID_HAIR} + **220** {emojis.BREAD}\n'
        f'{emojis.BP} {emojis.ARMOR_ELECTRONICAL} `Electronical Armor` ➜ 12 {emojis.CHIP} + 1 {emojis.LOG_HYPER} + **180** {emojis.BREAD}\n'
        f'{emojis.BP} {emojis.FOOD_CARROT_BREAD} `Carrot Bread` (+1 Level) ➜ **1** {emojis.BREAD} + 160 {emojis.CARROT}\n'
        f'{emojis.BP} Can be sold for 3,000 coins and 3 merchant XP\n'
        f'{emojis.BP} Heals the player and gives a temporary +5 LIFE when eaten (`rpg eat bread`)'
    )

    usage_carrot = (
        f'{emojis.BP} {emojis.FOOD_CARROT_BREAD} `Carrot Bread` (+1 Level) ➜ 1 {emojis.BREAD} + **160** {emojis.CARROT}\n'
        f'{emojis.BP} {emojis.FOOD_ORANGE_JUICE} `Orange Juice` (+3 AT, +3 DEF) ➜ **320** {emojis.CARROT}\n'
        f'{emojis.BP} {emojis.FOOD_CARROTATO_CHIPS} `Carrotato Chips` (+25 random profession XP) ➜ 80 {emojis.POTATO} + **80** {emojis.CARROT}\n'
        f'{emojis.BP} Can be sold for 2,500 coins and 3 merchant XP\n'
        f'{emojis.BP} Can be used to change the horse name with `rpg horse feed`'
    )

    usage_potato = (
        f'{emojis.BP} {emojis.SWORD_RUBY} `Ruby Sword` ➜ 4 {emojis.RUBY} + 1 {emojis.LOG_MEGA} + **36** {emojis.POTATO}\n'
        f'{emojis.BP} {emojis.ARMOR_RUBY} `Ruby Armor` ➜ 7 {emojis.RUBY} + 4 {emojis.UNICORN_HORN} + **120** {emojis.POTATO} + 2 {emojis.LOG_MEGA}\n'
        f'{emojis.BP} {emojis.SWORD_ELECTRONICAL} `Electronical Sword` ➜ 8 {emojis.CHIP} + 1 {emojis.LOG_MEGA} + **140** {emojis.POTATO}\n'
        f'{emojis.BP} {emojis.SWORD_WATERMELON} `Watermelon Sword` ➜ 1 {emojis.WATERMELON} + **10** {emojis.POTATO}\n'
        f'{emojis.BP} {emojis.FOOD_CARROTATO_CHIPS} `Carrotato Chips` (+25 random profession XP) ➜ **80** {emojis.POTATO} + 80 {emojis.CARROT}\n'
        f'{emojis.BP} Can be sold for 2,000 coins and 3 merchant XP'
    )

    stt_score = (
        f'{emojis.BP} 25 {emojis.BREAD} bread = 1 score\n'
        f'{emojis.BP} 30 {emojis.CARROT} carrots = 1 score\n'
        f'{emojis.BP} 35 {emojis.POTATO} potatoes = 1 score\n'
    )

    what_to_plant = (
        f'{emojis.BP} If you want to cook food for levels or stats: {emojis.CARROT} carrots\n'
        f'{emojis.BP} If you want to get more coins or a higher STT score: {emojis.BREAD} bread\n'
        f'{emojis.BP} If you want to flex potatoes for some reason: {emojis.POTATO} potatoes'
    )

    note = (
        f'{emojis.BP} Farming is unlocked in area 4\n'
        f'{emojis.BP} The command can be used in area 1+ when ascended\n'
        f'{emojis.BP} The amount of items you gain increases with your TT\n'
        f'{emojis.BP} You can not farm in the TOP'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'FARMING',
        description = f'It ain\'t much, but it\'s honest work.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='PLANTING NORMAL SEEDS', value=planting_normal, inline=False)
    embed.add_field(name='PLANTING SPECIAL SEEDS', value=planting_special, inline=False)
    embed.add_field(name='BREAD USAGE', value=usage_bread, inline=False)
    embed.add_field(name='CARROT USAGE', value=usage_carrot, inline=False)
    embed.add_field(name='POTATO USAGE', value=usage_potato, inline=False)
    embed.add_field(name='STT SCORE', value=stt_score, inline=False)
    embed.add_field(name='WHAT TO FARM?', value=what_to_plant, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed


# Starter guide
async def embed_start(prefix):

    goal = (
        f'The goal is to advance until you reach your highest reachable area. At that point you can time travel.\n'
        f'Think of this as new game+. This resets your progress but unlocks more of the game. For more information see `{prefix}tt`.\n'
        f'To check out the available commands in this game, use `rpg start` and `rpg help`.'
    )

    areas_dungeons = (
        f'You advance by moving through areas. You can check what you should do in each area in the area guides (see `{prefix}areas`).\n'
        f'To leave an area and advance to the next one you have to beat the dungeon for that area (so to leave area 1 you do dungeon 1).\n'
        f'Dungeons 1 to 9 are simple tank and spank affairs, there is no gear check. So, if needed, you can enter them undergeared and get carried.\n'
        f'**This does not work for dungeons 10+**. To enter those you **need** to have certain gear.'
    )

    first_run = (
        f'Your first run is called TT0 (time travel 0) because you haven\'t time traveled yet. In TT0 you need to reach area 11 which means you need to beat dungeon 10.\n'
        f'Now, as mentioned, D10 has gear requirements, so you can not cheese that dungeon, you **need** to craft the following gear:\n'
        f'{emojis.SWORD_EDGY} EDGY Sword (requires 1 {emojis.LOG_ULTRA} ULTRA log)\n'
        f'{emojis.ARMOR_EDGY} EDGY Armor (requires a lot of mob drops)\n'
        f'The ULTRA log needed for the sword equals 250,000 wooden logs and the mob drops for the armor are pretty rare (see `{prefix}drops`).\n'
        f'This means that your main goal in TT0 is to farm enough materials to be able to craft this shiny EDGY gear.'
    )

    grinding_trades = (
        f'Grinding all those materials takes time, so you want to do this smartly.\n'
        f'Trade rates are the single most important thing in this game to help you saving time. Every area has different trade rates, so every time you advance, your trade rates change (see `{prefix}trr`). You can **not** go back to earlier trade rates, these are tied to your highest unlocked area.\n'
        f'This means you can save a lot of time and materials if you farm **early** and exploit the trade rate changes to multiply your inventory. See `{prefix}trading` for more trading info.\n'
        f'In TT0 the most important area is **area 5**. You want to stay there until you have the recommended materials (see `{prefix}a5`).\n'
        f'If you do this, you will save a ton of time later on and be able to craft that EDGY gear as soon as you reach areas 9 and 10. Don\'t forget to check out the area guides for other recommendations.'
    )

    tips = (
        f'{emojis.BP} Yes, farming in area 5 is boring. But do not leave the area early, you **will** regret it.\n'
        f'{emojis.BP} Do not craft the EDGY Sword before area 10. You will lose materials if you do.'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'STARTER GUIDE',
        description = 'Welcome to EPIC RPG! This is a guide to help you out with your first run.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='GOAL OF THE GAME', value=goal, inline=False)
    embed.add_field(name='AREAS & DUNGEONS', value=areas_dungeons, inline=False)
    embed.add_field(name='YOUR FIRST RUN', value=first_run, inline=False)
    embed.add_field(name='GRINDING & TRADES', value=grinding_trades, inline=False)
    embed.add_field(name='TIPS', value=tips, inline=False)

    return embed


# Ultraining guide
async def embed_ultraining(prefix):

    how_it_works = (
        f'{emojis.BP} The EPIC NPC appears with stats depending on the stage (see `{prefix}uc`)\n'
        f'{emojis.BP} You have to choose between `ATTACK`, `BLOCK` and `ATTLOCK`\n'
        f'{emojis.BP} You win or lose depending on your stats vs the EPIC NPC\'s stats\n'
        f'{emojis.BP} If you win, the stage increases by +1 the next time\n'
        f'{emojis.BP} Stages never reset\n'
        f'{emojis.BP} You can use `rpg ultr p` to check your progress\n'
    )

    which_command = (
        f'{emojis.BP} The exact impact of the chosen answer is unknown\n'
        f'{emojis.BP} However, it seems that it doesn\'t matter at all\n'
    )

    when = (
        f'{emojis.BP} It is recommended to wait until {emojis.TIME_TRAVEL} TT 25+\n'
    )

    preparation = (
        f'{emojis.BP} Get VOID enchants\n'
        f'{emojis.BP} Get a MAGIC horse\n'
        f'{emojis.BP} Craft as many {emojis.FOOD_APPLE_JUICE} apple juice and {emojis.FOOD_ORANGE_JUICE} orange juice '
        f'you need to reach your desired stage\n'
        f'{emojis.BP} Duel on cooldown to increase your level\n'
    )

    rewards = (
        f'{emojis.BP} 2 {emojis.STAT_COOLNESS} coolness per win\n'
        f'{emojis.BP} XP (depends on your TT and your area)\n'
        f'{emojis.BP} Note: You can **not** get pets in ultraining\n'
    )

    calculators = (
        f'{emojis.BP} `{prefix}uc`: EPIC NPC stats calculator\n'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ULTRAINING',
        description = (
            f'Ultraining is a higher tier of training that is unlocked in area 12. It rewards coolness in addition to XP.\n'
            f'It is the main source of coolness which you need for dungeon 15-2.'
        )
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='HOW IT WORKS', value=how_it_works, inline=False)
    embed.add_field(name='ATTACK, BLOCK OR ATTLOCK?', value=which_command, inline=False)
    embed.add_field(name='WHEN TO DO ULTRAINING', value=when, inline=False)
    embed.add_field(name='PREPARING FOR ULTRAINING', value=preparation, inline=False)
    embed.add_field(name='REWARDS', value=rewards, inline=False)
    embed.add_field(name='CALCULATOR', value=calculators, inline=False)

    return embed