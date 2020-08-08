from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import os
import requests
import socks
import socket
import time
import sys

# ~ フロー ~
# idlist.txtからユーザーIDを読み込む
# main関数実行　並列化
# pwReset.txt, protect.txtに書き込む


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



def thread(id, retry):

    for _ in range(retry):

        try:

            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            br = Browser()
            br.set_handle_robots(False)
            br.addheaders = [("User-agent", "Opera/9.30 (Nintendo Wii; U; ; 2047-7; en)")]

            # ------------------------------ スクレイピング ------------------------------ #
            print("{} 処理".format(id))
            # ----------------------------------------------------------------------------- #

        except KeyboardInterrupt:
            print("強制終了")
            os.system("taskkill /IM tor.exe /F")

            # ----------------------書き込み------------------------ #
            print("書き込み処理")
            # ----------------------------------------------------- #
            print("\n終了")
            input()
            exit()

        except TypeError:
            for regulation in regulation_list:
                if regulation in title:
                    print("規制")

                    # --- Torプロキシ変更 --- #
                    os.system("taskkill /IM tor.exe /F")
                    print("--------------------------------")
                    os.system("tor")
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

        # - Tor終了
        os.system("taskkill /IM tor.exe /F")

        # ----------------------書き込み------------------------ #
        print("書き込み処理")
        # ----------------------------------------------------- #

        print("\n終了")
        input()
        exit()


def main(ids, retry=5):

    # スレッド設定
    th = ThreadPoolExecutor(max_workers=max_thread)

    # - コマンドラインからtor呼び出し
    os.system("tor")

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
    ids = f.read().splitlines()

# 関数実行
main(ids, retry=5)

# ----------------------書き込み------------------------ #
print("書き込み処理")
# ----------------------------------------------------- #

# Torタスク終了
os.system("taskkill /IM tor.exe /F")

print("\n終了")
input()
