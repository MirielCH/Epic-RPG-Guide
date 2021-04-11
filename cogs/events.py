# events.py

import discord
import emojis
import global_data

from discord.ext import commands

# events commands (cog)
class eventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    events_aliases = (
        'event','events',
        'enchantevent',
        'epicguard','guard','jail',
        'heal','healevent',
        'arena','arenaevent',
        'coinrain','rain','cointrumpet','trumpet','catch','catchevent',
        'epictree','tree','epicseed','seed','chop','chopevent',
        'god','godevent',
        'boss','legendary','legendaryboss','bossevent','legendarybossevent',
        'megalodon','fish','fishevent','megalodonevent',
        'miniboss','minibossevent',
        'specialtrade','tradeevent','specialtradeevent',
        'bigarena','arenabig','bigarenaevent',
        'lottery','ticket','lotteryticket',
        'notsominiboss','notsominibossevent','notsomini',
        'race','racing','hrace','horserace','horseracing',
        'lootbox','lootboxevent','lb','lbevent',
        'tournament','pettournament','petstournament','pet-tournament','pets-tournament',
        'lootboxsummoning','lootbox-summoning','summoning','lbsummoning','lb-summoning','lb-summon','lbsummon','lootbox-summon','lootboxsummon','summon',
        'ruby','rubydragon','working','work','nothing',
        'bunny','bunnyevent','bunnyboss','bunnybossevent'
    )
    
    # Command "events"
    @commands.command(aliases=events_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def events_overview(self, ctx, *args):
        invoked = ctx.invoked_with
        invoked = invoked.lower()

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
                if (invoked.find('bunny') > -1):
                    embed = await embed_event_bunnyboss(ctx.prefix)
                    await ctx.send(embed=embed)
                else:
                    embed = await embed_event_legendary(ctx.prefix)
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
            elif (event_name.find('tree') > -1) or (event_name.find('seed') > -1) or (event_name.find('chop') > -1):
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
            elif (event_name.find('notsomini') > -1):
                embed = await embed_event_notsominiboss(ctx.prefix)
                await ctx.send(embed=embed)
            elif (event_name.find('pet') > -1) or (event_name.find('tournament') > -1):
                embed = await embed_event_pettournamnent(ctx.prefix)
                await ctx.send(embed=embed)
            elif event_name.find('summon') > -1:
                embed = await embed_event_lootboxsummoning(ctx.prefix)
                await ctx.send(embed=embed)
            elif (event_name.find('ruby') > -1) or (event_name.find('work') > -1):
                embed = await embed_event_rubydragon(ctx.prefix)
                await ctx.send(embed=embed)
            elif (event_name.find('bunnyboss') > -1):
                embed = await embed_event_bunnyboss(ctx.prefix)
                await ctx.send(embed=embed)
            elif (event_name.find('bunny') > -1):
                embed = await embed_event_bunny(ctx.prefix)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'I can\'t find any event with that name\nUse `{ctx.prefix}events` to see a list of all events.')          
        else:
            if invoked.find('enchant') > -1:
                embed = await embed_event_enchant(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('guard') > -1) or (invoked.find('jail') > -1):
                embed = await embed_event_epicguard(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('heal') > -1):
                embed = await embed_event_heal(ctx.prefix)
                await ctx.send(embed=embed)
            elif invoked in ('arena','arenaevent'):
                embed = await embed_event_arena(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('rain') > -1) or (invoked.find('trumpet') > -1) or (invoked.find('catch') > -1):
                embed = await embed_event_coinrain(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('tree') > -1) or (invoked.find('seed') > -1) or (invoked.find('chop') > -1):
                embed = await embed_event_epictree(ctx.prefix)
                await ctx.send(embed=embed)
            elif invoked.find('god') > -1:
                embed = await embed_event_god(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked in ('boss','bossevent')) or (invoked.find('legendary') > -1):
                embed = await embed_event_legendary(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('megalodon') > -1) or (invoked.find('fish') > -1):
                embed = await embed_event_megalodon(ctx.prefix)
                await ctx.send(embed=embed)
            elif invoked in ('miniboss','minibossevent'):
                embed = await embed_event_miniboss(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('trade') > -1):
                embed = await embed_event_specialtrade(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('bigarena') > -1) or (invoked.find('arenabig') > -1):
                embed = await embed_event_bigarena(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('race') > -1) or (invoked.find('racing') > -1):
                embed = await embed_event_horserace(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('lottery') > -1) or (invoked.find('ticket') > -1):
                embed = await embed_event_lottery(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('notsomini') > -1):
                embed = await embed_event_notsominiboss(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('lootbox') > -1) or (invoked.find('lb') > -1):
                if (invoked.find('summon') > -1):
                    embed = await embed_event_lootboxsummoning(ctx.prefix)
                    await ctx.send(embed=embed)
                else:
                    embed = await embed_event_lootbox(ctx.prefix)
                    await ctx.send(embed=embed)
            elif (invoked.find('pet') > -1) or (invoked.find('tournament') > -1):
                embed = await embed_event_pettournamnent(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('summon') > -1):
                embed = await embed_event_lootboxsummoning(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('ruby') > -1) or (invoked.find('work') > -1):
                embed = await embed_event_rubydragon(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('bunnyboss') > -1):
                embed = await embed_event_bunnyboss(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('bunny') > -1):
                embed = await embed_event_bunny(ctx.prefix)
                await ctx.send(embed=embed)
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
    
    easter_event = (
        f'{emojis.bp} `bunny`\n'
        f'{emojis.bp} `bunny boss`'
    )
    
    sp_events = (
        f'{emojis.bp} `enchant`\n'
        f'{emojis.bp} `epic guard`\n'
        f'{emojis.bp} `heal`\n'
        f'{emojis.bp} `lootbox`\n'
        f'{emojis.bp} `ruby dragon`'
    )
    
    mp_events = (
        f'{emojis.bp} `arena`\n'
        f'{emojis.bp} `coin rain`\n'
        f'{emojis.bp} `epic tree`\n'
        f'{emojis.bp} `god`\n'
        f'{emojis.bp} `legendary boss`\n'
        f'{emojis.bp} `lootbox summoning`\n'
        f'{emojis.bp} `megalodon`\n'
        f'{emojis.bp} `miniboss`\n'
        f'{emojis.bp} `special trade`'
    )
                    
    global_events = (
        f'{emojis.bp} `big arena`\n'
        f'{emojis.bp} `horse race`\n'
        f'{emojis.bp} `lottery`\n'
        f'{emojis.bp} `not so mini boss`\n'
        f'{emojis.bp} `pet tournament`\n'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'EVENTS',
        description = (
            f'This page lists the names of all possible events.\n'
            f'Use `{prefix}event [name]` to see details about an event.'
        )
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'EASTER {emojis.easteregg}', value=easter_event, inline=False)
    embed.add_field(name='PERSONAL', value=sp_events, inline=True)
    embed.add_field(name='MULTIPLAYER', value=mp_events, inline=True)
    embed.add_field(name='GLOBAL', value=global_events, inline=True)
            
    return embed

# --- Embeds: Personal Events ---
# Enchant event
async def embed_event_enchant(prefix):

    trigger = f'{emojis.bp} `enchant`, `refine`, `transmute`, `transcend` (0.085 % chance)'
    
    answers = (
        f'{emojis.bp} `cry`: Nothing happens but you won\'t get an enchant\n'
        f'{emojis.bp} `fix`: You get an enchant and either gain **or lose** 5 LIFE\n'
        f'{emojis.bp} `again`: Small chance to get an ULTRA-EDGY enchant, high chance to die'
    )
        
    safe_answer = f'{emojis.bp} `cry`'
                    
    note = (
        f'{emojis.bp} {events_horse.format(emoji=emojis.horset4)}\n'
        f'{emojis.bp} Your gear doesn\'t break despite the event indicating this\n'
        f'{emojis.bp} {events_personal}'
    )

    embed = discord.Embed(
        color = global_data.color,
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

    trigger = f'{emojis.bp} `hunt`, `adventure` and work commands (chance unknown)'
    
    answers = (
        f'{emojis.bp} The name of the random item the guard shows you\n'
        f'{emojis.bp} Tip: You can use `fish` instead of `normie fish`\n'
        f'{emojis.bp} Tip: You can use `potion` instead of `life potion`\n'
        f'{emojis.bp} Tip: You can use `wolf` instead of `wolf skin`'
    )
    
    jail = (
        f'{emojis.bp} If you answer wrong, you will be put in jail\n'
        f'{emojis.bp} Use `rpg jail` and then `protest`\n'
        f'{emojis.bp} Do **not** try to kill the guard, there is a high chance to die'
    )
                    
    note = (
        f'{emojis.bp} {events_horse.format(emoji=emojis.horset4)}\n'
        f'{emojis.bp} You get some coins if you answer the question correctly\n'
        f'{emojis.bp} {events_personal}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'EPIC GUARD EVENT',
        description = 'This is a random captcha event to prevent autotyping.'
    )    
    
    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='REQUIRED ANSWER', value=answers, inline=False)
    embed.add_field(name='HOW TO GET OUT OF JAIL', value=jail, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
            
    return embed

# Heal event
async def embed_event_heal(prefix):

    trigger = f'{emojis.bp} `heal` (0.75 % chance)'
    
    answers = (
        f'{emojis.bp} `cry`: The event ends, nothing happens\n'
        f'{emojis.bp} `search`: Leads to the option to `fight` the thief. If you do this, you will either gain **or lose** a level'
    )
    
    safe_answer = f'{emojis.bp} `cry`'
                    
    note = (
        f'{emojis.bp} This event will not trigger if you are at full LIFE before healing\n'
        f'{emojis.bp} {events_personal}'
    )

    embed = discord.Embed(
        color = global_data.color,
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

    trigger = f'{emojis.bp} `open` (0.5 % chance)'
    
    answers = (
        f'{emojis.bp} `cry`: You get a {emojis.lbepic} EPIC, {emojis.lbrare} rare or {emojis.lbuncommon} uncommon lootbox\n'
        f'{emojis.bp} `fight`: You destroy the lootbox and get 400 lootboxer XP\n'
        f'{emojis.bp} `magic spell`: Low chance to get an {emojis.lbomega} OMEGA lootbox, high chance to get nothing'
    )
    
    rec_answer = (
        f'{emojis.bp} `fight` if lootboxer < 100\n'
        f'{emojis.bp} `magic spell` if lootboxer is maxed'
    )
                    
    note = f'{emojis.bp} {events_personal}'

    embed = discord.Embed(
        color = global_data.color,
        title = 'LOOTBOX EVENT',
        description = 'This is a rare random personal event in which a lootboxes refuses to open.'
    )    
    
    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='POSSIBLE ANSWERS & REWARDS', value=answers, inline=False)
    embed.add_field(name='RECOMMENDED ANSWER', value=rec_answer, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
            
    return embed

# Ruby dragon event
async def embed_event_rubydragon(prefix):

    trigger = f'{emojis.bp} Work commands (chance unknown)'
    
    answers = (
        f'{emojis.bp} `cry`: You get 1 {emojis.arenacookie} arena cookie\n'
        f'{emojis.bp} `move`: You move to another area and spawn the ruby dragon (see below)\n'
        f'{emojis.bp} `sleep`: You get whatever materials you were about to get'
    )

    answers_ruby = (
        f'{emojis.bp} `run`: The event ends, you get nothing\n'
        f'{emojis.bp} `fight`: You fight the dragon and get 10 {emojis.ruby} rubies if you win\n'
        f'{emojis.bp} `sleep`: The dragon leaves and you get 2 {emojis.ruby} rubies'
    )

    best_answer = (
        f'{emojis.bp} First `move`, then `fight`. The chance to win is very high or even 100%\n'
        f'{emojis.bp} If you want the original materials instead, use `sleep` right away'
    )
    
    note = (
        f'{emojis.bp} You actually _do_ move to another area, so you have to move back to your previous area after the event\n'
        f'{emojis.bp} {events_personal}'
    )
        
    embed = discord.Embed(
        color = global_data.color,
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
        f'{emojis.bp} `arena` or `arena @Users`\n'
        f'{emojis.bp} You can only mention users if their cooldown is ready\n'
        f'{emojis.bp} This will use up the cooldown of every player mentioned'
    )
    
    answers = f'{emojis.bp} `join`'
    
    rewards = (
        f'{emojis.bp} 1 {emojis.arenacookie} cookie per kill per initiator\n'
        f'{emojis.bp} Example: You get 3 {emojis.arenacookie} cookies per kill if you mention 2 players\n'
        f'{emojis.bp} 3 {emojis.arenacookie} cookies extra for the initiator(s) of the arena'
    )
    
    note = (
        f'{emojis.bp} {events_multiplayer}\n'
        f'{emojis.bp} {events_player_no.format(no=10)}\n'
        f'{emojis.bp} Requires at least 2 players, otherwise it will cancel\n'
        f'{emojis.bp} The outcome is completely random\n'
        f'{emojis.bp} This event shares its cooldown with `big arena`'
    )
                    
    whichone = f'{emojis.bp} `big arena` has higher rewards than `arena`'

    embed = discord.Embed(
        color = global_data.color,
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
        f'{emojis.bp} `hunt`, `adventure` and work commands (chance unknown)\n'
        f'{emojis.bp} By using a {emojis.cointrumpet} coin trumpet from the EPIC shop'
    )
    
    answers = f'{emojis.bp} `catch`'
    
    rewards = (
        f'{emojis.bp} {emojis.coin} coins\n'\
        f'{emojis.bp} The amount depends on the level of the player who triggered it, the amount of people that participate and some RNG'
    )
                    
    note = (
        f'{emojis.bp} {events_multiplayer}\n'
        f'{emojis.bp} {events_player_no.format(no=20)}'
    )

    embed = discord.Embed(
        color = global_data.color,
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
        f'{emojis.bp} `hunt`, `adventure` and work commands (chance unknown)\n'
        f'{emojis.bp} By using an {emojis.epicseed} epic seed from the EPIC shop'
    )
    
    answers = f'{emojis.bp} `chop`'
    
    rewards = (
        f'{emojis.bp} {emojis.log} wooden logs\n'
        f'{emojis.bp} The amount depends on the level of the player who triggered it, the amount of people that participate and some RNG'
    )
                    
    note = (
        f'{emojis.bp} {events_multiplayer}\n'
        f'{emojis.bp} {events_player_no.format(no=20)}'
    )

    embed = discord.Embed(
        color = global_data.color,
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

    trigger = f'{emojis.bp} `hunt`, `adventure` and work commands (chance unknown)'
    
    answers = (
        f'{emojis.bp} The phrase god asks for\n'
        f'{emojis.bp} For a list of all possible phrases see the [Wiki](https://epic-rpg.fandom.com/wiki/Events#God_Events)'
    )
    
    rewards = (
        f'{emojis.bp} {emojis.coin} Coins (amount depends on your highest area)\n'
        f'{emojis.bp} {emojis.epiccoin} EPIC coin'
    )
                    
    note = (
        f'{emojis.bp} {events_multiplayer}\n'
        f'{emojis.bp} {events_first_one}'
    )

    embed = discord.Embed(
        color = global_data.color,
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

    trigger = f'{emojis.bp} `hunt`, `adventure` and work commands (chance unknown)'
    
    answers = f'{emojis.bp} `time to fight`'
    
    rewards = f'{emojis.bp} + 1 level for every participant if successful'
                    
    note = (
        f'{emojis.bp} {events_rare}\n'
        f'{emojis.bp} {events_multiplayer}\n'
        f'{emojis.bp} {events_player_no.format(no=20)}\n'
        f'{emojis.bp} The chance to beat the boss is very low'
    )

    embed = discord.Embed(
        color = global_data.color,
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

    trigger = f'{emojis.bp} `hunt`, `adventure` and work commands (chance unknown)'
    
    answers = f'{emojis.bp} `summon`'
    
    rewards = (
        f'{emojis.bp} A lootbox for every player that entered\n'
        f'{emojis.bp} The lootbox tier depends on the amount of players that entered\n'
        f'{emojis.bp} The lootbox tier ranges from {emojis.lbcommon} common to {emojis.lbedgy} EDGY'
    )
                    
    note = (
        f'{emojis.bp} {events_rare}\n'
        f'{emojis.bp} {events_multiplayer}\n'
        f'{emojis.bp} {events_player_no.format(no=20)}'
    )

    embed = discord.Embed(
        color = global_data.color,
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
        f'{emojis.bp} `hunt`, `adventure` and work commands (chance unknown)\n'
        f'{emojis.bp} By using an {emojis.ultrabait} ultra bait from the EPIC shop'
    )
    
    answers = f'{emojis.bp} `fish`'
    
    rewards = (
        f'{emojis.bp} {emojis.fish} normie fish\n'
        f'{emojis.bp} The amount depends on the level of the player who triggered it, the amount of people that participate and some RNG'
    )
                    
    note = (
        f'{emojis.bp} {events_multiplayer}\n'
        f'{emojis.bp} {events_player_no.format(no=20)}'
    )

    embed = discord.Embed(
        color = global_data.color,
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
        f'{emojis.bp} `miniboss` or `miniboss @Users`\n'
        f'{emojis.bp} You can only mention users if their cooldown is ready\n'
        f'{emojis.bp} This will use up the cooldown of every player mentioned'
    )
    
    answers = f'{emojis.bp} `fight`'
    
    rewards = (
        f'{emojis.bp} {emojis.coin} Coins\n'
        f'{emojis.bp} Rare chance for the initiator(s) to get + 1 level\n'
        f'{emojis.bp} The initiators reward depends on the level of the initiator and the users mentioned. It depends most on the initiator however, thus the player with the highest level should start the event.\n'
        f'{emojis.bp} The participants get 5 % of the initiators reward, up to 5,000 coins if there is only one initiator. This maximum amount increases with more initiators.\n'
    )
                
    note = (
        f'{emojis.bp} {events_multiplayer}\n'
        f'{emojis.bp} {events_player_no.format(no=10)}\n'
        f'{emojis.bp} This event shares its cooldown with `dungeons`\n'
        f'{emojis.bp} This event shares its cooldown with `not so mini boss`\n'
        f'{emojis.bp} The chance increases by 5 % for every participant'
    )

    whichone = (
        f'{emojis.bp} Only do this event if you don\'t need to do a dungeon\n'
        f'{emojis.bp} `not so mini boss` rewards dragon scales instead of coins'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'MINIBOSS EVENT',
        description = 'This is a multiplayer event in which you fight a miniboss.'
    )    
    
    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='HOW TO START', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='DUNGEON OR MINIBOSS OR NOT SO MINI BOSS?', value=whichone, inline=False)
            
    return embed

# Special trade event
async def embed_event_specialtrade(prefix):

    trigger = f'{emojis.bp} `hunt`, `adventure` and work commands (chance unknown)'
    
    answers = (
        f'{emojis.bp} The phrase the epic NPC asks for\n'
        f'{emojis.bp} Note: You need the items for the trade in your inventory'
    )
    
    rewards = (
        f'{emojis.bp} 1 {emojis.wolfskin} wolf skin (for 15 {emojis.log} wooden logs)\n'
        f'{emojis.bp} 3 {emojis.epiccoin} EPIC coins (for 3 {emojis.coin} coins)\n'
        f'{emojis.bp} 40 {emojis.fishgolden} golden fish (for 15 {emojis.lifepotion} life potions)\n'
        f'{emojis.bp} 80 {emojis.logepic} EPIC logs (for 40 {emojis.log} wooden logs)\n'
        f'{emojis.bp} 80 {emojis.fish} normie fish (for 2 {emojis.arenacookie} cookies)\n'
        f'{emojis.bp} 125 {emojis.arenacookie} cookies (for 5 {emojis.fish} normie fish)'
    )
                    
    note = (
        f'{emojis.bp} You have time to trade to the required material while the event is active\n'
        f'{emojis.bp} {events_multiplayer}\n'
        f'{emojis.bp} {events_first_one}'
    )

    embed = discord.Embed(
        color = global_data.color,
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

    schedule = f'{emojis.bp} Monday, Wednesday, Friday at 18:00 UTC'
    
    answers = f'{emojis.bp} `big arena join` (unlocked in area 7)'
    
    rewards = f'{emojis.bp} {emojis.arenacookie} Arena cookies (usually 30+)'
                    
    note = (
        f'{emojis.bp} {events_official_server}\n'
        f'{emojis.bp} {events_once_cycle}\n'
        f'{emojis.bp} This event shares its cooldown with `arena`'
    )
                    
    whichone = f'{emojis.bp} `big arena` has higher rewards than unboosted `arena`'

    embed = discord.Embed(
        color = global_data.color,
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

    schedule = f'{emojis.bp} Every even hour (= every 2 hours)'
    
    answers = f'{emojis.bp} `horse race` (unlocked with a {emojis.horset5} T5+ horse)'
    
    rewards = (
        f'{emojis.bp} Random lootbox or + 1 horse tier\n'
        f'{emojis.bp} {emojis.horset9} T9 horse only: Chance to get a random pet\n'
        f'{emojis.bp} You **only** get rewards if you place third or higher'
    )
                    
    note = (
        f'{emojis.bp} {events_official_server}\n'
        f'{emojis.bp} {events_once_cycle}\n'
        f'{emojis.bp} This event shares its cooldown with `horse breeding`\n'
        f'{emojis.bp} Your chance to win is heavily influenced by your horse\'s level'
    )
                    
    whichone = f'{emojis.bp} Unless your horse is {emojis.horset9} T9, always breed instead'

    embed = discord.Embed(
        color = global_data.color,
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
async def embed_event_pettournamnent(prefix):

    schedule = f'{emojis.bp} Every 12 hours at 08:00 / 20:00 UTC'
    
    answers = f'{emojis.bp} `pets tournament [ID]`'
    
    rewards = (
        f'{emojis.bp} + 1 pet tier\n'
        f'{emojis.bp} You only get the reward if you **win** the tournament'
    )
                    
    note = (
        f'{emojis.bp} {events_official_server}\n'
        f'{emojis.bp} {events_once_cycle}\n'
        f'{emojis.bp} You can only enter **1** pet per cycle\n'
        f'{emojis.bp} You can apply with any pet, even pets on adventures\n'
        f'{emojis.bp} Your chance to win is influenced by your pet\'s score (see `{prefix}pet`)\n'
        f'{emojis.bp} The tournament will not happen if there are less than 100 pets'
    )

    embed = discord.Embed(
        color = global_data.color,
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

    schedule = f'{emojis.bp} Every 12 hours at 00:00 / 12:00 UTC'
    
    answers = f'{emojis.bp} `buy lottery ticket [1-10]`'
    
    rewards = (
        f'{emojis.bp} A huge amount of {emojis.coin} coins if you win\n'
        f'{emojis.bp} Absolutely nothing if you don\'t'
    )
                    
    note =(
        f'{emojis.bp} {events_official_server}\n'
        f'{emojis.bp} You can buy up to 10 lottery tickets for each draw\n'
        f'{emojis.bp} The size of the pot depends on ticket prices and tickets sold\n'
        f'{emojis.bp} The ticket prices are different with every lottery'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'LOTTERY EVENT',
        description = 'This is a global event which takes place every 12 hours.'
    )    
    
    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    
    return embed

# Not so mini boss event
async def embed_event_notsominiboss(prefix):

    schedule = f'{emojis.bp} Tuesday, Thursday, Saturday at 18:00 UTC'
    
    answers = f'{emojis.bp} `not so mini boss join` (unlocked in area 10)'
    
    rewards = f'{emojis.bp} A small amount of {emojis.dragonscale} dragon scales if the boss dies'
                    
    note = (
        f'{emojis.bp} {events_official_server}\n'
        f'{emojis.bp} {events_once_cycle}\n'
        f'{emojis.bp} This event shares its cooldown with `miniboss` and `dungeon`\n'
        f'{emojis.bp} This event has a chance to fail'
    )
                    
    whichone = (
        f'{emojis.bp} Only do this event if you don\'t need to do a dungeon\n'
        f'{emojis.bp} `miniboss` rewards coins instead of dragon scales'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'NOT SO MINI BOSS EVENT',
        description = 'This is a global event which takes place three times a week.'
    )    
    
    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    embed.add_field(name='DUNGEON OR MINIBOSS OR NOT SO MINI BOSS?', value=whichone, inline=False)
            
    return embed


# --- Embeds: Seasonal events ---
# Snowball fight event (xmas)
async def embed_event_snowball(prefix):

    trigger = (
        f'{emojis.bp} Any command (chance unknown)\n'
        f'{emojis.bp} By using a {emojis.xmashat} christmas hat'
    )
    
    answers = (
        f'{emojis.bp} `fight`: Low chance to get more loot than `summon`, high chance to get less.\n'
        f'{emojis.bp} `summon`: 50/50 chance to get more or less loot\n'
        f'{emojis.bp} `sleep`: Very low chance to get more loot than `summon` and `fight`, very high chance to get less'
    )
    
    best_answer = (
        f'{emojis.bp} If you don\'t feel like gambling, `summon` is the safest answer\n'
        f'{emojis.bp} If you _do_ feel like gambling, `sleep` has the highest potential rewards'
    )
    
    note =(
        f'{emojis.bp} This event gives much higher rewards if it\'s triggered with a {emojis.xmashat} christmas hat\n'
        f'{emojis.bp} You always get some loot, even if you lose'
    )

    embed = discord.Embed(
        color = global_data.color,
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

    trigger = f'{emojis.bp} `hunt`, `adventure` and work commands (0.75 % chance)'
    
    answers = (
        f'{emojis.bp} The bunny has a {emojis.pethappiness} happiness and :carrot: hunger stat\n'
        f'{emojis.bp} You can enter a line of commands to influence these stats\n'
        f'{emojis.bp} `feed` decreases hunger by 18-22\n'
        f'{emojis.bp} `pat` increases happiness by 8-12\n'
        f'{emojis.bp} Example: `feed feed pat pat pat`\n'
        f'{emojis.bp} If happiness is 85+ higher than hunger, catch chance is 100%\n'
        f'{emojis.bp} You can only use up to 6 commands\n'
        f'{emojis.bp} Less commands = 15 {emojis.easteregg} easter eggs for every command not used'
    )
    
    rewards = (
        f'{emojis.bp} {emojis.easterbunny} Bunny (used in crafting {emojis.easterspawner} boss spawners)\n'
        f'{emojis.bp} {emojis.petgoldenbunny} Fake golden bunny. Gifts you a {emojis.easterspawner} boss spawner every day.'
    )
    
    note =(
        f'{emojis.bp} You can increase the chance of this event by crafting {emojis.easterrainbowcarrot} rainbow carrots\n'
        f'{emojis.bp} You can craft up to 5 carrots which gives you a 3 % spawn chance'
    )

    embed = discord.Embed(
        color = global_data.color,
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
        f'{emojis.bp} Craft a {emojis.easterspawner} boss spawner\n'
        f'{emojis.bp} Use `egg use boss spawner` or `egg buy instant spawn`\n'
        f'{emojis.bp} If you don\'t buy an instant spawn, this will use your dungeon cooldown'
    )
    
    answers = (
        f'{emojis.bp} `fight` or `defend`\n'
        f'{emojis.bp} Look at the boss stats to decide what to choose'
    )
    
    rewards = (
        f'{emojis.bp} 1-2 {emojis.easteregggolden} golden eggs\n'
        f'{emojis.bp} {emojis.easteregg} Easter eggs\n'
        f'{emojis.bp} {emojis.arenacookie} Arena cookies\n'
        f'{emojis.bp} {emojis.epiccoin} EPIC coins\n'
        f'{emojis.bp} {emojis.easterlootbox} Easter lootboxes\n'
        f'{emojis.bp} The participants have a chance to get a few {emojis.easteregg} easter eggs and {emojis.arenacookie} cookies'
    )
                
    note = (
        f'{emojis.bp} {events_multiplayer}\n'
        f'{emojis.bp} {events_player_no.format(no=15)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = 'BUNNY BOSS EVENT',
        description = 'This is a multiplayer easter event in which you fight a bunny boss.'
    )    
    
    embed.set_footer(text=f'{events_footer.format(prefix=prefix)}')
    embed.add_field(name='HOW TO START', value=trigger, inline=False)
    embed.add_field(name='HOW TO JOIN', value=answers, inline=False)
    embed.add_field(name='POSSIBLE REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
            
    return embed