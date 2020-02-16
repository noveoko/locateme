import sqlite3
import glob
import csv



def dir_to_datbase(path_to_dir='lists_of_people'):
    conn = sqlite3.connect('locateme.db')
    c = conn.cursor()
    countries = glob.glob(path_to_dir+"/*.csv")
    errors = 0
    for country in countries:
        just_country = country.split("/")[-1].replace(".csv","")
        with open(country,'r',encoding='utf-8') as infile:
            reader = csv.DictReader(infile, fieldnames=['text','link','year'], delimiter='\t')
            for line in reader:
                clean_text = line['text'].replace('"',"").replace("'","")
                clean_link = line['link'].replace('"',"").replace("'","")
                name = f"'{clean_text}'"
                link = f"'{clean_link}'"
                start = line['year'].split(",")[0].replace("[","").replace("]","")
                end = line['year'].split(",")[-1].replace("[","").replace("]","")
                query = ("INSERT INTO people VALUES ({0},{1},{2},{3},'{4}')").format(name, link, start, end, just_country)
                try:
                    c.execute(query)
                except Exception as e:
                    errors +=1
                    print(e, query)
    conn.commit()
    conn.close()
    print("Total Error:",errors)
    
if __name__ == "__main__":
    dir_to_datbase()