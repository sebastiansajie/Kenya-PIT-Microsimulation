import numpy as np
import pandas as pd

# ============================================================
# SETTINGS
# ============================================================
INPUT_FILE = "taxcalc/pit_kenya.csv"          # change path if needed
OUTPUT_FILE = "taxcalc/synthetic_bootstrap_pit_kenya.csv"
WEIGHTS_FILE = "taxcalc/synthetic_bootstrap_pit_weights_kenya.csv"
N_SYNTH = 100_000
RANDOM_SEED = 27

TARGET_COLS = [
    "emp_income",
    "interest_income",
    "business_income",
    "mortage_interest",
    "home_own_saving_plan_dep",
    "pension_contribution",
    "hosp_tot_deposit_year",
    "is_disabled",
    "insurance_relief"
]

WEIGHT_COL = "weight"

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv(INPUT_FILE)

required_cols = TARGET_COLS + [WEIGHT_COL]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

df = df[required_cols].copy()

# Make sure columns are numeric
for c in TARGET_COLS + [WEIGHT_COL]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# Drop rows with missing or nonpositive weights
df = df[df[WEIGHT_COL].notna() & (df[WEIGHT_COL] > 0)].copy()

# Fill missing target values conservatively
for c in TARGET_COLS:
    if c == "is_disabled":
        df[c] = df[c].fillna(0)
        df[c] = (df[c] > 0).astype(int)
    else:
        df[c] = df[c].fillna(0)

# ============================================================
# WEIGHTED BOOTSTRAP
# ============================================================
rng = np.random.default_rng(RANDOM_SEED)

weights = df[WEIGHT_COL].to_numpy(dtype=float)
prob = weights / weights.sum()

sample_idx = rng.choice(
    df.index.to_numpy(),
    size=N_SYNTH,
    replace=True,
    p=prob
)

synthetic = df.loc[sample_idx, TARGET_COLS].reset_index(drop=True)

# Assign equal weights to synthetic rows
synthetic["weight"] = 1.0

# ============================================================
# OPTIONAL: SMALL JITTER FOR CONTINUOUS VARIABLES
# ============================================================
# This makes the synthetic data less like exact copies of original rows.
# Set APPLY_JITTER = False if you want pure bootstrap only.
APPLY_JITTER = True

continuous_cols = [
    "emp_income",
    "interest_income",
    "business_income",
    "mortage_interest",
    "home_own_saving_plan_dep",
    "pension_contribution",
    "hosp_tot_deposit_year",
    "insurance_relief"
]

if APPLY_JITTER:
    for c in continuous_cols:
        x = synthetic[c].to_numpy(dtype=float)

        # Add tiny noise only to positive values
        positive = x > 0
        if positive.any():
            # Use 1% of std as jitter scale
            std_c = df[c].std()
            jitter_scale = 0.01 * std_c if pd.notna(std_c) and std_c > 0 else 0.0

            if jitter_scale > 0:
                noise = rng.normal(loc=0.0, scale=jitter_scale, size=positive.sum())
                x[positive] = np.maximum(0, x[positive] + noise)

        synthetic[c] = x

# Ensure binary stays binary
synthetic["is_disabled"] = synthetic["is_disabled"].astype(int)
synthetic["is_disabled"] = (synthetic["is_disabled"] > 0).astype(int)

# ============================================================
# SAVE DATA FILE AND WEIGHTS FILE
# ============================================================
synthetic['id_n']=synthetic.index
synthetic['Year']=2023
synthetic.to_csv(OUTPUT_FILE, index=False)

df_weight = synthetic[['weight']].copy()

df_weight.columns = ['WT2023']
df_weight['WT2024'] = df_weight['WT2023']
df_weight['WT2025'] = df_weight['WT2023']
df_weight['WT2026'] = df_weight['WT2023']
df_weight['WT2027'] = df_weight['WT2023']
df_weight['WT2028'] = df_weight['WT2023']
df_weight['WT2029'] = df_weight['WT2023']
df_weight['WT2030'] = df_weight['WT2023']
df_weight['WT2031'] = df_weight['WT2023']
df_weight['WT2032'] = df_weight['WT2023']

df_weight.to_csv(WEIGHTS_FILE, index=False)
# ============================================================
# QUICK VALIDATION
# ============================================================
def weighted_mean(x, w):
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    return np.sum(x * w) / np.sum(w)

print("Synthetic dataset created.")
print(f"Output file: {OUTPUT_FILE}")
print(f"Synthetic rows: {len(synthetic):,}")
print(f"Original rows used: {len(df):,}")
print(f"All synthetic weights equal? {synthetic['weight'].nunique() == 1}")

print("\nComparison: weighted original mean vs synthetic mean")
for c in TARGET_COLS:
    orig_mean = weighted_mean(df[c].to_numpy(dtype=float), weights)
    syn_mean = synthetic[c].mean()
    print(f"{c:28s} original={orig_mean:,.2f}   synthetic={syn_mean:,.2f}")
    print(f"{c:28s} difference (%)={(orig_mean-syn_mean)*100/orig_mean:,.2f}")

# ============================================================
# CALIBRATION
# ============================================================

# reweight using tax projections calibrated
tax_collection_2023_24_billion = 543.186
# synthetic data has only 100,000 observations
tax_collection_model_billion_2023 = 22.99
multiplicative_factor_2023 = tax_collection_2023_24_billion/tax_collection_model_billion_2023

# reweight using tax projections calibrated
tax_collection_2024_25_billion = 560.945
# synthetic data has only 100,000 observations
tax_collection_model_billion_2024 = 26.76
multiplicative_factor_2024 = tax_collection_2024_25_billion/tax_collection_model_billion_2024


pit_synthetic = pd.read_csv(OUTPUT_FILE)
pit_synthetic['weight'] = multiplicative_factor_2023*pit_synthetic['weight']
pit_synthetic.to_csv(OUTPUT_FILE, index=False)

df_weight = pd.read_csv(WEIGHTS_FILE)
                 
df_weight['WT2023'] = multiplicative_factor_2023*df_weight['WT2023']
df_weight['WT2024'] = multiplicative_factor_2024*df_weight['WT2024']
df_weight['WT2025'] = df_weight['WT2024']
df_weight['WT2026'] = df_weight['WT2024']
df_weight['WT2027'] = df_weight['WT2024']
df_weight['WT2028'] = df_weight['WT2024']
df_weight['WT2029'] = df_weight['WT2024']
df_weight['WT2030'] = df_weight['WT2024']
df_weight['WT2031'] = df_weight['WT2024']
df_weight['WT2032'] = df_weight['WT2024']
df_weight.to_csv(WEIGHTS_FILE, index=False)

##################################################
# COMPARE KDEs of Original and Synthetic dataset
##################################################
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# FILE PATHS
# ============================================================

REAL_FILE = INPUT_FILE
SYN_FILE = OUTPUT_FILE

COL = "emp_income"
WEIGHT_COL = "weight"

# ============================================================
# LOAD DATA
# ============================================================
real = pd.read_csv(REAL_FILE)
syn = pd.read_csv(SYN_FILE)

# Clean data
real[COL] = pd.to_numeric(real[COL], errors="coerce")
syn[COL] = pd.to_numeric(syn[COL], errors="coerce")

real = real[real[COL].notna()]
syn = syn[syn[COL].notna()]

# Remove extreme outliers for stable KDE (optional but recommended)
upper = np.percentile(real[COL], 99.5)
real = real[real[COL] <= upper]
syn = syn[syn[COL] <= upper]

# ============================================================
# HANDLE WEIGHTS
# ============================================================
if WEIGHT_COL in real.columns:
    weights = real[WEIGHT_COL].to_numpy(dtype=float)
    weights = weights / weights.sum()
else:
    weights = None

# Synthetic usually equal-weight then syn_weights = None
if WEIGHT_COL in syn.columns:
    syn_weights = syn[WEIGHT_COL].to_numpy(dtype=float)
    syn_weights = syn_weights / syn_weights.sum()
else:
    syn_weights = None
    

# ============================================================
# KDE ESTIMATION
# ============================================================
real_values = real[COL].to_numpy()
syn_values = syn[COL].to_numpy()

kde_real = gaussian_kde(real_values, weights=weights)
kde_syn = gaussian_kde(syn_values, weights=syn_weights)

# Evaluation grid
x_min = min(real_values.min(), syn_values.min())
x_max = max(real_values.max(), syn_values.max())

x_grid = np.linspace(x_min, x_max, 500)

y_real = kde_real(x_grid)
y_syn = kde_syn(x_grid)

# ============================================================
# PLOT
# ============================================================
plt.figure(figsize=(8, 5))

plt.plot(x_grid, y_real, label="Real (weighted KDE)", linewidth=2)
plt.plot(x_grid, y_syn, label="Synthetic KDE", linewidth=2, linestyle="--")

plt.title("KDE Comparison: emp_income")
plt.xlabel("emp_income")
plt.ylabel("Density")
plt.legend()
plt.grid(True)

plt.show()

# ============================================================
# LOG SCALE VERSION (better for income)
# ============================================================
real_log = np.log1p(real_values)
syn_log = np.log1p(syn_values)

kde_real_log = gaussian_kde(real_log, weights=weights)
kde_syn_log = gaussian_kde(syn_log)

x_grid_log = np.linspace(real_log.min(), real_log.max(), 500)

plt.figure(figsize=(8, 5))
plt.plot(x_grid_log, kde_real_log(x_grid_log), label="Real (log)")
plt.plot(x_grid_log, kde_syn_log(x_grid_log), label="Synthetic (log)", linestyle="--")

plt.title("KDE Comparison (log scale): emp_income")
plt.xlabel("log(1 + emp_income)")
plt.ylabel("Density")
plt.legend()
plt.grid(True)

plt.show()