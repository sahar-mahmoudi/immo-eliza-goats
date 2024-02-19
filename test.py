import requests
from bs4 import BeautifulSoup as bs 
import json


def data_gathering(url:str):
    req = requests.get(url)
    soup = bs(req.content, "html.parser")
    script_2 = soup.find("script", {"type": "text/javascript"}).string

    start_2 = script_2.find("window.classified = ") + len("window.classified = ")
    end_2 = script_2.find("};", start_2)

    json_str_2 = script_2[start_2:end_2]
    print(json_str_2)
    #data_2 = json.loads(json_str_2)

data_gathering("https://www.immoweb.be/en/classified/villa/for-sale/pelt/3910/10773702")