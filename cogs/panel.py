import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import json
import asyncio
from pymongo import MongoClient
import sys
import time
from googletrans import Translator
import aiohttp
import string

COOLDOWN_AMOUNT = 2.0  # seconds
last_executed = time.time()
def assert_cooldown():
    global last_executed  # you can use a class for this if you wanted
    if last_executed + COOLDOWN_AMOUNT < time.time():
        last_executed = time.time()
        return True
    return False

class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def ank(self, ctx, *, arg):
        try:
            if arg:
                aka = arg.split(' ')
                a = aka[1]
                b = aka[2]
                c = aka[3].replace("None", "*")
                d = aka[4].replace("None", "*")
                e = aka[5].replace("None", "*")
                embed=discord.Embed(title=f"{aka[0]}", description=f"```[1] ... {a}\n[2] ... {b}\n[3] ... {c}\n[4] ... {d}\n[5] ... {e}```\n下のリアクションを付けて答えてください。", color=0xa6c412)
                m = await ctx.send(embed=embed)
                await m.add_reaction("<:1_:1266356576948850780>")
                await m.add_reaction("<:2_:1266356598524215326>")
                await m.add_reaction("<:3_:1266633035907072062>")
                await m.add_reaction("<:4_:1266633061303324682>")
                await m.add_reaction("<:5_:1266633990341660733>")
            else:
                await ctx.send("エラー。")
        except:
            await ctx.send("エラー。\n5つ必ず埋める必要があります。\n空いている場合は、「None」でうめてください。")

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def oldrolepanel(self, ctx, role: discord.Role):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            try:
                embed=discord.Embed(title=f"{role.name}", description=f"リアクションでロールを入手する", color=0xa6c412)
                m = await ctx.send(embed=embed)
                await m.add_reaction("🏅")
                add_datad = {f"IDs": f"{m.id}"}
                client['Main']["RolePanel"].delete_one(add_datad)
                add_data = {f"IDs": f"{m.id}", f"Role": f"{role.id}"}
                client['Main']["RolePanel"].insert_one(add_data)
                await ctx.message.delete()
            except:
                await ctx.send("Error!")
        except:
            await ctx.send(f"{sys.exc_info()}")


    @commands.hybrid_command(name = "top", with_app_command = True, description = "最前面に移動します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def top(self, ctx):
        try:
            lists = []
            async for ad in ctx.channel.history(limit=1, oldest_first=True):
                lists.append(ad.jump_url)
            embed = discord.Embed(title="最上部に移動する", url=lists[0])
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"{sys.exc_info()}")

    @commands.hybrid_command(name = "linkbutton", with_app_command = True, description = "URLをボタンにします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def linkbutton(self, ctx, url: str):
        try:
            await ctx.message.delete()
            embed = discord.Embed(title=f"{url}", url=f"{url}")
            embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"{sys.exc_info()}")

    @commands.hybrid_command(name = "rolepanel", with_app_command = True, description = "ロールパネルを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def rolepanel(self, ctx, title: str, role1: discord.Role, role2: discord.Role = None, role3: discord.Role = None, role4: discord.Role = None, role5: discord.Role = None):
        try:
            await ctx.message.delete()
            rolename = []
            rolename.append(f"1.{role1.mention}")
            if not role2 == None:
                rolename.append(f"2.{role2.mention}")
            if not role3 == None:
                rolename.append(f"3.{role3.mention}")
            if not role4 == None:
                rolename.append(f"4.{role4.mention}")
            if not role5 == None:
                rolename.append(f"5.{role5.mention}")
            embed = discord.Embed(title=f"{title}", description=f"{"\n".join(rolename)}")
            m = await ctx.send(embed = embed)
            await m.add_reaction("1️⃣")
            await m.add_reaction("2️⃣")
            await m.add_reaction("3️⃣")
            await m.add_reaction("4️⃣")
            await m.add_reaction("5️⃣")
            await asyncio.sleep(1)
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"IDs": f"{m.id}"}
            client['Main']["NRP"].delete_one(add_datad)
            if role5:
                add_data = {f"IDs": f"{m.id}", f"Role1": f"{role1.id}", f"Role2": f"{role2.id}", f"Role3": f"{role3.id}", f"Role4": f"{role4.id}", f"Role5": f"{role5.id}"}
            elif role4:
                add_data = {f"IDs": f"{m.id}", f"Role1": f"{role1.id}", f"Role2": f"{role2.id}", f"Role3": f"{role3.id}", f"Role4": f"{role4.id}"}
            elif role3:
                add_data = {f"IDs": f"{m.id}", f"Role1": f"{role1.id}", f"Role2": f"{role2.id}", f"Role3": f"{role3.id}"}
            elif role2:
                add_data = {f"IDs": f"{m.id}", f"Role1": f"{role1.id}", f"Role2": f"{role2.id}"}
            else:
                add_data = {f"IDs": f"{m.id}", f"Role1": f"{role1.id}"}
            client['Main']["NRP"].insert_one(add_data)
        except:
            await ctx.send(f"{sys.exc_info()}")

    @commands.hybrid_command(name = "mhw_panel", with_app_command = True, description = "MHWの武器をもぎ取るパネルを作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def mhww_panel(self, ctx):
        client = MongoClient('mongodb://localhost:27017/')
        m = await ctx.send(embed=discord.Embed(title="MHWの武器をランダムに取得", color=discord.Color.red()))
        await m.add_reaction("🔍")
        add_datad = {f"IDs": f"{m.id}"}
        client['Main']["MHWWPanel"].delete_one(add_datad)
        client['Main']["MHWWPanel"].insert_one(add_datad)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, pl):
        try:
            if pl.member.bot:
                return
            if not assert_cooldown():
                return
            client = MongoClient('mongodb://localhost:27017/')
            for mon in client["Main"]["RolePanel"].find():
                if mon["IDs"] == f"{pl.message_id}":
                    guild = self.bot.get_guild(pl.guild_id)
                    member = guild.get_member(pl.user_id)
                    role = guild.get_role(int(mon["Role"]))
                    await member.add_roles(role)
                    channel = self.bot.get_channel(pl.channel_id)
                    msg = await channel.send(f"{role.name}を{member.name}に付与しました。")
                    await asyncio.sleep(3)
                    await msg.delete()
                else:
                    continue
            for mon in client["Main"]["NRP"].find():
                if mon["IDs"] == f"{pl.message_id}":
                    channel = self.bot.get_channel(pl.channel_id)
                    guild = self.bot.get_guild(pl.guild_id)
                    member = guild.get_member(pl.user_id)
                    if pl.emoji.name == "1️⃣":
                        try:
                            role = guild.get_role(int(mon["Role1"]))
                        except:
                            msg = await channel.send(f"そこは登録されてないよ！")
                            await asyncio.sleep(3)
                            await msg.delete()
                            return
                    elif pl.emoji.name == "2️⃣":
                        try:
                            role = guild.get_role(int(mon["Role2"]))
                        except:
                            msg = await channel.send(f"そこは登録されてないよ！")
                            await asyncio.sleep(3)
                            await msg.delete()
                            return
                    elif pl.emoji.name == "3️⃣":
                        try:
                            role = guild.get_role(int(mon["Role3"]))
                        except:
                            msg = await channel.send(f"そこは登録されてないよ！")
                            await asyncio.sleep(3)
                            await msg.delete()
                            return
                    elif pl.emoji.name == "4️⃣":
                        try:
                            role = guild.get_role(int(mon["Role4"]))
                        except:
                            msg = await channel.send(f"そこは登録されてないよ！")
                            await asyncio.sleep(3)
                            await msg.delete()
                            return
                    elif pl.emoji.name == "5️⃣":
                        try:
                            role = guild.get_role(int(mon["Role5"]))
                        except:
                            msg = await channel.send(f"そこは登録されてないよ！")
                            await asyncio.sleep(3)
                            await msg.delete()
                            return
                    else:
                        msg = await channel.send(f"エラー。\n{pl.emoji}")
                        await asyncio.sleep(3)
                        await msg.delete()
                        return
                    await member.add_roles(role)
                    msmm = await channel.fetch_message(pl.message_id)
                    await msmm.remove_reaction(pl.emoji, member)
                    msg = await channel.send(f"{role.name}を{member.name}に付与しました。")
                    await asyncio.sleep(3)
                    await msg.delete()
                else:
                    continue
            for mon in client["Main"]["MHWWPanel"].find():
                if mon["IDs"] == f"{pl.message_id}":
                    channel = self.bot.get_channel(pl.channel_id)
                    guild = self.bot.get_guild(pl.guild_id)
                    member = guild.get_member(pl.user_id)
                    url = f"https://mhw-db.com/weapons/{random.randint(1, 800)}"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            jsonData = await response.json()
                            embed = discord.Embed(title=jsonData["name"], color=0x702f00)
                            embed.set_image(url=jsonData['assets']['image'])
                            embed.set_thumbnail(url=jsonData['assets']['icon'])
                    msmm = await channel.fetch_message(pl.message_id)
                    await msmm.remove_reaction(pl.emoji, member)
                    member = guild.get_member(pl.user_id)
                    msg = await channel.send(embed=embed)
                    await asyncio.sleep(5)
                    await msg.delete()
        except:
            print(f"{sys.exc_info()}")
            return

async def setup(bot):
    await bot.add_cog(Panel(bot))