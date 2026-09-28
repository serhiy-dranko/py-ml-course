import pandas as pd

X_dev = pd.read_parquet("X_dev.parquet")
y_dev = pd.read_parquet("y_dev.parquet").iloc[:, 0]

inventory = pd.DataFrame({
    "dtype": X_dev.dtypes,
    "pct_missing": (X_dev.isna().mean() * 100).round(2),
    "n_unique": X_dev.nunique(),
})
inventory["needs_treatment"] = inventory.apply(
    lambda r: "high missing" if r["pct_missing"] > 40 else
              ("constant" if r["n_unique"] <= 1 else
               ("high cardinality" if r["dtype"] == "object" and r["n_unique"] > 20 else "")),
    axis=1
)
print(inventory.sort_values("pct_missing", ascending=False).head(20))

# Re-verify DAYS_EMPLOYED sentinel
print("\nDAYS_EMPLOYED value_counts (top 3):")
print(X_dev["DAYS_EMPLOYED"].value_counts().head(3))

# Check similar anomalies in other numeric columns (large positive value where mostly negative)
print("\nScanning numeric columns for sentinel-like anomalies (mixed sign with dominant outlier):")
for col in X_dev.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns:
    if X_dev[col].min() < 0 and X_dev[col].max() > 0:
        top_val = X_dev[col].value_counts().index[0]
        top_count = X_dev[col].value_counts().iloc[0]
        if top_count > len(X_dev) * 0.05 and top_val == X_dev[col].max():
            print(f"{col}: dominant max value {top_val} appears {top_count} times ({top_count/len(X_dev)*100:.1f}%)")

# Constant / near-constant and high-cardinality categoricals
print("\nConstant or near-constant columns:")
print(inventory[inventory["needs_treatment"] == "constant"].index.tolist())

print("\nHigh-cardinality categorical columns:")
print(inventory[inventory["needs_treatment"] == "high cardinality"][["n_unique"]])

hypotheses = """
FEATURE HYPOTHESES (before coding):
1. Affordability ratios (credit/income, annuity/income) should help because raw
   AMT_CREDIT alone doesn't distinguish a wealthy applicant taking a large loan
   from a low-income applicant overextending themselves — the ratio captures
   relative burden, which is closer to what a credit analyst actually reasons about.
2. Fixing the DAYS_EMPLOYED sentinel (365243 -> NaN + indicator flag) should help
   because currently it's treated as a real number, implying "employed for 1000
   years," which would corrupt any linear relationship the model tries to learn
   between employment length and risk.
3. EXT_SOURCE_* aggregates (mean/min) should help because these are themselves
   external risk scores; combining them may be more robust than any single one,
   especially since each has missing values individually.
4. Age in years (from DAYS_BIRTH) should help interpretability and possibly
   capture non-linear age effects once binned, even though the raw negative-days
   version is already numeric and usable as-is.
"""
print(hypotheses)

with open("decision_log.md", "a") as f:
    f.write("\n## Day 3, Block 1 — Feature Inventory\n\n")
    f.write(hypotheses)