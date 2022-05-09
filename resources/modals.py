# views.py
"""Contains global interaction views"""

import discord
from discord.ui import InputText, Modal

from content import crafting
from resources import functions, strings


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
        amount = await functions.calculate_amount(self.children[0].value)
        if amount is None:
            await interaction.response.send_message(strings.MSG_INVALID_AMOUNT, ephemeral=True)
            return
        if amount < 1:
            await interaction.response.send_message(strings.MSG_AMOUNT_TOO_LOW, ephemeral=True)
            return
        if amount > 999_000_000_000_000:
            await interaction.response.send_message(strings.MSG_AMOUNT_TOO_HIGH, ephemeral=True)
            return
        self.view.value = 'triggered'
        await interaction.response.edit_message()
        self.view.stop()
        await crafting.command_crafting_calculator(self.ctx, self.item_name, amount)