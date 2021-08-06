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
        f'{emojis.bp} Get {emojis.easteregg} easter eggs in `hunt`, `adventure` and all fish command tiers\n'
        f'{emojis.bp} Tame bunnies in the new random **bunny event** (see `{prefix}event bunny`)\n'
        f'{emojis.bp} Defeat the {emojis.easterbunnyboss} **bunny boss** to get {emojis.easteregggolden} golden eggs (see `{prefix}event bunny boss`)\n'
        f'{emojis.bp} Complete the **quest** to get the {emojis.petgoldenbunny} golden bunny pet (see `rpg egg quest`)\n'
        f'{emojis.bp} Gamble all your eggs away with `rpg egg slots`'
    )

    bonuses = (
        f'{emojis.bp} Dungeon/Miniboss cooldown is lowered to 6h'
    )

    whattodo = (
        f'{emojis.bp} Craft 5 {emojis.easterrainbowcarrot} rainbow carrots first to increase bunny event spawns\n'
        f'{emojis.bp} Craft a {emojis.easterspawner} boss spawner whenever you have a {emojis.easterbunny} bunny and enough eggs to buy the instant spawn to spawn the {emojis.easterbunnyboss} bunny boss\n'
        f'{emojis.bp} Get at least 10 {emojis.easteregggolden} golden eggs to complete the quest\n'
        f'{emojis.bp} Craft {emojis.sleepypotion} sleepy potions with leftover {emojis.easteregggolden} golden eggs\n'
        f'{emojis.bp} Spend leftover {emojis.easteregg} easter eggs in the shop (`rpg egg shop`)'
    )

    schedule = (
        f'{emojis.bp} Event started on April 3, 2021\n'
        f'{emojis.bp} Event ended on April 17, 2021, 23:55 UTC\n'
        f'{emojis.bp} Items will vanish on April 22, 2021, 23:55 UTC'
    )

    guides = (
        f'{emojis.bp} {guide_bunny.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_bunnyboss.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_easter.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.color,
        title = f'EASTER EVENT 2021 {emojis.easteregg}',
        description = 'Hope you like eggs.'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='WHAT TO DO', value=whattodo, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)

    return embed