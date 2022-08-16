# events.py

from discord.ext import commands

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
        'coindrop',
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
        'trainingevent','voidevent',
    )

    # Command "events"
    @commands.command(aliases=events_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def events_overview(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'event guide')


# Initialization
def setup(bot):
    bot.add_cog(eventsCog(bot))