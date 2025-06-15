import pandas as pd

industri = pd.read_csv('perusahaan industri.csv')
industri.drop(columns='kode_provinsi',inplace=True)
industri.drop(columns='Nama_Provinsi',inplace=True)
industri.sort_values(['Tahun'],inplace=True) 
industri.reset_index(inplace=True)
industri.drop(columns='index',inplace=True)

# 1. Jumlah perusahaan per tahun
# 2. Berapa total jumlah perusahaan per kecamatan selama 3 tahun terakhir (2021–2023)?
# 3. Total investasi dan nilai produk di tahun 2023
# 4. Kecamatan dengan nilai produk tertinggi di 2023
# 5. Rata-rata produktivitas tenaga kerja di 2023
# 6. Pivot jumlah perusahaan

print(industri)
print(industri.info(), '\n')

jumlah_perusahaan_pertahun = industri.groupby('Tahun')['Jumlah_Perusahaan'].sum().reset_index()
print(jumlah_perusahaan_pertahun, '\n') #1


total_perusahaan_per_kecamatan = industri.groupby("Nama_Kecamatan")["Jumlah_Perusahaan"].sum().reset_index()
total_perusahaan_per_kecamatan = total_perusahaan_per_kecamatan.sort_values("Jumlah_Perusahaan", ascending=False)
print(total_perusahaan_per_kecamatan, '\n') #2


# Hapus koma dan spasi, lalu dtypes ubah ke float
industri['Nilai_Investasi'] = industri['Nilai_Investasi'].astype(str).str.replace(',', '', regex=False).str.replace(' ', '', regex=False).astype(float)
industri['Nilai_Produk'] = industri['Nilai_Produk'].astype(str).str.replace(',', '', regex=False).str.replace(' ', '', regex=False).astype(float)

industri_2023 = industri[industri['Tahun'] == 2023]
total_investasi_2023 = industri_2023['Nilai_Investasi'].sum()
total_produk_2023 = industri_2023['Nilai_Produk'].sum()
print(f"Total Invest 2023 = {total_investasi_2023:,.0f}")
print(f"Total Produk 2023 = {total_produk_2023:,.0f} \n") #3


tertinggi = industri_2023.loc[industri_2023['Nilai_Produk'].idxmax()]
print(f"Kecamatan dengan nilai produk tertinggi di 2023: {tertinggi['Nama_Kecamatan']}")
print(f"Dengan nilai produk: {tertinggi['Nilai_Produk']:,.0f} \n") #4


industri_2023 = industri[industri["Tahun"] == 2023].copy()
# Buang spasi dan koma di kolom 'Jumlah_Tenaga_Kerja' dan 'Nilai_Produk'
industri_2023["Jumlah_Tenaga_Kerja"] = industri_2023["Jumlah_Tenaga_Kerja"].astype(str).str.replace(",", "").str.strip()
industri_2023["Nilai_Produk"] = industri_2023["Nilai_Produk"].astype(str).str.replace(",", "").str.strip()

# Konversi ke float
industri_2023["Jumlah_Tenaga_Kerja"] = pd.to_numeric(industri_2023["Jumlah_Tenaga_Kerja"], errors='coerce')
industri_2023["Nilai_Produk"] = pd.to_numeric(industri_2023["Nilai_Produk"], errors='coerce')

industri_2023.dropna(subset=['Jumlah_Tenaga_Kerja','Nilai_Produk'])
industri_2023['Produktivitas'] = industri_2023['Nilai_Produk'] / industri_2023['Jumlah_Tenaga_Kerja']
mean_produktivitas = industri_2023['Produktivitas'].mean()
print(f"Rata_rata Produktivitas 2023: {mean_produktivitas:,.0f} \n") #5


pivot_perusahaan = industri.pivot_table(
    values='Jumlah_Perusahaan', 
    index='Nama_Kecamatan', 
    columns='Tahun', 
    aggfunc='sum',  # Aggregasi jumlah perusahaan
    fill_value=0    # Mengisi NaN dengan 0
)
print(pivot_perusahaan) #6


