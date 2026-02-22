import pandas as pd
from linearmodels.panel import PanelOLS, RandomEffects
from statsmodels.api import add_constant

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

#VARIABLES
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

# FIXED EFFECTS MODEL
fe_model = PanelOLS(y, X, entity_effects=True)
fe_results = fe_model.fit(cov_type='robust')

print("\n===== FIXED EFFECTS RESULTS =====")
print(fe_results.summary)

# RANDOM EFFECTS MODEL
re_model = RandomEffects(y, X)
re_results = re_model.fit(cov_type='robust')

print("\n===== RANDOM EFFECTS RESULTS =====")
print(re_results.summary)

# SAVE RESULTS TO FILES

# Fixed Effects table
with open('../results/fixed_effects_results.txt', 'w') as f:
    f.write(str(fe_results.summary))

# Random Effects table
with open('../results/random_effects_results.txt', 'w') as f:
    f.write(str(re_results.summary))

print("\nRegression tables saved to results folder.")
