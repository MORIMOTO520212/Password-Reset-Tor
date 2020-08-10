from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

driver.get('http://free-proxy.cz/ja/proxylist/main/1')

print(driver.page_source)

driver.quit()