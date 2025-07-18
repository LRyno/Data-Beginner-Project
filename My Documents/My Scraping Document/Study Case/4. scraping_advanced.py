import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from tqdm import tqdm

# Base URL
url = 'https://www.scrapingcourse.com/ecommerce/'

# Parameter scraping
max_page = 12
all_product = []

# Scraping tiap halaman dengan progress bar
for page in tqdm(range(1, max_page + 1), desc="Scraping Pages"):
    try:
        response = requests.get(f'{url}page/{page}/')
        soup = bs(response.text, 'html.parser')

        items = soup.find('ul', {'class': 'products columns-4'})

        if not items:
            print(f"Produk tidak ditemukan di halaman {page}")
            continue

        for item in items.find_all('li', {'data-products': 'item'}):
            name = item.find('h2', {'class': 'product-name woocommerce-loop-product__title'})
            price = item.find('span', {'class': 'product-price woocommerce-Price-amount amount'})
            if name and price:
                all_product.append({
                    'Product': name.get_text(strip=True),
                    'Price': price.get_text(strip=True)
                })

        time.sleep(1)

    except requests.exceptions.RequestException as error:
        print(f"Gagal akses halaman {page}: {error}")
        continue

# Buat DataFrame dan simpan
df = pd.DataFrame(all_product)
df.to_csv('advanced_ecommerce.csv', index=False)
