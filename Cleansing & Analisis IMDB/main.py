import pandas as pd
import numpy as np

imdb = pd.read_csv('imdb_dataset.csv', delimiter=';', on_bad_lines='skip')
print(imdb, '\n')

# CLEANSING
# Basic fixing columns
imdb = imdb.drop(columns='Income')
imdb = imdb.rename(columns={'Unnamed: 9':'Income'})
imdb = imdb.drop_duplicates(subset=['IMBD title ID'])
# Fixing release year format
imdb['Release year'] = (
    imdb['Release year']
    .str.replace(r'\s+','-', regex=True)
    .str.replace(r'-+', '-', regex=True)
    .str.replace(r'^-', '', regex=True)
    .str.replace(r'-$', '', regex=True)
)
imdb['Release year'] = pd.to_datetime(imdb['Release year'], errors='coerce')
# MISSING VALUE 1
nan_year = imdb[imdb['Release year'].isna() | (imdb['Release year'] == False)]
nan_title = imdb[imdb['Original title'].isna() | (imdb['Original title'] == False)]
nan_genre = imdb[imdb['Genre'].isna() | (imdb['Genre'] == False)]
# Drop NaN values
imdb = imdb.dropna(subset='Original title')
imdb = imdb.dropna(subset='Release year')
imdb = imdb.dropna(subset='Genre')
# Fixing duration format
imdb['Duration'] = (
    imdb['Duration']
    .replace('',np.nan)
    .replace(' ',np.nan)
    .replace(r'[a-zA-Z]+$',np.nan, regex=True)
)
# MISSING VALUE 2
nan_duration = imdb[imdb['Duration'].isna() | (imdb['Duration'] == False)]
imdb = imdb.dropna(subset='Duration')
# Fixing country format
imdb['Country'] = (
    imdb['Country']
    .str.replace('US$','USA')
    .str.replace('US.','USA')
    .str.replace('UK','United Kingdom')
    .str.replace('Italy1','Italy')
    .str.replace('West Germany','Germany')
)
# Fixing content rating format
imdb['Content Rating'] = (
    imdb['Content Rating']
    .replace(np.nan,'Not Rated')
    .replace('#N/A','Not Rated')
)
# Fixing director, income, votes format
imdb['Director'] = imdb['Director'].replace(np.nan,'Unknown')
imdb['Income'] = imdb['Income'].str.replace(r'[\Wa-z]+','', regex=True).astype(float)
imdb['Votes'] = imdb['Votes'].str.replace(r'[\Wa-z]+','', regex=True).astype(float)
# Fixing score format
imdb['Score'] = (
    imdb['Score']
    .replace(np.nan,'No Score')
    .str.replace(',','')
    .str.replace(':','.')
    .str.replace(r'\.+','.', regex=True)
    .str.replace(r'(?<=\d)(?=\d)','.', regex=True)
)
# Reset dataframe index
imdb = imdb.reset_index().drop(columns='index')
print(imdb, '\n')

# 1. Tampilkan tiga tahun dengan film terbanyak.
# 2. Genre Paling Populer
# 3. Film Terlaris sesuai income
# 4. Korelasi Durasi–Score
# 5. Director dengan Rata-rata Score Tertinggi
# 6. Hitung mean(Income) per Country.
# 7. Buat kolom baru GrossPerVote = Income / Votes. Tampilkan film dengan GrossPerVote tertinggi (top 5).
# 8. Content Rating vs Score
# 9. 3 Pasangan Genre Paling Umum
# 10. Tren Rilis Bulanan

# ANALYSIS
# Copy cleaned dataframe
imdb_copy = imdb.copy()
# 3 years with the most films released
imdb_copy['Year'] = imdb_copy['Release year'].dt.year
most_year = imdb_copy.groupby(['Year'])['IMBD title ID'].count().reset_index().rename(columns=({'IMBD title ID':'Film release'})).nlargest(3, 'Film release')
print(most_year, '\n')
# Most popular genre
imdb_copy['Genre list'] = imdb_copy['Genre'].str.split(',')
imdb_copy['Genre list'] = imdb_copy['Genre list'].apply(lambda genres: [g.strip() for g in genres])
genres_exploded = imdb_copy.explode('Genre list')
popular_genre = genres_exploded['Genre list'].value_counts().reset_index().head(1)
print(popular_genre, '\n')
# The biggest earnings from films
max_income_index = imdb_copy['Income'].idxmax()
most_income = imdb_copy.loc[max_income_index, ['IMBD title ID','Original title','Income']]
print(most_income, '\n')
# Duration-score correlation
imdb_copy['Score'] = pd.to_numeric(imdb_copy['Score'])
duration_score = imdb_copy.groupby(['Duration'])['Score'].mean().round(1).sort_values(ascending=False)
print(duration_score, '\n')
# The highest scored director
imdb_copy['Director list'] = imdb_copy['Director'].str.split(',')
imdb_copy['Director list'] = imdb_copy['Director list'].apply(lambda genres: [g.strip() for g in genres])
director_exploded = imdb_copy.explode('Director list')
most_score_director = director_exploded.groupby(['Director list'])['Score'].mean().reset_index().nlargest(1, 'Score')
print(most_score_director, '\n')
# Income per country
average_income_country = imdb_copy.groupby(['Country'])['Income'].mean().reset_index().rename(columns={'Income':'Average Income'})
print(average_income_country, '\n')
# Top 5 biggest Gross/Votes
imdb_copy['Gross/Votes'] = imdb_copy['Income'] / imdb_copy['Votes']
gross_votes = imdb_copy.drop(columns=['Director list','Genre list', 'Year']).nlargest(5, 'Gross/Votes')
print(gross_votes, '\n')
# Rating-score correlation
rating_score = imdb_copy.groupby(['Content Rating'])['Score'].mean()
print(rating_score, '\n')
# Top 3 popular genre pairing 
general_genre_pairing = imdb_copy['Genre'].value_counts().reset_index().head(3)
print(general_genre_pairing, '\n')
# Monthly release trend
imdb_copy['Month'] = imdb_copy['Release year'].dt.month
monthly_tren = imdb_copy.groupby(['Month'])['IMBD title ID'].count().reset_index().rename(columns={'IMBD title ID':'Film Release'})
print(monthly_tren, '\n')

# MISSING VALUE
print(nan_year, '\n')
print(nan_title, '\n')
print(nan_genre, '\n')
print(nan_duration, '\n')

# Save cleaned dataframe
imdb.to_csv('imdb_clean.csv', index=False)