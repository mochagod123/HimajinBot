import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import json
import asyncio
from pymongo import MongoClient 

class mongos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(mongos(bot))