import pandas as pd
from statsmodels.tsa.stattools import adfuller

#LOAD DATA
file_path = '../data/Financial_Irregularities.xlsx'
data = pd.read_excel(file_path)

#CLEAN VARIABLES
columns_to_keep = [
    'Team Name',
    'Season',
    'Financial Irregularities(1=yes,0=no)',
    'League Standing',
    'Net Profit Margin(Net profit/operating revenue)',
    'Firm Size(Natural log of total assets)',
    'Leverage(Total Liabilities/Total assets)',
    'Growth',
    'Return on Equity(Net profit/Total Equity)',
    'Goal Ratio(Goals scored/Goals conceded)'
]

df = data[columns_to_keep].copy()

#rename for readability
df.rename(columns={
    'Financial Irregularities(1=yes,0=no)': 'Financial Irregularity',
    'Net Profit Margin(Net profit/operating revenue)': 'Net Profit Margin',
    'Firm Size(Natural log of total assets)': 'Firm Size',
    'Leverage(Total Liabilities/Total assets)': 'Leverage',
    'Return on Equity(Net profit/Total Equity)': 'Return on Equity',
    'Goal Ratio(Goals scored/Goals conceded)': 'Goal Ratio'
}, inplace=True)

#convert season to time ordering
df['Season'] = df['Season'].map(lambda x: int(x.split('/')[1]))
df = df.sort_values(['Team Name', 'Season'])

#VARIABLES TO TEST
variables = [
    'League Standing',
    'Net Profit Margin',
    'Firm Size',
    'Leverage',
    'Growth',
    'Return on Equity',
    'Goal Ratio'
]

results = []

print("Performing ADF Test for Stationarity\n")

#ADF TEST BY TEAM
for team in df['Team Name'].unique():
    team_data = df[df['Team Name'] == team]

    for var in variables:
        series = team_data[var].dropna()

        # Need minimum observations
        if len(series) < 5:
            continue

        # constant series can't be tested
        if series.nunique() <= 1:
            continue

        try:
            adf_stat, p_value, _, _, _, _ = adfuller(series)

            results.append({
                'Team': team,
                'Variable': var,
                'ADF Statistic': adf_stat,
                'p-value': p_value
            })

            print(f"{team} - {var}: ADF = {adf_stat:.3f}, p-value = {p_value:.4f}")

        except:
            continue

#SAVE RESULTS
results_df = pd.DataFrame(results)
results_df.to_csv('../results/adf_stationarity_results.csv', index=False)

print("\nADF stationarity results saved to results folder.")
