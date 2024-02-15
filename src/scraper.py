import requests
import json
from bs4 import BeautifulSoup
import sys
import re

class CreateError(Exception):
    """
    Creates custom errors.
    Args:
        message (str): custom message for the error.
    """ 
    def __init__(self, message: str): 
        super().__init__(message)


class WikipediaScraper:
    """
    Extracts the first paragraph of an wikipedia article from a worldleader of a country.
    The leaders and countries are extracted from an API country-leaders.
    """ 
    # Base URL from the API   
    base_url = "https://country-leaders.onrender.com"

    def __init__(self) -> None:
        # Stablishes session request and collect cookie
        self.session = requests.Session()
        self.cookie = self.refresh_cookie()
        # Stores countries from API        
        self.countries = self.get_countries()    

    def refresh_cookie(self, base_url: str = base_url): 
        """
        Collects cookie from API and checks the connections and cookie status.
        """ 
        # Variables declaration     
        check_api_status_endpoint = "/status"  
        cookies_endpoint = "/cookie"
        check_cookie_endpoint = "/check"          
        ok_status = 200
        
        # API processing
        try: 
            # Stablishes connections to API and collect status
            api_status = self.session.get(f"{base_url}{check_api_status_endpoint}") 
            cookie = self.session.get(f"{base_url}{cookies_endpoint}")                
            check_cookie = self.session.get(f"{base_url}{check_cookie_endpoint}")
            # Checks statuses
            if api_status.status_code != ok_status: 
                raise CreateError(message = "Problem connecting to API.")
            if check_cookie.status_code != ok_status:
                raise CreateError(message = "Cookie is invalid.")
            # All good, returns cookie
            else:
                print ("Connection with API was well stablished and cookie was collected.")
                return cookie              
        except CreateError as error:
                print (error)
                sys.exit()

    def get_countries (self, base_url: str = base_url) -> list:  
        """
        Conects to the API, to get the countries and return them as a json list.
        """
        country_endpoint = "/countries"  
        countries = self.session.get(f"{base_url}{country_endpoint}")

        print ("List of countries was well collected.")
        return countries.json()    
      
    def get_leaders (self, country: str, base_url: str = base_url, ) -> list:
        """
        Connects with API to collect the detais of the country's leaders.
        Returns them as a json dict.
        """
        leaders_endpoint = "/leaders"    
        leaders = self.session.get(f"{base_url}{leaders_endpoint}", params = {'country': country})
        
        print (f"Information about leaders from {country} was well collected.")         
        return leaders.json()  
    
    def get_link (self, leader: dict) -> str:
        """Returns leader link from wikipedia"""       
        return leader['wikipedia_url']
    
    @staticmethod
    def get_first_paragraph(wikipedia_url: str):
        """
        Gets title and first paragraph of a leader's wikipedia page.
        """
        # Requests wikipedia HTML and starts parser
        r = requests.get(wikipedia_url)
        soup = BeautifulSoup(r.content.decode('utf-8'), "html.parser")
        # Gets webspage's title, where the name of the leader is
        search_name = soup.find('title').text
        # Gets webpage's first paragraph
        for p in soup.find_all('p'):
            paragraph = str(p)
            # First paragraphs contain a name in bold and a birthyear (four numbers)
            if '<p>' in paragraph and '<b>' in paragraph and bool(re.search(r'\d{4}', paragraph)):                               
                first_paragraph = p.text
                return first_paragraph, search_name
            
    @staticmethod
    def clean_name (title: str) -> str:
        """Cleans title of the wikipedia page and returns it as the name of the leader"""
        new_name = title.replace(" — Wikipédia", "").replace (" - Wikipedia", "")
        new_name = new_name.replace (" — Википедия", "").replace (" - ويكيبيديا", "")        
        return new_name        

    @staticmethod       
    def clean_paragraph(paragraph: str) -> str:
        """
        Takes a paragraph and cleans it from unwanted characteres, citation indexes, pronounciation blobs.
        Returns a clean first paragraph
        """
        # Deletes \n at the end
        paragraph = paragraph.rstrip("\n").strip()       
        # Corrects quotes
        paragraph = paragraph.replace('\"', "'")
        # Deletes quotation indexes [something]:
        correct_1 = re.sub(r"\[.*\]","", paragraph) 
        # Deletes pronounciation blobs from french leaders
        correct_2 = re.sub(r"\s\(.*Écouter\)","", correct_1)
        correct_3 = re.sub(r"\sÉcouter?\)",'', correct_2).replace("Écouter", "")
        # Deletes pronounciation blobs from american leaders
        correct_4 = re.sub(r"\(\/.*ˈ.*\;", '', correct_3)  
        # Deletes pronouciation sblobs from dutch leaders
        correct_5 = re.sub(r"uitspraakⓘ", "", correct_4 )
        # Correct excess of spaces:
        correct_6 = correct_5.replace("  "," ").replace (' ,', ",")       
        return correct_6           
    
    @staticmethod
    def to_json_file(filepath: str, paragraphs: dict) -> None:
        """Takes a filepah, a dictionary with the paragraphs and exports them into a json file"""
        with open(filepath, "w", encoding= 'utf-8') as jsonfile:
            json_summaries = json.dumps(paragraphs, ensure_ascii=False, indent=4)
            jsonfile.write(json_summaries)
        jsonfile.close()

