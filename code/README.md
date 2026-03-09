# Code

This folder contains all Python scripts used in the empirical analysis for the dissertation.

The scripts implement the full econometric pipeline including:

- Data preparation
- Descriptive statistics
- Correlation analysis
- Stationarity (ADF) tests
- Fixed Effects and Random Effects panel regression models
- Hausman specification test
- Diagnostic testing
- Robustness checks

---

## Reproducing the Results

Clone the repository:

```
git clone https://github.com/Brayo777/financial-irregularities-football.git
```

Install the required Python packages:

```
pip install -r requirements.txt
```

Run the full analysis pipeline:

```
python code/run_all.py
```

All tables and figures will be automatically generated in the `results/` folder in the local project directory.
