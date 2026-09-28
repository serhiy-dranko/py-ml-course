from datetime import date
from pathlib import Path
 
import pandas as pd
 

DATA_PATH = Path("application_train.csv")
 
df = pd.read_csv(DATA_PATH)
print("Data loaded.\n")

print("=== .shape ===")
print(df.shape)
 
# Compact summary first: how many columns of each type
print("\n=== .dtypes (summary by type) ===")
print(df.dtypes.value_counts())
 
# Full list of column types, as the task asks
print("\n=== .dtypes (all columns) ===")
print(df.dtypes.to_string())
 
# First 5 rows
print("\n=== .head() ===")
print(df.head())


counts = df["TARGET"].value_counts()
percents = df["TARGET"].value_counts(normalize=True) * 100
 

print("\n=== TARGET class balance ===")
print(f"TARGET = 0 (repaid):    {counts[0]:>8,} rows  ({percents[0]:.2f}%)")
print(f"TARGET = 1 (difficulty): {counts[1]:>7,} rows  ({percents[1]:.2f}%)")

# Accuracy of a model that always predicts 0 = share of class 0
always_zero_accuracy = percents[0]
default_rate = percents[1]

print(
    f"\nA model that always predicts 0 gets accuracy ~ {always_zero_accuracy:.1f}% "
    "while finding zero risky clients."
)
problem_statement = f"""
PROBLEM STATEMENT:
A credit analyst at Home Credit uses this model's output to rank loan applications
by predicted default risk before a human makes the final approve/decline/price
decision. The decision this model drives is not "approve everyone the model likes"
but "prioritize which applications get closer manual review and at what price."
Approving a client who later defaults is far costlier than declining a client who
would have repaid (a lost interest-bearing loan vs a lost customer who could
reapply or go elsewhere). So a useful model must rank risky applicants highly
enough to catch most defaults, not just be "usually right" overall.

METRIC JUSTIFICATION:
TARGET is heavily imbalanced ({default_rate:.1f}% default, {always_zero_accuracy:.1f}% repay).
Accuracy is misleading: a model predicting "repays" for every applicant would score
{always_zero_accuracy:.1f}% accuracy while providing zero decision value. ROC-AUC
measures ranking quality across all thresholds regardless of class balance, making
it the primary metric; PR-AUC is tracked as a secondary check since it's more
sensitive to performance on the minority (default) class specifically.

"""
print(problem_statement)

with open("decision_log.md", "w") as f:
    f.write("# Week 4 Decision Log\n\n")
    f.write("## Day 1\n\n")
    f.write(f"- Loaded application_train.csv: shape {df.shape}\n")
    f.write(f"- Class balance: {percents.to_dict()}\n")
    f.write(problem_statement)

print("\nDecision log started: decision_log.md")