# trading.py

import re

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

import database
from cache import messages
from content import trading
from resources import settings, strings


TRADECALC_MATERIALS = [
    'apple',
    'normie fish',
    'ruby',
    'wooden log',
]

class TradingCog(commands.Cog):
    """Cog with trading commands"""
    def __init__(self, bot):
        self.bot = bot

    # Commands
    cmd_trade = SlashCommandGroup("trade", "Trade guides and calculator")

    @cmd_trade.command(name='guide', description='Recommended trades before leaving areas.')
    async def trade_guide(
        self,
        ctx: discord.ApplicationContext,
        area_no: Option(int, 'The area you want to see the trades for. Shows all areas if empty.', name='area',
                        min_value=0, max_value=21, choices=strings.CHOICES_AREA, default=None),
    ) -> None:
        """Trade summary"""
        await trading.command_trade_guide(ctx, area_no)

    @cmd_trade.command(name='rates', description='All trade rates in one handy overview')
    async def trade_rates(self, ctx: discord.ApplicationContext) -> None:
        """Trade rates"""
        await trading.command_trade_rates(ctx)

    @cmd_trade.command(name='calculator', description='Calculates materials after trading')
    async def trade_calculator(
        self,
        ctx: discord.ApplicationContext,
        area_no: Option(int, 'The area you have the materials in', name='area', min_value=0,
                        max_value=21, choices=strings.CHOICES_AREA),
        material: Option(str, 'The material you currently have', choices=TRADECALC_MATERIALS),
        amount: Option(str, 'The amount you currently have')
    ) -> None:
        """Trade calculator"""
        await trading.command_trade_calculator(ctx, area_no, material, amount)

    # Events
    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message) -> None:
        """Runs when a message is edited in a channel."""
        if message_before.pinned != message_after.pinned: return
        for row in message_after.components:
            for component in row.children:
                if component.disabled:
                    return
        await self.on_message(message_after)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Runs when a message is sent in a channel."""
        if message.author.id not in [settings.EPIC_RPG_ID, settings.TESTY_ID]: return
        if not message.embeds: return
        embed: discord.Embed = message.embeds[0]
        embed_author = icon_url = ''
        if embed.author:
            embed_author = embed.author.name
            icon_url = embed.author.icon_url


        # Quick trade calculator
        search_strings = [
            "— inventory", #All languages
        ]
        if any(search_string in embed_author.lower() for search_string in search_strings):
            if icon_url == embed.Empty: return
            user_id = user_name = user_command_message = None
            embed_user = None
            if message.interaction is not None: return
            user_id_match = re.search(r"avatars\/(.+?)\/", icon_url)
            if user_id_match:
                user_id = int(user_id_match.group(1))
            user_name_match = re.search(r"^(.+?) — ", embed_author)
            if user_name_match:
                user_name = user_name_match.group(1)
            if not user_name_match and not user_id_match:
                await database.log_error(
                    f'Found neither user_id nor user name in inventory message.\n'
                    f'Embed author: {embed_author}\n'
                )
                return
            user_command_message = await messages.find_message(
                message.channel.id, strings.REGEX_COMMAND_QUICK_TRADE, user_id=user_id, user_name=user_name
            )
            if user_command_message is None: return
            interaction_user = user_command_message.author
            if embed_user is not None:
                if interaction_user != embed_user: return
            area_match = re.search(r'(?:\bi\b|\binv\b|\binventory\b)\s+\b(?:(\d\d?|top))\b',
                                   user_command_message.content.lower())
            area_no = int(area_match.group(1).replace('top','21'))
            if not 1 <= area_no <= 21: return
            try:
                user_settings: database.User = await database.get_user(interaction_user.id)
            except database.FirstTimeUser:
                user_settings: database.User = await database.get_user(interaction_user.id)
            if not user_settings.quick_trade_enabled: return
            await trading.command_quick_trade_calculator(message, area_no, interaction_user)

# Initialization
def setup(bot):
    bot.add_cog(TradingCog(bot))