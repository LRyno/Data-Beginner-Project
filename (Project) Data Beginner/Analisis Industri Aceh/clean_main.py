import pandas as pd

# Load data
industri = pd.read_csv('perusahaan_industri.csv')

# Preprocessing data
industri.drop(columns=['kode_provinsi', 'Nama_Provinsi'], inplace=True)
industri.sort_values(['Tahun'], inplace=True)
industri.reset_index(drop=True, inplace=True)

# Display basic information about the dataset
print(industri)
print(industri.info(), '\n')

# 1. Jumlah perusahaan per tahun
jumlah_perusahaan_pertahun = industri.groupby('Tahun')['Jumlah_Perusahaan'].sum().reset_index()
print(jumlah_perusahaan_pertahun, '\n')

# 2. Total jumlah perusahaan per kecamatan selama 3 tahun terakhir (2021–2023)
total_perusahaan_per_kecamatan = industri.groupby("Nama_Kecamatan")["Jumlah_Perusahaan"].sum().reset_index()
total_perusahaan_per_kecamatan.sort_values("Jumlah_Perusahaan", ascending=False, inplace=True)
print(total_perusahaan_per_kecamatan, '\n')

# 3. Total investasi dan nilai produk di tahun 2023
# Clean and convert data types
for column in ['Nilai_Investasi', 'Nilai_Produk']:
    industri[column] = (
        industri[column]
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.replace(' ', '', regex=False)
        .astype(float)
    )

industri_2023 = industri[industri['Tahun'] == 2023]
total_investasi_2023 = industri_2023['Nilai_Investasi'].sum()
total_produk_2023 = industri_2023['Nilai_Produk'].sum()
print(f"Total Invest 2023 = {total_investasi_2023:,.0f}")
print(f"Total Produk 2023 = {total_produk_2023:,.0f} \n")

# 4. Kecamatan dengan nilai produk tertinggi di 2023
tertinggi = industri_2023.loc[industri_2023['Nilai_Produk'].idxmax()]
print(f"Kecamatan dengan nilai produk tertinggi di 2023: {tertinggi['Nama_Kecamatan']}")
print(f"Dengan nilai produk: {tertinggi['Nilai_Produk']:,.0f} \n")

# 5. Rata-rata produktivitas tenaga kerja di 2023
industri_2023['Jumlah_Tenaga_Kerja'] = (
    industri_2023['Jumlah_Tenaga_Kerja']
    .astype(str)
    .str.replace(",", "")
    .str.strip()
)

# Convert to numeric and calculate productivity
industri_2023['Jumlah_Tenaga_Kerja'] = pd.to_numeric(industri_2023['Jumlah_Tenaga_Kerja'], errors='coerce')
industri_2023.dropna(subset=['Jumlah_Tenaga_Kerja', 'Nilai_Produk'], inplace=True)
industri_2023['Produktivitas'] = industri_2023['Nilai_Produk'] / industri_2023['Jumlah_Tenaga_Kerja']
mean_produktivitas = industri_2023['Produktivitas'].mean()
print(f"Rata-rata Produktivitas 2023: {mean_produktivitas:,.0f} \n")

# 6. Pivot jumlah perusahaan
pivot_perusahaan = industri.pivot_table(
    values='Jumlah_Perusahaan', 
    index='Nama_Kecamatan', 
    columns='Tahun', 
    aggfunc='sum',  
    fill_value=0    
)
print(pivot_perusahaan)
