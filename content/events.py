# events.py

import discord

from resources import emojis, functions, settings, strings, views


# --- Events ---
# Personal events
EVENT_ENCHANT = 'Enchant'
EVENT_EPIC_GUARD = 'Epic guard'
EVENT_FARM = 'Farm (failed planting)'
EVENT_HEAL = 'Healing (mysterious man)'
EVENT_HUNT = 'Hunt (zombie horde)'
EVENT_LB_OPEN = 'Lootbox opening'
EVENT_RETURNING = 'Returning'
EVENT_TRADE = 'Special trade'
EVENT_TRAINING = 'Training (void)'
EVENT_WORK = 'Work (ruby dragon)'

EVENTS_PERSONAL = [
    EVENT_ENCHANT,
    EVENT_EPIC_GUARD,
    EVENT_FARM,
    EVENT_HEAL,
    EVENT_HUNT,
    EVENT_LB_OPEN,
    EVENT_RETURNING,
    EVENT_TRADE,
    EVENT_TRAINING,
    EVENT_WORK,
]

# Multiplayer events
EVENT_ARENA = 'Arena'
EVENT_COIN_DROP = 'Coin drop (god)'
EVENT_CATCH = 'Coin rain (catch)'
EVENT_CHOP = 'Epic tree (chop)'
EVENT_LEGENDARY_BOSS = 'Legendary Boss (time to fight)'
EVENT_LB_SUMMON = 'Lootbox summoning (summon)'
EVENT_FISH = 'Megalodon (fish)'
EVENT_MINIBOSS = 'Miniboss'
EVENT_RARE_HUNT_MONSTER = 'Rare hunt monster (pickaxe)'

EVENTS_MULTIPLAYER = [
    EVENT_ARENA,
    EVENT_COIN_DROP,
    EVENT_CATCH,
    EVENT_CHOP,
    EVENT_LEGENDARY_BOSS,
    EVENT_LB_SUMMON,
    EVENT_FISH,
    EVENT_MINIBOSS,
    EVENT_RARE_HUNT_MONSTER,
]

# Global events
EVENT_BIG_ARENA = 'Big arena'
EVENT_HORSE_RACE = 'Horse race'
EVENT_LOTTERY = 'Lottery'
EVENT_MININTBOSS = 'Minin\'tboss'
EVENT_TOURNAMENT = 'Pet tournament'

EVENTS_GLOBAL = [
    EVENT_BIG_ARENA,
    EVENT_HORSE_RACE,
    EVENT_LOTTERY,
    EVENT_MININTBOSS,
    EVENT_TOURNAMENT,
]

EVENTS_ALL = EVENTS_PERSONAL + EVENTS_MULTIPLAYER + EVENTS_GLOBAL
EVENTS_ALL.sort()

# Event types
EVENT_TYPES = [
    'All',
    'Global',
    'Multiplayer',
    'Personal',
]


# --- Commands ---
async def command_event_guide(ctx: discord.ApplicationContext, event: str) -> None:
    """Event guide command"""
    for event_check in EVENTS_ALL:
        if event.lower() in event_check.lower():
            event = event_check
            break
    else:
        await ctx.respond('I don\'t know an event with that name, sorry.', ephemeral=True)
        return
    events_functions = {
        EVENT_ARENA: embed_event_arena,
        EVENT_BIG_ARENA: embed_event_bigarena,
        EVENT_COIN_DROP: embed_event_coin_drop,
        EVENT_CATCH: embed_event_coinrain,
        EVENT_ENCHANT: embed_event_enchant,
        EVENT_EPIC_GUARD: embed_event_epicguard,
        EVENT_CHOP: embed_event_epictree,
        EVENT_FARM: embed_event_farm,
        EVENT_HEAL: embed_event_heal,
        EVENT_HORSE_RACE: embed_event_horserace,
        EVENT_HUNT: embed_event_hunt,
        EVENT_LEGENDARY_BOSS: embed_event_legendary,
        EVENT_LB_OPEN: embed_event_lootbox,
        EVENT_LB_SUMMON: embed_event_lootboxsummoning,
        EVENT_LOTTERY: embed_event_lottery,
        EVENT_FISH: embed_event_megalodon,
        EVENT_MINIBOSS: embed_event_miniboss,
        EVENT_MININTBOSS: embed_event_minintboss,
        EVENT_RARE_HUNT_MONSTER: embed_event_rare_hunt_monster,
        EVENT_TOURNAMENT: embed_event_pettournament,
        EVENT_TRADE: embed_event_specialtrade,
        EVENT_TRAINING: embed_event_training,
        EVENT_RETURNING: embed_event_returning,
        EVENT_WORK: embed_event_rubydragon,
    }
    view = views.TopicView(ctx, events_functions, active_topic=event, placeholder='Choose event ...')
    embed = await events_functions[event]()
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    try:
        await functions.edit_interaction(interaction, view=None)
    except discord.errors.NotFound:
        pass


# --- Redundancies ---
events_horse = 'A {emoji} T4+ horse will **not** save you if you die in an event'
events_personal = 'Only you can answer'
events_multiplayer = 'Anyone can join'
events_player_no = 'This is a {no} player event'
events_rare = 'This event is very rare'
events_first_one = 'Only the first one to answer gets the reward'
events_once_cycle = 'You can only join once per cycle'
events_official_server = 'The outcome is announced in the [official server](https://discord.gg/epicrpg)'


# --- Embeds: Personal Events ---
async def embed_event_enchant() -> discord.Embed:
    """Enchant event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["enchant"]}, {strings.SLASH_COMMANDS_EPIC_RPG["refine"]}, '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["transmute"]}, {strings.SLASH_COMMANDS_EPIC_RPG["transcend"]} (0.085 % chance)'
    )
    answers = (
        f'{emojis.BP} `cry`: Nothing happens but you won\'t get an enchant\n'
        f'{emojis.BP} `fix`: You get an enchant and either gain **or lose** 5 LIFE\n'
        f'{emojis.BP} `again`: Small chance to get an ULTRA-EDGY enchant, high chance to die'
    )
    safe_answer = f'{emojis.BP} `cry`'
    note = (
        f'{emojis.BP} {events_horse.format(emoji=emojis.HORSE_T4)}\n'
        f'{emojis.BP} Your gear doesn\'t break despite the event indicating this\n'
        f'{emojis.BP} {events_personal}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ENCHANT EVENT',
        description = (
            'This is a random personal event in which you accidentally "break" your equipment while enchanting it.'
        )
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='SAFEST ANSWER', value=safe_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_epicguard() -> discord.Embed:
    """Epic guard event"""
    trigger = (
        f'{emojis.BP} Most commands that have a cooldown, with the exception of multiplayer commands like '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["arena"]}, {strings.SLASH_COMMANDS_EPIC_RPG["duel"]}, '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["horse breeding"]} or {strings.SLASH_COMMANDS_EPIC_RPG["miniboss"]} '
        f'(chance unknown)'
    )
    answers = f'{emojis.BP} The emoji of the random item the guard shows you\n'
    jail = (
        f'{emojis.BP} If you answer wrong, you will be put in jail\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["jail"]} and then `protest`\n'
        f'{emojis.BP} Do not try to kill the guard, there is a high chance of losing XP\n'
        f'{emojis.BP} If you manage to kill the guard anyway, you will get 100 XP'
    )
    note = (
        f'{emojis.BP} You can lose XP in this event, but you can not die\n'
        f'{emojis.BP} You get some coins if you answer the question correctly\n'
        f'{emojis.BP} {events_personal}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EPIC GUARD EVENT',
        description = 'This is a random captcha event to prevent autotyping.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='REQUIRED ANSWER', value=answers, inline=False)
    embed.add_field(name='HOW TO GET OUT OF JAIL', value=jail, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_farm() -> discord.Embed:
    """Farm (failed planting) event"""
    trigger = f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["farm"]} (chance unknown)'
    answers = (
        f'{emojis.BP} `cry`: You get `1` crop and your seed back.\n'
        f'{emojis.BP} `plant another`: You get your seed back.\n'
        f'{emojis.BP} `fight`: Small chance to get `20` levels and your seed back, high chance to only get your seed back.'
    )
    rec_answer = f'{emojis.BP} `fight`'
    note = (
        f'{emojis.BP} This event is only available in {emojis.TIME_TRAVEL}TT `2`+\n'
        f'{emojis.BP} {events_personal}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'FARM EVENT',
        description = 'This is a random personal event in which your planted seed won\'t grow as expected.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='RECOMMENDED ANSWER', value=rec_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_heal() -> discord.Embed:
    """Heal event (mysterious man)"""
    trigger = f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["heal"]} (`0.75`% chance)'
    answers = (
        f'{emojis.BP} `cry`: The event ends, nothing happens\n'
        f'{emojis.BP} `search`: Leads to the option to `fight` the thief. If you do this, you will either '
        f'gain **or lose** a level'
    )
    safe_answer = f'{emojis.BP} `cry`'
    note = (
        f'{emojis.BP} This event will not trigger if you are at full LIFE before healing\n'
        f'{emojis.BP} {events_personal}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HEAL EVENT (MYSTERIOUS MAN)',
        description = 'This is a random personal event in which you encounter a mysterious man while healing yourself.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='SAFEST ANSWER', value=safe_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_lootbox() -> discord.Embed:
    """Lootbox opening event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["open"]} {emojis.LB_COMMON}{emojis.LB_UNCOMMON}{emojis.LB_RARE}'
        f'{emojis.LB_EPIC}{emojis.LB_EDGY} lootboxes (chance unknown)'
    )
    answers = (
        f'{emojis.BP} `cry`: You get a {emojis.LB_EPIC} EPIC, {emojis.LB_RARE} rare or '
        f'{emojis.LB_UNCOMMON} uncommon lootbox\n'
        f'{emojis.BP} `fight`: You destroy the lootbox and get `400` lootboxer XP\n'
        f'{emojis.BP} `magic spell`: Low chance to get an {emojis.LB_OMEGA} OMEGA lootbox, high chance to get nothing'
    )
    rec_answer = (
        f'{emojis.BP} `fight`'
    )
    note = f'{emojis.BP} {events_personal}'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LOOTBOX OPENING EVENT',
        description = 'This is a rare random personal event in which a lootboxes refuses to open.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='RECOMMENDED ANSWER', value=rec_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_rubydragon() -> discord.Embed:
    """Work event (ruby dragon)"""
    trigger = (
        f'{emojis.BP} Work commands (chance unknown)\n'
        f'{emojis.DETAIL} The {emojis.ARTIFACT_SHINY_PICKAXE} shiny pickaxe artifact increases the spawn chance for `mine` commands by `x10`'
    )
    answers = (
        f'{emojis.BP} `cry`: The event ends, you get `1` {emojis.ARENA_COOKIE} arena cookie\n'
        f'{emojis.BP} `move`: You move to phase 2 and spawn the ruby dragon (see below)\n'
        f'{emojis.BP} `sleep`: The event ends, you get nothing'
    )
    answers_ruby = (
        f'{emojis.BP} `run`: You get nothing\n'
        f'{emojis.BP} `fight`: You get `1` {emojis.DRAGON_ESSENCE} dragon essence and `25 x [TT count]` {emojis.RUBY} rubies\n'
        f'{emojis.BP} `sleep`: You get `5 x [TT count]` {emojis.RUBY} rubies'
    )
    best_answer = (
        f'{emojis.BP} First `move`, then `fight`\n'
    )
    note = (
        f'{emojis.BP} You actually _do_ move to another area, so you have to move back to your previous area '
        f'after the event\n'
        f'{emojis.BP} This event is not available in the TOP\n'
        f'{emojis.BP} {events_personal}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'WORK EVENT (RUBY DRAGON)',
        description = 'This is a random personal event in which you don\'t find any materials when working... '
        f'but a ruby dragon instead.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS (PHASE 1)', value=answers, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS (PHASE 2)', value=answers_ruby, inline=False)
    embed.add_field(name='BEST ANSWERS', value=best_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed



# --- Embeds: Multiplayer events ---
async def embed_event_arena() -> discord.Embed:
    """Arena event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["arena"]} to start the event alone\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["arena"]} `user[1-9]` to start the event with up to 9 people '
        f'for greater rewards\n'
        f'{emojis.BP} You can only mention users if their cooldown is ready\n'
        f'{emojis.BP} This will use up the cooldown of every player mentioned'
    )
    answers = (
        f'{emojis.BP} Click `yes` if you got mentioned\n'
        f'{emojis.BP} Click ⚔️ if you are a participant'
    )
    rewards = (
        f'{emojis.BP} {emojis.ARENA_COOKIE} cookies if you kill <6 people\n'
        f'{emojis.BP} {emojis.ARENA_COOKIE} cookies and {emojis.TIME_COOKIE} TIME cookies if you kill 6+ people\n'
    )
    # Calculation is a mess, unclear how lume calculates it, because this is clearly wrong if boosted
    rewards_ = (
        f'{emojis.BP} `3` {emojis.ARENA_COOKIE} per player mentioned\n'
        f'{emojis.BP} +`1` {emojis.ARENA_COOKIE} per kill if you kill <6 people\n'
        f'{emojis.BP} +`3` {emojis.ARENA_COOKIE} and +`1` {emojis.TIME_COOKIE} per kill if you kill 6+ people\n'
        f'{emojis.BP} +`3` {emojis.ARENA_COOKIE} for the one who starts the arena\n'
    )
    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=10)}\n'
        f'{emojis.BP} Requires at least 2 players, otherwise it will cancel\n'
        f'{emojis.BP} The outcome is completely random\n'
        f'{emojis.BP} This event shares its cooldown with `big arena`'
    )
    whichone = f'{emojis.BP} `big arena` has higher rewards than `arena`'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ARENA EVENT',
        description =   f'This is a multiplayer event in which up to 10 players fight each other.'
    )
    embed.add_field(name='HOW TO START', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ARENA OR BIG ARENA?', value=whichone, inline=False)
    return embed


async def embed_event_coinrain() -> discord.Embed:
    """Coin rain event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'and work commands (chance unknown)\n'
        f'{emojis.BP} By using a {emojis.COIN_TRUMPET} coin trumpet from the EPIC shop'
    )
    answers = f'{emojis.BP} `catch`'
    rewards = (
        f'{emojis.BP} {emojis.COIN} coins\n'\
        f'{emojis.DETAIL} The amount depends on the level of the player who triggered it, the amount of people that '
        f'participate and some RNG\n'
        f'{emojis.BP} There is a small chance for one player to get lucky\n'
        f'{emojis.DETAIL} Getting lucky means getting more {emojis.COIN} coins than the others\n'
    )
    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=20)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'COIN RAIN EVENT',
        description = 'This is a multiplayer event in which up to 20 players can catch coins falling from the sky.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_epictree() -> discord.Embed:
    """Epic tree event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'and work commands (chance unknown)\n'
        f'{emojis.BP} By using an {emojis.EPIC_SEED} epic seed from the EPIC shop'
    )
    answers = f'{emojis.BP} `chop`'
    rewards = (
        f'{emojis.BP} {emojis.LOG} wooden logs\n'
        f'{emojis.DETAIL} The amount depends on the amount of people that participate and some RNG\n'
        f'{emojis.BP} There is a small chance for one player to get lucky\n'
        f'{emojis.DETAIL} Getting lucky means getting more {emojis.LOG} logs than the others\n'
    )
    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=20)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EPIC TREE EVENT (CHOP)',
        description = 'This is a multiplayer event in which you can chop yourself some logs from a huge tree.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_coin_drop() -> discord.Embed:
    """Coin drop (god) event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'and work commands (chance unknown)'
    )
    answers = (
        f'{emojis.BP} The phrase god asks for\n'
        f'{emojis.BP} For a list of all possible phrases see the '
        f'[Wiki](https://epic-rpg.fandom.com/wiki/Events#God_Events)'
    )
    rewards = (
        f'{emojis.BP} {emojis.COIN} Coins (amount depends on your level)\n'
        f'{emojis.BP} `1` {emojis.EPIC_COIN} EPIC coin'
    )
    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_first_one}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'COIN DROP EVENT',
        description = 'This is a random multiplayer event in which god gets clumsy and drops some coins that one '
        f'player can snatch up.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='REQUIRED ANSWER', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_legendary() -> discord.Embed:
    """Legendary boss event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'and work commands (chance unknown)'
    )
    answers = f'{emojis.BP} `time to fight`'
    rewards = (
        f'{emojis.BP} +`1` level for every participant if successful\n'
        f'{emojis.BP} `10`% chance to get {emojis.TIME_COOKIE} TIME cookies\n'
    )
    note = (
        f'{emojis.BP} {events_rare}\n'
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=20)}\n'
        f'{emojis.BP} The chance to beat the boss is very low'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LEGENDARY BOSS EVENT',
        description = 'This is a rare random multiplayer event in which a legendary boss spawns and up to 20 '
        f'players can defeat it.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_lootboxsummoning() -> discord.Embed:
    """Lootbox summoning event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'and work commands (chance unknown)\n'
        f'{emojis.BP} By using a {emojis.GUILD_TOOTHBRUSH} legendary toothbrush'
    )
    answers = f'{emojis.BP} `summon`'
    rewards = (
        f'{emojis.BP} A lootbox for every player that entered\n'
        f'{emojis.DETAIL} The lootbox tier depends on the amount of players that participate\n'
        f'{emojis.DETAIL} The lootbox tier ranges from {emojis.LB_COMMON} common to {emojis.LB_EDGY} EDGY\n'
        f'{emojis.BP} There is a small chance for one player to get lucky\n'
        f'{emojis.DETAIL} Getting lucky means getting more rewards than the others\n'
    )
    note = (
        f'{emojis.BP} {events_rare}\n'
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=20)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LOOTBOX SUMMONING EVENT',
        description = 'This is a rare random multiplayer event in which a lootbox gets summoned and up to 20 '
        f'players can help to do so.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_megalodon() -> discord.Embed:
    """Megalodon event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'and work commands (chance unknown)\n'
        f'{emojis.BP} By using an {emojis.ULTRA_BAIT} ultra bait from the EPIC shop'
    )
    answers = f'{emojis.BP} `fish`'
    rewards = (
        f'{emojis.BP} {emojis.FISH} normie fish\n'
        f'{emojis.DETAIL} The amount depends on the amount of people that participate and some RNG\n'
        f'{emojis.BP} There is a small chance for one player to get lucky\n'
        f'{emojis.DETAIL} Getting lucky means getting more {emojis.FISH} fish than the others\n'
    )
    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=20)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MEGALODON EVENT (FISH)',
        description = 'This is a multiplayer event in which a megalodon spawns in the river and up to 20 '
        f'players can get some fish.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_miniboss() -> discord.Embed:
    """Miniboss event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["miniboss"]} to start the event alone\n'
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["miniboss"]} `user[1-9]` to start the event with up to 9 people '
        f'for greater rewards\n'
        f'{emojis.BP} You can only mention users if their cooldown is ready\n'
        f'{emojis.BP} This will use up the cooldown of every player mentioned'
    )
    answers = (
        f'{emojis.BP} Click `yes` if you got mentioned\n'
        f'{emojis.BP} Click 🗡️ if you are a participant'
    )
    rewards = (
        f'{emojis.BP} {emojis.COIN} Coins\n'
        f'{emojis.BP} `2.5`% chance for the initiator(s) to get +`1` level\n'
        f'{emojis.BP} The initiator reward depends on the level of the initiator and the users mentioned. '
        f'It depends most on the original initiator however, thus the player with the highest level should '
        f'start the event.\n'
        f'{emojis.BP} Participants get `5`% of the iniators\' reward, up to `5,000` coins if there is only one initiator. '
        f'This maximum amount increases with more initiators.'
    )
    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=10)}\n'
        f'{emojis.BP} This event shares its cooldown with {strings.SLASH_COMMANDS_EPIC_RPG["dungeon"]}\n'
        f'{emojis.BP} This event shares its cooldown with {strings.SLASH_COMMANDS_EPIC_RPG["minintboss"]}\n'
        f'{emojis.BP} The chance increases by `5`% for every participant'
    )
    whichone = (
        f'{emojis.BP} Only do this event if you don\'t need to do a dungeon\n'
        f'{emojis.BP} Minin\'tboss rewards dragon scales instead of coins'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MINIBOSS EVENT',
        description = 'This is a multiplayer event in which you fight a miniboss to get coins.'
    )
    embed.add_field(name='HOW TO START', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='DUNGEON OR MINIBOSS OR NOT SO MININ\'TBOSS?', value=whichone, inline=False)
    return embed


async def embed_event_specialtrade() -> discord.Embed:
    """Special trade event"""
    trigger = (
        f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, {strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} '
        f'and work commands (chance unknown)'
    )
    answers = (
        f'{emojis.BP} The phrase the epic NPC asks for\n'
        f'{emojis.BP} Note: You need the items for the trade in your inventory'
    )
    rewards = (
        f'{emojis.BP} `1` {emojis.WOLF_SKIN} wolf skin (for `15` {emojis.LOG} wooden logs)\n'
        f'{emojis.BP} `3` {emojis.EPIC_COIN} EPIC coins (for `3` {emojis.COIN} coins)\n'
        f'{emojis.BP} `3` {emojis.LB_EPIC} EPIC lootboxes (for `5` {emojis.LIFE_POTION} life potions)\n'
        f'{emojis.BP} `40` {emojis.FISH_GOLDEN} golden fish (for `15` {emojis.LIFE_POTION} life potions)\n'
        f'{emojis.BP} `80` {emojis.LOG_EPIC} EPIC logs (for `40` {emojis.LOG} wooden logs)\n'
        f'{emojis.BP} `80` {emojis.FISH} normie fish (for `2` {emojis.ARENA_COOKIE} cookies)\n'
        f'{emojis.BP} `125` {emojis.ARENA_COOKIE} cookies (for `5` {emojis.FISH} normie fish)\n'
    )
    note = (
        f'{emojis.BP} You have time to trade to the required material while the event is active\n'
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_first_one}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'SPECIAL TRADE EVENT',
        description = 'This is a random multiplayer event in which the epic NPC appears and offers one player a '
        f'(very good) trade.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='REQUIRED ANSWER', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


# --- Embeds: Global Events ---
async def embed_event_bigarena() -> discord.Embed:
    """Big arena event"""
    schedule = f'{emojis.BP} Monday, Wednesday, Friday at 18:00 UTC'
    answers = f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["big arena"]} (unlocked in area 7)'
    rewards = (
        f'{emojis.BP} ~`1000`+ {emojis.ARENA_COOKIE} arena cookies for the winner\n'
        f'{emojis.BP} ~`200`+ {emojis.ARENA_COOKIE} arena cookies for second and third place\n'
        f'{emojis.BP} ~`30`+ {emojis.ARENA_COOKIE} arena cookies for everyone else'
    )
    note = (
        f'{emojis.BP} {events_official_server}\n'
        f'{emojis.BP} {events_once_cycle}\n'
        f'{emojis.BP} This event shares its cooldown with {strings.SLASH_COMMANDS_EPIC_RPG["arena"]}'
    )
    whichone = f'{emojis.BP} Big arena has higher rewards than unboosted arena'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'BIG ARENA EVENT',
        description = 'This is a global event which takes place three times a week.'
    )
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ARENA OR BIG ARENA?', value=whichone, inline=False)
    return embed


async def embed_event_horserace() -> discord.Embed:
    """Horse race event"""
    schedule = f'{emojis.BP} Every even hour (= every 2 hours)'
    answers = f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["horse race"]} (unlocked with a {emojis.HORSE_T5} T5+ horse)'
    rewards = (
        f'{emojis.BP} T5 - T8: A random lootbox, +`1` horse level or +`1` horse tier\n'
        f'{emojis.BP} T9: A random lootbox, a pet (up to T3), +`1` horse level or +`1` horse tier\n'
        f'{emojis.BP} T10: Up to 3 lootboxes or a pet (up to T5)\n'
        f'{emojis.BP} You **only** get rewards if you place third or higher'
    )
    note = (
        f'{emojis.BP} {events_official_server}\n'
        f'{emojis.BP} {events_once_cycle}\n'
        f'{emojis.BP} This event shares its cooldown with {strings.SLASH_COMMANDS_EPIC_RPG["horse breeding"]}\n'
        f'{emojis.BP} Your chance to win is heavily influenced by your horse\'s level'
    )
    whichone = f'{emojis.BP} Unless your horse is {emojis.HORSE_T10} T10, breed instead'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSE RACE EVENT',
        description = 'This is a global event which takes place every 2 hours.'
    )
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='RACE OR BREED?', value=whichone, inline=False)
    return embed


async def embed_event_pettournament() -> discord.Embed:
    """Pet tournament event"""
    schedule = f'{emojis.BP} Every 12 hours at 08:00 / 20:00 UTC'
    answers = f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["pets tournament"]}'
    rewards = (
        f'{emojis.BP} +`1` pet tier\n'
        f'{emojis.BP} You only get the reward if you **win** the tournament'
    )
    note = (
        f'{emojis.BP} {events_official_server}\n'
        f'{emojis.BP} {events_once_cycle}\n'
        f'{emojis.BP} You can only enter `1` pet per cycle.\n'
        f'{emojis.DETAIL} Entering a pet will replace an already entered pet.\n'
        f'{emojis.BP} You can apply with any pet, even pets on adventures\n'
        f'{emojis.BP} Your chance to win is influenced by your pet\'s score (see {strings.SLASH_COMMANDS_GUIDE["pets guide"]})\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'PET TOURNAMENT EVENT',
        description = 'This is a global event which takes place every 12 hours.'
    )
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_lottery() -> discord.Embed:
    """Lottery event"""
    schedule = f'{emojis.BP} Every 12 hours at 00:00 / 12:00 UTC'
    answers = f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["lottery"]} `amount: [1-200]`'
    rewards = (
        f'{emojis.BP} A huge amount of {emojis.COIN} coins if you win\n'
        f'{emojis.BP} Absolutely nothing if you don\'t'
    )
    note =(
        f'{emojis.BP} {events_official_server}\n'
        f'{emojis.BP} You can buy up to 200 lottery tickets for each draw\n'
        f'{emojis.BP} The size of the pot depends on ticket prices and tickets sold\n'
        f'{emojis.BP} The ticket prices are different with every lottery'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LOTTERY EVENT',
        description = 'This is a global event which takes place every 12 hours.'
    )
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_minintboss() -> discord.Embed:
    """Not so mini boss event"""
    schedule = f'{emojis.BP} Tuesday, Thursday, Saturday at 18:00 UTC'
    answers = f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["minintboss"]} (unlocked in area 10)'
    rewards = f'{emojis.BP} 11-13 {emojis.DRAGON_SCALE} dragon scales **if** the boss dies'
    note = (
        f'{emojis.BP} {events_official_server}\n'
        f'{emojis.BP} {events_once_cycle}\n'
        f'{emojis.BP} This event shares its cooldown with {strings.SLASH_COMMANDS_EPIC_RPG["miniboss"]} and '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["dungeon"]}\n'
        f'{emojis.BP} This event has a `20`% chance to fail'
    )
    whichone = (
        f'{emojis.BP} Only do this event if you don\'t need to do a dungeon\n'
        f'{emojis.BP} Miniboss rewards coins instead of dragon scales'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MININ\'TBOSS EVENT',
        description = 'This is a global event which takes place three times a week.'
    )
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='DUNGEON OR MINIBOSS OR MININ\'TBOSS?', value=whichone, inline=False)
    return embed


async def embed_event_hunt() -> discord.Embed:
    """Hunt event embed"""
    trigger = f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} in areas 3+ (chance unknown)'
    answers = (
        f'{emojis.BP} `cry`: The zombie horde walks away, you get nothing\n'
        f'{emojis.BP} `fight`: Small chance to get `1` coin and _almost_ `1` level, high chance to get nothing\n'
        f'{emojis.BP} `join`: You move to area `2` with the horde and get `5`-`7` {emojis.ZOMBIE_EYE} zombie eyes'
    )
    rec_answer = (
        f'{emojis.BP} `join` if you need the zombie eyes\n'
        f'{emojis.BP} `fight` otherwise\n'
    )
    note = (
        f'{emojis.BP} You actually _do_ move to area 2 if you choose `join`\n'
        f'{emojis.BP} {events_personal}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HUNT EVENT (ZOMBIE HORDE)',
        description = 'This is a rare random personal event in which you encounter a zombie horde.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='RECOMMENDED ANSWER', value=rec_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_training() -> discord.Embed:
    """Training event embed"""
    trigger = f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["training"]} in areas 16+ (chance unknown)'
    answers = (
        f'{emojis.BP} `cry`: A mysterious player saves you, you get nothing\n'
        f'{emojis.BP} `fly`: High chance to die and lose a level, low chance to get a lot of {emojis.DARK_ENERGY} dark energy\n'
        f'{emojis.BP} `teleport`: High chance to set your commands on random cooldowns. No other outcome known so far.'
    )
    rec_answer = (
        f'{emojis.BP} `fly` if you need the dark energy as losing one level is peanuts\n'
        f'{emojis.BP} `cry` otherwise\n'
    )
    note = (
        f'{emojis.BP} Your training cooldown is not used up by this event\n'
        f'{emojis.BP} {events_personal}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TRAINING EVENT (VOID)',
        description = 'This is a rare random personal event in which you fall into the void. Mind yer step, will ya?'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='RECOMMENDED ANSWER', value=rec_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_slime() -> discord.Embed:
    """Halloween: Bat slime event"""
    trigger = (
        f'{emojis.BP} By crafting a {emojis.HAL_CANDY_BAIT} candy bait'
    )
    answers = (
        f'{emojis.BP} `fight`: Get `3`-`6` {emojis.HAL_SPOOKY_ORB} spooky orbs\n'
        f'{emojis.BP} `boo`: Get `2`-`8` {emojis.HAL_SPOOKY_ORB} spooky orbs'
    )
    best_answer = (
        f'{emojis.BP} If you don\'t feel like gambling, `fight` is the safer answer\n'
        f'{emojis.BP} If you _do_ feel like gambling, `boo` has the higher potential rewards'
    )
    note =(
        f'{emojis.BP} You always get orbs, even if you let the event time out'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HALLOWEEN: BAT SLIME EVENT',
        description = (
            f'This is a random personal halloween event in which you spawn three {emojis.HAL_BAT_SLIME} bat slimes.'
        )
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='BEST ANSWER', value=best_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_scroll_boss() -> discord.Embed:
    """Halloween: Scroll boss event"""
    trigger = (
        f'{emojis.BP} By crafting a {emojis.HAL_SPOOKY_SCROLL} spooky scroll'
    )
    tactics = (
        f'{emojis.BP} Attack from **ahead**: `apple`\n'
        f'{emojis.BP} Attack from the **left**: `pumpkin`\n'
        f'{emojis.BP} Attack from the **right**: `t pose`\n'
        f'{emojis.BP} Attack from **behind**: `dodge`\n'
    )
    rewards_win = (
        f'{emojis.BP} `200` {emojis.HAL_PUMPKIN} pumpkins\n'
        f'{emojis.BP} `100` {emojis.ARENA_COOKIE} arena cookies\n'
        f'{emojis.BP} `2` {emojis.LB_EDGY} EDGY lootboxes\n'
    )
    rewards_lose = (
        f'{emojis.BP} `150` {emojis.HAL_PUMPKIN} pumpkins\n'
        f'{emojis.BP} `80` {emojis.ARENA_COOKIE} arena cookies\n'
        f'{emojis.BP} `1` {emojis.LB_EDGY} EDGY lootboxes\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HALLOWEEN: PUMPKIN BAT BOSS (SCROLL BOSS) EVENT',
        description = (
            f'This is a personal halloween event in which you spawn a {emojis.HAL_BOSS} pumpkin bat boss.\n'
            f'This boss is also called "scroll boss".\n'
        )
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='TACTICS', value=tactics, inline=False)
    embed.add_field(name='REWARDS IF YOU WIN', value=rewards_win, inline=False)
    embed.add_field(name='REWARDS IF YOU LOSE', value=rewards_lose, inline=False)
    return embed


async def embed_event_returning() -> discord.Embed:
    """Returning event"""
    activities = (
        f'{emojis.BP} Get {emojis.COIN_SMOL} smol coins in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} and all work commands\n'
        f'{emojis.BP} Complete the event quest to get several rewards '
        f'(see {strings.SLASH_COMMANDS_EPIC_RPG["returning quest"]})\n'
        f'{emojis.BP} Claim a reward from the super-daily every day '
        f'(see {strings.SLASH_COMMANDS_EPIC_RPG["returning superdaily"]})\n'
        f'{emojis.BP} Buy various rewards in the {strings.SLASH_COMMANDS_EPIC_RPG["returning shop"]}\n'
    )
    bonuses = (
        f'{emojis.BP} All command cooldowns except {strings.SLASH_COMMANDS_EPIC_RPG["vote"]}, '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["guild raid"]} and {strings.SLASH_COMMANDS_EPIC_RPG["guild upgrade"]} '
        f'are reduced by `33`%\n'
        f'{emojis.BP} You can enter all dungeons without buying a dungeon key\n'
        f'{emojis.BP} The drop chance of mob drops is doubled (see {strings.SLASH_COMMANDS_GUIDE["monster drops"]})\n'
    )
    schedule = (
        f'{emojis.BP} Event starts when you use a command after being inactive for at least 2 months\n'
        f'{emojis.BP} Event ends 7 days after it started\n'
    )
    tldr_guide = (
        f'{emojis.BP} Make sure to use {strings.SLASH_COMMANDS_EPIC_RPG["returning superdaily"]} every day\n'
        f'{emojis.BP} Play the game (welcome back!)\n'
    )
    note = (
        f'{emojis.BP} No, it\'s not worth going afk for 2 months to trigger this event\n'
        f'{emojis.BP} This is a personal event with no fixed schedule\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'RETURNING EVENT {emojis.EPIC_RPG_LOGO}',
        description = f'The returning event is an event for people that haven\'t played for at least 2 months'
    )
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_event_rare_hunt_monster() -> discord.Embed:
    """Rare hunt monster event embed"""
    trigger = f'{emojis.BP} {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} in areas 1~10 (chance unknown)'
    answers = f'{emojis.BP} `lets get that pickaxe`'
    rewards = (
        f'{emojis.BP} {emojis.ARTIFACT_SHINY_PICKAXE_PART_A} Shiny pickaxe part A from {emojis.MOB_GOLDEN_WOLF} golden wolf in areas 1~2\n'
        f'{emojis.BP} {emojis.ARTIFACT_SHINY_PICKAXE_PART_B} Shiny pickaxe part B from {emojis.MOB_RUBY_ZOMBIE} ruby zombie in areas 3~4\n'
        f'{emojis.BP} {emojis.ARTIFACT_SHINY_PICKAXE_PART_C} Shiny pickaxe part C from {emojis.MOB_DIAMOND_UNICORN} diamond unicorn in areas 5~6\n'
        f'{emojis.BP} {emojis.ARTIFACT_SHINY_PICKAXE_PART_D} Shiny pickaxe part D from {emojis.MOB_EMERALD_MERMAID} emerald mermaid in areas 7~8\n'
        f'{emojis.BP} {emojis.ARTIFACT_SHINY_PICKAXE_PART_E} Shiny pickaxe part E from {emojis.MOB_SAPPHIRE_KILLER_ROBOT} sapphire killer robot in areas 9~10\n'
    )
    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=20)}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'RARE HUNT MONSTER (PICKAXE)',
        description = 'This is a multiplayer event in which you can get an artifact part from a rare hunt monster.'
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed