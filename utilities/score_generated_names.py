from concurrent.futures import process
import sqlite3

PATH_TO_WIKIPEDIA_DUMP = "D:\WikipediaDUMP\enwiki-20210801-pages-articles-multistream.xml"
PATH_TO_DATABASE = "D:\WikipediaDUMP\database.db"

WORDS_TO_PROCESS = 100
MAX_LEN_OF_WORD = 25
MIN_LEN_OF_WORD = 2

conn = sqlite3.connect(PATH_TO_DATABASE)
c = conn.cursor()

#create table with columns word, frequency
c.execute("CREATE TABLE IF NOT EXISTS word_frequency (word TEXT NOT NULL, frequency INTEGER DEFAULT 0)")

def search_for_word(word):
    c.execute("SELECT * FROM word_frequency WHERE word = ?", (word,))
    return c.fetchone()

def update_word_frequency_by_increment_for_many_words(words):
    for word in words:
        if search_for_word(word) is None:
            c.execute("INSERT INTO word_frequency (word) VALUES (?)", (word,))
        c.execute("UPDATE word_frequency SET frequency = frequency + 1 WHERE word = ?", (word,))
    conn.commit()

def reset_all_frequencies_to_zero():
    c.execute("UPDATE word_frequency SET frequency = 0")
    conn.commit()

def get_next_word():
    processed = 0
    with open(PATH_TO_WIKIPEDIA_DUMP, 'r', encoding='utf-8') as f:
        while True:
            xml = f.read(500)
            pages = xml.split('<page>')
            for page in pages:
                words = [x.lower() for x in [a.split(" ") for a in page if len(a)]if len(x)<=MAX_LEN_OF_WORD and len(x) >= MIN_LEN_OF_WORD]
                for word in words:
                    processed+=1
                    yield word, processed

def print_first_100_words_in_database():
    c.execute("SELECT * FROM word_frequency LIMIT 100")
    print(c.fetchall())

#clean_up_previous_session()
# reset_all_frequencies_to_zero()

# every_word = get_next_word()
# last_processed = 0
# while last_processed < WORDS_TO_PROCESS:
#     words = []
#     for i in range(10000):
#         word, last_processed = next(every_word)
#         words.append(word)
#     update_word_frequency_by_increment_for_many_words(words)

# print_first_100_words_in_database()

conn.close()