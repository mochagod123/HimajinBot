import discord
from discord.ext import commands
import requests
import sys
import asyncio

class search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(fallback='info', description = "Bot関連のコマンドです。")
    async def bots(self, ctx):
        await ctx.reply("Bot関連のコマンドです。")

    @bots.command(name = "ping", with_app_command = True, description = "Pingを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def ping(self, ctx):
        raw_ping = self.bot.latency
        ping = round(raw_ping * 1000)
        await ctx.reply(f"BotのPing値は{ping}msです。")

async def setup(bot):
    await bot.add_cog(search(bot))