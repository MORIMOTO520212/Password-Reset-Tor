from selenium import webdriver
import requests, os, re
from selenium.webdriver.chrome.options import Options

print("プロキシの設定　例）54.197.199.34:80")
PROXY = input('Proxy Address: ').strip()
print("プロキシからのレスポンスを待機しています。")
os.system('ping {}'.format(re.sub(':.*', '', PROXY)))
options = Options()
options.add_argument('--proxy-server=http://%s' % PROXY)
print(f"[{PROXY}] 接続中...")
try:driver = webdriver.Chrome(chrome_options=options)
except Exception as e:
    if 'chromedriver' in str(e):
        input("エラー：\nカレントディレクトリにchromedriver.exeが見つかりませんでした。\nchromedriver.exeをカレントディレクトに配置してください。")
        exit()
driver.get("http://inet-ip.info")
print(f"[{PROXY}] プロキシの接続完了。")
input("終了する場合はエンターを押してください。")
driver.quit()