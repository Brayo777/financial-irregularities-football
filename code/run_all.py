import subprocess

scripts = [
    "1_data_preparation.py",
    "2_descriptive_statistics.py",
    "3_correlation_analysis.py",
    "4_stationarity_tests.py",
    "5_panel_models_FE_RE.py",
    "6_hausman_test.py",
    "7_model_diagnostics.py",
    "8_multicollinearity_vif.py",
    "9_robustness_checks.py"
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run(["python", script])
