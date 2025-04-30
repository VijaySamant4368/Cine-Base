import sqlite3
import requests
from bs4 import BeautifulSoup
import json

DB_PATH = "movies.db"
DB_PATH = "../" +DB_PATH

BASE_URL = "https://www.imdb.com/"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

JSON_FILE = "movieLinks.json"

try:
    with open(JSON_FILE, "r") as file:
        title_links = json.load(file)
except:
    title_links = []

cursor.execute('''
    SELECT title_id, title_name, year FROM titles WHERE title_id > ?;
''', (len(title_links), ))

title_data = cursor.fetchall()
for title_row in title_data:
    title_id = title_row[0]
    title_name = title_row[1]
    year = title_row[2]
    search_name = title_name.replace("&", "and") + " " + str(year)
    url = "https://www.imdb.com/find/?q=" + search_name
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')

    img_elem = soup.find_all("img", class_="ipc-image")[0]
    img_src = img_elem["src"]

    href = BASE_URL + img_elem.parent.parent.next_sibling.findChild().findChild()["href"]
    if not img_src or not href:
        break
    title_link = {
        "title_id": title_id,
        "href": href,
        "img_src": img_src
    }
    title_links.append(title_link)
    print(str(title_id)+ "/1000 completed")

    with open(JSON_FILE, "w") as file:
        json.dump(title_links, file, indent=4)

def getHighQualityImage(url:str):
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)
    src = BASE_URL + soup.find("a", class_ = "ipc-lockup-overlay ipc-focusable")["href"]
    
    res = requests.get(src, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup.find("img", class_ = "sc-7c0a9e7c-0 ekJWmC")["src"]
    
DONE = 0
DONE = 340

errors = [341]

for i in [341, 402, 473, 631, 683, 975]:
    try:
        href = title_links[i]["href"]
        title_links[i]["img_src_high"] = getHighQualityImage(href)
        with open(JSON_FILE, "w") as file:
            json.dump(title_links, file, indent=4)
    except TypeError:
        errors.append(title_links[i]["title_id"])
        print("ERROR IN " + str(title_links[i]["title_id"]))
    print(f"{i+1}/1000 done")

print(errors)