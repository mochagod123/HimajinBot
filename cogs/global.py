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
import aiofiles

modonetcooldown = []

class Global(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot
        self._modonet = commands.CooldownMapping.from_cooldown(1, 3.0, commands.BucketType.member)

    def NameSelect(self, ids: int):
        try:
            pmem = []
            for i in self.bot.get_guild(1265256517582717009).get_role(1266722263172911137).members:
                pmem.append(i.id)
            username = f"😊"
            ownername = f"🔨"
            premiumname = f"💎"
            hunter = f"🐲"
            magic = f"🔮"
            if ids == 1206048010740432906 or ids == 1275113699522252810:
                return ownername
            elif ids in pmem:
                return premiumname
            elif ids == 1217596121702993970:
                return hunter
            elif ids == 1067339603859734538:
                return magic
            else:
                return username
        except:
            print(f"{sys.exc_info()}")
            return "📩"

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
                            await webhook.send(re.sub(INVITE_PATTERN, "[Invite link]", message.replace("@", "＠")), username=f"[{self.NameSelect(userid)}]{displayname}-{userid}-{guildname}", avatar_url=f"{avatar}", files=files)
                        else:
                            ch_webhooks = await channel.webhooks()
                            whname = f"ModoBot-Global-{name}"
                            webhooks = discord.utils.get(ch_webhooks, name=whname)
                            if webhooks is None:
                                webhooks = await channel.create_webhook(name=f"{whname}")
                            webhook = Webhook.from_url(webhooks.url, session=session)
                            await webhook.send(re.sub(INVITE_PATTERN, "[Invite link]", message.replace("@", "＠")), username=f"[{self.NameSelect(userid)}]{displayname}-{userid}-{guildname}", avatar_url=f"{avatar}")
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

        if not message.author.avatar == None:
            avurl = message.author.avatar.url
        else:
            avurl = "https://kotonohaworks.com/free-icons/wp-content/uploads/kkrn_icon_user_1-768x768.png"

        client = MongoClient('mongodb://localhost:27017/')

        try:
            for channelss in client["Main"]["GlobalChat"].find(filter={'IDs':f'{str(message.channel.id)}'}):
                if not message.reference:
                    if message.attachments != []:
                        u = message.attachments[0].url
                        na = message.attachments[0].filename
                        await self.send_message(channelss["Name"], f"{message.content}\n+File", message.author.id, message.author.display_name, message.guild.name, avurl, message.channel.id, f"{u}", f"{na}")
                    else:
                        await self.send_message(channelss["Name"], message.content, message.author.id, message.author.display_name, message.guild.name, avurl, message.channel.id)
                else:
                    reference_msg = await message.channel.fetch_message(message.reference.message_id)
                    if message.attachments != []:
                        u = message.attachments[0].url
                        na = message.attachments[0].filename
                        await self.send_message(channelss["Name"], f"> 「{reference_msg.author.display_name}」さんに返信しました。\n{message.content}\n+File", message.author.id, message.author.display_name, message.guild.name, avurl, message.channel.id, f"{u}", f"{na}")
                    else:
                        await self.send_message(channelss["Name"], f"> 「{reference_msg.author.display_name}」さんに返信しました。\n{message.content}", message.author.id, message.author.display_name, message.guild.name, avurl, message.channel.id)
                await message.add_reaction("<a:wifi:1266328143384281118>")
        except:
            return
    @commands.hybrid_group(fallback='info', description = "グローバル関連のコマンドです。")
    async def globals(self, ctx):
        await ctx.reply("グローバル関連のコマンドです。")

    @globals.command(name = "talkglobal", with_app_command = True, description = "グローバルチャットを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def talkglobal(self, ctx, チャンネル名: str):
        chatname = チャンネル名
        try:
            client = MongoClient('mongodb://localhost:27017/')
            webhook = await ctx.channel.create_webhook(
                name=f"ModoBot-Global-{chatname}",
                )
            add_datad = {f"IDs": f"{ctx.channel.id}"}
            client['Main']["GlobalChat"].delete_one(add_datad)
            add_data = {f"IDs": f"{ctx.channel.id}", f"Name": f"{chatname}"}
            client['Main']["GlobalChat"].insert_one(add_data)
            embed=discord.Embed(title=f"GlobalChat-Join", description=f"グローバルチャットにログインしました。\nName: {chatname}", color=0x3acf26)
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"エラー!\n{sys.exc_info()}")

    @globals.command(name = "deactivate", with_app_command = True, description = "グローバルチャットを削除します。")
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

    @commands.group(aliases=["mn"])
    async def modonetwork(self, ctx):
        return

    async def write_logs(self, filename, contents):
        async with aiofiles.open(filename, mode='a') as file:
            await file.write(f"{contents}\n")

    @commands.Cog.listener("on_message")
    async def on_message_modonet(self, message):
        chs = []

        if message.author.bot:
            return
        if message.author.id == self.bot.user.id:
            return

        if (type(message.channel) == discord.DMChannel):
            return

        if await self.checkgmute(message.author):
            return
        
        if "mo." in message.content or "mo#" in message.content:
            return

        client = MongoClient('mongodb://localhost:27017/')

        for check in client["Main"]["ModoNet"].find():
            chs.append(check["IDs"])

        if not str(message.channel.id) in chs:
            return

        await self.write_logs("Logs/ModoNet.txt", f"{message.content} | {message.author.display_name} | {message.author.id}")

        await message.delete()

        for channels in client["Main"]["ModoNet"].find():
            channel = self.bot.get_channel(int(channels["IDs"]))
            embed = discord.Embed(title=f"{message.author.display_name}", description=f"{message.content.replace("@", "＠")}", color=0x36f9d7)
            embed.set_footer(text=f"{message.guild.id}|{message.guild.name}")
            mmm = await channel.send(embed=embed)
            await asyncio.sleep(0.8)

    @modonetwork.group(name="join")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def mn_join(self, ctx):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_data = {f"IDs": f"{ctx.channel.id}", f"GUD": f"{ctx.guild.id}"}
            add_datad = {f"GUD": f"{ctx.guild.id}"}
            client['Main']["ModoNet"].delete_one(add_datad)
            client['Main']["ModoNet"].insert_one(add_data)
            await ctx.reply(embed=discord.Embed(title=f"ModoNetworkに参加しました。"))
        except:
            await ctx.send("エラー。")

    @modonetwork.group(name="leave")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def mn_leave(self, ctx):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"GUD": f"{ctx.guild.id}"}
            client['Main']["ModoNet"].delete_one(add_datad)
            await ctx.reply(embed=discord.Embed(title=f"ModoNetworkから退出しました。"))
        except:
            await ctx.send("エラー。")

async def setup(bot):
    await bot.add_cog(Global(bot))