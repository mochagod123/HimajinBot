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

        client = MongoClient('mongodb://localhost:27017/')
        for mon in client["Main"]["Kana"].find():
            if mon["IDs"] == f"{message.channel.id}":
                try:
                    tokenjson = open('../token.json', 'r')
                    tokens = json.load(tokenjson)
                    whname = f"ModoBot"
                    ch_webhooks = await message.channel.webhooks()
                    webhooks = discord.utils.get(ch_webhooks, name=whname)
                    if webhooks is None:
                        webhooks = await message.channel.create_webhook(name=f"{whname}")
                    async with aiohttp.ClientSession() as session:
                        async with session.post("https://kana.renorari.net/api/v2/chat", json={"message":f"{message.content}","user":{"id":f"{tokens["kanaid"]}","password":f"{tokens["kanapass"]}"},"character_name":"discord","custom_character":"おは#100#5-9#おはよう!!,おっはー！,おはよーぅ!#null#{}\nおは#100#10-17#おそよう,今お昼だよ、おはよ#null#{}\nおは#100#18-4#昼夜逆転♫おはよ!,私はもう少しで寝ますよ?おはよ#null#{}"}) as response:
                            kkk = await response.text()
                            async with aiohttp.ClientSession() as session:
                                webhook = Webhook.from_url(webhooks.url, session=session)
                                await webhook.send(f"{json.loads(kkk)["reply"].replace("もどっぐ", f"{message.author.display_name}")}", username=f"かなちゃん", avatar_url=f"https://yt3.googleusercontent.com/Q2yN9GaRPKbMcRVthn2_FegI5PAvfA9DLNZK-pzLybxWw5j9Emdh_hXGMuSqqIKWjmcNmSwEfOY=s900-c-k-c0x00ffffff-no-rj")
            
                except:
                    continue

        for mon in client["Main"]["Yuda"].find():
            if mon["IDs"] == f"{message.channel.id}":
                try:
                    msg = "None"
                    mmm = message.content
                    if "こんにちは" in mmm:
                        msg = f"こんにちは。。{message.author.name}さん。。"
                    elif "使えない" in mmm:
                        msg = f"無料なんだから使わなきゃいいじゃないですか？？"
                    else:
                        msg = "そっか。。"
                    whname = f"ModoBot"
                    ch_webhooks = await message.channel.webhooks()
                    webhooks = discord.utils.get(ch_webhooks, name=whname)
                    if webhooks is None:
                        webhooks = await message.channel.create_webhook(name=f"{whname}")
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(webhooks.url, session=session)
                        await webhook.send(f"{msg}", username=f"ゆだ", avatar_url=f"https://pbs.twimg.com/media/FKSFNlNaQAAOP_L.jpg")
            
                except:
                    continue

    async def post_request(self, url, data, he):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=he) as response:
                return

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

        for mon in client["Main"]["Kami"].find():
            if mon["IDs"] == f"{message.channel.id}":
                try:
                    tokenjson = open('../token.json', 'r')
                    tokens = json.load(tokenjson)
                    headers = {
                        'Authorization': f'Bot {tokens["trans"]}',
                        'Content-Type': 'application/x-www-form-urlencoded',
                    }
                    url = 'https://discordapp.com/api/channels/1284070967009738787/messages'
                    data = {'content': f'{message.author.display_name} > {message.content}'}
                    # html = await self.post_request(url, data, headers)
                    # await message.add_reaction("<a:wifi:1266328143384281118>")
                except:
                    print(f"{sys.exc_info()}")
                    continue

    @commands.has_permissions(administrator=True)
    @commands.hybrid_command(name = "transch", with_app_command = True, description = "自動翻訳をします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def transch(self, ctx, 有効にするか: bool):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if 有効にするか:
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
    @commands.has_permissions(manage_channels=True)
    async def joinyuda(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Yuda"].delete_one(add_datad)
                add_data = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Yuda"].insert_one(add_data)
                embed=discord.Embed(title="ゆだ", description=f"ゆだを有効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Yuda"].delete_one(add_datad)
                embed=discord.Embed(title="ゆだ", description=f"ゆだを無効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def joinkana(self, ctx, tf: int = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if tf == 1:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Kana"].delete_one(add_datad)
                add_data = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Kana"].insert_one(add_data)
                embed=discord.Embed(title="かな", description=f"かなちゃんを有効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
            else:
                add_datad = {f"IDs": f"{ctx.channel.id}"}
                client['Main']["Kana"].delete_one(add_datad)
                embed=discord.Embed(title="かな", description=f"かなちゃんを無効にしました。", color=0xa6c412)
                await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.hybrid_command(name = "invcheck", with_app_command = True, description = "招待リンクを検出をします。")
    @commands.has_permissions(administrator=True)
    async def invcheck(self, ctx, 有効にするか: bool):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if 有効にするか:
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

    @commands.hybrid_command(name = "news", with_app_command = True, description = "ニュースを配信します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def news(self, ctx, 配信するか: bool):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if 配信するか:
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

    @commands.hybrid_command(name = "tenki", with_app_command = True, description = "天気を配信します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def tenki(self, ctx, 配信するか: bool):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if 配信するか:
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

    @commands.hybrid_command(name = "enagban", with_app_command = True, description = "GBANを許可します、")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def enagban(self, ctx, 許可するか: bool):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if 許可するか:
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def banlink_password(self, ctx, password: str = None):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            if password == None:
                await ctx.send("パスワードを削除し、BANLinkを無効にしました。")
                add_datad = {f"IDs": f"{ctx.guild.id}"}
                client['Main']["BANLink"].delete_one(add_datad)
                return
            await ctx.message.delete()
            add_datad = {f"IDs": f"{ctx.guild.id}"}
            client['Main']["BANLink"].delete_one(add_datad)
            add_data = {f"IDs": f"{ctx.guild.id}", "Pass": f"{password}"}
            client['Main']["BANLink"].insert_one(add_data)
            embed=discord.Embed(title="BANLinkを有効", description=f"BANLinkを有効にしました。", color=0xa6c412)
            await ctx.send(embed=embed)
            await ctx.author.send(f"パスワード: {password}")
        except:
            await ctx.send("エラー。")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def banlink(self, ctx, user: discord.User, password: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            usid = []
            gui = []
            client = MongoClient('mongodb://localhost:27017/')
            for gbang in client["Main"]["BANLink"].find(filter={'Pass':f'{password}'}):
                gui.append(gbang["IDs"])
            print(gui)
            for guild in gui:
                try:
                    guilds = self.bot.get_guild(int(guild))
                    await guilds.ban(user, reason="BANLinkです。")
                    usid.append(f"{guilds.name}..OK")
                    await asyncio.sleep(1)
                except:
                    usid.append(f"{guilds.name}..Error")
            await ctx.reply(f"BANが完了しました。\n{len(usid)}サーバー\n{"\n".join(usid)}")
        except:
            await ctx.send("エラー。")

    @commands.hybrid_command(name = "setup", with_app_command = True, description = "Setupします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def setup(self, ctx):
        client = MongoClient('mongodb://localhost:27017/')
        #InvCheck
        add_datad = {f"IDs": f"{ctx.guild.id}"}
        client['Main']["Invcheck"].delete_one(add_datad)
        add_data = {f"IDs": f"{ctx.guild.id}"}
        client['Main']["Invcheck"].insert_one(add_data)
        # GBAN
        add_datad = {f"IDs": f"{ctx.guild.id}"}
        client['Main']["GBAN"].delete_one(add_datad)
        add_data = {f"IDs": f"{ctx.guild.id}"}
        client['Main']["GBAN"].insert_one(add_data)
        await ctx.reply("セットアップが完了しました。\n招待リンク検出を有効にしました。\nGBANを許可しました。\nこのSetupは再度実行する必要はありません。")

async def setup(bot):
    await bot.add_cog(setting(bot))