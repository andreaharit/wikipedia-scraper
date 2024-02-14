import requests
import json

root_url = "https://country-leaders.onrender.com"

def write_json(dictionary, out_filename):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
 
    # Writing to sample.json
    with open(out_filename, "w") as outfile:
        outfile.write(json_object)

class Get_names:

    global root_url

    def __init__(self) -> None:
        self.session = requests.Session()
        self.status, self.message = self.check_api()        

    def get_request(self, endpoint, param = None):     
        response = self.session.get(f"{root_url}/{endpoint}", params = param)
        return response.json()
    
    def check_api(self):
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
        
    def get_countries (self):
        endpoint_countries = 'countries'
        countries = self.get_request(endpoint= endpoint_countries)
        return countries
    
    def get_leaders (self, country):
        xx= {'country': country}
        endpoint_leaders = 'leaders'
        leaders = self.get_request(endpoint= endpoint_leaders, param = xx)
        return leaders
    
    def get_name (self, leader):        
        return leader['first_name'] + " " + leader['last_name']
    def get_wiki (self, leader):
        return leader['wikipedia_url']
        
class extract_wiki:
    


s = Get_names()
b, message = s.check_api()
if b == 1:
    print (message)
leaders = s.get_countries()
ugly_json = s.get_leaders(leaders[0])
write_json(ugly_json,"first_test.json")
for i in ugly_json:
    print(s.get_name(i))
    print(s.get_wiki(i))


