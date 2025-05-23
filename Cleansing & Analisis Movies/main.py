import pandas as pd

movies = pd.read_csv('movies.csv')
print(movies)

# 1. Pembersihan Awal
# Buang/mengisi nilai kosong (NaN) di kolom RATING, Gross, RunTime, dan VOTES
# Format VOTES dan Gross menjadi angka
# Hapus karakter spesial dan spasi berlebih pada GENRE dan STARS
# Gabungkan baris panjang dari kolom seperti STARS, ONE-LINE, atau DIRECTOR yang terpecah

# CLEANSING
# MISSING VALUE
nan_year = movies[movies['YEAR'].isna() | (movies['YEAR'] == False)]
nan_genre = movies[movies['GENRE'].isna() | (movies['GENRE'] == False)]
# Clean the NaN and Dupe Value
movies = movies.drop_duplicates(subset=['MOVIES'])
movies = movies.dropna(subset=['MOVIES']) 
movies = movies.dropna(subset=['YEAR']) 
movies = movies.dropna(subset=['GENRE'])
movies = movies.dropna(subset=['STARS'])
# Clean Years
movies['YEARS'] = movies['YEAR'].str.findall(r'\d{4}')
movies['YEARS CLEAN'] = movies['YEARS'].apply(
    lambda x: '-'.join(x) if x else None
)
# Clean Genre
movies['GENRE CLEAN'] = movies['GENRE'].str.replace(r'^\W+|\W+$', '', regex=True)
movies['ONE-LINE CLEAN'] = movies['ONE-LINE'].str.replace(r'^\W+|\W+$', '', regex=True)
movies['STARS CLEAN'] = (
    movies['STARS']
    .str.replace(r'\|\s*', '', regex=True)           # hilangkan tanda '|'
    .str.replace(r'Stars:', '', regex=True)          # hilangkan 'Stars:'
    .str.replace(r'\n', ' ', regex=True)             # ganti newline jadi spasi
    .str.replace(r'\s+', ' ', regex=True)            # rapikan spasi ganda
    .str.replace(r'Director: ', '', regex=True)            # hapus 'director:'
    .str.strip()                                     # hapus spasi depan/belakang
)
# Change Votes & Gross Dtypes to float
movies["VOTES"] = movies["VOTES"].str.replace(",", "").astype(float)
movies['Gross'] = movies['Gross'].str.replace(r'\$+|[A-Z]', '', regex=True).astype(float)
nan_gross = movies[movies['Gross'].isna() | (movies['Gross'] == False)]
movies = movies.dropna(subset='Gross')
# Reset indexing
movies = movies.drop(columns=['YEARS','YEAR','GENRE','ONE-LINE','STARS'])
movies = movies.reset_index().drop(columns='index')
print(movies)

# 2. Analisis Data
# Cari 5 film/series dengan rating IMDb tertinggi
# Hitung berapa banyak film per genre (bisa multi-label)
# Film terbanyak rilis di tahun berapa
# Pemeran yang paling sering muncul di banyak film
# Hubungan antara runtime dengan rating
# Hubungan antara penghasilan dengan rating

# Analytics
# Top 5 Highest movies rating
top_movies_rating = movies.nlargest(5, 'RATING')
print(top_movies_rating, '\n')
# Number of movies each genre
movies_genre = movies.groupby(['GENRE CLEAN'])['MOVIES'].count().reset_index()
print(movies_genre, '\n')
# The year with the most film releases
movies_realese = movies.groupby(['YEARS CLEAN'])['MOVIES'].count().sort_values(ascending=False).head(1).reset_index()
print(movies_realese, '\n')
# Actor with the most films
top_stars = movies.groupby(['STARS CLEAN'])['MOVIES'].count().sort_values(ascending=False).head(1).reset_index()
print(top_stars, '\n')
# Runtime vs rating
runtime_rating = movies.groupby(['RATING'])['RunTime'].sum().reset_index()
print(runtime_rating, '\n')
# Gross vvs rating
gross_rating = movies.groupby(['RATING'])['Gross'].sum().reset_index()
print(gross_rating, '\n')

# MISSING VALUE
print(nan_year, '\n')
print(nan_genre, '\n')
print(nan_gross, '\n')

# Save Cleaned CSV
movies.to_csv('movies_clean.csv',index=False)