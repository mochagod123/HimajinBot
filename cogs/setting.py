import discord
from discord.ext import commands
import requests
from pymongo import MongoClient
import asyncio
import json
from googletrans import Translator
import sys
from discord import Webhook
import aiohttp
import random
import re
import io
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance
from langdetect import detect

INVITE_PATTERN = re.compile(r"(https?://)?((ptb|canary)\.)?(discord\.(gg|io)|discord(app)?.com/invite)/[0-9a-zA-Z]+")

class setting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message_cmd(self, message):
        if message.author.bot:
            return

        client = MongoClient('mongodb://localhost:27017/')
        for mon in client["Main"]["TransChannel"].find():
            if mon["IDs"] == f"{message.channel.id}":
                try:
                    if detect(f"{message.content}") == "ja":
                        translator = Translator()
                        translated = translator.translate(message.content.replace("@", ""), src='ja', dest='en')
                        embed = discord.Embed(title=f"{message.content.replace("@", "")}の翻訳結果", description=f"{translated.text}", color=discord.Color.green())
                        await message.channel.send(embed=embed)
                    else:
                        translator = Translator()
                        translated = translator.translate(message.content.replace("@", ""), src=detect(f"{message.content}"), dest='ja')
                        embed = discord.Embed(title=f"{message.content.replace("@", "")}の翻訳結果", description=f"{translated.text}", color=discord.Color.green())
                        await message.channel.send(embed=embed)
                except:
                    continue

    @commands.Cog.listener("on_message")
    async def on_message_hiroyuki(self, message):
        if message.author.bot:
            return

        client = MongoClient('mongodb://localhost:27017/')
        for mon in client["Main"]["Hiroyuki"].find():
            if mon["IDs"] == f"{message.channel.id}":
                try:
                    await asyncio.sleep(0.5)
                    meigen = [f"嘘を嘘と見抜けない人は、{message.guild.name}を使うのは難しいでしょう", "それってあなたの感想ですよね", "日本人はモラルが高いのではなく、同調圧力に弱いだけ。", "『こういうときは、こうしておこう』というルールを先に決めます", "それって明らかではないですよね？"]
                    whname = f"ModoBot-Hiroyuki"
                    ch_webhooks = await message.channel.webhooks()
                    webhooks = discord.utils.get(ch_webhooks, name=whname)
                    if webhooks is None:
                        webhooks = await message.channel.create_webhook(name=f"{whname}")
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(webhooks.url, session=session)
                        await webhook.send(f"{random.choice(meigen)}", username=f"ひろゆき", avatar_url=f"https://dol.ismcdn.jp/mwimgs/d/5/1200/img_d50898395a8e97cc62f70681d2bd541f381966.jpg")
            
                except:
                    continue
                    
    @commands.Cog.listener("on_message")
    async def on_message_yutas(self, message):
        if message.author.bot:
            return

        client = MongoClient('mongodb://localhost:27017/')
        for mon in client["Main"]["Yuta"].find():
            if mon["IDs"] == f"{message.channel.id}":
                try:
                    await asyncio.sleep(0.5)
                    meigen = ["はちみつちょうだい", "秘薬ください", "よろしく", "これいこ", "はやくいこ(ﾁﾘﾝﾁﾘﾝﾁﾘﾝﾁﾘﾝ)", "しっぽきって やくめでしょ", "かいぞうクエちょうだい", "これうごくやつ？", "ふざきんな!!111"]
                    icon = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-ZkkfRJ1eBaRHYa19He8-NpYntiUSf00eCQ&s", "https://www.4gamer.net/games/245/G024582/20141118074/TN/004.jpg"]
                    whname = f"ModoBot-Yuta"
                    ch_webhooks = await message.channel.webhooks()
                    webhooks = discord.utils.get(ch_webhooks, name=whname)
                    if webhooks is None:
                        webhooks = await message.channel.create_webhook(name=f"{whname}")
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(webhooks.url, session=session)
                        await webhook.send(f"{random.choice(meigen)}", username=f"ゆうた", avatar_url=f"{random.choice(icon)}")
            
                except:
                    continue

    @commands.Cog.listener("on_message")
    async def on_message_automod(self, message):
        if message.author.bot:
            return

        if (type(message.channel) == discord.DMChannel):
            return

        client = MongoClient('mongodb://localhost:27017/')
        for mon in client["Main"]["Invcheck"].find():
            if mon["IDs"] == f"{message.guild.id}":
                try:
                    await asyncio.sleep(1)
                    if INVITE_PATTERN.search(message.content):
                        if message.author.guild_permissions.administrator:
                            continue
                        await message.delete()
                        await message.author.kick()
                        await message.channel.send(
                            message.author.mention,
                            embed=discord.Embed(title="招待リンクが検出されました。\n5秒後に削除します。"),
                            mention_author=True,
                            delete_after=5,
                        )
                except:
                    continue
                    
        for mon in client["Main"]["BlockLongMSG"].find():
            if mon["IDs"] == f"{message.channel.id}":
                try:
                    await asyncio.sleep(1)
                    if len(message.content) >= 70:
                        if message.author.guild_permissions.administrator:
                            continue
                        await message.delete()
                        await message.channel.send(
                            message.author.mention,
                            embed=discord.Embed(title="長いメッセージが検出されました。\n5秒後に削除します。"),
                            mention_author=True,
                            delete_after=5,
                        )
                except:
                    continue

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def transch(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["TransChannel"].delete_one(add_datad)
                add_data = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["TransChannel"].insert_one(add_data)
                embed=discord.Embed(title="自動翻訳", description=f"自動翻訳を有効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["TransChannel"].delete_one(add_datad)
                embed=discord.Embed(title="自動翻訳", description=f"自動翻訳を無効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def joinhiro(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Hiroyuki"].delete_one(add_datad)
                add_data = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Hiroyuki"].insert_one(add_data)
                embed=discord.Embed(title="ひろゆき", description=f"ひろゆきを有効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Hiroyuki"].delete_one(add_datad)
                embed=discord.Embed(title="ひろゆき", description=f"ひろゆきを無効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")
            
    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def joinyuta(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Yuta"].delete_one(add_datad)
                add_data = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Yuta"].insert_one(add_data)
                embed=discord.Embed(title="ゆうた・ゆうき", description=f"ゆうた・ゆうきを有効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Yuta"].delete_one(add_datad)
                embed=discord.Embed(title="ゆうた・ゆうき", description=f"ゆうた・ゆうきを無効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def invcheck(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.guild.id}"}
                client['Main']["Invcheck"].delete_one(add_datad)
                add_data = {f"IDs": f"{ctx.guild.id}"}
                client['Main']["Invcheck"].insert_one(add_data)
                embed=discord.Embed(title="招待リンクチェック", description=f"招待リンクチェックを有効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.guild.id}"}
                client['Main']["Invcheck"].delete_one(add_datad)
                embed=discord.Embed(title="招待リンクチェック", description=f"招待リンクチェックを無効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def discmd(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["DisableCMD"].delete_one(add_datad)
                add_data = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["DisableCMD"].insert_one(add_data)
                embed=discord.Embed(title="コマンド無効チャンネル", description=f"コマンド無効チャンネルを有効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["DisableCMD"].delete_one(add_datad)
                embed=discord.Embed(title="コマンド無効チャンネル", description=f"コマンド無効チャンネルを無効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def blom(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["BlockLongMSG"].delete_one(add_datad)
                add_data = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["BlockLongMSG"].insert_one(add_data)
                embed=discord.Embed(title="長いめっせーじが無効なチャンネル", description=f"長いめっせーじが無効なチャンネルを有効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["BlockLongMSG"].delete_one(add_datad)
                embed=discord.Embed(title="長いめっせーじが無効なチャンネル", description=f"長いめっせーじが無効なチャンネルを無効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def enads(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["TaskAds"].delete_one(add_datad)
                client['Main']["TaskAds"].insert_one(add_datad)
                embed=discord.Embed(title="広告を有効化しました。", description=f"ここには、定期的に、広告が配信されます。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["TaskAds"].delete_one(add_datad)
                embed=discord.Embed(title="広告を無効かしました。", description=f"ここに、定期的に、広告が配信されなくなりました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def news(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["News"].delete_one(add_datad)
                client['Main']["News"].insert_one(add_datad)
                embed=discord.Embed(title="ニュースを配信するチャンネル", description=f"ここには、定期的に、ニュースが配信されます。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["News"].delete_one(add_datad)
                embed=discord.Embed(title="ニュースを配信するチャンネル", description=f"ここに、定期的に、ニュースが\n配信されなくなりました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def tenki(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Tenki"].delete_one(add_datad)
                client['Main']["Tenki"].insert_one(add_datad)
                embed=discord.Embed(title="天気を配信するチャンネル", description=f"ここには、定期的に、天気が配信されます。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Tenki"].delete_one(add_datad)
                embed=discord.Embed(title="天気を配信するチャンネル", description=f"ここに、定期的に、天気が\n配信されなくなりました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")
            
    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def enagban(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.guild.id}"}
                client['Main']["GBAN"].delete_one(add_datad)
                add_data = {f"IDs": f"{ctx.guild.id}"}
                client['Main']["GBAN"].insert_one(add_data)
                embed=discord.Embed(title="GBANを有効", description=f"GBANを有効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.guild.id}"}
                client['Main']["GBAN"].delete_one(add_datad)
                embed=discord.Embed(title="GBANを無効", description=f"GBANを無効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

async def setup(bot):
    await bot.add_cog(setting(bot))