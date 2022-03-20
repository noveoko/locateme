from concurrent.futures import ThreadPoolExecutor
import sqlite3
from bs4 import BeautifulSoup as bs
import re
from collections import Counter


PATH_TO_WIKIPEDIA_DUMP = "D:\WikipediaDUMP\enwiki-20210801-pages-articles-multistream.xml"
PATH_TO_DATABASE = "D:\WikipediaDUMP\database.db"

MAX_LEN_OF_WORD = 20
MIN_LEN_OF_WORD = 2

def get_next_word():
    processed = 0
    with open(PATH_TO_WIKIPEDIA_DUMP, 'r', encoding='utf-8') as f:
        while True:
            xml = f.read(500000)
            # soup = bs(xml, 'lxml')
            # blob = soup.get_text()
            yield Counter(set([a.lower().strip() for a in re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+").findall(xml)]))
            


k = get_next_word()
tally = Counter(["frog"])
last_count = len(tally.keys())
processes = 4

while len(tally) < 10000000:
    with ThreadPoolExecutor(processes) as pool:
        for i in range(processes):
            pool.submit(tally.update, next(k))
            print(len(tally.keys()), end='\r')

with open('wikipedia_frequencies.txt', 'w', encoding='utf-8') as f:
    for word, freq in tally.items():
        f.write(f"{word} {freq}\n")