import re
total_born =0


people_links = set()

with open('wikipedia_names.txt', 'r', encoding='utf-8') as f:
    while True:
        chunk = f.read(20000)
        if len(people_links) % 100 == 0:
            print(len(people_links))
        for line in chunk.split("\n"):
            if 'born ' in line:
                people_links.add(line)
                
with open('biographical_links.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['link','name','date','year'])
    writer.writeheader()
    for shot in people_links:
        try:
            name, date = shot.split(";")
            sub_name = name
            year = re.search('\d+', date).group(0)
            if '(' in name:
                sub_name = name.split("(")[0]
            else:
                sub_name = name
            clean_name = re.sub(r"[\[\]]","",sub_name)
            parts = clean_name.split(" ")
            d = {'link':name,'name':clean_name, 'date':date, 'year': year}
            writer.writerow(d)
        except Exception as ee:
            print(ee)
