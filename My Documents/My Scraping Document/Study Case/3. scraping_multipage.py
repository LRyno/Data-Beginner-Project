import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = 'https://www.scrapethissite.com/pages/forms/'
page = 1
all_data = []
max_pages = 24

while page <= max_pages:
    response = requests.get(f'{url}?page_num={page}')
    soup = bs(response.text, 'html.parser')

    table = soup.find('table', {'class':'table'})
    if not table:
        break

    if page == 1:
        headers = []
        for header in table.find_all('th'):
            item = header.get_text(strip=True)
            headers.append(item)

    for rows in table.find_all('tr', {'class':'team'}):
        items = rows.find_all('td')
        if items:
            data = [item.get_text(strip=True) for item in items]
            all_data.append(data)
        
    page += 1
    
df = pd.DataFrame(all_data, columns=headers)
df.to_csv('scraped_data.csv', index=False)
