# cards.py

import discord

from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_CARDS_GUIDE_OVERVIEW = 'Overview'
TOPIC_CARDS_GUIDE_PLAYING_CARDS = 'Playing cards basics'
TOPIC_CARDS_GUIDE_HAND_OVERVIEW = 'Cards hand: Guide'
TOPIC_CARDS_GUIDE_HAND_WINNING_HANDS = 'Cards hand: Winning hands'
TOPIC_CARDS_GUIDE_HAND_CALCULATION = 'Cards hand: Rewards calculation'

TOPIC_CARDS_DROPS_MONSTERS = 'Monsters, lootboxes & pets'
TOPIC_CARDS_DROPS_WORK_FARM_COMMANDS = 'Work & farm commands'
TOPIC_CARDS_DROPS_ALCHEMY = 'Alchemy'

TOPICS_CARDS_GUIDE = [
    TOPIC_CARDS_GUIDE_OVERVIEW,
    TOPIC_CARDS_GUIDE_PLAYING_CARDS,
    TOPIC_CARDS_GUIDE_HAND_OVERVIEW,
    TOPIC_CARDS_GUIDE_HAND_WINNING_HANDS,
    TOPIC_CARDS_GUIDE_HAND_CALCULATION,
]

TOPICS_CARDS_DROPS = [
    TOPIC_CARDS_DROPS_MONSTERS,
    TOPIC_CARDS_DROPS_WORK_FARM_COMMANDS,
    TOPIC_CARDS_DROPS_ALCHEMY,
]

# --- Commands ---
async def command_cards_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Cards guide command"""
    topics_functions = {
        TOPIC_CARDS_GUIDE_OVERVIEW: embed_cards_overview,
        TOPIC_CARDS_GUIDE_PLAYING_CARDS: embed_cards_playing_Cards,
        TOPIC_CARDS_GUIDE_HAND_OVERVIEW: embed_cards_hand,
        TOPIC_CARDS_GUIDE_HAND_WINNING_HANDS: embed_cards_hand_winning_hands,
        TOPIC_CARDS_GUIDE_HAND_CALCULATION: embed_cards_hand_calculations,
    }
    view = views.TopicView(ctx, topics_functions, active_topic=topic)
    embed = await topics_functions[topic]()
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    try:
        await functions.edit_interaction(interaction, view=None)
    except discord.errors.NotFound:
        pass

    
async def command_cards_drops(ctx: discord.ApplicationContext, topic: str) -> None:
    """Cards drops command"""
    topics_functions = {
        TOPIC_CARDS_DROPS_MONSTERS: embed_cards_drops_monsters,
        TOPIC_CARDS_DROPS_WORK_FARM_COMMANDS: embed_cards_drops_work_farm_commands,
        TOPIC_CARDS_DROPS_ALCHEMY: embed_cards_drops_alchemy,
    }
    view = views.TopicView(ctx, topics_functions, active_topic=topic)
    embed = await topics_functions[topic]()
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    try:
        await functions.edit_interaction(interaction, view=None)
    except discord.errors.NotFound:
        pass


# --- Embeds ---
async def embed_cards_overview() -> discord.Embed:
    """Cards overview"""
    overview = (
        f'{emojis.BP} Cards are rare drops which can be turned into playing cards\n'
        f'{emojis.BP} There are 8 card tiers: {emojis.CARD_COMMON}{emojis.CARD_UNCOMMON}{emojis.CARD_RARE}{emojis.CARD_EPIC}'
        f'{emojis.CARD_OMEGA}{emojis.CARD_GODLY}{emojis.CARD_VOID}{emojis.CARD_ETERNAL}\n'
        f'{emojis.BP} Check {strings.SLASH_COMMANDS_GUIDE["cards drops"]} to see all card sources\n'
        f'{emojis.DETAIL} The cards drop rate is **not** affected by TT and hardmode (or anything else)'
    )
    slotting_cards = (
        f'{emojis.BP} Once you have 3 cards of the **same tier**, you can use {strings.SLASH_COMMANDS_EPIC_RPG["cards slots"]} '
        f'to turn these into a random **playing** card\n'
        f'{emojis.BP} Slotting cards will always give you playing cards you don\'t own yet\n'
    )
    playing_cards = (
        f'{emojis.BP} Playing cards can be used with {strings.SLASH_COMMANDS_EPIC_RPG["cards hand"]}\n'
        f'{emojis.DETAIL} This command has a `1`d cooldown\n'
        f'{emojis.BP} Check `Playing card basics` for an explanation of rank and suit\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["cards deck"]} to see your current playing cards\n'
    )
    round_card = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} -`95`% cooldown reduction\n'
        f'{emojis.DETAIL2} +`200`% lootbox drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.DETAIL2} +`200`% mob drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.DETAIL2} +`200`% items from work commands\n'
        f'{emojis.DETAIL2} +`100`% item rarity from work commands\n'
        f'{emojis.DETAIL} Automatically heals you if you take damage\n'
        f'{emojis.BP} **Duration**: `3`m\n'
        f'{emojis.BP} **Source**: {strings.SLASH_COMMANDS_EPIC_RPG["cards hand"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CARDS',
        description = 'What are those monsters even doing with cards?'
    )
    embed.add_field(name='WHAT ARE CARDS?', value=overview, inline=False)
    embed.add_field(name='SLOTTING CARDS', value=slotting_cards, inline=False)
    embed.add_field(name='PLAYING CARDS', value=playing_cards, inline=False)
    embed.add_field(name='ROUND CARD', value=round_card, inline=False)
    return embed


async def embed_cards_drops_monsters() -> discord.Embed:
    """Cards sources guide"""
    monsters = (
        f'{emojis.BP} Areas 1-3: {emojis.CARD_COMMON} common\n'
        f'{emojis.BP} Areas 4-5 : {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.BP} Areas 6-8 : {emojis.CARD_RARE} rare\n'
        f'{emojis.BP} Areas 9-10 : {emojis.CARD_EPIC} EPIC\n'
        f'{emojis.BP} Areas 11-13 : {emojis.CARD_OMEGA} OMEGA\n'
        f'{emojis.BP} Areas 14-15 : {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.BP} Areas 16-19 : {emojis.CARD_VOID} VOID\n'
        f'{emojis.BP} Area 20 : {emojis.CARD_ETERNAL} ETERNAL\n'
    )
    lootboxes = (
        f'{emojis.LB_COMMON} Common: {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.LB_UNCOMMON} Uncommon: {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.LB_RARE} Rare: {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.LB_EPIC} EPIC: {emojis.CARD_GODLY} GODLY\n'
    )
    lootboxes_2 = (
        f'{emojis.LB_EDGY} EDGY: {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.LB_OMEGA} OMEGA: {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.LB_GODLY} GODLY: {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.LB_VOID} VOID: {emojis.CARD_GODLY} GODLY\n'
    )
    pets = (
        f'{emojis.PET_CAT} Cat: {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.PET_DOG} Dog: {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.PET_DRAGON} Dragon: {emojis.CARD_UNCOMMON} uncommon\n'
    )
    note = (
        f'{emojis.BP} Every source can drop exactly **once**\n'
        f'{emojis.BP} The drop rate is **not** affected by TT and hardmode (or anything else)\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["cards info"]} to track your drops so far\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["area guide"]} to see all monsters in an area\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["monster search"]} to look up monsters by name\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CARD DROPS: MONSTERS, LOOTBOXES & PETS',
    )
    embed.add_field(name='MONSTERS', value=monsters, inline=False)
    embed.add_field(name='LOOTBOXES (1)', value=lootboxes, inline=False)
    embed.add_field(name='LOOTBOXES (2)', value=lootboxes_2, inline=False)
    embed.add_field(name='PETS (FROM TRAINING)', value=pets, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_cards_drops_alchemy() -> discord.Embed:
    """Cards sources alchemy guide"""
    beginner_potions = (
        f'{emojis.POTION_BANANA} Banana Potion: {emojis.CARD_COMMON} common\n'
        f'{emojis.POTION_INVERTED} Inverted Potion: TBA\n'
        f'{emojis.POTION_MONSTER} Monster Potion: TBA\n'
        f'{emojis.POTION_POTION} Potion Potion: {emojis.CARD_COMMON} common\n'
        f'{emojis.POTION_SMOL} Smol Potion: {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.POTION_TRIPLE} Triple Potion: {emojis.CARD_COMMON} common\n'
    )
    simple_potions = (
        f'{emojis.POTION_FISH} Fish Potion: {emojis.CARD_RARE} rare\n'
        f'{emojis.POTION_FLASK} Flask Potion: {emojis.CARD_RARE} rare\n'
        f'{emojis.POTION_JUICE} Juice Potion: {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.POTION_LIQUID_HAIR} Liquid Hair Potion: {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.POTION_P2W} P2W Potion: TBA\n'
        f'{emojis.POTION_WOOD} Wood Potion: {emojis.CARD_RARE} rare\n'        
    )
    advanced_potions = (
        f'{emojis.POTION_COOKIE} Cookie Potion: {emojis.CARD_EPIC} EPIC\n'
        f'{emojis.POTION_DRAGON_BREATH} Dragon Breath Potion: {emojis.CARD_EPIC} EPIC\n'
        f'{emojis.POTION_ELECTRONICAL} Electronical potion: TBA\n'
        f'{emojis.POTION_LOOTBOX} Lootbox potion: {emojis.CARD_EPIC} EPIC\n'
    )
    endgame_potions = (
        f'{emojis.POTION_JUMPY} Jumpy potion: {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.POTION_KING} King potion: {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.POTION_TIME} TIME potion: {emojis.CARD_GODLY} GODLY\n'
        f'{emojis.POTION_VOID} VOID potion: TBA\n'
    )
    pets = (
        f'{emojis.BP} ?\n'
    )
    note = (
        f'{emojis.BP} Every source can drop exactly **once**\n'
        f'{emojis.BP} The drop rate is **not** affected by TT and hardmode (or anything else)\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["cards info"]} to track your drops so far\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["area guide"]} to see all monsters in an area\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["monster search"]} to look up monsters by name\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CARD DROPS: ALCHEMY',
    )
    embed.add_field(name='BEGINNER POTIONS', value=beginner_potions, inline=False)
    embed.add_field(name='SIMPLE POTIONS', value=simple_potions, inline=False)
    embed.add_field(name='ADVANCED POTIONS', value=advanced_potions, inline=False)
    embed.add_field(name='ENDGAME POTIONS', value=endgame_potions, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_cards_drops_work_farm_commands() -> discord.Embed:
    """Cards sources work & farm commands guide"""
    chop_commands = (
        f'{emojis.LOG} Wooden logs: {emojis.CARD_COMMON} common\n'
        f'{emojis.LOG_EPIC} EPIC logs: {emojis.CARD_COMMON} common\n'
        f'{emojis.LOG_SUPER} SUPER logs: {emojis.CARD_COMMON} common\n'
        f'{emojis.LOG_MEGA} MEGA logs: {emojis.CARD_RARE} rare\n'
        f'{emojis.LOG_HYPER} HYPER logs: {emojis.CARD_RARE} rare\n'
        f'{emojis.LOG_ULTRA} ULTRA logs: {emojis.CARD_RARE} rare\n'
        f'{emojis.LOG_ULTIMATE} ULTIMATE logs: {emojis.CARD_ETERNAL} ETERNAL\n'
    )
    fish_commands = (
        f'{emojis.FISH} Normie fish: {emojis.CARD_COMMON} common\n'
        f'{emojis.FISH_GOLDEN} Golden fish: {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.FISH_EPIC} EPIC fish: {emojis.CARD_RARE} rare\n'
        f'{emojis.FISH_SUPER} SUPER fish: {emojis.CARD_ETERNAL} ETERNAL\n'
    )
    pickup_commands = (
        f'{emojis.APPLE} Apples: {emojis.CARD_COMMON} common\n'
        f'{emojis.BANANA} Bananas: {emojis.CARD_UNCOMMON} uncommon\n'
        f'{emojis.WATERMELON} Watermelon: {emojis.CARD_ETERNAL} ETERNAL\n'
    )
    mine_commands = (
        f'{emojis.COIN} Coins: {emojis.CARD_COMMON} common\n'
        f'{emojis.RUBY} Rubies: {emojis.CARD_UNCOMMON} uncommon\n'
    )
    farm_command = (
        f'{emojis.POTATO} Potatoes: {emojis.CARD_EPIC} EPIC\n'
        f'{emojis.BREAD} Bread: {emojis.CARD_EPIC} EPIC\n'
        f'{emojis.CARROT} Carrots: {emojis.CARD_EPIC} EPIC\n'
    )
    note = (
        f'{emojis.BP} Every source can drop exactly **once**\n'
        f'{emojis.BP} The drop rate is **not** affected by TT and hardmode (or anything else)\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["cards info"]} to track your drops so far\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["area guide"]} to see all monsters in an area\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_GUIDE["monster search"]} to look up monsters by name\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CARD DROPS: WORK & FARM COMMANDS',
    )
    embed.add_field(name='CHOP WORK COMMANDS', value=chop_commands, inline=False)
    embed.add_field(name='FISH WORK COMMANDS', value=fish_commands, inline=False)
    embed.add_field(name='PICKUP WORK COMMANDS', value=pickup_commands, inline=False)
    embed.add_field(name='MINE WORK COMMANDS', value=mine_commands, inline=False)
    embed.add_field(name='FARM COMMAND', value=farm_command, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_cards_hand() -> discord.Embed:
    """Cards hand guide"""
    overview = (
        f'{emojis.BP} This command starts a video-poker-ish cards game\n'
        f'{emojis.BP} You always play with a full deck of 52 playing cards\n'
        f'{emojis.BP} Cards you don\'t own can be used, but are greyed out and only give `15`% rewards\n'
        f'{emojis.BP} The command has a `1`d cooldown\n'
    )
    how_to_play = (
        f'{emojis.BP} You start with 2 cards and play 3 rounds\n'
        f'{emojis.BP} Each round you can either select a card **or** you can pass\n'
        f'{emojis.BP} Selecting a card will **discard** that card and replace it with a random other card\n'
        f'{emojis.DETAIL} Discarded cards can not appear again in the same game\n'
        f'{emojis.BP} Passing will keep all the cards you currently have\n'
        f'{emojis.BP} Regardless of your action you will get a new extra card\n'
        f'{emojis.BP} The game ends once you have 5 cards\n'
        f'{emojis.DETAIL} Check `Winning hands` for all win conditions\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CARDS HAND: GUIDE',
        description = 'Others would call it "video poker"'
    )
    embed.add_field(name='OVERVIEW', value=overview, inline=False)
    embed.add_field(name='HOW TO PLAY', value=how_to_play, inline=False)
    return embed


async def embed_cards_hand_winning_hands() -> discord.Embed:
    """Cards hand winning hands guide"""
    royal_hearted_flush = (
        f'{emojis.BP} **Winning conditions**\n'
        f'{emojis.DETAIL2} You have 10, Jack, Queen, King, Ace\n'
        f'{emojis.DETAIL} All 5 cards are of the hearts suit\n'
        f'{emojis.BP} **Base rewards**: '
        f'3 {emojis.TIME_CAPSULE} + 1,200 {emojis.TIME_COOKIE} + 4 {emojis.LB_GODLY} + 30 {emojis.LB_OMEGA} + 15 {emojis.CARD_ROUND}\n'
    )
    royal_flush = (
        f'{emojis.BP} **Winning conditions**\n'
        f'{emojis.DETAIL2} You have 10, Jack, Queen, King and Ace\n'
        f'{emojis.DETAIL} All 5 cards are of the same non-hearts suit\n'
        f'{emojis.BP} **Base rewards**: '
        f'1 {emojis.TIME_CAPSULE} + 800 {emojis.TIME_COOKIE} + 2 {emojis.LB_GODLY} + 20 {emojis.LB_OMEGA} + 10 {emojis.CARD_ROUND}\n'
    )
    ace_gala = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} You have 4 Aces\n'
        f'{emojis.BP} **Base rewards**: '
        f'1 {emojis.TIME_CAPSULE} + 600 {emojis.TIME_COOKIE} + 1 {emojis.LB_GODLY} + 15 {emojis.LB_OMEGA} + 5 {emojis.CARD_ROUND}\n'
    )
    straight_flush = (
        f'{emojis.BP} **Winning conditions**\n'
        f'{emojis.DETAIL2} All 5 cards follow each other in rank\n'
        f'{emojis.DETAIL} All 5 cards are of the same suit\n'
        f'{emojis.BP} **Base rewards**: '
        f'450 {emojis.TIME_COOKIE} + 1 {emojis.LB_GODLY} + 8 {emojis.LB_OMEGA} + 5 {emojis.CARD_ROUND}\n'
    )
    four_of_a_kind = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} 4 cards are of the same rank\n'
        f'{emojis.BP} **Base rewards**: '
        f'250 {emojis.TIME_COOKIE} + 4 {emojis.LB_OMEGA} + 14 {emojis.FLASK} + 3 {emojis.CARD_ROUND}\n'
    )
    game_of_kings = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} You have 2 Kings and 2 Queens\n'
        f'{emojis.BP} **Base rewards**: '
        f'175 {emojis.TIME_COOKIE} + 3 {emojis.LB_OMEGA} + 12 {emojis.FLASK} + 3 {emojis.CARD_ROUND}\n'
    )
    full_house = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} 3 cards are of one rank + 2 cards are of another rank\n'
        f'{emojis.BP} **Base rewards**: '
        f'140 {emojis.TIME_COOKIE} + 3 {emojis.LB_OMEGA} + 10 {emojis.FLASK} + 2 {emojis.CARD_ROUND}\n'
    )
    flush = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} All 5 cards are of the same suit\n'
        f'{emojis.BP} **Base rewards**: '
        f'120 {emojis.TIME_COOKIE} + 2 {emojis.LB_OMEGA} + 8 {emojis.FLASK} + 2 {emojis.CARD_ROUND}\n'
    )
    unbreakable_fortress = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} You have Ace, 2, 3, 4 and 5\n'
        f'{emojis.BP} **Base rewards**: '
        f'90 {emojis.TIME_COOKIE} + 210 {emojis.GUILD_RING} + 6 {emojis.FLASK} + 1 {emojis.CARD_ROUND}\n'
    )
    straight = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} All 5 cards follow each other in rank\n'
        f'{emojis.BP} **Base rewards**: '
        f'70 {emojis.TIME_COOKIE} + 180 {emojis.GUILD_RING} + 4 {emojis.FLASK} + 1 {emojis.CARD_ROUND}\n'
    )
    three_of_a_kind = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} 3 cards are of the same rank\n'
        f'{emojis.BP} **Base rewards**: '
        f'35 {emojis.TIME_COOKIE} + 120 {emojis.GUILD_RING} + 2 {emojis.FLASK} + 160 {emojis.ARENA_COOKIE}\n'
    )
    two_pair = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} 2 cards are of one rank + 2 cards are of another rank\n'
        f'{emojis.BP} **Base rewards**: 25 {emojis.TIME_COOKIE} + 80 {emojis.GUILD_RING} + 100 {emojis.ARENA_COOKIE}\n'
    )
    pair = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} 2 cards are of the same rank\n'
        f'{emojis.BP} **Base rewards**: 10 {emojis.TIME_COOKIE} + 15 {emojis.GUILD_RING} + 30 {emojis.ARENA_COOKIE}\n'
    )
    random_cards = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} Your cards do not fulfill any of the other conditions\n'
        f'{emojis.BP} **Base reward**: 10 {emojis.ARENA_COOKIE}\n'
    )
    timeout = (
        f'{emojis.BP} **Winning condition**\n'
        f'{emojis.DETAIL} You didn\'t answer for some reason\n'
        f'{emojis.BP} **Reward**: 5 {emojis.ARENA_COOKIE}\n'
    )
    note = (
        f'{emojis.BP} The order of cards does not matter\n'
        f'{emojis.DETAIL} Example: 2, 3, 4, 5, 6 is the same hand as 4, 6, 2, 5, 3\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CARDS HAND: WINNING HANDS',
        description = 'These winning hands are listed in descending order by rarity / reward amount',
    )
    embed.add_field(name='ROYAL HEARTED FLUSH', value=royal_hearted_flush, inline=False)
    embed.add_field(name='ROYAL FLUSH', value=royal_flush, inline=False)
    embed.add_field(name='ACE GALA', value=ace_gala, inline=False)
    embed.add_field(name='STRAIGHT FLUSH', value=straight_flush, inline=False)
    embed.add_field(name='FOUR OF A KIND', value=four_of_a_kind, inline=False)
    embed.add_field(name='GAME OF KINGS', value=game_of_kings, inline=False)
    embed.add_field(name='FULL HOUSE', value=full_house, inline=False)
    embed.add_field(name='FLUSH', value=flush, inline=False)
    embed.add_field(name='UNBREAKABLE FORTRESS', value=unbreakable_fortress, inline=False)
    embed.add_field(name='STRAIGHT', value=straight, inline=False)
    embed.add_field(name='THREE OF A KIND', value=three_of_a_kind, inline=False)
    embed.add_field(name='TWO PAIRS', value=two_pair, inline=False)
    embed.add_field(name='PAIR', value=pair, inline=False)
    embed.add_field(name='RANDOM CARDS', value=random_cards, inline=False)
    embed.add_field(name='TIMEOUT', value=timeout, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_cards_hand_calculations() -> discord.Embed:
    """Cards hand reward calaclations guide"""
    overview = (
        f'{emojis.BP} These calculations apply to the base rewards\n'
        f'{emojis.DETAIL} Check `Cards hand: Winning hands` to see the base rewards\n'
    )
    owned_cards = (
        f'{emojis.BP} Finishing with cards you don\'t own **reduces** rewards\n'
        f'{emojis.DETAIL} Cards not being part of the winning hand still count\n'
        f'{emojis.BP} Every card you don\'t own reduces rewards by `17`%\n'
        f'{emojis.BP} Example: If you own 2/5 cards, you will get `49`% of rewards\n'
    )
    card_rank = (
        f'{emojis.BP} If a winning hand is rank independent, rewards **increase** by `5`% per rank\n'
        f'{emojis.DETAIL2} Example 1: A pair of 2s will give a `5`% increase\n'
        f'{emojis.DETAIL} Example 2: A pair of queens will give a `55`% increase\n'
        f'{emojis.BP} If different ranks form one hand, the increase is averaged\n'
        f'{emojis.DETAIL} Example: A full house of 2s (`5`%) and queens (`55`%) will give a `30`% increase\n'
    )
    example = (
        f'{emojis.BP} You finish with 5, K, 5, 10, K\n'
        f'{emojis.DETAIL2} This is a two pair of 5,5 and K,K\n'
        f'{emojis.DETAIL} Kings give +`60`% rewards, 5s give +`20`% rewards, so average is +`40`%\n'
        f'{emojis.BP} You own 3 of the 5 cards you finished with\n'
        f'{emojis.DETAIL} This reduces rewards by `2 * 17`%, so you get `66`% of the rewards\n'
        f'{emojis.BP} Final rewards are `[Base amount] * 1.4 * 0.66`\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CARDS HAND: REWARD CALCULATIONS',
        description = 'Confused? Don\'t worry.',
    )
    embed.add_field(name='OVERVIEW', value=overview, inline=False)
    embed.add_field(name='OWNED CARDS', value=owned_cards, inline=False)
    embed.add_field(name='CARD RANKS', value=card_rank, inline=False)
    embed.add_field(name='I WANT AN EXAMPLE', value=example, inline=False)
    return embed



async def embed_cards_playing_Cards() -> discord.Embed:
    """Playing cards guide"""
    overview = (
        f'{emojis.BP} There are 52 playing cards in total\n'
        f'{emojis.DETAIL} Use {strings.SLASH_COMMANDS_EPIC_RPG["cards deck"]} to see your current playing cards\n'
        f'{emojis.BP} Each card has a suit and a rank (see below)\n'
        f'{emojis.BP} A deck consists of 4 suits with 13 ranks each\n'
        f'{emojis.BP} You can always play with all 52 cards, but winning with cards you actually own increases your rewards\n'
    )
    suits = (
        f'{emojis.BP} The card suit is the "icon" of a card\n'
        f'{emojis.BP} Suits are clubs (C), diamonds (D), hearts (H), and spades (S)\n'
    )
    ranks = (
        f'{emojis.BP} The card rank is the value of a card\n'
        f'{emojis.BP} Ranks are 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, and Ace\n'
        f'{emojis.DETAIL} This list is in ascending order, so 2 is the lowest, Ace the highest rank\n'
    )
    naming = (
        f'{emojis.BP} Playing cards are labelled by their suit and rank\n'
        f'{emojis.DETAIL2} Example 1: **C9** is a clubs 9 card\n'
        f'{emojis.DETAIL} Example 2: **HQ** is a hearts queen card\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'PLAYING CARDS BASICS',
    )
    embed.add_field(name='BASICS', value=overview, inline=False)
    embed.add_field(name='SUIT', value=suits, inline=False)
    embed.add_field(name='RANK', value=ranks, inline=False)
    embed.add_field(name='NAMING', value=naming, inline=False)
    return embed