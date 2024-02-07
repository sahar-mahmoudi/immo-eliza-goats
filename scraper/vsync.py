import asyncio
from time import perf_counter
import aiohttp
from bs4 import BeautifulSoup as bs
import json
import pandas as pd 

class ImmoCrawler:
    def __init__(self) -> None:
        self.base_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&orderBy=postal_code&page="
        self.property_data = {}

    async def crawl_page(self, session, page, semaphore):
        async with semaphore:
            try:
                async with session.get(f"{self.base_url}{page}") as response:
                    response.raise_for_status()
                    html = await response.text()
                    r = bs(html, "html.parser")
                    properties = r.find_all("a", attrs={"class": "card__title-link"})

                for property in properties:
                    url = property.get("href")
                    await self.gather_data(session, url)
            except Exception as error:
                print(f"Error in fetching page {page}: {error}")

    async def gather_data(self, session, url):
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                html = await response.text()
                soup = bs(html, "html.parser")
                scripts = soup.find_all("script", attrs={"type": "text/javascript"})
                for script in scripts:
                    if "window.classified" in script.get_text():
                        classified_script = script
                        break
                script_content = classified_script.get_text()
                json_str = script_content[script_content.find('{'):script_content.rfind('}') + 1]
                data = json.loads(json_str)
        
            if data is not None:
                property_dict = {
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
                self.property_data[url] = property_dict
        except Exception as error:
            print(f"Error in gathering data from {url}: {error}")   

    async def get_properties(self):
        start_time = perf_counter()
        num_pages = 2
        semaphore = asyncio.Semaphore(15)  # Adjust the semaphore count based on server limits

        async with aiohttp.ClientSession() as session:
            tasks = [self.crawl_page(session, page, semaphore) for page in range(1, num_pages + 1)]
            await asyncio.gather(*tasks)

        print(f"\nTime spent inside the loop: {perf_counter() - start_time} seconds.")

    def to_csv(self, name):
        df = pd.DataFrame.from_dict(self.property_data, orient='index')
        df.to_csv(name + '.csv')




