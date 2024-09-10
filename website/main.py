from flask import Flask, render_template, request
from pymongo import MongoClient
import json
import requests
app = Flask(__name__)

@app.route('/gban')
def gban():
    tokenjson = open('../../token.json', 'r')
    tokens = json.load(tokenjson)
    mem = []
    client = MongoClient('mongodb://localhost:27017/')
    for mon in client["Main"]["GBANHist"].find():
        headers = {
            'Authorization': 'Bot ' + tokens["joho"],
            'Content-Type': 'application/json',
        }
        response = requests.get(f'https://discord.com/api/users/{mon["IDs"]}', headers=headers)
        mem.append(f"<img src='https://cdn.discordapp.com/avatars/{mon["IDs"]}/{response.json()["avatar"]}'><br>{response.json()["global_name"]}-{response.json()["id"]}")
    mem.reverse()
    return f"<big>GBANした危険者リスト</big><hr>{response.json()["global_name"]}-{response.json()["id"]}<br>{"<br>".join(mem)}"

@app.route('/userinfo/<int:user_id>')
def userinfo(user_id):
    try:
        tokenjson = open('../../token.json', 'r')
        tokens = json.load(tokenjson)
        headers = {
            'Authorization': 'Bot ' + tokens["joho"],
            'Content-Type': 'application/json',
        }
        response = requests.get(f'https://discord.com/api/users/{user_id}', headers=headers)
        return f"{response.json()["global_name"]}さんの情報。<br>アバター: <br><img src='https://cdn.discordapp.com/avatars/{response.json()["id"]}/{response.json()["avatar"]}'><br>ユーザーネーム: {response.json()["username"]}<br>ID: {response.json()["id"]}"
    except:
        return "エラー。"

@app.route('/')
def index():
    return "<a href='/gban'>GBAN者リスト</a>"

if __name__ == '__main__':
    app.run()