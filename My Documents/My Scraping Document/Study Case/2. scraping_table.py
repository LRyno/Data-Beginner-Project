import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv

# ---Get URL---
url = 'https://www.worldometers.info/coronavirus/'
response = requests.get(url)
soup = bs(response.text, 'html.parser')

# ---Get table---
table = soup.find('table', {'id':'main_table_countries_today'})

# ---Get table elements---
data = []

for rows in table.find_all('tr'):
    items = rows.find_all(['td', 'th'])
    data.append([item.get_text(strip=True) for item in items])

with open('data_tabel.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

