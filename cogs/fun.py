import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance
import io
import glob
import suddendeath
import aiohttp
import asyncio
from functools import cache
import cv2
import re
from alphabet2kana import a2k
import sys
import json
from discord import Webhook
import cv2

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name = "hunter", with_app_command = True, description = "MHの主人公を生成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def hunter(self, ctx):
        embed = discord.Embed(title="ハンター")
        fname="hunter.png"
        file = discord.File(fp="data/MonsterHunter/hunter.png",filename=fname,spoiler=False)
        embed.set_image(url=f"attachment://{fname}")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(file=file, embed=embed)

    @commands.hybrid_command(name = "mhavatar", with_app_command = True, description = "MHのアバターを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def mhavatar(self, ctx, ユーザー: discord.User):
        a = ユーザー.display_name
        n = 6
        join_string = "\n"
        new_string = join_string.join([a[i:i+n] for i in range(0, len(a), n)])
        sendio = io.BytesIO()
        image1 = Image.open("data/MonsterHunter/hunter.jpg")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 50)
        draw.text((270, 0), new_string, fill=(0, 0, 0), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="モンハンアバター")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @commands.hybrid_command(name = "shinchoku", with_app_command = True, description = "進捗を作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def shinchoku(self, ctx, テキスト: str):
        a = テキスト
        sendio = io.BytesIO()
        image1 = Image.open("data/Shinchoku/Base.png")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 10)
        draw.text((45, 24), a, fill=(255, 255, 255), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="進捗")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @commands.hybrid_command(name = "robokasu", with_app_command = True, description = "ろぼかすを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def robokasu(self, ctx, テキスト: str):
        a = テキスト
        n = 8
        join_string = "\n"
        new_string = join_string.join([a[i:i+n] for i in range(0, len(a), n)])
        sendio = io.BytesIO()
        image1 = Image.open("data/Robo/Base.png")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 15)
        draw.text((40, 35), new_string, fill=(0, 0, 0), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="ろぼかす")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @commands.hybrid_command(name = "yuta", with_app_command = True, description = "ゆうたを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def yuta(self, ctx, 名言: str):
        a = 名言
        sendio = io.BytesIO()
        image1 = Image.open("data/Yuta/Base.jpg")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 30)
        draw.text((75, 15), a, fill=(0, 0, 0), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="ゆうた・ふんたー")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @commands.hybrid_command(name = "dragon", with_app_command = True, description = "ドラゴンを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def dragon(self, ctx, 名言: str):
        a = 名言
        n = 9
        join_string = "\n"
        new_string = join_string.join([a[i:i+n] for i in range(0, len(a), n)])
        sendio = io.BytesIO()
        image1 = Image.open("data/LDr/Base.png")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 30)
        draw.text((110, 80), new_string, fill=(0, 0, 0), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="なんかのドラゴン")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @commands.hybrid_command(name = "nikuyaki", with_app_command = True, description = "肉焼きをします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def nikuyaki(self, ctx, *, メンバー: discord.User):
        member = メンバー
        content = requests.get(member.display_avatar)
        pdf_data = io.BytesIO(content.content)
        sendio = io.BytesIO()
        img = Image.open(pdf_data)
        image1 = Image.open("data/NikuYaki/Base.png")
        img_resize = img.resize((50, 50))
        image1.paste(img_resize, (60, 54))
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="肉焼き")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @commands.hybrid_command(name = "yusha", with_app_command = True, description = "勇者を召喚します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def yusha(self, ctx, *, ユーザー: discord.User):
        member = ユーザー
        content = requests.get(member.display_avatar)
        pdf_data = io.BytesIO(content.content)
        sendio = io.BytesIO()
        img = Image.open(pdf_data)
        image1 = Image.open("data/DRG/Base.png")
        img_resize = img.resize((140, 172))
        image1.paste(img_resize, (175, 100))
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="勇者")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @commands.hybrid_command(name = "riaju", with_app_command = True, description = "リア充が爆発します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def riaju(self, ctx, *, ユーザー: discord.User):
        member = ユーザー
        content = requests.get(member.display_avatar)
        pdf_data = io.BytesIO(content.content)
        sendio = io.BytesIO()
        img = Image.open(pdf_data)
        image1 = Image.open("data/Riaju/Base.jpg")
        img_resize = img.resize((184, 184))
        image1.paste(img_resize, (310, 300))
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="リア充の大爆発!")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @commands.hybrid_command(name = "3ds", with_app_command = True, description = "3dsを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def sands(self, ctx, 画像: discord.Attachment):
        try:
            image_byte = 画像
            async with aiohttp.ClientSession() as session:
                async with session.get(image_byte.url) as response:
                    content = await response.read()
                    pdf_data = io.BytesIO(content)
                    sendio = io.BytesIO()
                    img = Image.open(pdf_data)
                    image1 = Image.open("data/3ds/Base.jpg")
                    img_resize = img.resize((768, 772))
                    image1.paste(img_resize, (7, 23))
                    image1.save(sendio,format="png")
                    sendio.seek(0)
                    amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
                    embed = discord.Embed(title="3ds")
                    embed.set_image(url=amsg.attachments[0].url)
                    embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                    await ctx.reply(embed=embed)
                    sendio.close()
                    await ctx.message.delete()
        except:
            return
        
    @commands.hybrid_command(name = "ps2", with_app_command = True, description = "PS2を作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def pstwo(self, ctx, 画像: discord.Attachment):
        try:
            image_byte = 画像
            async with aiohttp.ClientSession() as session:
                async with session.get(image_byte.url) as response:
                    content = await response.read()
                    pdf_data = io.BytesIO(content)
                    sendio = io.BytesIO()
                    img = Image.open(pdf_data)
                    image1 = Image.open("data/ps2.jpg")
                    img_resize = img.resize((499, 638))
                    image1.paste(img_resize, (5, 80))
                    image1.save(sendio,format="png")
                    sendio.seek(0)
                    amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
                    embed = discord.Embed(title="PS2")
                    embed.set_image(url=amsg.attachments[0].url)
                    embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                    await ctx.reply(embed=embed)
                    sendio.close()
                    await ctx.message.delete()
        except:
            return
        
    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def switch_hard(self, ctx):
        try:
            if not ctx.message.attachments:
                e = discord.Embed(title="添付ファイルがないです!", description="このメッセージは、\n5秒後に削除されます。")
                msg = await ctx.reply(embed=e)
                await ctx.message.delete()
                await asyncio.sleep(5)
                await msg.delete()
                return
            image_byte = ctx.message.attachments[0]
            content = requests.get(image_byte)
            pdf_data = io.BytesIO(content.content)
            sendio = io.BytesIO()
            img = Image.open(pdf_data)
            image1 = Image.open("data/Switch.jpg")
            img_resize = img.resize((430, 235))
            image1.paste(img_resize, (158, 77))
            image1.save(sendio,format="png")
            sendio.seek(0)
            amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
            embed = discord.Embed(title="Switch_Hard")
            embed.set_image(url=amsg.attachments[0].url)
            embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
            await ctx.reply(embed=embed)
            sendio.close()
            await ctx.message.delete()
        except:
            return

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def myaq(self, ctx):
        if ctx.message.reference:
            reference_msg = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            user = reference_msg.author
            payload={
                "username": user.name,
                "display_name": user.display_name,
                "text": reference_msg.content,
                "avatar": user.avatar.url,
                "color": True
                }
            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.voids.top/quote", data=json.dumps(payload)) as response:
                    k = await response.text()
                    quote = json.loads(k)
                    await ctx.send(quote['url'])

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def love(self, ctx, *, member: discord.User):
        content = requests.get(ctx.author.display_avatar)
        mb = io.BytesIO(content.content)
        contenta = requests.get(member.display_avatar)
        ma = io.BytesIO(contenta.content)
        sendio = io.BytesIO()
        img = Image.open(mb)
        imga = Image.open(ma)
        image1 = Image.open("data/Love/Love.png")
        img_resize = img.resize((135, 135))
        image1.paste(img_resize, (25, 45))
        img_resizea = imga.resize((135, 135))
        image1.paste(img_resizea, (385, 45))
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 50)
        draw.text((210, 245), f"{random.randint(0, 100)}%", fill=(0, 0, 0), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="Love")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def naguru(self, ctx, *, member: discord.User):
        async with aiohttp.ClientSession() as session:
            async with session.get(member.display_avatar.url) as response:
                content = await response.read()
                pdf_data = io.BytesIO(content)
                sendio = io.BytesIO()
                img = Image.open(pdf_data)
                image1 = Image.open("data/naguru.jpg")
                img_resize = img.resize((67, 69))
                image1.paste(img_resize, (65, 65))
                image1.save(sendio,format="png")
                sendio.seek(0)
                amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
                embed = discord.Embed(title="なぐる")
                embed.set_image(url=amsg.attachments[0].url)
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                await ctx.reply(embed=embed)
                sendio.close()

    @commands.hybrid_command(name = "5000", with_app_command = True, description = "5000兆円を作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def gosenchoen(self, ctx, うえ: str, した: str):
        embed = discord.Embed(title="5000兆円ほしい!")
        embed.set_image(url=f"https://gsapi.cbrx.io/image?top={うえ}&bottom={した}")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "neko", with_app_command = True, description = "NyanNyan")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def neko(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=neko") as response:
                res = await response.json()
                embed = discord.Embed(title="猫耳娘", color=res["color"])
                embed.set_image(url=res["message"])
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "kemomimi", with_app_command = True, description = "けみみみを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def kemomimi(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=kemonomimi") as response:
                jsonData = await response.json()
                embed = discord.Embed(title="ケモミミちゃん", color=jsonData["color"])
                embed.set_image(url=jsonData["message"])
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "food", with_app_command = True, description = "食事を作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def food(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=food") as response:
                jsonData = await response.json()
                embed = discord.Embed(title="食べ物", color=jsonData["color"])
                embed.set_image(url=jsonData["message"])
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "coffee", with_app_command = True, description = "コーヒーを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def coffee(self, ctx):
        url = "https://nekobot.xyz/api/image?type=coffee"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jsonData = await response.json()
                embed = discord.Embed(title="コーヒー☕", color=jsonData["color"])
                embed.set_image(url=jsonData["message"])
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "kanna", with_app_command = True, description = "Kannaを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def kanna(self, ctx):
        url = "https://nekobot.xyz/api/image?type=kanna"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jsonData = await response.json()
                embed = discord.Embed(title="カンナちゃん", color=jsonData["color"])
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                embed.set_image(url=jsonData["message"])
                msg = await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def poke(self, ctx):
        url = "https://api.waifu.pics/sfw/poke"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jsonData = await response.json()
                embed = discord.Embed(title="突く")
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                embed.set_image(url=jsonData["url"])
                msg = await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "dog", with_app_command = True, description = "犬を作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def dog(self, ctx):
        url = "https://dog.ceo/api/breeds/image/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jsonData = await response.json()
                embed = discord.Embed(title="犬")
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                embed.set_image(url=jsonData["message"])
                msg = await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "httpcat", with_app_command = True, description = "HTTPCATを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def httpcat(self, ctx, 数字: str):
        embed = discord.Embed(title="HttpCat")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://http.cat/{数字}")
        msg = await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "fox", with_app_command = True, description = "きつねを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def fox(self, ctx):
        url = "https://randomfox.ca/floof/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jsonData = await response.json()
                embed = discord.Embed(title="きつね🦊")
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                embed.set_image(url=jsonData["image"])
                msg = await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "nounai", with_app_command = True, description = "脳内メーカーをします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def nounai(self, ctx, 名前: str):
        embed = discord.Embed(title="脳内メーカー")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://maker.usoko.net/nounai/img/{名前}.gif")
        msg = await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "isekai", with_app_command = True, description = "転生します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def isekai(self, ctx, 名前: str):
        embed = discord.Embed(title="異世界家系図メーカー")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/kakeizu_fantasy/r/img/{名前}.gif")
        msg = await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "kabuto", with_app_command = True, description = "かぶとを製作します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def kabuto(self, ctx, 名前: str):
        embed = discord.Embed(title=f"{名前}の兜")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/kabuto/img/{名前}.gif")
        msg = await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "smartphone", with_app_command = True, description = "スマホを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def smartphone(self, ctx, 名前: str):
        embed = discord.Embed(title=f"{名前}のスマホ")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/sumaho/img/{名前}.gif")
        msg = await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def busho(self, ctx, a: str):
        embed = discord.Embed(title=f"{a}が武将だったら？")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/busyo/img/{a}.gif")
        msg = await ctx.reply(embed=embed)
        
    @commands.hybrid_command(name = "gifs", with_app_command = True, description = "GIFを検索します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def gifs(self, ctx, 検索ワード: str):
        try:
            if not 検索ワード == None:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://tenor.com/ja/search/{検索ワード}-gifs') as response:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        title = soup.find_all('div', class_="Gif")[0]
                        titles = title.find_all('img')[0]
                        embed = discord.Embed(title=f"{検索ワード}の検索結果")
                        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                        embed.set_image(url=f"{titles["src"]}")
                        msg = await ctx.reply(embed=embed)
                        return
        except:
            await ctx.send(f"{sys.exc_info()}")
            return

    @commands.hybrid_command(name = "hikakin", with_app_command = True, description = "ヒカキンを表示します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def hikakin(self, ctx):
        embed = discord.Embed(title="ヒカキン")
        list = glob.glob('data/Hikakin/*.png')
        data = random.choice(list)
        file=discord.File(data, filename="hikakin.png")
        embed.set_image(url=f"attachment://hikakin.png")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(file=file, embed=embed)

    @commands.hybrid_command(name = "sud", with_app_command = True, description = "突然の死を作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def suddendeath(self, ctx, 言葉: str):
        await ctx.reply(f"```{suddendeath.suddendeathmessage(言葉).replace("@", "")}```")

    @commands.command(aliases=["ych"])
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def yudachat(self, ctx, a: str):
        msg = "None"
        whname = f"ModoBot-Yuda"
        ch_webhooks = await ctx.channel.webhooks()
        webhooks = discord.utils.get(ch_webhooks, name=whname)
        if webhooks is None:
            webhooks = await ctx.channel.create_webhook(name=f"{whname}")
        if "こんにちは" in a:
            msg = f"こんにちは。。{ctx.author.name}さん。。"
        elif "使えない" in a:
            msg = f"無料なんだから使わなきゃいいじゃないですか？？"
        else:
            msg = "そっか。。"
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(webhooks.url, session=session)
            await webhook.send(msg, username=f"ゆだ", avatar_url=f"https://pbs.twimg.com/media/FKSFNlNaQAAOP_L.jpg")

    @commands.hybrid_command(name = "kch", with_app_command = True, description = "かなチャットをします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def kanachat(self, ctx, 言葉: str):
        a = 言葉
        tokenjson = open('../token.json', 'r')
        tokens = json.load(tokenjson)
        whname = f"ModoBot"
        ch_webhooks = await ctx.channel.webhooks()
        webhooks = discord.utils.get(ch_webhooks, name=whname)
        if webhooks is None:
            webhooks = await ctx.channel.create_webhook(name=f"{whname}")
        async with aiohttp.ClientSession() as session:
            async with session.post("https://kana.renorari.net/api/v2/chat", json={"message":f"{a}","user":{"id":f"{tokens["kanaid"]}","password":f"{tokens["kanapass"]}"},"character_name":"discord","custom_character":"おは#100#5-9#おはよう!!,おっはー！,おはよーぅ!#null#{}\nおは#100#10-17#おそよう,今お昼だよ、おはよ#null#{}\nおは#100#18-4#昼夜逆転♫おはよ!,私はもう少しで寝ますよ?おはよ#null#{}"}) as response:
                kkk = await response.text()
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhooks.url, session=session)
                    await webhook.send(f"{json.loads(kkk)["reply"].replace("もどっぐ", f"{ctx.author.display_name}")}", username=f"かなちゃん", avatar_url=f"https://yt3.googleusercontent.com/Q2yN9GaRPKbMcRVthn2_FegI5PAvfA9DLNZK-pzLybxWw5j9Emdh_hXGMuSqqIKWjmcNmSwEfOY=s900-c-k-c0x00ffffff-no-rj")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def engjp(self, ctx, a: str):
        try:
            await ctx.reply(f"```{a2k(f"{a}").replace("@", "＠").replace("#", "＃")}```")
        except:
            await ctx.reply("Error.")

async def setup(bot):
    await bot.add_cog(Fun(bot))