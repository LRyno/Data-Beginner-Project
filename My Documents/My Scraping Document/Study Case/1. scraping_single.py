import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# ---Get URL---
url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
response = requests.get(url)
# print(response)
soup = bs(response.text, 'html.parser')
# print(soup)

# ---Get element---
title = soup.find('a', {'class':'title'})
# print(title.string)

# ---Get all element---
all_title = soup.find_all('a', {'class':'title'})
all_desc = soup.find_all('p', {'class':'description card-text'})
all_price = soup.find_all('span', {'itemprop':'price'})
all_review = soup.find_all('span', {'itemprop':'reviewCount'})

# ---Element to the list---
title_list = []
for item in all_title:
    title = item.get_text(strip=True)
    title_list.append(title)

desc_list = []
for item in all_desc:
    desc = item.get_text(strip=True)
    desc_list.append(desc)

price_list = []
for item in all_price:
    price = item.get_text(strip=True)
    price_list.append(price)

review_list = []
for item in all_review:
    review = item.get_text(strip=True)
    review_list.append(review)

# ---List to dataframe---
df = pd.DataFrame({
    'Laptop':title_list,
    'Price':price_list,
    'Reviews':review_list,
    'Description':desc_list
})

print(df)

# ---To CSV---
df.to_csv('laptop_dirty.csv', index=False)