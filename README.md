# Financial Irregularities and Football Performance

Reproducible Python econometrics project analysing whether financial irregularities influence the competitive performance of European football clubs using panel data methods.

---

## Research Objective

This project investigates whether football clubs involved in financial irregularities experience differences in league performance compared to compliant clubs. **League Standing** is used as a proxy for sporting success.

---

## Data

The dataset is an **unbalanced panel of European football clubs across multiple leagues and seasons**, where each observation represents a club–season.

### Key Variables

**Dependent Variable**

- League Standing

**Explanatory Variables**

- Financial Irregularity indicator (1 = irregularity, 0 = none)
- Net Profit Margin
- Firm Size
- Leverage
- Growth
- Return on Equity
- Goal Ratio

---

## Methodology

The analysis applies standard **panel econometric techniques** to evaluate the relationship between financial irregularities and sporting performance.

The empirical strategy includes:

- Correlation analysis  
- Stationarity (unit root) testing  
- Fixed Effects panel regression  
- Random Effects panel regression  
- Hausman specification test  
- Model diagnostics and robustness checks  

---

### Stationarity Testing

An Augmented Dickey–Fuller (ADF) unit root test was conducted for each club in the panel dataset to evaluate the time-series properties of the dependent variable.

Due to the short time dimension of football panel datasets (limited seasons per club), some entities produced “short series” or “constant” outcomes. This is expected in micro-panel sports datasets and does not invalidate panel estimation.

Overall, the results indicate the dataset is sufficiently stationary for panel regression modelling.

---

### Model Selection: Fixed vs Random Effects

A Hausman specification test was conducted to determine the appropriate panel estimator.

The test produced a statistically significant result (**p = 0.026**), leading to rejection of the null hypothesis that the random-effects estimator is consistent.

This indicates that unobserved club-specific characteristics are correlated with the explanatory variables. Therefore, the **Fixed Effects model** is used as the primary specification.

---

### Model Diagnostics

Several diagnostic tests were performed to validate the regression results, including:

- Breusch–Pagan test for heteroskedasticity  
- Durbin–Watson test for serial correlation  
- Shapiro–Wilk test for residual normality  
- Variance Inflation Factor (VIF) for multicollinearity  

The results indicate that the regression assumptions are broadly satisfied and that the model estimates are robust.

---

### Main Findings

The fixed-effects panel estimation indicates that **financial irregularities do not have a statistically significant impact on league standing** once unobserved club-specific characteristics are controlled for.

While cross-club differences may exist, within-club variation over time does not support a causal relationship between financial irregularities and short-term competitive performance.

Sporting performance indicators—particularly **goal ratio**—remain the strongest and most consistent determinants of league position.

Robustness checks confirm that these results are stable and not sensitive to alternative covariance specifications.

---

## Technologies Used

- Python  
- pandas  
- numpy  
- statsmodels  
- linearmodels  
- matplotlib  
- seaborn  

---

## Repository Structure

```
data/
Dataset used in the analysis.

code/
Python scripts implementing the full econometric pipeline, including data preparation, descriptive statistics, regression modelling, and diagnostics.

results/
Automatically generated outputs including regression tables and diagnostic figures.
```

---

## Requirements

Install required Python packages:

```
pip install -r requirements.txt
```

---

## Reproducing the Results

Clone the repository:

```
git clone https://github.com/Brayo777/financial-irregularities-football.git
```

Navigate into the project folder:

```
cd financial-irregularities-football
```

Run the full analysis pipeline:

```
python code/run_all.py
```

All tables and figures will be generated in the **results/** folder.

