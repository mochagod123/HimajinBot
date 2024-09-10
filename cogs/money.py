import discord
from discord.ext import commands
import asyncio
import sys
import random
from pymongo import MongoClient 

class MoneySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(MoneySystem(bot))