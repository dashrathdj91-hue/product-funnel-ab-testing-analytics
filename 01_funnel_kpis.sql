-- SQLite queries. Load data with: python src/run_sql.py
-- Unit of randomization: visitor and conversions count distinct visitor IDs.

-- 1. Whole-funnel drop-offs by experiment arm.
WITH event_flags AS (
  SELECT visitor_id,
         MAX(CASE WHEN event_type = 'signup_started' THEN 1 ELSE 0 END) AS started,
         MAX(CASE WHEN event_type = 'signup_completed' THEN 1 ELSE 0 END) AS completed,
         MAX(CASE WHEN event_type = 'activated' THEN 1 ELSE 0 END) AS activated,
         MAX(CASE WHEN event_type = 'subscribed' THEN 1 ELSE 0 END) AS subscribed
  FROM events
  GROUP BY visitor_id
)
SELECT v.variant,
       COUNT(*) AS visitors,
       SUM(f.started) AS signup_starts,
       SUM(f.completed) AS completed_signups,
       SUM(f.activated) AS activated,
       SUM(f.subscribed) AS paid_subscriptions,
       ROUND(100.0 * SUM(f.completed) / COUNT(*), 2) AS signup_conversion_pct,
       ROUND(100.0 * SUM(f.subscribed) / COUNT(*), 2) AS paid_conversion_pct
FROM visitors v JOIN event_flags f ON v.visitor_id = f.visitor_id
GROUP BY v.variant ORDER BY v.variant;

-- 2. Breakdown by acquisition source (exploratory).
WITH conversion AS (
  SELECT visitor_id, MAX(CASE WHEN event_type='signup_completed' THEN 1 ELSE 0 END) AS complete
  FROM events GROUP BY visitor_id
)
SELECT v.variant, v.source, COUNT(*) AS visitors,
       SUM(c.complete) AS signed_up,
       ROUND(100.0 * SUM(c.complete)/COUNT(*),2) AS conversion_pct
FROM visitors v JOIN conversion c USING(visitor_id)
GROUP BY v.variant,v.source ORDER BY v.source,v.variant;

-- 3. Paid revenue by variant (not a primary A/B outcome).
SELECT v.variant, SUM(CASE WHEN e.event_type='subscribed' THEN e.revenue_inr ELSE 0 END) AS revenue_inr
FROM visitors v JOIN events e USING(visitor_id)
GROUP BY v.variant ORDER BY v.variant;
