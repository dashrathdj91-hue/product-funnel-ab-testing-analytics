"""Reproducible A/B analysis: conversion, confidence interval, Z-test and guardrails."""
from pathlib import Path
import json
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'; IMG=ROOT/'images'
OUT.mkdir(exist_ok=True); IMG.mkdir(exist_ok=True)


def two_proportion_test(success_a, n_a, success_b, n_b):
    pa = success_a/n_a; pb = success_b/n_b
    pooled=(success_a+success_b)/(n_a+n_b)
    se_pooled=math.sqrt(pooled*(1-pooled)*(1/n_a+1/n_b))
    z=(pb-pa)/se_pooled if se_pooled>0 else float('nan')
    p=2*norm.sf(abs(z)) if math.isfinite(z) else float('nan')
    se_diff=math.sqrt(pa*(1-pa)/n_a+pb*(1-pb)/n_b)
    diff=pb-pa
    return {'rate_a':pa,'rate_b':pb,'absolute_lift_pp':100*diff,
            'relative_lift_pct':100*diff/pa if pa else None,
            '95pct_ci_difference_pp':[100*(diff-1.96*se_diff),100*(diff+1.96*se_diff)],
            'z_score':z,'two_sided_p_value':p,'significant_at_0_05':bool(p<.05)}


def main():
    visitors=pd.read_csv(ROOT/'data'/'visitors.csv')
    events=pd.read_csv(ROOT/'data'/'events.csv')
    assert visitors.visitor_id.is_unique
    assert events.visitor_id.isin(visitors.visitor_id).all()
    flags=pd.crosstab(events.visitor_id,events.event_type).gt(0).reindex(visitors.visitor_id,fill_value=False)
    flags=flags.rename_axis('visitor_id').reset_index()
    frame=visitors.merge(flags,on='visitor_id',validate='one_to_one')
    required=['visited','signup_started','signup_completed','activated','subscribed']
    assert all(x in frame.columns for x in required)
    assert frame['visited'].all()
    for earlier,later in zip(required,required[1:]):
        assert not (frame[later] & ~frame[earlier]).any(), 'Funnel ordering failure'
    grouped=frame.groupby('variant',sort=True)
    counts=grouped[required].sum().astype(int)
    counts.insert(0,'visitors',grouped.size())
    counts['visit_to_signup_pct']=(100*counts.signup_completed/counts.visitors).round(2)
    counts['visit_to_paid_pct']=(100*counts.subscribed/counts.visitors).round(2)
    counts.to_csv(OUT/'funnel_summary.csv')

    a=counts.loc['A - Current']; b=counts.loc['B - Simplified']
    primary=two_proportion_test(int(a.signup_completed),int(a.visitors),int(b.signup_completed),int(b.visitors))
    paid=two_proportion_test(int(a.subscribed),int(a.visitors),int(b.subscribed),int(b.visitors))
    revenue=events[events.event_type=='subscribed'].merge(visitors[['visitor_id','variant']],on='visitor_id')
    revenue_by_variant=revenue.groupby('variant').revenue_inr.sum().to_dict()
    report={
        'data_type':'synthetic; not real business outcome', 'random_seed':20261109,
        'primary_metric':'visitor-to-signup-completed conversion',
        'primary_test':primary,
        'guardrail_metric':'visitor-to-paid-subscription conversion',
        'guardrail_test':paid,
        'revenue_inr_by_variant':{v:int(revenue_by_variant.get(v,0)) for v in counts.index},
        'note':'Simulated experiment only. Significance is for this constructed sample, not evidence of real-world impact. Multiple secondary metrics are exploratory.'
    }
    (OUT/'experiment_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    for metric,title,filename in [('visit_to_signup_pct','Visitor-to-signup conversion','signup_conversion.png'),('visit_to_paid_pct','Visitor-to-paid conversion','paid_conversion.png')]:
        fig,ax=plt.subplots(figsize=(7.0,4.2))
        vals=counts[metric]
        bars=ax.bar(['A: Current','B: Simplified'],vals.values,color=['#2563EB','#0F766E'],width=.52)
        ax.set_ylim(0,max(vals.values)*1.32)
        ax.set_ylabel('Conversion rate (%)'); ax.set_title(title)
        for bar,v in zip(bars,vals.values): ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+.2,f'{v:.2f}%',ha='center',fontsize=11)
        ax.grid(axis='y',alpha=.20)
        fig.tight_layout(); fig.savefig(IMG/filename,dpi=170);plt.close(fig)
    print(counts.to_string())
    print('Primary result:',json.dumps(primary,indent=2))
    print('Saved output CSV, JSON and 2 charts.')

if __name__=='__main__': main()
