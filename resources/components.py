# views.py
"""Contains global interaction views"""

from typing import Optional

import discord

from content import areas, dungeons
from resources import strings


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
        for child in self.view.children.copy():
            if child.custom_id == 'select_area':
                self.view.remove_item(child)
                self.view.add_item(AreaCheckSelect(self.view.active_area))
            if child.custom_id == 'next':
                child.disabled = True if self.view.active_area == 21 else False
            if child.custom_id == 'prev':
                child.disabled = True if self.view.active_area == 1 else False
        await interaction.response.edit_message(embed=embed, view=self.view)


class AreaDungeonCheckSwitchButton(discord.ui.Button):
    """Button for area/dungeon check that switches to the opposite check"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message()
        if self.custom_id == 'dungeon-switch':
            area_dungeon = float(self.view.active_area)
            function = dungeons.command_dungeon_check
        else:
            area_dungeon = self.view.active_dungeon
            if area_dungeon.is_integer(): area_dungeon = int(self.view.active_dungeon)
            if area_dungeon == 15.2: area_dungeon = 15
            function = areas.command_area_check

        self.view.value = 'switched'
        self.view.stop()
        await function(self.view.bot, self.view.ctx, area_dungeon, switch_view=self.view)


class AreaDungeonGuideSwitchButton(discord.ui.Button):
    """Button for area/dungeon guide that switches to the opposite guide"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message()
        if self.custom_id == 'dungeon-switch':
            area_dungeon = float(self.view.active_area)
            function = dungeons.command_dungeon_guide
        else:
            area_dungeon = self.view.active_dungeon
            if area_dungeon.is_integer(): area_dungeon = int(self.view.active_dungeon)
            if area_dungeon == 15.2: area_dungeon = 15
            function = areas.command_area_guide

        self.view.value = 'switched'
        self.view.stop()
        await function(self.view.ctx, area_dungeon, switch_view=self.view)


class AreaCheckPaginatorButton(discord.ui.Button):
    """Paginator button for area check view"""
    def __init__(self, custom_id: str, label: str, disabled: bool = False, emoji: Optional[discord.PartialEmoji] = None):
        super().__init__(style=discord.ButtonStyle.grey, custom_id=custom_id, label=label, emoji=emoji,
                         disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.custom_id == 'prev':
            self.view.active_area -= 1
            if self.view.active_area == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    break
        elif self.custom_id == 'next':
            self.view.active_area += 1
            if self.view.active_area == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
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
        for child in self.view.children.copy():
            if child.custom_id == 'select_area':
                self.view.remove_item(child)
                self.view.add_item(AreaGuideSelect(self.view.active_area))
            if child.custom_id == 'next':
                child.disabled = True if self.view.active_area == 21 else False
            if child.custom_id == 'prev':
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
            if self.view.active_area == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    break
        elif self.custom_id == 'next':
            self.view.active_area += 1
            if self.view.active_area == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
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
        for child in self.view.children.copy():
            if child.custom_id == 'select_dungeon':
                self.view.remove_item(child)
                self.view.add_item(DungeonCheckSelect(self.view.active_dungeon))
            if child.custom_id == 'next':
                child.disabled = True if self.view.active_dungeon == 21 else False
            if child.custom_id == 'prev':
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
            if self.view.active_dungeon == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    break
        elif self.custom_id == 'next':
            if self.view.active_dungeon == 15:
                self.view.active_dungeon = 15.2
            elif self.view.active_dungeon == 15.2:
                self.view.active_dungeon = 16.0
            else:
                self.view.active_dungeon += 1
            if self.view.active_dungeon == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
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
        for child in self.view.children.copy():
            if child.custom_id == 'select_dungeon':
                self.view.remove_item(child)
                self.view.add_item(DungeonGuideSelect(self.view.active_dungeon))
            if child.custom_id == 'next':
                child.disabled = True if self.view.active_dungeon == 21 else False
            if child.custom_id == 'prev':
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
            if self.view.active_dungeon == 1: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'next':
                    child.disabled = False
                    break
        elif self.custom_id == 'next':
            if self.view.active_dungeon == 15:
                self.view.active_dungeon = 15.2
            elif self.view.active_dungeon == 15.2:
                self.view.active_dungeon = 16.0
            else:
                self.view.active_dungeon += 1
            if self.view.active_dungeon == 21: self.disabled = True
            for child in self.view.children:
                if child.custom_id == 'prev':
                    child.disabled = False
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