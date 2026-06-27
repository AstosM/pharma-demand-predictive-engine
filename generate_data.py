import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for consistency
np.random.seed(42)
num_records = 10000

# Setup categories matching a health consulting scenario
regions = ['North', 'South', 'East', 'West', 'Central']
drugs = ['GlycaCure 50mg', 'OncoShield 10mg']
hospitals = [f'Apollo Medical Center {i}' for i in range(1, 6)] + \
            [f'Fortis Healthcare {i}' for i in range(1, 6)] + \
            [f'Max Super Speciality {i}' for i in range(1, 6)]

# Create a realistic timeline over the last year
start_date = datetime(2025, 6, 1)
date_list = [start_date + timedelta(days=int(np.random.randint(0, 365))) for _ in range(num_records)]

# Create the data dictionary
data = {
    'Transaction_ID': [f'TXN{100000 + i}' for i in range(num_records)],
    'Date': date_list,
    'Region': np.random.choice(regions, num_records),
    'Drug_Name': np.random.choice(drugs, num_records),
    'Hospital_Name': np.random.choice(hospitals, num_records),
    'Units_Ordered': np.random.randint(10, 150, num_records),
    'Price_Per_Unit': np.random.choice([120, 250], num_records)
}

df = pd.DataFrame(data)

# Make OncoShield premium priced for realism
df.loc[df['Drug_Name'] == 'OncoShield 10mg', 'Price_Per_Unit'] = 450
df['Total_Revenue'] = df['Units_Ordered'] * df['Price_Per_Unit']

# Sort sequentially by date
df = df.sort_values(by='Date').reset_index(drop=True)

# Generate the CSV in your current directory
df.to_csv('pharma_raw_data.csv', index=False)
print("✅ Success! 'pharma_raw_data.csv' with 10,000 records has been generated in your folder.")