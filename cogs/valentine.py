# valentine.py

import discord
from discord.ext import commands

import emojis
import global_data


# Valentine commands (cog)
class ValentineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "love"
    @commands.command(aliases=('love','val'))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def valentine(self, ctx: commands.Context) -> None:
        """Valentine"""
        embed = await embed_valentine_overview(ctx.prefix)
        await ctx.send(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(ValentineCog(bot))


# --- Embeds ---
async def embed_valentine_overview(prefix: str) -> discord.Embed:
    """Valentine overview embed"""
    activities = (
        f'{emojis.BP} Use `rpg love share` to get {emojis.COIN_LOVE} love coins\n'
        f'{emojis.BP} Complete the event quest to get a {emojis.PET_PINK_FISH} pink fish pet\n'
        f'{emojis.BP} Kill the rare {emojis.MOB_PINK_WOLF} pink wolf in `hunt` to get extra coins\n'
        f'{emojis.BP} Buy various rewards in the `rpg love shop`\n'
        f'{emojis.BP} Gamble all your love coins away with `rpg love slots`\n'
    )
    bonuses = (
        f'{emojis.BP} `hunt` cooldown is reduced by 25%\n'
        f'{emojis.BP} `adventure` cooldown is reduced by 10% (**only if you are married**)\n'
    )
    love_tokens = (
        f'{emojis.BP} Love tokens are basically lootboxes with a special way of opening\n'
        f'{emojis.BP} To open these, use `rpg love share` with a player **who also has one**\n'
        f'{emojis.BP} If you **don\'t** want to open your token, use `rpg love share @player notokens`\n'
        f'{emojis.BP} You can only get these by completing the quest\n'
        f'{emojis.BP} Check `rpg love info love tokens` for what they can contain\n'
    )
    love_share = (
        f'{emojis.BP} Use `rpg love share @player` to ping another player\n'
        f'{emojis.BP} You need to be able to heal both yourself **and** the pinged player\n'
        f'{emojis.BP} You need at least 1 {emojis.LIFE_POTION} life potion in your inventory\n'
        f'{emojis.BP} Marriage is the easiest way of doing this since you both take damage in `hunt t`\n'
        f'{emojis.BP} If you are not married, find someone to do this with during this event\n'
        f'{emojis.BP} Please don\'t spam ping random players :eyes:\n'
    )
    titles = (
        f'{emojis.BP} **Wood you be my valentine?** (bought in `rpg love shop`)\n'
        f'{emojis.BP} **lovely fren** (Achievement #145, see `{prefix}title 145`)\n'
        f'{emojis.BP} **Heart broken** (Achievement #146, see `{prefix}title 146`)\n'
    )
    schedule = (
        f'{emojis.BP} Event started on February 11, 2022\n'
        f'{emojis.BP} Event ends on February 17, 2022, 23:55 UTC\n'
    )
    tldr_guide = (
        f'{emojis.BP} Use `rpg love share` after every hunt to get {emojis.COIN_LOVE} love coins\n'
        f'{emojis.BP} Complete the `rpg love quest` to unlock the {emojis.PET_PINK_FISH} pink fish pet\n'
        f'{emojis.BP} Use your coins for whatever you want in `rpg love shop`\n'
    )
    chances = (
        f'{emojis.BP} 0.5% to find the {emojis.MOB_PINK_WOLF} pink wolf in `hunt`\n'
        f'{emojis.BP} The chance is increased do 1% if the world buff from the shop is active\n'
    )
    embed = discord.Embed(
        color = 0xED04F5,
        title = f'VALENTINE EVENT 2022 {emojis.COIN_LOVE}',
        description = 'Voulez-vous trinquer avec moi, ce soir ?'
    )
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='TITLES', value=titles, inline=False)
    embed.add_field(name='HOW LOVE SHARING WORKS', value=love_share, inline=False)
    embed.add_field(name=f'WHAT TO DO WITH {emojis.TOKEN_LOVE} LOVE TOKENS', value=love_tokens, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    #embed.add_field(name='CHANCES', value=chances, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed