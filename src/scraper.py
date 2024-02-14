import requests
import json
import sys



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
        country_endpoint= "/countries"  
        countries = self.session.get(f"{base_url}{country_endpoint}")
        return countries.json()    
      
    def get_leaders (self, base_url = base_url, country = None):    
        leaders_endpoint = "/leaders"    
        leaders = self.session.get(f"{base_url}{leaders_endpoint}", params = {'country': country}) 
        return leaders.json()
    

    
    def get_link (self, leader):
        return leader['wikipedia_url']
        
    
    def get_first_paragraph(wikipedia_url: str):
        pass

    
 




s = WikipediaScraper()

for country in s.countries:
    leaders = s.get_leaders(country=country)
    for leader in leaders:          
        link = s.get_link(leader=leader)        
        break
    break


