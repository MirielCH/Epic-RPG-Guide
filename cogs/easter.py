# easter.py

import discord
from discord.ext import commands

import emojis
import global_data


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
        f'{emojis.BP} Get {emojis.EASTER_EGG} easter eggs in `hunt`, `adventure` and all fish command tiers\n'
        f'{emojis.BP} Tame bunnies in the new random **bunny event** (see `{prefix}event bunny`)\n'
        f'{emojis.BP} Defeat the {emojis.EASTER_BUNNY_BOSS} **bunny boss** to get {emojis.EASTER_EGG_GOLDEN} golden eggs (see `{prefix}event bunny boss`)\n'
        f'{emojis.BP} Complete the **quest** to get the {emojis.PET_GOLDEN_BUNNY} golden bunny pet (see `rpg egg quest`)\n'
        f'{emojis.BP} Gamble all your eggs away with `rpg egg slots`'
    )

    bonuses = (
        f'{emojis.BP} Dungeon/Miniboss cooldown is lowered to 6h'
    )

    whattodo = (
        f'{emojis.BP} Craft 5 {emojis.EASTER_RAINBOW_CARROT} rainbow carrots first to increase bunny event spawns\n'
        f'{emojis.BP} Craft a {emojis.EASTER_SPAWNER} boss spawner whenever you have a {emojis.EASTER_BUNNY} bunny and enough eggs to buy the instant spawn to spawn the {emojis.EASTER_BUNNY_BOSS} bunny boss\n'
        f'{emojis.BP} Get at least 10 {emojis.EASTER_EGG_GOLDEN} golden eggs to complete the quest\n'
        f'{emojis.BP} Craft {emojis.SLEEPY_POTION} sleepy potions with leftover {emojis.EASTER_EGG_GOLDEN} golden eggs\n'
        f'{emojis.BP} Spend leftover {emojis.EASTER_EGG} easter eggs in the shop (`rpg egg shop`)'
    )

    schedule = (
        f'{emojis.BP} Event started on April 3, 2021\n'
        f'{emojis.BP} Event ended on April 17, 2021, 23:55 UTC\n'
        f'{emojis.BP} Items will vanish on April 22, 2021, 23:55 UTC'
    )

    guides = (
        f'{emojis.BP} {guide_bunny.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_bunnyboss.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_easter.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = f'EASTER EVENT 2021 {emojis.EASTER_EGG}',
        description = 'Hope you like eggs.'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='WHAT TO DO', value=whattodo, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)

    return embed