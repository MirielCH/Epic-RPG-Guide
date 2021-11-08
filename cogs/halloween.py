# halloween.py

import discord
from discord.ext import commands

import emojis
import global_data


# Additional guides
GUIDE_OVERVIEW = '`{prefix}hal` : Halloween overview'
GUIDE_ITEMS = '`{prefix}hal items` : Halloween item overview'
GUIDE_SLIME = '`{prefix}event slime` : Bat slime event'
GUIDE_BOSS = '`{prefix}event scroll boss` : Scroll boss event & tactics'
GUIDE_CHANCES = '`{prefix}hal chances` : Spawn and drop chances'
GUIDE_ERPG = '`rpg hal info` : EPIC RPG event guide'
GUIDE_EPRG_CONSUMABLES = '`rpg hal info consumables` : EPIC RPG consumables guide'
GUIDE_EPRG_ITEMS = '`rpg hal info items` : EPIC RPG items guide'

# Items
ITEMS = ['epic candy', 'monster soul', 'pumpkin', 'sleepy potion', 'spooky orb']


# Halloween commands (cog)
class HalloweenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command "hal"
    @commands.command(aliases=('hal',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def halloween(self, ctx: commands.Context, *args: str) -> None:
        """Halloween"""
        full_args = ''.join([arg.lower() for arg in args]) if args else ''
        if any(word in full_args for word in ['scroll','slime']):
            command = self.bot.get_command(name='event')
            if command is not None:
                await command.callback(command.cog, ctx, args)
            return
        elif any(word in full_args for word in ['monster','soul']):
            embed = await embed_halloween_item(ctx.prefix, 'monster soul')
        elif any(word in full_args for word in ['epic','candy']):
            embed = await embed_halloween_item(ctx.prefix, 'epic candy')
        elif any(word in full_args for word in ['sleepy','potion']):
            embed = await embed_halloween_item(ctx.prefix, 'sleepy potion')
        elif any(word in full_args for word in ['spooky','orb']):
            embed = await embed_halloween_item(ctx.prefix, 'spooky orb')
        elif 'pumpkin' in full_args:
            embed = await embed_halloween_item(ctx.prefix, 'pumpkin')
        elif 'item' in full_args:
            embed = await embed_halloween_item_overview(ctx.prefix)
        elif 'chance' in full_args:
            embed = await embed_halloween_chances(ctx.prefix)
        else:
            embed = await embed_halloween_overview(ctx.prefix)
        await ctx.send(embed=embed)


# Initialization
def setup(bot):
    bot.add_cog(HalloweenCog(bot))


# --- Embeds ---
async def embed_halloween_overview(prefix: str) -> discord.Embed:
    """Halloween overview embed"""
    activities = (
        f'{emojis.BP} **Loot** various event items (see `{prefix}hal items`)\n'
        f'{emojis.BP} **Craft** various items (see `rpg hal info consumables`)\n'
        f'{emojis.BP} Scare your friends with `rpg hal boo` (2h cooldown)\n'
        f'{emojis.BP} Complete daily and weekly **tasks** (see `rpg hal tasks`)\n'
        f'{emojis.BP} Defeat the event themed {emojis.HAL_JACK_O_LANTERN} Sleepy Jack O\'Lantern **miniboss**\n'
        f'{emojis.BP} Join the **world boss** fight to unlock codes (see `rpg hal wb`)\n'
        f'{emojis.BP} Complete the event **quest** to get the {emojis.PET_PUMPKIN_BAT} pumpkin bat pet '
        f'(see `rpg hal quest`)\n'
        f'{emojis.BP} Buy stuff in the event shop (see `rpg hal shop`)\n'
    )
    bonuses = (
        f'{emojis.BP} Miniboss/dungeon cooldown is reduced by 33%'
    )
    schedule = (
        f'{emojis.BP} Event started on October 18, 2021\n'
        f'{emojis.BP} World boss fight ends on October 31, 2021, 23:55 UTC\n'
        f'{emojis.BP} Event ends on November 14, 2021, 23:00 UTC\n'
        f'{emojis.BP} Items will vanish on November 22, 2021, 23:00 UTC'
    )
    tldr_guide = (
        f'{emojis.BP} **Optional**: Craft a {emojis.HAL_CANDY_FISH} candy fish and use it to get the SPOOKY horse\n'
        f'{emojis.BP} Complete your daily and weekly tasks\n'
        f'{emojis.BP} Craft as many {emojis.HAL_CANDY_BELL} candy bells as you are allowed daily\n'
        f'{emojis.BP} Use your first 40 {emojis.HAL_SPOOKY_ORB} spooky orbs to craft 10 {emojis.HAL_SPOOKY_SCROLL} '
        f'spooky scrolls. Use `{prefix}scroll` for the correct answers.\n**Do not spend orbs in the shop until you have done this.**\n'
        f'{emojis.BP} Use {emojis.HAL_MONSTER_SOUL} monster souls you get with `rpg hal wb throw`\n'
        f'{emojis.BP} Complete the quest\n'
        f'{emojis.BP} Check the rest of this guide for everything else\n'
    )
    guides = (
        f'{emojis.BP} {GUIDE_ITEMS.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_SLIME.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_BOSS.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_CHANCES.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_ERPG}'
    )
    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = f'HALLOWEEN EVENT 2021 {emojis.HAL_PUMPKIN}',
        description = 'Boo.'
    )
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    return embed


async def embed_halloween_item_overview(prefix: str) -> discord.Embed:
    """Halloween item overview"""

    items_value = ''
    for item in sorted(ITEMS):
        items_value = f'{items_value}\n{emojis.BP} `{item}`'
    items_value.strip()
    guides = (
        f'{emojis.BP} {GUIDE_OVERVIEW.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_SLIME.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_BOSS.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_CHANCES.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_EPRG_CONSUMABLES}\n'
        f'{emojis.BP} {GUIDE_EPRG_ITEMS}\n'
    )
    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'HALLOWEEN ITEM OVERVIEW',
        description = (
            f'Use `{prefix}hal [item name]` to see details about a listed item.\n'
            f'For other items see `rpg hal info items` / `rpg hal info consumables`\n'
        )

    )
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='ITEM NAMES', value=items_value, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    return embed


async def embed_halloween_item(prefix: str, item: str) -> discord.Embed:
    """Halloween item embed"""
    sources = (
        f'{emojis.BP} {emojis.SLEEPY_POTION} Sleepy potion: `hal quest`, {emojis.HAL_JACK_O_LANTERN} miniboss, '
        f'{emojis.HAL_BOSS} scroll boss\n'
        f'{emojis.BP} ➜ See `rpg hal info items` and `rpg hal info consumables` for more items\n'
    )
    epic_candy_source = (
        f'{emojis.BP} 3 per defeated {emojis.HAL_JACK_O_LANTERN} Jack O\'Lantern miniboss\n'
        f'{emojis.BP} 2 per daily task, 5 per weekly task in `hal tasks`\n'
    )
    epic_candy_usage = (
        f'{emojis.BP} **Optional**: Craft 1 {emojis.HAL_CANDY_FISH} candy fish and use it. This will get you a SPOOKY horse which '
        f'increases the chance to find pumpkins and bat slimes. Note that your horse type will **not** revert after the event.\n'
        f'{emojis.BP} Craft 12 {emojis.HAL_CANDY_BELL} candy bells. This increases your chance to find bat slimes, '
        f'plus you need to do this for the quest. You can have 3 on first day and +1 per day after that (20 max).\n'
        f'{emojis.BP} Craft 10 {emojis.HAL_SPOOKY_SCROLL} spooky scrolls to spawn scroll bosses '
        f'(see `{prefix}event scroll boss`). You need these for the quest.\n'
        f'{emojis.BP} Craft {emojis.HAL_CANDY_BAIT} candy bait after finishing the quest and use them to spawn bat '
        f'slimes (see `{prefix}event slime`)\n'
    )
    orb_source = (
        f'{emojis.BP} 1 per encountered {emojis.HAL_BAT_SLIME} bat slime in `adventure`\n'
        f'{emojis.BP} 4-8 per {emojis.HAL_BAT_SLIME} bat slime event (see `{prefix}event slime`)\n'
        f'{emojis.BP} 50 from `hal quest`\n'
        f'{emojis.BP} 5 from code `worldboss4`\n'
        f'{emojis.BP} 3 from code `worldboss5`\n'
    )
    orb_usage = (
        f'{emojis.BP} Craft 10 {emojis.HAL_SPOOKY_SCROLL} spooky scrolls to spawn scroll bosses '
        f'(see `{prefix}event scroll boss`). You need these for the quest.\n'
        f'{emojis.BP} **Do not use orbs for anything else until you have done the 10 scrolls**\n'
        f'{emojis.BP} Buy the {emojis.LB_OMEGA} OMEGA lootboxes in the shop\n'
        f'{emojis.BP} Buy the event title and background if you like them\n'
        f'{emojis.BP} Craft more {emojis.HAL_SPOOKY_SCROLL} spooky scrolls if you want\n'
    )
    soul_source = (
        f'{emojis.BP} `hunt`\n'
    )
    soul_usage = (
        f'{emojis.BP} Join the fight against the world boss (`rpg hal wb throw`). You also need to do this '
        f'at least 5 times for the quest.\n'
        f'{emojis.BP} If you like, craft {emojis.HAL_RED_SOUL} red souls and use them to activate the world buff'
    )
    pumpkin_source = (
        f'{emojis.BP} 2 for successful scare, 1 for failed scare with `rpg hal boo`\n'
        f'{emojis.BP} 100 per day from `hunt`, `training` and fish commands\n'
        f'{emojis.BP} 100 per daily task, 500 per weekly task in `hal tasks`\n'
        f'{emojis.BP} 5,000 from `hal quest`\n'
        f'{emojis.BP} 200 if you defeat the {emojis.HAL_BOSS} scroll boss\n'
        f'{emojis.BP} 150 if you lose against the {emojis.HAL_BOSS} scroll boss\n'
        f'{emojis.BP} 300 (so far) from event codes (see `{prefix}codes`)\n'
    )
    pumpkin_usage = (
        f'{emojis.BP} Keep some pumpkins around to craft the items you need\n'
        f'{emojis.BP} Buy whatever you fancy from the shop'
    )
    potion_source = (
        f'{emojis.BP} 30 from `hal shop`\n'
        f'{emojis.BP} 15 from `hal quest`\n'
        f'{emojis.BP} 1 from code `halloween`\n'
        f'{emojis.BP} 1 from code `halpensation`\n'
        f'{emojis.BP} 1 from code `worldboss1`\n'
        f'{emojis.BP} 1 from code `worldboss2`\n'
        f'{emojis.BP} 1 from code `worldboss3`\n'
    )
    potion_usage = (
        f'{emojis.BP} Use them to reset your cooldowns\n'
    )
    titles = {
        'epic candy': f'EPIC CANDY {emojis.HAL_EPIC_CANDY}',
        'monster soul': f'MONSTER SOUL {emojis.HAL_MONSTER_SOUL}',
        'pumpkin': f'PUMPKIN {emojis.HAL_PUMPKIN}',
        'sleepy potion': f'SLEEPY POTION {emojis.SLEEPY_POTION}',
        'spooky orb': f'SPOOKY ORB {emojis.HAL_SPOOKY_ORB}'
    }
    sources = {
        'epic candy': epic_candy_source,
        'monster soul': soul_source,
        'pumpkin': pumpkin_source,
        'sleepy potion': potion_source,
        'spooky orb': orb_source
    }
    usages = {
        'epic candy': epic_candy_usage,
        'monster soul': soul_usage,
        'pumpkin': pumpkin_usage,
        'sleepy potion': potion_usage,
        'spooky orb': orb_usage
    }

    guides = (
        f'{emojis.BP} {GUIDE_OVERVIEW.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_ITEMS.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_SLIME.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_BOSS.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_CHANCES.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_EPRG_CONSUMABLES}\n'
        f'{emojis.BP} {GUIDE_EPRG_ITEMS}\n'
    )
    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = f'HALLOWEEN ITEM: {titles[item]}'
    )
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='SOURCE', value=sources[item], inline=False)
    embed.add_field(name='WHAT TO DO WITH IT', value=usages[item], inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    return embed


async def embed_halloween_chances(prefix: str) -> discord.Embed:
    """Halloween chances"""

    bat_slime = (
        f'{emojis.BP} Base spawn chance unknown\n'
        f'{emojis.BP} Inceases with {emojis.HAL_CANDY_BELL} candy bells (% unknown, 20 bells max)\n'
        f'{emojis.BP} + 5% if horse has SPOOKY type (use a {emojis.HAL_CANDY_FISH} candy fish to get this type)\n'
        f'{emojis.BP} * 1.3 if world buff is active (use a {emojis.HAL_RED_SOUL} red soul to activate it)\n'
    )
    monster_soul = (
        f'{emojis.BP} Base drop chance unknown\n'
        f'{emojis.BP} Increases with the time since your last hunt\n'
        f'{emojis.BP} Increases with {emojis.TIME_TRAVEL} TT\n'
    )
    miniboss = (
        f'{emojis.BP} 50% chance to get this miniboss when using `rpg miniboss` or when buying an instant miniboss\n'
    )
    boo = (
        f'{emojis.BP} 70% chance to scare someone when using `rpg hal boo`\n'
    )
    guides = (
        f'{emojis.BP} {GUIDE_OVERVIEW.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_ITEMS.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_SLIME.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_BOSS.format(prefix=prefix)}\n'
        f'{emojis.BP} {GUIDE_ERPG}'
    )
    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = 'HALLOWEEN SPAWN AND DROP CHANCES',
        description = 'This page lists all known spawn and drop chances.'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name=f'BAT SLIME {emojis.HAL_BAT_SLIME}', value=bat_slime, inline=False)
    embed.add_field(name=f'MONSTER SOUL {emojis.HAL_MONSTER_SOUL}', value=monster_soul, inline=False)
    embed.add_field(name=f'SLEEPY JACK O\'LANTERN {emojis.HAL_JACK_O_LANTERN}', value=miniboss, inline=False)
    embed.add_field(name='BOO', value=boo, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    return embed