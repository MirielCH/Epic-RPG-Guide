# views.py
"""Contains global interaction views"""

from typing import Callable, List, Optional, Union

import discord
from discord.ext import commands

import database
from resources import components, emojis, settings, strings


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
        if interaction.user.id != self.user.id:
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
    def __init__(self, bot: discord.Bot, ctx: discord.ApplicationContext, active_area: int, user_at: int,
                 user_def: int, user_life: int, function_embed: Callable, function_area_check: Callable,
                 function_dungeon_check: Callable,
                 interaction: Optional[Union[discord.Interaction, discord.WebhookMessage]] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.bot = bot
        self.ctx = ctx
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.active_area = active_area
        self.user_at = user_at
        self.user_def = user_def
        self.user_life = user_life
        self.function_embed = function_embed
        self.function_area_check = function_area_check
        self.function_dungeon_check = function_dungeon_check
        self.add_item(components.AreaCheckSelect(self.active_area))
        prev_disabled = True if active_area == 1 else False
        next_disabled = True if active_area == 21 else False
        self.add_item(components.AreaCheckPaginatorButton(custom_id='prev', label='◀', disabled=prev_disabled,
                                                          emoji=None))
        self.add_item(components.AreaCheckPaginatorButton(custom_id='next', label='▶', disabled=next_disabled,
                                                          emoji=None))
        self.add_item(components.AreaDungeonCheckSwitchButton(custom_id="dungeon-switch", label='↪ Dungeon check',
                                                              emoji=None))


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
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
                 function_embed: Callable, function_area_guide: Callable, function_dungeon_guide: Callable,
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.ctx = ctx
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.active_area = active_area
        self.db_user = db_user
        self.full_guide = full_guide
        self.function_embed = function_embed
        self.function_area_guide = function_area_guide
        self.function_dungeon_guide = function_dungeon_guide
        self.add_item(components.AreaGuideSelect(self.active_area))
        prev_disabled = True if active_area == 1 else False
        next_disabled = True if active_area == 21 else False
        self.add_item(components.AreaGuidePaginatorButton(custom_id='prev', label='◀', disabled=prev_disabled,
                                                          emoji=None))
        self.add_item(components.AreaGuidePaginatorButton(custom_id='next', label='▶', disabled=next_disabled,
                                                          emoji=None))
        self.add_item(components.AreaDungeonGuideSwitchButton(custom_id="dungeon-switch", label='↪ Dungeon guide',
                                                              emoji=None))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user.id:
            from resources import logs
            logs.logger.error(
                f'--- Mismatched user ---\n'
                f'Interaction user: {interaction.user.name} ({interaction.user.id})\n'
                f'Self interaction user: {self.interaction.user.name} ({self.interaction.user.id})\n'
                f'Self user: {self.user.name} ({self.user.id})\n'
                f'Context user: {self.ctx.author.name} ({self.ctx.author.id})\n'
                f'DB user: {self.db_user.user_id}\n'
            )
            #await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            #return False
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
    def __init__(self, bot: discord.Bot, ctx: discord.ApplicationContext, active_dungeon: float, user_at: int,
                 user_def: int, user_life: int, function_embed: Callable, function_area_check: Callable,
                 function_dungeon_check: Callable,
                 interaction: Optional[Union[discord.Interaction, discord.Webhook]] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.bot = bot
        self.ctx = ctx
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.active_dungeon = active_dungeon
        self.user_at = user_at
        self.user_def = user_def
        self.user_life = user_life
        self.function_embed = function_embed
        self.function_area_check = function_area_check
        self.function_dungeon_check = function_dungeon_check
        self.add_item(components.DungeonCheckSelect(self.active_dungeon))
        prev_disabled = True if active_dungeon == 1 else False
        next_disabled = True if active_dungeon == 21 else False
        self.add_item(components.DungeonCheckPaginatorButton(custom_id='prev', label='◀', disabled=prev_disabled,
                                                             emoji=None))
        self.add_item(components.DungeonCheckPaginatorButton(custom_id='next', label='▶', disabled=next_disabled,
                                                             emoji=None))
        self.add_item(components.AreaDungeonCheckSwitchButton(custom_id="area-switch", label='↪ Area check',
                                                              emoji=None))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
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
    def __init__(self, ctx: discord.ApplicationContext, active_dungeon: float, function_embed: Callable,
                 function_area_guide: Callable, function_dungeon_guide: Callable,
                 db_user: Optional[database.User] = None, full_guide: Optional[bool] = None,
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.ctx = ctx
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.active_dungeon = active_dungeon
        self.function_embed = function_embed
        self.function_area_guide = function_area_guide
        self.function_dungeon_guide = function_dungeon_guide
        self.db_user = db_user
        self.full_guide = full_guide
        self.add_item(components.DungeonGuideSelect(self.active_dungeon))
        prev_disabled = True if active_dungeon == 1 else False
        next_disabled = True if active_dungeon == 21 else False
        self.add_item(components.DungeonGuidePaginatorButton(custom_id='prev', label='◀', disabled=prev_disabled,
                                                             emoji=None))
        self.add_item(components.DungeonGuidePaginatorButton(custom_id='next', label='▶', disabled=next_disabled,
                                                             emoji=None))
        self.add_item(components.AreaDungeonGuideSwitchButton(custom_id="area-switch", label='↪ Area guide',
                                                              emoji=None))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
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
    topics: Topics to select from - dict (description: function). The functions need to return an embed and have no
    arguments
    active_topic: Currently chosen topic

    Returns
    -------
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: discord.ApplicationContext, topics: dict, active_topic: str,
                 placeholder: Optional[str] = 'Choose topic ...',
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.topics = topics
        self.active_topic = active_topic
        self.placeholder = placeholder
        self.add_item(components.TopicSelect(self.topics, self.active_topic, self.placeholder))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
            #await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            #return False
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
        self.add_item(components.PaginatorButton(custom_id='prev', label='◀', disabled=True, emoji=None))
        self.add_item(discord.ui.Button(custom_id="pages", style=discord.ButtonStyle.grey, disabled=True,
                                        label=f'1/{len(self.pages)}'))
        self.add_item(components.PaginatorButton(custom_id='next', label='▶', emoji=None))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
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
        self.add_item(components.CustomButton(style=discord.ButtonStyle.green,
                                              custom_id='confirm',
                                              label=self.label_confirm))
        self.add_item(components.CustomButton(style=discord.ButtonStyle.red,
                                              custom_id='cancel',
                                              label=self.label_cancel))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            return False
        return True

    async def on_timeout(self):
        self.value = None
        if self.interaction is not None:
            try:
                if isinstance(self.interaction, discord.WebhookMessage):
                    await self.interaction.edit(view=None)
                else:
                    await self.interaction.edit_original_response(view=None)
            except discord.errors.NotFound:
                pass
        self.stop()


class FollowupCommandView(discord.ui.View):
    """Followup view with a single button that calls another command and then removes itself.

    Also needs the interaction of the response with the view, so do
    FollowupCommandView.interaction = await ctx.respond('foo').

    Returns
    -------
    'timeout' on timeout.
    None if nothing happened yet.
    """
    def __init__(self, user: discord.User, label: str,
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = user
        self.label = label
        self.active_page = 1
        self.add_item(components.CustomButton(custom_id='followup', label=label, emoji=None,
                                              style=discord.ButtonStyle.grey))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
        return True

    async def on_timeout(self) -> None:
        self.stop()


class FollowupCraftingCalculatorView(discord.ui.View):
    """Followup view with a single button that calls the CraftinCalculatorAmountModal and then removes itself.

    Also needs the interaction of the response with the view, so do
    FollowupCommandView.interaction = await ctx.respond('foo').

    Returns
    -------
    'timeout' on timeout.
    None if nothing happened yet.
    """
    def __init__(self, ctx: discord.ApplicationContext, item_name: str, item_emoji: str, label: str,
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.ctx = ctx
        self.user = ctx.author
        self.item_name = item_name
        self.item_emoji = item_emoji
        self.add_item(components.CraftingRecalculateButton(custom_id='craft', label=label))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        if self.interaction is not None:
            try:
                if isinstance(self.interaction, discord.WebhookMessage):
                    await self.interaction.edit(view=None)
                else:
                    await self.interaction.edit_original_response(view=None)
            except discord.errors.NotFound:
                pass
        self.stop()


class ComplainView(discord.ui.View):
    """View with button to complain. Because yes.

    Also needs the message of the response with the view, so do ComplainView.message = await ctx.send('foo').

    Returns
    -------
    'timeout' on timeout.
    None if nothing happened yet.
    """
    def __init__(self, ctx: commands.Context, message: Optional[discord.Message] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.ctx = ctx
        self.message = message

    @discord.ui.button(custom_id="complain", style=discord.ButtonStyle.grey, label='Complain')
    async def button_complain(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Complain button"""
        response = (
            f'What the hell is this nonsense, where are my old commands??!!!??\n\n'
            f'**THE DEV IS A BLOODY GOBSHITE!** {emojis.SAD_ANGRY}\n\n'
            f'**BRING ME THE MANAGER!** {emojis.PEPE_ANGRY_POLICE}\n\n'
            f'**I DEMAND MY MONEY BACK!** {emojis.PEPE_TABLESLAM}\n\n'
        )
        embed = discord.Embed(
            color = settings.EMBED_COLOR,
            title = f'{self.ctx.author.name} IS COMPLAINING'.upper(),
            description = response
        )
        image = discord.File(settings.IMG_CRANKY, filename='cranky.png')
        image_url = 'attachment://cranky.png'
        embed.set_thumbnail(url=image_url)
        self.disable_all_items()
        await self.message.edit(view=self)
        await interaction.response.send_message(embed=embed, file=image)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.ctx.author.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        await self.message.edit(view=None)
        self.stop()


class TimeJumpCalculatorView(discord.ui.View):
    """View with interactions to manually set stats, gear and enchants in the time jump score calculator.

    Also needs the interaction of the response with the view, so do view.interaction = await ctx.respond('foo').

    Returns
    -------
    None
    """
    def __init__(self, ctx: Union[commands.Context, discord.ApplicationContext], area_no: int, inventory: str,
                 profile_data: dict, boosts_data: dict, option_inventory: str, option_stats: str, all_items: dict,
                 embed_function: callable, interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.ctx = ctx
        self.user = ctx.author
        self.interaction = interaction
        self.area_no = area_no
        self.inventory = inventory
        self.profile_data = profile_data
        self.boosts_data = boosts_data
        self.option_inventory = option_inventory
        self.option_stats = option_stats
        self.all_items = all_items
        self.embed_function = embed_function
        self.add_item(components.TimeJumpCalculatorGearSelect(gear_type='sword', all_items=all_items,
                                                              placeholder='Change sword', profile_data=profile_data))
        self.add_item(components.TimeJumpCalculatorGearSelect(gear_type='armor', all_items=all_items,
                                                              placeholder='Change armor', profile_data=profile_data))
        self.add_item(components.TimeJumpCalculatorEnchantSelect(enchant_type='sword', placeholder='Change sword enchant'))
        self.add_item(components.TimeJumpCalculatorEnchantSelect(enchant_type='armor', placeholder='Change armor enchant'))
        self.add_item(components.TimeJumpCalculatorChangeStatsButton(custom_id='change_stats', label='Change stats'))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
        return True

    async def on_timeout(self) -> None:
        if self.interaction is not None:
            try:
                if isinstance(self.interaction, discord.WebhookMessage):
                    await self.interaction.edit(view=None)
                else:
                    await self.interaction.edit_original_response(view=None)
            except discord.errors.NotFound:
                pass
        self.stop()


class DropChanceCalculatorView(discord.ui.View):
    """View with a drop type select.
    Also needs the interaction of the response with the view, so do view.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    drop_types: Drop types to select from - list[str]
    embed_function: function that returns the embed. Needs the arguments active_drop_type, timetravel, horse_tier.
    active_drop_type: Currently chosen drop type

    Returns
    -------
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: discord.ApplicationContext, embed_function: Callable, drop_types: List[str],
                 active_drop_type: str, timetravel: int, horse_data: dict, mob_world_boost: bool,
                 lootbox_world_boost: bool, mob_boost_percentage: int,
                 lootbox_boost_percentage: int, vampire_teeth_artifact: bool, claus_belt_artifact: bool,
                 placeholder: Optional[str] = 'Choose drop type ...',
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.embed_function = embed_function
        self.drop_types = drop_types
        self.active_drop_type = active_drop_type
        self.timetravel = timetravel
        self.horse_data = horse_data
        self.placeholder = placeholder
        self.mob_world_boost = mob_world_boost
        self.lootbox_world_boost = lootbox_world_boost
        self.mob_boost_percentage = mob_boost_percentage
        self.lootbox_boost_percentage = lootbox_boost_percentage
        self.claus_belt_artifact = claus_belt_artifact
        self.vampire_teeth_artifact = vampire_teeth_artifact
        self.add_item(components.DropTypeSelect(self.drop_types, self.active_drop_type, self.placeholder))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class PetTierView(discord.ui.View):
    """View with a pet tier select.
    Also needs the interaction of the response with the view, so do view.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    pet_tier: Currently chosen pet tier

    Returns
    -------
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: discord.ApplicationContext, embed_function: callable, tt_no: int, pet_tier: int,
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.embed_function = embed_function
        self.tt_no = tt_no
        self.pet_tier = pet_tier
        self.add_item(components.PetTierSelect(self.pet_tier, 'Choose pet tier ...'))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class ItemView(discord.ui.View):
    """View with an item select.
    Also needs the interaction of the response with the view, so do TopicView.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    items: Items to select from - dict (description: [emoji, function]). The functions need to return an embed and have no
    arguments
    active_item: Currently chosen item

    Returns
    -------
    'timeout if timed out.
    None otherwise.
    """
    def __init__(self, ctx: discord.ApplicationContext, items: dict, active_item: str,
                 placeholder: Optional[str] = 'Choose item ...',
                 interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.items = items
        self.active_item = active_item
        self.placeholder = placeholder
        self.add_item(components.ItemSelect(self.items, self.active_item, self.placeholder))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        #if interaction.user.id != self.user.id:
         #   await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
          #  return False
        return True

    async def on_timeout(self) -> None:
        self.value = 'timeout'
        self.stop()


class SettingsUserView(discord.ui.View):
    """View with a all components to manage user settings.
    Also needs the interaction of the response with the view, so do view.interaction = await ctx.respond('foo').

    Arguments
    ---------
    ctx: Context.
    bot: Bot.
    user_settings: User object with the settings of the user.
    embed_function: Function that returns the settings embed. The view expects the following arguments:
    - bot: Bot
    - user_settings: User object with the settings of the user

    Returns
    -------
    None

    """
    def __init__(self, ctx: discord.ApplicationContext, user_settings: database.User,
                 embed_function: callable, interaction: Optional[discord.Interaction] = None):
        super().__init__(timeout=settings.INTERACTION_TIMEOUT)
        self.ctx = ctx
        self.value = None
        self.interaction = interaction
        self.user = ctx.author
        self.user_settings = user_settings
        self.embed_function = embed_function
        self.add_item(components.ManageUserSettingsSelect(self))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(strings.MSG_INTERACTION_ERROR, ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        if isinstance(self.interaction, discord.WebhookMessage):
            await self.interaction.edit(view=None)
        else:
            await self.interaction.edit_original_response(view=None)
        self.stop()