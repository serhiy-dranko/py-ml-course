# Part 3 Reflection: What's Next

Heading past this week, I'd want to learn how to actually *fix* the recall gap I
found in the Titanic model rather than just diagnosing it right now I know
*that* the model misses a third of real survivors and *why* the threshold trade-off
exists. But not yet what techniques (resampling the minority class, trying a
different model entirely, engineering better features) would genuinely improve
recall without just arbitrarily sliding the threshold and accepting worse
precision as a trade. I'd also want to understand feature engineering more
deeply. Day 1's dropped columns (`Name`, `Cabin`) clearly held *some* signal
(a passenger's title, their deck) that a smarter transformation could have
recovered instead of discarding outright, and that feels like the natural next
skill this week's simple encoding didn't touch.