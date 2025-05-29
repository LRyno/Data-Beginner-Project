import pandas as pd
import numpy as np

food = pd.read_csv('raw_dirty_food_dataset.csv')
print(food, '\n')

# Save original df
food_copy = food.copy()
# CLEANSING
# Remove Dupe Food ID
food = food.drop_duplicates(subset='Food ID')
# Name
food['Name'] = food['Name'].str.title()
food['Name'] = food['Name'].str.replace(r'^\s+|\s+$','', regex=True)
# Calories
food['Calories'] = food['Calories'].str.replace('kcal','')
food['Calories'] = pd.to_numeric(food['Calories'], errors='coerce')
food['Ingredients'] = (
    food['Ingredients']
    .str.replace(r'^\s+|\s+$|\s+,',',', regex=True)
    .str.replace(r',(\S)', r', \1', regex=True)
    .replace(r',$',np.nan, regex=True)
)
# Country
food['Country'] = food['Country'].str.title()
food['Country'] = (
    food['Country']
    .replace('N/A',np.nan)
    .str.replace(r'Indo$','Indonesia', regex=True)
)
# Price
food['Price'] = food['Price'].str.replace(r'\D+','', regex=True)
food['Price'] = pd.to_numeric(food['Price'])
# Rating
food['Rating'] = (
    food['Rating']
    .str.replace(r'^\s+|\s+$','', regex=True)
    .str.replace(',','.', regex=True)
)
food['Rating'] = food['Rating'].str.replace('excellent','5')
food['Rating'] = pd.to_numeric(food['Rating'], errors='coerce')
# Available
food['Available'] = (
    food['Available']
    .str.replace(r'Y$|y$|yes$|TRUE$|True$|true$','Yes', regex=True)
    .str.replace(r'N$|n$|no$|FALSE$|False$|false$','No', regex=True)
)
# Date Added
food['Date Added'] = (
    food['Date Added']
    .str.replace(r'/','-', regex=True)
    .str.replace(r'\s+Jan\s+','/01/', regex=True)
)
food['Date Added'] = pd.to_datetime(food['Date Added'], errors='coerce')
# Reset Index
food = food.reset_index().drop(columns='index')
print(food, '\n')

# 🎯 Soal Analisis
# 1. Berapa rata-rata kalori makanan yang valid?
# 2. Makanan apa saja yang memiliki kalori di atas 500?
# 3. Berapa total jumlah makanan yang berasal dari Indonesia?
# 4. Berapa harga rata-rata makanan di dataset tersebut?
# 5. Tampilkan 5 makanan dengan rating tertinggi.
# 6. Ada berapa makanan yang tersedia dan tidak tersedia?
# 7. Berapa jumlah makanan yang ditambahkan pada tahun 2021?
# 8. Berapa banyak makanan yang punya nama unik?

# ANALYTICS
# 1
average_calories = food.dropna(subset=['Food ID','Name','Calories'])
average_calories = average_calories.groupby(['Name'])['Calories'].mean().__round__().reset_index().rename(columns={'Calories':'Average Calories'})
print(average_calories, '\n')
# 2
up_500_calories = food[food['Calories'] > 500][['Food ID','Name','Calories']]
print(up_500_calories, '\n')
# 3
indonesian_food = food[food['Country'] == 'Indonesia']['Name'].count()
print('Total makanan dari Indonesia:', indonesian_food, '\n')
# 4
average_price = food['Price'].mean().__round__()
print(f'Harga rata-rata makanan: Rp. {average_price}')
# 5
top_rating = food.nlargest(5, 'Rating')
print(top_rating, '\n')
# 6
availability = food['Available'].value_counts().reset_index()
print(availability, '\n')
# 7
food['Date Year'] = food['Date Added'].dt.year
added_2021 = food[food['Date Year'] == 2021]['Name'].count()
food = food.drop(columns='Date Year')
print('Jumlah makanan yang ditambah pada tahun 2021:', added_2021, '\n')
# 8
unique_food = food['Name'].nunique()
print('Jumlah makanan dengan nama unik:', unique_food, '\n')

# Save cleaned df
food.to_csv('food_clean_dataset.csv', index=False)