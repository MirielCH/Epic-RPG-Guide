# returning.py

import discord
from discord.ext import commands

import emojis
import global_data


# Returning commands (cog)
class ReturningCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "love"
    @commands.command(aliases=('return','ret'))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def returning(self, ctx: commands.Context) -> None:
        """Returning event"""
        embed = await embed_returning_overview(ctx.prefix)
        await ctx.send(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(ReturningCog(bot))


# --- Embeds ---
async def embed_returning_overview(prefix: str) -> discord.Embed:
    """Returning overview embed"""
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
        f'{emojis.BP} You can only get this event if you have not played at all for **at least 2 months**\n'
        f'{emojis.BP} This is a personal event with no fixed schedule\n'
    )
    embed = discord.Embed(
        color = 0xED04F5,
        title = f'RETURNING EVENT {emojis.EPIC_RPG_LOGO}',
        description = 'Oh hi, nice to see you again'
    )
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed