import re
from pathlib import Path

person_date = re.compile(r"(?P<link>(\[\[|\()[\w\s\-\(\)\|\,XVI]+(\]\]|\)))\s*(?P<date>\((born\s[\w+\s\;\,]+|born \d+|\d+|\d+â€“\d+|\d+\-\d+|\d+–\d+|\d+–\d+\?)\))")

links = set()


with open('wikipedia_names.txt','w', encoding='utf-8') as outfile:
    with open(Path(r'../locations/bunch/enwiki-20210801-pages-articles-multistream.xml',encoding='utf-8'),'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(50000)
            for i in person_date.finditer(chunk):
                result = f"{i['link']};{i['date']}\n"
                if result not in links:
                    links.add(result)
                    outfile.write(result)
                    print(len(links))

