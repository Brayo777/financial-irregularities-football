import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


# LOAD DATA
file_path = '../data/Financial_Irregularities.xlsx'
data = pd.read_excel(file_path)


# SELECT VARIABLES
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

# Cleaning names
df.rename(columns={
    'Financial Irregularities(1=yes,0=no)': 'Financial Irregularity',
    'Net Profit Margin(Net profit/operating revenue)': 'Net Profit Margin',
    'Firm Size(Natural log of total assets)': 'Firm Size',
    'Leverage(Total Liabilities/Total assets)': 'Leverage',
    'Return on Equity(Net profit/Total Equity)': 'Return on Equity',
    'Goal Ratio(Goals scored/Goals conceded)': 'Goal Ratio'
}, inplace=True)


# CORRELATION MATRIX ----------------
corr_matrix = df.corr()


# P-VALUE MATRIX
p_values = pd.DataFrame(
    np.ones((len(df.columns), len(df.columns))),
    columns=df.columns,
    index=df.columns
)

for i in range(len(df.columns)):
    for j in range(len(df.columns)):
        if i != j:
            _, p = pearsonr(df.iloc[:, i], df.iloc[:, j])
            p_values.iloc[i, j] = p
        else:
            p_values.iloc[i, j] = np.nan

# SIGNIFICANCE STARS
stars_matrix = p_values.copy()

for i in range(len(p_values.columns)):
    for j in range(len(p_values.columns)):
        p = p_values.iloc[i, j]

        if pd.isna(p):
            stars_matrix.iloc[i, j] = ""
        elif p < 0.01:
            stars_matrix.iloc[i, j] = "***"
        elif p < 0.05:
            stars_matrix.iloc[i, j] = "**"
        elif p < 0.10:
            stars_matrix.iloc[i, j] = "*"
        else:
            stars_matrix.iloc[i, j] = ""

# TABLE WITH STARS
corr_with_stars = corr_matrix.copy()

for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        if i != j:
            corr_with_stars.iloc[i, j] = f"{corr_matrix.iloc[i, j]:.3f}{stars_matrix.iloc[i, j]}"
        else:
            corr_with_stars.iloc[i, j] = f"{corr_matrix.iloc[i, j]:.3f}"

print("\nCorrelation Matrix with Significance Levels:\n")
print(corr_with_stars)

corr_with_stars.to_csv('../results/correlation_matrix.csv')

# HEATMAP
plt.figure(figsize=(11, 9))

sns.heatmap(
    corr_matrix.astype(float),
    cmap="coolwarm",
    center=0,
    square=True,
    linewidths=0.5,
    cbar_kws={"label": "Correlation coefficient"},
    annot=False
)

plt.title("Correlation Heatmap")
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('../results/correlation_heatmap.png', dpi=400)
plt.show()
plt.close()

print("Correlation outputs saved to /results/")
