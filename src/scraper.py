import requests
import json
from bs4 import BeautifulSoup
import csv
import sys
import re

class CookieError(Exception): 
    def __init__(self): 
        super().__init__("Error in creating a cookie!")


class WikipediaScraper:    
    base_url = "https://country-leaders.onrender.com"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.cookie = self.refresh_cookie()        
        self.countries = self.get_countries()    


    def refresh_cookie(self, base_url = base_url):

        cookies_endpoint = "/cookie"
        check_cookie_endpoint = "/check"        
               
        cookie_ok_status = 200

        while True:
            try:   
                cookie = self.session.get(f"{base_url}{cookies_endpoint}")
                check_cookie = self.session.get(f"{base_url}{check_cookie_endpoint}")
                if check_cookie.status_code != cookie_ok_status:
                    raise CookieError()
                else:
                    return cookie
            except CookieError as error:
                    print (error)
                    sys.exit()


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
        
    @staticmethod
    def get_first_paragraph(wikipedia_url: str):
        r = requests.get(wikipedia_url)
        soup = BeautifulSoup(r.content.decode('utf-8'), "html.parser")

        for p in soup.find_all('p'):
            paragraph = str(p)
            # First paragraphs contain a name in bold and a year (four numbers) for the birthdate
            if '<p>' in paragraph and '<b>' in paragraph and bool(re.search(r'\d{4}', paragraph)):                               
                first_paragraph = p.text
                return first_paragraph
    @staticmethod       
    def clean_paragraph(paragraph):
        # supress \n at the end
        paragraph = paragraph.rstrip("\n").strip()
        # supress lost \
        paragraph = paragraph.replace('\\', "")
        # corrects quotes
        paragraph = paragraph.replace('\"', "'")
        # supress [something]:
        correct_1 = re.sub(r"\[.*\]","", paragraph) 
        # suppress Écouters in french paragraphs
        correct_2 = re.sub(r"\s\(.*Écouter\)","", correct_1)
        correct_3 = re.sub(r"\sÉcouter?\)",'', correct_2).replace("Écouter", "")
        # correct pronounciation strings from american leaders
        correct_4 = re.sub(r"\(\/.*ˈ.*\;", '', correct_3)  
        # correct pronouciation strings from dutch
        correct_5 = re.sub(r"uitspraakⓘ", "", correct_4 )
        # correct excess of spaces:
        correct_6 = correct_5.replace("  "," ").replace (' ,', ",")
        
        

        return correct_6
        

            
    
    @staticmethod
    def to_json_file(filepath: str, summaries: dict):
        with open(filepath, "w", encoding= 'utf-8') as outfile:
            json_summaries = json.dumps(summaries, ensure_ascii=False, indent=4)
            outfile.write(json_summaries)
        outfile.close()

    @staticmethod
    def to_csv_file(filepath: str, summaries: dict):
        header = ["Name", "Summary"]
        with open(filepath, "w", encoding= 'utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames = header)
            writer.writeheader()
            writer.writerows(summaries)
        outfile.close()

def main():
    s = WikipediaScraper()

    links = {}

    for country in s.countries:
        leaders = s.get_leaders(country=country)
        for leader in leaders:          
            name, link = s.get_link(leader=leader) 
            links[name]= link

    summaries = {}              
    for key, value in links.items():
        summary = WikipediaScraper.get_first_paragraph(value)
        summary = WikipediaScraper.clean_paragraph (summary)
        summaries[key] = summary

    out_filepath = "summaries_v3.json"   
    WikipediaScraper.to_json_file(filepath= out_filepath, summaries = summaries)


if __name__ == "__main__":
    main()

# TO DO: CLEAN PARAGRAPHS FROM WEIRD THINGS, CHECK IF THEY ARE RIGHT.
# FIX RUSSIAN GUY WITH QUOTES    
    


