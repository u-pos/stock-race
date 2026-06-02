import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://www.sbisec.co.jp/ETGate/?_ControlID=WPLETmgR001Control&_DataStoreID=DSWPLETmgR001Control&_PageID=WPLETmgR001Mdtl20&_ActionID=DefaultAID&getFlg=on&OutSide=on&burl=iris_ranking&cat1=market&cat2=ranking&file=index.html&dir=tl1-rnk%7Ctl2-stock%7Ctl3-salesval%7Ctl4-high%7Ctl5-priceview%7Ctl7-T1"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("SBI取得中...")

r = requests.get(URL, headers=headers, timeout=30)

r.encoding = "cp932"

html = r.text

with open("debug_sbi.html", "w", encoding="utf-8") as f:
    f.write(html)

print("debug_sbi.html 保存完了")

soup = BeautifulSoup(html, "html.parser")

table = soup.find("table", class_="md-table06")

if not table:
    print("ランキングテーブルが見つかりません")
    exit()

stocks = []

rows = table.find("tbody").find_all("tr")

for row in rows:

    tds = row.find_all("td")

    if len(tds) < 4:
        continue

    try:

        rank = int(tds[0].get_text(strip=True))

        stock_td = tds[1]

        text = stock_td.get_text("\n", strip=True)

        parts = text.split("\n")

        if len(parts) < 2:
            continue

        name = parts[0].strip()
        code = parts[1].strip()

        change_td = tds[3]

        change_text = change_td.get_text(" ", strip=True)

        m = re.search(r'([+-]\d+\.\d+)％', change_text)

        if not m:
            continue

        change = float(m.group(1))

        stocks.append({
            "rank": rank,
            "code": code,
            "name": name,
            "change": change
        })

    except Exception as e:
        print("スキップ:", e)

stocks.sort(key=lambda x: x["change"], reverse=True)

with open("stocks.json", "w", encoding="utf-8") as f:
    json.dump(
        stocks,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"stocks.json 作成完了 ({len(stocks)}件)")
