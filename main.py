from src.scraper import WikipediaScraper
from time import perf_counter
from threading import Thread


def build_dict (link: str, paragraphs: dict) -> None:
    """
    Populates paragraph dictionary with {leader name : first paragraph}
    """
    # Gets title and first paragraph from wiki
    dirty_paragraph, dirty_name = WikipediaScraper.get_first_paragraph(link)
    # Cleans paragraph
    clean_paragraph = WikipediaScraper.clean_paragraph (dirty_paragraph)
    # Gets cleans title and transforms into  name
    clean_name = WikipediaScraper.clean_name(dirty_name)
    # Populates dictionary
    paragraphs[clean_name] = clean_paragraph 


def main():

    # Starts a session to connect to the leaders API
    print("Starting a session to leaders API.")
    s = WikipediaScraper()

    print ("Collecting the links for each leader.")
    # List that will hold the links for the wikipedias
    links = []
    
    # Loop each country and appends the url to the list
    for country in s.countries:
        leaders = s.get_leaders(country=country)
        for leader in leaders:          
            link = s.get_link(leader=leader) 
            links.append(link)

    print("Collecting leader's names and paragraphs.")
    # Dictionary where key, value pair is leader name: first paragraph of his/her wiki
    paragraphs = {}  

    # List to keep threads 
    threads = list() 

    # Loops each link in list with all wiki pages 
    # Creates a threads to populate paragraphs, processing time was cut in half.   
    for link in links:
        thread = Thread(target=build_dict, args=(link, paragraphs))
        threads.append(thread)
    
    for thread in threads:
        thread.start()

    for thread in threads:  
        thread.join()
    
    # Exporting dictionary into json
    print ("Exporting to json file.")
    out_filepath = "leaders_data.json"   
    WikipediaScraper.to_json_file(filepath= out_filepath, paragraphs = paragraphs)
    print ("Finished exporting json.")

    # Exporting dictionary into csv
    print ("Exporting to csv file.")
    out_filepath = "leaders_data.csv"   
    WikipediaScraper.to_csv_file(filepath= out_filepath, paragraphs = paragraphs)
    print ("Finished exporting csv.")

if __name__ == "__main__":
    main()


    


