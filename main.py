from src.scraper import WikipediaScraper

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

    # Loops each link in list with all wiki pages         
    for link in links:
        # Extracts raw title and paragraph
        dirty_paragraph, dirty_name = WikipediaScraper.get_first_paragraph(link)
        # Cleans both
        clean_paragraph = WikipediaScraper.clean_paragraph (dirty_paragraph)
        clean_name = WikipediaScraper.clean_name(dirty_name)
        # Builds dictionary
        paragraphs[clean_name] = clean_paragraph
    
    # Exporting dictionary into json
    print ("Exporting to json file.")
    out_filepath = "first_paragraphs.json"   
    WikipediaScraper.to_json_file(filepath= out_filepath, paragraphs = paragraphs)
    print ("Finished exporting.")

if __name__ == "__main__":
    main()


    


