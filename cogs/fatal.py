import discord
from discord.ext import commands
import asyncio
import random
import sys
import time
import io
import json
import aiohttp
from pymongo import MongoClient
from discord import Webhook
import datetime

class Fatal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_warnlog(self, wuser: str, juser: str):
        try:
            chid = []
            client = MongoClient('mongodb://localhost:27017/')
            for channels in client["Main"]["GlobalChat"].find():
                if channels["Name"] == "warnlog":
                    try:
                        chid.append(channels["IDs"])
                    except:
                        continue

            for ch in chid:
                channel = self.bot.get_channel(int(ch))
                async with aiohttp.ClientSession() as session:
                    ch_webhooks = await channel.webhooks()
                    whname = f"ModoBot-Global-warnlog"
                    webhooks = discord.utils.get(ch_webhooks, name=whname)
                    if webhooks is None:
                        webhooks = await channel.create_webhook(name=f"{whname}")
                    webhook = Webhook.from_url(webhooks.url, session=session)
                    await webhook.send(f"`{wuser}`を`{juser}`がWarnしました。", username=f"🔨 WarnLogSystem", avatar_url=f"https://free-icons.net/wp-content/uploads/2020/09/symbol018.png")
        except:
            await self.bot.get_channel(1265894171747680298).send(f"{sys.exc_info()}")

    async def warn_handle(self, guild: discord.Guild, member: discord.Member, level: int):
        if level == 0:
            warndRole = discord.utils.get(guild.roles, name="ModoBot-Warn")
            await warndRole.edit(colour=discord.Colour.from_rgb(0, 0, 9))
            if not warndRole:
                warndRoleC = await guild.create_role(name="ModoBot-Warn")
                await warndRoleC.edit(colour=discord.Colour.from_rgb(0, 0, 9))
                await member.add_roles(warndRoleC)
                return
            await member.add_roles(warndRole)
        elif level == 1:
            try:
                duration = datetime.timedelta(minutes=5)
                await member.timeout(duration, reason="ModoBotによる、Warnです。")
                return
            except:
                return
        elif level == 2:
            await guild.kick(member, reason="ModoBotによる、WarnKickです。")
            return
        elif level == 3:
            await guild.ban(member, reason="ModoBotによる、WarnBANです。")
            return
        else:
            try:
                duration = datetime.timedelta(minutes=3)
                await member.timeout(duration, reason="ModoBotによる、Warnです。")
                return
            except:
                return

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, *, member: discord.Member):
        await ctx.guild.kick(member)
        await ctx.send(f'{member.mention}をKickしました。')

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, *, member: discord.Member):
        await ctx.guild.ban(member)
        await ctx.send(f'{member.mention}をBANしました。')

    @commands.group(aliases=["purge"])
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def clear_channel(self, ctx, a: int):
        if a == 0:
            await ctx.channel.purge()
            await ctx.send(f'チャンネルをきれいにしました。')
            return
        else:
            v = a + 1
            await ctx.channel.purge(limit=v)
            await ctx.send(f'チャンネルをきれいにしました。')
            return

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, level: int):
        await ctx.send(embed=discord.Embed(title=f"{member.display_name}をWarnしてみます。。"))
        await self.send_warnlog(member.display_name, ctx.author.display_name)
        await self.warn_handle(ctx.guild, member, level)
        await ctx.send(embed=discord.Embed(title=f"Warnが完了しました。"))

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def shuffle(self, ctx):
        member_nicks = []
        targets = []
        for m in ctx.guild.members:
            member_nicks.append(m.display_name)
            targets.append(m)

        try:

            loop = asyncio.get_event_loop()
            random.shuffle(member_nicks)

            for i, m in enumerate(targets):
                loop.create_task(m.edit(nick=member_nicks[i]))

            e = discord.Embed(title=f"`{len(member_nicks)}`人のニックネームをシャッフルしました。")
            await ctx.reply(embed=e)

        except:
            await ctx.reply(f"error!\n{sys.exc_info()}")

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def nickreset(self, ctx):
        targets = []
        for m in ctx.guild.members:
            targets.append(m)
        loop = asyncio.get_event_loop()
        for i, m in enumerate(targets):
            loop.create_task(m.edit(nick=None))  
        e = discord.Embed(title=f"`{len(targets)}`人のニックネームをリセットしました。")
        await ctx.reply(embed=e)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def chnick(self, ctx, a: str):
        targets = []
        for m in ctx.guild.members:
            targets.append(m)
        loop = asyncio.get_event_loop()
        for i, m in enumerate(targets):
            loop.create_task(m.edit(nick=a))  
        e = discord.Embed(title=f"`{len(targets)}`人のニックネームを`{a}`にしました。")
        await ctx.reply(embed=e)

async def setup(bot):
    await bot.add_cog(Fatal(bot))