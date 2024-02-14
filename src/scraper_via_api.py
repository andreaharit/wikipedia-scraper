import requests
import json
import sys



root_url = "https://country-leaders.onrender.com"

def write_json(dictionary, out_filename):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
 
    # Writing to sample.json
    with open(out_filename, "w") as outfile:
        outfile.write(json_object)

class Country_leaders:

    global root_url

    def __init__(self) -> None:
        self.session = requests.Session()
        self.status, self.message = self.check_api()
        self.countries = self.extract_countries()        

    def get_request(self, endpoint, param = None): 
        # Opens a request session    
        response = self.session.get(f"{root_url}/{endpoint}", params = param)
        return response.json()
    
    def check_api(self):
        # Checks if leaders API is anwering well
        endpoint_status = "status"
        status_ok = 'Alive'
        endpoit_cookie = "cookie"
        cookie_created = 'The cookie has been created'
        endpoit_check_cookie = "check"
        cookie_ok = 'The cookie is valid'
        
        if self.get_request(endpoint= endpoint_status) != status_ok:            
            return 0, "API is down"        
        if self.get_request(endpoint= endpoit_cookie)['message'] != cookie_created:
            return 0, "Problem creating cookie"        
        if self.get_request (endpoint= endpoit_check_cookie)['message'] != cookie_ok:
            return 0, "Cookie is invalid"
        else: 
            return 1, "Stablished connection with API"
        
    def extract_countries (self): 
        # extract countries from API       
        countries = self.get_request(endpoint= 'countries')
        return countries
    
    def leaders_info (self, country):
        # extracts leader info from api
        leaders = self.get_request(endpoint= 'leaders', param = {'country': country})
        return leaders
            
    def dict_leaders_wiki (self, leaders_info):
        # Builds dictionaru where key is name of the leader and value is the wikipage
        dict_leaders = {}
        for leader in leaders_info:
            dict_leaders[s.get_name(leader)] = s.get_wiki(leader)
        return dict_leaders
        
    def get_name (self, leader):        
        return leader['first_name'] + " " + leader['last_name']
    def get_wiki (self, leader):
        return leader['wikipedia_url']  

class Api_wiki:

    def __init__(self, url) -> None:
        self.original_url = url
        self.title, self.language = self.extract_title_lang()
        self.summary = self.get_summary_en()
    
    def extract_title_lang(self):
        url_parts = self.original_url.split(".wikipedia.org/wiki/")     
        title = url_parts[1]
        language_url = url_parts[0].lstrip("https://")
        return title, language_url
    
    def get_summary_en (self):
        base_url = ".wikipedia.org/api/rest_v1/page/summary/"
        full_url = "https://" + self.language + base_url + self.title
        r = requests.get(full_url)
        api_content = r.content.decode('utf-8')
        api_content_json= json.loads(api_content)
        summary = api_content_json["extract"]
        return summary




s = Country_leaders()
b, message = s.check_api()

if b == 1:
    print (message)
else:
    print (message)
    sys.exit()    


all_countries_links = {}

for country in s.countries:
    all_info_leaders = s.leaders_info(country)
    leaders_links = s.dict_leaders_wiki(all_info_leaders)
    all_countries_links.update(leaders_links)

for name, link in all_countries_links.items():
    leader_link = Api_wiki(link)  
    summary = leader_link.summary  
    print (name)
    print (summary)
    print ("=======================")

 






