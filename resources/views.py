# views.py
"""Contains global interaction views"""

from typing import Callable, List, Optional, Union, Tuple

import discord

import database
from resources import settings, strings


# --- Functions ---
def get_area_button_labels(active_area: int) -> Tuple[str, str]:
    """Returns the labels for previous and next area buttons"""
    next_label = f'Area {active_area + 1} ▶'
    prev_label = f'◀ Area {active_area - 1}'
    if active_area == 1:
        prev_label = '◀'
    if active_area == 20:
        next_label = 'The TOP ▶'
    if active_area == 21:
       next_label = '▶'
    return (prev_label, next_label)


def get_dungeon_button_labels(active_dungeon: float) -> Tuple[str, str]:
    """Returns the labels for previous and next dungeon buttons"""
    if active_dungeon.is_integer(): active_dungeon = int(active_dungeon)
    next_label = f'Dungeon {active_dungeon + 1} ▶'
    prev_label = f'◀ Dungeon {active_dungeon - 1}'
    if active_dungeon == 1:
        prev_label = '◀'
    if active_dungeon == 15:
        next_label = f'Dungeon 15-2 ▶'
    if active_dungeon == 15.2:
        prev_label = '◀ Dungeon 15'
        next_label = f'Dungeon 16 ▶'
    if active_dungeon == 16:
        prev_label = '◀ Dungeon 15-2'
    if active_dungeon == 20:
        next_label = 'EPIC NPC fight ▶'
    if active_dungeon == 21:
       next_label = '▶'
    return (prev_label, next_label)


# --- Components ---
class AreaCheckSelect(discord.ui.Select):
    """Area check select"""
    def __init__(self, active_area: int):
        options = []
        for area_no in range(1,22):
            label = f'Area {area_no}' if area_no != 21 else 'The TOP'
            emoji = '🔹' if area_no == active_area else None
            options.append(discord.SelectOption(label=label, value=str(area_no), emoji=emoji))
        super().__init__(placeholder='Choose area...', min_values=1, max_values=1, options=options,
                         custom_id='select_area', row=0)

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_area = int(select_value)
        embed = await self.view.function(self.view.active_area, self.view.user_at, self.view.user_def,
                                         self.view.user_life)
        prev_label, next_label = get_area_button_labels(self.view.active_area)
        for child in self.view.children.copy():
            if child.custom_id == 'select_area':
                self.view.remove_item(child)
                self.view.add_item(AreaCheckSelect(self.view.active_area))
            if child.custom_id == 'next':
                child.label = next_label
                child.disabled = True if self.view.active_area == 21 else False
            if child.custom_id == 'prev':
                child.label = prev_label
                child.disabled = True if self.view.active_area == 1 else False
        await interaction.response.edit_message(embed=embed, view=self.view)


class AreaCheckPaginatorButton(discord.ui.Button):
    """Paginator button for area check view"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            self.view.active_area -= 1
            prev_label, next_label = get_area_button_labels(self.view.active_area)
            self.label = prev_label
            if self.view.active_area == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    child.label = next_label
                    break
        elif self.custom_id == 'next':
            self.view.active_area += 1
            prev_label, next_label = get_area_button_labels(self.view.active_area)
            self.label = next_label
            if self.view.active_area == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
                    child.label = prev_label
                    break
        else:
            return
        for child in self.view.children:
            if child.custom_id == 'select_area':
                options = []
                for area_no in range(1,22):
                    label = f'Area {area_no}' if area_no != 21 else 'The TOP'
                    emoji = '🔹' if area_no == self.view.active_area else None
                    options.append(discord.SelectOption(label=label, value=str(area_no), emoji=emoji))
                child.options = options
                break
        embed = await self.view.function(self.view.active_area, self.view.user_at, self.view.user_def,
                                         self.view.user_life)
        await interaction.response.edit_message(embed=embed, view=self.view)


class AreaGuideSelect(discord.ui.Select):
    """Area guide select"""
    def __init__(self, active_area: int):
        options = []
        for area_no in range(1,22):
            label = f'Area {area_no}' if area_no != 21 else 'The TOP'
            emoji = '🔹' if area_no == active_area else None
            options.append(discord.SelectOption(label=label, value=str(area_no), emoji=emoji))
        super().__init__(placeholder='Choose area...', min_values=1, max_values=1, options=options,
                         custom_id='select_area', row=0)

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_area = int(select_value)
        embed = await self.view.function(self.view.ctx, self.view.active_area, self.view.db_user, self.view.full_guide)
        prev_label, next_label = get_area_button_labels(self.view.active_area)
        for child in self.view.children.copy():
            if child.custom_id == 'select_area':
                self.view.remove_item(child)
                self.view.add_item(AreaGuideSelect(self.view.active_area))
            if child.custom_id == 'next':
                child.label = next_label
                child.disabled = True if self.view.active_area == 21 else False
            if child.custom_id == 'prev':
                child.label = prev_label
                child.disabled = True if self.view.active_area == 1 else False
        await interaction.response.edit_message(embed=embed, view=self.view)


class AreaGuidePaginatorButton(discord.ui.Button):
    """Paginator button for area guide view"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            self.view.active_area -= 1
            prev_label, next_label = get_area_button_labels(self.view.active_area)
            self.label = prev_label
            if self.view.active_area == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    child.label = next_label
                    break
        elif self.custom_id == 'next':
            self.view.active_area += 1
            prev_label, next_label = get_area_button_labels(self.view.active_area)
            self.label = next_label
            if self.view.active_area == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
                    child.label = prev_label
                    break
        else:
            return
        for child in self.view.children:
            if child.custom_id == 'select_area':
                options = []
                for area_no in range(1,22):
                    label = f'Area {area_no}' if area_no != 21 else 'The TOP'
                    emoji = '🔹' if area_no == self.view.active_area else None
                    options.append(discord.SelectOption(label=label, value=str(area_no), emoji=emoji))
                child.options = options
                break
        embed = await self.view.function(self.view.ctx, self.view.active_area, self.view.db_user, self.view.full_guide)
        await interaction.response.edit_message(embed=embed, view=self.view)


class DungeonCheckSelect(discord.ui.Select):
    """Dungeon check select"""
    def __init__(self, active_dungeon: float):
        options = []
        for dungeon_no in strings.DUNGEONS:
            label = f'Dungeon {dungeon_no:g}' if dungeon_no != 21 else 'EPIC NPC fight'
            label = label.replace('.','-')
            emoji = '🔹' if dungeon_no == active_dungeon else None
            options.append(discord.SelectOption(label=label, value=str(dungeon_no), emoji=emoji))
        super().__init__(placeholder='Choose dungeon...', min_values=1, max_values=1, options=options,
                         custom_id='select_dungeon', row=0)

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_dungeon = float(select_value)
        embed = await self.view.function(self.view.active_dungeon, self.view.user_at, self.view.user_def,
                                         self.view.user_life)
        prev_label, next_label = get_dungeon_button_labels(self.view.active_dungeon)
        for child in self.view.children.copy():
            if child.custom_id == 'select_dungeon':
                self.view.remove_item(child)
                self.view.add_item(DungeonCheckSelect(self.view.active_dungeon))
            if child.custom_id == 'next':
                child.label = next_label
                child.disabled = True if self.view.active_dungeon == 21 else False
            if child.custom_id == 'prev':
                child.label = prev_label
                child.disabled = True if self.view.active_dungeon == 1 else False
        await interaction.response.edit_message(embed=embed, view=self.view)


class DungeonCheckPaginatorButton(discord.ui.Button):
    """Paginator button for dungeon check view"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            if self.view.active_dungeon == 15.2:
                self.view.active_dungeon = 15.0
            elif self.view.active_dungeon == 16:
                self.view.active_dungeon = 15.2
            else:
                self.view.active_dungeon -= 1
            prev_label, next_label = get_dungeon_button_labels(self.view.active_dungeon)
            self.label = prev_label
            if self.view.active_dungeon == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    child.label = next_label
                    break
        elif self.custom_id == 'next':
            if self.view.active_dungeon == 15:
                self.view.active_dungeon = 15.2
            elif self.view.active_dungeon == 15.2:
                self.view.active_dungeon = 16.0
            else:
                self.view.active_dungeon += 1
            prev_label, next_label = get_dungeon_button_labels(self.view.active_dungeon)
            self.label = next_label
            if self.view.active_dungeon == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
                    child.label = prev_label
                    break
        else:
            return
        for child in self.view.children:
            if child.custom_id == 'select_dungeon':
                options = []
                for dungeon_no in strings.DUNGEONS:
                    label = f'Dungeon {dungeon_no:g}' if dungeon_no != 21 else 'EPIC NPC fight'
                    label = label.replace('.','-')
                    emoji = '🔹' if dungeon_no == self.view.active_dungeon else None
                    options.append(discord.SelectOption(label=label, value=str(dungeon_no), emoji=emoji))
                child.options = options
                break
        embed = await self.view.function(self.view.active_dungeon, self.view.user_at, self.view.user_def,
                                         self.view.user_life)
        await interaction.response.edit_message(embed=embed, view=self.view)


class DungeonGuideSelect(discord.ui.Select):
    """Dungeon guide select"""
    def __init__(self, active_dungeon: float):
        options = []
        for dungeon_no in strings.DUNGEONS:
            label = f'Dungeon {dungeon_no:g}' if dungeon_no != 21 else 'EPIC NPC fight'
            label = label.replace('.','-')
            emoji = '🔹' if dungeon_no == active_dungeon else None
            options.append(discord.SelectOption(label=label, value=str(dungeon_no), emoji=emoji))
        super().__init__(placeholder='Choose dungeon...', min_values=1, max_values=1, options=options,
                         custom_id='select_dungeon', row=0)

    async def callback(self, interaction: discord.Interaction):
        select_value = self.values[0]
        self.view.active_dungeon = float(select_value)
        embed = await self.view.function(self.view.active_dungeon)
        prev_label, next_label = get_dungeon_button_labels(self.view.active_dungeon)
        for child in self.view.children.copy():
            if child.custom_id == 'select_dungeon':
                self.view.remove_item(child)
                self.view.add_item(DungeonGuideSelect(self.view.active_dungeon))
            if child.custom_id == 'next':
                child.label = next_label
                child.disabled = True if self.view.active_dungeon == 21 else False
            if child.custom_id == 'prev':
                child.label = prev_label
                child.disabled = True if self.view.active_dungeon == 1 else False
        await interaction.response.edit_message(embed=embed, view=self.view)


class DungeonGuidePaginatorButton(discord.ui.Button):
    """Paginator button for dungeon guide view"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            if self.view.active_dungeon == 15.2:
                self.view.active_dungeon = 15.0
            elif self.view.active_dungeon == 16:
                self.view.active_dungeon = 15.2
            else:
                self.view.active_dungeon -= 1
            prev_label, next_label = get_dungeon_button_labels(self.view.active_dungeon)
            self.label = prev_label
            if self.view.active_dungeon == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    child.label = next_label
                    break
        elif self.custom_id == 'next':
            if self.view.active_dungeon == 15:
                self.view.active_dungeon = 15.2
            elif self.view.active_dungeon == 15.2:
                self.view.active_dungeon = 16.0
            else:
                self.view.active_dungeon += 1
            prev_label, next_label = get_dungeon_button_labels(self.view.active_dungeon)
            self.label = next_label
            if self.view.active_dungeon == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
                    child.label = prev_label
                    break
        else:
            return
        for child in self.view.children:
            if child.custom_id == 'select_dungeon':
                options = []
                for dungeon_no in strings.DUNGEONS:
                    label = f'Dungeon {dungeon_no:g}' if dungeon_no != 21 else 'EPIC NPC fight'
                    label = label.replace('.','-')
                    emoji = '🔹' if dungeon_no == self.view.active_dungeon else None
                    options.append(discord.SelectOption(label=label, value=str(dungeon_no), emoji=emoji))
                child.options = options
                break
        embed = await self.view.function(self.view.active_dungeon)
        await interaction.response.edit_message(embed=embed, view=self.view)


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
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            self.view.active_page -= 1
            if self.view.active_page == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    break
        elif self.custom_id == 'next':
            self.view.active_page += 1
            if self.view.active_page == len(self.view.pages): self.disabled = True
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


class CustomButton(discord.ui.Button):
    """Custom Button"""
    def __init__(self, style: discord.ButtonStyle, custom_id: str, label: Optional[str],
                 emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=style, custom_id=custom_id, label=label, emoji=emoji)

    async def callback(self, interaction: discord.Interaction):
        self.view.value = self.custom_id
        await interaction.message.edit(view=None)
        self.view.stop()


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


class AreaCheckView(discord.ui.View):
    """View with an area select that shows area checks on select.
    Also needs the interaction of the response with the view, so do AreaView.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    active_area: Currently chosen area. Use 21 if the top.
    user_at: AT of the player.
    user_def: DEF of the player.
    user_life: LIFE of the player.
    function: The function that returns the area check embed. The function needs to return an embed and have the
    following arguments: area_no: int, user_at: int, user_def: int, user_life: int

    Returns
    -------
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: discord.ApplicationContext, active_area: int, user_at: int, user_def: int, user_life: int,
                 function: Callable, interaction: Optional[Union[discord.Interaction, discord.Webhook]] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.ctx = ctx
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.active_area = active_area
        self.user_at = user_at
        self.user_def = user_def
        self.user_life = user_life
        self.function = function
        self.add_item(AreaCheckSelect(self.active_area))
        prev_disabled = True if active_area == 1 else False
        next_disabled = True if active_area == 21 else False
        prev_label, next_label = get_area_button_labels(self.active_area)
        self.add_item(AreaCheckPaginatorButton(custom_id='prev', label=prev_label, disabled=prev_disabled, emoji=None))
        self.add_item(AreaCheckPaginatorButton(custom_id='next', label=next_label, disabled=next_disabled, emoji=None))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class AreaGuideView(discord.ui.View):
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
    def __init__(self, ctx: discord.ApplicationContext, active_area: int, db_user: database.User, full_guide: bool,
                 function: Callable, interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.ctx = ctx
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.active_area = active_area
        self.db_user = db_user
        self.full_guide = full_guide
        self.function = function
        self.add_item(AreaGuideSelect(self.active_area))
        prev_disabled = True if active_area == 1 else False
        next_disabled = True if active_area == 21 else False
        prev_label, next_label = get_area_button_labels(active_area)
        self.add_item(AreaGuidePaginatorButton(custom_id='prev', label=prev_label, disabled=prev_disabled, emoji=None))
        self.add_item(AreaGuidePaginatorButton(custom_id='next', label=next_label, disabled=next_disabled, emoji=None))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class DungeonCheckView(discord.ui.View):
    """View with a dungeon select that shows dungeon checks on select.
    Also needs the interaction of the response with the view, so do DungeonCheckView.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    active_dungeon: Currently chosen dungeon. Use 21 if EPIC NPC fight.
    user_at: AT of the player.
    user_def: DEF of the player.
    user_life: LIFE of the player.
    function: The function that returns the area check embed. The function needs to return an embed and have the
    following arguments: dungeon_no: float, user_at: int, user_def: int, user_life: int

    Returns
    -------
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: discord.ApplicationContext, active_dungeon: float, user_at: int, user_def: int, user_life: int,
                 function: Callable, interaction: Optional[Union[discord.Interaction, discord.Webhook]] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.ctx = ctx
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.active_dungeon = active_dungeon
        self.user_at = user_at
        self.user_def = user_def
        self.user_life = user_life
        self.function = function
        self.add_item(DungeonCheckSelect(self.active_dungeon))
        prev_disabled = True if active_dungeon == 1 else False
        next_disabled = True if active_dungeon == 21 else False
        prev_label, next_label = get_dungeon_button_labels(self.active_dungeon)
        self.add_item(DungeonCheckPaginatorButton(custom_id='prev', label=prev_label, disabled=prev_disabled, emoji=None))
        self.add_item(DungeonCheckPaginatorButton(custom_id='next', label=next_label, disabled=next_disabled, emoji=None))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class DungeonGuideView(discord.ui.View):
    """View with a dungeon select that shows dungeon guides on select.
    Also needs the interaction of the response with the view, so do DungeonGuideView.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    active_dungeon: Currently chosen dungeon. Use 21 if EPIC NPC fight.
    function: The function that returns the dungeon embed, The function needs to return an embed and have the
    following arguments: dungeon_no: float

    Returns
    -------
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: discord.ApplicationContext, active_dungeon: float, function: Callable,
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.ctx = ctx
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.active_dungeon = active_dungeon
        self.function = function
        self.add_item(DungeonGuideSelect(self.active_dungeon))
        prev_disabled = True if active_dungeon == 1 else False
        next_disabled = True if active_dungeon == 21 else False
        prev_label, next_label = get_dungeon_button_labels(active_dungeon)
        self.add_item(DungeonGuidePaginatorButton(custom_id='prev', label=prev_label, disabled=prev_disabled, emoji=None))
        self.add_item(DungeonGuidePaginatorButton(custom_id='next', label=next_label, disabled=next_disabled, emoji=None))

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
    Also needs the interaction of the response with the view, so do TopicView.interaction = await ctx.respond('foo').

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
    def __init__(self, ctx: discord.ApplicationContext, pages: List[discord.Embed],
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


class ConfirmCancelView(discord.ui.View):
    """View with confirm and cancel button.

    Args: ctx, labels: Optional[list[str]]

    Also needs the message with the view, so do view.message = await ctx.interaction.original_message().
    Without this message, buttons will not be disabled when the interaction times out.

    Returns 'confirm', 'cancel' or None (if timeout/error)
    """
    def __init__(self, ctx: discord.ApplicationContext, labels: Optional[list[str]] = ['Yes','No'],
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.label_confirm = labels[0]
        self.label_cancel = labels[1]
        self.add_item(CustomButton(style=discord.ButtonStyle.green,
                                    custom_id='confirm',
                                    label=self.label_confirm))
        self.add_item(CustomButton(style=discord.ButtonStyle.red,
                                    custom_id='cancel',
                                    label=self.label_cancel))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            return False
        return True

    async def on_timeout(self):
        self.value = None
        if self.interaction is not None:
            if isinstance(self.interaction, discord.WebhookMessage):
                await self.interaction.edit(view=None)
            else:
                await self.interaction.edit_original_message(view=None)
        self.stop()


class FollowupCommandView(discord.ui.View):
    """Paginator view with a single button that calls another command and then removes itself.

    Also needs the interaction of the response with the view, so do
    FollowupCommandView.interaction = await ctx.respond('foo').

    Returns
    -------
    'timeout' on timeout.
    None if nothing happened yet.
    """
    def __init__(self, ctx: discord.ApplicationContext, label: str,
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.label = label
        self.active_page = 1
        self.add_item(CustomButton(custom_id='followup', label=label, emoji=None, style=discord.ButtonStyle.grey))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        if self.interaction is not None:
            if isinstance(self.interaction, discord.WebhookMessage):
                await self.interaction.edit(view=None)
            else:
                await self.interaction.edit_original_message(view=None)
        self.stop()