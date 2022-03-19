from concurrent.futures import process
import sqlite3
from bs4 import BeautifulSoup as bs
import re
from collections import Counter
from multiprocessing import Pool

PATH_TO_WIKIPEDIA_DUMP = "D:\WikipediaDUMP\enwiki-20210801-pages-articles-multistream.xml"
PATH_TO_DATABASE = "D:\WikipediaDUMP\database.db"

WORDS_TO_PROCESS = 100
MAX_LEN_OF_WORD = 25
MIN_LEN_OF_WORD = 2

conn = sqlite3.connect(PATH_TO_DATABASE)
c = conn.cursor()

c.execute("Drop table if exists word_frequency")

#create table with columns word, frequency
c.execute("CREATE TABLE IF NOT EXISTS word_frequency (word TEXT NOT NULL, frequency INTEGER DEFAULT 0)")

#print total unique keys in db
def record_count():
    total = c.execute("SELECT COUNT(DISTINCT word) FROM word_frequency")
    print("Total unique keys in db:", total.fetchone()[0])

def search_for_word(word):
    match = c.execute("SELECT * FROM word_frequency WHERE word = ?", (word,))
    return match

def add_word_to_database(word):
    c.execute("INSERT INTO word_frequency (word) VALUES (?)", (word,))
    conn.commit()

def update_word_frequency_by_increment_for_many_words(words):
    frequencies = Counter(words).items()
    for word, freq in frequencies:
        c.execute("UPDATE word_frequency SET frequency = ? WHERE word = ?", (freq, word))
    conn.commit()

def reset_all_frequencies_to_zero():
    c.execute("UPDATE word_frequency SET frequency = 0")
    conn.commit()

def get_next_word():
    processed = 0
    with open(PATH_TO_WIKIPEDIA_DUMP, 'r', encoding='utf-8') as f:
        while True:
            xml = f.read(50000)
            pages = xml.split('<page>')
            for page in pages:
                #parse page using bs4
                soup = bs(page, 'lxml')
                #get words from page
                text_blob = soup.get_text()
                single_words = [a.lower() for a in re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+").findall(text_blob)]
                for word in single_words:
                    if len(word) > MAX_LEN_OF_WORD or len(word) < MIN_LEN_OF_WORD:
                        continue
                    processed += 1
                    yield word, processed


def print_first_500_words_in_database():
    c.execute("SELECT * FROM word_frequency LIMIT 500")
    print(c.fetchall())

k = get_next_word()
max_size = 1000
common_len = 2500
unique_words_to_get = 500000

words_already_added = set()

with open('wikipedia_300k_top_words.txt', 'r',encoding='utf-8') as f:
    unique_words = [words_already_added.add(a.strip()) for a in f.readlines()]
    
#using multiprocessing
with Pool(processes=4) as pool:
    while len(words_already_added) < unique_words_to_get:
        frequencies = Counter([next(k)[0] for i in range(max_size)]).most_common(common_len)
        for word, count in frequencies:
            if count > 1:
                words_already_added.add(word)
        print(len(words_already_added))

with open('wikipedia_300k_top_words.txt','w',encoding='utf-8') as f:
    print(len(words_already_added))
    for word in words_already_added:
        f.write(word+'\n')
