from yt_dlp import YoutubeDL
import sys
import discord_webhook
import os
import json
from flask import Flask, render_template, request
import threading

DLl = []

app = Flask(__name__)

def Run():
    while True:
        for ll in DLl:
            try:
                DL(ll.split(",")[0], ll.split(",")[1], ll.split(",")[2])
            except:
                continue

def DL(url, filename, wurl):
    if not "youtube" in url:
        webhook = discord_webhook.DiscordWebhook(url=wurl, username="YTDL-ModoBot", content="これはDLできません。")

        response = webhook.execute()

        DLl.remove(f'{url},{filename},{wurl}')

        return

    webhook = discord_webhook.DiscordWebhook(url=wurl, username="YTDL-ModoBot", content="ダウンロードを開始します。。")

    response = webhook.execute()

    ydl_opts = {
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'max_filesize': 700000000,
        'quiet': True,
        'no_warnings': True,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'Sound/{filename}.%(ext)s'
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)

    try:

        webhook = discord_webhook.DiscordWebhook(url=wurl, username="YTDL-ModoBot")

        with open(f"Sound/{filename}.mp4", "rb") as f:
            webhook.add_file(file=f.read(), filename="Video.mp4")

        response = webhook.execute()
    except:
        os.remove(f"Sound/{filename}.mp4")

        DLl.remove(f'{url},{filename},{wurl}')

        return

    os.remove(f"Sound/{filename}.mp4")

    DLl.remove(f'{url},{filename},{wurl}')

    return "OK"

@app.route("/ytdl", methods=['POST'])
def ytdl():
    switch = request.data.decode('utf-8')  # デコード
    switch = json.loads(switch)

    DLl.append(f"{switch["url"]},{switch["filename"]},{switch["webhookurl"]}")

    return f"{len(DLl)}個待機しています。。"

@app.route("/dlist")
def dlist():
    return f"{len(DLl)}個待機しています。。"

def RR():
    app.run(debug=False, port=5001)

if __name__ == '__main__':
    thread1 = threading.Thread(target=RR)
    thread1.start()
    Run()