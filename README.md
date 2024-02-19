# Immo-Eliza-GOATS

Welcome to Immo-Eliza-GOATS, your premier solution for sophisticated real estate data acquisition and analysis from Immoweb. It features a Web Scraper, with data cleaning and soon to be Machine Learning model built in Python for collecting real estate data. It fetches property details such as price, location, and many more, then saves the data to a CSV file. The data can be cleaned and pre-processed, as well as analysed through the notebooks.

## 🚀Features

- Asynchronous web scraping using asyncio and aiohttp.
- Extracts detailed information about properties listed on Immoweb.
- Saves collected data to a CSV file.
- Cleaning and Pre-processing
- Variable analysis and dynamic map

## 🏡Real Estate Data
Our scraper module extracts the following house features from each property:
- Locality
- Construction Year
- Number of Frontages
- Province
- ZIP Code
- Price
- Property Type
- Subproperty Type
- Bedroom Count
- Total Area (m²)
- Equipped Kitchen
- Furnished
- Open Fire
- Terrace Area (m²)
- Terrace
- Garden Area (m²)
- Garden
- Flood Zone Type
- Surface Land
- Swimming Pool
- State of Building
- EPC (Energy Performance Certificate)
- Primary Energy Consumption per m²
- Heating Type
- Double Glazing
- Cadastral Income
- Latitude
- Longitude
# 🏁Getting Started


## 🛠️Installation

**Clone the Repository:**

```bash
git clone git@github.com:sahar-mahmoudi/immo-eliza-goats.git
cd immo-eliza-goats
```
**Create a Virtual Environment (Optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate
```
**Install Dependencies:**

```bash
pip install -r requirements.txt
```
## 👩‍💻Usage
For the ImmoCrawler:

```bash
python scrape.py
```
To clean the dataset:

```bash
python clean.py
```

##  📁Project Structure
- scraper/: Contains the ImmoCrawler class and related modules.
- scrape.py: Main script to run the ImmoCrawler.
- requirements.txt: List of Python dependencies.
- clean.py/: Cleans the output dataset from the scraper
- Data/: Contains a sample output from both the cleaned and raw dataset
- analysis/: Notebook and figures from analysis the dataset
## 👥Contributors 
Hazem El-Dabaa : [GitHub](https://github.com/HazemEldabaa)

Sahar Mahmoudi : [Github](https://github.com/sahar-mahmoudi)

Mimoun Atmani : [Github](https://github.com/1Dh2Be)

