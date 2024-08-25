import pandas as pd

file_name = 'Jeff_Wilson_Sources.xlsx'
df = pd.read_excel(file_name)

def extract_info(soup, source_type):
    if source_type == 'blog':
        return ' '.join([p.get_text() for p in soup.find_all('p')])
    elif source_type == 'video':
        return soup.find('title').get_text()
    # Add more conditions as needed
extracted_data = []

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def fetch_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_info(soup, source_type):
    if source_type == 'blog':
        return ' '.join([p.get_text() for p in soup.find_all('p')])
    elif source_type == 'video':
        return soup.find('title').get_text()
    # Add more conditions as needed

file_name = 'Jeff_Wilson_Sources.xlsx'
df = pd.read_excel(file_name)

extracted_data = []

for index, row in df.iterrows():
    url = row['Source']
    description = row['Description']
    soup = fetch_data(url)
    content = extract_info(soup, 'blog')  # Adjust based on source type
    extracted_data.append({'Description': description, 'Content': content})
    print(f"Content from {description}: {content}")

with open('extracted_data.json', 'w') as json_file:
    json.dump(extracted_data, json_file, indent=4)