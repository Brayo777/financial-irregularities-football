import pandas as pd

# Load cleaned dataset
file_path = '../data/Financial_Irregularities.xlsx'
data = pd.read_excel(file_path)

# Select relevant variables
columns = [
    'Financial Irregularities(1=yes,0=no)',
    'League Standing',
    'Net Profit Margin(Net profit/operating revenue)',
    'Firm Size(Natural log of total assets)',
    'Leverage(Total Liabilities/Total assets)',
    'Growth',
    'Return on Equity(Net profit/Total Equity)',
    'Goal Ratio(Goals scored/Goals conceded)'
]

df = data[columns].copy()

# Rename variables for cleaner output
df.rename(columns={
    'Financial Irregularities(1=yes,0=no)': 'Financial Irregularity',
    'Net Profit Margin(Net profit/operating revenue)': 'Net Profit Margin',
    'Firm Size(Natural log of total assets)': 'Firm Size',
    'Leverage(Total Liabilities/Total assets)': 'Leverage',
    'Return on Equity(Net profit/Total Equity)': 'Return on Equity',
    'Goal Ratio(Goals scored/Goals conceded)': 'Goal Ratio'
}, inplace=True)

# Generate descriptive statistics
desc_stats = df.describe().T

# Add additional statistics
desc_stats['median'] = df.median()
desc_stats['skewness'] = df.skew()
desc_stats['kurtosis'] = df.kurtosis()

# Reorder columns
desc_stats = desc_stats[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'skewness', 'kurtosis']]

print("\nDescriptive Statistics:\n")
print(desc_stats)

# Optional: Save results for dissertation tables
desc_stats.to_csv('../results/descriptive_statistics.csv')

print("\nDescriptive statistics saved to results folder.")
