from bs4 import BeautifulSoup as bs
import requests
from time import perf_counter

class crawlerV2 ():
    def __init__(self) -> None:
        self.base_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&isALifeAnnuitySale=false&orderBy=postal_code&page="
        self.links = []

    def get_links(self, page:int):
        start = perf_counter()

        link = f"{self.base_url}{page}"
        response = requests.get(link)
        soup = bs(response.text, "html.parser")
        links_loc = soup.find_all("a", attrs={"class": "card__title-link"})
        for href in links_loc:
            self.links.append(href.get("href"))
        print(f"It took {perf_counter() - start} to gather the links")

    def get_all_properties(self):
        page = 333
        
