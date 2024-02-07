import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
import csv
import asyncio
import aiohttp
from time import perf_counter
import time
import pandas as pd



class ImmoCrawler():
    def __init__(self) -> None:
        self.base_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&orderBy=postal_code&page="
        self.links = []
        self.property_data = {}
        self.property_key = 0
        self.links_counter = 0
        

    async def crawl_page(self, session, page, semaphore):
        async with semaphore:

            try:
                async with session.get(f"{self.base_url}{page}") as response:
                    response.raise_for_status()
                    html = await response.text()
                    r = BeautifulSoup(html, "html.parser")
                    properties = r.find_all("a", attrs={"class": "card__title-link"})
                    self.page_counter = len(properties) * page
                    for property in properties:
                            href = property.get("href")
                            if "new-real-estate-project-apartments" in href or "new-real-estate-project-houses" in href:
                                async with session.get(f"{href}") as response:
                                    html = await response.text()
                                    r = BeautifulSoup(html, "html.parser")
                                    sub_properties = r.find_all("a", attrs={"class":"classified__list-item-link"})
                                
                                    for sub_property in sub_properties:
                                        self.links_counter += 1
                                        self.links.append(sub_property.get("href"))
                                        
                                        self.property_key += 1
                                        print(f"Grabbing Links & Extracting Data: {self.property_key}/{len(self.links)}")
                                        await self.get_data(session, sub_property.get("href"))

                            else:
                                self.links_counter += 1
                                
                                self.links.append(property.get("href"))
                                self.property_key += 1
                                print(f"Grabbing Links & Extracting Data: {self.property_key}/{len(self.links)}")
                                await self.get_data(session, property.get("href"))
                    
            except Exception as error:
                print(f"Error in thread for page {page}: {error}")


    '''def get_properties(self , num_pages=333):
        
        with ThreadPoolExecutor() as executor: 
            executor.map(self.crawl_page, range(1, num_pages + 1))

        
        
        for url in self.links:
             self.property_key += 1
             print(f"Extracting Data: {self.property_key}/{len(self.links)}")
             self.get_data(url)
        return self.links'''
    async def get_data(self, session, url):
        try:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
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
                "link": url,
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
                "public_sales":  data['flag']['isPublicSale']  if data.get('flag') else None,
                "notary_sales":  data['flag']['isNotarySale']  if data.get('flag') else None
            }
            
                
                    

            
            
            return self.property_data[self.property_key]
        except Exception as error:
            print(f"Error in gathering data from {url}: {error}") 

    async def get_properties(self, num_pages=333):
        start_time = perf_counter()
        
        semaphore = asyncio.Semaphore(15)  # Adjust the semaphore count based on server limits

        async with aiohttp.ClientSession() as session:
            tasks = [self.crawl_page(session, page, semaphore) for page in range(1, num_pages + 1)]
            await asyncio.gather(*tasks)
            

    
    def to_csv(self, name):
        df = pd.DataFrame.from_dict(self.property_data, orient='index')
        df.to_csv(name + '.csv')

