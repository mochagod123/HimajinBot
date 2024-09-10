import discord
from discord.ext import commands
import requests
import sys

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(music(bot))