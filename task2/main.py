import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

base_url = 'https://quotes.toscrape.com/page/{}/'

client = MongoClient(
    "mongodb+srv://oleksiilozovyi:Pa5swordOl)@cluster0.jy8nj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)
db = client.book

quotes_data = []

page = 1
while True:
    url = base_url.format(page)

    response = requests.get(url)

    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.select('div[class=quote]')

    if not content:
        break

    for link in content:
        text = (link.find('span', attrs={'class': 'text'})).text.strip()
        author = (link.find('small', attrs={'class': 'author'})).text.strip()
        tags = (link.find('meta', attrs={'class': 'keywords'}).get('content', '').strip())
        quotes_data.append({"tags": tags, "author": author, "quote": text})

    page += 1

with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

result_many = db.quotes.insert_many(quotes_data)
print(f"Inserted {len(result_many.inserted_ids)} quotes into MongoDB")