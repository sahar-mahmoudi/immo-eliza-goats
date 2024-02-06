import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json

class ImmoCrawler():
    def __init__(self) -> None:
        self.base_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&orderBy=postal_code&page="
        self.links = []
        self.property_data = {}
        self.property_key = 0

    def crawl_page(self, page):
        try:
            response = requests.get(f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&orderBy=postal_code&page={page}")
            response.raise_for_status()
            r = BeautifulSoup(response.content, "html.parser")
            properties = r.find_all("a", attrs={"class": "card__title-link"})

            for property in properties:
                    print(property.get("href"))
                    self.links.append(property.get("href"))
        except Exception as error:
            print(f"Error in thread for page {page}: {error}")

    def get_properties(self):
        num_pages = 333
        with ThreadPoolExecutor(max_workers=5) as executor: 
            executor.map(self.crawl_page, range(1, num_pages + 1))

        print(self.links)
        
        for url in self.links:
             self.property_key += 1
             self.get_data(url)

    def get_data(self, url):

        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        scripts = soup.find_all("script", attrs={"type": "text/javascript"})
        #print(script)

        for script in scripts:
            if "window.classified" in script.get_text():
                classified_script = script
                break
        
        
        # Extract the text content of the script tag
        script_content = classified_script.get_text()

        # Use string manipulation to extract the window.classified object
        json_str = script_content[script_content.find('{'):script_content.rfind('}') + 1]

        # Load the JSON data
        data = json.loads(json_str)
        
        #Make the empty list 

       

        
        self.property_data[self.property_key] = {
            "id": data['id'],
            "locality": data['property']['location']['district'],
            "zip_code": data['property']['location']['postalCode'],
            "price": data['transaction']['sale']['price'],
            "property_type": data['property']['type'],
            "subproperty_type": data['property']['subtype'],
            "bedroom_count": data['property']['bedroomCount'],
            "total_area_m2": data['property']['netHabitableSurface'],
            "equipped_kitchen": 1 if data['property']['type'] else 0,
            "furnished": 1 if data['transaction']['sale']['isFurnished'] else 0,
            "open_fire": 1 if data['property']['fireplaceExists'] else 0,
            "terrace": data['property']['terraceSurface'] if data['property']['hasTerrace'] else 0,
            "garden" : data['property']['gardenSurface'] if data['property']['hasGarden']else 0,
            "surface_land": data['property']['land']['surface'] if data['property']['land']else 0,
            "facades":  data['property']['building']['facadeCount'],
            "swimming_pool": 1 if data['property']['hasSwimmingPool'] else 0,
            "state_building":  data['property']['building']['condition'],
        # "type_sale1": "public_sales" if data['flag']['isPublicSale'] else 0,
            #"type_sale2": "notary_sale" if data['flag']['isNotarySale'] else 0
        }
                

            
        return self.property_data

# Example usage
crawler = ImmoCrawler()
crawler.get_properties()
