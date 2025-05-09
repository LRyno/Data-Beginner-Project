import pandas as pd
import datetime as dt

people_df = pd.read_csv('people-100.csv')
people_df = people_df.drop(columns='Index')
print(people_df.head(), '\n')

# Tugas Anda:
# 1. Hitung jumlah pengguna laki-laki dan perempuan untuk setiap jenis pekerjaan (pekerjaan).
#    Hitung juga persentase masing-masing jenis kelamin di setiap pekerjaan.
#    Tampilkan hasil dalam bentuk DataFrame

# 2. Buat kolom baru segment_usia berdasarkan umur:
    # <25 → "muda"
    # 25–44 → "dewasa"
    # ≥45 → "tua"
#    Hitung jumlah pengguna di setiap kombinasi pekerjaan dan segment_usia.
#    Tampilkan hasil dalam format pivot

# 3. Hitung rata-rata usia untuk laki-laki dan perempuan.
#    Hitung juga rentang usia (usia terkecil dan terbesar) untuk masing-masing jenis kelamin.
#    Tampilkan hasilnya dalam bentuk tabel

jumlah_kelamin = people_df.groupby(['Job Title', 'Sex']).size().unstack(fill_value=0)
jumlah_kelamin['Total'] = jumlah_kelamin.sum(axis=1)

jumlah_kelamin['Female Pct'] = jumlah_kelamin['Female'] / jumlah_kelamin['Total'] * 100
jumlah_kelamin['Male Pct'] = jumlah_kelamin['Male'] / jumlah_kelamin['Total'] * 100
print(jumlah_kelamin, '\n') #1

people_df['Datetime'] = pd.to_datetime(people_df['Date of birth'],format="%Y-%m-%d")
today_date = dt.date.today()
people_df['Age(2025)'] = today_date.year - people_df['Datetime'].dt.year
people_df['Age(2025)'] -= ((today_date.month < people_df['Datetime'].dt.month) | 
                      ((today_date.month == people_df['Datetime'].dt.month) & 
                       (today_date.day < people_df['Datetime'].dt.day))).astype(int)
print(people_df)

people_df['Segment'] = people_df['Age(2025)'].apply(lambda x:'Teen' if x < 25 else 'Old' if  x >= 45 else 'Adult')
print(people_df, '\n')

jumlah_segment_usia = people_df.groupby(['Job Title', 'Segment']).size().unstack(fill_value=0)
print(jumlah_segment_usia, '\n') #2

mean_female_age = people_df[people_df['Sex'] == 'Female']['Age(2025)'].mean().__round__()
mean_male_age = people_df[people_df['Sex'] == 'Male']['Age(2025)'].mean().__round__()
female_df = people_df[people_df['Sex'] == 'Female'].copy()
male_df = people_df[people_df['Sex'] == 'Male'].copy()
max_female_age = female_df['Age(2025)'].max()
min_female_age = female_df['Age(2025)'].min()
max_male_age = male_df['Age(2025)'].max()
min_male_age = male_df['Age(2025)'].min()

summary_age_df = pd.DataFrame({
    'Statistic': ['Mean Age', 'Max Age', 'Min Age'],
    'Female': [mean_female_age, max_female_age, min_female_age],
    'Male': [mean_male_age, max_male_age, min_male_age]
})
print(summary_age_df, '\n') #3

