# Cost estimates based on Day 1 timings:
# Dev subsample fit time: 2.71s (logistic regression pipeline)
# HGB is typically similar or faster per fit on this size, but has more hyperparameters

print("=== Search cost planning ===\n")

print("Logistic Regression grid search:")
print("Grid: C in [0.001, 0.01, 0.1, 1, 10] (5 values, log scale. spans orders of magnitude,")
print("      since regularization strength effects are multiplicative, not additive)")
print("      class_weight in [None, 'balanced'] (2 values.tests whether explicitly")
print("      accounting for the 8%/92% imbalance helps ROC-AUC)")
print("Total candidates: 5 x 2 = 10")
print("Folds: 5")
print("Estimated cost: 10 x 5 x 2.71s = 135.5s (~2.3 min) -> use GridSearchCV, small space")

print("\nHistGradientBoosting random search:")
print("Distributions:")
print("  learning_rate: loguniform(0.01, 0.3) — spans orders of magnitude")
print("  max_leaf_nodes: randint(15, 127) — controls tree complexity/depth")
print("  min_samples_leaf: randint(10, 100) — regularizes against overfitting on leaves")
print("  l2_regularization: loguniform(1e-3, 10) — regularization strength, log scale")
print("n_iter: 30 (budget-driven choice)")
print("Folds: 5")
print("Estimated cost: 30 x 5 x ~3s = 450s (~7.5 min) to use RandomizedSearchCV, larger space")

print("\nTotal Day 2 compute budget target: under 15 minutes for both primary searches,")
print("leaving room for Block 5's equal-budget comparison and Block 6's full-data confirmation.")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 2, Block 2 — Search Planning\n\n")
    f.write("- LogisticRegression: GridSearchCV, 10 candidates x 5 folds, ~2.3 min estimated\n")
    f.write("- HistGradientBoosting: RandomizedSearchCV, n_iter=30 x 5 folds, ~7.5 min estimated\n")
    f.write("- Total Day 2 budget target: under 15 minutes for primary searches\n")