# Interview practice | Product Funnel & A/B Testing

## 30-second project explanation
"I built an end-to-end simulated product-analytics project using SQL and Python. I generated 24,000 synthetic visitors and 48,679 user events, implemented user-level A/B assignment and five funnel events, calculated conversion metrics in SQL, and ran a two-proportion Z-test with a 95% confidence interval in Python. In the simulation, signup conversion was 28.04% for A versus 31.34% for B. I explicitly documented that the results are synthetic, not real company impact."

## Five common questions

**Q: Why is signup completion your primary metric?**
A: It directly measures the proposed onboarding change. It is calculated per exposed visitor to avoid selection bias from only counting people who started signup.

**Q: Why user-level rather than event-level denominators?**
A: Events are repeated observations. Counting unique visitors prevents inflating sample size and breaking the independence assumption.

**Q: What does p = 2.19e-08 mean?**
A: Under a null of equal conversion rates, a difference this extreme or more extreme would be unlikely in the statistical model. It is not the probability that B works and not proof of real product improvement, since data is simulated.

**Q: Is this a real business result?**
A: No. It is a reproducible synthetic portfolio simulation to demonstrate SQL, data validation, funnel definitions and A/B test interpretation.

**Q: What would you add for a production experiment?**
A: Sample-size planning, A/A testing, experiment tracking audits, sample ratio mismatch checks, pre-registered primary and guardrail metrics, and 30-day retention checks.

## How to discuss independent work
You should run the code, inspect SQL query outputs and understand how the generator works before presenting this portfolio project in a referral or interview.
