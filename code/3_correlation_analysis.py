#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 20:07:36 2026

@author: briangichuhi
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

# Load dataset
file_path = '../data/Financial_Irregularities.xlsx'
data = pd.read_excel(file_path)

# Select variables
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

# Rename for clean table output
df.rename(columns={
    'Financial Irregularities(1=yes,0=no)': 'Financial Irregularity',
    'Net Profit Margin(Net profit/operating revenue)': 'Net Profit Margin',
    'Firm Size(Natural log of total assets)': 'Firm Size',
    'Leverage(Total Liabilities/Total assets)': 'Leverage',
    'Return on Equity(Net profit/Total Equity)': 'Return on Equity',
    'Goal Ratio(Goals scored/Goals conceded)': 'Goal Ratio'
}, inplace=True)

# Compute correlation matrix
corr_matrix = df.corr()

# Create matrix for p-values
p_values = pd.DataFrame(np.ones((len(df.columns), len(df.columns))),
                        columns=df.columns,
                        index=df.columns)

# Calculate p-values
for row in df.columns:
    for col in df.columns:
        if row != col:
            corr, p_val = pearsonr(df[row].dropna(), df[col].dropna())
            p_values.loc[row, col] = p_val

# Function to assign significance stars
def stars(p):
    if p < 0.01:
        return '***'
    elif p < 0.05:
        return '**'
    elif p < 0.10:
        return '*'
    else:
        return ''

# Combine correlations + stars
corr_with_stars = corr_matrix.copy()

for row in corr_matrix.columns:
    for col in corr_matrix.columns:
        if row != col:
            corr_with_stars.loc[row, col] = f"{corr_matrix.loc[row, col]:.3f}{stars(p_values.loc[row, col])}"
        else:
            corr_with_stars.loc[row, col] = f"{corr_matrix.loc[row, col]:.3f}"

print("\nCorrelation Matrix with Significance Levels:\n")
print(corr_with_stars)

# Save table
corr_with_stars.to_csv('../results/correlation_matrix.csv')

# --------- HEATMAP FIGURE ---------

plt.figure(figsize=(10, 8))

# heatmap using actual correlation coefficients
sns.heatmap(
    corr_matrix.astype(float),
    cmap='coolwarm',
    center=0,
    annot=True,
    fmt=".2f",
    linewidths=0.5
)

plt.title('Correlation Matrix Heatmap')
plt.tight_layout()

# save figure
plt.savefig('../results/correlation_heatmap.png', dpi=300)

# Show inside Python (interactive view)
plt.show()

plt.close()

print("Correlation heatmap saved to results folder.")

print("\nCorrelation matrix saved to results folder.")
