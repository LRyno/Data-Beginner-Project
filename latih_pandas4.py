import pandas as pd
import numpy as np

coffee = pd.read_csv('coffee.csv')
bios = pd.read_csv('bios.csv')
nocs = pd.read_csv('noc_regions.csv')
results = pd.read_csv('results.csv')

coffee['Price'] = 4.99 # nambah kolom jika tidak ada
coffee['New_Price'] = np.where(coffee['Coffee Type']=='Espresso',3.99,5.99) # ubah harga
coffee.drop(columns=['Price'],inplace=True) # hapus kolom harga lama
coffee['Revenue'] = coffee['Units Sold'] * coffee['New_Price'] # buat kolom baru = revenue
coffee.rename(columns={'New_Price':'Price'},inplace=True) # ganti nama kolom

# print(coffee)

bios_new = bios.copy()
bios_new['first_name'] = bios_new['name'].str.split(' ').str[0] # hanya ambil nama pertama
bios_new['born_datetime'] = pd.to_datetime(bios_new['born_date']) # ubah ke format datetime
bios_new['born_year'] = bios_new['born_datetime'].dt.year
bios_new.drop(columns=['born_datetime'],inplace=True)
bios_new['height_category'] = bios_new['height_cm'].apply(lambda x:'Short' if x < 165 else 'Average' if x < 185 else 'Tall')

def categorize_athlete(row):
    if row['height_cm'] < 175 and row['weight_kg'] < 70:
        return 'Lightweight'
    elif row['height_cm'] < 185 and row['weight_kg'] <= 80:
        return 'Middleweight'

    else:
        return 'Heavyweight'
    
bios_new['Category'] = bios_new.apply(categorize_athlete,axis=1)
bios_new = pd.merge(bios_new,nocs,left_on='born_country',right_on='NOC',how='left') # menggabungkan 2 dataframe (kiri dari nocs cocok ke born country, kanan dari nocs cocok ke NOC)
bios_new.rename(columns={'region':'born_country_full'},inplace=True)
bios_new.drop(columns=['notes'],inplace=True)

# print(bios_new.head())

usa_df = bios_new[bios_new['born_country']=='USA'].copy() # membuat datafram khusus USA
gbr_df = bios_new[bios_new['born_country']=='GBR'].copy()
only_usagbr = pd.concat([usa_df,gbr_df]) # menggabung datafram USA dan GBR yg telah dibuat secara tumpuk

# print(only_usagbr.head())
# print(only_usagbr.tail())

combined_df = pd.merge(results,bios_new,on='athlete_id',how='left') # menggabungkan secara athlete id yang cocok
# print(combined_df.head())

# coffee.loc[[0,1], 'Units Sold'] = np.nan
# coffee.fillna(coffee['Units Sold'].mean(),inplace=True) # akan mengisi NaN dengan Mean jika diawal disarankan begini
coffee.loc[[2,3], 'Units Sold'] = np.nan
coffee['Units Sold'] = coffee['Units Sold'].interpolate() # akan mengisi NaN dengan prediksi pola
# coffee.loc[[4,5], 'Units Sold'] = np.nan
# coffee.dropna(subset=['Units Sold'],inplace=True) # Menghapus yang ada NaN
# coffee.loc[[6,7], 'Units Sold'] = np.nan
# coffee = coffee[coffee['Units Sold'].isna()] # mencari nilai NaN
# coffee = coffee[coffee['Units Sold'].notna()] # mencari nilai selain NaN

# print(coffee)

value_born_city = bios['born_city'].value_counts() # menghitung berapa banyak value tersebut
value_usa_born_country = bios[bios['born_country']=='USA']['born_region'].value_counts() # hanya di USA
# print(value_usa_born_country)

total_sold_by_type = coffee.groupby(['Coffee Type'])['Units Sold'].sum() # total sold setiap tipe kopi nya
groupby = coffee.groupby(['Coffee Type']).agg({'Units Sold':'sum','Price':'mean'}) # jika units sold = sum, jika price = mean
# print(groupby)

pivot_coffee = coffee.pivot(columns='Coffee Type',index='Day',values='Revenue') # mengelompokan sendiri Coffe type mnjadi kolom, day menjadi index, revenue menjadi nilai 
# print(pivot_coffee)

coffee['Yesterday_Revenue'] = coffee['Revenue'].shift(2) # melihat 2 nilai sebelumnya dari 'Revenue'
coffee['pct_change'] = coffee['Revenue'] / coffee['Yesterday_Revenue'] 
# print(coffee)

bios['height_rank'] = bios['height_cm'].rank(ascending=False) # meranking height_cm, ascending = false
bios.sort_values(['height_rank'],inplace=True)
# print(bios[['name','height_cm','height_rank']])

coffee['cumulative_revenue'] = coffee['Revenue'].cumsum() # menghitung total revenue dari awal sampai akhir
# print(coffee)

