# easter.py

import discord
from discord.ext import commands

from resources import emojis
from resources import settings
from resources import functions


# easter event commands (cog)
class easterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "easter"
    @commands.command(aliases=('egg','eggs','easterevent',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def easter(self, ctx, *args):
        embed = await embed_easter_overview(ctx.prefix)
        await ctx.send(embed=embed)
        return

# Initialization
def setup(bot):
    bot.add_cog(easterCog(bot))


# --- Redundancies ---
# Additional guides
guide_bunny = '`{prefix}event bunny` : Bunny event'
guide_bunnyboss = '`{prefix}event bunny boss` : Bunny boss event'
guide_easter = '`rpg egg info` : Easter event guide'



# --- Embeds ---
# Easter overview
async def embed_easter_overview(prefix):

    activities = (
        f'{emojis.BP} Complete daily and weekly **tasks** (`rpg egg tasks`)\n'
        f'{emojis.BP} Get {emojis.EASTER_EGG} easter eggs in `hunt`, `adventure` and all fish command tiers\n'
        f'{emojis.BP} Tame bunnies in the random **bunny event** (see `{prefix}event bunny`)\n'
        f'{emojis.BP} Defeat the **bunny slime** in `rpg hunt`\n'
        f'{emojis.BP} Defeat the {emojis.EASTER_BUNNY_BOSS} **bunny boss** to get {emojis.EASTER_EGG_GOLDEN} golden '
        f'eggs (see `{prefix}event bunny boss`)\n'
        f'{emojis.BP} Buy various rewards in the **shop** (`rpg egg shop`)\n'
        f'{emojis.BP} Complete the **quest** to get the {emojis.PET_GOLDEN_BUNNY} golden bunny pet (see `rpg egg quest`)\n'
        f'{emojis.BP} Gamble all your eggs away with `rpg egg slots`'
    )

    bonuses = (
        f'{emojis.BP} Dungeon/Miniboss cooldown is lowered to 6h'
    )

    guide = (
        f'{emojis.BP} Complete your tasks daily / weekly in `rpg egg tasks`\n'
        f'{emojis.BP} Craft 5 {emojis.EASTER_RAINBOW_CARROT} rainbow carrots to increase bunny spawns\n'
        f'{emojis.BP} Craft a {emojis.EASTER_SPAWNER} boss spawner when you have a {emojis.EASTER_BUNNY} bunny'
        f'{emojis.BLANK} Requires a dungeon cooldown to use\n'
        f'{emojis.BP} Get at least 10 {emojis.EASTER_EGG_GOLDEN} golden eggs to complete the quest\n'
        f'{emojis.BP} Spend {emojis.EASTER_CHOCOLATE_COIN} chocolate coins and leftover {emojis.EASTER_EGG_GOLDEN} '
        f'in the shop\n'
    )

    schedule = (
        f'{emojis.BP} Event started on April 11, 2022\n'
        f'{emojis.BP} Event ended on April 25, 2022, 23:55 UTC\n'
        f'{emojis.BP} Items will vanish on May 2, 2022, 23:55 UTC'
    )

    guides = (
        f'{emojis.BP} {guide_bunny.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_bunnyboss.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_easter.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'EASTER EVENT 2022 {emojis.EASTER_EGG}',
        description = 'CHOCOLATE! EGGS! CHOCOLATE EGGS! Ah no, coins, sorry.'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='TL;DR GUIDE', value=guide, inline=False)
    embed.add_field(name='ALL ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)

    return embed