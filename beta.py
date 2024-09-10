import discord
from discord.ext import commands, tasks
import os
from pymongo import MongoClient
import asyncio
import pathlib
import sys
import json
import time
import requests
from threading import Thread
import subprocess
from flask import Flask, redirect, request, session, url_for

intents = discord.Intents().all()
intents.message_content = True
bot = commands.AutoShardedBot(command_prefix=("!"), intents=intents, help_command=None)

client = MongoClient('mongodb://localhost:27017')

perm_dic = {"add_reactions": "リアクションの追加", "administrator": "管理者", "attach_files": "ファイルを添付", "ban_members": "メンバーをBAN", "change_nickname": "ニックネームの変更", "connect": "接続(ボイスチャンネル)", "create_instant_invite": "招待を作成", "deafen_members": "メンバーのスピーカーをミュート", "embed_links": "埋め込みリンク", "external_emojis": "外部の絵文字を使用する", "external_stickers": "外部のスタンプを使用する(Use Ecternal Stickers)", "kick_members": "メンバーをキック", "manage_channels": "チャンネルの管理", "manage_emojis": "絵文字の管理", "manage_emojis_and_stickers": "絵文字・スタンプの管理", "manage_events": "", "manage_guild": "サーバー管理", "manage_messages": "メッセージの管理", "manage_nicknames": "ニックネームの管理", "manage_permissions": "ロールの管理", "manage_roles": "ロールの管理", "manage_threads": "スレッドの管理", "manage_webhooks": "ウェブフックの管理", "mention_everyone": "`@evryone`,`@here`,すべてのロールにメンション", "move_members": "メンバーを移動(ボイスチャンネル)", "mute_members": "メンバーをミュート", "priority_speaker": "優先スピーカー", "read_message_history": "メッセージ履歴を読む", "read_messages": "チャンネルを見る", "request_to_speak": "スピーカー参加権をリクエスト", "send_messages": "メッセージを送信", "send_tts_messages": "テキスト読み上げメッセージを送信する", "speak": "発言(ボイスチャンネル)", "stream": "WEBカメラ(映像を配信する)", "use_external_emojis": "外部の絵文字を使用する", "use_external_stickers": "外部のスタンプを使用する(Use Ecternal Stickers)", "use_private_threads": "非公開スレッドの使用(Private Thread)", "use_slash_commands": "スラッシュコマンドを使用", "use_threads": "公開スレッドの使用(Public Thread)", "use_voice_activation": "音声検出を使用", "value": "", "view_audit_log": "監査ログを表示", "view_channel": "チャンネルを見る", "view_guild_insights": "サーバーインサイトを見る", }

tokenjson = open('../token.json', 'r')
tokens = json.load(tokenjson)

def t_perm(perm):
    if perm in perm_dic:
        return perm_dic[perm]
    else:
        return perm

@bot.event
async def on_ready():
    os.system('cls')
    await bot.tree.sync()
    print("======================")
    print("  Created by もどっぐ  ")
    print("======================")
    print("Log >>")
    await bot.change_presence(activity=discord.CustomActivity(name=f"mo.help | {len(bot.guilds)}鯖-{len(bot.users)}人"))
    loopchp.start()

@tasks.loop(seconds=10)
async def loopchp():
    await bot.change_presence(activity=discord.CustomActivity(name=f"mo.help | {len(bot.guilds)}鯖-{len(bot.users)}人"))

@bot.event
async def on_guild_join(guild):
    try:
        client = MongoClient('mongodb://localhost:27017/')
        for mon in client["Main"]["BANServer"].find():
            if mon["IDs"] == f"{guild.id}":
                embed=discord.Embed(title="このサーバーはBANされています。", description="さようなら..", color=0x00ccff)
                if guild.system_channel:
                    await guild.system_channel.send(embed=embed)
                await guild.owner.send(embed=embed)
                await guild.leave()
        if guild.system_channel:
            embed=discord.Embed(title="ModoBotを入れていただきありがとうございます！", description="Created by もどっぐ(Axe-Owner)\nヘルプは、mo#helpで表示します。", color=0x00ccff)
            await guild.system_channel.send(embed=embed)
    except:
        return

@bot.event
async def on_message(message):
    if '!' in message.content:
        client = MongoClient('mongodb://localhost:27017/')
        for mon in client["Main"]["DisableCMD"].find():
            if mon["IDs"] == f"{message.channel.id}":
                try:
                    msg = await message.channel.send(embed=discord.Embed(title="コマンドが無効なチャンネルです", description="このメッセージは、3秒後に削除されます。"))
                    await asyncio.sleep(3)
                    await msg.delete()
                    return
                except:
                    continue
    await bot.process_commands(message)

@bot.event
async def setup_hook():
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            await bot.load_extension(f"cogs.{cog[:-3]}")

bot.run(tokens["token2"])