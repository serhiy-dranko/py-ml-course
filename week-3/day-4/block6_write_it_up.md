# Model Evaluation Summary

The regression model achieved an **RMSE of $5,796.28** and an **R² of 0.784**. Compared with the baseline RMSE of **$12,465.61**, the model reduced the typical prediction error by about **$6,669**, which shows a substantial improvement over simply predicting the mean.

The classification model achieved **80.4% accuracy**, with **79.3% precision** and **66.7% recall**. The baseline accuracy was **61.5%** when always predicting the majority class. This means the model clearly performed better than the baseline. However, the recall for class 1 was lower than its precision, so the model still missed some positive cases.

The threshold experiment showed that changing the classification threshold changes the balance between precision and recall. At the default **0.50 threshold**, precision was **79.3%** and recall was **66.7%**. Lowering the threshold to **0.35** increased recall to **78.3%**, but precision dropped to **69.2%**. This demonstrates the typical precision/recall trade-off: identifying more positive cases comes with more false positives.

