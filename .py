from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from mechanize import Browser
import os
import requests
import base64
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
success_count = 0
connect_count = 0

def thread(id, proxies, retry):
    global success_count, connect_count
    connect_count += 1
    print("connection:", proxies_list[0])
    try:
        br = Browser()
        # br.set_proxy("http://example.com:8080", "http")
        br.set_proxies(proxies)
        br.set_handled_schemes(['http', 'https'])
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", "Opera/9.30 (Nintendo Wii; U; ; 2047-7; en)")]
        res = requests.get("http://inet-ip.info/ip", proxies=proxies, timeout=timeout)
        print("connected successfully:", res.text)
        success_count += 1
        # ------------------------------ スクレイピング ------------------------------ #
        #br.open("https://twitter.com/account/begin_password_reset", timeout=10.0)
        #html = BeautifulSoup(br.response().read(), "html.parser")
        #title = html.find("title").text
        #body = html.find("body").text
        #print(body)
        # ----------------------------------------------------------------------------- #

    except Exception as e:
        print("connection failed",str(e))
        # --- プロキシ変更 --- #
        proxies_list.remove(proxies_list[0])
        proxies = {
            "http": "http://"+proxies_list[0],
            "https": "https://"+proxies_list[0]
        }


def main(ids, retry):
    # page
    page = 1

    # スレッド設定
    th = ThreadPoolExecutor(max_workers=max_thread)


    for id in ids:

        # ---------------- プロキシ追加 ---------------- #
        if [] == proxies_list:
            req = requests.get("http://free-proxy.cz/ja/proxylist/main/"+str(page))
            page += 1
            html = BeautifulSoup(req.text, "html.parser")
            tr = html.find_all("tr")
            for _tr in tr:
                address = ''
                port    = ''
                td = _tr.find_all("td")
                if 2 < len(td):
                    port    = td[1].find("span").get_text()
                    script  = td[0].find("script").string
                    _base64 = script.replace("document.write(Base64.decode(\"", "").replace("\"))", "")
                    address = base64.b64decode(_base64).decode()
                    #proxies_list.append('{}:{}'.format(address, port))
                    proxies_list.append(address)
        # ---------------------------------------------- #
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

print("終了")
prtcentage = int((success_count/connect_count)*100)
print("接続成功率：{}%".format(str(prtcentage)))
input()
