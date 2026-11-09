# Product Signup Funnel & A/B Testing Analytics

**SQL | Python | Pandas | Statistical Hypothesis Testing | Business Decision-Making**

> **Portfolio simulation - not a real company's experiment.** This repository uses completely **synthetic, reproducible** data and a **simulated** user-level randomized A/B assignment. The observed effects are examples for technical demonstration, not evidence of real-world product impact.

## Business question

A subscription product is considering a simplified signup flow (Variant B) versus its current signup flow (Variant A). Does Variant B increase **visitor-to-signup-completion conversion**? What happens to the downstream paid-subscription metric?

## Executive summary

A reproducible simulation of **24,000 visitors** and **48,679 events** produced the following comparison:

| Metric | A: Current flow | B: Simplified flow |
|---|---:|---:|
| Visitors | 11,980 | 12,020 |
| Started signup | 6,030 | 6,040 |
| Completed signup | 3,359 | 3,767 |
| Visitor → completed signup | 28.04% | 31.34% |
| Activated users | 2,212 | 2,476 |
| Paid subscriptions | 373 | 422 |
| Visitor → paid subscription | 3.11% | 3.51% |

- **Primary metric:** B - A = **+3.30 percentage points** (approximately **+11.77% relative**).
- **Two-proportion z-test:** two-sided p ≈ **2.19e-08**, with 95% CI for the absolute difference of **[+2.15, +4.46] percentage points**.
- **Guardrail:** B's simulated paid conversion was 3.51% versus A's 3.11%. We did **not** pre-register or power the experiment for paid conversion; treat that comparison as exploratory.
- **Business recommendation in the simulated scenario:** B is a plausible candidate for wider testing, subject to independent validation, production instrumentation, additional guardrails and real-world performance.

**Important interpretation:** The generator deliberately assigns a higher conditional signup-completion probability to B, so significance is unsurprising. It only proves the analysis pipeline works on the designed example. It is **not** a causal claim about actual customers.

## Pipeline

```text
24,000 synthetic visitors
          |
          v
Randomly assign A / B + simulate user event progression
          |
          v
visitors.csv + events.csv
          |
          +--> SQLite SQL: variant funnel, source breakdown, revenue
          |
          +--> Python: sanity checks, Z-test, 95% CI and figures
          |
          v
Business-ready KPI summary and experiment decision note
```

## Run locally (Windows, macOS or Linux)

1. Install Python 3.10+.
2. Open a terminal in this repository directory.
3. Install dependencies and run:

```bash
python -m pip install -r requirements.txt
python src/generate_data.py
python src/analyze_experiment.py
python src/run_sql.py
```

If `python` is not recognized on Windows, try `py` instead.

Each run produces deterministic results because the seed is `20261109`. Outputs are included, so recruiters can inspect them without running code.

## Repository map

```text
README.md
requirements.txt
src/
  generate_data.py        # synthetic experiment + event tracking
  analyze_experiment.py   # funnel KPIs, two-proportion test, confidence interval
  run_sql.py              # load CSVs in SQLite, run SQL queries
sql/
  01_funnel_kpis.sql      # conversion funnel, channel analysis, revenue
images/
  signup_conversion.png
  paid_conversion.png
data/
  visitors.csv
  events.csv
  README.md
outputs/
  funnel_summary.csv
  experiment_results.json
  sql_query_1.csv
  sql_query_2.csv
  sql_query_3.csv
docs/
  business_brief.md
  interview_practice.md
```

## Core analytical definitions

- **Unit of assignment:** visitor. Each visitor belongs to exactly one experiment arm.
- **Primary metric:** distinct visitors completing signup / distinct visitors exposed.
- **Guardrail metric:** distinct visitors purchasing subscription / distinct visitors exposed.
- **Statistical method:** pooled standard error for the two-sided Z-test; unpooled Wald CI for difference in proportions.
- **Decision threshold:** exploratory `alpha=0.05` for a single predefined primary metric.
- **Funnel integrity:** every downstream event requires all prior steps.

## Limits and ethical reporting

- Synthetic data only. Not evidence of an actual business improvement.
- Paid conversion and channel subgroup analysis are exploratory, not evidence of causal effects.
- Only one simulated experiment; no power calculation, pre-registration, long-term retention, seasonality or production traffic.
- Revenue is illustrative, not recognized revenue from a real company.
- `variant` is randomized at the user level; treatment effects are deliberately programmed into the generator.

**Portfolio owner:** Dashrath Kumar | [GitHub](https://github.com/dashrathdj91-hue)
