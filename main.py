from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from mechanize import Browser
import subprocess
import requests
import socks
import socket
import time
import sys

# idlist.txtからユーザーIDを読み込む
# main関数実行
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
pwReset   = []
# 保護済み
protected = []

# プロキシリストの読み込み
with open("proxylist.txt") as f:
    proxylist = f.read().splitlines() # 一行ずつ

def main(ids, retry=5):

    # コマンドラインからtor呼び出し
    subprocess.Popen("tor")

    # プロキシ設定
    proxies = {"http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"}

    # 自分のIPを表示
    res = requests.get("http://inet-ip.info/ip", proxies=proxies)
    print(res.text)
    print()

    for id in ids:

        for i in range(retry):

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

                with open("pwReset.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(pwReset))

                with open("protected.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(protected))

                print("\n終了")
                input()
                exit()

            except TypeError:
                for regulation in regulation_list:
                    if regulation in title:
                        print("規制")
                        subprocess.run("taskkill /IM tor.exe /F")
                        print("--------------------------------")
                        subprocess.Popen("tor")
                        print()
                        # 自分のIPアドレスを表示する
                        res = requests.get("http://inet-ip.info/ip", proxies=proxies)
                        print(res.text)
                        print()
                        pass
                    pass
                break

            else:
                break

        else:
            print("5回試行しましたが実行できませんでした。")
            subprocess.run("taskkill /IM tor.exe /F")

            with open("pwReset.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(pwReset))

            with open("protected.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(protected))

            print("\n終了")
            input()
            exit()


# IDリスト読み込み
with open("idlist.txt") as f:
    ids = f.read().splitlines() # 一行ずつ

main(ids, retry=5)

with open("pwReset.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(pwReset))
with open("protected.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(protected))

subprocess.run("taskkill /IM tor.exe /F")

print("\n終了")
input()
