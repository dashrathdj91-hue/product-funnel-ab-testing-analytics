"""Generate reproducible, purely synthetic user-level funnel and event logs.

No real users, customers, proprietary company records or PII are used.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DATA.mkdir(parents=True, exist_ok=True)
SEED = 20261109
N = 24000


def main():
    rng = np.random.default_rng(SEED)
    variant = rng.choice(['A - Current', 'B - Simplified'], size=N)
    device = rng.choice(['Android', 'iOS', 'Desktop'], size=N, p=[.57, .21, .22])
    source = rng.choice(['Organic', 'Paid Search', 'Social', 'Referral'], size=N,
                        p=[.38, .29, .21, .12])
    region = rng.choice(['North', 'South', 'West', 'East'], size=N,
                        p=[.29, .26, .27, .18])
    dates = pd.Timestamp('2026-08-01') + pd.to_timedelta(rng.integers(0, 31*24*60, N), unit='m')

    # All conditions known in advance; user-level random assignment is independent.
    device_modifier = np.where(device == 'Desktop', .035, np.where(device == 'iOS', .018, 0))
    started = rng.random(N) < np.clip(.495 + device_modifier, 0, 1)
    completion_conditional = np.where(variant == 'B - Simplified', .630, .566)
    completed = started & (rng.random(N) < completion_conditional)
    activated = completed & (rng.random(N) < .655)
    paid = activated & (rng.random(N) < .173)
    revenue = np.where(paid, rng.choice([799, 1499], size=N, p=[.74,.26]), 0)

    visitors = pd.DataFrame({
        'visitor_id': [f'V{i:06d}' for i in range(1, N+1)],
        'variant': variant, 'device':device,'source':source,'region':region,
        'visit_time': pd.to_datetime(dates).strftime('%Y-%m-%d %H:%M:%S')
    })
    events = []
    for i in range(N):
        t = pd.Timestamp(dates[i])
        uid = visitors.at[i,'visitor_id']
        events.append((uid, 'visited', t.strftime('%Y-%m-%d %H:%M:%S'), 0))
        if started[i]:
            events.append((uid, 'signup_started', (t+pd.Timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'), 0))
        if completed[i]:
            events.append((uid, 'signup_completed', (t+pd.Timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'), 0))
        if activated[i]:
            events.append((uid, 'activated', (t+pd.Timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'), 0))
        if paid[i]:
            events.append((uid, 'subscribed', (t+pd.Timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'), int(revenue[i])))
    events = pd.DataFrame(events, columns=['visitor_id', 'event_type', 'event_time', 'revenue_inr'])
    visitors.to_csv(DATA/'visitors.csv',index=False)
    events.to_csv(DATA/'events.csv',index=False)
    print(f'Saved {len(visitors):,} synthetic visitors and {len(events):,} events; seed={SEED}.')

if __name__ == '__main__':
    main()
