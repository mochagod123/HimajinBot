import discord
from discord.ext import commands
import asyncio
import os
from pymongo import MongoClient
import sys
import aiohttp
from discord import Webhook
import subprocess
import datetime
import re

adminlist = [1206048010740432906]

class AdminCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_gban(self, userid: discord.User, listenss: str):
        try:
            chid = []
            client = MongoClient('mongodb://localhost:27017/')
            for channels in client["Main"]["GlobalChat"].find():
                if channels["Name"] == "gban":
                    try:
                        chid.append(channels["IDs"])
                    except:
                        continue

            for ch in chid:
                channel = self.bot.get_channel(int(ch))
                async with aiohttp.ClientSession() as session:
                    ch_webhooks = await channel.webhooks()
                    whname = f"ModoBot-Global-gban"
                    webhooks = discord.utils.get(ch_webhooks, name=whname)
                    if webhooks is None:
                        webhooks = await channel.create_webhook(name=f"{whname}")
                    webhook = Webhook.from_url(webhooks.url, session=session)
                    await webhook.send(f"「{userid.display_name}」をGBANしました。\n理由: `{listenss}`", username=f"🔨 GBANSystem", avatar_url=f"https://i.imgur.com/7jaHr6p.png")
        except:
            await self.bot.get_channel(1265894171747680298).send(f"{sys.exc_info()}")
            
    async def send_gmute(self, userid: discord.User, listenss: str):
        try:
            chid = []
            client = MongoClient('mongodb://localhost:27017/')
            for channels in client["Main"]["GlobalChat"].find():
                if channels["Name"] == "gban":
                    try:
                        chid.append(channels["IDs"])
                    except:
                        continue

            for ch in chid:
                channel = self.bot.get_channel(int(ch))
                async with aiohttp.ClientSession() as session:
                    ch_webhooks = await channel.webhooks()
                    whname = f"ModoBot-Global-gban"
                    webhooks = discord.utils.get(ch_webhooks, name=whname)
                    if webhooks is None:
                        webhooks = await channel.create_webhook(name=f"{whname}")
                    webhook = Webhook.from_url(webhooks.url, session=session)
                    await webhook.send(f"「{userid.display_name}」をGMuteしました。\n理由:`{listenss}`", username=f"🔨 GMuteSystem", avatar_url=f"https://i.imgur.com/To5oSqi.png")
        except:
            await self.bot.get_channel(1265894171747680298).send(f"{sys.exc_info()}")

    async def send_gkujo(self, userid: discord.User, listenss: str):
        try:
            chid = []
            client = MongoClient('mongodb://localhost:27017/')
            for channels in client["Main"]["GlobalChat"].find():
                if channels["Name"] == "gban":
                    try:
                        chid.append(channels["IDs"])
                    except:
                        continue

            for ch in chid:
                channel = self.bot.get_channel(int(ch))
                async with aiohttp.ClientSession() as session:
                    ch_webhooks = await channel.webhooks()
                    whname = f"ModoBot-Global-gban"
                    webhooks = discord.utils.get(ch_webhooks, name=whname)
                    if webhooks is None:
                        webhooks = await channel.create_webhook(name=f"{whname}")
                    webhook = Webhook.from_url(webhooks.url, session=session)
                    await webhook.send(f"「{userid.display_name}」を駆除対象にしました。\nID:`{userid.id}`\n理由:`{listenss}`", username=f"🔨 GKujoSystem", avatar_url=f"https://i.imgur.com/f3z2liL.png")
        except:
            await self.bot.get_channel(1265894171747680298).send(f"{sys.exc_info()}")

    async def send_sleave(self, servername: str, listenss: str):
        try:
            chid = []
            client = MongoClient('mongodb://localhost:27017/')
            for channels in client["Main"]["GlobalChat"].find():
                if channels["Name"] == "gban":
                    try:
                        chid.append(channels["IDs"])
                    except:
                        continue

            for ch in chid:
                channel = self.bot.get_channel(int(ch))
                async with aiohttp.ClientSession() as session:
                    ch_webhooks = await channel.webhooks()
                    whname = f"ModoBot-Global-gban"
                    webhooks = discord.utils.get(ch_webhooks, name=whname)
                    if webhooks is None:
                        webhooks = await channel.create_webhook(name=f"{whname}")
                    webhook = Webhook.from_url(webhooks.url, session=session)
                    await webhook.send(f"`{servername}`から退出させました。\n理由:`{listenss}`", username=f"🔨 SLeaveSytem", avatar_url=f"https://thumb.ac-illust.com/d5/d5079b1d5dd2aec1e2a64b2699e23db5_t.jpeg")
        except:
            await self.bot.get_channel(1265894171747680298).send(f"{sys.exc_info()}")

    @commands.group(aliases=["re"])
    @commands.cooldown(3, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def reload(self, ctx, a: str = None):
        if a == None:
            for cog in os.listdir("cogs"):
                if cog.endswith(".py"):
                    await self.bot.reload_extension(f"cogs.{cog[:-3]}")
                    await ctx.reply("Reload .. OK!")
                    return
        if (os.path.isfile(f"cogs/{a}.py")):
            await self.bot.reload_extension(f"cogs.{a}")
            await ctx.reply("Reload .. OK!")
        else:
            await ctx.reply("Error! No File!")

    @commands.group()
    @commands.cooldown(3, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def addload(self, ctx, a: str):
        if (os.path.isfile(f"cogs/{a}.py")):
            await self.bot.load_extension(f"cogs.{a}")
            await ctx.reply("Load .. OK!")
        else:
            await ctx.reply("Error! No File!")

    @commands.group()
    @commands.is_owner()
    async def gmute(self, ctx, member: discord.User, listss: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            usid = []
            gui = []
            for gbang in client["Main"]["GBAN"].find():
                gui.append(gbang["IDs"])
            for guild in gui:
                try:
                    guilds = self.bot.get_guild(int(guild))
                    mem = await guilds.fetch_member(member.id)
                    duration = datetime.timedelta(days=7)
                    await mem.timeout(duration, reason="ModoBotによる、GMuteです。")
                    usid.append(f"{guilds.name}..OK")
                    await asyncio.sleep(1)
                except:
                    usid.append(f"{guilds.name}..Error")
            add_datad = {f"IDs": f"{member.id}"}
            client['Main']["GMute"].delete_one(add_datad)
            client['Main']["GMute"].insert_one(add_datad)
            await self.send_gmute(member, listss)
            await ctx.send(f"{member.display_name}をGMuteをしました。\n{len(usid)}鯖。")
        except:
            await ctx.send(f"error!\n{sys.exc_info()}")

    @commands.group()
    @commands.is_owner()
    async def ungmute(self, ctx, *, member: discord.User):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"IDs": f"{member.id}"}
            client['Main']["GMute"].delete_one(add_datad)
            await ctx.send(f"{member.display_name}のGMuteを解除をしました。")
        except:
            await ctx.send(f"error!\n{sys.exc_info()}")

    @commands.group()
    @commands.is_owner()
    async def gban(self, ctx, user: discord.User, lis: str):
        await ctx.send(f"{user.display_name}をGBANしています..")
        usid = []
        gui = []
        client = MongoClient('mongodb://localhost:27017/')
        for gbang in client["Main"]["GBAN"].find():
            gui.append(gbang["IDs"])
        for guild in gui:
            try:
                guilds = self.bot.get_guild(int(guild))
                await guilds.ban(user, reason=lis)
                usid.append(f"{guilds.name}..OK")
                await asyncio.sleep(1)
            except:
                usid.append(f"{guilds.name}..Error")
        client = MongoClient('mongodb://localhost:27017/')
        add_datad = {f"IDs": f"{user.id}"}
        client['Main']["GBANHist"].delete_one(add_datad)
        add_data = {f"IDs": f"{user.id}"}
        client['Main']["GBANHist"].insert_one(add_data)
        await self.send_gban(user, lis)
        await ctx.send(f"{user.display_name}のGBANが完了しました。\n{len(usid)}鯖。")

    @commands.group()
    @commands.is_owner()
    async def ungban(self, ctx, user: discord.User):
        await ctx.send(f"{user.display_name}のGBANを解除しています..")
        usid = []
        gui = []
        client = MongoClient('mongodb://localhost:27017/')
        for gbang in client["Main"]["GBAN"].find():
            gui.append(gbang["IDs"])
        for guild in gui:
            try:
                guilds = self.bot.get_guild(int(guild))
                await guilds.unban(user)
                usid.append(f"{guilds.name}..OK")
                await asyncio.sleep(1)
            except:
                usid.append(f"{guilds.name}..Error")
        await ctx.send(f"{user.display_name}のGBAN解除が完了しました。\n```{'\n'.join(usid)}```")

    @commands.group()
    @commands.is_owner()
    async def gkujotai(self, ctx, user: discord.User, lis: str):
        await self.send_gkujo(user, lis)
        await ctx.send(f"{user.display_name}を駆除対象にしました。")

    @commands.group()
    @commands.is_owner()
    async def pollgban(self, ctx, user: discord.User, riyu: str):
        embed=discord.Embed(title=f"「{user.name}」のGBANをしたほうがいい？\n理由:「{riyu}」", description=f"```[1] ... したほうがいい！！\n[2] ... しないほうがいい。。```\n下のリアクションを付けて答えてください。", color=0xa6c412)
        m = await ctx.send(embed=embed)
        await m.add_reaction("<:1_:1266356576948850780>")
        await m.add_reaction("<:2_:1266356598524215326>")

    @commands.group()
    @commands.is_owner()
    async def sleave(self, ctx, server: int, lis: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            user = await self.bot.fetch_guild(int(server))
            add_datad = {f"IDs": f"{server}"}
            client['Main']["BANServer"].delete_one(add_datad)
            add_data = {f"IDs": f"{server}"}
            client['Main']["BANServer"].insert_one(add_data)
            await self.send_sleave(user.name, lis)
            await user.leave()
            await ctx.send(f"{user.name}から退出させました。")
        except:
            await ctx.send("Error!")

    @commands.group()
    @commands.is_owner()
    async def sunban(self, ctx, server: int):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"IDs": f"{server}"}
            client['Main']["BANServer"].delete_one(add_datad)
            await ctx.send(f"BANを解除しました。")
        except:
            await ctx.send("Error!")

    @commands.group()
    @commands.is_owner()
    async def repre(self, ctx):
        try:
            await self.bot.change_presence(activity=discord.CustomActivity(name=f"mo.help | {len(self.bot.guilds)}鯖-{len(self.bot.users)}人"))
            await ctx.send(f"アクティビティを更新しました。")
        except:
            await ctx.send("Error!")

    @commands.group()
    @commands.is_owner()
    async def slist(self, ctx):
        try:
            for i in adminlist:
                if i == ctx.author.id:
                    join_servers_information = '\n'.join(f"{s.name} ({s.member_count}人) ({s.owner})" for s in self.bot.guilds)
                    embed = discord.Embed(title="導入鯖一覧", description=join_servers_information)
                    await ctx.send(embed=embed)
                    return
        except:
            await ctx.send("Error!")

    @commands.group()
    @commands.is_owner()
    async def reboot(self, ctx):
        try:
            await ctx.send("Botを再起動しています。。")
            await asyncio.sleep(2)
            subprocess.run(["shutdown", "/r", "/t", "0"])
        except:
            await ctx.send("Error!")

    @commands.group()
    @commands.is_owner()
    async def exec(self, ctx, *, code: str):
        exec(code)
        msg = await ctx.send("コードを実行しました。")
        await msg.add_reaction("✅")

    @commands.group()
    @commands.is_owner()
    async def datacb(self, ctx, filename: str):
        msg = await ctx.send(file=discord.File(f"data/{filename}"))
        await msg.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(AdminCommand(bot))