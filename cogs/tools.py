import discord
from discord.ext import commands
import asyncio
import requests
import urllib
import io
import aiohttp
import sys
import logging
from contextlib import redirect_stdout
from io import BytesIO
from yt_dlp import YoutubeDL
import requests
from bs4 import BeautifulSoup
import re
import subprocess
from pyshorteners import Shortener
from googletrans import Translator
from threading import Thread
from pymongo import MongoClient
import json
from langdetect import detect
import random
import aiohttp

def download_bytesio(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': '-',
        'logger': logging.getLogger()
    }

    video = BytesIO()
    with redirect_stdout(video):
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    return video


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def afk(self, ctx, yoke: str):
        embed=discord.Embed(title="AFKになりました。", description=f"理由: {yoke}", color=0x00d5ff)
        await ctx.send(embed=embed)
        while True:
            numc = await self.bot.wait_for("message", timeout=None)
            try:
                if not numc.content == "" and numc.author == ctx.author:
                    embed=discord.Embed(title="AFKが解除されました。", description=f"理由: {yoke}", color=0x00d5ff)
                    await numc.channel.send(embed=embed)
                    break
            except:
                await ctx.reply("エラーが発生しました。")
                break

    @commands.hybrid_command(name = "2ch", with_app_command = True, description = "引用します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def nichan(self, ctx, 数字: int):
        try:
            try:
                await ctx.message.delete()
            except:
                pass
            if 数字 > 301:
                await ctx.send(f"300以内にしてください。")
                return
            lists = []
            async for ad in ctx.channel.history(limit=300):
                lists.append(ad.jump_url)

            for ads in range(len(lists)):
                if ads == 数字 - 1:
                    await ctx.send(f"[>>{数字}]({lists[ads]})")
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")


    @commands.hybrid_command(name = "shorturl", with_app_command = True, description = "短縮URLを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def shorturl(self, ctx, url: str):
        await ctx.defer()
        try:
            s = Shortener()
            shortened_link = s.tinyurl.short(url)
            embed = discord.Embed(title="短縮URL", description=f"{shortened_link}", color=discord.Color.green())
            await ctx.reply(embed=embed)
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

    @commands.hybrid_command(name = "qrcode", with_app_command = True, description = "QRコードを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def qrcode(self, ctx, url: str):
        await ctx.reply(f"https://api.qrserver.com/v1/create-qr-code/?data={url.replace("@", "")}&size=100x100")

    @commands.hybrid_command(name = "trans", with_app_command = True, description = "翻訳をします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def trans(self, ctx, テキストを入力: str):
        await ctx.defer()
        try:
            if detect(f"{テキストを入力}") == "ja":
                translator = Translator()
                translated = translator.translate(テキストを入力, src='ja', dest='en')
                embed = discord.Embed(title=f"{テキストを入力}の翻訳結果", description=f"{translated.text}", color=discord.Color.green())
                await ctx.reply(embed=embed)
                return
            translator = Translator()
            translated = translator.translate(テキストを入力, src=detect(f"{テキストを入力}"), dest='ja')
            embed = discord.Embed(title=f"{テキストを入力}の翻訳結果", description=f"{translated.text}", color=discord.Color.green())
            await ctx.reply(embed=embed)
            return
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

    @commands.hybrid_command(name = "download", with_app_command = True, description = "ダウンロードします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def yt_dl(self, ctx, url: str, youtube: bool, filename: str = None):
        if youtube:
            whname = f"ModoBot"
            ch_webhooks = await ctx.channel.webhooks()
            webhooks = discord.utils.get(ch_webhooks, name=whname)
            if webhooks is None:
                webhooks = await ctx.channel.create_webhook(name=f"{whname}")
            async with aiohttp.ClientSession() as session:
                async with session.post("http://127.0.0.1:5001/ytdl", json={"webhookurl": f"{webhooks.url}", "filename": f"{ctx.author.name}_{random.randint(1, 9999)}", "url": f"{url}"}) as response:
                    await ctx.send(await response.text())
            return
        else:
            await ctx.defer()
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    content = await response.read()
                    data = io.BytesIO(content)
                    if not filename == None:
                        await ctx.reply(file=discord.File(data, filename=f"{filename}"))
                    else:
                        await ctx.reply(file=discord.File(data, filename=f"File.mp4"))
    
    @commands.hybrid_command(name = "download_list", with_app_command = True, description = "ダウンロードの待機数を取得します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def yt_dl_list(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:5001/dlist") as response:
                await ctx.send(await response.text())
        return

async def setup(bot):
    await bot.add_cog(Tools(bot))