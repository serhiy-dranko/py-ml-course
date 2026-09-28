import pandas as pd
import numpy as np

df = pd.read_csv("application_train.csv")

# Point 1: memory usage before/after downcasting
mem_before = df.memory_usage(deep=True).sum() / 1024**2
print(f"Memory before downcasting: {mem_before:.2f} MB")

for col in df.select_dtypes(include=["int64"]).columns:
    df[col] = pd.to_numeric(df[col], downcast="integer")
for col in df.select_dtypes(include=["float64"]).columns:
    df[col] = pd.to_numeric(df[col], downcast="float")

mem_after = df.memory_usage(deep=True).sum() / 1024**2
print(f"Memory after downcasting: {mem_after:.2f} MB")
print(f"Reduction: {(1 - mem_after/mem_before)*100:.1f}%")

# Point 2: missing values, worst 15
missing_pct = (df.isna().mean() * 100).sort_values(ascending=False)
print("\n15 worst columns by missing %:")
print(missing_pct.head(15))

# Point 3: duplicates
print("\nFully duplicate rows:", df.duplicated().sum())
print("Duplicate SK_ID_CURR:", df.duplicated(subset=["SK_ID_CURR"]).sum())

# Point 4: DAYS_EMPLOYED anomaly check
print("\nDAYS_EMPLOYED value_counts (top 5):")
print(df["DAYS_EMPLOYED"].value_counts().head())
anomaly_count = (df["DAYS_EMPLOYED"] > 0).sum()
print(f"\nRows with positive DAYS_EMPLOYED (likely placeholder/anomaly): {anomaly_count}")

# Check similar anomalies in other DAYS_ columns
days_cols = [c for c in df.columns if c.startswith("DAYS_")]
print("\nOther DAYS_ columns — checking for positive values (should all be <= 0):")
for col in days_cols:
    positive_count = (df[col] > 0).sum()
    if positive_count > 0:
        print(f"{col}: {positive_count} positive values")

# Point 5: constant / near-constant and high-cardinality columns
print("\nConstant or near-constant columns (< 2 unique values):")
for col in df.columns:
    if df[col].nunique() <= 1:
        print(col)

print("\nHigh-cardinality categorical columns (> 50 unique values):")
for col in df.select_dtypes(include="object").columns:
    if df[col].nunique() > 50:
        print(f"{col}: {df[col].nunique()} unique values")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 1, Block 2 — Quality Audit\n\n")
    f.write(f"- Memory: {mem_before:.2f} MB -> {mem_after:.2f} MB after downcasting\n")
    f.write(f"- Duplicate rows: {df.duplicated().sum()}, duplicate SK_ID_CURR: {df.duplicated(subset=['SK_ID_CURR']).sum()}\n")
    f.write(f"- DAYS_EMPLOYED anomaly: {anomaly_count} rows with positive values (likely a 365243 placeholder) — planned treatment: convert to NaN inside the pipeline, not permanently now.\n")