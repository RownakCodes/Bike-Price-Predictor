import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Base URL of the webpage to scrape
base_url = "https://bikroy.com/en/ads/bangladesh/motorbikes-scooters?page="

# Initialize lists to store scraped data
models = []
speeds = []
types = []
prices = []
brands = []

# Specify the number of pages to scrape
num_pages = 1 # Change this to the desired number of pages

# Loop through each page
for page_num in range(1, num_pages + 1):
    url = base_url + str(page_num)
    
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        print(f"Successfully fetched page {page_num}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        time.sleep(5)  # Wait before retrying
        continue

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the listings on the page
    listings = soup.find_all('div', class_='content--3JNQz')

    # Iterate through the listings and extract data
    for listing in listings:
        model_element = listing.find('h2', class_='heading--2eONR heading-2--1OnX8 title--3yncE block--3v-Ow')
        model = model_element.text.strip() if model_element else ""
        brand = model.split() if model else ["nan"]
        description = listing.find('div', class_='description--2-ez3').text.strip() if listing.find('div', class_='description--2-ez3') else "nan"
        b_type = description.split(',')[1].strip() if ',' in description else "nan"
        speed = listing.find('div').text.strip() if listing.find('div') else "nan"
        speed_list = speed.split() if speed else ["nan"]
        price = listing.find('div', class_='price--3SnqI color--t0tGX').text.strip() if listing.find('div', class_='price--3SnqI color--t0tGX') else "nan"
        price_list = price.split() if price else ["nan"]

        models.append(model)
        brands.append(brand)
        types.append(b_type)
        speeds.append(speed_list)
        prices.append(price_list)

# Create a DataFrame from the scraped data
data_list = []
for i in range(len(models)):
    data_list.append({
        'Brand': brands[i][0] if brands[i] else "nan",
        'Model': models[i],
        'Type': types[i],
        'Speed': speeds[i][0] if speeds[i] else "nan",
        'Price': prices[i][1] if len(prices[i]) > 1 else "nan"
    })

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data_list)

# Print the first few rows of the DataFrame
print(f"Total rows collected: {len(df)}")

# Ensure absolute path is used
save_path = r'C:\bike\Data'  # Use raw string to handle backslashes
try:
    # Create directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)
    
    # Full path to the CSV file
    csv_path = os.path.join(save_path, 'motorbike_data.csv')
    
    # Save the DataFrame
    df.to_csv(csv_path, index=False)
    
    print(f"CSV file saved successfully at: {csv_path}")
    print(f"File exists: {os.path.exists(csv_path)}")
except Exception as e:
    print(f"Error saving CSV file: {e}")