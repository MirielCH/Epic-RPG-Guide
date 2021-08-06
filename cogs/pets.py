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
            f'{emojis.bp} `{prefix}fuse [tier]` to get recommendations for your current TT.\n'
            f'{emojis.bp} `{prefix}fuse [tier] [tt]` to get recommendations for another TT.\n\n'
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
                    if not 1 <= pet_tier <= 12:
                        await ctx.send(f'Please enter a pet tier between 1 and 12.')
                        return
                    if pet_tier == 12:
                        await ctx.send(
                            f'There is no fusion data for T12 pets yet.\n'
                            f'However, do not try this before TT 25 at the absolute earliest and only use **T11** + **T11**.'
                        )
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
                    current_settings = await database.get_settings(ctx)
                    user_tt = current_settings[0]

                embed = await embed_fuse(ctx.prefix, pet_tier, user_tt)
                await ctx.send(embed=embed)
            else:
                await ctx.send(syntax)
                return
        else:
            await ctx.send(
                f'This command takes a pet of a certain tier and tells you:\n'
                f'{emojis.bp} What you can fuse if you **want** that tier\n'
                f'{emojis.bp} What you can fuse if you **have** that tier\n\n'
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
        f'{emojis.bp} {emojis.timetravel} TT 2+\n'
        f'{emojis.bp} Exception: Event and giveaway pets are not TT locked'
    )

    whattodo = f'{emojis.bp} Send them on adventures (see `{prefix}pet adv`)'


    tier = (
        f'{emojis.bp} Tiers range from I to XII (1 to 12)\n'
        f'{emojis.bp} Increases the number of items you get in adventures\n'
        f'{emojis.bp} Increases the chance to increase a skill rank in adventures\n'
        f'{emojis.bp} Increases the chance to keep a skill when fusing\n'
        f'{emojis.bp} Increased by fusing pets (see `{prefix}pet fusion`)'
    )

    normalskills = (
        f'{emojis.bp} There are 8 normal skills (see `{prefix}pet skills`)\n'
        f'{emojis.bp} Skills have a rank that ranges from F to SS+\n'
        f'{emojis.bp} Mainly found by fusing pets (see `{prefix}pet fusion`)\n'
        f'{emojis.bp} Small chance of getting a skill when catching pets'
    )

    specialskills = (
        f'{emojis.bp} There are 6 special skills (see `{prefix}pet skills special`)\n'
        f'{emojis.bp} Special skills don\'t have a rank and can **not** be lost\n'
        f'{emojis.bp} Only available on special event reward pets\n'
        f'{emojis.bp} Each special skill is unique to a certain special pet'
    )

    type = (
        f'{emojis.bp} The basic types are {emojis.petcat} cat, {emojis.petdog} dog and {emojis.petdragon} dragon\n'
        f'{emojis.bp} Event pets can have unique types\n'
        f'{emojis.bp} The type you get when catching pets is random\n'
        f'{emojis.bp} All types are purely cosmetic'
    )

    score = (
        f'{emojis.bp} The pet score increases your chance to win pet tournaments\n'
        f'{emojis.bp} See `{prefix}event pet tournament` for details about tournaments\n'
        f'{emojis.bp} The pet score is influenced by tier, skills and skill ranks\n'
        f'{emojis.bp} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Pets#Pet_Score)'
    )

    guides = (
        f'{emojis.bp} {guide_catch.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_fusion.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_skills.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_skills_special.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_adv.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_fuse.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'PETS',
        description = (
            f'Pets have tiers, types and skills and can be sent on adventures to find stuff for you.\n'
            f'You can have up to (5 + TT) pets (= 7 pets at {emojis.timetravel} TT 2).'
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
        f'{emojis.bp} After using `training` (4% chance, 10% with {emojis.horset9} T9 horse)\n'
        f'{emojis.bp} By ranking at least 3rd in {emojis.horset9} T9 horse races\n'
        f'{emojis.bp} In some seasonal events (these are not TT locked)\n'
        f'{emojis.bp} In some dev giveaways (these are not TT locked)\n'
        f'{emojis.bp} By sending {emojis.skillascended} ascended pets on adventures (see `{prefix}pet adv`)'
    )

    catch =  (
        f'{emojis.bp} Pets you encounter have a {emojis.pethappiness} happiness and {emojis.pethunger} hunger stat\n'
        f'{emojis.bp} You can enter a line of commands to influence these stats\n'
        f'{emojis.bp} `feed` decreases hunger by 18-22\n'
        f'{emojis.bp} `pat` increases happiness by 8-12\n'
        f'{emojis.bp} If happiness is 85+ higher than hunger, catch chance is 100%\n'
        f'{emojis.bp} Example: `feed feed pat pat pat`\n'
        f'{emojis.bp} You can only use up to 6 commands\n'
        f'{emojis.bp} Less commands = lower catch chance but higher chance for the pet to have a normal skill if caught (see `{prefix}pet skills`)'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_fusion.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_skills.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_skills_special.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_adv.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'CATCHING PETS',
        description = f'With the exception of event and giveaway pets you can only find and catch pets in {emojis.timetravel} TT 2+'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='HOW TO FIND PETS', value=source, inline=False)
    embed.add_field(name='HOW TO CATCH PETS', value=catch, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Pet fusion
async def embed_pets_fusion(prefix):

    general = (
        f'{emojis.bp} Use `pets fusion [petID1] [petID2]`\n'
        f'{emojis.bp} You can fuse more than 2 pets but you should only do that if you want to maximize the chance to keep certain skills or want to control the type you get\n'
        f'{emojis.bp} You can **not** lose tiers when fusing\n'
        f'{emojis.bp} You can **not** lose special skills when fusing\n'
        f'{emojis.bp} You **can** lose normal skills when fusing\n'
        f'{emojis.bp} Exception: You can not lose {emojis.skillascended} ascended and {emojis.skillfighter} fighter'
    )

    tiers = (
        f'{emojis.bp} Check `{prefix}fuse` on what to fuse to get a tier up\n'
        f'{emojis.bp} For the highest chance of a tier up, fuse 2 pets of the **same** tier\n'
        f'{emojis.bp} The chance to tier up gets lower the higher your tier is'
    )

    skills = (
        f'{emojis.bp} You have a random chance of getting a new normal skill when fusing\n'
        f'{emojis.bp} You can **not** get special skills when fusing\n'
        f'{emojis.bp} The more skills you already have, the lower the chance to get one\n'
        f'{emojis.bp} If your sole goal is getting skills, fuse with T1 throwaway pets\n'
        f'{emojis.bp} You can keep normal skills you already have, but the chance depends on the skill rank and how many of that skill you have in the fusion (see `{prefix}pet skills`)\n'
        f'{emojis.bp} To maximize the chance to keep normal skills, rank them to SS+ first and fuse pets that have the same skill\n'
        f'{emojis.bp} The exact chances to keep skills are unknown'
    )

    type = (
        f'{emojis.bp} The resulting type depends on the most used type in the fusion\n'
        f'{emojis.bp} If you fuse different types evenly, the result is randomly one of those types\n'
        f'{emojis.bp} Example 1: {emojis.petcat} + {emojis.petcat} results in {emojis.petcat}\n'
        f'{emojis.bp} Example 2: {emojis.petdog} + {emojis.petcat} + {emojis.petdog} results in {emojis.petdog}\n'
        f'{emojis.bp} Example 3: {emojis.petcat} + {emojis.petdog} results in {emojis.petcat} **or** {emojis.petdog}\n'
        f'{emojis.bp} Exception: Fusing an event pet will always give you the event pet back\n'
        f'{emojis.bp} Note: You can only fuse multiple event pets if they all are the **same** type'
    )

    whatfirst = (
        f'{emojis.bp} Try to tier up to T4+ before you start fusing for skills\n'
        f'{emojis.bp} The best normal skill to keep first is {emojis.skillhappy} happy'
    )

    skillsimpact = f'{emojis.bp} {emojis.skillhappy} **Happy**: Increases the chance to tier up'

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_catch.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_skills.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_skills_special.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_adv.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_fuse.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
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

    normie = f'{emojis.bp} This is not a skill, it simply means the pet has no skills'

    fast = (
        f'{emojis.bp} Reduces the time to do adventures\n'
        f'{emojis.bp} Reduces the time down to 2h 33m 36s at rank SS+'
    )

    happy = f'{emojis.bp} Increases the chance to tier up when fusing'

    clever = f'{emojis.bp} Increases the chance to rank up skills in adventures'

    digger = f'{emojis.bp} Increases the amount of coins you get in adventures'

    lucky = f'{emojis.bp} Increases the chance to find better items in adventures'

    timetraveler = (
        f'{emojis.bp} Has a chance of finishing an adventure instantly\n'
        f'{emojis.bp} Note: You can not cancel an adventure if the pet has this skill\n'
    )

    epic = (
        f'{emojis.bp} If you send this pet on an adventure, you can send another\n'
        f'{emojis.bp} Note: You have to send the pet with this skill **first**'
    )

    ascended = (
        f'{emojis.bp} Has a chance to find another pet in adventures\n'
        f'{emojis.bp} This skill has to be unlocked with `pets ascend`\n'
        f'{emojis.bp} You can only ascend pets that have **all** other skills at SS+\n'
        f'{emojis.bp} Pets can only ascend in {emojis.timetravel} TT 26+\n'
        f'{emojis.bp} **You will lose all other skills when ascending**\n'
        f'{emojis.bp} You can **not** lose this skill when fusing\n'
        f'{emojis.bp} You can **not** rank up this skill with adventures\n'
        f'{emojis.bp} To rank up the skill, get all other skills to SS+ and ascend again'
    )

    fighter = (
        f'{emojis.bp} Pet can be used to acquire {emojis.dragonessence} dragon essence in D1-D9\n'
        f'{emojis.bp} You have a 20% base chance to get an essence after the dungeon\n'
        f'{emojis.bp} This chance increases with skill rank\n'
        f'{emojis.bp} You can **not** find this skill, it is unlocked once a pet reaches Tier X\n'
        f'{emojis.bp} You can **not** lose this skill when fusing\n'
        f'{emojis.bp} To rank up the skill, you have to tier up further (1 rank per tier)\n'
        f'{emojis.bp} Note: You need to be in {emojis.timetravel} TT 25+ to be able to use the skill'
    )

    skillranks = (
        f'{emojis.bp} Every skill has 9 possible ranks\n'
        f'{emojis.bp} The ranks are F, E, D, C, B, A, S, SS and SS+\n'
        f'{emojis.bp} To rank up skills, do adventures (see `{prefix}pet adv`)\n'
        f'{emojis.bp} Higher ranks increase the skill bonus\n'
        f'{emojis.bp} Higher ranks increase the chance to keep a skill when fusing'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_skills_special.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_catch.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_fusion.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_adv.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'PET SKILLS',
        description = (
            f'Overview of all **normal** pet skills. See `{prefix}pet` on how to get these skills.\n'
            f'To see an overview of the **special** pet skills, see `{prefix}pet skills special`.\n'
            f'Purple and yellow skills are rarer than blue ones.'
        )
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'NORMIE {emojis.skillnormie}', value=normie, inline=False)
    embed.add_field(name=f'FAST {emojis.skillfast}', value=fast, inline=False)
    embed.add_field(name=f'HAPPY {emojis.skillhappy}', value=happy, inline=False)
    embed.add_field(name=f'CLEVER {emojis.skillclever}', value=clever, inline=False)
    embed.add_field(name=f'DIGGER {emojis.skilldigger}', value=digger, inline=False)
    embed.add_field(name=f'LUCKY {emojis.skilllucky}', value=lucky, inline=False)
    embed.add_field(name=f'TIME TRAVELER {emojis.skilltraveler}', value=timetraveler, inline=False)
    embed.add_field(name=f'EPIC {emojis.skillepic}', value=epic, inline=False)
    embed.add_field(name=f'ASCENDED {emojis.skillascended}', value=ascended, inline=False)
    embed.add_field(name=f'FIGHTER {emojis.skillfighter}', value=fighter, inline=False)
    embed.add_field(name='SKILL RANKS', value=skillranks, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Pet special skills
async def embed_pets_skills_special(prefix):

    competitive = (
        f'{emojis.bp} The pet has 1 more score point\n'
        f'{emojis.bp} This skill is unique to the {emojis.petpanda} epic panda pet\n'
        f'{emojis.bp} This pet was given to the first player who reached {emojis.timetravel} TT 100'
    )

    fisherfish = (
        f'{emojis.bp} If the pet finds fish, you get 3 times the amount\n'
        f'{emojis.bp} This skill is unique to the {emojis.petpinkfish} pink fish pet\n'
        f'{emojis.bp} This pet is a reward in the valentine event'
    )

    faster = (
        f'{emojis.bp} If the pet also has the {emojis.skillfast} fast skill, the time reduction is doubled\n'
        f'{emojis.bp} This skill is unique to the {emojis.petgoldenbunny} golden bunny pet\n'
        f'{emojis.bp} This pet is a reward in the easter event'
    )

    monsterhunter = (
        f'{emojis.bp} Has a chance to find random mob drops in pet adventures\n'
        f'{emojis.bp} This skill is unique to the {emojis.petpumpkinbat} pumpkin bat pet\n'
        f'{emojis.bp} This pet is a reward in the halloween event'
    )

    gifter = (
        f'{emojis.bp} Has a chance to find a random lootbox in a pet adventure\n'
        f'{emojis.bp} This skill is unique to the {emojis.petsnowball} snowball pet\n'
        f'{emojis.bp} This pet is a reward in the christmas event'
    )

    booster = (
        f'{emojis.bp} **All** pets have a chance to advance skills twice in a pet adventure\n'
        f'{emojis.bp} This skill is unique to the {emojis.pethamster} hamster pet\n'
        f'{emojis.bp} This pet is a reward in the anniversary event'
    )

    skillranks = f'{emojis.bp} Special skills can not be ranked up'

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_skills.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_catch.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_fusion.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_adv.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'SPECIAL PET SKILLS',
        description = (
            f'Overview of all **special** pet skills. Each special skill is unique to a certain special pet and can **not** be lost.\n'
            f'To see an overview of the **normal** pet skills, see `{prefix}pet skills`.'
        )
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'COMPETITIVE {emojis.skillcompetitive}', value=competitive, inline=False)
    embed.add_field(name=f'FISHERFISH {emojis.skillfisherfish}', value=fisherfish, inline=False)
    embed.add_field(name=f'FASTER {emojis.skillfaster}', value=faster, inline=False)
    embed.add_field(name=f'MONSTER HUNTER {emojis.skillmonsterhunter}', value=monsterhunter, inline=False)
    embed.add_field(name=f'GIFTER {emojis.skillgifter}', value=gifter, inline=False)
    embed.add_field(name=f'BOOSTER {emojis.skillbooster}', value=booster, inline=False)
    embed.add_field(name='SKILL RANKS', value=skillranks, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Pet adventures
async def embed_pets_adventures(prefix):

    usage = (
        f'{emojis.bp} Command: `pets adv [type] [petIDs]`\n'
        f'{emojis.bp} Use `pets adv cancel [petID]` to cancel an adventure\n'
        f'{emojis.bp} You can only send **1** pet unless you have the {emojis.skillepic} EPIC skill\n'
        f'{emojis.bp} Note: To send all EPIC pets at once, use `pets adv [type] epic`\n'
        f'{emojis.bp} Note: You can not cancel an adventure if the pet has the {emojis.skilltraveler} time traveler skill \n'
    )

    types = (
        f'{emojis.bp} **Find**: Pet is more likely to find items\n'
        f'{emojis.bp} **Drill**: Pet is more likely to find coins\n'
        f'{emojis.bp} **Learn**: Pet is more likely to rank up a skill\n'
        f'{emojis.bp} The type does **not** guarantee the outcome \n'
        f'{emojis.bp} Your pet will never come back emptyhanded'
    )

    rewards = (
        f'{emojis.bp} **Items**: {emojis.log}{emojis.logepic}{emojis.logsuper}{emojis.logmega}{emojis.loghyper}{emojis.logultra} {emojis.fish}{emojis.fishgolden}{emojis.fishepic}{emojis.lifepotion}\n'
        f'{emojis.bp} **Coins**: ~ 700k+\n'
        f'{emojis.bp} **Skill rank**: +1 rank of 1 skill the pet has\n'
        f'{emojis.bp} **Pet**: Random T1-3 pet (only if pet has {emojis.skillascended} ascended skill)\n'
        f'{emojis.bp} Note: You get a pet **in addition** to the other reward'
    )

    normalskillsimpact = (
        f'{emojis.bp} {emojis.skillfast} **Fast**: Reduces the time to do adventures\n'
        f'{emojis.bp} {emojis.skilldigger} **Digger**: Increases the amount of coins you get\n'
        f'{emojis.bp} {emojis.skilllucky} **Lucky**: Increases the chance to find better items\n'
        f'{emojis.bp} {emojis.skilltraveler} **Time traveler**: Has a chance of finishing instantly\n'
        f'{emojis.bp} {emojis.skillepic} **EPIC**: If you send this pet **first**, you can send another\n'
        f'{emojis.bp} {emojis.skillascended} **Ascended**: Has a chance to find a pet'
    )

    specialskillsimpact = (
        f'{emojis.bp} {emojis.skillfisherfish} **Fisherfish**: Increases the amount of fish you get by 300%\n'
        f'{emojis.bp} {emojis.skillfaster} **Faster**: Doubles time reduction from {emojis.skillfast} fast skill\n'
        f'{emojis.bp} {emojis.skillmonsterhunter} **Monster hunter**: Has a chance to find mob drops\n'
        f'{emojis.bp} {emojis.skillgifter} **Gifter**: Has a chance to find a lootbox\n'
        f'{emojis.bp} {emojis.skillbooster} **BOOSTER**: All pets have a chance to advance skills twice'
    )

    guides = (
        f'{emojis.bp} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_catch.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_fusion.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_skills.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_skills_special.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
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
async def embed_fuse(prefix, pet_tier, user_tt):

    if pet_tier == 1:
        how_to_get_tier = f'{emojis.bp} There are no lower tier fusions'
        what_to_fuse_with_tier = f'{emojis.bp} **T1** + **T1** ➜ **T2**'
    elif pet_tier == 2:
        how_to_get_tier = f'{emojis.bp} **T1** + **T1**'
        what_to_fuse_with_tier = f'{emojis.bp} **T1** + **T2** ➜ **T3**'
    elif pet_tier == 3:
        how_to_get_tier = f'{emojis.bp} **T1** + **T2**'
        if 0 <= user_tt <= 9:
            what_to_fuse_with_tier = f'{emojis.bp} **T3** + **T3** ➜ **T4**'
        elif 10 <= user_tt <= 24:
            what_to_fuse_with_tier = f'{emojis.bp} **T2** + **T3** ➜ **T4**'
        else:
            what_to_fuse_with_tier = f'{emojis.bp} **T1** + **T3** ➜ **T4**'
    elif pet_tier == 4:
        if 0 <= user_tt <= 9:
            how_to_get_tier = f'{emojis.bp} **T3** + **T3**'
            what_to_fuse_with_tier = f'{emojis.bp} **T4** + **T4** ➜ **T5**'
        elif 10 <= user_tt <= 24:
            how_to_get_tier = f'{emojis.bp} **T2** + **T3**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T3** + **T4** ➜ **T5**\n'
                f'{emojis.bp} **T4** + **T5** ➜ **T6**'
            )
        elif 25 <= user_tt <= 40:
            how_to_get_tier = f'{emojis.bp} **T1** + **T3**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T2** + **T4** ➜ **T5**\n'
                f'{emojis.bp} **T4** + **T6** ➜ **T7**'
            )
        elif 41 <= user_tt <= 60:
            how_to_get_tier = f'{emojis.bp} **T1** + **T3**'
            what_to_fuse_with_tier = f'{emojis.bp} **T1** + **T4** ➜ **T5**'
        elif 61 <= user_tt <= 90:
            how_to_get_tier = f'{emojis.bp} **T1** + **T3**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T1** + **T4** ➜ **T5**\n'
                f'{emojis.bp} **T4** + **T7** ➜ **T8**'
            )
        else:
            how_to_get_tier = f'{emojis.bp} **T1** + **T3**'
            what_to_fuse_with_tier = f'{emojis.bp} **T1** + **T4** ➜ **T5**'
    elif pet_tier == 5:
        if 0 <= user_tt <= 9:
            how_to_get_tier = f'{emojis.bp} **T4** + **T4**'
            what_to_fuse_with_tier = f'{emojis.bp} **T5** + **T5** ➜ **T6**'
        elif 10 <= user_tt <= 24:
            how_to_get_tier = f'{emojis.bp} **T3** + **T4**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T4** + **T5** ➜ **T6**\n'
                f'{emojis.bp} **T5** + **T6** ➜ **T7**'
            )
        elif 25 <= user_tt <= 40:
            how_to_get_tier = f'{emojis.bp} **T2** + **T4**'
            what_to_fuse_with_tier = f'{emojis.bp} **T3** + **T5** ➜ **T6**'
        elif 41 <= user_tt <= 60:
            how_to_get_tier = f'{emojis.bp} **T1** + **T4**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T2** + **T5** ➜ **T6**\n'
                f'{emojis.bp} **T5** + **T7** ➜ **T8**'
            )
        elif 61 <= user_tt <= 90:
            how_to_get_tier = f'{emojis.bp} **T1** + **T4**'
            what_to_fuse_with_tier = f'{emojis.bp} **T1** + **T5** ➜ **T6**'
        else:
            how_to_get_tier = f'{emojis.bp} **T1** + **T4**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T1** + **T5** ➜ **T6**\n'
                f'{emojis.bp} **T5** + **T8** ➜ **T9**'
            )
    elif pet_tier == 6:
        if 0 <= user_tt <= 9:
            how_to_get_tier = f'{emojis.bp} **T5** + **T5**'
            what_to_fuse_with_tier = f'{emojis.bp} **T6** + **T6** ➜ **T7**'
        elif 10 <= user_tt <= 24:
            how_to_get_tier = f'{emojis.bp} **T4** + **T5**'
            what_to_fuse_with_tier = f'{emojis.bp} **T5** + **T6** ➜ **T7**'
        elif 25 <= user_tt <= 40:
            how_to_get_tier = f'{emojis.bp} **T3** + **T5**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T4** + **T6** ➜ **T7**\n'
                f'{emojis.bp} **T6** + **T7** ➜ **T8**'
            )
        elif 41 <= user_tt <= 60:
            how_to_get_tier = f'{emojis.bp} **T2** + **T5**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T3** + **T6** ➜ **T7**\n'
                f'{emojis.bp} **T6** + **T8** ➜ **T9**'
            )
        elif 61 <= user_tt <= 90:
            how_to_get_tier = f'{emojis.bp} **T1** + **T5**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T2** + **T6** ➜ **T7**\n'
                f'{emojis.bp} **T6** + **T8** ➜ **T9**'
            )
        else:
            how_to_get_tier = f'{emojis.bp} **T1** + **T5**'
            what_to_fuse_with_tier = f'{emojis.bp} **T2** + **T6** ➜ **T7**'
    elif pet_tier == 7:
        if 0 <= user_tt <= 9:
            how_to_get_tier = f'{emojis.bp} **T6** + **T6**'
            what_to_fuse_with_tier = f'{emojis.bp} **T7** + **T7** ➜ **T8**'
        elif 10 <= user_tt <= 24:
            how_to_get_tier = f'{emojis.bp} **T5** + **T6**'
            what_to_fuse_with_tier = f'{emojis.bp} **T7** + **T7** ➜ **T8**'
        elif 25 <= user_tt <= 40:
            how_to_get_tier = f'{emojis.bp} **T4** + **T6**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T6** + **T7** ➜ **T8**\n'
                f'{emojis.bp} **T7** + **T8** ➜ **T9**'
            )
        elif 41 <= user_tt <= 60:
            how_to_get_tier = f'{emojis.bp} **T3** + **T6**'
            what_to_fuse_with_tier = f'{emojis.bp} **T5** + **T7** ➜ **T8**'
        elif 61 <= user_tt <= 90:
            how_to_get_tier = f'{emojis.bp} **T2** + **T6**'
            what_to_fuse_with_tier = f'{emojis.bp} **T4** + **T7** ➜ **T8**'
        else:
            how_to_get_tier = f'{emojis.bp} **T2** + **T6**'
            what_to_fuse_with_tier = f'{emojis.bp} **T3** + **T7** ➜ **T8**'
    elif pet_tier == 8:
        if 0 <= user_tt <= 9:
            how_to_get_tier = f'{emojis.bp} **T7** + **T7**'
            what_to_fuse_with_tier = f'{emojis.bp} **T8** + **T8** ➜ **T9**'
        elif 10 <= user_tt <= 24:
            how_to_get_tier = f'{emojis.bp} **T7** + **T7**'
            what_to_fuse_with_tier = f'{emojis.bp} **T8** + **T8** ➜ **T9**'
        elif 25 <= user_tt <= 40:
            how_to_get_tier = f'{emojis.bp} **T6** + **T7**'
            what_to_fuse_with_tier = f'{emojis.bp} **T7** + **T8** ➜ **T9**'
        elif 41 <= user_tt <= 60:
            how_to_get_tier = f'{emojis.bp} **T5** + **T7**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T6** + **T8** ➜ **T9**\n'
                f'{emojis.bp} **T8** + **T9** ➜ **T10**'
            )
        elif 61 <= user_tt <= 90:
            how_to_get_tier = f'{emojis.bp} **T4** + **T7**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T6** + **T8** ➜ **T9**\n'
                f'{emojis.bp} **T8** + **T9** ➜ **T10**'
            )
        else:
            how_to_get_tier = f'{emojis.bp} **T3** + **T7**'
            what_to_fuse_with_tier = (
                f'{emojis.bp} **T5** + **T8** ➜ **T9**\n'
                f'{emojis.bp} **T8** + **T9** ➜ **T10**'
            )
    elif pet_tier == 9:
        if 0 <= user_tt <= 9:
            how_to_get_tier = f'{emojis.bp} **T8** + **T8**'
            what_to_fuse_with_tier = f'{emojis.bp} None. A T9 is unlikely to tier up in this TT.'
        elif 10 <= user_tt <= 24:
            how_to_get_tier = f'{emojis.bp} **T8** + **T8**'
            what_to_fuse_with_tier = f'{emojis.bp} **T9** + **T9** ➜ **T10**'
        elif 25 <= user_tt <= 40:
            how_to_get_tier = f'{emojis.bp} **T7** + **T8**'
            what_to_fuse_with_tier = f'{emojis.bp} **T9** + **T9** ➜ **T10**'
        elif 41 <= user_tt <= 60:
            how_to_get_tier = f'{emojis.bp} **T6** + **T8**'
            what_to_fuse_with_tier = f'{emojis.bp} **T8** + **T9** ➜ **T10**'
        elif 61 <= user_tt <= 90:
            how_to_get_tier = f'{emojis.bp} **T6** + **T8**'
            what_to_fuse_with_tier = f'{emojis.bp} **T8** + **T9** ➜ **T10**'
        else:
            how_to_get_tier = f'{emojis.bp} **T5** + **T8**'
            what_to_fuse_with_tier = f'{emojis.bp} **T8** + **T9** ➜ **T10**'
    elif pet_tier == 10:
        if 0 <= user_tt <= 9:
            how_to_get_tier = f'{emojis.bp} None. A T10 is unlikely to get in this TT.'
            what_to_fuse_with_tier = f'{emojis.bp} None. A T10 is unlikely to tier up in this TT.'
        elif 10 <= user_tt <= 24:
            how_to_get_tier = f'{emojis.bp} **T9** + **T9**'
            what_to_fuse_with_tier = f'{emojis.bp} None. A T10 is unlikely to tier up in this TT.'
        elif 25 <= user_tt <= 40:
            how_to_get_tier = f'{emojis.bp} **T9** + **T9**'
            what_to_fuse_with_tier = f'{emojis.bp} **T10** + **T10** ➜ **T11**'
        else:
            how_to_get_tier = f'{emojis.bp} **T8** + **T9**'
            what_to_fuse_with_tier = f'{emojis.bp} **T10** + **T10** ➜ **T11**'
    elif pet_tier == 11:
        if 0 <= user_tt <= 9:
            how_to_get_tier = f'{emojis.bp} None. A T11 is unlikely to get in this TT.'
            what_to_fuse_with_tier = f'{emojis.bp} None. This is the maximum tier.'
        elif 10 <= user_tt <= 24:
            how_to_get_tier = f'{emojis.bp} None. A T11 is unlikely to get in this TT.'
            what_to_fuse_with_tier = f'{emojis.bp} None. This is the maximum tier.'
        else:
            how_to_get_tier = f'{emojis.bp} **T10** + **T10**'
            what_to_fuse_with_tier = f'{emojis.bp} None. This is the maximum tier.'

    note = (
        f'{emojis.bp} Tier up is **not** guaranteed!\n'
        f'{emojis.bp} If you want the maximum chance, do same-tier fusions.\n'
        f'{emojis.bp} You can lose skills in fusions!\n'
        f'{emojis.bp} If you are unsure about fusions, see `{prefix}pet fusion`'
    )

    guides = (
        f'{emojis.bp} {guide_fusion.format(prefix=prefix)}\n'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = f'TIER {pet_tier} PET FUSIONS • TT {user_tt}'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'MINIMUM FUSION TO GET A T{pet_tier} PET', value=how_to_get_tier, inline=False)
    embed.add_field(name=f'MINIMUM FUSIONS THAT INCLUDE A T{pet_tier} PET', value=what_to_fuse_with_tier, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed