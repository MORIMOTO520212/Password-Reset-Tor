from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from mechanize import Browser
import os
import requests
import socket
import time
import sys



# -------------- 設定 -------------- #
# 最高スレッド数
max_thread = 3
# 接続タイムアウト設定
timeout = 5
# test
ids = [
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0
]
# ---------------------------------- #

proxies_list = []
for address in open("proxies_list.txt", "r").readlines():
    proxies_list.append(address.strip())



def thread(id, proxies, retry):
    try:
        br = Browser()
        # br.set_proxy("http://example.com:8080", "http")
        br.set_proxies(proxies)
        br.set_handled_schemes(['http', 'https'])
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", "Opera/9.30 (Nintendo Wii; U; ; 2047-7; en)")]
        res = requests.get("http://inet-ip.info/ip", proxies=proxies, timeout=timeout)
        print("connected successfully:", res.text)
        # ------------------------------ スクレイピング ------------------------------ #
        #br.open("https://twitter.com/account/begin_password_reset", timeout=10.0)
        #html = BeautifulSoup(br.response().read(), "html.parser")
        #title = html.find("title").text
        #body = html.find("body").text
        #print(body)
        # ----------------------------------------------------------------------------- #

    except Exception as e:
        #print("ERROR:", str(e))
        print("connection failed")
        # --- プロキシ変更 --- #
        proxies_list.remove(proxies_list[0])
        proxies = {
            "http": "http://"+proxies_list[0],
            "https": "https://"+proxies_list[0]
        }
        # 処理



def main(ids, retry):

    # スレッド設定
    th = ThreadPoolExecutor(max_workers=max_thread)


    for id in ids:
        try:
            proxies = {
                    "http": "http://"+proxies_list[0],
                    "https": "https://"+proxies_list[0]
            }
        except: pass

        # スレッド実行
        th.submit(thread, id, proxies, retry)

        try:
            proxies_list.remove(proxies_list[0])
        except: pass
        
    
    # スレッド終了
    th.shutdown()


# 関数実行
main(ids, 5)

print("\n終了")
input()
