import discord
from discord.ext import commands
import asyncio
import sys
import math

def create_nnid_code(nnid: str):return "\n".join(["30000000 10AD1C58\n10000000 50000000\n01100020 00000050"]+[f"{x[:8]} {x[8:]}"for x in[nnid.encode("utf-16be").hex()[i*16:i*16+16].ljust(16,"0")for i in range(len(nnid))]if x!="0"*16]+["00000000 000000FF\nD0000000 DEADCAFE"]).upper()

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_permissions()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def gnnid(self, ctx, name: str):
        embed=discord.Embed(title=f"NNID: {name}", description=f"{create_nnid_code(f"{name}")}", color=0x006eff)
        await ctx.send(embed=embed)

    @commands.group()
    @commands.has_permissions()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def cbuild(self, ctx):
        e = discord.Embed(title=f"Minecraftコマンドビルダー v1.1\nリアクションを付けて作ります。\n====================\n🌳..Giveコマンド\n😙..Clearコマンド\n⚔..Killコマンド\n💬..Sayコマンド\n✖..終了")
        cmds = ""
        msg = await ctx.send(embed=e)
        await msg.add_reaction("🌳")
        await msg.add_reaction("😙")
        await msg.add_reaction("⚔")
        await msg.add_reaction("💬")
        await msg.add_reaction("✖")
        try:
            while True:
                def check(r, u):
                    if u.id == ctx.author.id:
                        return r.message.id == msg.id
                    else:
                        return False
                r, _ = await self.bot.wait_for("reaction_add", check=check, timeout=10)
                await r.remove(ctx.author)
                if r.emoji == "🌳":
                    def checks(m=ctx.message):
                        return m.author == ctx.author
                    await ctx.send('アイテムIDを入れて')
                    numc = await self.bot.wait_for("message", check=checks, timeout=10)
                    await ctx.send("Giveコマンドを追加しました。")
                    cmds += f"\n/give @p {numc.content.replace("@", "＠").replace("\n", "")}"
                if r.emoji == "😙":
                    def checks(m=ctx.message):
                        return m.author == ctx.author
                    await ctx.send('アイテムIDを入れて')
                    numc = await self.bot.wait_for("message", check=checks, timeout=10)
                    await ctx.send('個数を入れて')
                    numcs = await self.bot.wait_for("message", check=checks, timeout=10)
                    await ctx.send("Clearコマンドを追加しました。")
                    cmds += f"\n/clear @p {numc.content.replace("@", "＠").replace("\n", "")} 0 {numcs.content.replace("@", "＠").replace("\n", "")}"
                elif r.emoji == "⚔":
                    def checks(m=ctx.message):
                        return m.author == ctx.author
                    await ctx.send('ユーザーネームを入れて')
                    numc = await self.bot.wait_for("message", check=checks, timeout=10)
                    await ctx.send("Killコマンドを追加しました。")
                    cmds += f"\n/kill {numc.content.replace("@", "＠").replace("\n", "")}"
                elif r.emoji == "💬":
                    def checks(m=ctx.message):
                        return m.author == ctx.author
                    await ctx.send('メッセージを入れて')
                    numc = await self.bot.wait_for("message", check=checks, timeout=10)
                    await ctx.send("Sayコマンドを追加しました。")
                    cmds += f"\n/say {numc.content.replace("@", "＠").replace("\n", "")}"
                elif r.emoji == "✖":
                    await ctx.send("コードが完成しました。")
                    await ctx.send(f"```{cmds}```")
                    break
        except asyncio.TimeoutError:
            return
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

async def setup(bot):
    await bot.add_cog(Minecraft(bot))