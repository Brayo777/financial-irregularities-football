# -------------------------------------------
# MULTICOLLINEARITY CHECK (VIF)
# -------------------------------------------

import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.api import add_constant

# -----------------------
# LOAD DATA
# -----------------------
file_path = '../data/Financial_Irregularities.xlsx'
data = pd.read_excel(file_path)

# -----------------------
# SELECT VARIABLES
# -----------------------
columns_to_keep = [
    'Financial Irregularities(1=yes,0=no)',
    'League Standing',
    'Net Profit Margin(Net profit/operating revenue)',
    'Firm Size(Natural log of total assets)',
    'Leverage(Total Liabilities/Total assets)',
    'Growth',
    'Return on Equity(Net profit/Total Equity)',
    'Goal Ratio(Goals scored/Goals conceded)'
]

data = data[columns_to_keep].copy()

# Rename for clarity
data.rename(columns={
    'Financial Irregularities(1=yes,0=no)': 'Financial Irregularity',
    'Net Profit Margin(Net profit/operating revenue)': 'Net Profit Margin',
    'Firm Size(Natural log of total assets)': 'Firm Size',
    'Leverage(Total Liabilities/Total assets)': 'Leverage',
    'Return on Equity(Net profit/Total Equity)': 'Return on Equity',
    'Goal Ratio(Goals scored/Goals conceded)': 'Goal Ratio'
}, inplace=True)

# -----------------------
# INDEPENDENT VARIABLES ONLY
# -----------------------
X = data.drop(columns=['League Standing'])

# Add constant
X = add_constant(X)

# -----------------------
# COMPUTE VIF
# -----------------------
vif = pd.DataFrame()
vif["Variable"] = X.columns
vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

# Display in Python
print("\nVariance Inflation Factor (VIF):\n")
print(vif)

# Save to results folder
vif.to_csv('../results/vif_table.csv', index=False)

print("\nVIF table saved to results folder.")
