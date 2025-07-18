import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = 'https://www.scrapethissite.com/pages/simple/'
response = requests.get(url)
soup = bs(response.text, 'html.parser')

name = soup.find_all('div', {'class':'col-md-4 country'})
info = soup.find_all('div', {'class':'country-info'})

country_name = []
capital_country = []
population_country = []
area_country = []

for item in name:
    name = item.find('h3', {'class':'country-name'})
    get_name = name.get_text(strip=True)
    country_name.append(get_name)
    
for item in info:
    capital = item.find('span', {'class':'country-capital'})
    get_capital = capital.get_text(strip=True)
    capital_country.append(get_capital)

    population = item.find('span', {'class':'country-population'})
    get_population = population.get_text(strip=True)
    population_country.append(get_population)

    area = item.find('span', {'class':'country-area'})
    get_area = area.get_text(strip=True)
    area_country.append(get_area)
    
df_list = {
    'Country':country_name,
    'Capital City':capital_country,
    'Population':population_country,
    'Area(Km)':area_country
}

df = pd.DataFrame(df_list)
print(df)