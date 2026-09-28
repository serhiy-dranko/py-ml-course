# Week 4, Day 3 Write-Up: Feature Engineering

## What Helped

Stateless feature engineering (sentinel fix, age/employment in years, affordability
ratios, EXT_SOURCE aggregates, document count) combined with the Day 2 tuned
HistGradientBoosting hyperparameters produced 0.7555 ± 0.0016 ROC-AUC on the full
working set — up from 0.7458 ± 0.0025 after Day 2's tuning alone, and 0.7387 after
Day 1's untuned baseline. Feature engineering contributed a larger gain (+0.0097)
than hyperparameter tuning did the day before (+0.0071), confirming the Concepts
doc's expectation that better features often beat better tuning on tabular data.

## What Didn't Help

Filtering out constant and highly-correlated columns (Block 5) actually *hurt*
performance slightly (0.7459 vs. 0.7488 without filtering) — gradient boosting
tolerated redundant correlated features without penalty, and some apparently
"redundant" columns still carried marginal signal the correlation filter couldn't
see. TargetEncoder for `ORGANIZATION_TYPE`, done safely inside the pipeline,
underperformed simple one-hot encoding (0.7371 vs. 0.7458) — a reminder that a
"more sophisticated" encoding isn't automatically better.

## The Pandas vs. Pipeline Finding

Running the identical target-encoding + imputation + scaling steps ad-hoc in
pandas before cross-validation versus inside a sklearn Pipeline produced a 0.0045
gap (0.7416 leaky vs. 0.7371 safe) — comparable in size to a full day's worth of
legitimate feature engineering gains. This is concrete evidence, not just a
warning to take on faith: any stateful transformation fit on the whole dataset
before splitting inflates the reported score by an amount large enough to
completely mask whether a change is real. Every stateful step (imputation,
scaling, encoding) now lives inside the pipeline going forward.

## Most Important Discovery

Permutation importance revealed `EXT_SOURCE_MEAN` — an engineered feature — as
roughly 15x more important than the next-best feature (0.109 vs. 0.007), and 5 of
the day's 10 engineered features landed in the top 15 by importance. This directly
validated the Block 1 hypothesis that combining the three EXT_SOURCE columns would
be more robust than any single one alone, and explains most of today's score gain.

## Open Note for Day 4

The final pipeline is saved (`final_feature_pipeline.pkl`) with Day 2's tuned
hyperparameters applied to Day 3's engineered features — but those hyperparameters
were tuned *before* these new features existed. Day 4 should check whether a
short re-tune on the new feature set improves things further, and this is also
where the locked test set finally gets touched for the one honest, final read.