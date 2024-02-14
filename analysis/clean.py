import pandas as pd
import matplotlib.pyplot as plt


# Specify the path to your CSV file
csv_file_path = '/Users/sahar/becode/immo-eliza-scraping-goats/dayta.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Replace empty values with NaN
df.replace('', pd.NA, inplace=True)