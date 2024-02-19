import pandas as pd

# Clean EPC column
def extract_epc(value):
    if isinstance(value, str) and '_' in value:
        parts = value.split('_')
        return parts[-1]
    else:
        return value
    
def map_to_numerical(column, mapping):
    return column.map(mapping)

# Read the CSV file into a pandas DataFrame
immo = pd.read_csv('Data/raw/final_raw.csv')

#remove unnecessary columns
#immo_c = immo.drop(columns=["Unnamed: 0", "public_sales","notary_sales","country","id", "longitude", "latitude", "link"], axis=1)
immo_c = immo.drop(columns=["Unnamed: 0",  "link", "country", "public_sales", "notary_sales", "id"], axis=1)


#df = df.drop(df.columns[[0, 1, 30, 31, 32, 33]], axis=1)

# Replace empty values with NaN
immo_c.replace('', pd.NA, inplace=True)

immo_c.head()
#clean EPC
immo_c['epc'] = immo_c['epc'].apply(extract_epc)
immo_c['epc'].value_counts().to_frame()

#Custom mappings
epc_mapping = {'A++': 9, 'A+': 8, 'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1}
state_mapping = {'JUST_RENOVATED': 6, 'AS_NEW': 5, 'GOOD': 4, 'TO_BE_DONE_UP': 3, 'TO_RENOVATE': 2, 'TO_RESTORE': 1}
propert_type={'APARTMENT': 1, 'HOUSE': 0}
# Apply mappings to create new numerical columns
immo_c["epc"] = map_to_numerical(immo_c["epc"], epc_mapping)
immo_c["state_building"] = map_to_numerical(immo_c["state_building"], state_mapping)
immo_c["property_type"] = map_to_numerical(immo_c["property_type"], propert_type)


# Create a dictionary with the different regions. 
belgium_regions = {
    'Antwerp': 'Flanders',
    'Limburg': 'Flanders',
    'East Flanders': 'Flanders',
    'Flemish Brabant': 'Flanders',
    'West Flanders': 'Flanders',
    'Hainaut': 'Wallonia',
    'Walloon Brabant': 'Wallonia',
    'Namur': 'Wallonia',
    'Liège': 'Wallonia',
    'Luxembourg': 'Wallonia',
    'Brussels': 'Brussels-Capital'
}
# Create a new data set and map it with belgium_regions
immo_c["region"] = immo_c["province"].map(belgium_regions)

# clean the data -> romove nan in total_area_m2
cleaned_sqm = immo_c.dropna(subset="total_area_m2")

# calculate the price/sqm
immo_c["price_square"] = cleaned_sqm["price"] / cleaned_sqm["total_area_m2"]


immo_c.head()
immo_c.to_csv("Data/cleaned/clean_set.csv")

