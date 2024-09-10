import discord
from discord.ext import commands
import sys

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def getid(self, ctx, mem: discord.User = None):
        try:
            if not mem == None:
                await ctx.send(embed=discord.Embed(title=f"{mem.display_name}さんのユーザーIDは、`{mem.id}`です。", color=discord.Color.green()))
                return
            await ctx.send(embed=discord.Embed(title=f"あなたのユーザーIDは、`{ctx.author.id}`です。", color=discord.Color.green()))
        except:
            await ctx.send("Error!")

async def setup(bot):
    await bot.add_cog(info(bot))