# views.py
"""Contains global interaction views"""

from typing import Optional

import discord
from discord.ui import InputText, Modal

from content import crafting
import database
from resources import strings


class CraftingCalculatorAmountModal(Modal):
    def __init__(self, ctx: discord.ApplicationContext, item_name: str, item_emoji: str) -> None:
        super().__init__(title='Crafting calculator')
        self.ctx = ctx
        self.item_name = item_name
        self.item_emoji = item_emoji
        self.add_item(
            InputText(
                label=f'Amount of {item_name} you want to craft:',
                placeholder="Enter amount ..."
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message()
        await crafting.command_crafting_calculator(self.ctx, self.item_name, self.children[0].value)