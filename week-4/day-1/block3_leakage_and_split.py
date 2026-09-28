import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("application_train.csv")

# Point 1: drop identifier
X = df.drop(columns=["SK_ID_CURR", "TARGET"])
y = df["TARGET"]

print("X shape:", X.shape)
print("y shape:", y.shape)

# Point 3: locked test set (80/20, stratified)
X_working, X_test, y_working, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

X_test.to_parquet("X_test.parquet")
y_test.to_frame().to_parquet("y_test.parquet")
print("\nLocked test set saved: X_test.parquet, y_test.parquet")
print("Test set shape:", X_test.shape)

# Point 4: development subsample (~50k rows, stratified) from the working set
dev_fraction = 50000 / len(X_working)
X_dev, _, y_dev, _ = train_test_split(
    X_working, y_working, train_size=dev_fraction, random_state=42, stratify=y_working
)

X_dev.to_parquet("X_dev.parquet")
y_dev.to_frame().to_parquet("y_dev.parquet")
print("\nDevelopment subsample saved: X_dev.parquet, y_dev.parquet")
print("Dev subsample shape:", X_dev.shape)

# Also save the full working set for later confirmation runs
X_working.to_parquet("X_working.parquet")
y_working.to_frame().to_parquet("y_working.parquet")

# Point 5: confirm class balance is consistent
print("\nClass balance check:")
print("Full y:", y.mean())
print("Working y:", y_working.mean())
print("Test y:", y_test.mean())
print("Dev subsample y:", y_dev.mean())

with open("decision_log.md", "a") as f:
    f.write("\n## Day 1, Block 3 Leakage Audit and Split Design\n\n")
    f.write("- Dropped SK_ID_CURR (pure identifier, no predictive signal)\n")
    f.write(f"- Locked test set: {X_test.shape}, saved to X_test.parquet/y_test.parquet, untouched until Day 4\n")
    f.write(f"- Development subsample: {X_dev.shape}, saved for fast iteration\n")
    f.write(f"- Class balance held consistent: full={y.mean():.4f}, working={y_working.mean():.4f}, test={y_test.mean():.4f}, dev={y_dev.mean():.4f}\n")