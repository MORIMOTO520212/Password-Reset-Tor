from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from mechanize import Browser
import subprocess
import requests
import socks
import socket
import time
import sys

# ~ フロー ~
# idlist.txtからユーザーIDを読み込む
# main関数実行　並列化
# pwReset.txt, protect.txtに書き込む

keywords_list = ["Request help signing in to your account."]

# 規制リスト
regulation_list = [
    "Réinitialisation du mot de passe",
    "Passwortrücksetzung",
    "Wachtwoordherstel",
    "Password Reset",
    "パスワードをリセット",
    "Restablecimiento de contraseña",
    "Lösenordsåterställning",
    "Resetowanie hasła",
    "Salasanan nollaus",
    "Сброс пароля",
]

# パスワードリセット
pwReset       = []
# 保護済み
protected     = []
# IDリストファイルパス
idlistPath    = "idlist.txt"
# パスワードリセットファイルパス
pwResetPath   = "pwReset.txt"
# 保護済みファイルパス
protectedPath = "protected.txt"
# プロキシリストファイルパス
proxylistPath = "proxylist.txt"
# 最高スレッド数
max_thread    = 3

# プロキシリストの読み込み
with open(proxylistPath, "r") as f:
    proxylist = f.read().splitlines() # 一行ずつ

def thread(id, retry):

    for _ in range(retry):

        try:

            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            br = Browser()
            br.set_handle_robots(False)
            br.addheaders = [("User-agent", "Opera/9.30 (Nintendo Wii; U; ; 2047-7; en)")]

            # リンクを開く　タイムアウト10秒
            br.open("https://twitter.com/account/begin_password_reset", timeout=10.0)
            # フォーム選択
            br.select_form(action="/account/begin_password_reset")
            # ユーザー名入力
            br["account_identifier"] = id
            # 検索
            br.submit()

            html = BeautifulSoup(br.response().read(), "html.parser")
            title = html.find("title").text
            body = html.find("body").text

            for keyword in keywords_list:
                if keyword in title:

                    print("パスリセメソッド不在")
                    break

            soupobject = BeautifulSoup(br.response().read(), "html.parser")
            mailaddresses = soupobject.find_all("strong")
            fullname = soupobject.find_all("b")
            willwritedata = id

            for mailaddress in mailaddresses:
                willwritedata += "," + mailaddress.text

            for fullname in fullname:
                fullname = fullname.text

            print(fullname)
            print(willwritedata + "\n")
            pwReset.append(fullname + "," + willwritedata + "\n")
            print("--------------------------------")

        except KeyboardInterrupt:
            print("強制終了")
            subprocess.run("taskkill /IM tor.exe /F")

            # ----------------------書き込み------------------------ #
            with open(pwResetPath, "w", encoding="utf-8") as f:
                f.write("\n".join(pwReset))

            with open(protectedPath, "w", encoding="utf-8") as f:
                f.write("\n".join(protected))
            # ----------------------------------------------------- #
            print("\n終了")
            input()
            exit()

        except TypeError:
            for regulation in regulation_list:
                if regulation in title:
                    print("規制")
                    # - Torタスク終了
                    subprocess.run("taskkill /IM tor.exe /F")
                    print("--------------------------------")
                    # - コマンドラインからtor呼び出し
                    subprocess.Popen("tor")
                    print()
                    # - 自分のIPアドレスを表示する
                    res = requests.get("http://inet-ip.info/ip", proxies=proxies)
                    print(res.text)
                    print()
                    pass
                pass
            break

        # - 正常終了後、ループを抜ける
        else:
            break

    else:
        print("5回試行しましたが実行できませんでした。")
        subprocess.run("taskkill /IM tor.exe /F")

        # ----------------------書き込み------------------------ #
        with open(pwResetPath, "w", encoding="utf-8") as f:
            f.write("\n".join(pwReset))

        with open(protectedPath, "w", encoding="utf-8") as f:
            f.write("\n".join(protected))
        # ----------------------------------------------------- #

        print("\n終了")
        input()
        exit()

def main(ids, retry=5):

    # スレッド設定
    th = ThreadPoolExecutor(max_workers=max_thread)

    # - コマンドラインからtor呼び出し
    subprocess.Popen("tor")

    # - プロキシ設定
    proxies = {"http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"}

    # - 自分のIPを表示
    res = requests.get("http://inet-ip.info/ip", proxies=proxies)
    print(res.text)
    print()

    for id in ids:
        # スレッド実行
        th.submit(thread, id, retry)
    th.shutdown()

# IDリスト読み込み
with open(idlistPath, "r") as f:
    ids = f.read().splitlines() # 一行ずつ

# 関数実行
main(ids, retry=5)

# ----------------------書き込み------------------------ #
with open(pwResetPath, "w", encoding="utf-8") as f:
    f.write("\n".join(pwReset))
with open(protectedPath, "w", encoding="utf-8") as f:
    f.write("\n".join(protected))
# ----------------------------------------------------- #

# Torタスク終了
subprocess.run("taskkill /IM tor.exe /F")

print("\n終了")
input()
