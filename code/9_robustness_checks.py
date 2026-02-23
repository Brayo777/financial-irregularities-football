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

BASELINE FE MODEL
                          PanelOLS Estimation Summary                           
================================================================================
Dep. Variable:        League Standing   R-squared:                        0.3552
Estimator:                   PanelOLS   R-squared (Between):              0.6971
No. Observations:                 406   R-squared (Within):               0.3552
Date:                Mon, Feb 23 2026   R-squared (Overall):              0.6506
Time:                        20:21:53   Log-likelihood                   -893.81
Cov. Estimator:                Robust                                           
                                        F-statistic:                      22.896
Entities:                         108   P-value                           0.0000
Avg Obs:                       3.7593   Distribution:                   F(7,291)
Min Obs:                       1.0000                                           
Max Obs:                       5.0000   F-statistic (robust):             11.364
                                        P-value                           0.0000
Time periods:                       5   Distribution:                   F(7,291)
Avg Obs:                       81.200                                           
Min Obs:                       77.000                                           
Max Obs:                       89.000                                           
                                                                                
                                   Parameter Estimates                                    
==========================================================================================
                        Parameter  Std. Err.     T-stat    P-value    Lower CI    Upper CI
------------------------------------------------------------------------------------------
const                      18.100     4.7044     3.8474     0.0001      8.8407      27.358
Financial Irregularity    -0.3098     0.5219    -0.5935     0.5533     -1.3369      0.7174
Net Profit Margin         -0.2112     0.4674    -0.4518     0.6517     -1.1310      0.7087
Firm Size                 -0.1672     0.3867    -0.4324     0.6658     -0.9282      0.5938
Leverage                  -0.2057     0.6138    -0.3351     0.7378     -1.4136      1.0023
Growth                     0.2444     0.5456     0.4479     0.6546     -0.8294      1.3182
Return on Equity          -0.0049     0.0553    -0.0880     0.9299     -0.1138      0.1040
Goal Ratio                -5.2406     0.6293    -8.3271     0.0000     -6.4793     -4.0020
==========================================================================================

F-test for Poolability: 2.6862
P-value: 0.0000
Distribution: F(107,291)

Included effects: Entity

CLUSTERED SE MODEL
                          PanelOLS Estimation Summary                           
================================================================================
Dep. Variable:        League Standing   R-squared:                        0.3552
Estimator:                   PanelOLS   R-squared (Between):              0.6971
No. Observations:                 406   R-squared (Within):               0.3552
Date:                Mon, Feb 23 2026   R-squared (Overall):              0.6506
Time:                        20:21:53   Log-likelihood                   -893.81
Cov. Estimator:             Clustered                                           
                                        F-statistic:                      22.896
Entities:                         108   P-value                           0.0000
Avg Obs:                       3.7593   Distribution:                   F(7,291)
Min Obs:                       1.0000                                           
Max Obs:                       5.0000   F-statistic (robust):             7.7579
                                        P-value                           0.0000
Time periods:                       5   Distribution:                   F(7,291)
Avg Obs:                       81.200                                           
Min Obs:                       77.000                                           
Max Obs:                       89.000                                           
                                                                                
                                   Parameter Estimates                                    
==========================================================================================
                        Parameter  Std. Err.     T-stat    P-value    Lower CI    Upper CI
------------------------------------------------------------------------------------------
const                      18.100     4.3198     4.1899     0.0000      9.5975      26.602
Financial Irregularity    -0.3098     0.5159    -0.6004     0.5487     -1.3252      0.7056
Net Profit Margin         -0.2112     0.4162    -0.5074     0.6123     -1.0303      0.6080
Firm Size                 -0.1672     0.3668    -0.4558     0.6489     -0.8891      0.5548
Leverage                  -0.2057     0.6089    -0.3377     0.7358     -1.4041      0.9928
Growth                     0.2444     0.5462     0.4474     0.6549     -0.8305      1.3193
Return on Equity          -0.0049     0.0483    -0.1008     0.9198     -0.1000      0.0902
Goal Ratio                -5.2406     0.8200    -6.3909     0.0000     -6.8546     -3.6267
==========================================================================================

F-test for Poolability: 2.6862
P-value: 0.0000
Distribution: F(107,291)

Included effects: Entity
