# Week 3, Day 3 — Write-Up: Logistic Regression & Classification

## 1. Class Balance Check

The target is moderately imbalanced: 61.6% of passengers died, 38.4% survived.
A model that always predicted "died" would score 61.6% accuracy without learning
anything — this sets a real baseline to beat, not zero. Any accuracy score reported
tomorrow needs to be read against this 61.6% floor, not against 50%, or the model's
actual skill would be overstated.

## 2. Confusion Matrix

![alt text](file:///c%3A/Users/User/Pictures/Screenshots/Screenshot%202026-09-17%20110007.png)

- **True Negatives (98):** correctly predicted died
- **False Positives (12):** predicted survived, actually died
- **False Negatives (23):** predicted died, actually survived
- **True Positives (46):** correctly predicted survived

Overall accuracy: (98+46)/179 ≈ 80.4% — meaningfully above the 61.6% baseline.

**False negatives feel more costly here.** A false positive means telling someone
"you would have survived" when they didn't — sobering, but doesn't change any real
outcome retroactively. A false negative means the model failed to recognize a real
survivor's chances — in a hypothetical real-time triage scenario (rather than this
historical dataset), that's the error type that would cost an actual life if acted
on. With 23 false negatives vs. 12 false positives, the model currently leans toward
under-predicting survival more than over-predicting it.

## 3. Threshold Exploration

For one borderline test passenger with a 43.5% predicted survival probability, the
default 0.5 threshold labels them "died," but lowering the threshold to 0.4 flips
that same probability to "survived" — with the model's actual belief about that
passenger completely unchanged. This showed clearly that `.predict()` is not a
separate, independent decision from `.predict_proba()` — it's just probability plus
an arbitrary cutoff. Given the false-negative concern above, someone prioritizing
"catch more true survivors" over "avoid false alarms" would have a real reason to
lower the threshold below 0.5, accepting more false positives in exchange for fewer
missed survivors.

## 4. Open Question for Day 4

Given that the classes aren't perfectly balanced (62/38) and false negatives and
false positives clearly carry different real-world weight here, is accuracy alone
even the right headline metric to trust tomorrow — or should precision and recall
(which separate out exactly these two error types) be the primary numbers reported
instead, with accuracy as a secondary sanity check rather than the main score?
