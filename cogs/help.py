import discord
from discord.ext import commands
import requests
import sys
import asyncio

class search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def ping(self, ctx):
        raw_ping = self.bot.latency
        ping = round(raw_ping * 1000)
        await ctx.reply(f"BotのPing値は{ping}msです。")

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def help(self, ctx, *, arg=None):
        if not arg:
            embed=discord.Embed(title=f"`{self.bot.user.display_name}`ヘルプへようこそ！", description=
                                "カテゴリ名一覧です。\n"\
                                "`bot` .. Bot関連のコマンドです。\n"\
                                "`fatal` .. 危険なコマンドです。\n"\
                                "`mod` .. モデレートコマンドです。\n"\
                                "`game` .. ゲームコマンドです。\n"\
                                "`fun` .. 面白いコマンドです。\n"\
                                "`global` .. グローバル関連のコマンドです。\n"\
                                "`panels` .. パネル関連のコマンドです。\n"\
                                "`search` .. 検索するコマンドです。\n"\
                                "`tools` .. ツールコマンドです。\n"\
                                "`setting` .. 設定コマンドです。\n"\
                                "`mo.help カテゴリ名`でカテゴリのヘルプが見れます。\n"\
                                "重要！ コマンド名は反応しません！"\
                                , color=discord.Color.red())
            await ctx.send(embed=embed)
        if arg == "bot":
            embed=discord.Embed(title="Bot関連", description=
                                "`help` .. あなたの今見ているコマンドです。\n"\
                                "`ping` .. Pingを図ります。\n"\
                                )
            await ctx.send(embed=embed)
        elif arg == "fatal":
            embed=discord.Embed(title="危険なコマンド関連", description=
                                "`chnick` .. ニックネームを統一します。\n"\
                                "`shuffle` .. ニックネームをシャッフルします。\n"\
                                "`nickreset` .. ニックネームをリセットします。"\
                                )
            await ctx.send(embed=embed)
        elif arg == "mod":
            embed=discord.Embed(title="モデレートコマンド関連", description=
                                "`kick` .. メンバーをキックします。\n"\
                                "`ban` .. メンバーをBANします。\n"\
                                "`warn` .. メンバーをWarnします。\n"\
                                "`purge` .. チャンネルをきれいにします\n"\
                                )
            await ctx.send(embed=embed)
        elif arg == "game":
            embed=discord.Embed(title="ゲーム関連", description=
                                "`uranai` .. 占います。\n"\
                                "`whn` .. 数字ゲームをします。\n"\
                                "`invert` .. 文字列を反転させます。\n"\
                                "`cli` .. 文字列の改行コードを変換します。\n"\
                                "`loop_trans` .. 繰り返し翻訳します。\n"\
                                "`lubl` .. ラッキーブロックを使います。\n"\
                                "`cbuild` .. Minecraftのコマンドを作成します。\n"\
                                )
            await ctx.send(embed=embed)
        elif arg == "image":
            embed=discord.Embed(title="画像コマンド関連", description=
                                "`hunter` .. ハンターさんの画像を送信します。\n"\
                                "`mhavatar` .. ハンターさんの画像を作成します。\n"\
                                "`shinchoku` .. 進捗を作成します。\n"\
                                "`robokasu` .. ロボかすを作成します。\n"\
                                "`yuta` .. ゆうたを作成します。\n"\
                                "`dragon` .. ドラゴンを作成します。\n"\
                                "`nikuyaki` .. お肉を焼きます。\n"\
                                "`yusha` .. 勇者を作成します。\n"\
                                "`riaju` .. リア充を爆発させます。\n"\
                                "`3ds` .. 3dsを作成します。\n"\
                                "`myqu` .. 説明がありません。\n"\
                                "`love` .. 説明がありません。\n"\
                                "`naguru` .. ヒカキンに殴られます。\n"\
                                "`5000` .. 5000兆円ほしい!\n"\
                                "`neko` .. にゃーん!\n"\
                                "`kemomimi` .. なんだこれ\n"\
                                )
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("⏭️")
            try:
                def check(r, u):
                    if u.id == ctx.author.id:
                        return r.message.id == msg.id
                    else:
                        return False
                r, _ = await self.bot.wait_for("reaction_add", check=check, timeout=10)
                await r.remove(ctx.author)
                if r.emoji == "⏭️":
                    await msg.delete()
                    embed=discord.Embed(title="画像コマンド関連", description=
                                        "`food` .. 食べ物を注文します。\n"\
                                        "`coffee` .. コーヒーを飲みます。\n"\
                                        "`kanna` .. 殴られます。\n"\
                                        "`poke` .. 突きます。\n"\
                                        "`dog` .. わんわん\n"\
                                        "`httpcat` .. HTTPCATを出現させます。\n"\
                                        "`fox` .. 狐を出します。\n"\
                                        "`nounai` .. 脳内メーカーをします。\n"\
                                        "`isekai` .. 異世界に行きます。\n"\
                                        "`kabuto` .. あなたの兜は？\n"\
                                        "`smartphone` .. スマホを見せて!!\n"\
                                        "`busho` .. 武将ってなにそれおいしいの？\n"\
                                        "`gifs` .. GIFを検索します。\n"\
                                        "`hikakin` .. 説明がありません。\n"\
                                        )
                    msg = await ctx.send(embed=embed)
            except asyncio.TimeoutError:
                return
        elif arg == "fun":
            embed=discord.Embed(title="面白いコマンド", description=
                                """
                                `image` .. image関連のコマンドです。(helpで見てね)
                                `suddendeath` .. 突然の死を作成します。
                                `yudachat` .. ゆだチャットをします。
                                `engjp` .. 英語から日本語に無理やり変換します。
                                """
                                )
            await ctx.send(embed=embed)
        elif arg == "global":
            embed=discord.Embed(title="グローバル関連", description=
                                "`talkglobal` .. グローバルチャットを作成します。\n"\
                                "`deactivate` .. グローバルチャットから退出します。\n"\
                                )
            await ctx.send(embed=embed)
        elif arg == "panels":
            embed=discord.Embed(title="パネルコマンド関連", description=
                                "`poll` .. アンケートをとります。\n"\
                                "`rolepanel` .. ロールパネルを作成します。\n"\
                                "`top` .. 最上部のメッセージに飛びます。\n"\
                                "`linkbutton` .. リンクボタンを作成します。\n"\
                                )
            await ctx.send(embed=embed)
        elif arg == "search":
            embed=discord.Embed(title="検索コマンド関連", description=
                                """
                                `google` .. Googleで検索します。
                                `amazon` .. アマゾンで検索します。
                                `safeweb` .. サイトを分析します。
                                `ggrks` .. Google検索をGGRKSドメインに変換します。
                                `niconico` .. NicoNico検索します。
                                `ulookup` .. ユーザーを検索します。
                                `slookup` .. サーバーを検索します。
                                `pypi` .. PyPiで検索します。
                                `mhnews` .. モンハンニュースを取得します。
                                `pcnews` .. PCのニュースを取得します。
                                """
                                )
            await ctx.send(embed=embed)
        elif arg == "tools":
            embed=discord.Embed(title="ツール関連", description=
                                """
                                `afk `.. AFKになります。
                                `wcalc` .. 電子レンジのwを変換します。(前のw, 何秒, 変換したいw)
                                `2ch` .. 2ch風に引用するよ
                                `shorturl` .. 短縮URLを作成するよ。
                                `trans` .. 日本語から英語に翻訳するよ。
                                `qrcode` .. QRコードを作成するするよ。
                                """
                                )
            await ctx.send(embed=embed)
        elif arg == "setting":
            embed=discord.Embed(title="設定関連", description=
                                """
                                `transch` .. 自動翻訳の設定。
                                `joinyuta` .. 空気を凍らせます
                                `joinhiro` .. ひろゆきを招待します。
                                `invcheck` .. 招待リンクを検出します。
                                `discmd` .. コマンド無効チャンネルを設定します。
                                `blom` .. 長いメッセージを無効にします。
                                `enagban` .. GBANを有効にし、サーバーを保護します。
                                `ar` .. 自動返信を設定します。(mo.help arで詳細。)
                                """
                                )
            await ctx.send(embed=embed)
        elif arg == "ar":
            embed=discord.Embed(title="自動返信関連", description=
                                """
                                `add` .. 自動返信を追加します。
                                `remove` .. 自動返信を消します。
                                `list` .. ARのリストを表示します
                                """
                                )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name = "slashelp", with_app_command = True, description = "スラッシュコマンドのヘルプを表示します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def slashelp(self, ctx):
        try:
            await ctx.send(embed=discord.Embed(title="スラッシュコマンド用ヘルプへようこそ！", description="```「ヘルプ」のカテゴリ\n/slashelp .. ヘルプを見ます。``````\n「あいさつ」のカテゴリ\n/hello .. こんにちは！をします。```\n=> Prefixコマンドは、mo!helpでお願いします。"))
        except:
            await ctx.send(f"{sys.exc_info()}")

async def setup(bot):
    await bot.add_cog(search(bot))