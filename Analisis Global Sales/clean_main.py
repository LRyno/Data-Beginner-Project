import pandas as pd

def load_data(file_path):
    """Load sales data from a CSV file."""
    return pd.read_csv(file_path)

def analyze_sales_by_region(sales):
    """Calculate total revenue and profit by region and country."""
    return sales.groupby(['Region', 'Country']).agg({
        'Total Revenue': 'sum',
        'Total Profit': 'sum'
    })

def analyze_profit_by_item_type(sales):
    """Calculate total profit by item type and sort by profit."""
    profit_by_item = sales.groupby(['Item Type'])['Total Profit'].sum().reset_index()
    return profit_by_item.sort_values(['Total Profit'], ascending=False)

def compare_sales_channels(sales):
    """Compare total revenue between online and offline sales channels."""
    sales_offline = sales[sales['Sales Channel'] == 'Offline']['Total Revenue'].sum()
    sales_online = sales[sales['Sales Channel'] == 'Online']['Total Revenue'].sum()
    return sales_offline, sales_online

def analyze_sales_trend(sales):
    """Analyze sales trend over time."""
    sales['Order Date'] = pd.to_datetime(sales['Order Date'])
    sales['Order Year'] = sales['Order Date'].dt.year
    return sales.groupby(['Order Year'])[['Units Sold', 'Total Revenue', 'Total Profit']].sum().reset_index().astype(int)

def analyze_order_priority(sales):
    """Compare average profit based on order priority."""
    high_priority_profit = sales[sales['Order Priority'] == 'H']['Total Profit'].mean()
    non_high_priority_profit = sales[sales['Order Priority'] != 'H']['Total Profit'].mean()
    return high_priority_profit, non_high_priority_profit

def main():
    # Load data
    sales = load_data('global_sales.csv')
    
    # 1. Analyze total revenue and profit by region and country
    region_country_sales = analyze_sales_by_region(sales)
    print(region_country_sales, '\n')

    # 2. Analyze item type with highest profit
    most_profit = analyze_profit_by_item_type(sales)
    print(most_profit, '\n')

    # 3. Compare total revenue between sales channels
    sales_offline, sales_online = compare_sales_channels(sales)
    print(f"Total Revenue Channel Offline = {sales_offline:,.0f}")
    print(f"Total Revenue Channel Online = {sales_online:,.0f} \n")

    # 4. Analyze sales trend over time
    sales_per_year = analyze_sales_trend(sales)
    print(sales_per_year, '\n')

    # 5. Compare average profit based on order priority
    is_priority_H, is_priority_not_H = analyze_order_priority(sales)
    print(f'Rata-rata Priority "H" Profit = {is_priority_H:,.0f}')
    print(f'Rata-rata Priority "selain H" Profit = {is_priority_not_H:,.0f} \n')

if __name__ == "__main__":
    main()
