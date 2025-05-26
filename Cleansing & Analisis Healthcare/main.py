import pandas as pd
import numpy as np

healthcare = pd.read_csv('Healthcare.csv')
print(healthcare, '\n')
# print(healthcare.dtypes, '\n')

# Save original df
healthcare_original = healthcare.copy()

# Name Capitalize Fixing
healthcare['Patient Name'] = healthcare['Patient Name'].str.title()
# Age and Visit Date Fixing
healthcare['Age'] = healthcare['Age'].str.replace('forty', '40')
healthcare['Visit Date'] = (
    healthcare['Visit Date']
    .str.replace('-', '/')
    .str.replace('.', '/')
)
healthcare['Visit Date'] = pd.to_datetime(healthcare['Visit Date'], errors='coerce')
# MISSING VALUE
nan_gender = healthcare[healthcare['Gender'].isna() | (healthcare['Gender'] == False)]
nan_age = healthcare[healthcare['Age'].isna() | (healthcare['Age'] == False)]
nan_date = healthcare[healthcare['Visit Date'].isna() | (healthcare['Visit Date'] == False)]
nan_blood = healthcare[healthcare['Blood Pressure'].isna() | (healthcare['Blood Pressure'] == False)]
nan_cholesterol = healthcare[healthcare['Cholesterol'].isna() | (healthcare['Cholesterol'] == False)]
# Change Age Dtype
healthcare['Age'] = pd.to_numeric(healthcare['Age'], errors='coerce')
# Contact Fixing 
healthcare['Phone Number'] = (
    healthcare['Phone Number']
    .replace('', np.nan)
    .replace(' ', np.nan)
)
healthcare['Email'] = (
    healthcare['Email']
    .replace('', np.nan)
    .replace(' ', np.nan)
)
# Drop NaN Value
healthcare = healthcare.dropna(subset='Gender')
healthcare = healthcare.dropna(subset='Age')
healthcare = healthcare.dropna(subset='Visit Date')
healthcare = healthcare.dropna(subset='Blood Pressure')
healthcare = healthcare.dropna(subset='Cholesterol')
print(healthcare, '\n')

# 📊 Analytics:
# Berapa rata-rata umur pasien yang memiliki catatan usia valid dan lengkap?
# Berapa jumlah pasien unik berdasarkan nama (tidak hanya baris data)?
# Apa 2 kondisi medis terbanyak yang dicatat dalam data ini?
# Berapa banyak pasien yang tidak menerima obat apapun (Medication = NONE atau kosong)?
# Berapa proporsi pasien yang memiliki tekanan darah tinggi (Blood Pressure > 130/80)?
# Berapa jumlah pasien yang tidak memiliki informasi kontak (baik Email maupun Phone Number kosong atau 'nan')?
# Tampilkan tren jumlah kunjungan pasien dari tahun ke tahun (Visit Date).

# Average patient age was 45
average_age = healthcare['Age'].mean().__round__()
print(f'Rata-rata umur pasien yang datang: {average_age} \n')
# The number of unique patient names is 10
healthcare_unique = healthcare.drop_duplicates(subset='Patient Name', keep='first')
total_unique = healthcare_unique['Patient Name'].nunique()
print(f'Jumlah nama pasien yang unik: {total_unique} \n')
# Top 2 conditions
most_condition = healthcare['Condition'].value_counts(ascending=False).reset_index()
print(most_condition.head(2), '\n')
# Number of patients who didnt reveive medication
medication_none = healthcare[healthcare['Medication'] == 'NONE']['Medication'].value_counts().reset_index()
print(medication_none, '\n')
# Blood pressure comparison
def is_higher_blood(pressure):
    sistolik, diastolik = map(int, pressure.split('/'))
    return(sistolik > 130) or (sistolik == 130 and diastolik > 80)
total_blood = healthcare['Blood Pressure'].apply(is_higher_blood).count()
ishigh_blood = healthcare['Blood Pressure'].apply(is_higher_blood).sum()
print(f'Proporsi pasien yang memiliki tekanan darah tinggi: {ishigh_blood}/{total_blood} \n')
# Number of patients who have no contacts
contact_none = healthcare[(healthcare['Email'].isna()) | (healthcare['Phone Number'].isna())].shape[0]
print(f'jumlah pasien yang tidak memiliki informasi kontak: {contact_none} \n')
# Visit trends per year
healthcare['Visit Date'] = pd.to_datetime(healthcare['Visit Date'], errors='coerce')
healthcare['Visit Years'] = healthcare['Visit Date'].dt.year
year_tren = healthcare.groupby(['Visit Years'])['Patient Name'].count()
healthcare = healthcare.drop(columns='Visit Years')
print(year_tren, '\n')

# MISSING VALUE
print(nan_gender, '\n')
print(nan_age, '\n')
print(nan_date, '\n')
print(nan_blood, '\n')
print(nan_cholesterol, '\n')

# Save the cleaned CSV
healthcare.to_csv('healthcare_clean.csv',index=False)