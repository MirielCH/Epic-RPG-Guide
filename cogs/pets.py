# pets.py

import discord
from discord.ext import commands

import database
import emojis
import global_data


# pets commands (cog)
class petsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pets_aliases = (
        'pet',
        'petcatch','petscatch','petscatching','petcatching','catchpet','catchpets','catchingpet','catchingpets',
        'petfind','petsfind','petfinding','petsfinding','findpet','findingpet','findpets','findingpets',
        'petsfusion','fusion','petfusing','petsfusing','fusing','fusepet','fusepets','fusingpet','fusingpets',
        'petsskills','petskill','skill','skills','petsskill',
        'petsspecial','petsspecialskill','petsspecialskills','petspecial','petspecialskill','petspecialskills','petskillspecial','petskillsspecial','petsskillspecial','petsskillsspecial',
        'petsadv','petsadventures','petadv','petadventure','petadventures'
    )

    # Command "pets"
    @commands.command(aliases=pets_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def pets(self, ctx, *args):
        invoked = ctx.invoked_with
        invoked = invoked.lower()

        if args:
            arg = args[0]
            if (arg.find('catch') > -1) or (arg.find('find') > -1):
                embed = await embed_pets_catch(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('fusi') > -1:
                embed = await embed_pets_fusion(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('skill') > -1:
                if len(args) == 2:
                    arg2 = args[1]
                    if arg2.find('special') > -1:
                        embed = await embed_pets_skills_special(ctx.prefix)
                        await ctx.send(embed=embed)
                    else:
                        embed = await embed_pets_skills(ctx.prefix)
                        await ctx.send(embed=embed)
                else:
                    embed = await embed_pets_skills(ctx.prefix)
                    await ctx.send(embed=embed)
            elif arg.find('adv') > -1:
                embed = await embed_pets_adventures(ctx.prefix)
                await ctx.send(embed=embed)
            else:
                embed = await embed_pets_overview(ctx.prefix)
                await ctx.send(embed=embed)
        else:
            if (invoked.find('catch') > -1) or (invoked.find('find') > -1):
                embed = await embed_pets_catch(ctx.prefix)
                await ctx.send(embed=embed)
            elif invoked.find('fusi') > -1:
                embed = await embed_pets_fusion(ctx.prefix)
                await ctx.send(embed=embed)
            elif invoked.find('skill') > -1:
                if invoked.find('special') > -1:
                    embed = await embed_pets_skills_special(ctx.prefix)
                    await ctx.send(embed=embed)
                else:
                    embed = await embed_pets_skills(ctx.prefix)
                    await ctx.send(embed=embed)
            elif invoked.find('skill') > -1:
                embed = await embed_pets_skills(ctx.prefix)
                await ctx.send(embed=embed)
            elif invoked.find('adv') > -1:
                embed = await embed_pets_adventures(ctx.prefix)
                await ctx.send(embed=embed)
            else:
                embed = await embed_pets_overview(ctx.prefix)
                await ctx.send(embed=embed)

    # Command "Fuse" - Recommendations for pet tiers in fusions
    @commands.command(aliases=('petfuse',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def fuse(self, ctx, *args):

        prefix = ctx.prefix

        syntax = (
            f'The syntax is:\n'
            f'{emojis.BP} `{prefix}fuse [tier]` to get recommendations for your current TT.\n'
            f'{emojis.BP} `{prefix}fuse [tier] [tt]` to get recommendations for another TT.\n\n'
            f'Examples: `{prefix}fuse t5` / `{prefix}fuse 6 25`'
        )

        if args:
            if len(args) in (1,2):
                pet_tier = args[0]
                if pet_tier.lower().find('tt') > -1:
                    await ctx.send(syntax)
                    return
                pet_tier = pet_tier.lower().replace('t','')
                if pet_tier.isnumeric():
                    pet_tier = int(pet_tier)
                    if not 1 <= pet_tier <= 15:
                        await ctx.send('Please enter a pet tier between 1 and 15.')
                        return
                else:
                    await ctx.send(syntax)
                    return
                if len(args) == 2:
                    user_tt = args[1]
                    user_tt = user_tt.lower().replace('tt','')
                    if user_tt.isnumeric():
                        user_tt = int(user_tt)
                        if not 0 <= user_tt <= 999:
                            await ctx.send(f'Please enter a TT between 0 and 999.')
                            return
                    else:
                        await ctx.send(syntax)
                        return
                elif len(args) > 2:
                    await ctx.send(syntax)
                    return
                else:
                    user = await database.get_user(ctx.author.id)
                    user_tt = user.tt
                embed = await embed_fuse(ctx, pet_tier, user_tt)
                await ctx.send(embed=embed)
            else:
                await ctx.send(syntax)
                return
        else:
            await ctx.send(
                f'This command takes a pet of a certain tier and tells you:\n'
                f'{emojis.BP} What you can fuse if you **want** that tier\n'
                f'{emojis.BP} What you can fuse if you **have** that tier\n\n'
                f'{syntax}'
            )


# Initialization
def setup(bot):
    bot.add_cog(petsCog(bot))



# --- Redundancies ---
# Guides
guide_overview = '`{prefix}pet` : Pets overview'
guide_catch = '`{prefix}pet catch` : How to find and catch pets'
guide_fusion = '`{prefix}pet fusion` : Details about pet fusion'
guide_fuse = '`{prefix}fuse` : Pet fusion recommendations'
guide_skills = '`{prefix}pet skills` : Details about pet skills'
guide_skills_special = '`{prefix}pet skills special` : Details about special pet skills'
guide_adv = '`{prefix}pet adv` : Details about pet adventures'



# --- Embeds ---
# Pets overview
async def embed_pets_overview(prefix):

    requirements = (
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 2+\n'
        f'{emojis.BP} Exception: Event and giveaway pets are not TT locked'
    )

    whattodo = f'{emojis.BP} Send them on adventures (see `{prefix}pet adv`)'


    tier = (
        f'{emojis.BP} Tiers range from I to XX (1 to 20)\n'
        f'{emojis.BP} Increases the number of items you get in adventures\n'
        f'{emojis.BLANK} Tier I and higher has a chance of returning up to 1 ULTRA log\n'
        f'{emojis.BLANK} Tier X and higher has a chance of returning up to 2 ULTRA logs\n'
        f'{emojis.BLANK} Tier XX has a chance of returning up to 3 ULTRA logs\n'
        f'{emojis.BP} Increases the chance to increase a skill rank in adventures\n'
        f'{emojis.BP} Increases the chance to keep a skill when fusing\n'
        f'{emojis.BP} Increased by fusing pets (see `{prefix}pet fusion`)'
    )

    normalskills = (
        f'{emojis.BP} There are 8 normal skills (see `{prefix}pet skills`)\n'
        f'{emojis.BP} Skills have a rank that ranges from F to SS+\n'
        f'{emojis.BP} Mainly found by fusing pets (see `{prefix}pet fusion`)\n'
        f'{emojis.BP} Small chance of getting a skill when catching pets'
    )

    specialskills = (
        f'{emojis.BP} There are 7 special skills (see `{prefix}pet skills special`)\n'
        f'{emojis.BP} Special skills don\'t have a rank and can **not** be lost\n'
        f'{emojis.BP} Only available on special event reward pets\n'
        f'{emojis.BP} Each special skill is unique to a certain special pet'
    )

    type = (
        f'{emojis.BP} The basic types are {emojis.PET_CAT} cat, {emojis.PET_DOG} dog and {emojis.PET_DRAGON} dragon\n'
        f'{emojis.BP} Event pets can have unique types\n'
        f'{emojis.BP} The type you get when catching pets is random\n'
        f'{emojis.BP} All types are purely cosmetic'
    )

    score = (
        f'{emojis.BP} The pet score increases your chance to win pet tournaments\n'
        f'{emojis.BP} See `{prefix}event pet tournament` for details about tournaments\n'
        f'{emojis.BP} The pet score is influenced by tier, skills and skill ranks\n'
        f'{emojis.BP} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Pets#Pet_Score)'
    )

    guides = (
        f'{emojis.BP} {guide_catch.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_fusion.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_skills.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_skills_special.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_adv.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_fuse.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'PETS',
        description = (
            f'Pets have tiers, types and skills and can be sent on adventures to find stuff for you.\n'
            f'You can have up to (5 + TT) pets (= 7 pets at {emojis.TIME_TRAVEL} TT 2).'
        )
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='WHAT TO DO WITH PETS', value=whattodo, inline=False)
    embed.add_field(name='TIER', value=tier, inline=False)
    embed.add_field(name='NORMAL SKILLS', value=normalskills, inline=False)
    embed.add_field(name='SPECIAL SKILLS', value=specialskills, inline=False)
    embed.add_field(name='TYPE', value=type, inline=False)
    embed.add_field(name='SCORE', value=score, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Catching pets
async def embed_pets_catch(prefix):

    source = (
        f'{emojis.BP} After using `training` (4% base chance, 10% with {emojis.HORSE_T9} T9 horse, 20% with {emojis.HORSE_T10} T10 horse)\n'
        f'{emojis.BP} By ranking at least 3rd in {emojis.HORSE_T9} T9 or {emojis.HORSE_T10} T10 horse races\n'
        f'{emojis.BP} In some seasonal events (these are not TT locked)\n'
        f'{emojis.BP} In some dev giveaways (these are not TT locked)\n'
        f'{emojis.BP} By sending {emojis.SKILL_ASCENDED} ascended pets on adventures (see `{prefix}pet adv`)'
    )

    catch =  (
        f'{emojis.BP} Pets you encounter have a {emojis.PET_HAPPINESS} happiness and {emojis.PET_HUNGER} hunger stat\n'
        f'{emojis.BP} You can enter a line of commands to influence these stats\n'
        f'{emojis.BP} `feed` decreases hunger by 18-22\n'
        f'{emojis.BP} `pat` increases happiness by 8-12\n'
        f'{emojis.BP} If happiness is 85+ higher than hunger, catch chance is 100%\n'
        f'{emojis.BP} Example: `feed feed pat pat pat`\n'
        f'{emojis.BP} You can use up to 6 commands\n'
        f'{emojis.BP} If you use less than 6 commands, you have a 25% chance at getting skills on the pet\n'
        f'{emojis.BP} The less commands you use, the higher the chance to get rarer skills\n'
    )

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_fusion.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_skills.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_skills_special.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_adv.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'CATCHING PETS',
        description = f'With the exception of event and giveaway pets you can only find and catch pets in {emojis.TIME_TRAVEL} TT 2+'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='HOW TO FIND PETS', value=source, inline=False)
    embed.add_field(name='HOW TO CATCH PETS', value=catch, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Pet fusion
async def embed_pets_fusion(prefix):

    general = (
        f'{emojis.BP} Use `pets fusion [petID1] [petID2]`\n'
        f'{emojis.BP} You can fuse more than 2 pets but you should only do that if you want to maximize the chance to keep certain skills or want to control the type you get\n'
        f'{emojis.BP} You can **not** lose tiers when fusing\n'
        f'{emojis.BP} You can **not** lose special skills when fusing\n'
        f'{emojis.BP} You **can** lose normal skills when fusing\n'
        f'{emojis.BP} Exception: You can not lose {emojis.SKILL_ASCENDED} ascended and {emojis.SKILL_FIGHTER} fighter'
    )

    tiers = (
        f'{emojis.BP} Check `{prefix}fuse` on what to fuse to get a tier up\n'
        f'{emojis.BP} For the highest chance of a tier up, fuse 2 pets of the **same** tier\n'
        f'{emojis.BP} The chance to tier up gets lower the higher your tier is'
    )

    skills = (
        f'{emojis.BP} You have a random chance of getting a new normal skill when fusing\n'
        f'{emojis.BP} You can **not** get special skills when fusing\n'
        f'{emojis.BP} The more skills you already have, the lower the chance to get one\n'
        f'{emojis.BP} If your sole goal is getting skills, fuse with T1 throwaway pets\n'
        f'{emojis.BP} You can keep normal skills you already have, but the chance depends on the skill rank and how many of that skill you have in the fusion (see `{prefix}pet skills`)\n'
        f'{emojis.BP} To maximize the chance to keep normal skills, rank them to SS+ first and fuse pets that have the same skill\n'
        f'{emojis.BP} The exact chances to keep skills are unknown'
    )

    type = (
        f'{emojis.BP} The resulting type depends on the most used type in the fusion\n'
        f'{emojis.BP} If you fuse different types evenly, the result is randomly one of those types\n'
        f'{emojis.BP} Example 1: {emojis.PET_CAT} + {emojis.PET_CAT} results in {emojis.PET_CAT}\n'
        f'{emojis.BP} Example 2: {emojis.PET_DOG} + {emojis.PET_CAT} + {emojis.PET_DOG} results in {emojis.PET_DOG}\n'
        f'{emojis.BP} Example 3: {emojis.PET_CAT} + {emojis.PET_DOG} results in {emojis.PET_CAT} **or** {emojis.PET_DOG}\n'
        f'{emojis.BP} Exception: Fusing an event pet will always give you the event pet back\n'
        f'{emojis.BP} Note: You can only fuse multiple event pets if they all are the **same** type'
    )

    whatfirst = (
        f'{emojis.BP} Try to tier up to T4+ before you start fusing for skills\n'
        f'{emojis.BP} The best normal skill to keep first is {emojis.SKILL_HAPPY} happy'
    )

    skillsimpact = f'{emojis.BP} {emojis.SKILL_HAPPY} **Happy**: Increases the chance to tier up'

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_catch.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_skills.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_skills_special.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_adv.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_fuse.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'PET FUSION',
        description = 'You can fuse pets to tier them up and/or find or transfer normal skills.'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='HOW TO FUSE', value=general, inline=False)
    embed.add_field(name='TIERING UP', value=tiers, inline=False)
    embed.add_field(name='HOW TO GET (AND KEEP) SKILLS', value=skills, inline=False)
    embed.add_field(name='IMPACT ON TYPE', value=type, inline=False)
    embed.add_field(name='WHAT TO DO FIRST', value=whatfirst, inline=False)
    embed.add_field(name='SKILLS THAT AFFECT FUSION', value=skillsimpact, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Pet normal skills
async def embed_pets_skills(prefix):

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

    ascended = (
        f'{emojis.BP} Has a chance to find another pet in adventures\n'
        f'{emojis.BP} The chance is 11.11...% per rank (100% at SS+)\n'
        f'{emojis.BP} This skill has to be unlocked with `pets ascend`\n'
        f'{emojis.BP} You can only ascend pets that have **all** other skills at SS+\n'
        f'{emojis.BP} Pets can only ascend in {emojis.TIME_TRAVEL} TT 26+\n'
        f'{emojis.BP} **You will lose all other skills when ascending**\n'
        f'{emojis.BP} You can **not** lose this skill when fusing\n'
        f'{emojis.BP} You can **not** rank up this skill with adventures\n'
        f'{emojis.BP} To rank up the skill, get all other skills to SS+ and ascend again'
    )

    fighter = (
        f'{emojis.BP} Pet can be used to acquire {emojis.DRAGON_ESSENCE} dragon essence in D1-D9\n'
        f'{emojis.BP} You have a 20% base chance to get an essence after the dungeon\n'
        f'{emojis.BP} This chance increases with skill rank\n'
        f'{emojis.BP} You can **not** find this skill, it is unlocked once a pet reaches Tier X\n'
        f'{emojis.BP} You can **not** lose this skill when fusing\n'
        f'{emojis.BP} To rank up the skill, you have to tier up further (1 rank per tier)\n'
    )

    master = (
        f'{emojis.BP} Increases the tier of pets found with the {emojis.SKILL_ASCENDED} ascended skill\n'
        f'{emojis.BP} You can **not** find this skill, it is unlocked once a pet reaches Tier XX\n'
        f'{emojis.BP} You can **not** lose this skill when fusing\n'
        f'{emojis.BP} This skill can currently not be ranked up\n'
    )

    skillranks = (
        f'{emojis.BP} Every skill has 9 possible ranks\n'
        f'{emojis.BP} The ranks are F, E, D, C, B, A, S, SS and SS+\n'
        f'{emojis.BP} To rank up skills, do adventures (see `{prefix}pet adv`)\n'
        f'{emojis.BP} Higher ranks increase the skill bonus\n'
        f'{emojis.BP} Higher ranks increase the chance to keep a skill when fusing'
    )

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_skills_special.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_catch.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_fusion.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_adv.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'PET SKILLS',
        description = (
            f'Overview of all **normal** pet skills. See `{prefix}pet` on how to get these skills.\n'
            f'To see an overview of the **special** pet skills, see `{prefix}pet skills special`.\n'
            f'Purple and yellow skills are rarer than blue ones.'
        )
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'NORMIE {emojis.SKILL_NORMIE}', value=normie, inline=False)
    embed.add_field(name=f'FAST {emojis.SKILL_FAST}', value=fast, inline=False)
    embed.add_field(name=f'HAPPY {emojis.SKILL_HAPPY}', value=happy, inline=False)
    embed.add_field(name=f'CLEVER {emojis.SKILL_CLEVER}', value=clever, inline=False)
    embed.add_field(name=f'DIGGER {emojis.SKILL_DIGGER}', value=digger, inline=False)
    embed.add_field(name=f'LUCKY {emojis.SKILL_LUCKY}', value=lucky, inline=False)
    embed.add_field(name=f'TIME TRAVELER {emojis.SKILL_TRAVELER}', value=timetraveler, inline=False)
    embed.add_field(name=f'EPIC {emojis.SKILL_EPIC}', value=epic, inline=False)
    embed.add_field(name=f'ASCENDED {emojis.SKILL_ASCENDED}', value=ascended, inline=False)
    embed.add_field(name=f'FIGHTER {emojis.SKILL_FIGHTER}', value=fighter, inline=False)
    embed.add_field(name=f'MASTER {emojis.SKILL_MASTER}', value=master, inline=False)
    embed.add_field(name='SKILL RANKS', value=skillranks, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Pet special skills
async def embed_pets_skills_special(prefix):

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

    skillranks = f'{emojis.BP} Special skills can not be ranked up'

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_skills.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_catch.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_fusion.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_adv.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'SPECIAL PET SKILLS',
        description = (
            f'Overview of all **special** pet skills. Each special skill is unique to a certain special pet and can **not** be lost.\n'
            f'To see an overview of the **normal** pet skills, see `{prefix}pet skills`.'
        )
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'COMPETITIVE {emojis.SKILL_COMPETITIVE}', value=competitive, inline=False)
    embed.add_field(name=f'FARMER {emojis.SKILL_FARMER}', value=farmer, inline=False)
    embed.add_field(name=f'FISHERFISH {emojis.SKILL_FISHER_FISH}', value=fisherfish, inline=False)
    embed.add_field(name=f'FASTER {emojis.SKILL_FASTER}', value=faster, inline=False)
    embed.add_field(name=f'GIFTER {emojis.SKILL_GIFTER}', value=gifter, inline=False)
    embed.add_field(name=f'MONSTER HUNTER {emojis.SKILL_MONSTER_HUNTER}', value=monsterhunter, inline=False)
    embed.add_field(name=f'BOOSTER {emojis.SKILL_BOOSTER}', value=booster, inline=False)
    embed.add_field(name='SKILL RANKS', value=skillranks, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Pet adventures
async def embed_pets_adventures(prefix):

    usage = (
        f'{emojis.BP} Command: `pets adv [type] [petIDs]`\n'
        f'{emojis.BP} Use `pets adv cancel [petID]` to cancel an adventure\n'
        f'{emojis.BP} You can only send **1** pet unless you have the {emojis.SKILL_EPIC} EPIC skill\n'
        f'{emojis.BP} Note: To send all EPIC pets at once, use `pets adv [type] epic`\n'
        f'{emojis.BP} Note: You can not cancel an adventure if the pet has the {emojis.SKILL_TRAVELER} time traveler skill \n'
    )

    types = (
        f'{emojis.BP} **Find**: Pet is more likely to find items\n'
        f'{emojis.BP} **Drill**: Pet is more likely to find coins\n'
        f'{emojis.BP} **Learn**: Pet is more likely to rank up a skill\n'
        f'{emojis.BP} The type does **not** guarantee the outcome \n'
        f'{emojis.BP} Your pet will never come back emptyhanded'
    )

    rewards = (
        f'{emojis.BP} **Items**: {emojis.LOG}{emojis.LOG_EPIC}{emojis.LOG_SUPER}{emojis.LOG_MEGA}{emojis.LOG_HYPER}{emojis.LOG_ULTRA} {emojis.FISH}{emojis.FISH_GOLDEN}{emojis.FISH_EPIC}{emojis.LIFE_POTION}\n'
        f'{emojis.BP} **Coins**: ~ 700k+\n'
        f'{emojis.BP} **Skill rank**: +1 rank of 1 skill the pet has\n'
        f'{emojis.BP} **Pet**: Random T1-3 pet (only if pet has {emojis.SKILL_ASCENDED} ascended skill)\n'
        f'{emojis.BP} Note: You get a pet **in addition** to the other reward'
    )

    normalskillsimpact = (
        f'{emojis.BP} {emojis.SKILL_FAST} **Fast**: Reduces the time to do adventures\n'
        f'{emojis.BP} {emojis.SKILL_DIGGER} **Digger**: Increases the amount of coins you get\n'
        f'{emojis.BP} {emojis.SKILL_LUCKY} **Lucky**: Increases the chance to find better items\n'
        f'{emojis.BP} {emojis.SKILL_TRAVELER} **Time traveler**: Has a chance of finishing instantly\n'
        f'{emojis.BP} {emojis.SKILL_EPIC} **EPIC**: If you send this pet **first**, you can send another\n'
        f'{emojis.BP} {emojis.SKILL_ASCENDED} **Ascended**: Has a chance to find a pet'
    )

    specialskillsimpact = (
        f'{emojis.BP} {emojis.SKILL_FISHER_FISH} **Fisherfish**: Increases the amount of fish you get by 300%\n'
        f'{emojis.BP} {emojis.SKILL_FASTER} **Faster**: Doubles time reduction from {emojis.SKILL_FAST} fast skill\n'
        f'{emojis.BP} {emojis.SKILL_MONSTER_HUNTER} **Monster hunter**: Has a chance to find mob drops\n'
        f'{emojis.BP} {emojis.SKILL_GIFTER} **Gifter**: Has a chance to find a lootbox\n'
        f'{emojis.BP} {emojis.SKILL_BOOSTER} **BOOSTER**: All pets have a chance to advance skills twice'
    )

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_catch.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_fusion.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_skills.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_skills_special.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'PET ADVENTURES',
        description = 'You can send pets on adventures to find items or coins or to rank up their skills.'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='HOW TO SEND PETS', value=usage, inline=False)
    embed.add_field(name='ADVENTURE TYPES', value=types, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NORMAL SKILLS THAT AFFECT ADVENTURES', value=normalskillsimpact, inline=False)
    embed.add_field(name='SPECIAL SKILLS THAT AFFECT ADVENTURES', value=specialskillsimpact, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Pet fusion recommendations
async def embed_fuse(ctx: commands.Context, pet_tier: int, user_tt: int) -> discord.Embed:

    pet_data: database.PetTier = await database.get_pet_tier(ctx, pet_tier, user_tt)

    how_to_get_tier =f'{emojis.BP} {pet_data.fusion_to_get_tier.fusion}'

    what_to_fuse_with_tier = ''
    for fusion in pet_data.fusions_including_tier:
        what_to_fuse_with_tier = (
            f'{what_to_fuse_with_tier}\n'
            f'{emojis.BP} {fusion.fusion} ➜ T{fusion.tier}'
        )
    if what_to_fuse_with_tier == '': what_to_fuse_with_tier = f'{emojis.BP} None'

    note = (
        f'{emojis.BP} Tier up is **not** guaranteed!\n'
        f'{emojis.BP} Lower fusions _might_ be possible but are rarely successful.\n'
        f'{emojis.BP} If you want the maximum chance, do same-tier fusions.\n'
        f'{emojis.BP} You can lose skills in fusions!\n'
        f'{emojis.BP} If you are unsure about fusions, see `{ctx.prefix}pet fusion`'
    )

    guides = (
        f'{emojis.BP} {guide_fusion.format(prefix=ctx.prefix)}\n'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = f'TIER {pet_tier} PET FUSIONS • TT {user_tt}',
        description = 'This guide lists the minimum recommended fusions for a decent tier up chance.'
    )

    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    embed.add_field(name=f'FUSION TO GET A T{pet_tier} PET', value=how_to_get_tier, inline=False)
    embed.add_field(name=f'FUSIONS THAT INCLUDE A T{pet_tier} PET', value=what_to_fuse_with_tier, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed