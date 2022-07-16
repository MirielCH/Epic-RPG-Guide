# pets.py
# Contains the content for pet commands

from typing import Optional

import discord

import database
from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_ADVENTURES = 'Pet adventures'
TOPIC_CATCH = 'Catching pets'
TOPIC_FUSION = 'Fusing pets'
TOPIC_OVERVIEW = 'Overview'
TOPIC_SKILLS = 'Skills: Normal skills'
TOPIC_SKILLS_SPECIAL = 'Skills: Special skills'
TOPIC_SKILLS_UNIQUE = 'Skills: Unique skills'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_CATCH,
    TOPIC_FUSION,
    TOPIC_ADVENTURES,
    TOPIC_SKILLS,
    TOPIC_SKILLS_SPECIAL,
    TOPIC_SKILLS_UNIQUE,
]


# --- Commands ---
async def command_pets_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Pet guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_pets_overview,
        TOPIC_CATCH: embed_pets_catch,
        TOPIC_FUSION: embed_pets_fusion,
        TOPIC_ADVENTURES: embed_pets_adventures,
        TOPIC_SKILLS: embed_pets_skills_normal,
        TOPIC_SKILLS_SPECIAL: embed_pets_skills_special,
        TOPIC_SKILLS_UNIQUE: embed_pets_skills_unique,
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


async def command_pets_fuse(ctx: discord.ApplicationContext, pet_tier: int, timetravel: Optional[int] = None) -> None:
    """Pet fuse command"""
    if timetravel is None:
        user: database.User = await database.get_user(ctx.author.id)
        timetravel = user.tt
    embed = await embed_fuse(pet_tier, timetravel)
    await ctx.respond(embed=embed)


# --- Embeds ---
async def embed_pets_overview() -> discord.Embed:
    """Pet overview"""
    requirements = (
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 2+\n'
        f'{emojis.BP} Exception: Event and giveaway pets are not TT locked'
    )
    whattodo = f'{emojis.BP} Send them on adventures (see topic `Pet adventures`)'
    tier = (
        f'{emojis.BP} Tiers range from I to XX (1 to 20)\n'
        f'{emojis.BP} Increases the number of items you get in adventures\n'
        f'{emojis.BLANK} Tier I and higher has a chance of returning up to 1 ULTRA log\n'
        f'{emojis.BLANK} Tier X and higher has a chance of returning up to 2 ULTRA logs\n'
        f'{emojis.BLANK} Tier XX has a chance of returning up to 3 ULTRA logs\n'
        f'{emojis.BP} Increases the chance to increase a skill rank in adventures\n'
        f'{emojis.BP} Increases the chance to keep a skill when fusing\n'
        f'{emojis.BP} Increased by fusing pets (see topic `Fusing pets`)'
    )
    normalskills = (
        f'{emojis.BP} There are 7 normal skills\n'
        f'{emojis.BP} Normal skills rank from F to SS+\n'
        f'{emojis.BP} Mainly found by fusing pets (see topic `Fusing pets`)\n'
        f'{emojis.BP} Small chance of getting a skill when catching pets\n'
        f'{emojis.BP} See topic `Normal skills` for details\n'
    )
    specialskills = (
        f'{emojis.BP} There are 3 special skills\n'
        f'{emojis.BP} Special skills rank from F to SS+\n'
        f'{emojis.BP} Special skills can **not** be lost\n'
        f'{emojis.BP} See topic `Special skills` for details\n'
    )
    uniqueskills = (
        f'{emojis.BP} There are 8 unique skills\n'
        f'{emojis.BP} Special skills don\'t have a rank and can **not** be lost\n'
        f'{emojis.BP} Each unique skill is tied to a certain pet\n'
        f'{emojis.BP} See topic `Unique skills` for details\n'
    )
    type = (
        f'{emojis.BP} The basic types are {emojis.PET_CAT} cat, {emojis.PET_DOG} dog and {emojis.PET_DRAGON} dragon\n'
        f'{emojis.BP} Event pets can have unique types\n'
        f'{emojis.BP} The type you get when catching pets is random\n'
        f'{emojis.BP} All types are purely cosmetic'
    )
    score = (
        f'{emojis.BP} The pet score increases your chance to win pet tournaments\n'
        f'{emojis.BP} See {strings.SLASH_COMMANDS_GUIDE["event guide"]} for details about tournaments\n'
        f'{emojis.BP} The pet score is influenced by tier, skills and skill ranks\n'
        f'{emojis.BP} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Pets#Pet_Score)'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'PETS',
        description = (
            f'Pets have tiers, types and skills and can be sent on adventures to find stuff for you.\n'
            f'You can have up to (5 + TT) pets (= 7 pets at {emojis.TIME_TRAVEL} TT 2).'
        )
    )
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='WHAT TO DO WITH PETS', value=whattodo, inline=False)
    embed.add_field(name='TIER', value=tier, inline=False)
    embed.add_field(name='NORMAL SKILLS', value=normalskills, inline=False)
    embed.add_field(name='SPECIAL SKILLS', value=specialskills, inline=False)
    embed.add_field(name='UNIQUE SKILLS', value=uniqueskills, inline=False)
    embed.add_field(name='TYPE', value=type, inline=False)
    embed.add_field(name='SCORE', value=score, inline=False)
    return embed


async def embed_pets_catch() -> discord.Embed:
    """Pet catching guide"""
    source = (
        f'{emojis.BP} After using {strings.SLASH_COMMANDS_EPIC_RPG["training"]}\n'
        f'{emojis.BLANK} 4% base encounter chance\n'
        f'{emojis.BLANK} 10% chance with {emojis.HORSE_T9} T9 horse\n'
        f'{emojis.BLANK} 20% chance with {emojis.HORSE_T10} T10 horse\n'
        f'{emojis.BP} By ranking at least 3rd in {emojis.HORSE_T9} T9 or {emojis.HORSE_T10} T10 horse races\n'
        f'{emojis.BP} In some seasonal events (these are not TT locked)\n'
        f'{emojis.BP} In some dev giveaways (these are not TT locked)\n'
        f'{emojis.BP} As a reward from professions (these are not TT locked)\n'
        f'{emojis.BP} From {emojis.LB_VOID} VOID lootboxes\n'
        f'{emojis.BP} By sending {emojis.SKILL_ASCENDED} ascended pets on adventures (see topic `Pet adventures`)'
    )
    catch =  (
        f'{emojis.BP} Pets you encounter have a {emojis.PET_HAPPINESS} happiness and {emojis.PET_HUNGER} hunger stat\n'
        f'{emojis.BP} You can use actions to influence these stats\n'
        f'{emojis.BLANK} 1 `feed` decreases hunger by 18-22\n'
        f'{emojis.BLANK} 1 `pat` increases happiness by 8-12\n'
        f'{emojis.BP} If happiness is 85+ higher than hunger, catch chance is 100%\n'
        f'{emojis.BP} You can use up to 6 actions\n'
        f'{emojis.BP} If you use less than 6 actions, you have a 25% chance at getting skills\n'
        f'{emojis.BP} The less commands you use, the higher the chance to get rarer skills\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CATCHING PETS',
        description = (
            f'With the exception of event, giveaway and profession reward pets you can only find and catch '
            f'pets in {emojis.TIME_TRAVEL} TT 2+'
        )
    )
    embed.add_field(name='HOW TO FIND PETS', value=source, inline=False)
    embed.add_field(name='HOW TO CATCH PETS', value=catch, inline=False)
    return embed


async def embed_pets_fusion() -> discord.Embed:
    """Pet fusion guide"""
    general = (
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["pets fusion"]}\n'
        f'{emojis.BP} You can fuse more than 2 pets but you should only do that if you want to maximize the chance to '
        f'keep certain skills or want to control the type you get\n'
        f'{emojis.BP} You can **not** lose tiers when fusing\n'
        f'{emojis.BP} You can **not** lose special skills when fusing\n'
        f'{emojis.BP} You **can** lose normal skills when fusing\n'
        f'{emojis.BP} Exception: You can not lose {emojis.SKILL_ASCENDED} ascended and {emojis.SKILL_FIGHTER} fighter'
    )
    tiers = (
        f'{emojis.BP} Check {strings.SLASH_COMMANDS_GUIDE["pets fuse"]} on what to fuse to get a tier up\n'
        f'{emojis.BP} For the highest chance of a tier up, fuse 2 pets of the **same** tier\n'
        f'{emojis.BP} The chance to tier up gets lower the higher your tier is'
    )
    skills = (
        f'{emojis.BP} You have a random chance of getting a new normal skill when fusing\n'
        f'{emojis.BP} You can **not** get special skills when fusing\n'
        f'{emojis.BP} The more skills you already have, the lower the chance to get one\n'
        f'{emojis.BP} If your sole goal is getting skills, fuse with T1 throwaway pets\n'
        f'{emojis.BP} You can keep normal skills you already have, but the chance depends on the skill rank and how '
        f'many of that skill you have in the fusion (see topic `Normal skills`)\n'
        f'{emojis.BP} To maximize the chance to keep normal skills, rank them to SS+ first and fuse pets that have the '
        f'same skill\n'
        f'{emojis.BP} The exact chances to keep skills are unknown'
    )
    type = (
        f'{emojis.BP} The resulting type depends on the most used type in the fusion\n'
        f'{emojis.BP} If you fuse different types evenly, the result is randomly one of those types\n'
        f'{emojis.BLANK} Example 1: {emojis.PET_CAT} + {emojis.PET_CAT} results in {emojis.PET_CAT}\n'
        f'{emojis.BLANK} Example 2: {emojis.PET_DOG} + {emojis.PET_CAT} + {emojis.PET_DOG} results in {emojis.PET_DOG}\n'
        f'{emojis.BLANK} Example 3: {emojis.PET_CAT} + {emojis.PET_DOG} results in {emojis.PET_CAT} **or** {emojis.PET_DOG}\n'
        f'{emojis.BP} Exception: Fusing an event pet will always give you the event pet back\n'
        f'{emojis.BP} Note: You can only fuse multiple event pets if they all are the **same** type'
    )
    whatfirst = (
        f'{emojis.BP} Try to tier up to T4+ before you start fusing for skills\n'
        f'{emojis.BP} The best normal skill to keep first is {emojis.SKILL_HAPPY} happy'
    )
    skillsimpact = f'{emojis.BP} {emojis.SKILL_HAPPY} **Happy**: Increases the chance to tier up'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'FUSING PETS',
        description = 'You can fuse pets to tier them up and/or find or transfer normal skills.'
    )
    embed.add_field(name='HOW TO FUSE', value=general, inline=False)
    embed.add_field(name='TIERING UP', value=tiers, inline=False)
    embed.add_field(name='HOW TO GET (AND KEEP) SKILLS', value=skills, inline=False)
    embed.add_field(name='IMPACT ON TYPE', value=type, inline=False)
    embed.add_field(name='WHAT TO DO FIRST', value=whatfirst, inline=False)
    embed.add_field(name='SKILLS THAT AFFECT FUSION', value=skillsimpact, inline=False)
    return embed


async def embed_pets_skills_normal() -> discord.Embed:
    """Normal skills guide"""
    normie = f'{emojis.BP} This is not a skill, it simply means the pet has no skills'
    fast = (
        f'{emojis.BP} Reduces the time to do adventures\n'
        f'{emojis.BP} Reduces the time down to 2h 33m 36s at rank SS+'
    )
    happy = f'{emojis.BP} Increases the chance to tier up when fusing'
    clever = f'{emojis.BP} Increases the chance to rank up skills in adventures'
    digger = f'{emojis.BP} Increases the amount of coins you get in adventures'
    lucky = f'{emojis.BP} Increases the chance to find better items in adventures'
    timetraveler = (
        f'{emojis.BP} Has a chance of finishing an adventure instantly\n'
        f'{emojis.BP} Note: You can not cancel an adventure if the pet has this skill\n'
    )
    epic = (
        f'{emojis.BP} If you send this pet on an adventure, you can send another\n'
        f'{emojis.BP} Note: You have to send the pet with this skill **first**'
    )
    skillranks = (
        f'{emojis.BP} Every skill has 9 possible ranks\n'
        f'{emojis.BLANK} The ranks are F, E, D, C, B, A, S, SS and SS+\n'
        f'{emojis.BP} To rank up skills, do adventures (see topic `Pet adventures`)\n'
        f'{emojis.BP} Higher ranks increase the skill bonus\n'
        f'{emojis.BP} Higher ranks increase the chance to keep a skill when fusing'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'NORMAL PET SKILLS',
        description = (
            f'Overview of all **normal** pet skills. See topic `Overview` on how to get these skills.\n'
            f'Purple and yellow skills are rarer than blue ones.'
        )
    )
    embed.add_field(name=f'NORMIE {emojis.SKILL_NORMIE}', value=normie, inline=False)
    embed.add_field(name=f'FAST {emojis.SKILL_FAST}', value=fast, inline=False)
    embed.add_field(name=f'HAPPY {emojis.SKILL_HAPPY}', value=happy, inline=False)
    embed.add_field(name=f'CLEVER {emojis.SKILL_CLEVER}', value=clever, inline=False)
    embed.add_field(name=f'DIGGER {emojis.SKILL_DIGGER}', value=digger, inline=False)
    embed.add_field(name=f'LUCKY {emojis.SKILL_LUCKY}', value=lucky, inline=False)
    embed.add_field(name=f'TIME TRAVELER {emojis.SKILL_TRAVELER}', value=timetraveler, inline=False)
    embed.add_field(name=f'EPIC {emojis.SKILL_EPIC}', value=epic, inline=False)
    embed.add_field(name='SKILL RANKS', value=skillranks, inline=False)
    return embed


async def embed_pets_skills_special() -> discord.Embed:
    """Special skills guide"""
    ascended = (
        f'{emojis.BP} Has a chance to find another pet in adventures\n'
        f'{emojis.BLANK} The chance is 11.11...% per rank (100% at SS+)\n'
        f'{emojis.BP} This skill has to be unlocked with {strings.SLASH_COMMANDS_EPIC_RPG["pets ascend"]}\n'
        f'{emojis.BP} You can only ascend pets that have **all** other skills at SS+\n'
        f'{emojis.BP} Pets can only ascend in {emojis.TIME_TRAVEL} TT 26+\n'
        f'{emojis.BP} **You will lose all other skills when ascending**\n'
        f'{emojis.BP} You can **not** lose this skill when fusing\n'
        f'{emojis.BP} You can **not** rank up this skill with adventures\n'
        f'{emojis.BP} To rank up the skill, either ascend again or fuse with other ascended pets\n'
        f'{emojis.BP} Fusing ascended pets combines the ascended skills into one (e.g. F+E=D)\n'
    )
    fighter = (
        f'{emojis.BP} Pet can be used to acquire {emojis.DRAGON_ESSENCE} dragon essence in D1-D9\n'
        f'{emojis.BP} You have a 25% base chance to get an essence after the dungeon\n'
        f'{emojis.BLANK} This chance increases by 7.5% per rank\n'
        f'{emojis.BLANK} Multiple fighter pets do not stack\n'
        f'{emojis.BP} You can **not** find this skill, it is unlocked once a pet reaches Tier X\n'
        f'{emojis.BP} You can **not** lose this skill when fusing\n'
        f'{emojis.BP} To rank up the skill, you have to tier up further (1 rank per tier)\n'
    )
    master = (
        f'{emojis.BP} Increases the tier of pets found with the {emojis.SKILL_ASCENDED} ascended skill\n'
        f'{emojis.BP} You can **not** find this skill, it is unlocked once a pet reaches Tier XV\n'
        f'{emojis.BP} You can **not** lose this skill when fusing\n'
        f'{emojis.BP} To rank up the skill, you have to tier up further (1 rank per tier)\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'SPECIAL PET SKILLS',
        description = 'Overview of all **special** pet skills.'
    )
    embed.add_field(name=f'ASCENDED {emojis.SKILL_ASCENDED}', value=ascended, inline=False)
    embed.add_field(name=f'FIGHTER {emojis.SKILL_FIGHTER}', value=fighter, inline=False)
    embed.add_field(name=f'MASTER {emojis.SKILL_MASTER}', value=master, inline=False)
    return embed


async def embed_pets_skills_unique() -> discord.Embed:
    """Unique skills guide"""
    competitive = (
        f'{emojis.BP} The pet has 1 more score point\n'
        f'{emojis.BP} This skill is unique to the {emojis.PET_PANDA} epic panda pet\n'
        f'{emojis.BP} This pet was given to the first player who reached {emojis.TIME_TRAVEL} TT 100'
    )
    fisherfish = (
        f'{emojis.BP} If the pet finds fish, you get 3 times the amount\n'
        f'{emojis.BP} This skill is unique to the {emojis.PET_PINK_FISH} pink fish pet\n'
        f'{emojis.BP} This pet is a reward in the valentine event'
    )
    faster = (
        f'{emojis.BP} If the pet also has the {emojis.SKILL_FAST} fast skill, the time reduction is doubled\n'
        f'{emojis.BP} This skill is unique to the {emojis.PET_GOLDEN_BUNNY} golden bunny pet\n'
        f'{emojis.BP} This pet is a reward in the easter event'
    )
    monsterhunter = (
        f'{emojis.BP} Has a 35% chance to find 3-5 random mob drops in pet adventures\n'
        f'{emojis.BP} This skill is unique to the {emojis.PET_PUMPKIN_BAT} pumpkin bat pet\n'
        f'{emojis.BP} This pet is a reward in the halloween event'
    )
    gifter = (
        f'{emojis.BP} Has a 35% chance to find a random lootbox in a pet adventure\n'
        f'{emojis.BP} This skill is unique to the {emojis.PET_SNOWBALL} snowball pet\n'
        f'{emojis.BP} This pet is a reward in the christmas event'
    )
    booster = (
        f'{emojis.BP} **All** pets have a 75% chance of advancing skills twice in a pet adventure\n'
        f'{emojis.BP} This chance only applies if the pet decided to learn\n'
        f'{emojis.BP} The chance increases if you have multiple pets with this skill\n'
        f'{emojis.BP} This skill is unique to the {emojis.PET_HAMSTER} hamster pet\n'
        f'{emojis.BP} This pet is a reward in the anniversary event\n'
    )
    farmer = (
        f'{emojis.BP} Has a 40% chance to find normal or special seeds in pet adventures\n'
        f'{emojis.BP} This skill is unique to the {emojis.PET_PONY} pony pet\n'
        f'{emojis.BP} This pet is a reward in the horse festival'
    )
    resetter = (
        f'{emojis.BP} If the pet also has the {emojis.SKILL_TRAVELER} time traveler skill and it triggers, '
        f'it has a chance to reset **all** pets on an adventure\n'
        f'{emojis.BP} This skill is unique to the {emojis.PET_VOIDOG} VOIDog pet\n'
        f'{emojis.BP} This pet can drop in dungeons 16 to 20.\n'
        f'{emojis.BLANK} The drop chance increases with higher dungeons.\n'
        f'{emojis.BLANK} You can get multiple, but each time you get one, the drop chance lowers.\n'
    )
    skillranks = f'{emojis.BP} Unique skills can not be ranked up'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'UNIQUE PET SKILLS',
        description = (
            f'Overview of all **unique** pet skills. These skill are unique to certain pets and can **not** be lost.\n'
        )
    )
    embed.add_field(name=f'BOOSTER {emojis.SKILL_BOOSTER}', value=booster, inline=False)
    embed.add_field(name=f'COMPETITIVE {emojis.SKILL_COMPETITIVE}', value=competitive, inline=False)
    embed.add_field(name=f'FARMER {emojis.SKILL_FARMER}', value=farmer, inline=False)
    embed.add_field(name=f'FASTER {emojis.SKILL_FASTER}', value=faster, inline=False)
    embed.add_field(name=f'FISHERFISH {emojis.SKILL_FISHER_FISH}', value=fisherfish, inline=False)
    embed.add_field(name=f'GIFTER {emojis.SKILL_GIFTER}', value=gifter, inline=False)
    embed.add_field(name=f'MONSTER HUNTER {emojis.SKILL_MONSTER_HUNTER}', value=monsterhunter, inline=False)
    embed.add_field(name=f'RESETTER {emojis.SKILL_RESETTER}', value=resetter, inline=False)
    embed.add_field(name='SKILL RANKS', value=skillranks, inline=False)
    return embed


async def embed_pets_adventures() -> discord.Embed:
    """Pet adventure guide"""
    usage = (
        f'{emojis.BP} Command: {strings.SLASH_COMMANDS_EPIC_RPG["pets adventure"]}\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["pets adventure"]} `action: cancel` to cancel an adventure\n'
        f'{emojis.BP} You can only send **1** pet unless you have the {emojis.SKILL_EPIC} EPIC skill\n'
        f'{emojis.BP} Note: To send all EPIC pets at once, use pet ID `epic`\n'
        f'{emojis.BP} Note: You can not cancel an adventure if the pet has the {emojis.SKILL_TRAVELER} '
        f'time traveler skill \n'
    )
    types = (
        f'{emojis.BP} **Find**: Pet is more likely to find items\n'
        f'{emojis.BP} **Drill**: Pet is more likely to find coins\n'
        f'{emojis.BP} **Learn**: Pet is more likely to rank up a skill\n'
        f'{emojis.BP} The type does **not** guarantee the outcome \n'
        f'{emojis.BP} Your pet will never come back emptyhanded'
    )
    rewards = (
        f'{emojis.BP} **Items**: {emojis.LOG}{emojis.LOG_EPIC}{emojis.LOG_SUPER}{emojis.LOG_MEGA}{emojis.LOG_HYPER}'
        f'{emojis.LOG_ULTRA} {emojis.FISH}{emojis.FISH_GOLDEN}{emojis.FISH_EPIC}{emojis.LIFE_POTION}\n'
        f'{emojis.BP} **Coins**: ~ 700k+\n'
        f'{emojis.BP} **Skill rank**: +1 rank of 1 skill the pet has\n'
        f'{emojis.BP} **Pet**: Random T1-3 pet (only if pet has {emojis.SKILL_ASCENDED} ascended skill)\n'
        f'{emojis.BLANK} You get a pet **in addition** to the other reward'
    )
    normalskillsimpact = (
        f'{emojis.BP} {emojis.SKILL_FAST} **Fast**: Reduces the time to do adventures\n'
        f'{emojis.BP} {emojis.SKILL_DIGGER} **Digger**: Increases the amount of coins you get\n'
        f'{emojis.BP} {emojis.SKILL_LUCKY} **Lucky**: Increases the chance to find better items\n'
        f'{emojis.BP} {emojis.SKILL_TRAVELER} **Time traveler**: Has a chance of finishing instantly\n'
        f'{emojis.BP} {emojis.SKILL_EPIC} **EPIC**: If you send this pet **first**, you can send another\n'
    )
    specialskillsimpact = (
        f'{emojis.BP} {emojis.SKILL_ASCENDED} **Ascended**: Has a chance to find a pet'
    )
    uniqueskillsimpact = (
        f'{emojis.BP} {emojis.SKILL_FISHER_FISH} **Fisherfish**: Increases the amount of fish you get by 300%\n'
        f'{emojis.BP} {emojis.SKILL_FASTER} **Faster**: Doubles time reduction from {emojis.SKILL_FAST} fast skill\n'
        f'{emojis.BP} {emojis.SKILL_MONSTER_HUNTER} **Monster hunter**: Has a chance to find mob drops\n'
        f'{emojis.BP} {emojis.SKILL_GIFTER} **Gifter**: Has a chance to find a lootbox\n'
        f'{emojis.BP} {emojis.SKILL_BOOSTER} **BOOSTER**: All pets have a chance to advance skills twice\n'
        f'{emojis.BP} {emojis.SKILL_BOOSTER} **Resetter**: Adds a chance to {emojis.SKILL_TRAVELER} time traveler skill '
        f'to reset all pets\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'PET ADVENTURES',
        description = 'You can send pets on adventures to find items or coins or to rank up their skills.'
    )
    embed.add_field(name='HOW TO SEND PETS', value=usage, inline=False)
    embed.add_field(name='ADVENTURE TYPES', value=types, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NORMAL SKILLS THAT AFFECT ADVENTURES', value=normalskillsimpact, inline=False)
    embed.add_field(name='SPECIAL SKILLS THAT AFFECT ADVENTURES', value=specialskillsimpact, inline=False)
    embed.add_field(name='UNIQUE SKILLS THAT AFFECT ADVENTURES', value=uniqueskillsimpact, inline=False)
    return embed


async def embed_fuse(pet_tier: int, timetravel: int) -> discord.Embed:
    """Pet fusion recommendations"""
    pet_data: database.PetTier = await database.get_pet_tier(pet_tier, timetravel)
    if pet_data.fusion_to_get_tier.fusion != 'None':
        how_to_get_tier = f'{emojis.BP} {pet_data.fusion_to_get_tier.fusion}'
    else:
        how_to_get_tier = f'{emojis.BP} Chance too low' if pet_tier > 1 else f'{emojis.BP} None'
    what_to_fuse_with_tier = ''
    for fusion in pet_data.fusions_including_tier:
        what_to_fuse_with_tier = (
            f'{what_to_fuse_with_tier}\n'
            f'{emojis.BP} {fusion.fusion} ➜ T{fusion.tier}'
        )
    if what_to_fuse_with_tier == '':
        what_to_fuse_with_tier = f'{emojis.BP} Chance too low' if pet_tier < 15 else f'{emojis.BP} None'
    note = (
        f'{emojis.BP} Tier up is **not** guaranteed!\n'
        f'{emojis.BP} Lower fusions _might_ be possible but are rarely successful.\n'
        f'{emojis.BP} If you want the maximum chance, do same-tier fusions.\n'
        f'{emojis.BP} You can lose skills in fusions!\n'
        f'{emojis.BP} If you are unsure about fusions, see {strings.SLASH_COMMANDS_GUIDE["pets guide"]}'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'TIER {pet_tier} PET FUSIONS • TT {timetravel}',
        description = 'This guide lists the minimum recommended fusions for a decent tier up chance.'
    )
    embed.add_field(name=f'FUSION TO GET A T{pet_tier} PET', value=how_to_get_tier, inline=False)
    embed.add_field(name=f'FUSIONS THAT INCLUDE A T{pet_tier} PET', value=what_to_fuse_with_tier, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed