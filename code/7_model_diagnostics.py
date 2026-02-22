# MODEL DIAGNOSTICS FOR FIXED EFFECTS PANEL MODEL
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from statsmodels.api import add_constant
from statsmodels.stats.diagnostic import het_breuschpagan
from scipy.stats import shapiro

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

# panel index
data['Season'] = data['Season'].map(lambda x: pd.to_datetime('20' + x.split('/')[1] + '-05-31'))
data.set_index(['Team Name','Season'], inplace=True)

# MODEL
y = data['League Standing']
X = data[['Financial Irregularity','Net Profit Margin','Firm Size','Leverage','Growth','Return on Equity','Goal Ratio']]
X = add_constant(X)

model = PanelOLS(y, X, entity_effects=True)
results = model.fit()

# RESIDUAL PLOT
fitted = results.predict().fitted_values
residuals = y - fitted

plt.figure(figsize=(8,6))
plt.scatter(fitted, residuals, alpha=0.6)
plt.axhline(0)
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.title("Residuals vs Fitted Values (Fixed Effects)")
plt.tight_layout()
plt.savefig('../results/residual_plot.png', dpi=300)
plt.close()

print("Residual plot saved.")

# BREUSCH-PAGAN (Heteroskedasticity)
bp_test = het_breuschpagan(residuals, X)
bp_pvalue = bp_test[1]

print("Breusch-Pagan p-value:", bp_pvalue)

# SHAPIRO-WILK (Normality)
sample_resid = residuals.sample(min(len(residuals), 5000))
shapiro_stat, shapiro_p = shapiro(sample_resid)

print("Shapiro-Wilk p-value:", shapiro_p)

# DURBIN-WATSON (Autocorrelation)
dw = sm.stats.stattools.durbin_watson(residuals)
print("Durbin-Watson:", dw)

# SAVE RESULTS
with open('../results/model_diagnostics.txt', 'w') as f:
    f.write("MODEL DIAGNOSTICS\n\n")
    f.write(f"Breusch-Pagan p-value: {bp_pvalue}\n")
    f.write(f"Shapiro-Wilk p-value: {shapiro_p}\n")
    f.write(f"Durbin-Watson: {dw}\n")

print("Diagnostics saved to results folder.")
