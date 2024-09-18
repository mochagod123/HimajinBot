import discord
from discord.ext import commands, tasks
import sys
from pymongo import MongoClient
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import random
import datetime

perm_dic = {"add_reactions": "リアクションの追加", "administrator": "管理者", "attach_files": "ファイルを添付", "ban_members": "メンバーをBAN", "change_nickname": "ニックネームの変更", "connect": "接続(ボイスチャンネル)", "create_instant_invite": "招待を作成", "deafen_members": "メンバーのスピーカーをミュート", "embed_links": "埋め込みリンク", "external_emojis": "外部の絵文字を使用する", "external_stickers": "外部のスタンプを使用する(Use Ecternal Stickers)", "kick_members": "メンバーをキック", "manage_channels": "チャンネルの管理", "manage_emojis": "絵文字の管理", "manage_emojis_and_stickers": "絵文字・スタンプの管理", "manage_events": "", "manage_guild": "サーバー管理", "manage_messages": "メッセージの管理", "manage_nicknames": "ニックネームの管理", "manage_permissions": "ロールの管理", "manage_roles": "ロールの管理", "manage_threads": "スレッドの管理", "manage_webhooks": "ウェブフックの管理", "mention_everyone": "`@evryone`,`@here`,すべてのロールにメンション", "move_members": "メンバーを移動(ボイスチャンネル)", "mute_members": "メンバーをミュート", "priority_speaker": "優先スピーカー", "read_message_history": "メッセージ履歴を読む", "read_messages": "チャンネルを見る", "request_to_speak": "スピーカー参加権をリクエスト", "send_messages": "メッセージを送信", "send_tts_messages": "テキスト読み上げメッセージを送信する", "speak": "発言(ボイスチャンネル)", "stream": "WEBカメラ(映像を配信する)", "use_external_emojis": "外部の絵文字を使用する", "use_external_stickers": "外部のスタンプを使用する(Use Ecternal Stickers)", "use_private_threads": "非公開スレッドの使用(Private Thread)", "use_slash_commands": "スラッシュコマンドを使用", "use_threads": "公開スレッドの使用(Public Thread)", "use_voice_activation": "音声検出を使用", "value": "", "view_audit_log": "監査ログを表示", "view_channel": "チャンネルを見る", "view_guild_insights": "サーバーインサイトを見る", }

def t_perm(perm):
    if perm in perm_dic:
        return perm_dic[perm]
    else:
        return perm

class system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.sendads.start()
        self.sendnews.start()
        self.sendtenki.start()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            a = None
            return a
        elif isinstance(err, commands.BotMissingPermissions):
            p = "\n".join([t_perm(perm) for perm in err.missing_permissions])
            embed=discord.Embed(title="Botの権限がありません!", description=f"{p}", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(err, commands.MissingPermissions):
            p = "\n".join([t_perm(perm) for perm in err.missing_permissions])
            embed=discord.Embed(title="あなたの権限がありません!", description=f"{p}", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(err, commands.errors.MissingRequiredArgument ):
            await ctx.send(embed=discord.Embed(title="引数が足りません。", description=f"```{err}```", color=0xff0000))
        elif isinstance(err, commands.errors.NotOwner ):
            await ctx.send(embed=discord.Embed(title="あなたはオーナーではありません！", description=f"```{err}```", color=0xff0000))
        else:
            await ctx.send(embed=discord.Embed(title="エラーが発生しました。", description=f"```{err}```", color=0xff0000))

    @tasks.loop(hours=2)
    async def sendads(self):
        ads = ["現在広告募集中です！"]
        chid = []
        client = MongoClient('mongodb://localhost:27017/')
        for channels in client["Main"]["TaskAds"].find():
            chid.append(channels["IDs"])
        for ch in chid:
            try:
                adschannel = self.bot.get_channel(int(ch))
                await adschannel.send(f'{random.choice(ads)}')
                await asyncio.sleep(0.8)
            except:
                continue

    @tasks.loop(hours=2)
    async def sendnews(self):
        chid = []
        client = MongoClient('mongodb://localhost:27017/')
        for channels in client["Main"]["News"].find():
            chid.append(channels["IDs"])
        for ch in chid:
            try:
                adschannel = self.bot.get_channel(int(ch))
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://www3.nhk.or.jp/news/') as response:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        title = soup.find_all('h1', class_="content--header-title")[0]
                        urls = title.find_all('a')[0]
                        await adschannel.send(f'https://www3.nhk.or.jp{urls["href"]}')
                        await asyncio.sleep(0.8)
            except:
                continue

    @tasks.loop(hours=2)
    async def sendtenki(self):
        dt_now = datetime.datetime.now()
        chid = []
        client = MongoClient('mongodb://localhost:27017/')
        for channels in client["Main"]["Tenki"].find():
            chid.append(channels["IDs"])
        for ch in chid:
            try:
                adschannel = self.bot.get_channel(int(ch))
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://tenki.jp/forecast/3/16/4410/13104/') as response:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        title = soup.find_all('p', class_="weather-telop")[0]
                        embed = discord.Embed(title=f"天気は、{title.get_text()}", description="東京の天気です。")
                        await adschannel.send(embed=embed)
                        await asyncio.sleep(0.8)
            except:
                continue

async def setup(bot):
    await bot.add_cog(system(bot))