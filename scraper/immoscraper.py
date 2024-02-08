import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
import asyncio
import aiohttp
from time import perf_counter
import pandas as pd



class ImmoCrawler():
    """
    A web scraper class for collecting real estate data from Immoweb.
    """
    def __init__(self) -> None:
        """
        Initializes the ImmoCrawler class.
        """
        self.base_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale/"
        self.links = []
        self.property_data = {}
        self.property_key = 0
        self.links_counter = 0
        self.regions = ["west-flanders", "east-flanders", "antwerp", "brussels", "walloon-brabant", "limburg", "liege", "luxembourg", "namur", "hainaut"]
        self.provinces = ["West Flanders", "East Flanders", "Antwerp", "Brussels", "Walloon Brabant", "Limburg", "Liege", "Luxembourg", "Namur", "Hainaut"]
        self.filters_url = "/province?countries=BE&isALifeAnnuitySale=false&orderBy=postal_code&page="

    async def crawl_page(self, session, region, page, semaphore):
        """
        Asynchronously crawls a page to extract property links and data.

        Parameters
        ----------
        session : aiohttp.ClientSession
            The aiohttp session for making asynchronous requests.
        page : int
            The page number to crawl.
        semaphore : asyncio.Semaphore
            Semaphore for controlling the number of concurrent requests.

        Returns
        -------
        None
        """
        async with semaphore:
        

                try:
                    # Asynchronously fetch the HTML content of the page
                    async with session.get(f"{self.base_url}{region}{self.filters_url}{page}") as response:
                        response.raise_for_status()
                        html = await response.text()
                        r = BeautifulSoup(html, "html.parser")
                        properties = r.find_all("a", attrs={"class": "card__title-link"})
                        self.page_counter = len(properties) * page
                        print(f"{self.base_url}{region}{self.filters_url}{page}")
                        # Iterate over each property link on the page
                        for property in properties: 
                                href = property.get("href")
                                
                                # Check if it is the new project of real estate 
                                if "new-real-estate-project-apartments" in href or "new-real-estate-project-houses" in href:
                                    # Extract links from sub-properties 
                                    async with session.get(f"{href}") as response:
                                        html = await response.text()
                                        r = BeautifulSoup(html, "html.parser")
                                        sub_properties = r.find_all("a", attrs={"class":"classified__list-item-link"})

                                        for sub_property in sub_properties:
                                            self.links_counter += 1
                                            self.links.append(sub_property.get("href"))
                                            
                                            self.property_key += 1
                                            print(f"Grabbing Links & Extracting Data: {self.property_key}")
                                            await self.get_data(session, sub_property.get("href"), region)

                                else:
                                    self.links_counter += 1
                                    
                                    self.links.append(property.get("href"))
                                    self.property_key += 1
                                    print(f"Grabbing Links & Extracting Data: {self.property_key}")
                                    await self.get_data(session, property.get("href"), region)
                        
                except Exception as error:
                    print(f"Error in thread for page {page}: {error}")


    async def get_data(self, session, url, region):
        """
        Asynchronously fetches and extracts property data from a given URL.

        Parameters
        ----------
        session : aiohttp.ClientSession
            The aiohttp session for making asynchronous requests.
        url : str
            The URL of the property.

        Returns
        -------
        dict or None
            Extracted property data if the property is in Belgium; otherwise, None.
        """
        try:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                scripts = soup.find_all("script", attrs={"type": "text/javascript"})
                
                # Find the script containing window.classified
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
                
                def multi_get(dict_obj, *attrs, default=None):
                    result = dict_obj
                    for attr in attrs:
                        if not result or attr not in result:
                            return default
                        result = result[attr]
                    return result
                
                if data is not None:


                    if multi_get(data,'property','location', 'country') == "Belgium" and multi_get(data,'property','location', 'province') == self.provinces[self.regions.index(region)]:
                        # Extract relevant property data
                        self.property_data[self.property_key] = {
                            "link": url,
                            "id": data.get('id',None),
                            "locality": multi_get(data,'property','location','district'),
                            "country": multi_get(data,'property','location', 'country'),
                            "province": multi_get(data,'property','location', 'province'),
                            "zip_code":multi_get(data,'property','location','postalCode'),
                            "price": multi_get(data,'transaction','sale','price'),
                            "property_type": multi_get(data,'property','type'),
                            "subproperty_type": multi_get(data,'property','subtype'),
                            "bedroom_count": multi_get(data,'property','bedroomCount'),
                            "total_area_m2": multi_get(data,'property','netHabitableSurface'),
                            "equipped_kitchen": 1 if multi_get(data,'property','kitchen','type') else 0,
                            "furnished": 1 if multi_get(data,'transaction','sale','isFurnished') else 0,
                            "open_fire": 1 if multi_get(data, 'property', 'fireplaceExists') else 0,
                            "terrace": multi_get(data,'property','terraceSurface') if data['property']['hasTerrace'] else 0,
                            "garden": multi_get(data,'property','gardenSurface') if data['property']['hasGarden'] else 0,
                            "surface_land": multi_get(data,'property','land','surface'),
                            "swimming_pool": 1 if multi_get(data,'property','hasSwimmingPool') else 0,
                            "state_building": multi_get(data,'property','building','condition'),
                            "epc": multi_get(data,'transaction','certificates','epcScore'),
                            "public_sales":  multi_get(data,'flag','isPublicSale'), 
                            "notary_sales":  multi_get(data,'flag','isNotarySale'),
                            }
                
                
                        return self.property_data[self.property_key]
                    else:
                        pass
        except Exception as error:
            print(f"Error in gathering data from {url}: {error}") 

    async def get_properties(self, num_pages=333):
        """
        Asynchronously fetches and extracts property data from multiple pages.

        Parameters
        ----------
        num_pages : int, optional
            The number of pages to crawl, by default 333.

        Returns
        -------
        None
        """
        start_time = perf_counter()
        
        # Adjust the semaphore count based on server limits
        semaphore = asyncio.Semaphore(20)
        for region in self.regions[0:2]:
            async with aiohttp.ClientSession() as session:
                
                    tasks = [self.crawl_page(session, region, page, semaphore) for page in range(1, num_pages + 1)]
                    await asyncio.gather(*tasks)
                    print(f"finished with {region}")

        print(f"Took {perf_counter() - start_time}")
        
        

    
    def to_csv(self, name):
        """
        Convert the collected property data to a CSV file.

        Parameters
        ----------
        name : str
            The name of the CSV file (without extension).

        Returns
        -------
        None
        """

        df = pd.DataFrame.from_dict(self.property_data, orient="index")
        df.to_csv(name + '.csv')