import pandas as pd

df_reg = pd.read_csv("insurance.csv")
df_clf = pd.read_csv("titanic.csv")

# 1: mean of charges
mean_charges = df_reg["charges"].mean()
print(f"Mean charges: {mean_charges:.2f}")
print("This mean is a meaningful number because it summarizes the entire collection of dollar amount into a single central balance point")
print("billed per policyholder, directly interpretable as a typical cost.")

# 2: mean of Survived
mean_survived = df_clf["Survived"].mean()
print(f"\nMean Survived: {mean_survived:.2f}")
print(f"Averaging 0/1 survival labels gives a proportion ({mean_survived:.2f}) not a meaningful 'typical passenger'")
print(f"There's no such thing as a passenger who is ({mean_survived:.2f}) alive.")
print("The number only makes sense as a survival RATE, not a prediction target value the way the insurance mean represents a real cost.")

# 3: explicit labeling

print("\n=== Problem type labels ===")
print("=" * 60)
print("insurance.csv -> REGRESSION: 'charges' is a continuous dollar amount that")
print("can be sensibly averaged, compared numerically and predicted as any value along a continuous range.")
print("=" * 60)
print("titanic.csv -> CLASSIFICATION: 'Survived' is a discrete category (0 or 1)")
print("Representing membership in one of two classes and not a quantity of the model's. It's job to assign a class label, not estimate a numeric amount.")
