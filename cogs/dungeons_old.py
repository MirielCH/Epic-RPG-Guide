# dungeons.py

from discord.ext import commands

from resources import functions


# dungeon commands (cog)
class DungeonsOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Dungeons menu
    @commands.command(aliases=('dungeons',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def dungeonguide(self, ctx):
        await functions.send_slash_migration_message(ctx, 'dungeon guide')

    # Dungeon guide, can be invoked with "dX", "d X", "dungeonX" and "dungeon X"
    dungeon_aliases = ['dungeon','dung','dung15-1','d15-1','dungeon15-1','dung15-2','d15-2','dungeon15-2','dung152',
                       'd152','dungeon152','dung151','d151','dungeon151','dtop','dfinal','dungtop','dungfinal',
                       'dungeontop','dungeonfinal','finalfight']
    for x in range(1,21):
        dungeon_aliases.append(f'd{x}')
        dungeon_aliases.append(f'dungeon{x}')
        dungeon_aliases.append(f'dung{x}')

    @commands.command(name='d',aliases=(dungeon_aliases))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True, attach_files=True)
    async def dungeon(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'dungeon guide')

    # Command "dungeonstats" - Returns recommended stats for all dungeons
    @commands.command(aliases=('dstats','ds',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeonstats(self, ctx):
        await functions.send_slash_migration_message(ctx, 'dungeon guide')

    # Command "dungeongear" - Returns recommended gear for all dungeons
    @commands.command(aliases=('dgear','dg','dg1','dg2','dg3'))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeongear(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'dungeon guide')

    # Command "dungeoncheck" - Checks user stats against recommended stats
    @commands.command(aliases=('dcheck','dungcheck','dc','check',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeoncheck(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'dungeon check')


    # Command "dungeoncheckX" - Checks user stats against recommended stats of a specific dungeon
    dungeon_check_aliases = ['dcheck1','check1','dungcheck1','dc1','dcheck15-1','check15-1','dungcheck15-1','dc15-1','dcheck151','check151','dungcheck151','dc151','dcheck15-2','check15-2','dungcheck15-2','dc15-2','dcheck152','check152','dungcheck152','dc152',]
    for x in range(2,21):
        dungeon_check_aliases.append(f'dcheck{x}')
        dungeon_check_aliases.append(f'check{x}')
        dungeon_check_aliases.append(f'dungeoncheck{x}')
        dungeon_check_aliases.append(f'dungcheck{x}')
        dungeon_check_aliases.append(f'dc{x}')

    @commands.command(aliases=dungeon_check_aliases)
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeoncheck1(self, ctx, *args):
        await functions.send_slash_migration_message(ctx, 'dungeon check')


# Initialization
def setup(bot):
    bot.add_cog(DungeonsOldCog(bot))