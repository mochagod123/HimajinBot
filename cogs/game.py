import discord
from discord.ext import commands
import random
import asyncio
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance
import io
import sys
from googletrans import Translator

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name = "uranai", with_app_command = True, description = "占いをします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def uranai(self, ctx):
        unsei = ["大吉", "中吉", "吉", "末吉", "小吉", "凶", "大凶"]
        choice = random.choice(unsei)
        await ctx.send(choice)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def invert(self, ctx, text: str):
        textf = text[::-1]
        embed=discord.Embed(title="文字列を反転", color=0xbce7ff)
        embed.add_field(name="反転前", value=f"{text}", inline=False)
        embed.add_field(name="反転後", value=f"{textf}", inline=False)
        await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def cli(self, ctx, text: str):
        embed=discord.Embed(title="改行コードを改行に変換", color=0x00d5ff)
        embed.add_field(name="変換前", value=f"{text.replace("@", "＠")}", inline=False)
        embed.add_field(name="変換後", value=f"{text.replace("\\n", "\n").replace("@", "＠").replace("<br>", "\n")}", inline=False)
        embed.add_field(name="対応コード", value="\\n, <br>")
        await ctx.reply(embed=embed)

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def loop_trans(self, ctx, text: str):
        try:
            translator = Translator()
            jpen = translator.translate(text, src='ja', dest='en')
            enfr = translator.translate(jpen.text, src='en', dest='fr')
            frch = translator.translate(enfr.text, src='fr', dest='zh-cn')
            chjp = translator.translate(frch.text, src='zh-cn', dest='ja')
            c = discord.Embed(title=f"{text}", description=f"JP->EN->FR->ZH->JP")
            msg = await ctx.send(embed=c)
            await asyncio.sleep(2)
            v = discord.Embed(title=f"{jpen.text}", description=f"JP->EN->FR->ZH->JP")
            await msg.edit(embed=v)
            await asyncio.sleep(2)
            a = discord.Embed(title=f"{enfr.text}", description=f"JP->EN->FR->ZH->JP")
            await msg.edit(embed=a)
            await asyncio.sleep(2)
            c = discord.Embed(title=f"{frch.text}", description=f"JP->EN->FR->ZH->JP")
            await msg.edit(embed=c)
            await asyncio.sleep(2)
            s = discord.Embed(title=f"{chjp.text}", description=f"JP->EN->FR->ZH->JP")
            await msg.edit(embed=s)
            await asyncio.sleep(2)
            await ctx.reply("LoopTransが終了しました。")
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

    @commands.hybrid_command(name = "lubl", with_app_command = True, description = "ラッキーブロックをします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def lubl(self, ctx):
        try:
            embed = discord.Embed(title="ラッキーブロック", color=0xED900D)
            embed.set_thumbnail(url="https://play-lh.googleusercontent.com/Df6zwvxb2yjXI-vSQnBzlPfltmTeb8Kf4drJMTkOtqQbaDpUKN7-OuW7s3gpltJCfgcQ")
            imagelis = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzDPALvPaqwXC1WSIn4H3DLzO4IirsjYi8Yw&s", "https://img.game8.jp/1683801/e12428e9ef4239d330b7eb6fc61148b8.png/show", "https://static.wikia.nocookie.net/minecraft_ja_gamepedia/images/6/6a/Diamond_Sword_JE2_BE2.png/revision/latest?cb=20190716024931"]
            embed.set_image(url=random.choice(imagelis))
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")
            return

    @commands.hybrid_command(name = "janken", with_app_command = True, description = "じゃんけんします。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def janken(self, ctx):
        jankenk = ["ぼくのかち", "ぼくのまけ、、", "あいこ。"]
        e = discord.Embed(title=f"じゃんけん", description="リアクションをつけてね")
        msg = await ctx.send(embed=e)
        await msg.add_reaction("✊")
        await msg.add_reaction("✌️")
        await msg.add_reaction("🖐️")
        def check(r, u):
            if u.id == ctx.author.id:
                return r.message.id == msg.id
            else:
                return False
        try:
            r, _ = await self.bot.wait_for("reaction_add", check=check, timeout=20)
            await r.remove(ctx.author)
            await msg.delete()
            if r.emoji == "✊":
                await ctx.send(embed=discord.Embed(title=random.choice(jankenk)))
            elif r.emoji == "✌️":
                await ctx.send(embed=discord.Embed(title=random.choice(jankenk)))
            elif r.emoji == "🖐️":
                await ctx.send(embed=discord.Embed(title=random.choice(jankenk)))
        except asyncio.TimeoutError:
            return

async def setup(bot):
    await bot.add_cog(Game(bot))