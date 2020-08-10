import requests, base64
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# ---------- ウィンドウを閉じた状態でChromeでウェブページを開きます ボット回避のため ---------- #
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get('http://free-proxy.cz/ja/proxylist/main/1')

html = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()
# ---------------------------------------------------------------------------------------- #

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
        print("Address: {}:{}".format(address, port))