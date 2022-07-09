# gambling.py

import discord
from discord.ext import commands

from resources import emojis
from resources import settings
from resources import functions


# gambling commands (cog)
class GamblingOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Trading menu
    @commands.command(aliases=('gamble','gambling',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def gamblingguide(self, ctx, *args):
        if args:
            arg = args[0]
            if arg in ('blackjack','bj'):
                embed = await embed_blackjack(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg in ('coinflip','cf'):
                embed = await embed_coinflip(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('cup') > -1:
                embed = await embed_cups(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.endswith('dice'):
                if arg.startswith('big'):
                    embed = await embed_bigdice(ctx.prefix)
                    await ctx.send(embed=embed)
                else:
                    embed = await embed_dice(ctx.prefix)
                    await ctx.send(embed=embed)
            elif arg == 'multidice':
                embed = await embed_multidice(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('slot') > -1:
                embed = await embed_slots(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('slot') > -1:
                embed = await embed_slots(ctx.prefix)
                await ctx.send(embed=embed)
            else:
                embed = await embed_gambling_menu(ctx)
                await ctx.send(embed=embed)
        else:
            embed = await embed_gambling_menu(ctx)
            await ctx.send(embed=embed)

    # Command "blackjack"
    @commands.command(aliases=('bj',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def blackjack(self, ctx):
        embed = await embed_blackjack(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "coinflip"
    @commands.command(aliases=('cf',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def coinflip(self, ctx):
        embed = await embed_coinflip(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "cups"
    @commands.command(aliases=('cup',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def cups(self, ctx):
        embed = await embed_cups(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "dice"
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def dice(self, ctx):
        embed = await embed_dice(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "bigdice"
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def bigdice(self, ctx):
        embed = await embed_bigdice(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "multidice"
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def multidice(self, ctx):
        embed = await embed_multidice(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "slots"
    @commands.command(aliases=('slot',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def slots(self, ctx):
        embed = await embed_slots(ctx.prefix)
        await ctx.send(embed=embed)

    # Command "wheels"
    @commands.command(aliases=('wheels',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def wheel(self, ctx):
        embed = await embed_wheel(ctx.prefix)
        await ctx.send(embed=embed)

# Initialization
def setup(bot):
    bot.add_cog(GamblingOldCog(bot))



# --- Redundancies ---
# Guides
guide_gambling = '`{prefix}gambling` : Gambling guides'



# --- Embeds ---
# Gambling menu
async def embed_gambling_menu(ctx):

    prefix = ctx.prefix

    trading = (
        f'{emojis.BP} `{prefix}bigdice` : Big dice guide\n'
        f'{emojis.BP} `{prefix}blackjack` / `{prefix}bj` : Blackjack guide\n'
        f'{emojis.BP} `{prefix}coinflip` / `{prefix}cf` : Coinflip guide\n'
        f'{emojis.BP} `{prefix}cups` : Cups guide\n'
        f'{emojis.BP} `{prefix}dice` : Dice guide\n'
        f'{emojis.BP} `{prefix}multidice` : Multidice guide\n'
        f'{emojis.BP} `{prefix}slots` : Slots guide\n'
        f'{emojis.BP} `{prefix}wheel` : Wheel guide'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'GAMBLING GUIDES',
        description = f'Hey **{ctx.author.name}**, stop gambling.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='GAMBLING', value=trading, inline=False)

    return embed


# Big dice
async def embed_bigdice(prefix: str) -> discord.Embed:
    """Big dice embed"""
    command = f'{emojis.BP} `rpg big dice [$]`'
    rules = (
        f'{emojis.BP} You roll a die that can go from 1 to infinity\n'
        f'{emojis.BLANK} The higher the pot, the higher the amount of sides\n'
        f'{emojis.BLANK} Increasing your bet lowers the amount of sides\n'
        f'{emojis.BP} No matter the outcome, **you always lose your bet**\n'
        f'{emojis.BLANK} Therefore never bet higher than the pot\n'
        f'{emojis.BP} Half of your bet goes into the pot\n'
        f'{emojis.BLANK} If you win, the pot is increased _after_ your payout\n'
        f'{emojis.BP} You need to get side 6 or lower to win\n'
        f'{emojis.BP} The pot doesn\'t get reset if someone wins\n'
        f'{emojis.BLANK} The pot instead resets every monday at 00:00 UTC\n'
    )
    outcomes = (
        f'{emojis.BP} {emojis.GAME_DIE}**- 6** or lower • You win the whole pot but lose your bet\n'
        f'{emojis.BP} {emojis.GAME_DIE}**- 7** or higher • You lose your bet\n'
    )
    note = (
        f'{emojis.BP} This command is unlocked in area 14\n'
    )
    guides = (
        f'{emojis.BP} {guide_gambling.format(prefix=prefix)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'BIG DICE',
        description = 'There is but one good throw upon the dice, which is, to throw them away.'
    )
    embed.add_field(name='COMMAND', value=command, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    return embed


# Blackjack
async def embed_blackjack(prefix):

    syntax = (
        f'{emojis.BP} `rpg blackjack [$]`\n'
        f'{emojis.BP} `rpg bj [$]`\n'
    )

    rules = (
        f'{emojis.BP} Both the dealer (the bot) and you have 2 cards on hand\n'
        f'{emojis.BP} The goal is go get 21 or a number close to it (but not exceed it)\n'
        f'{emojis.BP} Each round you must choose to either `hit` or `stay`\n'
        f'{emojis.BP} `Hit` will give you another card, `stay` will end the game and count the cards\n'
        f'{emojis.BP} If your total value is higher than the dealer\'s and you are below or at 21, you win\n'
        f'{emojis.BP} If you get 21 on the first hand, you win\n'
        f'{emojis.BP} If you exceed 21 at any point (bust), you lose. The dealer can bust too.\n'
        f'{emojis.BP} If you manage to hold 7 cards without busting, you win'
    )

    card_values = (
        f'{emojis.BP} All numbered cards (2-10) are worth that number in points\n'
        f'{emojis.BP} Jack, Queen and King are worth 10 points\n'
        f'{emojis.BP} The Ace is worth 11 points if it does not push you over 21\n'
        f'{emojis.BP} The Ace is worth 1 point if its full value of 11 points would push you over 21'
    )

    outcomes = (
        f'{emojis.BP} **Win** • You win 100% of your bet\n'
        f'{emojis.BP} **Lose** • You lose your bet'
    )

    chances = (
        f'{emojis.BP} The chance to win depends on luck _and_ your skill\n'
        f'{emojis.BP} Therefore exact chances are unknown'
    )

    guides = (
        f'{emojis.BP} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'BLACKJACK',
        description = f'\"Blackjack is very scientific. There\'s always a right answer and wrong answer.\"'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='CARD VALUES', value=card_values, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Coinflip
async def embed_coinflip(prefix):

    syntax = (
        f'{emojis.BP} `rpg coinflip head|tail [$]`\n'
        f'{emojis.BP} `rpg cf h|t [$]`'
    )

    rules = (
        f'{emojis.BP} You flip a coin and bet on heads or tails\n'
        f'{emojis.BP} The coin can either be heads, tails or land on the side'
    )

    outcomes = (
        f'{emojis.BP} **Correct bet** • You win 100% of your bet\n'
        f'{emojis.BP} **Wrong bet** • You lose your bet\n'
        f'{emojis.BP} **Side** • You win 5x your bet'
    )

    chances = (
        f'{emojis.BP} 45% to win\n'
        f'{emojis.BP} 54% to lose\n'
        f'{emojis.BP} 1% to land on the side'
    )

    note = (
        f'{emojis.BP} There is an extremely low chance that the event fails\n'
        f'{emojis.BLANK} If this happens, your coin will land in another area, and you will lose 1 coin\n'
        f'{emojis.BP} This command doesn\'t work in area 19'
    )

    guides = (
        f'{emojis.BP} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'COINFLIP',
        description = f'\"Ah. Fortune smiles. Another day of wine and roses. Or, in your case, beer and pizza!\"'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Cups
async def embed_cups(prefix):

    syntax = f'{emojis.BP} `rpg cups [$]`'

    rules = (
        f'{emojis.BP} You are presented with three {emojis.CUPS} cups\n'
        f'{emojis.BP} You have to enter either `1`, `2` or `3` to pick one of the cups\n'
        f'{emojis.BP} If you pick the correct cup, you win'
    )

    outcomes = (
        f'{emojis.BP} **Correct cup** • You win 1.75x your bet\n'
        f'{emojis.BP} **Wrong cup** • You lose your bet'
    )

    chances = (
        f'{emojis.BP} 33.33% chance to pick the correct cup'
    )

    note = f'{emojis.BP} The cups don\'t move, so don\'t bother waiting for a hint, there is none'

    guides = (
        f'{emojis.BP} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CUPS',
        description = 'These ain\'t coffee cups.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Dice
async def embed_dice(prefix):

    syntax = f'{emojis.BP} `rpg dice [$]`'

    rules = (
        f'{emojis.BP} You roll a die that can go from 1 to 7\n'
        f'{emojis.BP} If you get a 1, 2 or 3, you lose\n'
        f'{emojis.BP} If you get a 4, 5, 6 or 7, you win'
    )

    outcomes = (
        f'{emojis.BP} {emojis.GAME_DIE}**- 1** • You  lose your bet\n'
        f'{emojis.BP} {emojis.GAME_DIE}**- 2** • You  lose half your bet\n'
        f'{emojis.BP} {emojis.GAME_DIE}**- 3** • You  lose a quarter of your bet\n'
        f'{emojis.BP} {emojis.GAME_DIE}**- 4** • You win a quarter of your bet\n'
        f'{emojis.BP} {emojis.GAME_DIE}**- 5** • You win half your bet\n'
        f'{emojis.BP} {emojis.GAME_DIE}**- 6** • You win 100% of your bet\n'
        f'{emojis.BP} {emojis.GAME_DIE}**- 7** • You win 10x your bet'
    )

    chances = (
        f'{emojis.BP} 1 to 6: ~16.7% each\n'
        f'{emojis.BP} 7: Unknown (but very rare)\n'
        f'{emojis.BP} Total winning chance: ~50%\n'
        f'{emojis.BP} Total chance to lose: ~50%'
    )

    note = (
        f'{emojis.BP} This command doesn\'t work in area 19'
    )

    guides = (
        f'{emojis.BP} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'DICE',
        description = 'Dice, dice, baby.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Multidice
async def embed_multidice(prefix):

    syntax = f'{emojis.BP} `rpg multidice [@player] [$]`'

    rules = (
        f'{emojis.BP} You roll a die against another player\n'
        f'{emojis.BP} Whoever gets the higher roll, wins'
    )

    outcomes = (
        f'{emojis.BP} **You roll lower** • The other player wins the bet, you lose the bet\n'
        f'{emojis.BP} **You roll higher** • You win the bet, the other player loses the bet\n'
        f'{emojis.BP} **You roll the same** • You tie, noone wins or loses anything\n'
    )

    chances = (
        f'{emojis.BP} 41.67% to win\n'
        f'{emojis.BP} 41.67%% to lose\n'
        f'{emojis.BP} 16.67% to get a tie'
    )

    note = (
        f'{emojis.BP} This command is unlocked in area 5\n'
        f'{emojis.BP} This is basically a gambling version of `give`\n'
        f'{emojis.BP} The amount you can bet is limited by your coin cap (see `{prefix}coincap`)'
    )

    guides = (
        f'{emojis.BP} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MULTIDICE',
        description = 'Someone wins. Someone loses. Such is life.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Slots
async def embed_slots(prefix):

    syntax = f'{emojis.BP} `rpg slots [$]`'

    rules = (
        f'{emojis.BP} The slot machine gives you a row of 5 emojis\n'
        f'{emojis.BP} If you get **3 or more** of the same emoji, you win (see below)\n'
        f'{emojis.BP} If you get 2 or less of the same emoji, you lose 100% of your bet\n'
        f'{emojis.BP} There are five possible emojis: {emojis.SLOTS_DIAMOND}{emojis.SLOTS_100}{emojis.SLOTS_CLOVER}{emojis.SLOTS_GIFT}{emojis.SLOTS_SPARKLES}'
    )

    rewards_five = (
        f'{emojis.BP}{emojis.SLOTS_DIAMOND} • **20x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_100} • **17.5x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_CLOVER} • **15x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_GIFT} • **12.5x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_SPARKLES} • **10x** your bet'
    )

    rewards_four = (
        f'{emojis.BP}{emojis.SLOTS_DIAMOND} • **5.5x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_100} • **4.8125x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_CLOVER} • **4.125x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_GIFT} • **3.4375x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_SPARKLES} • **2.75x** your bet'
    )

    rewards_three = (
        f'{emojis.BP}{emojis.SLOTS_DIAMOND} • **2x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_100} • **1.75x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_CLOVER} • **1.5x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_GIFT} • **1.25x** your bet\n'
        f'{emojis.BP}{emojis.SLOTS_SPARKLES} • **1x** your bet'
    )

    chances = (
        f'{emojis.BP} Unknown'
    )

    guides = (
        f'{emojis.BP} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'SLOTS',
        description = 'Keep rollin\', rollin\', rollin\', rollin\'.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='5-OF-THE-SAME WINNINGS', value=rewards_five, inline=False)
    embed.add_field(name='4-OF-THE-SAME WINNINGS', value=rewards_four, inline=False)
    embed.add_field(name='3-OF-THE-SAME WINNINGS', value=rewards_three, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Wheel
async def embed_wheel(prefix):

    syntax = f'{emojis.BP} `rpg wheel [$]`'

    rules = (
        f'{emojis.BP} This is a simple wheel of fortune\n'
        f'{emojis.BP} The wheel lands on one of 7 possible colors\n'
        f'{emojis.BP} The outcome is shown at the top of the wheel'
    )

    outcomes = (
        f'{emojis.BP}{emojis.WHEEL_BLUE} • You lose your bet\n'
        f'{emojis.BP}{emojis.WHEEL_RED} • You lose your bet and win a {emojis.LIFE_POTION} life potion\n'
        f'{emojis.BP}{emojis.WHEEL_YELLOW} • You lose your bet and win a {emojis.LOTTERY_TICKET} lottery ticket\n'
        f'{emojis.BP}{emojis.WHEEL_BROWN} • You lose 90% of your bet\n'
        f'{emojis.BP}{emojis.WHEEL_ORANGE} • You lose 75% of your bet\n'
        f'{emojis.BP}{emojis.WHEEL_GREEN} • You win 100% of your bet\n'
        f'{emojis.BP}{emojis.WHEEL_PURPLE} • You win 10x your bet'
    )

    chances = (
        f'{emojis.BP} {emojis.WHEEL_GREEN}{emojis.WHEEL_PURPLE}{emojis.WHEEL_YELLOW}{emojis.WHEEL_RED} • 6.25% each\n'
        f'{emojis.BP} {emojis.WHEEL_BLUE}{emojis.WHEEL_BROWN}{emojis.WHEEL_ORANGE} • 25% each\n'
        f'{emojis.BP} Total winning chance: 12.5%\n'
        f'{emojis.BP} Total chance to lose: 87.5%'
    )

    note = (
        f'{emojis.BP} This command is unlocked in area 8\n'
        f'{emojis.BP} You need to bet at least 25,000 coins\n'
        f'{emojis.BP} If the wheel lands on {emojis.WHEEL_YELLOW}, you only get a {emojis.LOTTERY_TICKET} lottery ticket if you have less than 10'
    )

    guides = (
        f'{emojis.BP} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'WHEEL',
        description = 'What you gonna tell your dad?'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed