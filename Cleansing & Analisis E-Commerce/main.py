import pandas as pd

ecommerce = pd.read_csv('ecommerce_dirty_data.csv')
print(ecommerce.head(), '\n')

# 📌 Bagian 1 – Data Cleansing
# 1. Bersihkan kolom Price per Unit dan Total Amount dari simbol $, tulisan USD, dan tanda koma. Ubah menjadi tipe data (float).
# 2. Hitung kembali nilai total penjualan dengan cara Quantity * Price per Unit dan bandingkan dengan kolom Total Amount.
#    Buat kolom baru bernama Calculated Amount. Apakah ada perbedaan nilai?
# 3. Cek transaksi tidak valid, seperti:
#     Total Amount negatif
#     Quantity bernilai 0
#     Price per Unit bernilai 0
# 4. Perbaiki kolom Rating, ubah "4 stars" jadi 4, "Not Rated" atau NaN menjadi 0.
# 5. Isi nama pelanggan yang kosong (Customer Name) dengan "Unknown Customer".
# 6. Standarkan nama negara, misalnya ubah [US] menjadi USA, [UK] menjadi United Kingdom, dan hapus karakter tidak perlu.
# 7. Hapus baris produk yang tidak valid, seperti produk bernama "Unknown [deprecated]".

# Price per Unit & Total Amount
ecommerce['Price per Unit'] = ecommerce['Price per Unit'].str.replace(r"(\D)",'',regex=True)
ecommerce['Total Amount'] = ecommerce['Total Amount'].str.replace(r"(\D)",'',regex=True)
ecommerce['Price per Unit'] = pd.to_numeric(ecommerce['Price per Unit'])
ecommerce['Total Amount'] = pd.to_numeric(ecommerce['Total Amount'])
# Re-Calculate Total Amount
ecommerce['Calculated Amount'] = ecommerce['Quantity'] * ecommerce['Price per Unit']
ecommerce = ecommerce.drop(ecommerce[ecommerce['Quantity'] <= 0].index)
ecommerce = ecommerce.drop(ecommerce[ecommerce['Price per Unit'] <= 0].index)
# Get Rating
ecommerce['Rating'] = ecommerce['Rating'].str.replace(r"Not Rated",'0',regex=True)
ecommerce['Rating'] = ecommerce['Rating'].str.replace(r"(\D+)",'',regex=True)
ecommerce['Rating'] = ecommerce['Rating'].fillna(value=0)
ecommerce['Rating'] = pd.to_numeric(ecommerce['Rating'])
# Cleansing Name, Country, and Product
ecommerce['Customer Name'] = ecommerce['Customer Name'].fillna(value='Unknown Customer')
ecommerce['Country'] = ecommerce['Country'].str.replace(r"[\[\]\W+]",'',regex=True)
ecommerce['Country'] = ecommerce['Country'].str.replace(r"(US$)",'USA',regex=True)
ecommerce['Country'] = ecommerce['Country'].str.replace(r"UK",'United Kingdom',regex=True)
ecommerce = ecommerce.drop(ecommerce[ecommerce['Product'] == 'Unknown [deprecated]'].index)
ecommerce = ecommerce.reset_index().drop(columns='index')
print(ecommerce, '\n')

# 📌 Bagian 2 – Analisis Data
# 1. Hitung total penjualan (Total Amount) per negara. Urutkan dari negara dengan penjualan terbesar ke terkecil.
# 2. Hitung jumlah transaksi per kategori produk. Apa kategori dengan penjualan terbanyak?
# 3. Tampilkan 5 produk dengan pendapatan tertinggi.
# 4. Rating = 0 padahal Total Amount 5 tertinggi
# 5. Cek rata-rata rating per kategori produk. Kategori mana yang paling disukai pelanggan?

# Highest income in India
country_amount = ecommerce.groupby(['Country'])['Calculated Amount'].sum().reset_index()
country_amount = country_amount.sort_values(by='Calculated Amount', ascending=False)
print(country_amount, '\n')
# Highest category purchases in Accessories
quantity_category = ecommerce.groupby(['Category'])['Quantity'].sum().reset_index()
quantity_category = quantity_category.sort_values(by='Quantity', ascending=False)
print(quantity_category, '\n')
# Top 5 Product with highest revenue
most_valueable = ecommerce.groupby(['Product'])['Calculated Amount'].sum().reset_index()
most_valueable = most_valueable.sort_values(by='Calculated Amount', ascending=False)
print(most_valueable.head(5), '\n')
# The 0 rating product but with highest revenue
zero_rating = ecommerce[ecommerce['Rating'] == 0][['Country','Product','Calculated Amount','Rating']]
zero_rating = zero_rating.nlargest(5, 'Calculated Amount')
print(zero_rating, '\n')
# Average rating in each category
average_rating = ecommerce.groupby(['Category'])['Rating'].mean().round()
print(average_rating)

# Conclusion:
# 1. Menurut data, kita bisa memfokuskan penjualan kita lebih banyak di negara India
#    dan untuk UK kita bisa mengurangi stok nya guna menghemat biaya atau kita harus lebih mengusahakan marketing di UK
# 2. Menurut data, banyak penjualan terjadi di kategori aksesoris sehingga masalah stok kita bisa atasi jelas.
#    Sedang kita tau bahwa kategori elektronik kurang digemari entah karena harga yang kita beri terlalu mahal atau kita kurang dimarketing sehingga kurang peminat
# 3. Kita bisa membuat sistem jika pembeli memberikan rating maka akan diberi hadiah berupa koin yang bisa ditukarkan menjadi kupon.
#    Karena menurut data kita memiliki produk dengan pendapatan tinggi namun memiliki rating 0. Disitu banyak di produk camera dan negara jepang
# 4. Dapat dilihat sesuai data, rata rata rating kategori gadgets dan office adalah 2. Kita perlu melakukan quality control terhadap produk di kategori tersebut
#    dan juga alangkah baiknya kita terbuka terhadap review pembeli

