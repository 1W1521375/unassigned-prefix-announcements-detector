import requests
from bs4 import BeautifulSoup
from datetime import datetime
import codecs

outfile = "uploaded_log.txt"

ripe_rcc06 = "http://data.ris.ripe.net/rrc06/2019.12/"

res = requests.get(ripe_rcc06)
soup = BeautifulSoup(res.text, 'html.parser')
links = [url.get('href') for url in soup.find_all('a')]

today = datetime.now()
yyyymmdd = today.strftime('%Y%m%d')

for link in links:
    if ("bview" in link and yyyymmdd in link):
        print(f"{link}, confirmed at {yyyymmdd}-{today.strftime('%X')}", file = codecs.open(outfile, "a", "utf-8"))
