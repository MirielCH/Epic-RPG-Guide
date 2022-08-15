# horse_festival.py
"""Contains all horse festival guides"""

import discord
from cogs.horse_festival_old import embed_megarace

from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_MEGARACE = 'Megarace'
TOPIC_MINIRACE = 'Minirace'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_MEGARACE,
    TOPIC_MINIRACE,
]


# --- Commands ---
async def command_horse_festival_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Horse festival guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_overview,
        TOPIC_MEGARACE: embed_megarace,
        TOPIC_MINIRACE: embed_minirace,
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
async def embed_overview() -> discord.Embed:
    """Horse overview embed"""
    activities = (
        f'{emojis.BP} Get 25 {emojis.HORSESHOE} horseshoes each day in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]} and all fish command tiers\n'
        f'{emojis.BP} Get {emojis.HORSESHOE} horseshoes and {emojis.HORSESHOE_GOLDEN} golden horseshoes in the daily '
        f'and weekly **tasks** (see {emojis.EPIC_RPG_LOGO_SMALL}`/hf tasks`)\n'
        #f'{emojis.BP} Play in the daily **minirace** (see topic `Minirace`)\n'
        f'{emojis.BP} Play in the weekly **megarace** (see topic `Megarace`)\n'
        f'{emojis.BP} Defeat the {emojis.HORSLIME} **horslime** in {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]} '
        f'(drops 1 {emojis.OMEGA_HORSE_TOKEN} OMEGA horse token)\n'
        f'{emojis.BP} Complete the **quest** to get the {emojis.PET_PONY} pony pet (see {emojis.EPIC_RPG_LOGO_SMALL}`/hf quest`)\n'
        f'{emojis.BP} Buy stuff in the event shop (see {emojis.EPIC_RPG_LOGO_SMALL}`/hf shop`)\n'
    )
    bonuses = (
        f'{emojis.BP} Horse breed cooldown is reduced by 35%\n'
        f'{emojis.BP} You can use {emojis.EPIC_RPG_LOGO_SMALL}`/hf lightspeed` to reduce your active cooldowns by half.\n'
        f'{emojis.BLANK} This consumes 1 {emojis.OMEGA_HORSE_TOKEN} OMEGA horse token and your horse cooldown.\n'
        f'{emojis.BLANK} This does not affect `vote` and `guild`.\n'
    )
    whattodo = (
        #f'{emojis.BP} Play in the minirace every day\n'
        f'{emojis.BP} Do megarace whenever a stage is available\n'
        f'{emojis.BP} Optional: Melt 1 {emojis.STEEL} and craft the {emojis.COWBOY_ARMOR}{emojis.COWBOY_SWORD} cowboy gear.\n'
        f'{emojis.BLANK} This will increase your chance to encounter the {emojis.HORSLIME} horslime to 0.6%.\n'
        f'{emojis.BLANK} Materials required: 25 {emojis.HORSESHOE}\n'
        f'{emojis.BP} Melt 21 {emojis.STEEL} and 4 {emojis.GOLD} and craft the {emojis.HORSE_ARMOR} horse armor.\n'
        f'{emojis.BLANK} This will increase your luck in the megarace.\n'
        f'{emojis.BLANK} Materials required: 525 {emojis.HORSESHOE} and 8 {emojis.HORSESHOE_GOLDEN}\n'
        f'{emojis.BP} Complete the event quest and get showered in stuff'
    )
    chances = (
        f'{emojis.BP} 0.5% to encounter a {emojis.HORSLIME} with {strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}\n'
        f'{emojis.BLANK} 0.05% extra chance with each cowboy item, so 0.6% chance max\n'
    )
    schedule = (
        f'{emojis.BP} Event started on August 1, 2022\n'
        f'{emojis.BP} Event ends on August 21, 2022, 23:55 UTC\n'
        f'{emojis.BP} Items will vanish on August 28, 2022, with the exception of the {emojis.GODLY_HORSE_TOKEN} '
        f'GODLY horse token'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'HORSE FESTIVAL EVENT 2022 {emojis.HORSE_T10}',
        description = 'Neigh?'
    )
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='WHAT TO DO FIRST', value=whattodo, inline=False)
    embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed


async def embed_megarace() -> discord.Embed:
    """Megarace embed"""
    overview = (
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/hf megarace action: start` to start a stage\n'
        f'{emojis.BP} Every megarace has 9 stages and resets weekly\n'
        f'{emojis.BP} Every stage you will encounter 3 random events and have to choose what to do\n'
        f'{emojis.BP} The cooldown of the next stage depends on your answers\n'
    )
    best_answers_1 = (
        f'{emojis.BP} Ancient Racer: **C**\n'
        f'{emojis.BP} Annoying Racer: **B** (**C** for gamblers)\n'
        f'{emojis.BP} Asteroid: **A** (**C** for gamblers)\n'
        f'{emojis.BP} Black Hole: **C** (**A** for gamblers)\n'
        f'{emojis.BP} Bottleneck: **C**\n'
        f'{emojis.BP} Cliff: **B**\n'
        f'{emojis.BP} Cooldown: **A**\n'
        f'{emojis.BP} Dinosaur: **C**\n'
        f'{emojis.BP} EPIC Dealer: **C** (**A** for gamblers)\n'
        f'{emojis.BP} EPIC Guards: **A** (**B** for gamblers)\n'
        f'{emojis.BP} EPIC Horse Trainer: **A** or **C**\n'
        f'{emojis.BP} EPIC NPC: **C**\n'
        f'{emojis.BP} Giant Life Potion: **C**\n'
        f'{emojis.BP} Horseless Racer: **B**\n'
        f'{emojis.BP} Hot Air Balloons: **B**\n'
        f'{emojis.BP} Injured Racers: **C**\n'
        f'{emojis.BP} Legendary Boss: **A** (**C** for gamblers)\n'
    )
    best_answers_2 = (
        f'{emojis.BP} Legendary Boss: **A** (**C** for gamblers)\n'
        f'{emojis.BP} Many Horses: **B**\n'
        f'{emojis.BP} Mountains: **C**\n'
        f'{emojis.BP} Mysterious Racer: All answers are the same\n'
        f'{emojis.BP} Nothing: **A**\n'
        f'{emojis.BP} Party: **B** (**A** for gamblers)\n'
        f'{emojis.BP} Plane: **A** (**B** for gamblers)\n'
        f'{emojis.BP} Quicksand: **C**\n'
        f'{emojis.BP} Racer ^ -1: **A** (**C** for gamblers)\n'
        f'{emojis.BP} Rainy: **A**\n'
        f'{emojis.BP} Sandstorm: **B**\n'
        f'{emojis.BP} Snowy: **C**\n'
        f'{emojis.BP} Sus: **B** (**A** for gamblers)\n'
        f'{emojis.BP} Suspicious Horse: **B**\n'
        f'{emojis.BP} Sleepy: **A** (**B** for gamblers)\n'
        f'{emojis.BP} Team: **B** (**A** for gamblers)\n'
        f'{emojis.BP} Waterfall: **A** (**B** for gamblers)\n'
        f'{emojis.BP} World Border: **A**\n'
        f'{emojis.BP} Zombie Horde: **B**\n'
    )
    note = (
        f'{emojis.BP} The answers for gamblers are better **if** you get lucky, otherwise they are worse\n'
        f'{emojis.BP} If you want to choose those, get a {emojis.HORSE_ARMOR} horse armor first\n'
    )
    megarace_boost = (
        f'{emojis.BP} You can find a boost in commands while you are in a megarace\n'
        f'{emojis.BP} If you accept it, it will slightly lower or increase your remaining time\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MEGARACE',
        description = 'This race makes perfect sense.'
    )
    embed.add_field(name='OVERVIEW', value=overview, inline=False)
    embed.add_field(name='SHORTEST ANSWERS (1)', value=best_answers_1, inline=False)
    embed.add_field(name='SHORTEST ANSWERS (2)', value=best_answers_2, inline=False)
    embed.add_field(name=f'MEGARACE BOOST {emojis.MEGARACE_BOOST}', value=megarace_boost, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_minirace() -> discord.Embed:
    """Minirace embed"""
    overview = (
        f'{emojis.BP} Miniraces are 16 player knockout tournaments\n'
        f'{emojis.BP} There are 4 rounds in every minirace\n'
        f'{emojis.BP} Every round lasts up to one day\n'
        f'{emojis.BP} You can do one round a day\n'
    )
    howtoplay = (
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/hf minirace` to check your minirace or join one\n'
        f'{emojis.BP} If your round is ready, the game will notify you\n'
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/hf minirace` again to choose an action\n'
        f'{emojis.BP} Use {emojis.EPIC_RPG_LOGO_SMALL}`/hf minirace` after the round ended to see the players\n'
    )
    actions = (
        f'{emojis.BP} `RIDE` vs `SUS`: `RIDE` has higher chance to win\n'
        f'{emojis.BP} `SUS` vs `SPEEDRUN`: `SUS` has higher chance to win\n'
        f'{emojis.BP} `SPEEDRUN` vs `RIDE`: `SPEEDRUN` has higher chance to win\n'
        f'{emojis.BP} `RIDE` vs `RIDE`: Winner is RNG\n'
        f'{emojis.BP} `SUS` vs `SUS`: Both players lose\n'
        f'{emojis.BP} `SPEEDRUN` vs `SPEEDRUN`: Player with lower horse fatigue wins.\n'
        f'{emojis.BLANK} If both players have the same value, winner is RNG.\n'
        f'{emojis.BP} If your opponent doesn\'t answer, you win\n'
    )
    debuffs = (
        f'{emojis.BP} Suspiciousness lowers the chance to win using `SUS`\n'
        f'{emojis.BLANK} `SPEEDRUN` lowers your suspiciousness greatly\n'
        f'{emojis.BLANK} `RIDE` lowers your suspiciousness slightly\n'
        f'{emojis.BP} Horse fatigue lowers the chance to win using `SPEEDRUN`\n'
        f'{emojis.BLANK} `SUS` lowers your horse fatigue greatly\n'
        f'{emojis.BLANK} `RIDE` lowers your horse fatigue slightly\n'
    )
    round_win = (
        f'{emojis.BP} If you win a round, you will stay in the minirace.\n'
        f'{emojis.BLANK} You can fight the next round next day.\n'
        f'{emojis.BP} If you lose a round, you will drop out of the minirace.\n'
        f'{emojis.BLANK} You can join a new minirace next day.\n'
    )
    race_win = (
        f'{emojis.BP} If you win a tournament, you advance a tier and get 1 {emojis.SLEEPY_POTION}.\n'
        f'{emojis.BLANK} Higher tiered tournaments play exactly the same.\n'
        f'{emojis.BP} If you manage to win a tier III tournament, you get an exclusive background\n'
    )
    disabled = (
        f'{emojis.BP} Miniraces are not available anymore due to bugs.\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MINIRACE',
        description = 'Good luck with that background, lol.'
    )
    #embed.add_field(name='OVERVIEW', value=overview, inline=False)
    #embed.add_field(name='HOW TO PLAY', value=howtoplay, inline=False)
    #embed.add_field(name='POSSIBLE ACTIONS', value=actions, inline=False)
    #embed.add_field(name='DEBUFFS', value=debuffs, inline=False)
    #embed.add_field(name='WINNING A ROUND', value=round_win, inline=False)
    #embed.add_field(name='WINNING THE TOURNAMENT', value=race_win, inline=False)
    embed.add_field(name='NOTE', value=disabled, inline=False)
    return embed