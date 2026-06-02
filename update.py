import requests
from bs4 import BeautifulSoup
import json

URL = "https://kabutan.jp/warning/trading_value_ranking"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

html = requests.get(
    URL,
    headers=headers,
    timeout=20
).text

with open("debug.html", "w", encoding="utf-8") as f:
    f.write(html)

print("debug.html 保存完了")
