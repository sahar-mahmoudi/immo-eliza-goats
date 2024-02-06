import requests
from bs4 import BeautifulSoup as bs 
import json
import csv

url="https://www.immoweb.be/en/classified/villa/for-sale/lommel/3920/10932953"

def data_gathering(url:str):
    req = requests.get(url)
    soup = bs(req.content, "html.parser")
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
    property_information = []

    property_dict = {
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

    
    return property_dict


def export_to_csv(data_dict, csv_filename):
    """
    Export a dictionary to a CSV file.

    Parameters
    ----------
    data_dict : dict
        Dictionary containing the data.

    csv_filename : str
        File path and name for the CSV file.

    Returns
    -------
    None
    """
    if not isinstance(data_dict, dict):
        print("Error: Input should be a dictionary.")
        return

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_dict.keys())

        # Write the header
        csv_writer.writeheader()

        # Write the data row
        csv_writer.writerow(data_dict)
        
     
     
property_dict=data_gathering(url)
export_to_csv(property_dict, "file.csv")