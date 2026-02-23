# Financial Irregularities and Football Performance
Panel data econometric analysis examining whether financial irregularities influence the competitive performance of European football clubs.

## Research Objective
This project investigates whether clubs involved in financial irregularities experience differences in league performance compared to compliant clubs. League Standing is used as a proxy for sporting success.

## Data
The dataset is an unbalanced panel of European football clubs across multiple leagues and seasons. Each observation represents a club-season.

**Key variables include:**
* League Standing (dependent variable)
* Financial Irregularity indicator (1 = irregularity, 0 = none)
* Net Profit Margin
* Firm Size
* Leverage
* Growth
* Return on Equity
* Goal Ratio

## Methodology
**The study applies panel econometric techniques:**
* Correlation analysis
* Stationarity (unit root) testing
* Fixed Effects and Random Effects models
* Hausman specification test
* Model diagnostics and robustness checks

### Stationarity Check (Unit Root Testing)
An Augmented Dickey–Fuller (ADF) unit root test was conducted for each club in the panel dataset to verify the time-series properties of the dependent variable.
Due to the short time dimension of football panel data (limited number of seasons per club), several entities produced “short series” or “constant” outcomes. This is expected in micro-panel sports datasets and does not invalidate panel estimation.
Overall, the results indicate that the dataset is sufficiently stationary for fixed-effects panel estimation and does not suffer from spurious regression. Therefore, proceeding with panel regression modelling is econometrically appropriate.

### Model Selection: Fixed vs Random Effects
A Hausman specification test was conducted to determine whether a fixed-effects or random-effects panel estimator is appropriate. The null hypothesis states that the random-effects estimator is consistent and efficient.
The test produced a statistically significant result (p = 0.026), leading to rejection of the null hypothesis. This indicates that unobserved club-specific characteristics are correlated with the explanatory variables. Consequently, the random-effects estimator is inconsistent.
Therefore, the fixed-effects panel model is the appropriate econometric specification and is used as the primary model in the analysis.

### Model Diagnostics
Diagnostic tests were performed on the fixed-effects regression residuals. The Breusch–Pagan test did not detect significant heteroskedasticity, and the Durbin–Watson statistic indicated no serial correlation. The Shapiro–Wilk test rejected normality of residuals; however, this is common in micro-panel data and does not invalidate fixed-effects estimation, which relies on large-sample consistency rather than normally distributed errors.
Overall, the diagnostic results support the validity of the fixed-effects model with robust standard errors.

### Multicollinearity (Variance Inflation Factor)
A Variance Inflation Factor (VIF) test was conducted to assess multicollinearity among the explanatory variables. All VIF values were below 2, indicating negligible multicollinearity and confirming that the regression coefficients are stable and reliably estimated.

## Repository Structure
* `data/` raw dataset
* `code/` all Python analysis scripts
* `results/` generated tables and figures

## Requirements
The project uses Python with pandas, numpy, statsmodels, linearmodels, seaborn, and matplotlib.

