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


class TimeJumpCalculatorStatsModal(Modal):
    def __init__(self, view: discord.ui.View) -> None:
        super().__init__(title='Time jump calculator stats')
        self.ctx = view.ctx
        self.view = view
        self.add_item(
            InputText(
                label='Level:',
                placeholder="Enter level ..."
            )
        )
        self.add_item(
            InputText(
                label='(Optional) AT from boosts or food:',
                placeholder="Enter AT ...",
                required=False
            )
        )
        self.add_item(
            InputText(
                label='(Optional) DEF from boosts or food:',
                placeholder="Enter DEF ...",
                required=False
            )
        )
        self.add_item(
            InputText(
                label='(Optional) LIFE from boosts or food:',
                placeholder="Enter LIFE ...",
                required=False
            )
        )

    async def callback(self, interaction: discord.Interaction):
        level = await functions.calculate_amount(self.children[0].value)
        extra_at_value = self.children[1].value if self.children[1].value != '' else '0'
        extra_def_value = self.children[2].value if self.children[2].value != '' else '0'
        extra_life_value = self.children[3].value if self.children[3].value != '' else '0'
        extra_at = await functions.calculate_amount(extra_at_value)
        extra_def = await functions.calculate_amount(extra_def_value)
        extra_life = await functions.calculate_amount(extra_life_value)
        if level is None:
            await interaction.response.send_message('That\'s a valid level.', ephemeral=True)
            return
        if extra_at is None:
            await interaction.response.send_message('That\'s an invalid AT amount.', ephemeral=True)
            return
        if extra_def is None:
            await interaction.response.send_message('That\'s an invalid DEF amount.', ephemeral=True)
            return
        if extra_life is None:
            await interaction.response.send_message('That\'s an invalid LIFE amount.', ephemeral=True)
            return
        if level < 1:
            await interaction.response.send_message('Level needs to be 1 or higher', ephemeral=True)
            return
        if level > 999_000 or extra_at > 999_000_000 or extra_def >  999_000_000 or extra_life > 999_000_000:
            await interaction.response.send_message(strings.MSG_AMOUNT_TOO_HIGH, ephemeral=True)
            return
        if extra_at < (level * -1) or extra_def < (level * -1) or extra_life < (level * -1):
            await interaction.response.send_message('Stats can\'t go below level 1', ephemeral=True)
            return
        self.view.profile_data['level'] = level
        self.view.profile_data['extra_at'] = extra_at
        self.view.profile_data['extra_def'] = extra_def
        self.view.profile_data['extra_life'] = extra_life
        embed = await self.view.embed_function(self.view.area_no, self.view.inventory, self.view.profile_data,
                                               self.view.option_inventory, self.view.option_stats)
        await interaction.response.edit_message(embed=embed, view=self.view)


class SetCurrentTTModal(Modal):
    def __init__(self, view: discord.ui.View) -> None:
        super().__init__(title='Change current TT')
        self.view = view
        self.add_item(
            InputText(
                label='Your current TT [0-999]',
                placeholder="Enter TT number ..."
            )
        )

    async def callback(self, interaction: discord.Interaction):
        tt_no = self.children[0].value.lower()
        msg_error = 'Invalid TT number. Please enter a number between 0 and 999.'
        try:
            tt_no = int(tt_no)
        except:
            await interaction.response.edit_message(view=self.view)
            await interaction.followup.send(msg_error, ephemeral=True)
            return
        if not 0 <= tt_no <= 999:
            await interaction.response.edit_message(view=self.view)
            await interaction.followup.send(msg_error, ephemeral=True)
            return
        await self.view.user_settings.update(tt=tt_no)
        embed = await self.view.embed_function(self.view.ctx, self.view.user_settings)
        await interaction.response.edit_message(embed=embed, view=self.view)