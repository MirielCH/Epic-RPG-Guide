# alchemy.py

import discord

from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_ALCHEMY_RECOMMENDATIONS = 'Recommended potions'
TOPIC_ALCHEMY_BEGINNER = 'All beginner potions'
TOPIC_ALCHEMY_SIMPLE = 'All simple potions'
TOPIC_ALCHEMY_ADVANCED = 'All advanced potions'
TOPIC_ALCHEMY_ENDGAME = 'All endgame potions'

TOPICS_ALCHEMY = [
    TOPIC_OVERVIEW,
    TOPIC_ALCHEMY_RECOMMENDATIONS,
    TOPIC_ALCHEMY_BEGINNER,
    TOPIC_ALCHEMY_SIMPLE,
    TOPIC_ALCHEMY_ADVANCED,
    TOPIC_ALCHEMY_ENDGAME,
]


# --- Commands ---
async def command_alchemy_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Alchemy command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_alchemy_overview,
        TOPIC_ALCHEMY_RECOMMENDATIONS: embed_alchemy_recommended_potions,
        TOPIC_ALCHEMY_BEGINNER: embed_alchemy_beginner,
        TOPIC_ALCHEMY_SIMPLE: embed_alchemy_simple,
        TOPIC_ALCHEMY_ADVANCED: embed_alchemy_advanced,
        TOPIC_ALCHEMY_ENDGAME: embed_alchemy_endgame,
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
async def embed_alchemy_overview() -> discord.Embed:
    """Alchemy guide overview"""
    overview = (
        f'{emojis.BP} Potions activate boosts that last for a certain amount of time\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["alchemy make"]} to brew potions.\n'
        f'{emojis.DETAIL} Potions are instantly active after brewing!\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["boosts"]} to check your active boosts\n'
        f'{emojis.BP} Boosts of different potions stack additively (e.g. `10`% + `15`% = `25`% total)\n'
        f'{emojis.BP} You can not brew a potion already active...\n'
        f'{emojis.DETAIL2} ...unless you have the {emojis.ARTIFACT_GOLDEN_PAN} golden pan artifact\n'
        f'{emojis.DETAIL} This will refresh their duration, not add time\n'
        f'{emojis.BP} **Boosts are not lost when time traveling!**\n'
    )
    flasks = (
        f'{emojis.BP} Potions require {emojis.FLASK} flasks to brew\n'
        f'{emojis.BP} Flasks are lost when time traveling\n'
        f'{emojis.BP} Flasks are obtained from the following commands:\n'
        f'{emojis.DETAIL2} `2` from {strings.SLASH_COMMANDS_EPIC_RPG["weekly"]}\n'
        f'{emojis.DETAIL2} `1` from {strings.SLASH_COMMANDS_EPIC_RPG["daily"]} (if you have 7/7 streak)\n'
        f'{emojis.DETAIL} `1` from {strings.SLASH_COMMANDS_EPIC_RPG["vote"]} (if you have 7/7 streak)\n'
    )
    note = (
        f'{emojis.BP} Alchemy is unlocked in area 7\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ALCHEMY GUIDE',
        description = 'Netflix and Distill'
    )
    embed.add_field(name='OVERVIEW', value=overview, inline=False)
    embed.add_field(name=f'FLASKS {emojis.FLASK}', value=flasks, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_alchemy_recommended_potions() -> discord.Embed:
    """Alchemy recommended potions"""
    best_potions = (
        f'{emojis.BP} {emojis.POTION_FISH} `Fish potion` and {emojis.POTION_WOOD} `Wood potion`\n'
        f'{emojis.DETAIL} Both increase profession XP and work item yield\n'
        f'{emojis.BP} Try to always have 2 flasks ready for those at the end of your TT\n'
        f'{emojis.BP} If you have only 1 flask left, craft the fish potion\n'
        f'{emojis.BP} Brew them right before you level professions and time travel\n'
    )
    good_potions_tt0 = (
        f'{emojis.BP} {emojis.POTION_MONSTER} `Monster potion`\n'
        f'{emojis.DETAIL2} Helps getting mob drops for the EDGY armor faster\n'
        f'{emojis.BP} {emojis.POTION_BANANA} `Banana potion` and {emojis.POTION_SMOL} `Smol potion`\n'
        f'{emojis.DETAIL} Helps leveling up faster\n'
    )
    good_potions_tt3 = (
        f'{emojis.BP} {emojis.POTION_COOKIE} `Cookie potion`\n'
        f'{emojis.DETAIL2} Increases pet spawn chance\n'
        f'{emojis.DETAIL} Helps leveling up faster\n'
    )
    good_potions_tt25 = (
        f'{emojis.BP} {emojis.POTION_DRAGON_BREATH} `Dragon breath potion`\n'
        f'{emojis.DETAIL} Doubles dragon scale drops in areas 11-15\n'
        f'{emojis.BP} {emojis.POTION_LOOTBOX} `Lootbox potion`\n'
        f'{emojis.DETAIL} Helps farming those OMEGA lootboxes for D15-2\n'
    )
    good_potions_ultraining = (
        f'{emojis.BP} {emojis.POTION_TRIPLE} `Triple potion`\n'
        f'{emojis.DETAIL} Helps you get more farm items for cooking stats\n'
        f'{emojis.BP} {emojis.POTION_ELECTRONICAL} `Electronical potion`\n'
        f'{emojis.DETAIL} Boosts pretty much everything\n'
    )
    good_potions_void = (
        f'{emojis.BP} {emojis.POTION_VOID} `Void potion`\n'
        f'{emojis.DETAIL} Increases dark energy drop chance and saves money enchanting\n'
        f'{emojis.BP} {emojis.POTION_JUMPY} `Jumpy potion`\n'
        f'{emojis.DETAIL} Increases VOID aura drop chance\n'
    )
    note = (
        f'{emojis.BP} This list does not include all potions\n'
        f'{emojis.BP} Not being on this page does **not** mean a potion is useless!\n'
        f'{emojis.DETAIL} Well, not all of them at least\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ALCHEMY: RECOMMENDED POTIONS',
        description = 'You could also just look through them, you know.'
    )
    embed.add_field(name='IF YOU WANT THE BEST', value=best_potions, inline=False)
    embed.add_field(name='IF YOU JUST STARTED', value=good_potions_tt0, inline=False)
    embed.add_field(name='IF YOU ARE TT 3+ AND LIKE PETS', value=good_potions_tt3, inline=False)
    embed.add_field(name='IF YOU ARE TT 25+', value=good_potions_tt25, inline=False)
    embed.add_field(name='IF YOU ARE IN AN ULTRAINING RUN', value=good_potions_ultraining, inline=False)
    embed.add_field(name='IF YOU ARE IN A VOID AREA', value=good_potions_void, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_alchemy_beginner() -> discord.Embed:
    """Alchemy beginner potion"""
    potion_banana = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`30`% XP from all sources\n'
        f'{emojis.DETAIL} +`15`% items from work commands\n'
        f'{emojis.BP} **Duration**: `6`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `5` {emojis.BANANA}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Level up faster in early TTs\n'
    )
    potion_inverted = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`40`% random event spawn chance\n'
        f'{emojis.DETAIL} +`15`% enchanting luck\n'
        f'{emojis.BP} **Duration**: `11`h `11`m `11`s\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `1` {emojis.POTATO} + `1` {emojis.UNICORN_HORN} '
        f'+ `12` {emojis.APPLE}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Increase your event spawns during some seasonal events\n'
    )
    potion_monster = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`30`% mob drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.DETAIL2} +`10`% lootbox drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.DETAIL2} +`10`% XP from all sources\n'
        f'{emojis.DETAIL} +`10`% coins from all sources except selling & miniboss\n'
        f'{emojis.BP} **Duration**: `7`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `6` {emojis.WOLF_SKIN} + `2` {emojis.ZOMBIE_EYE} '
        f'+ `1` {emojis.UNICORN_HORN}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Get the mob drops for the EDGY armor faster in early TTs\n'
    )
    potion_potion = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`60` {emojis.STAT_LIFE} LIFE\n'
        f'{emojis.DETAIL} Automatically heals you if you take damage\n'
        f'{emojis.BP} **Duration**: `20`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `1` {emojis.LIFE_POTION}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL2} Helps with taking damage in `hunt together`\n'
        f'{emojis.DETAIL} Peace of mind, especially if your horse is not T4 yet\n'
    )
    potion_smol = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL} +`80`% XP from all sources\n'
        f'{emojis.BP} **Duration**: `2`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `1` {emojis.LOG} + `1` {emojis.FISH}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Level up faster in early TTs\n'
    )
    potion_triple = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`30`% special seed drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["farm"]}\n'
        f'{emojis.DETAIL} +`20`% items from {strings.SLASH_COMMANDS_EPIC_RPG["farm"]}\n'
        f'{emojis.BP} **Duration**: `10`h\n'
        f'{emojis.BP} **Recipe**: `3` {emojis.FLASK} + `15` {emojis.BREAD} + `15` {emojis.CARROT} '
        f'+ `15` {emojis.POTATO}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Use in ultraining runs to cook more stats\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ALCHEMY: BEGINNER POTIONS',
    )
    embed.add_field(name=f'BANANA POTION {emojis.POTION_BANANA}', value=potion_banana, inline=False)
    embed.add_field(name=f'INVERTED POTION {emojis.POTION_INVERTED}', value=potion_inverted, inline=False)
    embed.add_field(name=f'MONSTER POTION {emojis.POTION_MONSTER}', value=potion_monster, inline=False)
    embed.add_field(name=f'POTION POTION {emojis.POTION_POTION}', value=potion_potion, inline=False)
    embed.add_field(name=f'SMOL POTION {emojis.POTION_SMOL}', value=potion_smol, inline=False)
    embed.add_field(name=f'TRIPLE POTION {emojis.POTION_TRIPLE}', value=potion_triple, inline=False)
    return embed


async def embed_alchemy_simple() -> discord.Embed:
    """Alchemy simple potion"""
    potion_fish = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`30`% items from work commands\n'
        f'{emojis.DETAIL2} +`15`% profession XP\n'
        f'{emojis.DETAIL} +`10`% item rarity from work commands\n'
        f'{emojis.BP} **Duration**: `1`d\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `42` {emojis.FISH_EPIC}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Use before TT to level professions and get more items after TT\n'
    )
    potion_flask = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL} -`0.01`% cooldown reduction\n'
        f'{emojis.BP} **Duration**: `12`h\n'
        f'{emojis.BP} **Recipe**: `2` {emojis.FLASK}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} If you somehow don\'t know what else to do with your flasks, do this\n'
    )
    potion_juice = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`10` {emojis.STAT_AT} AT\n'
        f'{emojis.DETAIL2} +`10` {emojis.STAT_DEF} DEF\n'
        f'{emojis.DETAIL} +`25` {emojis.STAT_LIFE} LIFE\n'
        f'{emojis.BP} **Duration**: `1`d `6`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `45` {emojis.APPLE} + `3` {emojis.EPIC_BERRY} '
        f'+ `60` {emojis.CARROT}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Reach recommended dungeon stats easier in early TTs\n'
    )
    potion_liquid_hair = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} -`10`% pet adventure time if pet returns while boost is active\n'
        f'{emojis.DETAIL} +`5`% enchanting luck\n'
        f'{emojis.BP} **Duration**: `5`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `60` {emojis.MERMAID_HAIR}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Lol\n'
    )
    potion_p2w = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`15` {emojis.STAT_AT} AT\n'
        f'{emojis.DETAIL2} +`15` {emojis.STAT_DEF} DEF\n'
        f'{emojis.DETAIL2} +`35` {emojis.STAT_LIFE} LIFE\n'
        f'{emojis.DETAIL2} +`100`% coins from all sources except selling & miniboss\n'
        f'{emojis.DETAIL} +`20`% increased selling price of all items\n'
        f'{emojis.BP} **Duration**: `10`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `2` {emojis.COIN_TRUMPET} + `2` {emojis.EPIC_SEED} + `2`{emojis.ULTRA_BAIT}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} It\'s basically a potion to turn epic coins into coins, hence the name\n'
    )
    potion_wood = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`30`% item rarity from work commands\n'
        f'{emojis.DETAIL2} +`10`% items from work commands\n'
        f'{emojis.DETAIL} +`10`% profession XP\n'
        f'{emojis.BP} **Duration**: `1`d\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `15` {emojis.LOG_MEGA} + `3` {emojis.LOG_ULTRA}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Use before TT to level professions and get more items after TT\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ALCHEMY: SIMPLE POTIONS',
    )
    embed.add_field(name=f'FISH POTION {emojis.POTION_FISH}', value=potion_fish, inline=False)
    embed.add_field(name=f'FLASK POTION {emojis.POTION_FLASK}', value=potion_flask, inline=False)
    embed.add_field(name=f'JUICE POTION {emojis.POTION_JUICE}', value=potion_juice, inline=False)
    embed.add_field(name=f'LIQUID HAIR POTION {emojis.POTION_LIQUID_HAIR}', value=potion_liquid_hair, inline=False)
    embed.add_field(name=f'P2W POTION {emojis.POTION_P2W}', value=potion_p2w, inline=False)
    embed.add_field(name=f'WOOD POTION {emojis.POTION_WOOD}', value=potion_wood, inline=False)
    return embed


async def embed_alchemy_advanced() -> discord.Embed:
    """Alchemy advanced potions"""
    potion_cookie = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`55`% XP from all sources\n'
        f'{emojis.DETAIL} +`20`% pet encounter chance in {strings.SLASH_COMMANDS_EPIC_RPG["training"]}\n'
        f'{emojis.BP} **Duration**: `10`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `500` {emojis.ARENA_COOKIE}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL2} Level up faster in early TTs\n'
        f'{emojis.DETAIL} Get more pets in early TTs and/or with a horse below T10\n'
    )
    potion_dragon_breath = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`100`% dragon scales from {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.DETAIL2} +`30`% XP from all sources\n'
        f'{emojis.DETAIL2} +`5`% mob drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.DETAIL} +`60` {emojis.STAT_AT} AT\n'
        f'{emojis.BP} **Duration**: `14`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `35` {emojis.DRAGON_SCALE} + `500` {emojis.STAT_LIFE}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Get your dragon scales faster in areas 11-15\n'
    )
    potion_electronical = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`35`% random event spawn chance\n'
        f'{emojis.DETAIL2} +`30`% XP from all sources\n'
        f'{emojis.DETAIL2} +`30`% coins from all sources except selling & miniboss\n'
        f'{emojis.DETAIL2} -`30`% pet adventure time if pet returns while boost is active\n'
        f'{emojis.DETAIL2} +`25`% items from work commands\n'
        f'{emojis.DETAIL2} +`25`% items from {strings.SLASH_COMMANDS_EPIC_RPG["farm"]}\n'
        f'{emojis.DETAIL} +`20`% lootbox drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.DETAIL2} +`20`% mob drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.DETAIL} +`5`% item rarity from work commands\n'
        f'{emojis.BP} **Duration**: `1`d\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `2,222` {emojis.CHIP}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL2} Use in ultraining runs when you have the chips\n'
        f'{emojis.DETAIL} Get an auto flex in Navi\n'
    )
    potion_lootbox = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`35`% lootbox drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.DETAIL} +`1` lootbox rarity in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} **Duration**: `8`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `1` {emojis.LB_COMMON} + `1` {emojis.LB_UNCOMMON} '
        f'+ `1` {emojis.LB_RARE} + `1` {emojis.LB_EPIC} + `1` {emojis.LB_EDGY} + `1` {emojis.LB_OMEGA}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Get some help getting those 12 OMEGA lootboxes for D15-2\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ALCHEMY: ADVANCED POTIONS',
    )
    embed.add_field(name=f'COOKIE POTION {emojis.POTION_COOKIE}', value=potion_cookie, inline=False)
    embed.add_field(name=f'DRAGON BREATH POTION {emojis.POTION_DRAGON_BREATH}', value=potion_dragon_breath, inline=False)
    embed.add_field(name=f'ELECTRONICAL POTION {emojis.POTION_ELECTRONICAL}', value=potion_electronical, inline=False)
    embed.add_field(name=f'LOOTBOX POTION {emojis.POTION_LOOTBOX}', value=potion_lootbox, inline=False)
    return embed


async def embed_alchemy_endgame() -> discord.Embed:
    """Alchemy endgame potions"""
    potion_jumpy = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL} +`50`% chance to get an item from the VOID aura in areas 16-20\n'
        f'{emojis.BP} **Duration**: `2`d\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `1` {emojis.EPIC_JUMP}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Get ULTIMATE logs, SUPER fish and watermelons faster in VOID areas\n'
    )
    potion_king = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`250`% coins from all sources except selling & miniboss\n'
        f'{emojis.DETAIL2} +`50`% random event spawn chance\n'
        f'{emojis.DETAIL} +`35`% increased selling price of all items\n'
        f'{emojis.BP} **Duration**: `8`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `1t` {emojis.COIN} + `100k` {emojis.RUBY}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Make more money with **if** you can make a profit after brewing this\n'
    )
    potion_time = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL} You keep `7.5`% of the items in your inventory when time traveling\n'
        f'{emojis.BP} **Duration**: `5`m\n'
        f'{emojis.DETAIL} Only brew this potion right before you time travel!\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `42` {emojis.TIME_COOKIE}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL} Use right before TT to trade TIME cookies for more materials\n'
    )
    potion_void = (
        f'{emojis.BP} **Boosts**\n'
        f'{emojis.DETAIL2} +`300`% enchanting luck\n'
        f'{emojis.DETAIL2} +`50`% mob drop chance in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.DETAIL2} +`10`% is refunded when contributing items to areas 16-20\n'
        f'{emojis.DETAIL} +`2` lootbox rarity in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'and {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} **Duration**: `1`d `12`h\n'
        f'{emojis.BP} **Recipe**: `1` {emojis.FLASK} + `250` {emojis.DARK_ENERGY} + `1` {emojis.LOG_ULTIMATE} '
        f'+ `1` {emojis.FISH_SUPER} + `1` {emojis.WATERMELON}\n'
        f'{emojis.BP} **Possible use**\n'
        f'{emojis.DETAIL2} Save money enchanting in VOID areas\n'
        f'{emojis.DETAIL} Get dark energy faster in VOID areas\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ALCHEMY: ENDGAME POTIONS',
    )
    embed.add_field(name=f'JUMPY POTION {emojis.POTION_JUMPY}', value=potion_jumpy, inline=False)
    embed.add_field(name=f'KING POTION {emojis.POTION_KING}', value=potion_king, inline=False)
    embed.add_field(name=f'TIME POTION {emojis.POTION_TIME}', value=potion_time, inline=False)
    embed.add_field(name=f'VOID POTION {emojis.POTION_VOID}', value=potion_void, inline=False)
    return embed
