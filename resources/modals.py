# views.py
"""Contains global interaction views"""

import discord
from discord.ui import InputText, Modal

from content import crafting


class CraftingCalculatorAmountModal(Modal):
    def __init__(self, view: discord.ui.View) -> None:
        super().__init__(title='Crafting calculator')
        self.ctx = view.ctx
        self.view = view
        self.item_name = view.item_name
        self.item_emoji = view.item_emoji
        self.add_item(
            InputText(
                label=f'Amount of {self.item_name} you want to craft:',
                placeholder="Enter amount ..."
            )
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.value = 'triggered'
        await interaction.response.edit_message()
        self.view.stop()
        await crafting.command_crafting_calculator(self.ctx, self.item_name, self.children[0].value)