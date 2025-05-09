import pandas as pd
import datetime as dt

def load_data(file_path):
    """Load data from CSV and drop unnecessary columns."""
    df = pd.read_csv(file_path)
    return df.drop(columns='Index')

def calculate_gender_distribution(df):
    """Calculate the number of users by gender for each job and their percentages."""
    gender_count = df.groupby(['Job Title', 'Sex']).size().unstack(fill_value=0)
    gender_count['Total'] = gender_count.sum(axis=1)
    gender_count['Female Pct'] = (gender_count['Female'] / gender_count['Total']) * 100
    gender_count['Male Pct'] = (gender_count['Male'] / gender_count['Total']) * 100
    return gender_count

def calculate_age(df):
    """Calculate age based on the date of birth."""
    df['Datetime'] = pd.to_datetime(df['Date of birth'], format="%Y-%m-%d")
    today_date = dt.date.today()
    df['Age(2025)'] = today_date.year - df['Datetime'].dt.year
    df['Age(2025)'] -= ((today_date.month < df['Datetime'].dt.month) | 
                         ((today_date.month == df['Datetime'].dt.month) & 
                          (today_date.day < df['Datetime'].dt.day))).astype(int)
    return df

def segment_age(df):
    """Create age segments based on the calculated age."""
    df['Segment'] = df['Age(2025)'].apply(lambda x: 'Teen' if x < 25 else 'Old' if x >= 45 else 'Adult')
    return df

def calculate_age_statistics(df):
    """Calculate mean, max, and min age for each gender."""
    mean_female_age = df[df['Sex'] == 'Female']['Age(2025)'].mean().round()
    mean_male_age = df[df['Sex'] == 'Male']['Age(2025)'].mean().round()
    
    female_df = df[df['Sex'] == 'Female']
    male_df = df[df['Sex'] == 'Male']
    
    age_stats = {
        'Statistic': ['Mean Age', 'Max Age', 'Min Age'],
        'Female': [mean_female_age, female_df['Age(2025)'].max(), female_df['Age(2025)'].min()],
        'Male': [mean_male_age, male_df['Age(2025)'].max(), male_df['Age(2025)'].min()]
    }
    
    return pd.DataFrame(age_stats)

def main():
    # Load data
    people_df = load_data('people-100.csv')
    print(people_df.head(), '\n')

    # Task 1: Gender distribution by job
    gender_distribution = calculate_gender_distribution(people_df)
    print(gender_distribution, '\n')

    # Calculate age
    people_df = calculate_age(people_df)

    # Segment age
    people_df = segment_age(people_df)
    print(people_df, '\n')

    # Task 2: Count users by job and age segment
    age_segment_count = people_df.groupby(['Job Title', 'Segment']).size().unstack(fill_value=0)
    print(age_segment_count, '\n')

    # Task 3: Age statistics by gender
    age_statistics = calculate_age_statistics(people_df)
    print(age_statistics, '\n')

if __name__ == "__main__":
    main()
