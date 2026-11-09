# One-page Business Brief | Synthetic Signup Experiment

**Decision:** In a constructed demonstration of an onboarding experiment, the simplified flow shows higher visitor-to-signup-completion conversion. No production rollout is justified from simulated data alone.

## Problem and hypothesis
Simplifying the signup experience could reduce funnel drop-off, increasing completed signups. Primary outcome is user-level completed-signup conversion. Paid subscription conversion is a downstream guardrail.

## Results
- 24,000 synthetic visitors; 48,679 simulated event records.
- A (11,980 visitors): 3,359 completions / **28.04%**.
- B (12,020 visitors): 3,767 completions / **31.34%**.
- Absolute difference: **+3.30 pp**; 95% CI **[+2.15, +4.46] pp**; two-sided Z-test p≈**2.19e-08**.
- Paid conversion: **3.11%** (A), **3.51%** (B); exploratory only.

## Recommendations
1. If this were a real product, first audit experiment randomization, data completeness, device tracking and metric definitions.
2. Repeat on genuine production users with a pre-registered decision rule, sample-size/power plan and guardrails.
3. Evaluate post-signup activation, payment failures, refunds, support complaints and 30-day retention.
4. Segment exploratory results by source and device without claiming causality from subgroup comparisons.

## Caveat
All data and effects in this exercise were generated synthetically. This is an analytical skills demonstration, not a real-world business case or rollout recommendation.
