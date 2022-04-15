# dev.py
"""Contains internal testing commands"""

from typing import Optional

import discord
from discord.commands import SlashCommandGroup, CommandPermission
from discord.ext import commands

from resources import emojis, settings, strings


class DummySelect(discord.ui.Select):
    """Dummy select"""
    def __init__(self, placeholder: str):
        options = []
        for x in range(1,4):
            options.append(discord.SelectOption(label=x, value=x))
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options,
                         custom_id='select', row=0)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message()


class EnchantingTableView(discord.ui.View):
    """View with an area select that shows area guides on select.
    Also needs the interaction of the response with the view, so do AreaView.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    active_area: Currently chosen area. Use 21 if the top.
    function: The function that returns the area embed, The function needs to return an embed and have the
    following arguments: context: discord.ApplicationContext, area_no: int, tt_no: int, ascended: bool, full_guide: bool

    Returns
    -------
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: discord.ApplicationContext, interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.ctx = ctx
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.add_item(DummySelect('Select enchant tier ...'))

    @discord.ui.button(label='Enchant sword', style=discord.ButtonStyle.grey, row=1)
    async def enchant_sword(self, button, interaction):
        self.stop()

    @discord.ui.button(label='Enchant armor', style=discord.ButtonStyle.grey, row=1)
    async def enchant_armor(self, button, interaction):
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class TestingCog(commands.Cog):
    """Cog with internal testing commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd_testing = SlashCommandGroup(
        "testing",
        "Testing commands",
        guild_ids=settings.DEV_GUILDS,
        permissions=[
            CommandPermission(
                "owner", 2, True
            )
        ],
    )

    # Commands
    @cmd_testing.command(name='enchanting', description='Enchanting table mockup')
    async def enchant_test(self, ctx: discord.ApplicationContext) -> None:
        """Enchanting table mockup"""
        embed = discord.Embed(
            title = 'Enchanting table',
        )
        field_sword = (
            f'{emojis.SWORD_EDGY} `EDGY sword`\n'
            f':sparkles: `ULTRA-EDGY`\n'
        )
        field_armor = (
            f'{emojis.ARMOR_ELECTRONICAL} `Electronical armor`\n'
            f':sparkles: `OMEGA`\n'
        )
        field_status = (
            f'⇨ You enchanted your armor to :sparkles: `OMEGA`!'
        )
        embed.add_field(name='Sword', value=field_sword, inline=True)
        embed.add_field(name='Armor', value=field_armor, inline=True)
        embed.add_field(name='History', value=field_status, inline=False)
        embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQb1y54astHLrMyCWJSwAPtaMjWSo9sZD2E1w&usqp=CAU')

        view = EnchantingTableView(ctx)
        interaction = await ctx.respond(embed=embed, view=view)
        view.interaction = interaction
        await view.wait()


# Initialization
def setup(bot):
    bot.add_cog(TestingCog(bot))