import pandas as pd

# Load dataset
file_path = '../data/Financial_Irregularities.xlsx'
data = pd.read_excel(file_path)

# Extract country
data['Country'] = data['League'].apply(lambda x: x.split('(')[-1].rstrip(')'))

# Select necessary columns
columns_to_keep = [
    'Team Name', 'League', 'Season', 
    'Financial Irregularities(1=yes,0=no)', 
    'League Standing', 
    'Net Profit Margin(Net profit/operating revenue)', 
    'Firm Size(Natural log of total assets)', 
    'Leverage(Total Liabilities/Total assets)', 
    'Growth',
    'Return on Equity(Net profit/Total Equity)',
    'Goal Ratio(Goals scored/Goals conceded)'
]

data_cleaned = data[columns_to_keep].copy()

# Rename variables
data_cleaned.rename(columns={
    'Financial Irregularities(1=yes,0=no)': 'Financial Irregularity',
    'Net Profit Margin(Net profit/operating revenue)': 'Net Profit Margin',
    'Firm Size(Natural log of total assets)': 'Firm Size',
    'Leverage(Total Liabilities/Total assets)': 'Leverage',
    'Return on Equity(Net profit/Total Equity)': 'Return on Equity',
    'Goal Ratio(Goals scored/Goals conceded)': 'Goal Ratio'
}, inplace=True)

# Convert season
data_cleaned['Season'] = data_cleaned['Season'].map(
    lambda x: pd.to_datetime('20' + x.split('/')[1] + '-05-31')
)

# Set panel index
data_cleaned.set_index(['Team Name', 'Season'], inplace=True)

print("Data preparation complete.")
print(data_cleaned.head())
