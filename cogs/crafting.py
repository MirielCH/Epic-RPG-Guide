# crafting.py

import asyncio

import discord
from discord.ext import commands
from discord.commands import Option, slash_command, SlashCommandGroup

from content import crafting
import database
from resources import functions, strings


ALL_ITEMS = functions.await_coroutine(database.get_all_items())
INVCALC_ITEMS = [
    'apple',
    'banana',
    'EPIC fish',
    'EPIC log',
    'golden fish',
    'HYPER log',
    'MEGA log',
    'normie fish',
    'ruby',
    'SUPER log',
    'ULTRA log',
    'wooden log',
]


# --- Autocomplete functions ---
async def craft_item_searcher(ctx: discord.AutocompleteContext):
    """Returns a list of matching craftable items from ALL_ITEM_NAMES"""
    return [item.name for item in ALL_ITEMS if ctx.value.lower() in item.name.lower() and item.ingredients]


async def dismantle_item_searcher(ctx: discord.AutocompleteContext):
    """Returns a list of matching dismanteable items from ALL_ITEM_NAMES"""
    return [item.name for item in ALL_ITEMS if ctx.value.lower() in item.name.lower() and item.dismanteable]


class CraftingCog(commands.Cog):
    """Cog with crafting related commands"""
    def __init__(self, bot):
        self.bot = bot

    cmd_dropchance = SlashCommandGroup(
        "dropchance",
        "Dropchance commands",
    )

    cmd_inventory = SlashCommandGroup(
        "inventory",
        "Inventory commands",
    )

    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_dropchance.command(name='calculator', description='Calculates your dropchance')
    async def dropchance_calculator(
        self,
        ctx: discord.ApplicationContext,
        timetravel: Option(int, 'The TT you want to calculate for. Uses your progress setting if empty.',
                           min_value = 0, max_value = 999, default=None),
        horse_tier: Option(int, 'The horse tier you want to calculate for. Reads from EPIC RPG if empty.',
                           min_value = 1, max_value = 10, default=None),
    ) -> None:
        """Dropchance calculator"""
        await crafting.command_dropchance_calculator(self.bot, ctx, timetravel=timetravel, horse_tier=horse_tier)

    @slash_command(description='Shows the materials you need to craft an item')
    async def craft(
        self,
        ctx: discord.ApplicationContext,
        item_name: Option(str, 'The item you want to craft', name='item',
                          autocomplete=craft_item_searcher),
        amount: Option(str, 'The amount of items you want to see the materials for'),
    ) -> None:
        """Calculates mats you need when crafting items"""
        await crafting.command_craft(ctx, item_name, amount)

    @slash_command(description='Shows the materials you get when dismantling an item')
    async def dismantle(
        self,
        ctx: discord.ApplicationContext,
        item_name: Option(str, 'The item you want to dismantle', name='item',
                          autocomplete=dismantle_item_searcher),
        amount: Option(str, 'The amount of items you want to see the materials for'),
    ) -> None:
        """Calculates mats you get when dismantling items"""
        await crafting.command_dismantle(ctx, item_name, amount)

    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_inventory.command(name='calculator', description='Converts your inventory into one material')
    async def inventory_calculator(
        self,
        ctx: discord.ApplicationContext,
        area_no: Option(int, 'The area you are currently in. Use 21 if in the TOP.', name='area',
                        min_value = 1, max_value = 21, autocomplete=functions.area_choice),
        material: Option(str, 'The material you want to convert to', choices=INVCALC_ITEMS),
    ) -> None:
        """Dropchance calculator"""
        await crafting.command_inventory_calculator(self.bot, ctx, area_no, material)

# Initialization
def setup(bot):
    bot.add_cog(CraftingCog(bot))