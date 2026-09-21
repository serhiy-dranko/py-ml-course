# Week 3, Day 4 Write-Up: Evaluation Metrics

## 1. Regression Model (Insurance): RMSE and R²

The linear regression model achieved an RMSE of $5,796.28 and an R² of 0.784 on
the test set. Compared against the trivial baseline (always predicting the mean
charge, RMSE $12,465.61), the model cuts typical prediction error by $6,669.33 —
more than halving the baseline's error. This is a convincing result: the model
isn't just capturing noise, it's meaningfully using age, BMI, smoking status, and
the other features to beat a "know nothing" prediction by a wide margin.

## 2. Classification Model (Titanic): Accuracy, Precision, Recall

The logistic regression model reached 80.4% accuracy, comfortably above the 61.5%
majority-class baseline. However, precision (0.793) and recall (0.667) are not
close together: the model is fairly trustworthy when it predicts "survived" (79%
of those predictions are correct), but it misses a third of the passengers who
actually survived. This gap matters more than the single accuracy number suggests
— a stakeholder only shown 80.4% accuracy would not know the model is
systematically better at avoiding false alarms than at catching every real
survivor.

## 3. Threshold Experiment: Precision/Recall Trade-off

Lowering the decision threshold from 0.5 to 0.35 moved the two metrics in exactly
opposite directions, as predicted: precision dropped from 0.793 to 0.692, while
recall rose from 0.667 to 0.783. This confirms the trade-off is real and
controllable — the model's underlying probabilities didn't change at all between
the two runs, only the cutoff used to convert them into a "survived"/"died" label.
Choosing 0.5 vs. 0.35 isn't a modeling decision at all; it's a business decision
about which mistake (false alarm vs. missed survivor) is more expensive to make.

## 4. Open Question for Day 5

Between the two models built this week, I'd be more comfortable showing the
insurance regression model to someone else — its baseline comparison felt more
immediately convincing (cutting error by more than half, in a unit — dollars —
anyone can interpret without translation) than the Titanic classifier's accuracy
number, which needed the precision/recall breakdown to actually mean something.
Heading into Day 5, my open question is: for a classification problem like this,
should the "one number to report" ever just be accuracy, or should precision and
recall always be reported together as a pair, with accuracy demoted to a
secondary sanity check rather than the headline metric?
