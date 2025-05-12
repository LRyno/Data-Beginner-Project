import pandas as pd

sales = pd.read_csv('global_sales.csv')
print(sales.head())

# 🧠 Soal Analisis Dataset Penjualan
# 1. Penjualan per wilayah atau negara
# Hitung total revenue dan/atau profit untuk setiap region (atau country jika ada).
# 2. Produk dengan profit tertinggi
# Agregasikan data berdasarkan kolom Item Type, lalu hitung total profit untuk setiap jenis produk. Urutkan dari yang tertinggi.
# 3. Perbandingan saluran penjualan
# Bandingkan total revenue antara Sales Channel (Online vs Offline).
# 4. Trend waktu penjualan
# Jika kolom Order Date tersedia, lihat tren penjualan (revenue atau quantity) dari waktu ke waktu (per bulan atau tahun).
# 5. Analisis berdasarkan prioritas pesanan
# Apakah pesanan dengan Order Priority "High (H)" menghasilkan rata-rata profit lebih tinggi dibanding prioritas lain?

region_country_sales = sales.groupby(['Region','Country']).agg({
    'Total Revenue': 'sum',
    'Total Profit': 'sum'
})
print(region_country_sales, '\n') # 1 : Analisis Total Revenue & Total Profit berdasarkan Region & Country

most_profit = sales.groupby(['Item Type'])['Total Profit'].sum().reset_index()
most_profit = most_profit.sort_values(['Total Profit'],ascending=False)
print(most_profit, '\n') # 2 : Analisis Tipe Produk dengan Profit Tertinggi

sales_offline = sales[sales['Sales Channel'] == 'Offline']['Total Revenue'].sum()
sales_online = sales[sales['Sales Channel'] == 'Online']['Total Revenue'].sum()
print(f"Total Revenue Channel Offline = {sales_offline:,.0f}")
print(f"Total Revenue Channel Online = {sales_online:,.0f} \n") # 3 : Membandingkan Total Revenue di Channel Off/Online

sales['Order Date'] = pd.to_datetime(sales['Order Date'])
sales['Order Year'] = sales['Order Date'].dt.year
sales_per_year = sales.groupby(['Order Year'])[['Units Sold','Total Revenue','Total Profit']].sum().reset_index().astype(int)
print(sales_per_year, '\n') # 4 : Tren Unit terjual, Total Revenue, dan Total Profit sepanjang Tahun

is_priority_H = sales[sales['Order Priority'] == 'H']['Total Profit'].mean()
is_priority_not_H = sales[sales['Order Priority'] != 'H']['Total Profit'].mean()
print(f'Rata-rata Priority "H" Profit = {is_priority_H:,.0f}')
print(f'Rata-rata Priority "selain H" Profit = {is_priority_not_H:,.0f} \n') # 5 : Membandingkan rata-rata Profit berdasarkan Prioritas H dan selain H

# Hasil Analisis
# Jenis Produk dengan Profit tertinggi: Cosmetics
# Jenis Produk dengan Profit terendah: Fruits
# Sales dengan Channel Offline memiliki Total Revenue lebih tinggi
# Produk dengan Prioritas H memiliki Profit lebih tinggi




