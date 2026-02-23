# ROBUSTNESS CHECKS - CLUSTERED STANDARD ERRORS

import pandas as pd
from linearmodels.panel import PanelOLS
from statsmodels.api import add_constant

# -----------------------
# LOAD DATA
# -----------------------
data = pd.read_excel('../data/Financial Irregularities.xlsx')

# -----------------------
# CLEAN VARIABLES
# -----------------------
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

# panel index
data['Season'] = data['Season'].map(lambda x: pd.to_datetime('20' + x.split('/')[1] + '-05-31'))
data.set_index(['Team Name','Season'], inplace=True)

# -----------------------
# MODEL
# -----------------------
y = data['League Standing']
X = data[['Financial Irregularity','Net Profit Margin','Firm Size','Leverage','Growth','Return on Equity','Goal Ratio']]
X = add_constant(X)

# BASELINE FE
fe_model = PanelOLS(y, X, entity_effects=True)
baseline = fe_model.fit(cov_type='robust')

# CLUSTERED BY CLUB
clustered = fe_model.fit(cov_type='clustered', cluster_entity=True)

print("\nBASELINE FE RESULTS")
print(baseline.summary)

print("\nCLUSTERED STANDARD ERRORS RESULTS")
print(clustered.summary)

# SAVE
with open('../results/robustness_results.txt', 'w') as f:
    f.write("BASELINE FE MODEL\n")
    f.write(str(baseline.summary))
    f.write("\n\nCLUSTERED SE MODEL\n")
    f.write(str(clustered.summary))

print("Robustness results saved to results folder.")
