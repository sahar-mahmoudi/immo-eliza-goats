import requests
from bs4 import BeautifulSoup
import json

url = "https://www.immoweb.be/en/classified/town-house/for-sale/nazareth/9810/11119383"
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')
script_tags = soup.find_all("script", attrs={"type": "text/javascript"})

# Find the script tag containing window.classified
classified_script = None

for script in script_tags:
    if "window.classified" in script.get_text():
        classified_script = script
        #print(classified_script.text)
        break

# Check if the script tag is found
if classified_script:
    # Extract the text content of the script tag
    script_content = classified_script.get_text()

    # Use string manipulation to extract the window.classified object
    classified_data = script_content[script_content.find('{'):script_content.rfind('}') + 1]

    # Load the JSON data
    classified_dict = json.loads(classified_data)

  # Access the value 
    id=classified_dict.get("id")
    locality= classified_dict.get("property",{}).get("location",{}).get("district")
    postal_code= classified_dict.get("property",{}).get("location",{}).get("postalCode")
    price_house = classified_dict.get('transaction', {}).get('sale', {}).get("price")
    type_property=classified_dict.get("property", {}).get("type")
    type_subproperty=classified_dict.get("property", {}).get("subtype")
    num_rooms = classified_dict.get("property", {}).get("bedroomCount")
    living_area = classified_dict.get("property", {}).get("netHabitableSurface")
    equipped_kitchen= 1 if classified_dict.get('property', {}).get('kitchen', {}).get('type') else 0
    furnished= 1 if classified_dict.get('transaction', {}).get('sale', {}).get('isFurnished') else 0
    open_fire= 1 if classified_dict.get("property",{}).get("fireplaceExists") else 0
    terrace = classified_dict.get('property', {}).get('terraceSurface') if classified_dict.get('property', {}).get('hasTerrace') else 0
    garden = classified_dict.get('property', {}).get('gardenSurface') if classified_dict.get('property', {}).get('hasGarden') else 0
    surface_land = classified_dict.get('property', {}).get("land",{}).get('surface') if classified_dict.get('property', {}).get('land') else 0
    facades=  classified_dict.get('property', {}).get('building', {}).get('facadeCount')
    swimming_pool= 1 if classified_dict.get("property", {}).get("hasSwimmingPool") else 0
    state_building=  classified_dict.get('property', {}).get('building', {}).get('condition')
    #epc = classified_dict.get('transaction', {}).get('certificates', {}).get("epcScore")
    type_sale1= "Public Sales" if classified_dict.get("flag",{}).get("isPublicSale") else 0
    type_sale2= "Notary Sale" if classified_dict.get("flag",{}).get("isNotarySale") else 0
    type_sale3= "New Real Estate Project" if classified_dict.get("flag",{}).get("isNewRealEstateProject") else 0


    
    
    
     # Print all variables
    print(f"ID: {id}")
    print(f"Locality: {locality}")
    print(f"Postal Code: {postal_code}")
    print(f"Price: {price_house}")
    print(f"Type of Property: {type_property}")
    print(f"Type of Subproperty: {type_subproperty}")
    print(f"Number of Rooms: {num_rooms}")
    print(f"Living Area: {living_area}")
    print(f"Equipped Kitchen: {equipped_kitchen}")
    print(f"Furnished: {furnished}")
    print(f"Open Fire: {open_fire}")
    print(f"Terrace: {terrace}")
    print(f"Garden: {garden}")
    print(f"Surface of Land: {surface_land}")
    print(f"Facades: {facades}")
    print(f"Swimming Pool: {swimming_pool}")
    print(f"State of Building: {state_building}")
    #print(f"Energy class: {epc}")

else:
    print("No script containing 'window.classified' found.")

#print(print(json.dumps(classified_dict, indent=2)))

with open("classified_data.json", 'w') as json_file:
        json.dump(classified_dict, json_file, indent=2)