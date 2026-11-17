"""Generate reproducible fictional transactions. No customer PII."""
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).parent / 'data' / 'transactions.csv'
rng = np.random.default_rng(42)
anchor = pd.Timestamp('2026-09-30')
rows=[]
for cid in range(1, 1201):
    group = rng.choice(['regular', 'loyal', 'occasional'], p=[.52,.20,.28])
    params = {'regular': (5, 45, 250), 'loyal': (18, 18, 420), 'occasional': (2, 140, 180)}[group]
    n=max(1,int(rng.poisson(params[0])))
    recency=int(np.clip(rng.exponential(params[1]), 0, 340))
    for i in range(n):
        lag=int(np.clip(recency+rng.exponential(65),0,364))
        date=anchor-pd.Timedelta(days=lag)
        amount=round(float(np.clip(rng.lognormal(np.log(params[2]),.48), 15, 3000)),2)
        rows.append((f'C{cid:05d}',f'O{len(rows)+1:07d}',date.date().isoformat(),amount))
df=pd.DataFrame(rows, columns=['customer_id','order_id','order_date','amount'])
OUT.parent.mkdir(parents=True,exist_ok=True)
df.to_csv(OUT,index=False)
print(f'Generated {len(df)} transactions for {df.customer_id.nunique()} customers -> {OUT}')
