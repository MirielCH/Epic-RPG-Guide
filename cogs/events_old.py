# events.py

import discord
from discord.ext import commands

from resources import emojis
from resources import settings
from resources import functions


# events commands (cog)
class eventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    events_aliases = (
        'event','events',
        'zombiehorde','horde',
        'enchantevent',
        'epicguard','guard','jail',
        'heal','healevent',
        'arena','arenaevent',
        'coinrain','rain','cointrumpet','trumpet','catch','catchevent',
        'epictree','tree','epicseed','chop','chopevent',
        'god','godevent',
        'boss','legendary','legendaryboss','bossevent','legendarybossevent',
        'megalodon','fish','fishevent','megalodonevent',
        'miniboss','minibossevent',
        'specialtrade','tradeevent','specialtradeevent',
        'bigarena','arenabig','bigarenaevent',
        'lottery','ticket','lotteryticket',
        'notsominiboss','notsominibossevent','notsomini','minintboss','minint'
        'race','racing','hrace','horserace','horseracing',
        'lootbox','lootboxevent','lb','lbevent',
        'tournament','pettournament','petstournament','pet-tournament','pets-tournament',
        'lootboxsummoning','lootbox-summoning','summoning','lbsummoning','lb-summoning','lb-summon','lbsummon','lootbox-summon','lootboxsummon','summon',
        'ruby','rubydragon','working','work','nothing',
        'failedseed','farmevent',
        'returning','ret',
        'bunny','bunnyboss',
    )

    # Command "events"
    @commands.command(aliases=events_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def events_overview(self, ctx, *args):
        invoked = ctx.invoked_with
        invoked = invoked.lower()

        if invoked.find('enchant') > -1:
            embed = await embed_event_enchant(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('guard') > -1) or (invoked.find('jail') > -1):
            embed = await embed_event_epicguard(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('heal') > -1):
            embed = await embed_event_heal(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif invoked in ('arena','arenaevent'):
            embed = await embed_event_arena(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('rain') > -1) or (invoked.find('trumpet') > -1) or (invoked.find('catch') > -1):
            embed = await embed_event_coinrain(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('tree') > -1) or (invoked.find('epicseed') > -1) or (invoked.find('chop') > -1):
            embed = await embed_event_epictree(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif invoked.find('god') > -1:
            embed = await embed_event_god(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked in ('boss','bossevent')) or (invoked.find('legendary') > -1):
            embed = await embed_event_legendary(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('megalodon') > -1) or (invoked.find('fish') > -1):
            embed = await embed_event_megalodon(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif invoked in ('miniboss','minibossevent'):
            embed = await embed_event_miniboss(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('trade') > -1):
            embed = await embed_event_specialtrade(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('bigarena') > -1) or (invoked.find('arenabig') > -1):
            embed = await embed_event_bigarena(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('race') > -1) or (invoked.find('racing') > -1):
            embed = await embed_event_horserace(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('lottery') > -1) or (invoked.find('ticket') > -1):
            embed = await embed_event_lottery(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('notsomini') > -1) or (invoked.find('minint') > -1):
            embed = await embed_event_notsominiboss(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('lootbox') > -1) or (invoked.find('lb') > -1):
            if (invoked.find('summon') > -1):
                embed = await embed_event_lootboxsummoning(ctx.prefix)
                await ctx.send(embed=embed)
                return
            else:
                embed = await embed_event_lootbox(ctx.prefix)
                await ctx.send(embed=embed)
                return
        elif (invoked.find('pet') > -1) or (invoked.find('tournament') > -1):
            embed = await embed_event_pettournament(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('summon') > -1):
            embed = await embed_event_lootboxsummoning(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('horde') > -1):
            embed = await embed_event_hunt(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('ruby') > -1) or (invoked.find('work') > -1):
            embed = await embed_event_rubydragon(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('failedseed') > -1) or (invoked.find('farm') > -1):
            embed = await embed_event_farm(ctx.prefix)
            await ctx.send(embed=embed)
            return
        elif (invoked.find('ret') > -1):
            embed = await embed_event_returning(ctx.prefix)
            await ctx.send(embed=embed)
            return
        else:
            if args:
                event_name = ''
                for arg in args:
                    event_name = f'{event_name}{arg}'
                event_name = event_name.lower().replace(' ','').strip()
                if event_name.find('enchant') > -1:
                    embed = await embed_event_enchant(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('guard') > -1) or (event_name.find('jail') > -1):
                    embed = await embed_event_epicguard(ctx.prefix)
                    await ctx.send(embed=embed)
                elif event_name.find('god') > -1:
                    embed = await embed_event_god(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('heal') > -1) or (event_name.find('mysterious') > -1) or (event_name.find('potion') > -1):
                    embed = await embed_event_heal(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('legendary') > -1) or (event_name == 'boss'):
                    embed = await embed_event_legendary(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('hunt') > -1) or (event_name.find('zombie') > -1) or (event_name.find('horde') > -1):
                    embed = await embed_event_hunt(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('lootbox') > -1) or (event_name == 'lb'):
                    if (event_name.find('summon') > -1):
                        embed = await embed_event_lootboxsummoning(ctx.prefix)
                        await ctx.send(embed=embed)
                    else:
                        embed = await embed_event_lootbox(ctx.prefix)
                        await ctx.send(embed=embed)
                elif event_name == 'arena':
                    embed = await embed_event_arena(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('coin') > -1) or (event_name.find('rain') > -1) or (event_name.find('trumpet') > -1) or (event_name.find('catch') > -1):
                    embed = await embed_event_coinrain(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('tree') > -1) or (event_name.find('epicseed') > -1) or (event_name.find('chop') > -1):
                    embed = await embed_event_epictree(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('megalodon') > -1) or (event_name.find('ultrabait') > -1) or (event_name.find('fish') > -1):
                    embed = await embed_event_megalodon(ctx.prefix)
                    await ctx.send(embed=embed)
                elif event_name == 'miniboss':
                    embed = await embed_event_miniboss(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('specialtrade') > -1) or (event_name.find('trade') > -1):
                    embed = await embed_event_specialtrade(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('bigarena') > -1):
                    embed = await embed_event_bigarena(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('horserace') > -1) or (event_name.find('race') > -1):
                    embed = await embed_event_horserace(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('lottery') > -1) or (event_name.find('ticket') > -1):
                    embed = await embed_event_lottery(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('notsomini') > -1) or (event_name.find('minint') > -1):
                    embed = await embed_event_notsominiboss(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('pet') > -1) or (event_name.find('tournament') > -1):
                    embed = await embed_event_pettournament(ctx.prefix)
                    await ctx.send(embed=embed)
                elif event_name.find('summon') > -1:
                    embed = await embed_event_lootboxsummoning(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('ruby') > -1) or (event_name.find('work') > -1):
                    embed = await embed_event_rubydragon(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('failed') > -1) or (event_name.find('farm') > -1) or (event_name.find('seed') > -1):
                    embed = await embed_event_farm(ctx.prefix)
                    await ctx.send(embed=embed)
                elif (event_name.find('ret') > -1):
                    embed = await embed_event_returning(ctx.prefix)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'I can\'t find any event with that name\nUse `{ctx.prefix}events` to see a list of all events.')
            else:
                embed = await embed_events_overview(ctx.prefix)
                await ctx.send(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(eventsCog(bot))


# --- Redundancies ---
# Sentences
events_horse = 'A {emoji} T4+ horse will **not** save you if you die in an event'
events_personal = 'Only you can answer'
events_multiplayer = 'Anyone can join'
events_player_no = 'This is a {no} player event'
events_rare = 'This event is very rare'
events_first_one = 'Only the first one to answer gets the reward'
events_once_cycle = 'You can only join once per cycle'
events_official_server = 'The outcome is announced in the [official server](https://discord.gg/epicrpg)'

# Footer
events_footer = 'Use {prefix}events to see a list of all events.'


# --- Embeds: Overview ---
# Events overview
async def embed_events_overview(prefix):

    seasonal_event = (
        f'{emojis.BP} `bunny`\n'
        f'{emojis.BP} `bunny boss`\n'
    )

    sp_events = (
        f'{emojis.BP} `enchant`\n'
        f'{emojis.BP} `failed seed` / `farm`\n'
        f'{emojis.BP} `epic guard`\n'
        f'{emojis.BP} `heal`\n'
        f'{emojis.BP} `lootbox`\n'
        f'{emojis.BP} `returning`\n'
        f'{emojis.BP} `ruby dragon` / `work`\n'
        f'{emojis.BP} `zombie horde` / `hunt`'
    )

    mp_events = (
        f'{emojis.BP} `arena`\n'
        f'{emojis.BP} `coin rain` / `catch`\n'
        f'{emojis.BP} `epic tree` / `chop`\n'
        f'{emojis.BP} `god`\n'
        f'{emojis.BP} `legendary boss`\n'
        f'{emojis.BP} `lootbox summoning` / `summon`\n'
        f'{emojis.BP} `megalodon` / `fish`\n'
        f'{emojis.BP} `miniboss`\n'
        f'{emojis.BP} `special trade`'
    )

    global_events = (
        f'{emojis.BP} `big arena`\n'
        f'{emojis.BP} `horse race`\n'
        f'{emojis.BP} `lottery`\n'
        f'{emojis.BP} `minintboss`\n'
        f'{emojis.BP} `pet tournament`\n'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EVENTS',
        description = (
            f'This page lists the names of all possible events.\n'
            f'Use `{prefix}event [name]` to see details about an event.'
        )
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    #embed.add_field(name=f'EASTER {emojis.EASTER_EGG}', value=seasonal_event, inline=False)
    embed.add_field(name='PERSONAL', value=sp_events, inline=True)
    embed.add_field(name='MULTIPLAYER', value=mp_events, inline=True)
    embed.add_field(name='GLOBAL', value=global_events, inline=True)

    return embed

# --- Embeds: Personal Events ---
# Enchant event
async def embed_event_enchant(prefix):

    trigger = f'{emojis.BP} `enchant`, `refine`, `transmute`, `transcend` (0.085 % chance)'

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
        description = 'This is a random personal event in which you accidentally "break" your equipment while enchanting it.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='SAFEST ANSWER', value=safe_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Epic Guard event
async def embed_event_epicguard(prefix):

    trigger = f'{emojis.BP} Most commands that have a cooldown, with the exception of multiplayer commands like `arena`, `duel`, `horse breed` or `miniboss` (chance unknown)'

    answers = (
        f'{emojis.BP} The name of the random item the guard shows you\n'
        f'{emojis.BP} Tip: You can use `fish` instead of `normie fish`\n'
        f'{emojis.BP} Tip: You can use `potion` instead of `life potion`\n'
        f'{emojis.BP} Tip: You can use `wolf` instead of `wolf skin`'
    )

    jail = (
        f'{emojis.BP} If you answer wrong, you will be put in jail\n'
        f'{emojis.BP} Use `rpg jail` and then `protest`\n'
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

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='REQUIRED ANSWER', value=answers, inline=False)
    embed.add_field(name='HOW TO GET OUT OF JAIL', value=jail, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Failed seed event
async def embed_event_farm(prefix):

    trigger = f'{emojis.BP} `farm` (chance unknown)'

    answers = (
        f'{emojis.BP} `cry`: You get 1 crop and your seed back.\n'
        f'{emojis.BP} `plant another`: You get your seed back.\n'
        f'{emojis.BP} `fight`: Small chance to get 20 levels and your seed back, high chance to only get your seed back.'
    )

    rec_answer = f'{emojis.BP} `fight`'

    note = (
        f'{emojis.BP} This event is only available in {emojis.TIME_TRAVEL}TT 2+\n'
        f'{emojis.BP} {events_personal}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'FAILED SEED EVENT',
        description = 'This is a random personal event in which your planted seed won\'t grow as expected.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='RECOMMENDED ANSWER', value=rec_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Heal event
async def embed_event_heal(prefix):

    trigger = f'{emojis.BP} `heal` (0.75 % chance)'

    answers = (
        f'{emojis.BP} `cry`: The event ends, nothing happens\n'
        f'{emojis.BP} `search`: Leads to the option to `fight` the thief. If you do this, you will either gain **or lose** a level'
    )

    safe_answer = f'{emojis.BP} `cry`'

    note = (
        f'{emojis.BP} This event will not trigger if you are at full LIFE before healing\n'
        f'{emojis.BP} {events_personal}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HEAL EVENT',
        description = 'This is a random personal event in which you encounter a mysterious man while healing yourself.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='SAFEST ANSWER', value=safe_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Lootbox event
async def embed_event_lootbox(prefix):

    trigger = f'{emojis.BP} `open` (chance unknown)'

    answers = (
        f'{emojis.BP} `cry`: You get a {emojis.LB_EPIC} EPIC, {emojis.LB_RARE} rare or {emojis.LB_UNCOMMON} uncommon lootbox\n'
        f'{emojis.BP} `fight`: You destroy the lootbox and get 400 lootboxer XP\n'
        f'{emojis.BP} `magic spell`: Low chance to get an {emojis.LB_OMEGA} OMEGA lootbox, high chance to get nothing'
    )

    rec_answer = (
        f'{emojis.BP} `fight` if lootboxer < 100\n'
        f'{emojis.BP} `magic spell` if lootboxer 100+'
    )

    note = f'{emojis.BP} {events_personal}'

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LOOTBOX EVENT',
        description = 'This is a rare random personal event in which a lootbox refuses to open.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='RECOMMENDED ANSWER', value=rec_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Ruby dragon event
async def embed_event_rubydragon(prefix):

    trigger = f'{emojis.BP} Work commands (chance unknown)'

    answers = (
        f'{emojis.BP} `cry`: You get 1 {emojis.ARENA_COOKIE} arena cookie\n'
        f'{emojis.BP} `move`: You move to another area and spawn the ruby dragon (see below)\n'
        f'{emojis.BP} `sleep`: The event ends, you get nothing'
    )

    answers_ruby = (
        f'{emojis.BP} `run`: The event ends, you get nothing\n'
        f'{emojis.BP} `fight`: You fight the dragon and get 10 {emojis.RUBY} rubies\n'
        f'{emojis.BP} `sleep`: The dragon leaves and you get 2 {emojis.RUBY} rubies'
    )

    best_answer = (
        f'{emojis.BP} First `move`, then `fight`\n'
    )

    note = (
        f'{emojis.BP} You actually _do_ move to another area, so you have to move back to your previous area after the event\n'
        f'{emojis.BP} This event is not available in the TOP\n'
        f'{emojis.BP} {events_personal}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'THE RUBY DRAGON EVENT',
        description = 'This is a random personal event in which you don\'t find any materials when working... but a ruby dragon instead.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS (START)', value=answers, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS (RUBY DRAGON)', value=answers_ruby, inline=False)
    embed.add_field(name='BEST ANSWERS', value=best_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed



# --- Embeds: Multiplayer events ---
# Arena event
async def embed_event_arena(prefix):

    trigger = (
        f'{emojis.BP} `arena` to start the event alone\n'
        f'{emojis.BP} `arena @Users` to start the event with up to 9 people for greater rewards\n'
        f'{emojis.BP} You can only mention users if their cooldown is ready\n'
        f'{emojis.BP} This will use up the cooldown of every player mentioned'
    )

    answers = (
        f'{emojis.BP} `yes` or `y` if you got mentioned\n'
        f'{emojis.BP} `join` if you are a participant'
    )

    rewards = (
        f'{emojis.BP} 1 {emojis.ARENA_COOKIE} cookie per kill per initiator\n'
        f'{emojis.BP} Example: You get 3 {emojis.ARENA_COOKIE} cookies per kill if you mention 2 players\n'
        f'{emojis.BP} 3 {emojis.ARENA_COOKIE} cookies extra for the initiator(s) of the arena'
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

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='HOW TO START', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ARENA OR BIG ARENA?', value=whichone, inline=False)

    return embed

# Coin rain event
async def embed_event_coinrain(prefix):

    trigger = (
        f'{emojis.BP} `hunt`, `adventure` and work commands (chance unknown)\n'
        f'{emojis.BP} By using a {emojis.COIN_TRUMPET} coin trumpet from the EPIC shop'
    )

    answers = f'{emojis.BP} `catch`'

    rewards = (
        f'{emojis.BP} {emojis.COIN} coins\n'\
        f'{emojis.BLANK} The amount depends on the level of the player who triggered it, the amount of people that '
        f'participate and some RNG\n'
        f'{emojis.BP} There is a small chance for one player to get lucky\n'
        f'{emojis.BLANK} Getting lucky means getting more {emojis.COIN} coins than the others\n'
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

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Epic tree event
async def embed_event_epictree(prefix):

    trigger = (
        f'{emojis.BP} `hunt`, `adventure` and work commands (chance unknown)\n'
        f'{emojis.BP} By using an {emojis.EPIC_SEED} epic seed from the EPIC shop'
    )

    answers = f'{emojis.BP} `chop`'

    rewards = (
        f'{emojis.BP} {emojis.LOG} wooden logs\n'
        f'{emojis.BLANK} The amount depends on the amount of people that participate and some RNG\n'
        f'{emojis.BP} There is a small chance for one player to get lucky\n'
        f'{emojis.BLANK} Getting lucky means getting more {emojis.LOG} logs than the others\n'
    )

    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=20)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'EPIC TREE EVENT',
        description = 'This is a multiplayer event in which you can chop yourself some logs from a huge tree.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# God event
async def embed_event_god(prefix):

    trigger = f'{emojis.BP} `hunt`, `adventure` and work commands (chance unknown)'

    answers = (
        f'{emojis.BP} The phrase god asks for\n'
        f'{emojis.BP} For a list of all possible phrases see the [Wiki](https://epic-rpg.fandom.com/wiki/Events#God_Events)'
    )

    rewards = (
        f'{emojis.BP} {emojis.COIN} Coins (amount depends on your highest area)\n'
        f'{emojis.BP} {emojis.EPIC_COIN} EPIC coin'
    )

    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_first_one}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'GOD EVENT',
        description = 'This is a random multiplayer event in which god gets clumsy and drops some coins that one player can snatch up.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='REQUIRED ANSWER', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Legendary boss event
async def embed_event_legendary(prefix):

    trigger = f'{emojis.BP} `hunt`, `adventure` and work commands (chance unknown)'

    answers = f'{emojis.BP} `time to fight`'

    rewards = f'{emojis.BP} + 1 level for every participant if successful'

    note = (
        f'{emojis.BP} {events_rare}\n'
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=20)}\n'
        f'{emojis.BP} The chance to beat the boss is very low'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LEGENDARY BOSS EVENT',
        description = 'This is a rare random multiplayer event in which a legendary boss spawns and up to 20 players can defeat it.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Lootbox summoning event
async def embed_event_lootboxsummoning(prefix):

    trigger = f'{emojis.BP} `hunt`, `adventure` and work commands (chance unknown)'

    answers = f'{emojis.BP} `summon`'

    rewards = (
        f'{emojis.BP} A lootbox for every player that entered\n'
        f'{emojis.BLANK} The lootbox tier depends on the amount of players that participate\n'
        f'{emojis.BLANK} The lootbox tier ranges from {emojis.LB_COMMON} common to {emojis.LB_EDGY} EDGY\n'
        f'{emojis.BP} There is a small chance for one player to get lucky\n'
        f'{emojis.BLANK} Getting lucky means getting more rewards than the others\n'
    )

    note = (
        f'{emojis.BP} {events_rare}\n'
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=20)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LOOTBOX SUMMONING EVENT',
        description = 'This is a rare random multiplayer event in which a lootbox gets summoned and up to 20 players can help to do so.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Megalodon event
async def embed_event_megalodon(prefix):

    trigger = (
        f'{emojis.BP} `hunt`, `adventure` and work commands (chance unknown)\n'
        f'{emojis.BP} By using an {emojis.ULTRA_BAIT} ultra bait from the EPIC shop'
    )

    answers = f'{emojis.BP} `fish`'

    rewards = (
        f'{emojis.BP} {emojis.FISH} normie fish\n'
        f'{emojis.BLANK} The amount depends on the amount of people that participate and some RNG\n'
        f'{emojis.BP} There is a small chance for one player to get lucky\n'
        f'{emojis.BLANK} Getting lucky means getting more {emojis.FISH} fish than the others\n'
    )

    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=20)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MEGALODON EVENT',
        description = 'This is a multiplayer event in which a megalodon spawns in the river and up to 20 players can get some fish.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Miniboss event
async def embed_event_miniboss(prefix):

    trigger = (
        f'{emojis.BP} `miniboss` to start the event alone\n'
        f'{emojis.BP} `miniboss @Users` to start the event with up to 9 people for greater rewards\n'
        f'{emojis.BP} You can only mention users if their cooldown is ready\n'
        f'{emojis.BP} This will use up the cooldown of every player mentioned'
    )

    answers = (
        f'{emojis.BP} `yes` or `y` if you got mentioned\n'
        f'{emojis.BP} `fight` if you are a participant'
    )

    rewards = (
        f'{emojis.BP} {emojis.COIN} Coins\n'
        f'{emojis.BP} 2.5% chance for the initiator(s) to get + 1 level\n'
        f'{emojis.BP} The initiator reward depends on the level of the initiator and the users mentioned. It depends most on the original initiator however, thus the player with the highest level should start the event.\n'
        f'{emojis.BP} Participants get 5% of the iniators\' reward, up to 5,000 coins if there is only one initiator. This maximum amount increases with more initiators.'
    )

    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=10)}\n'
        f'{emojis.BP} This event shares its cooldown with `dungeons`\n'
        f'{emojis.BP} This event shares its cooldown with `minintboss`\n'
        f'{emojis.BP} The chance increases by 5% for every participant'
    )

    whichone = (
        f'{emojis.BP} Only do this event if you don\'t need to do a dungeon\n'
        f'{emojis.BP} `minintboss` rewards dragon scales instead of coins'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MINIBOSS EVENT',
        description = 'This is a multiplayer event in which you fight a miniboss to get coins.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='HOW TO START', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='DUNGEON OR MINIBOSS OR MININ\'TBOSS?', value=whichone, inline=False)

    return embed

# Special trade event
async def embed_event_specialtrade(prefix):

    trigger = f'{emojis.BP} `hunt`, `adventure` and work commands (chance unknown)'

    answers = (
        f'{emojis.BP} The phrase the epic NPC asks for\n'
        f'{emojis.BP} Note: You need the items for the trade in your inventory'
    )

    rewards = (
        f'{emojis.BP} 1 {emojis.WOLF_SKIN} wolf skin (for 15 {emojis.LOG} wooden logs)\n'
        f'{emojis.BP} 3 {emojis.EPIC_COIN} EPIC coins (for 3 {emojis.COIN} coins)\n'
        f'{emojis.BP} 3 {emojis.LB_EPIC} EPIC lootboxes (for 5 {emojis.LIFE_POTION} life potions)\n'
        f'{emojis.BP} 40 {emojis.FISH_GOLDEN} golden fish (for 15 {emojis.LIFE_POTION} life potions)\n'
        f'{emojis.BP} 80 {emojis.LOG_EPIC} EPIC logs (for 40 {emojis.LOG} wooden logs)\n'
        f'{emojis.BP} 80 {emojis.FISH} normie fish (for 2 {emojis.ARENA_COOKIE} cookies)\n'
        f'{emojis.BP} 125 {emojis.ARENA_COOKIE} cookies (for 5 {emojis.FISH} normie fish)\n'
    )

    note = (
        f'{emojis.BP} You have time to trade to the required material while the event is active\n'
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_first_one}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'SPECIAL TRADE EVENT',
        description = 'This is a random multiplayer event in which the epic NPC appears and offers one player a (very good) trade.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='REQUIRED ANSWER', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed



# --- Embeds: Global Events ---
# Big arena event
async def embed_event_bigarena(prefix):

    schedule = f'{emojis.BP} Monday, Wednesday, Friday at 18:00 UTC'

    answers = f'{emojis.BP} `big arena join` (unlocked in area 7)'

    rewards = (
        f'{emojis.BP} ~1000+ {emojis.ARENA_COOKIE} arena cookies for the winner\n'
        f'{emojis.BP} ~200+ {emojis.ARENA_COOKIE} arena cookies for second and third place\n'
        f'{emojis.BP} ~30+ {emojis.ARENA_COOKIE} arena cookies for everyone else'
    )

    note = (
        f'{emojis.BP} {events_official_server}\n'
        f'{emojis.BP} {events_once_cycle}\n'
        f'{emojis.BP} This event shares its cooldown with `arena`'
    )

    whichone = f'{emojis.BP} `big arena` has higher rewards than unboosted `arena`'

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'BIG ARENA EVENT',
        description = 'This is a global event which takes place three times a week.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='ARENA OR BIG ARENA?', value=whichone, inline=False)

    return embed

# Horse race event
async def embed_event_horserace(prefix):

    schedule = f'{emojis.BP} Every even hour (= every 2 hours)'

    answers = f'{emojis.BP} `horse race` (unlocked with a {emojis.HORSE_T5} T5+ horse)'

    rewards = (
        f'{emojis.BP} T1 - T8: A random lootbox, +1 horse level or +1 horse tier\n'
        f'{emojis.BP} T9: A random lootbox, a pet (up to T3), +1 horse level or +1 horse tier\n'
        f'{emojis.BP} T10: Up to 3 lootboxes or a pet (up to T5)\n'
        f'{emojis.BP} You **only** get rewards if you place third or higher'
    )

    note = (
        f'{emojis.BP} {events_official_server}\n'
        f'{emojis.BP} {events_once_cycle}\n'
        f'{emojis.BP} This event shares its cooldown with `horse breeding`\n'
        f'{emojis.BP} Your chance to win is heavily influenced by your horse\'s level'
    )

    whichone = f'{emojis.BP} Unless your horse is {emojis.HORSE_T10} T10, breed instead'

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HORSE RACE EVENT',
        description = 'This is a global event which takes place every 2 hours.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='RACE OR BREED?', value=whichone, inline=False)

    return embed

# Pet tournament event
async def embed_event_pettournament(prefix):

    schedule = f'{emojis.BP} Every 12 hours at 08:00 / 20:00 UTC'

    answers = f'{emojis.BP} `pets tournament [ID]`'

    rewards = (
        f'{emojis.BP} + 1 pet tier\n'
        f'{emojis.BP} You only get the reward if you **win** the tournament'
    )

    note = (
        f'{emojis.BP} {events_official_server}\n'
        f'{emojis.BP} {events_once_cycle}\n'
        f'{emojis.BP} You can only enter **1** pet per cycle\n'
        f'{emojis.BP} You can apply with any pet, even pets on adventures\n'
        f'{emojis.BP} Your chance to win is influenced by your pet\'s score (see `{prefix}pet`)\n'
        f'{emojis.BP} The tournament will not happen if there are less than 50 pets'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'PET TOURNAMENT EVENT',
        description = 'This is a global event which takes place every 12 hours.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Lottery event
async def embed_event_lottery(prefix):

    schedule = f'{emojis.BP} Every 12 hours at 00:00 / 12:00 UTC'

    answers = f'{emojis.BP} `buy lottery ticket [1-10]`'

    rewards = (
        f'{emojis.BP} A huge amount of {emojis.COIN} coins if you win\n'
        f'{emojis.BP} Absolutely nothing if you don\'t'
    )

    note =(
        f'{emojis.BP} {events_official_server}\n'
        f'{emojis.BP} You can buy up to 10 lottery tickets for each draw\n'
        f'{emojis.BP} The size of the pot depends on ticket prices and tickets sold\n'
        f'{emojis.BP} The ticket prices are different with every lottery'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LOTTERY EVENT',
        description = 'This is a global event which takes place every 12 hours.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# minintboss event
async def embed_event_notsominiboss(prefix):

    schedule = f'{emojis.BP} Tuesday, Thursday, Saturday at 18:00 UTC'

    answers = f'{emojis.BP} `minintboss join` (unlocked in area 10)'

    rewards = f'{emojis.BP} 2-4 {emojis.DRAGON_SCALE} dragon scales **if** the boss dies'

    note = (
        f'{emojis.BP} {events_official_server}\n'
        f'{emojis.BP} {events_once_cycle}\n'
        f'{emojis.BP} This event shares its cooldown with `miniboss` and `dungeon`\n'
        f'{emojis.BP} This event has a 20% chance to fail'
    )

    whichone = (
        f'{emojis.BP} Only do this event if you don\'t need to do a dungeon\n'
        f'{emojis.BP} `miniboss` rewards coins instead of dragon scales'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MININ\'TBOSS EVENT',
        description = 'This is a global event which takes place three times a week.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='DUNGEON OR MINIBOSS OR MININ\'TBOSS?', value=whichone, inline=False)

    return embed


async def embed_event_hunt(prefix):
    """Hunt event embed"""
    trigger = f'{emojis.BP} `hunt` in areas 3+ (chance unknown)'

    answers = (
        f'{emojis.BP} `cry`: The zombie horde walks away, you get nothing\n'
        f'{emojis.BP} `fight`: Small chance to get 1 coin and _almost_ one level, high chance to get nothing\n'
        f'{emojis.BP} `join`: You move to area 2 with the horde and get 5-7 {emojis.ZOMBIE_EYE} zombie eyes'
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
        title = 'ZOMBIE HORDE EVENT',
        description = 'This is a rare random personal event in which you encounter a zombie horde.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='RECOMMENDED ANSWER', value=rec_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed


# --- Embeds: Seasonal events ---
# Snowball fight event (xmas)
async def embed_event_snowball(prefix):

    trigger = (
        f'{emojis.BP} Any command (chance unknown)\n'
        f'{emojis.BP} By using a {emojis.XMAS_HAT} christmas hat'
    )

    answers = (
        f'{emojis.BP} `fight`: Low chance to get more loot than `summon`, high chance to get less.\n'
        f'{emojis.BP} `summon`: 50/50 chance to get more or less loot\n'
        f'{emojis.BP} `sleep`: Very low chance to get more loot than `summon` and `fight`, very high chance to get less'
    )

    best_answer = (
        f'{emojis.BP} If you don\'t feel like gambling, `summon` is the safest answer\n'
        f'{emojis.BP} If you _do_ feel like gambling, `sleep` has the highest potential rewards'
    )

    note =(
        f'{emojis.BP} This event gives much higher rewards if it\'s triggered with a {emojis.XMAS_HAT} christmas hat\n'
        f'{emojis.BP} You always get some loot, even if you lose'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'SNOWBALL FIGHT EVENT',
        description =   f'This is a random personal christmas event in which the EPIC NPC starts a snowball fight with you.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='BEST ANSWER', value=best_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Bunny event (easter)
async def embed_event_bunny(prefix):

    trigger = f'{emojis.BP} `hunt`, `adventure` and work commands (chance unknown)' # was 0.75% last year

    answers = (
        f'{emojis.BP} The bunny has a {emojis.PET_HAPPINESS} happiness and :carrot: hunger stat\n'
        f'{emojis.BP} You can enter a line of commands to influence these stats\n'
        f'{emojis.BLANK} `feed` decreases hunger by 18-22\n'
        f'{emojis.BLANK} `pat` increases happiness by 8-12\n'
        f'{emojis.BLANK} Example: `feed feed pat pat pat`\n'
        f'{emojis.BP} If happiness is 85+ higher than hunger, catch chance is 100%\n'
        f'{emojis.BP} You can only use up to 6 commands\n'
        f'{emojis.BP} Less commands = 15 {emojis.EASTER_EGG} easter eggs for every command not used'
    )

    rewards = (
        f'{emojis.BP} {emojis.EASTER_BUNNY} Bunny (used in crafting {emojis.EASTER_SPAWNER} boss spawners)\n'
        f'{emojis.BP} {emojis.PET_GOLDEN_BUNNY} Fake golden bunny. '
        f'Gifts you a {emojis.EASTER_SPAWNER} boss spawner every day.'
    )

    note =(
        f'{emojis.BP} You can increase the chance of this event by crafting'
        f'{emojis.EASTER_RAINBOW_CARROT} rainbow carrots\n'
        f'{emojis.BP} You can craft up to 10 carrots which gives you a 5.25% spawn chance'
        #f'{emojis.BP} You can craft up to 5 carrots which gives you a 3 % spawn chance'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'BUNNY EVENT',
        description = 'This is a random personal easter event in which a bunny appears for you to tame.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='HOW TO TAME THE BUNNY', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Bunny boss event (easter)
async def embed_event_bunnyboss(prefix):

    trigger = (
        f'{emojis.BP} Craft a {emojis.EASTER_SPAWNER} boss spawner\n'
        f'{emojis.BP} Use `egg use boss spawner` or `egg buy instant spawn`\n'
        f'{emojis.BLANK} If you don\'t buy an instant spawn, this will use your dungeon cooldown'
    )

    answers = (
        f'{emojis.BP} `fight` or `defend`\n'
        f'{emojis.BP} Look at the boss stats to decide what to choose'
    )

    rewards = (
        f'{emojis.BP} 1-2 {emojis.EASTER_EGG_GOLDEN} golden eggs\n'
        f'{emojis.BP} {emojis.EASTER_EGG} Easter eggs\n'
        f'{emojis.BP} {emojis.ARENA_COOKIE} Arena cookies\n'
        f'{emojis.BP} {emojis.EPIC_COIN} EPIC coins\n'
        f'{emojis.BP} {emojis.EASTER_LOOTBOX} Easter lootboxes\n'
        f'{emojis.BP} The participants have a chance to get a few {emojis.EASTER_EGG} easter eggs '
        f'and {emojis.ARENA_COOKIE} cookies'
    )

    note = (
        f'{emojis.BP} {events_multiplayer}\n'
        f'{emojis.BP} {events_player_no.format(no=15)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'BUNNY BOSS EVENT',
        description = 'This is a multiplayer easter event in which you fight a bunny boss.'
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='HOW TO START', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Bat slime event (halloween)
async def embed_event_slime(prefix):

    trigger = (
        f'{emojis.BP} By crafting a {emojis.HAL_CANDY_BAIT} candy bait'
    )

    answers = (
        f'{emojis.BP} `fight`: Get 3-6 {emojis.HAL_SPOOKY_ORB} spooky orbs\n'
        f'{emojis.BP} `boo`: Get 2-8 {emojis.HAL_SPOOKY_ORB} spooky orbs'
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
        title = 'BAT SLIME EVENT',
        description = (
            f'This is a random personal halloween event in which you spawn three {emojis.HAL_BAT_SLIME} bat slimes.'
        )
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='BEST ANSWER', value=best_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)

    return embed

# Scroll boss event (halloween)
async def embed_event_scroll_boss(prefix):

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
        f'{emojis.BP} 200 {emojis.HAL_PUMPKIN} pumpkins\n'
        f'{emojis.BP} 100 {emojis.ARENA_COOKIE} arena cookies\n'
        f'{emojis.BP} 2 {emojis.LB_EDGY} EDGY lootboxes\n'
    )

    rewards_lose = (
        f'{emojis.BP} 150 {emojis.HAL_PUMPKIN} pumpkins\n'
        f'{emojis.BP} 80 {emojis.ARENA_COOKIE} arena cookies\n'
        f'{emojis.BP} 1 {emojis.LB_EDGY} EDGY lootboxes\n'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'PUMPKIN BAT BOSS (SCROLL BOSS) EVENT',
        description = (
            f'This is a personal halloween event in which you spawn a {emojis.HAL_BOSS} pumpkin bat boss.\n'
            f'This boss is also called "scroll boss".\n'
        )
    )

    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='TACTICS', value=tactics, inline=False)
    embed.add_field(name='REWARDS IF YOU WIN', value=rewards_win, inline=False)
    embed.add_field(name='REWARDS IF YOU LOSE', value=rewards_lose, inline=False)

    return embed


async def embed_event_returning(prefix: str) -> discord.Embed:
    """Returning event"""
    activities = (
        f'{emojis.BP} Get {emojis.COIN_SMOL} smol coins in `hunt`, `adventure` and all work commands\n'
        f'{emojis.BP} Complete the event quest to get several rewards (see `rpg ret quest`)\n'
        f'{emojis.BP} Claim a reward from the super-daily every day (see `rpg ret superdaily`)\n'
        f'{emojis.BP} Buy various rewards in the `rpg ret shop`\n'
    )
    bonuses = (
        f'{emojis.BP} All command cooldowns except `vote` and `guild` are reduced by 33%\n'
        f'{emojis.BP} You can enter all dungeons without buying a dungeon key\n'
        f'{emojis.BP} The drop chance of mob drops is doubled (see `{prefix}drops`)\n'
    )
    schedule = (
        f'{emojis.BP} Event starts when you use a command after being inactive for at least 2 months\n'
        f'{emojis.BP} Event ends 7 days after it started\n'
    )
    tldr_guide = (
        f'{emojis.BP} Make sure to use `rpg ret superdaily` every day\n'
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
    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed