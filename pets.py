# pets.py

import discord
import emojis
import global_data

# Pets overview
async def pets(prefix):

    requirements =  f'{emojis.bp} {emojis.timetravel} TT 2+\n'\
                    f'{emojis.bp} Exception: Event and giveaway pets are not TT locked'
            
    whattodo =      f'{emojis.bp} Send them on adventures (see `{prefix}petadv`)'
                     
    tier =          f'{emojis.bp} Tiers range from I to IX (1 to 9)\n'\
                    f'{emojis.bp} Increases the number of items you get in adventures\n'\
                    f'{emojis.bp} Increases the chance to increase a skill rank in adventures\n'\
                    f'{emojis.bp} Increases the chance to keep a skill when fusing\n'\
                    f'{emojis.bp} Increased by fusing pets (see `{prefix}petfusion`)'

    skills =        f'{emojis.bp} There are 8 different skills (see `{prefix}petskills`)\n'\
                    f'{emojis.bp} Skills have a rank that ranges from F to SS+\n'\
                    f'{emojis.bp} Mainly found by fusing pets (see `{prefix}petfusion`)\n'\
                    f'{emojis.bp} Small chance of getting a skill when catching pets'
                    
    type =          f'{emojis.bp} The basic types are {emojis.petcat} cat, {emojis.petdog} dog and {emojis.petdragon} dragon\n'\
                    f'{emojis.bp} Event pets can have unique types\n'\
                    f'{emojis.bp} The type you get when catching pets is random\n'\
                    f'{emojis.bp} All types are purely cosmetic'
                    
    guides =        f'{emojis.bp} `{prefix}petcatch` : How to find and catch pets\n'\
                    f'{emojis.bp} `{prefix}petfusion` : Details about pet fusion\n'\
                    f'{emojis.bp} `{prefix}petskills` : Details about pet skills\n'\
                    f'{emojis.bp} `{prefix}petadv` : Details about pet adventures'

    embed = discord.Embed(
        color = global_data.color,
        title = f'PETS',
        description =   f'Pets have tiers, types and skills and can be sent on adventures to find stuff for you.\n'\
                        f'You can have up to (5 + TT) pets (= 7 pets at {emojis.timetravel} TT 2).'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name=f'WHAT TO DO WITH PETS', value=whattodo, inline=False)
    embed.add_field(name=f'TIER', value=tier, inline=False)
    embed.add_field(name=f'SKILLS', value=skills, inline=False)
    embed.add_field(name=f'TYPE', value=type, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=guides, inline=False)
            
    return (thumbnail, embed)

# Catching pets
async def petscatch(prefix):
          
    source =        f'{emojis.bp} After using `training` (4% chance, 10% with {emojis.horset9} T9 horse)\n'\
                    f'{emojis.bp} By ranking at least 3rd in {emojis.horset9} T9 horse races\n'\
                    f'{emojis.bp} In some seasonal events (these are not TT locked)\n'\
                    f'{emojis.bp} In some dev giveaways (these are not TT locked)\n'\
                    f'{emojis.bp} By sending {emojis.skillascended} ascended pets on adventures (see `{prefix}petadv`)'

    catch =         f'{emojis.bp} Pets you encounter have a {emojis.pethappiness} happiness and {emojis.pethunger} hunger stat\n'\
                    f'{emojis.bp} You can enter a line of commands to influence these stats\n'\
                    f'{emojis.bp} `feed` decreases hunger by 18-22\n'\
                    f'{emojis.bp} `pat` increases happiness by 8-12\n'\
                    f'{emojis.bp} If happiness is 85+ higher than hunger, catch chance is 100%\n'\
                    f'{emojis.bp} Example: `feed feed pat pat pat`\n'\
                    f'{emojis.bp} You can only use up to 6 commands\n'\
                    f'{emojis.bp} Less commands = lower catch chance but higher chance for the pet to have a skill if caught (see `{prefix}petskills`)'

    guides =        f'{emojis.bp} `{prefix}pets` : Pets overview\n'\
                    f'{emojis.bp} `{prefix}petfusion` : Details about pet fusion\n'\
                    f'{emojis.bp} `{prefix}petskills` : Details about pet skills\n'\
                    f'{emojis.bp} `{prefix}petadv` : Details about pet adventures'

    embed = discord.Embed(
        color = global_data.color,
        title = f'CATCHING PETS',
        description =   f'With the exception of event and giveaway pets you can only find and catch pets in {emojis.timetravel} TT 2+'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'HOW TO FIND PETS', value=source, inline=False)
    embed.add_field(name=f'HOW TO CATCH PETS', value=catch, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=guides, inline=False)
            
    return (thumbnail, embed)

# Pet fusion
async def petsfusion(prefix):
          
    general =       f'{emojis.bp} Use `pets fusion [petID1] [petID2]`\n'\
                    f'{emojis.bp} You can fuse more than 2 pets but you shouldn\'t\n'\
                    f'{emojis.bp} You can **not** lose tiers when fusing\n'\
                    f'{emojis.bp} You **can** lose skills when fusing\n'\
                    f'{emojis.bp} Exception: You can not lose the {emojis.skillascended} ascended skill'

    tiers =         f'{emojis.bp} Fuse 2 pets of the **same** tier for max chance to get a tier\n'\
                    f'{emojis.bp} The chance to tier up gets lower the higher your tier is'

    skills =        f'{emojis.bp} You have a random chance of getting a new skill when fusing\n'\
                    f'{emojis.bp} The more skills you already have, the lower the chance\n'\
                    f'{emojis.bp} If your sole goal is getting skills, fuse with T1 pets\n'\
                    f'{emojis.bp} You can keep skills you already have, but the chance depends on the skill rank (see `{prefix}petskills`)\n'\
                    f'{emojis.bp} To maximize the chance to keep skills rank them to SS+ first\n'\
                    f'{emojis.bp} The max chance to keep a skill is 90%'

    type =          f'{emojis.bp} Fusing changes your pet type randomly\n'\
                    f'{emojis.bp} Exception: Fusing an event pet will give you the event pet back\n'\
                    f'{emojis.bp} Note: If you fuse 2+ event pets, you will **lose all but one**'

    whatfirst =     f'{emojis.bp} Try to tier up to T4+ before you start fusing for skills\n'\
                    f'{emojis.bp} The best skill to keep first is {emojis.skillhappy} happy'
                    
    skillsimpact =  f'{emojis.bp} {emojis.skillhappy} **Happy**: Increases the chance to tier up'

    guides =        f'{emojis.bp} `{prefix}pets` : Pets overview\n'\
                    f'{emojis.bp} `{prefix}petcatch` : How to find and catch pets\n'\
                    f'{emojis.bp} `{prefix}petskills` : Details about pet skills\n'\
                    f'{emojis.bp} `{prefix}petadv` : Details about pet adventures'

    embed = discord.Embed(
        color = global_data.color,
        title = f'PET FUSION',
        description =   f'You can fuse pets to tier them up and/or find or transfer skills.'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'HOW TO FUSE', value=general, inline=False)
    embed.add_field(name=f'TIERING UP', value=tiers, inline=False)
    embed.add_field(name=f'HOW TO GET (AND KEEP) SKILLS', value=skills, inline=False)
    embed.add_field(name=f'IMPACT ON TYPE', value=type, inline=False)
    embed.add_field(name=f'WHAT TO DO FIRST', value=whatfirst, inline=False)
    embed.add_field(name=f'SKILLS THAT AFFECT FUSION', value=skillsimpact, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=guides, inline=False)
            
    return (thumbnail, embed)

# Pet skills
async def petsskills(prefix):
          
    normie =        f'{emojis.bp} This is not a skill, it simply means the pet has no skills'

    fast =          f'{emojis.bp} Reduces the time to do adventures\n'\
                    f'{emojis.bp} Reduces the time down to 2h 33m 36s at rank SS+'

    happy =         f'{emojis.bp} Increases the chance to tier up when fusing'

    clever =        f'{emojis.bp} Increases the chance to rank up skills in adventures'
    
    digger =        f'{emojis.bp} Increases the amount of coins you get in adventures'
    
    lucky =         f'{emojis.bp} Increases the chance to find better items in adventures'
    
    timetraveler =  f'{emojis.bp} Has a chance of finishing an adventure instantly'
    
    epic =          f'{emojis.bp} If you send this pet on an adventure, you can send another\n'\
                    f'{emojis.bp} Note: You have to send the pet with this skill **first**'
    
    ascended =      f'{emojis.bp} Has a chance to find another pet in adventures\n'\
                    f'{emojis.bp} This skill has to be unlocked with `pets ascend`\n'\
                    f'{emojis.bp} You can only ascend pets that have **all** other skills at SS+\n'\
                    f'{emojis.bp} **You will lose all other skills when ascending**\n'\
                    f'{emojis.bp} You can **not** lose this skill when fusing\n'\
                    f'{emojis.bp} You can **not** rank up this skill with adventures\n'\
                    f'{emojis.bp} To rank up the skill, get all other skills to SS+ and ascend again\n'\
    
    skillranks =    f'{emojis.bp} Every skill has 9 possible ranks\n'\
                    f'{emojis.bp} The ranks are F, E, D, C, B, A, S, SS and SS+\n'\
                    f'{emojis.bp} To rank up skills, do adventures (see `{prefix}petadv`)\n'\
                    f'{emojis.bp} Higher ranks increase the skill bonus\n'\
                    f'{emojis.bp} Higher ranks increase the chance to keep a skill when fusing'
    
    guides =        f'{emojis.bp} `{prefix}pets` : Pets overview\n'\
                    f'{emojis.bp} `{prefix}petcatch` : How to find and catch pets\n'\
                    f'{emojis.bp} `{prefix}petfusion` : Details about pet fusion\n'\
                    f'{emojis.bp} `{prefix}petadv` : Details about pet adventures'

    embed = discord.Embed(
        color = global_data.color,
        title = f'PET SKILLS',
        description =   f'Overview of all pet skills. See `{prefix}pets` on how to get skills.\n'\
                        f'Note: Purple and yellow skills are rarer than blue ones.'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'NORMIE {emojis.skillnormie}', value=normie, inline=False)
    embed.add_field(name=f'FAST {emojis.skillfast}', value=fast, inline=False)
    embed.add_field(name=f'HAPPY {emojis.skillhappy}', value=happy, inline=False)
    embed.add_field(name=f'CLEVER {emojis.skillclever}', value=clever, inline=False)
    embed.add_field(name=f'DIGGER {emojis.skilldigger}', value=digger, inline=False)
    embed.add_field(name=f'LUCKY {emojis.skilllucky}', value=lucky, inline=False)
    embed.add_field(name=f'TIME TRAVELER {emojis.skilltraveler}', value=timetraveler, inline=False)
    embed.add_field(name=f'EPIC {emojis.skillepic}', value=epic, inline=False)
    embed.add_field(name=f'ASCENDED {emojis.skillascended}', value=ascended, inline=False)
    embed.add_field(name=f'SKILL RANKS', value=skillranks, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=guides, inline=False)
            
    return (thumbnail, embed)

# Pet adventures
async def petsadventures(prefix):
          
    usage =         f'{emojis.bp} Command: `pets adv [petID] [type]`\n'\
                    f'{emojis.bp} You can only send one pet unless it has the {emojis.skillepic} EPIC skill'

    types =         f'{emojis.bp} **Dig**: Pet is more likely to find items\n'\
                    f'{emojis.bp} **Drill**: Pet is more likely to find coins\n'\
                    f'{emojis.bp} **Learn**: Pet is more likely to rank up a skill\n'\
                    f'{emojis.bp} The type does **not** guarantee the outcome \n'\
                    f'{emojis.bp} Your pet will never come back emptyhanded'

    rewards =       f'{emojis.bp} **Items**: {emojis.log}{emojis.logepic}{emojis.logsuper}{emojis.logmega}{emojis.loghyper}{emojis.logultra} {emojis.fish}{emojis.fishgolden}{emojis.fishepic}\n'\
                    f'{emojis.bp} **Coins**: ~ 700k+\n'\
                    f'{emojis.bp} **Skill rank**: +1 rank of 1 random skill\n'\
                    f'{emojis.bp} **Pet**: Random T1-3 pet (only if pet has {emojis.skillascended} ascended skill)\n'\
                    f'{emojis.bp} Note: You get a pet **in addition** to the other reward'

    skillsimpact =  f'{emojis.bp} {emojis.skillfast} **Fast**: Reduces the time to do adventures\n'\
                    f'{emojis.bp} {emojis.skilldigger} **Digger**: Increases the amount of coins you get\n'\
                    f'{emojis.bp} {emojis.skilllucky} **Lucky**: Increases the chance to find better items\n'\
                    f'{emojis.bp} {emojis.skilltraveler} **Time traveler**: Has a chance of finishing instantly\n'\
                    f'{emojis.bp} {emojis.skillepic} **EPIC**: If you send this pet **first**, you can send another\n'\
                    f'{emojis.bp} {emojis.skillascended} **Ascended**: Has a chance to find a pet'
    
    guides =        f'{emojis.bp} `{prefix}pets` : Pets overview\n'\
                    f'{emojis.bp} `{prefix}petcatch` : How to find and catch pets\n'\
                    f'{emojis.bp} `{prefix}petfusion` : Details about pet fusion\n'\
                    f'{emojis.bp} `{prefix}petskills` : Details about pet skills'

    embed = discord.Embed(
        color = global_data.color,
        title = f'PET ADVENTURES',
        description =   f'You can send pets on adventures to find items or coins or to rank up their skills.'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    thumbnail = discord.File(global_data.thumbnail, filename='thumbnail.png')
    embed.set_thumbnail(url='attachment://thumbnail.png')

    embed.add_field(name=f'HOW TO SEND PETS', value=usage, inline=False)
    embed.add_field(name=f'ADVENTURE TYPES', value=types, inline=False)
    embed.add_field(name=f'POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name=f'SKILLS THAT AFFECT ADVENTURES', value=skillsimpact, inline=False)
    embed.add_field(name=f'ADDITIONAL GUIDES', value=guides, inline=False)
            
    return (thumbnail, embed)