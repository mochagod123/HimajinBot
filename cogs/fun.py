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
from discord import Webhook
import cv2

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def hunter(self, ctx):
        embed = discord.Embed(title="ハンター")
        fname="hunter.png"
        file = discord.File(fp="data/MonsterHunter/hunter.png",filename=fname,spoiler=False)
        embed.set_image(url=f"attachment://{fname}")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(file=file, embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def mhavatar(self, ctx, a: str):
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def shinchoku(self, ctx, a: str):
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def robokasu(self, ctx, a: str):
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def yuta(self, ctx, a: str):
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def dragon(self, ctx, a: str):
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def nikuyaki(self, ctx, *, member: discord.User):
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def yusha(self, ctx, *, member: discord.User):
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def riaju(self, ctx, *, member: discord.User):
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

    @commands.command(name="3ds")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def sands(self, ctx):
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def myqu(self, ctx, user: discord.User, a: str):
        payload={
            "username": user.name,
            "display_name": user.display_name,
            "text": a,
            "avatar": user.avatar.url,
            "color": True
            }
        quote=requests.post("https://api.voids.top/quote",json=payload).json()
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
        content = requests.get(member.display_avatar)
        pdf_data = io.BytesIO(content.content)
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

    @commands.command(name="5000")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def gosenchoen(self, ctx, a: str, b: str):
        embed = discord.Embed(title="5000兆円ほしい!")
        embed.set_image(url=f"https://gsapi.cbrx.io/image?top={a}&bottom={b}")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def neko(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=neko") as response:
                res = await response.json()
                embed = discord.Embed(title="猫耳娘", color=res["color"])
                embed.set_image(url=res["message"])
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def kemomimi(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=kemonomimi") as response:
                jsonData = await response.json()
                embed = discord.Embed(title="ケモミミちゃん", color=jsonData["color"])
                embed.set_image(url=jsonData["message"])
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def food(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=food") as response:
                jsonData = await response.json()
                embed = discord.Embed(title="食べ物", color=jsonData["color"])
                embed.set_image(url=jsonData["message"])
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                await ctx.reply(embed=embed)

    @commands.group()
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

    @commands.group()
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

    @commands.group()
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def httpcat(self, ctx, a: str):
        embed = discord.Embed(title="HttpCat")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://http.cat/{a}")
        msg = await ctx.reply(embed=embed)

    @commands.group()
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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def nounai(self, ctx, a: str):
        embed = discord.Embed(title="脳内メーカー")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://maker.usoko.net/nounai/img/{a}.gif")
        msg = await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def isekai(self, ctx, a: str):
        embed = discord.Embed(title="異世界家系図メーカー")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/kakeizu_fantasy/r/img/{a}.gif")
        msg = await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def kabuto(self, ctx, a: str):
        embed = discord.Embed(title=f"{a}の兜")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/kabuto/img/{a}.gif")
        msg = await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def smartphone(self, ctx, a: str):
        embed = discord.Embed(title=f"{a}のスマホ")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/sumaho/img/{a}.gif")
        msg = await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def busho(self, ctx, a: str):
        embed = discord.Embed(title=f"{a}が武将だったら？")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/busyo/img/{a}.gif")
        msg = await ctx.reply(embed=embed)
        
    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def gifs(self, ctx, a: str):
        try:
            if not a == None:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://tenor.com/ja/search/{a}-gifs') as response:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        title = soup.find_all('div', class_="Gif")[0]
                        titles = title.find_all('img')[0]
                        embed = discord.Embed(title=f"{a}の検索結果")
                        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
                        embed.set_image(url=f"{titles["src"]}")
                        msg = await ctx.reply(embed=embed)
                        return
        except:
            await ctx.send(f"{sys.exc_info()}")
            return

    @commands.command(aliases=["hika"])
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def hikakin(self, ctx):
        embed = discord.Embed(title="ヒカキン")
        list = glob.glob('data/Hikakin/*.png')
        data = random.choice(list)
        file=discord.File(data, filename="hikakin.png")
        embed.set_image(url=f"attachment://hikakin.png")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(file=file, embed=embed)

    @commands.command(aliases=["sud"])
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def suddendeath(self, ctx, a: str):
        await ctx.reply(f"```{suddendeath.suddendeathmessage(a).replace("@", "")}```")

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

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def engjp(self, ctx, a: str):
        try:
            await ctx.reply(f"```{a2k(f"{a}").replace("@", "＠").replace("#", "＃")}```")
        except:
            await ctx.reply("Error.")

async def setup(bot):
    await bot.add_cog(Fun(bot))