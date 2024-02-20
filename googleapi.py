from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests
import csv
import os

def search_google(query, site = None):
    api_key = os.getenv("API_KEY")
    cx = os.getenv("cx")

    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cx, num = 3, siteSearch = site if site else None).execute()
    return res["items"] if "items" in res else []

records = [
    {'name': 'What is Canoo'},
    {'name': 'Canoo introduction size growth trends'},
    {'name': 'Canoo competitors market share products'},
    {'name': 'Canoo market trends'},
    {'name': 'Canoo financial performance revenue profit margins'}
]

with open('output.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Link', 'Content'])
    for record in records:
        site = "https://canoo.com"
        results = search_google(record['name'], site)

        print(f"Results for: {record['name']}")
        for result in results:
            print(result['link'])
            response = requests.get(result["link"])
            soup = BeautifulSoup(response.text, "html.parser")
            p_tags = soup.find_all("p")
            for para in p_tags:
                content = para.get_text()
                writer.writerow([result['link'], content])
                print(content)
        print()
