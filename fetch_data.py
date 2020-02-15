import requests
from bs4 import BeautifulSoup as bs
import re
from pathlib import Path
import csv
from textblob import TextBlob
import time

def get_year(string, last_year='2025'):
    """Extract the year of an event"""
    
    year = re.compile(r"(\([c\.\s+]*(\d{2,4})[\–\-](\d{2,4})\)|(born\s(\d{2,4})))")
    result = [a for a in re.findall(year, string)[0] if a != '' and a.isalnum()]
    if len(result) == 1:
        result.append(last_year)
    if result:
        return sorted(result,key=len)

def fetch_all_links(url):
    """Get all the people links for a given URL"""
    
    place_holder = ['1900','1950']
    e_count = 0
    response = requests.get(url)
    if response.status_code == 200:
        #fetch all links
        soup = bs(response.content, 'html.parser')
        body = soup.find("div",{"id":"bodyContent"})
        list_items = body.find_all("li")
        links = []
        for i in list_items:
            try:
                link = i.find("a")
                text = i.text
                if '/wiki/' in link['href']:
                    try:
                        years = get_year(text)
                        links.append({'text':link['title'].split("(")[0].strip(), 'link':link['href'], 'year':get_year(text)})
                    except Exception as ee:
                        links.append({'text':link['title'].split("(")[0].strip(), 'link':link['href'],'year':place_holder})
            except Exception as ee:
                e_count += 1
        print(f"Errors:{e_count}")
        return links 
    
def save_names_to_csv(url,data):
    """Given a list of names, save it to CSV"""
    
    forbid = ['list of','category:','lists of','portal:',' of ',' in ']
    name = url.split("/")[-1]
    blob  = TextBlob(name.split("_")[-1])
    forbid.append(blob.words[0].singularize().lower())
    path = Path("countries","lists_of_people",name+".csv")
    with open(path,'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['text','link','year'],delimiter='\t')
        writer.writeheader()
        for line in data:
            if not any(i for i in forbid if i in line['text'].lower()):
                writer.writerow(line)
    print(f"done writing {path}")
    
            
def fetch_lists(save_file="countries_lists", url='https://en.wikipedia.org/wiki/Lists_of_people_by_nationality'):
    """Fetch a list of lists"""
    
    path = Path("countries",f"{save_file}"+".txt")
    with open(path,'w') as outfile:
        lists = set()
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs(response.content, 'html.parser')
            target_divs = [13,14]
            for div in target_divs:
                div = soup.find_all("div")[div]
                list_items = div.find_all("li")
                links = []
                for i in list_items:
                    try:
                        link = i.find("a")
                        if '/wiki/' in link['href']:
                            lists.add(link['href'])
                    except Exception as ee:
                        print(ee)
        for line in lists:
            outfile.write(f"{line}\n")
        return lists
            
            
def fetch_all_people(file='countries/countries_to_fetch.txt'):
    """Visit each URL in file and collect all people links"""
    
    links = [a.strip() for a in open(file).readlines()]
    base = "https://en.wikipedia.org"
    with open("countries/failures.txt","w") as errorfile:
        errorfile.write("These countries failed -- review these urls")
        for link in links:
            time.sleep(0.1)
            url = f"{base}{link}"
            assert url.startswith("https://en.wikipedia.org/")
            people = fetch_all_links(url)
            print(f"Collecting...{url}")
            if len(people) < 25:
                errorfile.write(f"{url}\n")
            else:
                print("People found:",len(people))
                save_names_to_csv(url, people)