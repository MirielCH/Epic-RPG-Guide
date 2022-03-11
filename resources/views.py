# views.py
"""Contains global interaction views"""

from typing import Callable, List, Optional

import discord
from discord.ext import commands, pages

from resources import emojis, settings, strings


# --- Components ---
class TopicSelect(discord.ui.Select):
    """Topic Select"""
    def __init__(self, topics: dict, active_topic: str):
        options = []
        for topic in topics.keys():
            label = topic
            emoji = '🔹' if topic == active_topic else None
            options.append(discord.SelectOption(label=label, value=label, emoji=emoji))
        super().__init__(placeholder='Choose topic...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_topic = select_value
        embed = await self.view.topics[select_value]()
        self.view.clear_items()
        self.view.add_item(TopicSelect(self.view.topics, self.view.active_topic))
        await interaction.response.edit_message(embed=embed, view=self.view)


class PaginatorButton(discord.ui.Button):
    """Paginator button"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.blurple, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            self.view.active_page -= 1
            if self.view.active_page == 1:
                self.disabled = True
                for child in self.view.children:
                    if child.custom_id == 'next':
                        child.disabled = False
                        break
        elif self.custom_id == 'next':
            self.view.active_page += 1
            if self.view.active_page == len(self.view.pages):
                self.disabled = True
                for child in self.view.children:
                    if child.custom_id == 'prev':
                        child.disabled = False
                        break
        else:
            return
        for child in self.view.children:
            if child.custom_id == 'pages':
                child.label = f'{self.view.active_page}/{len(self.view.pages)}'
                break
        await interaction.response.edit_message(embed=self.view.pages[self.view.active_page-1], view=self.view)


class AreaSelect(discord.ui.Select):
    """Area select"""
    def __init__(self, areas: int):
        options = []
        for area in range(1, areas + 1):
            options.append(discord.SelectOption(label=f'Area {area}', value=str(area)))
        options.append(discord.SelectOption(label='<Abort>', value='abort'))
        super().__init__(placeholder='Choose area...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        if select_value == 'abort':
            self.view.value = select_value
            await interaction.message.edit(view=None)
            self.view.stop()
            return
        area = int(select_value)
        self.view.area = area
        embed = await self.view.function(self.view.prefix, area)
        await interaction.response.edit_message(embed=embed, view=self.view)


# --- Views ---
class AbortView(discord.ui.View):
    """View with an abort button.

    Also needs the interaction of the response with the view, so do AbortView.interaction = await ctx.respond('foo').

    Returns
    -------
    'abort' while button is active.
    'timeout' on timeout.
    None if nothing happened yet.
    """
    def __init__(self, ctx: discord.ApplicationContext, interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author

    @discord.ui.button(custom_id="abort", style=discord.ButtonStyle.grey, label='Abort')
    async def button_abort(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Abort button"""
        self.value = button.custom_id
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class TopicView(discord.ui.View):
    """View with a topic select.
    Also needs the interaction of the response with the view, so do AreaView.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    topics: Topics to select from - dict (description: function). The functions need to return an embed and have one
    argument (context)
    active_topic: Currently chosen topic
    function: Function that generates the embed, this will be called with every button press. The function needs to
        return an embed and have two arguments: prefix: str, page_no: int.

    Returns
    -------
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: discord.ApplicationContext, topics: dict, active_topic: str,
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.topics = topics
        self.active_topic = active_topic
        self.add_item(TopicSelect(self.topics, self.active_topic))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class PaginatorView(discord.ui.View):
    """Paginator view with three buttons (previous, page count, next).

    Also needs the interaction of the response with the view, so do AbortView.interaction = await ctx.respond('foo').

    Returns
    -------
    'timeout' on timeout.
    None if nothing happened yet.
    """
    def __init__(self, ctx: discord.ApplicationContext, pages = List[discord.Embed],
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.pages = pages
        self.active_page = 1
        self.add_item(PaginatorButton(custom_id='prev', label='◀', disabled=True, emoji=None))
        self.add_item(discord.ui.Button(custom_id="pages", style=discord.ButtonStyle.grey, disabled=True,
                                        label=f'1/{len(self.pages)}'))
        self.add_item(PaginatorButton(custom_id='next', label='▶', emoji=None))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class AreaView(discord.ui.View):
    """View with an area select.
    Also needs the interaction of the response with the view, so do AreaView.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    areas: Amount of areas the select will list. First area is always 1.
    function: Function that generates the embed, this will be called with every button press. The function needs to
        return an embed and have two arguments: prefix: str, page_no: int.

    Returns
    -------
    'abort' when abort was selected.
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: commands.Context, areas: int, function: Callable[[str, int], discord.Embed],
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=20)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.prefix = ctx.prefix
        self.function = function
        self.areas = areas
        self.area = 0
        self.add_item(AreaSelect(self.areas))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()