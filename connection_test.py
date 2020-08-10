import requests

success_count = 0
connect_count = 0
for prox in open("proxies_list.txt", "r").readlines():
    connect_count += 1
    try:
        proxies = {
                "http": "http://"+prox.strip(),
                "https": "https://"+prox.strip()
        }

        res = requests.get("http://inet-ip.info/ip", proxies=proxies, timeout=5)
        print("connected successfully:", res.text)
        success_count += 1
    except Exception as e:
        print(str(e))


prtcentage = (success_count/connect_count)*100
print("接続成功率：{}%".format(str(prtcentage)))