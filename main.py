import requests
from bs4 import BeautifulSoup as bs 
import json


def data_gathering(url:str):
    req = requests.get(url)
    soup = bs(req.content, "html.parser")
    script = soup.find_all("script")[1].string
    print(script)

    start = script.find("window.dataLayer = [") + len("window.datalayer = [")
    end = script.find("];", start)

    start_second = script.find("av_items = ") + len("av_items = ")
    end_second = script.find("// GA4 event", start)

    property_information = []

    json_str = script[start:end]
    data = json.loads(json_str)
    # print(data)

    json_str_second = script[start_second:end_second]
    data_second = json.loads(json_str_second)
    #print(data_second)

    property_dict = {
        "id": data['classified']['id'],
        "property_type": data['classified']['type'],
        "subtype": data['classified']['subtype'],
        "price_eur": '€' + data['classified']['price'],
        "transaction_type": data['classified']['transactionType'],
        "zip_code": data['classified']['zip'],
        "bedroom_count": data['classified']['bedroom']['count'],
        "building_condition": data["classified"]["building"]["condition"],
        "total_area_m2": data["classified"]["land"]["surface"] + 'm²',
        "living_area_m2": data_second['indoor_surface'] + 'm²',
        "locality": data_second['country'] + ', ' + data_second['province'] + ', ' + data_second['city']
    }

    old_format = data["classified"]["wellnessEquipment"]["hasSwimmingPool"]    
    binary_format = 1 if old_format else 0
    property_dict["swimmingpool"] = binary_format
    
    property_information.append(property_dict)
    print(f"\n\n{property_dict}")



data_gathering("https://www.immoweb.be/en/classified/villa/for-sale/lommel/3920/10932953")

data_gathering("https://www.immoweb.be/en/classified/apartment/for-sale/brussels-city/1000/11121021")