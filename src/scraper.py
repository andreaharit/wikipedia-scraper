import requests
import json
from bs4 import BeautifulSoup


def write_json(dictionary, out_filename):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
 
    # Writing to sample.json
    with open(out_filename, "w") as outfile:
        outfile.write(json_object)

class WikipediaScraper:    
    base_url = "https://country-leaders.onrender.com"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.cookie = self.refresh_cookie()
        self.countries = self.get_countries()
    

    def refresh_cookie(self, base_url = base_url):
        cookies_endpoint = "/cookie"
        cookie = self.session.get(f"{base_url}{cookies_endpoint}")
        return cookie

    def get_countries (self, base_url = base_url):  
        country_endpoint = "/countries"  
        countries = self.session.get(f"{base_url}{country_endpoint}")
        return countries.json()    
      
    def get_leaders (self, base_url = base_url, country = None):    
        leaders_endpoint = "/leaders"    
        leaders = self.session.get(f"{base_url}{leaders_endpoint}", params = {'country': country}) 
        return leaders.json()  

    
    def get_link (self, leader):
        if leader["last_name"] != None:
            name = f"{leader['first_name']} {leader['last_name']}"
        else:
            name = f"{leader['first_name']}"
        return name, leader['wikipedia_url']
        
    
    def get_first_paragraph(self, wikipedia_url: str):
        r = requests.get(wikipedia_url)
        soup = BeautifulSoup(r.content.decode('utf-8'), "html.parser")

        for p in soup.find_all('p'):
            paragraph = str(p)
            if '<p><b>' in paragraph:
                return (p.text)


    
 




s = WikipediaScraper()

links = {}

for country in s.countries:
    leaders = s.get_leaders(country=country)
    for leader in leaders:          
        name, link = s.get_link(leader=leader) 
        links[name]= link



# Serializing json
#json_link = json.dumps(links, indent=4)
 
    # Writing to sample.json
#with open("names_links.json", "w") as outfile:
 #   outfile.write(json_link)
summaries = {}              
for key, value in links.items():
    summary = s.get_first_paragraph(value)
    summaries[key] = summary


with open("summaries.json", "w", encoding= 'utf-8') as outfile:
    json_summaries = json.dumps(summaries, ensure_ascii=False, indent=4)

    outfile.write(json_summaries)



        
    


