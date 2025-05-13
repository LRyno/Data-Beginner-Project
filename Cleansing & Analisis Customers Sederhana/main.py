import pandas as pd

customer = pd.read_csv('raw_customer_data.csv')
print(customer, '\n')

# 🔧 Bagian Cleansing (Sederhana)
# 1. Tangani nilai yang hilang (missing values) di kolom Customer ID, Gender, Purchase Amount, dan Country.
# 2. Perbaiki format tanggal pada kolom Join Date ke format standar YYYY-MM-DD.
# 3. Validasi kolom Email — hanya email yang valid (mengandung "@" dan ".") yang boleh dipakai.
# 4. Hapus duplikat jika ada (misalnya duplikat Customer ID atau baris yang identik).

# 📊 Bagian Analisis (Setelah Cleansing)
# 5. Hitung rata-rata dan total Purchase Amount per negara.
# 6. Hitung jumlah pelanggan berdasarkan jenis kelamin (Gender).
# 7. Urutkan pelanggan dengan Purchase Amount tertinggi.

# Cleansing
customer['Join Date'] = pd.to_datetime(customer['Join Date'], errors='coerce')
customer = customer.drop_duplicates(subset='Customer ID')
customer = customer.dropna(subset=['Customer ID','Join Date'])
customer['Valid Email'] = customer['Email'].str.contains(r'^[\w\.-]+@[\w\.-]+\.\w+$', na=False)
customer = customer[customer['Valid Email'] == True]
customer = customer.drop(columns='Valid Email')
customer['Gender'] = customer['Gender'].fillna('Unknown')
print(customer, '\n')

# Analytics
# Total dan rata-rata purchase amount setiap country
total_purchase_country = customer.groupby(['Country'])['Purchase Amount'].sum().reset_index().rename(columns={'Purchase Amount':'Total Purchase'})
mean_purchase_country = customer.groupby(['Country'])['Purchase Amount'].mean().reset_index().rename(columns={'Purchase Amount':'Mean Purchase'})
total_mean_purchase_country = pd.merge(total_purchase_country,mean_purchase_country, on='Country',how='left')
print(total_mean_purchase_country, '\n')

# jumlah pelanggan setiap gender
gender_purchase = customer['Gender'].value_counts()
print(gender_purchase, '\n')

# urutan pelanggan dari purchase amount tertinggi
sort_customers = customer.sort_values(by='Purchase Amount', ascending=False)
print(sort_customers)


