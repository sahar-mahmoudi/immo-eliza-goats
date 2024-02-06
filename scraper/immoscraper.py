import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
import csv

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
             print(f"Progress: {self.property_key}/10000")
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

       
        if data is not None:
        
             self.property_data[self.property_key] = {
        "id": data.get('id'),
        "locality": data['property']['location']['district'] if data.get('property') and data['property'].get('location') else None,
        "zip_code": data['property']['location']['postalCode'] if data.get('property') and data['property'].get('location') else None,
        "price": data['transaction']['sale']['price'] if data.get('transaction') and data['transaction'].get('sale') else None,
        "property_type": data['property']['type'] if data.get('property') else None,
        "subproperty_type": data['property']['subtype'] if data.get('property') else None,
        "bedroom_count": data['property']['bedroomCount'] if data.get('property') else None,
        "total_area_m2": data['property']['netHabitableSurface'] if data.get('property') else None,
        "equipped_kitchen": 1 if data['property']['type'] else 0 if data.get('property') else None,
        "furnished": 1 if data['transaction']['sale']['isFurnished'] else 0 if data.get('transaction') and data['transaction'].get('sale') else None,
        "open_fire": 1 if data['property']['fireplaceExists'] else 0 if data.get('property') else None,
        "terrace": data['property']['terraceSurface'] if data['property']['hasTerrace'] else 0 if data.get('property') else None,
        "garden": data['property']['gardenSurface'] if data['property']['hasGarden'] else 0 if data.get('property') else None,
        "surface_land": data['property']['land']['surface'] if data['property']['land'] else 0 if data.get('property') and data['property'].get('land') else None,
        "facades": data['property']['building']['facadeCount'] if data.get('property') and data['property'].get('building') else None,
        "swimming_pool": 1 if data['property']['hasSwimmingPool'] else 0 if data.get('property') else None,
        "state_building": data['property']['building']['condition'] if data.get('property') and data['property'].get('building') else None,
    }
            # "type_sale1": "public_sales" if data['flag']['isPublicSale'] else 0,
                #"type_sale2": "notary_sale" if data['flag']['isNotarySale'] else 0
            
                

        final_properties.append(self.property_data[self.property_key])  
        return self.property_data[self.property_key]
    def export_to_csv(data_list, csv_filename):
        """
        Export a list of dictionaries to a CSV file.

        Parameters
        ----------
        data_list : list
            List containing dictionaries.

        csv_filename : str
            File path and name for the CSV file.

        Returns
        -------
        None
        """
        if not isinstance(data_list, list) or not all(isinstance(d, dict) for d in data_list):
            print("Error: Input should be a list of dictionaries.")
            return

        if not data_list:
            print("Error: Input list is empty.")
            return

        with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
            # Get the field names from the first dictionary in the list
            fieldnames = data_list[0].keys()
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header
            csv_writer.writeheader()

            # Write the data rows
            csv_writer.writerows(data_list)

# main.py
final_properties = []
crawler = ImmoCrawler()
crawler.get_properties()
crawler.export_to_csv(final_properties, "data.csv")