import pandas as pd

def load_data(file_path):
    """Load sales data from a CSV file."""
    return pd.read_csv(file_path)

def calculate_revenue(data):
    """Calculate revenue and net revenue with discounts."""
    data['Pendapatan'] = data['Harga'] * data['Jumlah']
    data['Diskon'] = data['Jumlah'].apply(lambda x: 0.1 if x >= 20 else 0.05)
    data['Pendapatan_Bersih'] = data['Pendapatan'] * (1 - data['Diskon'])
    return data

def analyze_revenue(data):
    """Perform revenue analysis and return relevant insights."""
    total_revenue = data.groupby(['Produk'])['Pendapatan_Bersih'].sum()
    data['Pendapatan_Hari_Sebelumnya'] = data.groupby('Kategori')['Pendapatan_Bersih'].shift()
    data['Perubahan_pct'] = data['Pendapatan_Bersih'] / data['Pendapatan_Hari_Sebelumnya'] * 100
    data['Pendapatan_Rank'] = data['Pendapatan_Bersih'].rank(ascending=False)
    return data, total_revenue

def prepare_data(data):
    """Prepare and sort data for analysis."""
    data['Tanggal'] = pd.to_datetime(data['Tanggal'])
    data.sort_values(['Kategori', 'Tanggal'], inplace=True)
    data['Pendapatan_Total'] = data.groupby('Kategori')['Pendapatan'].cumsum()
    return data

def get_insights(data):
    """Extract insights from the data."""
    most_valuable = data.sort_values(['Pendapatan_Bersih'], ascending=False)[['Kategori', 'Produk', 'Pendapatan_Bersih']]
    most_sold_day = data.sort_values(['Jumlah'], ascending=False)[['Tanggal', 'Produk', 'Jumlah']]
    mean_category_minuman = data[data['Kategori'] == 'Minuman']['Pendapatan'].mean()
    mean_category_makanan = data[data['Kategori'] == 'Makanan']['Pendapatan'].mean()
    
    return most_valuable, most_sold_day, mean_category_minuman, mean_category_makanan

def main():
    # Load data
    data_penjualan = load_data('data_penjualan.csv')
    
    # Calculate revenue
    data_penjualan = calculate_revenue(data_penjualan)
    
    # Analyze revenue
    data_penjualan, total_revenue = analyze_revenue(data_penjualan)
    
    # Prepare data for further analysis
    data_penjualan = prepare_data(data_penjualan)
    
    # Get insights
    most_valuable, most_sold_day, mean_category_minuman, mean_category_makanan = get_insights(data_penjualan)
    
    # Print results
    print(data_penjualan)
    print(most_valuable.head())  # Most valuable products
    print(most_sold_day.head())   # Most sold days
    print(mean_category_minuman)   # Mean revenue for Minuman category
    print(mean_category_makanan)    # Mean revenue for Makanan category
    print(data_penjualan[['Tanggal', 'Pendapatan', 'Perubahan_pct']].sort_values('Tanggal'))  # Revenue pattern

if __name__ == "__main__":
    main()
