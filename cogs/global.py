import discord
from discord.ext import commands
import asyncio
from pymongo import MongoClient
import aiohttp
from discord import Webhook
import json
import requests
import io
from functools import cache
import sys
import urllib
import re
import typing

modonetcooldown = []

class Global(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot
        self._modonet = commands.CooldownMapping.from_cooldown(1, 3.0, commands.BucketType.member)

    def NameSelect(self, ids: int):
        username = f"😊"
        ownername = f"🔨"
        premiumname = f"💎"
        hunter = f"🐲"
        magic = f"🔮"
        if ids == 1206048010740432906 or ids == 1275113699522252810:
            return ownername
        elif ids == 1274684996858150975:
            return premiumname
        elif ids == 1217596121702993970:
            return hunter
        elif ids == 1067339603859734538:
            return magic
        else:
            return username

    async def send_login(self, name: str):
        chid = []
        client = MongoClient('mongodb://localhost:27017/')
        for channels in client["Main"]["GlobalChat"].find():
            if channels["Name"] == f"{name}":
                chid.append(channels["IDs"])

        for ch in chid:
            channel = self.bot.get_channel(int(ch))
            async with aiohttp.ClientSession() as session:
                ch_webhooks = await channel.webhooks()
                whname = f"ModoBot-Global-{name}"
                webhooks = discord.utils.get(ch_webhooks, name=whname)
                if webhooks is None:
                    webhooks = await channel.create_webhook(name=f"{whname}")
                webhook = Webhook.from_url(webhooks.url, session=session)
                await webhook.send(f"新しいサーバーが入出したよ！", username=f"🔨 GlobalChat-Join", avatar_url=f"https://media.discordapp.net/attachments/1265857640026603520/1268169914154483743/join.png?ex=66ab72c4&is=66aa2144&hm=b30c0a8208ac92fc398dea75c6daa6b56e693c5dcb7b341c7cf7c2244a329d4a&=&format=webp&quality=lossless")

    async def send_message(self, name: str, message: str, userid: int, displayname: str, guildname: str, avatar: str, channelid: int, fileurl=None, filename=None):
        chid = []

        INVITE_PATTERN = re.compile(r"(https?://)?((ptb|canary)\.)?(discord\.(gg|io)|discord(app)?.com/invite)/[0-9a-zA-Z]+")

        client = MongoClient('mongodb://localhost:27017/')

        for channels in client["Main"]["GlobalChat"].find(filter={'Name':f'{name}'}):
            chid.append(channels["IDs"])

        for ch in chid:
            try:
                channel = self.bot.get_channel(int(ch))
                if not channel.id == channelid:
                    async with aiohttp.ClientSession() as session:
                        files = []
                        if fileurl:
                            u = urllib.parse.unquote(fileurl)
                            fio = io.BytesIO()
                            async with session.get(u) as r:
                                fio.write(await r.read())
                            fio.seek(0)
                            files.append(discord.File(fio, filename=f"{filename}"))
                            fio.close()
                            ch_webhooks = await channel.webhooks()
                            whname = f"ModoBot-Global-{name}"
                            webhooks = discord.utils.get(ch_webhooks, name=whname)
                            if webhooks is None:
                                webhooks = await channel.create_webhook(name=f"{whname}")
                            webhook = Webhook.from_url(webhooks.url, session=session)
                            await webhook.send(re.sub(INVITE_PATTERN, "[Invite link]", message.replace("@", "＠")), username=f"{self.NameSelect(userid)}{displayname}-{userid}-{guildname}", avatar_url=f"{avatar}", files=files)
                        else:
                            ch_webhooks = await channel.webhooks()
                            whname = f"ModoBot-Global-{name}"
                            webhooks = discord.utils.get(ch_webhooks, name=whname)
                            if webhooks is None:
                                webhooks = await channel.create_webhook(name=f"{whname}")
                            webhook = Webhook.from_url(webhooks.url, session=session)
                            await webhook.send(re.sub(INVITE_PATTERN, "[Invite link]", message.replace("@", "＠")), username=f"{self.NameSelect(userid)}{displayname}-{userid}-{guildname}", avatar_url=f"{avatar}")
            except:
                # await self.bot.get_channel(1265894171747680298).send(f"{sys.exc_info()}")
                # print(f"{sys.exc_info()}")
                continue

    async def checkgmute(self, user: discord.User):
        client = MongoClient('mongodb://localhost:27017/')
        for usercheck in client['Main']["GMute"].find():
            if str(user.id) == usercheck["IDs"]:
                return True

    @commands.Cog.listener("on_message")
    async def on_message_global(self, message):
        if message.author.bot:
            return
        if message.author.id == self.bot.user.id:
            return

        if (type(message.channel) == discord.DMChannel):
            return

        if await self.checkgmute(message.author):
            return

        client = MongoClient('mongodb://localhost:27017/')

        try:
            for channelss in client["Main"]["GlobalChat"].find(filter={'IDs':f'{str(message.channel.id)}'}):
                if not message.reference:
                    if message.attachments != []:
                        u = message.attachments[0].url
                        na = message.attachments[0].filename
                        await self.send_message(channelss["Name"], f"{message.content}\n+File", message.author.id, message.author.display_name, message.guild.name, message.author.avatar.url, message.channel.id, f"{u}", f"{na}")
                    else:
                        await self.send_message(channelss["Name"], message.content, message.author.id, message.author.display_name, message.guild.name, message.author.avatar.url, message.channel.id)
                else:
                    reference_msg = await message.channel.fetch_message(message.reference.message_id)
                    if message.attachments != []:
                        u = message.attachments[0].url
                        na = message.attachments[0].filename
                        await self.send_message(channelss["Name"], f"> 「{reference_msg.author.display_name}」さんに返信しました。\n{message.content}\n+File", message.author.id, message.author.display_name, message.guild.name, message.author.avatar.url, message.channel.id, f"{u}", f"{na}")
                    else:
                        await self.send_message(channelss["Name"], f"> 「{reference_msg.author.display_name}」さんに返信しました。\n{message.content}", message.author.id, message.author.display_name, message.guild.name, message.author.avatar.url, message.channel.id)
                await message.add_reaction("✅")
        except:
            await message.channel.send(f"GlobalChat-Crashed!\n{sys.exc_info()}")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def talkglobal(self, ctx, chatname: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            webhook = await ctx.channel.create_webhook(
                name=f"ModoBot-Global-{a}",
                )
            add_datad = {f"IDs": f"{ctx.channel.id}", f"Name": f"{chatname}"}
            client['Main']["GlobalChat"].delete_one(add_datad)
            add_data = {f"IDs": f"{ctx.channel.id}", f"Name": f"{chatname}"}
            client['Main']["GlobalChat"].insert_one(add_data)
            embed=discord.Embed(title=f"GlobalChat-Join", description=f"グローバルチャットにログインしました。\nName: {chatname}", color=0x3acf26)
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"エラー!\n{sys.exc_info()}")

    @commands.group()
    @commands.is_owner()
    async def deleteglobal(self, ctx, chatname: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"Name": f"{chatname}"}
            client['Main']["GlobalChat"].delete_many(add_datad)
            embed=discord.Embed(title=f"GlobalChat-Join", description=f"Botの管理者権限でグローバルチャットから全員退出させました。\nName: {chatname}", color=0x3acf26)
            await ctx.send(embed=embed)
        except:
            await ctx.send("エラー!")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def deactivate(self, ctx):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"IDs": f"{ctx.channel.id}"}
            client['Main']["GlobalChat"].delete_many(add_datad)
            embed=discord.Embed(title=f"GlobalChat-Leave", description=f"グローバルチャットからログオフしました。", color=0x3acf26)
            await ctx.send(embed=embed)
        except:
            await ctx.send("エラー!")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def lookgc(self, ctx, name: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            chid = []
            client = MongoClient('mongodb://localhost:27017/')
            for channels in client["Main"]["GlobalChat"].find():
                if channels["Name"] == f"{name}":
                    try:
                        ch = await self.bot.fetch_channel(int(channels["IDs"]))
                        chid.append(ch.guild.name)
                    except:
                        continue
            embed=discord.Embed(title=f"グローバルチャット情報", description=f"{"\n".join(chid)}\n参加は、`mo.talkglobal {name}`", color=0x3acf26)
            await ctx.send(embed=embed)
        except:
            await ctx.send("エラー!")

async def setup(bot):
    await bot.add_cog(Global(bot))