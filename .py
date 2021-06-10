import requests


timeout = 5

prox = input(">")

proxies = {
        "http": "http://"+prox,
        "https": "https://"+prox
}

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
headers = {'User-Agent': ua}

res = requests.get("https://twitter.com", proxies=proxies, headers=headers, timeout=timeout)

print("connected successfully:", res.text)
