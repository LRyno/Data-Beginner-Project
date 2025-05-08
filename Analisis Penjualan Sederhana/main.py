import pandas as pd

data_penjualan = pd.read_csv('data_penjualan.csv')

data_penjualan['Pendapatan'] = data_penjualan['Harga'] * data_penjualan['Jumlah']
data_penjualan['Diskon'] = data_penjualan['Jumlah'].apply(lambda x:0.1 if x >= 20 else 0.05)
data_penjualan['Pendapatan_Bersih'] = data_penjualan['Pendapatan'] * (1 - data_penjualan['Diskon'])
total_revenue = data_penjualan.groupby(['Produk'])['Pendapatan_Bersih'].sum()
pivot_df = data_penjualan.pivot(index='Tanggal',columns='Produk',values='Pendapatan_Bersih')
data_penjualan['Pendapatan_Hari_Sebelumnya'] = data_penjualan.groupby('Kategori')['Pendapatan_Bersih'].shift()
data_penjualan['Perubahan_pct'] = data_penjualan['Pendapatan_Bersih'] / data_penjualan['Pendapatan_Hari_Sebelumnya'] * 100
data_penjualan['Pendapatan_Rank'] = data_penjualan['Pendapatan_Bersih'].rank(ascending=False)
data_penjualan.sort_values(['Pendapatan_Rank'],inplace=True)
data_penjualan['Tanggal'] = pd.to_datetime(data_penjualan['Tanggal'])
data_penjualan = data_penjualan.sort_values(['Kategori', 'Tanggal'])
data_penjualan['Pendapatan_Total'] = data_penjualan.groupby('Kategori')['Pendapatan'].cumsum()
print(data_penjualan)

# Insight:

most_valueable = data_penjualan.sort_values(['Pendapatan_Bersih'],ascending=False)[['Kategori','Produk','Pendapatan_Bersih']]
print(most_valueable.head()) # paling menguntungkan: Muffin & Kopi Latte

most_sold_day = data_penjualan.sort_values(['Jumlah'],ascending=False)[['Tanggal','Produk','Jumlah']]
print(most_sold_day.head()) # tanggal penjualan tertinggi: 03

mean_category_minuman = data_penjualan[data_penjualan['Kategori']=='Minuman']['Pendapatan'].mean()
mean_category_makanan = data_penjualan[data_penjualan['Kategori']=='Makanan']['Pendapatan'].mean()
print(mean_category_minuman)
print(mean_category_makanan) # rata_rata kategori pendapatan tertinggi: Minuman

pola_df = data_penjualan.sort_values('Tanggal')[['Tanggal','Pendapatan','Perubahan_pct']]
print(pola_df) # berikut polanya
