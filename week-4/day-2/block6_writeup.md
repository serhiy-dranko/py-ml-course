# Week 4, Day 2 Write-Up: Hyperparameter Tuning

## What Improved

Two models were tuned: LogisticRegression via GridSearchCV (10 candidates × 5
folds) and HistGradientBoostingClassifier via RandomizedSearchCV (30 candidates
× 5 folds). On the full working set, LogisticRegression improved from 0.7399 to
0.7442 (+0.0043), and HistGradientBoosting reached 0.7499 — the best score of the
week so far, and clearly ahead of LogisticRegression by 0.0057, a gap now larger
than either model's cross-validation standard deviation (0.0025-0.0032).

## Relative to the Noise Floor

On the 50k development subsample, LogisticRegression's tuning gain (+0.0017) sat
well *inside* Day 1's noise floor (std 0.0098) — genuinely indistinguishable from
random split variation at that scale. The full working set confirmation was
essential here: with std shrinking to 0.0032 on 246k rows, the same improvement
became real and reproducible, illustrating exactly why Day 1's "iterate small,
confirm big" discipline matters, not as a formality but as the difference between
a real finding and noise.

## Which Hyperparameters Mattered Most

For LogisticRegression, `C=0.1` (moderate regularization) beat both stronger
(`C=0.001`) and weaker (`C=10`) regularization, though the margin between all 10
candidates was tiny — near-ties across the whole grid, suggesting this model has
limited room to improve regardless of tuning. For HistGradientBoosting, a low
`learning_rate` (~0.038) paired with a small `max_leaf_nodes` (22) and a high
`min_samples_leaf` (97) won — all three point the same direction: a *simpler*,
more conservative tree structure generalized better than more complex candidates,
several of which showed visibly larger train/validation gaps (up to 0.17) despite
similar validation scores.

## What Surprised Me

The grid-vs-random comparison at equal budget (Block 5) found the *exact same*
best score (0.7416) via two different paths this reminder that random search's
advantage only shows up when the search space has enough dimensions to matter;
for a simple 2-parameter space, exhaustive grid search and random sampling
converge to the same answer. The clearer surprise was how much every top HGB
candidate showed a real train/validation gap (0.07-0.17) even at the "best"
setting a signal worth carrying into Day 3's feature engineering and Day 4's
overfitting diagnosis, since gradient boosting's flexibility cuts both ways.