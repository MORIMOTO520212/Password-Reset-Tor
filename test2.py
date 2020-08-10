import requests, base64
from bs4 import BeautifulSoup

req = requests.get("http://free-proxy.cz/ja/proxylist/main/1")

html = BeautifulSoup(req.text, "html.parser")
tr = html.find_all("tr")

for _tr in tr:
    address = ''
    port    = ''
    td = _tr.find_all("td")
    script = td[0].find("script").get_text()
    span   = td[1].find("span").get_text()
    if "Base64.decode" in script:
        _base64 = script.replace("document.write(Base64.decode(\"", "").replace("\"))", "")
        address = base64.b64decode(_base64)
        print("Address:",address+span)