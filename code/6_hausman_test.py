import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS, RandomEffects
from statsmodels.api import add_constant
from scipy.stats import chi2

# LOAD DATA
file_path = '../data/Financial_Irregularities.xlsx'
data = pd.read_excel(file_path)

# CLEAN VARIABLES
columns_to_keep = [
    'Team Name','Season',
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

data.rename(columns={
    'Financial Irregularities(1=yes,0=no)': 'Financial Irregularity',
    'Net Profit Margin(Net profit/operating revenue)': 'Net Profit Margin',
    'Firm Size(Natural log of total assets)': 'Firm Size',
    'Leverage(Total Liabilities/Total assets)': 'Leverage',
    'Return on Equity(Net profit/Total Equity)': 'Return on Equity',
    'Goal Ratio(Goals scored/Goals conceded)': 'Goal Ratio'
}, inplace=True)

# PANEL INDEX
data['Season'] = data['Season'].map(lambda x: pd.to_datetime('20' + x.split('/')[1] + '-05-31'))
data.set_index(['Team Name','Season'], inplace=True)

# DEFINE MODEL
y = data['League Standing']

X = data[[
    'Financial Irregularity',
    'Net Profit Margin',
    'Firm Size',
    'Leverage',
    'Growth',
    'Return on Equity',
    'Goal Ratio'
]]

X = add_constant(X)

# ESTIMATE MODELS
fe_model = PanelOLS(y, X, entity_effects=True)
fe_results = fe_model.fit()

re_model = RandomEffects(y, X)
re_results = re_model.fit()

# HAUSMAN CALCULATION
beta_diff = fe_results.params - re_results.params
cov_diff = fe_results.cov - re_results.cov

stat = np.dot(np.dot(beta_diff.T, np.linalg.inv(cov_diff)), beta_diff)
df = len(beta_diff)
p_value = 1 - chi2.cdf(stat, df)

print("\n===== HAUSMAN TEST =====")
print(f"Test statistic: {stat:.4f}")
print(f"Degrees of freedom: {df}")
print(f"P-value: {p_value:.6f}")

if p_value < 0.05:
    print("Result: Reject H0 → Fixed Effects preferred.")
else:
    print("Result: Fail to reject H0 → Random Effects preferred.")

# SAVE RESULT
with open('../results/hausman_test.txt', 'w') as f:
    f.write("Hausman Test Results\n")
    f.write(f"Statistic: {stat:.4f}\n")
    f.write(f"Degrees of freedom: {df}\n")
    f.write(f"P-value: {p_value:.6f}\n")

print("\nHausman test saved to results folder.")
