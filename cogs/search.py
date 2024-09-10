import discord
from discord.ext import commands
import asyncio
from bs4 import BeautifulSoup
import requests
import csv
import sys
import random
import urllib.request
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

class helpc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def google(self, ctx, a: str):
        await ctx.send(f"https://www.google.co.jp/search?q={a.replace("@", "＠")}")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def ggrks(self, ctx, a: str):
        await ctx.send(f"http://ggrks.atspace.tv/?{a.replace("@", "＠")}")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def amazon(self, ctx, a: str):
        await ctx.send(f"https://www.amazon.co.jp/s?k={a.replace("@", "＠")}")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def safeweb(self, ctx, a: str):
        await ctx.send(f"分析結果: \nhttps://safeweb.norton.com/report?url={a.replace("@", "＠")}")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def rafi(self, ctx):
        try:
            lists = []
            filename = 'data/malnet.csv'
            with open(filename, encoding='utf8', newline='') as f:
                csvreader = csv.reader(f)
                for row in csvreader:
                    lists.append(row[1])

            embed=discord.Embed(title=f"とても危険なサイト\nURL-> {random.choice(lists).replace("http", "ht0p")}", description="このサイトはとても危険です。\nアクセスする際は自己責任でお願いします。\n(リンク切れかも。。)")
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"{sys.exc_info()}")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def niconico(self, ctx, key: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://www.nicovideo.jp/search/{urllib.parse.quote_plus(key, encoding='utf-8')}?ref=nicotop_search') as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    name = soup.find_all("p", class_="itemTitle")
                    url = soup.find_all("a", class_="itemThumbWrap")
                    ret = []
                    rets = []
                    for t in name:
                        ret.append(t.text)
                    for a in ret:
                        if a != '':
                            rets.append(a)

                    reta = []
                    retsa = []
                    for t in url:
                        reta.append(t['href'])
                    for a in reta:
                        if a != '':
                            retsa.append(a)

                    embed=discord.Embed(title="NicoNico検索", description=f"{rets[0].replace("@", "")}\nhttps://www.nicovideo.jp{retsa[0].replace("@", "")}", color=0x00ff62, url=f"https://www.nicovideo.jp{retsa[0].replace("@", "")}")
                    msg = await ctx.send(embed=embed)

        except IndexError:
            embed=discord.Embed(title="NicoNico検索", description="エラーが発生しました。\nそのような動画はありませんでした。", color=0x00ff62)
            await ctx.send(embed=embed)
        except:
            return

    @commands.command(aliases=["ul"])
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def ulookup(self, ctx, usera: int):
        try:
            unsei = ["大吉", "中吉", "吉", "末吉", "小吉", "凶", "大凶"]
            choice = random.choice(unsei)
            checkgban = 0
            checkgmute = 0
            client = MongoClient('mongodb://localhost:27017/')
            user = await self.bot.fetch_user(usera)
            embed = discord.Embed(title=f"{user.display_name}",color=user.accent_color)
            embed.add_field(name="ユーザーの名前",value=str(user))
            embed.add_field(name="アカウント作成日",value=user.created_at)
            if user.bot:
                embed.add_field(name="Botかどうか？",value="はい")
            else:
                embed.add_field(name="Botかどうか？",value="いいえ")
            for mon in client["Main"]["GBANHist"].find():
                if mon["IDs"] == f"{user.id}":
                    checkgban = 1
                    break
            for mon in client["Main"]["GMute"].find():
                if mon["IDs"] == f"{user.id}":
                    checkgmute = 1
                    break
            embed.add_field(name="GBAN済みか？",value=f"{str(checkgban).replace("0", "いいえ").replace("1", "はい")}")
            embed.add_field(name="GMute済みか？",value=f"{str(checkgmute).replace("0", "いいえ").replace("1", "はい")}")
            embed.add_field(name="占い結果",value=choice)
            embed.set_thumbnail(url=user.avatar)
            msg = await ctx.send(embed=embed)
            return
        except:
            return

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def slookup(self, ctx, ser: discord.Guild):
        try:
            user = await self.bot.fetch_user(ser.owner_id)
            embed = discord.Embed(title="サーバー情報", color=0x70006e)
            embed.add_field(name="名前",value=str(ser))
            embed.add_field(name="サーバーID",value=str(ser.id))
            embed.add_field(name="オーナーID",value=str(ser.owner_id))
            embed.add_field(name="オーナーの名前",value=f"{user.display_name}")
            embed.add_field(name="オーナーの作成日",value=f"{user.created_at}")
            embed.set_thumbnail(url=ser.icon)
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"{sys.exc_info()}")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def pypi(self, ctx, key: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://pypi.org/search/?q={key}') as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    title = soup.find('span', class_="package-snippet__name")
                    link = soup.find('a', class_="package-snippet")
                    embed=discord.Embed(title=f"PyPi検索 - {title.get_text()}", url=f"https://pypi.org{link["href"]}", description=f"https://pypi.org{link["href"]}", color=0x316cb9)
                    await ctx.send(embed=embed)

        except:
            embed=discord.Embed(title=f"該当するものがなかったかも。。\n{sys.exc_info()}", color=0x316cb9)
            await ctx.send(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def mhnews(self, ctx, key: int):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://prtimes.jp/topics/keywords/%E3%83%A2%E3%83%B3%E3%83%8F%E3%83%B3') as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    title = soup.find_all('a', class_="link-thumbnail link-thumbnail-ordinary")[key]
                    await ctx.send(f"https://prtimes.jp{title["href"]}")

        except:
            embed=discord.Embed(title=f"該当するものがなかったかも。。", color=0x316cb9)
            await ctx.send(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def pcnews(self, ctx, key: int):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://prtimes.jp/topics/keywords/PC') as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    title = soup.find_all('a', class_="link-thumbnail link-thumbnail-ordinary")[key]
                    await ctx.send(f"https://prtimes.jp{title["href"]}")

        except:
            embed=discord.Embed(title=f"該当するものがなかったかも。。", color=0x316cb9)
            await ctx.send(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def flipmemo(self, ctx, title: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://archive.sudomemo.net/search/?q={title}&mode=user') as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                url = soup.find_all('h3', class_="UserInfo__name")[0]
                url2 = url.find_all('a')[0]
                await ctx.send(f"https://archive.sudomemo.net/user{url2["href"]}")

async def setup(bot):
    await bot.add_cog(helpc(bot))