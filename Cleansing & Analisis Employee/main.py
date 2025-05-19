import pandas as pd

employee = pd.read_csv('hr_dirty_employee_data.csv')
print(employee, '\n')
print(employee.dtypes, '\n')

# 🧹 Bagian 1 – Data Cleansing
# 1. Kolom Monthly Salary memiliki format yang campur aduk: ada tanda $, tulisan "USD", koma ribuan, dll. Ubah jadi float.
# 2. Kolom Join Date dalam berbagai format tanggal. Standarkan ke format YYYY-MM-DD.
# 3. Kolom Gender memiliki nilai yang tidak konsisten seperti "M", "f", "FEMALE", dll. Standarkan jadi "Male" dan "Female".
# 4. Kolom Department juga tidak konsisten: misalnya "IT" dan "I.T.", atau "HR" dan "Human Resources". Standarkan nama departemen.
# 5. Kolom Employee Name mengandung spasi tidak perlu atau kosong. Isikan yang kosong dengan "Unknown Employee".
# 6. Kolom Performance Rating berisi "N/A", NaN, atau string kosong. Gantilah nilai tersebut dengan "Unknown".

# CLEANSING
# Salary Format
employee['Monthly Salary'] = employee['Monthly Salary'].str.replace(r'(\D)','',regex=True)
employee['Monthly Salary'] = pd.to_numeric(employee['Monthly Salary'])
# Date Format
employee['Join Date'] = pd.to_datetime(employee['Join Date'], errors='coerce')
nan_date_employee = employee[employee['Join Date'].isna() | (employee['Join Date'] == False)]
employee = employee.dropna(subset=['Join Date'])
# Gender Standardize
employee['Gender'] = employee['Gender'].replace({
    r'^MALE|^male|M$|m$':'Male',
    r'FEMALE|female|F$|f$':'Female'
}, regex=True)
nan_gender_employee = employee[employee['Gender'].isna() | (employee['Gender'] == False)]
employee = employee.dropna(subset=['Gender'])
# Department Standardize
employee['Department'] = employee['Department'].replace({
    'HR':'Human Resources',
    'sales':'Sales',
    'I.T.':'IT'
})
employee['Department'] = employee['Department'].str.replace(r'Fin$','Finance',regex=True)
nan_department_employee = employee[employee['Department'].isna() | (employee['Department'] == False)]
employee = employee.dropna(subset=['Department'])
# Employee Identity Cleansing
employee['Employee Name'] = employee['Employee Name'].str.replace(r'\s+','',regex=True)
employee['Employee Name'] = employee['Employee Name'].str.replace(r'(?<!^)(?=[A-Z])',' ',regex=True)
employee['Employee Name'] = employee['Employee Name'].fillna(value='Unknown Employee')
employee = employee.drop_duplicates(subset='Employee ID')
# Employee Rating Fixing
employee['Performance Rating'] = employee['Performance Rating'].str.replace('N/A','Unknown')
employee['Performance Rating'] = employee['Performance Rating'].fillna(value='Unknown')
# Reset Dataframe Index
employee = employee.reset_index().drop(columns='index')

print(employee, '\n')

# print(nan_date_employee)
# print(nan_gender_employee)
# print(nan_department_employee)

# 📈 Bagian 2 – Data Analysis
# 1. Hitung jumlah karyawan per departemen.
# 2. Hitung rata-rata gaji bulanan tiap departemen.
# 3. Hitung rata-rata rating kinerja per gender.
# 4. Tampilkan 5 karyawan dengan gaji tertinggi.
# 5. Tampilkan berapa banyak karyawan yang belum diberi rating (Unknown) per departemen.

# ANALYTICS
# Number of Employee in each Department
employee_department = employee.groupby(['Department'])['Employee ID'].size().reset_index().rename(columns={'Employee ID':'Total Employee'})
print(employee_department, '\n')
# Average Monthly Salary in each Department
salary_department = employee.groupby(['Department'])['Monthly Salary'].mean().round().reset_index()
print(salary_department, '\n')
# Average Performance Rating in each Gender
rating_gender_male = employee[employee['Gender'] == 'Male']['Performance Rating'].value_counts().idxmax()
rating_gender_female = employee[employee['Gender'] == 'Female']['Performance Rating'].value_counts().idxmax()
rating_gender_unknown = employee[employee['Gender'] == 'unknown']['Performance Rating'].value_counts().idxmax()
rating_gender = {
    'Gender':['Male','Female','Unknown'],
    'Average Rating':[rating_gender_male,rating_gender_female,rating_gender_unknown]
}
rating_gender = pd.DataFrame(rating_gender)
print(rating_gender, '\n')
# Top 5 Highest Monthly Salary
highest_salary = employee.nlargest(5, 'Monthly Salary')
print(highest_salary, '\n')
# Number of unrated Employee
unknown_rating = employee[employee['Performance Rating'] == 'Unknown'].groupby('Department').size().reset_index(name='Unrated Employees')
print(unknown_rating, '\n')

# MISSING VALUE
# Data yang Join Date tidak sesuai
print(nan_date_employee, '\n')
# Data yang Gender tidak ada
print(nan_gender_employee, '\n')
# Data yang Department tidak ada
print(nan_department_employee, '\n')

# SUGGESTION
# 1. menurut data, dari 100 data karyawan hanya tersisa 9 karyawan. Inidikarenakan data penting yang 91 karyawan isi tidak sesuai sehingga
#    terjadi missing value. Disarankannya untuk menghimbau karyawan agar senantiasa mengisi laporan data dengan benar atau bisa diberi contoh tutorial
#    sehingga bisa terisi dengan benar kedepannya.
# 2. Kita perlu melakukan training yang layak kepada karyawan, karena menurut data ada SEDIKIT ketidakseimbangan rating kemampuan antara male dan female  
# 3. mempertimbangkan gaji karena menurut data karyawan dengan kemampuan rata rata memiliki gaji lebih banyak daripada karyawan yang memiliki rating bagus
#    di department yang sama

# LRyno