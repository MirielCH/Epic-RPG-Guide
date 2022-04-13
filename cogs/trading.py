# trading.py

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands

from content import trading
from resources import strings


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

    cmd_trade = SlashCommandGroup("trade", "Trade commands")

    @cmd_trade.command(name='guide', description='Trades you have to do before leaving areas')
    async def trade_guide(
        self,
        ctx: discord.ApplicationContext,
        area_no: Option(int, 'The area you want to see the trades for. Shows all areas if empty.', name='area',
                        min_value=1, max_value=21, choices=strings.CHOICES_AREA, default=None),
    ) -> None:
        """Trade guide"""
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


# Initialization
def setup(bot):
    bot.add_cog(TradingCog(bot))