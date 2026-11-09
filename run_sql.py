"""Load synthetic funnel events into in-memory SQLite and run the 3 KPI queries."""
from pathlib import Path
import sqlite3
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
with sqlite3.connect(':memory:') as conn:
    pd.read_csv(ROOT/'data'/'visitors.csv').to_sql('visitors',conn,index=False)
    pd.read_csv(ROOT/'data'/'events.csv').to_sql('events',conn,index=False)
    text=(ROOT/'sql'/'01_funnel_kpis.sql').read_text(encoding='utf8')
    for i,query in enumerate(text.split(';')):
        query=query.strip()
        if not query: continue
        res=pd.read_sql_query(query,conn)
        res.to_csv(ROOT/'outputs'/f'sql_query_{i+1}.csv',index=False)
        print(f'\nSQL query {i+1}\n',res.to_string(index=False))
