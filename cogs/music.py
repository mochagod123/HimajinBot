import discord
from discord.ext import commands
import requests
import random
import sys
import glob
import io
import aiohttp        
import aiofiles
import asyncio
import os
import datetime
import pyttsx3

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name = "join", with_app_command = True, description = "VCに参加します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def join(self, ctx):
        await ctx.send("接続しました。")
        await ctx.author.voice.channel.connect()

    @commands.hybrid_command(name = "leave", with_app_command = True, description = "VCから退出します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def leave(self, ctx):
        await ctx.send("退出しました。")
        await ctx.guild.voice_client.disconnect()

    @commands.hybrid_command(name = "musicquiz", with_app_command = True, description = "音楽をランダムに流します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def musicquiz(self, ctx):
        list = glob.glob('Music/*.mp3')
        musics = random.choice(list)
        await ctx.send("再生を開始します。")
        ctx.guild.voice_client.play(discord.FFmpegPCMAudio(musics))

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def addquiz(self, ctx):
        mu_byte = ctx.message.attachments[0].url
        now = datetime.datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.get(mu_byte) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f'Music/{now.strftime('%Y%m%d_%H%M%S')}.mp3', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        await ctx.send("クイズの音楽を追加しました。")

async def setup(bot):
    await bot.add_cog(music(bot))