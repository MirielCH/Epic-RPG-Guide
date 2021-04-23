# gambling.py

import discord
import emojis
import global_data

from discord.ext import commands

# gambling commands (cog)
class gamblingCog(commands.Cog):
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
            elif arg == 'dice':
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
    bot.add_cog(gamblingCog(bot))



# --- Redundancies ---
# Guides
guide_gambling = '`{prefix}gambling` : Gambling guides'

                    

# --- Embeds ---
# Gambling menu
async def embed_gambling_menu(ctx):
    
    prefix = ctx.prefix
                    
    trading = (
        f'{emojis.bp} `{prefix}blackjack` / `{prefix}bj` : Blackjack guide\n'
        f'{emojis.bp} `{prefix}coinflip` / `{prefix}cf` : Coinflip guide\n'
        f'{emojis.bp} `{prefix}cups` : Cups guide\n'
        f'{emojis.bp} `{prefix}dice` : Dice guide\n'
        f'{emojis.bp} `{prefix}multidice` : Multidice guide\n'
        f'{emojis.bp} `{prefix}slots` : Slots guide\n'
        f'{emojis.bp} `{prefix}wheel` : Wheel guide'
    )
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'GAMBLING GUIDES',
        description = f'Hey **{ctx.author.name}**, stop gambling.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='GAMBLING', value=trading, inline=False)
    
    return embed

# Blackjack
async def embed_blackjack(prefix):

    syntax = (
        f'{emojis.bp} `rpg blackjack [$]`\n'
        f'{emojis.bp} `rpg bj [$]`\n'
    )

    rules = (
        f'{emojis.bp} Both the dealer (the bot) and you have 2 cards on hand\n'
        f'{emojis.bp} The goal is go get 21 or a number close to it (but not exceed it)\n'
        f'{emojis.bp} Each round you must choose to either `hit` or `stay`\n'
        f'{emojis.bp} `Hit` will give you another card, `stay` will end the game and count the cards\n'
        f'{emojis.bp} If your total value is higher than the leader\'s and you are below or at 21, you win\n'
        f'{emojis.bp} If you get 21 on the first hand, you win\n'
        f'{emojis.bp} If you exceed 21 at any point (bust), you lose. The dealer can bust too.\n'
        f'{emojis.bp} If you manage to hold 7 cards without busting, you win'
    )
    
    card_values = (
        f'{emojis.bp} All numbered cards (2-10) are worth that number in points\n'
        f'{emojis.bp} Jack, Queen and King are worth 10 points\n'
        f'{emojis.bp} The Ace is worth 11 points if it does not push you over 21\n'
        f'{emojis.bp} The Ace is worth 1 point if its full value of 11 points would push you over 21'
    )
    
    outcomes = (
        f'{emojis.bp} **Win** • You win 100% of your bet\n'
        f'{emojis.bp} **Lose** • You lose your bet'
    )
                   
    chances = (
        f'{emojis.bp} The chance to win depends on luck _and_ your skill\n'
        f'{emojis.bp} Therefore exact chances are unknown'
    )
     
    guides = (
        f'{emojis.bp} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'BLACKJACK',
        description = f'\"Blackjack is very scientific. There\'s always a right answer and wrong answer.\"'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
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
        f'{emojis.bp} `rpg coinflip head|tail [$]`\n'
        f'{emojis.bp} `rpg cf h|t [$]`'
    )

    rules = (
        f'{emojis.bp} You flip a coin and bet on heads or tails\n'
        f'{emojis.bp} The coin can either be heads, tails or land on the side'
    )
    
    outcomes = (
        f'{emojis.bp} **Correct bet** • You win 100% of your bet\n'
        f'{emojis.bp} **Wrong bet** • You lose your bet\n'
        f'{emojis.bp} **Side** • You win 5x your bet'
    )
              
    chances = (
        f'{emojis.bp} 45% to win\n'
        f'{emojis.bp} 54% to lose\n'
        f'{emojis.bp} 1% to land on the side'
    )
    
    note = (
        f'{emojis.bp} There is an extremely low chance that the event fails\n'
        f'{emojis.bp} If this happens, your coin will land in another area, and you will lose 1 coin'
    )
          
    guides = (
        f'{emojis.bp} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'COINFLIP',
        description = f'\"Ah. Fortune smiles. Another day of wine and roses. Or, in your case, beer and pizza!\"'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Cups
async def embed_cups(prefix):

    syntax = f'{emojis.bp} `rpg cups [$]`'

    rules = (
        f'{emojis.bp} You are presented with three {emojis.cups} cups\n'
        f'{emojis.bp} You have to enter either `1`, `2` or `3` to pick one of the cups\n'
        f'{emojis.bp} If you pick the correct cup, you win'
    )
    
    outcomes = (
        f'{emojis.bp} **Correct cup** • You win 1.75x your bet\n'
        f'{emojis.bp} **Wrong cup** • You lose your bet'
    )
    
    chances = (
        f'{emojis.bp} 33.33% go get pick the correct cup'
    )
    
    note = f'{emojis.bp} The cups don\'t move, so don\'t bother waiting for a hint, there is none'
                    
    guides = (
        f'{emojis.bp} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'CUPS',
        description = 'These ain\'t coffee cups.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Dice
async def embed_dice(prefix):

    syntax = f'{emojis.bp} `rpg dice [$]`'

    rules = (
        f'{emojis.bp} You roll a die that can go from 1 to 7\n'
        f'{emojis.bp} If you get a 1, 2 or 3, you lose\n'
        f'{emojis.bp} If you get a 4, 5, 6 or 7, you win'
    )
    
    outcomes = (
        f'{emojis.bp} {emojis.game_die}**- 1** • You  lose your bet\n'
        f'{emojis.bp} {emojis.game_die}**- 2** • You  lose half your bet\n'
        f'{emojis.bp} {emojis.game_die}**- 3** • You  lose a quarter of your bet\n'
        f'{emojis.bp} {emojis.game_die}**- 4** • You win a quarter of your bet\n'
        f'{emojis.bp} {emojis.game_die}**- 5** • You win half your bet\n'
        f'{emojis.bp} {emojis.game_die}**- 6** • You win 100% of your bet\n'
        f'{emojis.bp} {emojis.game_die}**- 7** • You win 10x your bet'
    )
                    
    chances = (
        f'{emojis.bp} 1 to 6: ~16.7% each\n'
        f'{emojis.bp} 7: Unknown (but very rare)\n'
        f'{emojis.bp} Total winning chance: ~50%\n'
        f'{emojis.bp} Total chance to lose: ~50%'
    )
    
    guides = (
        f'{emojis.bp} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'DICE',
        description = 'Dice, dice, baby.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Multidice
async def embed_multidice(prefix):

    syntax = f'{emojis.bp} `rpg multidice [@player] [$]`'

    rules = (
        f'{emojis.bp} You roll a die against another player\n'
        f'{emojis.bp} Whoever gets the higher roll, wins'
    )
    
    outcomes = (
        f'{emojis.bp} **You roll lower** • The other player wins the bet, you lose the bet\n'
        f'{emojis.bp} **You roll higher** • You win the bet, the other player loses the bet'
    )
     
    chances = (
        f'{emojis.bp} 50% to win\n'
        f'{emojis.bp} 50% lose'
    )
              
    note = (
        f'{emojis.bp} This command is unlocked in area 5\n'
        f'{emojis.bp} This is basically a gambling version of `give`\n'
        f'{emojis.bp} The amount you can bet is limited by your coin cap (see `{prefix}coincap`)'
    )
          
    guides = (
        f'{emojis.bp} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'MULTIDICE',
        description = 'Someone wins. Someone loses. Such is life.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Slots
async def embed_slots(prefix):

    syntax = f'{emojis.bp} `rpg slots [$]`'

    rules = (
        f'{emojis.bp} The slot machine gives you a row of 5 emojis\n'
        f'{emojis.bp} If you get **3 or more** of the same emoji, you win (see below)\n'
        f'{emojis.bp} If you get 2 or less of the same emoji, you lose 100% of your bet\n'
        f'{emojis.bp} There are five possible emojis: {emojis.slots_diamond}{emojis.slots_100}{emojis.slots_clover}{emojis.slots_gift}{emojis.slots_sparkles}'
    )
    
    rewards_five = (
        f'{emojis.bp}{emojis.slots_diamond} • **20x** your bet\n'
        f'{emojis.bp}{emojis.slots_100} • **17.5x** your bet\n'
        f'{emojis.bp}{emojis.slots_clover} • **15x** your bet\n'
        f'{emojis.bp}{emojis.slots_gift} • **12.5x** your bet\n'
        f'{emojis.bp}{emojis.slots_sparkles} • **10x** your bet'
    )
    
    rewards_four = (
        f'{emojis.bp}{emojis.slots_diamond} • **5.5x** your bet\n'
        f'{emojis.bp}{emojis.slots_100} • **4.8125x** your bet\n'
        f'{emojis.bp}{emojis.slots_clover} • **4.125x** your bet\n'
        f'{emojis.bp}{emojis.slots_gift} • **3.4375x** your bet\n'
        f'{emojis.bp}{emojis.slots_sparkles} • **2.75x** your bet'
    )
    
    rewards_three = (
        f'{emojis.bp}{emojis.slots_diamond} • **2x** your bet\n'
        f'{emojis.bp}{emojis.slots_100} • **1.75x** your bet\n'
        f'{emojis.bp}{emojis.slots_clover} • **1.5x** your bet\n'
        f'{emojis.bp}{emojis.slots_gift} • **1.25x** your bet\n'
        f'{emojis.bp}{emojis.slots_sparkles} • **1x** your bet'
    )
                    
    chances = (
        f'{emojis.bp} Unknown'
    )
    
    guides = (
        f'{emojis.bp} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'SLOTS',
        description = 'Keep rollin\', rollin\', rollin\', rollin\'.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
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

    syntax = f'{emojis.bp} `rpg wheel [$]`'

    rules = (
        f'{emojis.bp} This is a simple wheel of fortune\n'
        f'{emojis.bp} The wheel lands on one of 7 possible colors\n'
        f'{emojis.bp} The outcome is shown at the top of the wheel'
    )
    
    outcomes = (
        f'{emojis.bp}{emojis.wheel_blue} • You lose your bet\n'
        f'{emojis.bp}{emojis.wheel_red} • You lose your bet and win a {emojis.lifepotion} life potion\n'
        f'{emojis.bp}{emojis.wheel_yellow} • You lose your bet and win a {emojis.ticketlottery} lottery ticket\n'
        f'{emojis.bp}{emojis.wheel_brown} • You lose 90% of your bet\n'
        f'{emojis.bp}{emojis.wheel_orange} • You lose 75% of your bet\n'
        f'{emojis.bp}{emojis.wheel_green} • You win 100% of your bet\n'
        f'{emojis.bp}{emojis.wheel_purple} • You win 10x your bet'
    )
    
    chances = (
        f'{emojis.bp} {emojis.wheel_green}{emojis.wheel_purple}{emojis.wheel_yellow}{emojis.wheel_red} • 6.25% each\n'
        f'{emojis.bp} {emojis.wheel_blue}{emojis.wheel_brown}{emojis.wheel_orange} • 25% each\n'
        f'{emojis.bp} Total winning chance: 12.5%\n'
        f'{emojis.bp} Total chance to lose: 87.5%'
    )
    
    note = (
        f'{emojis.bp} This command is unlocked in area 8\n'
        f'{emojis.bp} You need to bet at least 25,000 coins\n'
        f'{emojis.bp} If the wheel lands on {emojis.wheel_yellow}, you only get a {emojis.ticketlottery} lottery ticket if you have less than 10'
    )
                    
    guides = (
        f'{emojis.bp} {guide_gambling.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'WHEEL',
        description = 'What you gonna tell your dad?'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='SYNTAX', value=syntax, inline=False)
    embed.add_field(name='RULES', value=rules, inline=False)
    embed.add_field(name='POSSIBLE OUTCOMES', value=outcomes, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed