import discord
from discord.ext import commands
import requests
import sys
import openpyxl
import io
import asyncio

class excel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(excel(bot))