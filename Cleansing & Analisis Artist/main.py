import pandas as pd

artist = pd.read_csv('artist rank.csv')
print(artist)
print(artist.dtypes, '\n')

# ✅ Langkah-langkah yang harus kamu lakukan:
# 1. Hilangkan tanda dolar, koma, dan kurung dari kolom keuangan dan ubah ke tipe float.
# 2. Bersihkan kolom Rank, Peak, dan All Time Peak dari karakter kurung siku [ ], huruf, dan angka acuan (misalnya [4], [b]).
# 3. Tangani duplikat baris (hilangkan jika perlu).
# 4. Tangani missing values secara tepat, misalnya: 
#         Jika Rank kosong, isi dengan Unknown.
#         Jika Year(s) atau Tour title kosong, isi dengan Unknown.
# 5. Ubah kolom Year(s) menjadi tahun awal dan akhir terpisah (Start Year, End Year).

# Cleansing
artist = artist.drop(columns='Ref.')
artist['Actual gross'] = artist['Actual gross'].str.replace(r'(\D)','',regex=True)
artist['Actual gross'] = pd.to_numeric(artist['Actual gross'])
artist['Adjusted gross (in 2022 dollars)'] = artist['Adjusted gross (in 2022 dollars)'].str.replace(r'(\D)','',regex=True)
artist['Adjusted gross (in 2022 dollars)'] = pd.to_numeric(artist['Adjusted gross (in 2022 dollars)'])
artist['Average gross'] = artist['Average gross'].str.replace(r'(\D)','',regex=True)
artist['Average gross'] = pd.to_numeric(artist['Average gross'])

artist['Peak'] = artist['Peak'].str.replace(r'\[.+\]','',regex=True)
artist['All Time Peak'] = artist['All Time Peak'].str.replace(r'\[.+\]','',regex=True)

artist[['Peak','All Time Peak']] = artist[['Peak','All Time Peak']].fillna('Unknown')
artist['Tour title'] = artist['Tour title'].str.replace(r'\s[†‡*\[\]].*','',regex=True)
print(artist, '\n')

# ✅ Jawablah pertanyaan berikut:
# 1. Tampilkan 5 artis dengan Actual gross tertinggi secara keseluruhan.
# 2. Hitung jumlah tur yang dilakukan oleh setiap artis, lalu urutkan dari yang paling banyak.
# 3. Berapa rata-rata gross per show dari semua artis?
# 4. Berapa total adjusted gross dari konser yang dilakukan di atas 100 show?
# 5. Tur mana yang memiliki rata-rata gross tertinggi per show?
# 6. Total gross per artis
# 8. Jumlah konser per tahun awal (Start Year)

# Analytics
# 5 Artis actual gross tertinggi
top_actual_gross = artist.nlargest(5, 'Actual gross')[['Artist','Actual gross']]
print(top_actual_gross, '\n')

# Jumlah tur setiap artis, dari paling banyak
count_tour = artist.groupby(['Artist'])['Tour title'].count().reset_index().rename(columns={'Tour title':'Numbers of tour'})
count_tour = count_tour.sort_values(by='Numbers of tour', ascending= False)
print(count_tour, '\n')

# Rata=rata gross per shows semua artis
mean_gross_tour = artist.groupby('Artist').agg({'Actual gross':'sum','Shows':'sum'}).reset_index()
mean_gross_tour['Gross per Shows'] = mean_gross_tour['Actual gross']/mean_gross_tour['Shows']
print(mean_gross_tour, '\n')

# Total adjusted gross dari konser yang dilakukan lebih dari 100 show
hundred_shows_adjusted_gross = artist[artist['Shows'] > 100]['Adjusted gross (in 2022 dollars)'].sum()
print(f"Total Adjusted gross (in 2020 dollars) from shows > 100: {hundred_shows_adjusted_gross:,.0f} \n")

# Tur dengan rata-rata gross per shows tertinggi
tour_highest = artist.copy()
tour_highest['Gross per Shows'] = tour_highest['Actual gross']/tour_highest['Shows']
result = tour_highest[['Tour title','Gross per Shows']].sort_values(by='Gross per Shows',ascending=False).head(1)
print(result, '\n')

# Total gross setiap artis
gross_artist = artist.groupby(['Artist'])['Actual gross'].sum().reset_index()
print(gross_artist, '\n')

# Jumlah konser setiap tahun
artist[['Start Year', 'End Year']] = artist['Year(s)'].str.extract(r'(\d{4})[–-](\d{4})')
artist['Start Year'] = pd.to_numeric(artist['Start Year'], errors='coerce')
tour_per_year = artist.groupby(['Start Year'])['Tour title'].count()
print(tour_per_year)


