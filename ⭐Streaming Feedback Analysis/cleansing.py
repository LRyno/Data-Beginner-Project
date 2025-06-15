import pandas as pd
import numpy as np

df = pd.read_csv('streaming_feedback_dirty.csv')
print(df, 'n')

df = df.drop_duplicates(subset='User_ID')
df = df.dropna(subset='User_ID')
df['Nama'] = df['Nama'].replace(np.nan, 'Unknown')
df['Email'] = df['Email'].replace(np.nan, 'Unknown')
df['Gender'] = (
    df['Gender']
    .str.replace(r'\s+', '', regex=True)
    .str.replace(r'M$|m$', 'Male', regex=True)
    .str.replace(r'F$|f$', 'Female', regex=True)
    .replace(np.nan, 'Unknown')
)
df['Nama'] = df['Nama'].str.title()
df['Gender'] = df['Gender'].str.title()
df['Age'] = df['Age'].apply(lambda x: x if 6 <= x <= 100 else None)
df = df.dropna(subset='Age')
df['Subscription_Date'] = df['Subscription_Date'].str.replace('/', '-')
df['Subscription_Date'] = pd.to_datetime(df['Subscription_Date'], errors='coerce')
df = df.dropna(subset='Subscription_Date')
df['Subscription_Type'] = df['Subscription_Type'].replace(np.nan, 'Unknown')
df['Subscription_Type'] = df['Subscription_Type'].str.lower()
df['Subscription_Type'] = df['Subscription_Type'].str.title()

def monthly_fee(type):
    if type == 'Basic':
        return 50000
    elif type == 'Premium':
        return 100000
    elif type == 'Free':
        return 0
    else:
        return 'Unknown'
    
df['Monthly_Fee'] = df['Subscription_Type'].apply(monthly_fee)
df['Watch_Time_Hours'] = df['Watch_Time_Hours'].str.replace('-', '')
df['Watch_Time_Hours'] = pd.to_numeric(df['Watch_Time_Hours'], errors='coerce')
df['Watch_Time_Hours'] = df['Watch_Time_Hours'].replace(np.nan, 'Unknown')

def satisfaction_score(score):
    if score in ['0', '1', '2', '3', '4', '5']:
        return 'Very Bad'
    elif score in ['6', '7', '8', '9', '10']:
        return 'Good'
    else:
        return 'Unknown'
    
df['Satisfaction_Score'] = df['Satisfaction_Score'].apply(satisfaction_score)
df['Feedback_Text'] = df['Feedback_Text'].replace(np.nan, 'Unknown')

print(df, '\n')

df.to_csv('streaming_feedback_clean.csv', index=False)