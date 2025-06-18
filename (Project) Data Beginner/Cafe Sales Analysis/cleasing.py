import pandas as pd
import numpy as np

df = pd.read_csv('dirty_cafe_sales.csv')
print(df, '\n')

df = df.drop_duplicates(subset='Transaction ID')
df['Item'] = (
    df['Item']
    .replace('UNKNOWN', np.nan)
    .replace('Unknown', np.nan)
    .replace('ERROR', np.nan)
    .replace('Error', np.nan)
)
nan_df_item = df[df['Item'].isna() | (df['Item'] == False)]
df = df.dropna(subset='Item')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Price Per Unit'] = pd.to_numeric(df['Price Per Unit'], errors='coerce')
df['Total Spent'] = pd.to_numeric(df['Total Spent'], errors='coerce')
df['Payment Method'] = (
    df['Payment Method']
    .str.replace('UNKNOWN', 'Unknown')
    .str.replace('ERROR', 'Error')
    .replace(np.nan, 'Unknown')
)
df['Location'] = (
    df['Location']
    .str.replace('UNKNOWN', 'Unknown')
    .str.replace('ERROR', 'Error')
    .replace(np.nan, 'Unknown')
)
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
nan_df_date = df[df['Transaction Date'].isna() | (df['Transaction Date'] == False)]
df = df.dropna(subset='Transaction Date')
df = df.reset_index(drop=True)

print(df, '\n')

# MISSING VALUE (on Item and Transaction Date)
nan_df = pd.concat([nan_df_date, nan_df_item]).reset_index(drop=True)
print(nan_df, '\n')

df.to_csv('clean_cafe_sales.csv', index=False)
nan_df.to_csv('nan_cafe_sales.csv', index=False)
