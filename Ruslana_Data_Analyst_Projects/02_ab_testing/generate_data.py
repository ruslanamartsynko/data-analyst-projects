"""Generate synthetic randomised A/B experiment. Assignment is user-level."""
from pathlib import Path
import numpy as np
import pandas as pd
rng=np.random.default_rng(57)
n=12000
variant=rng.permutation(np.array(['A']*(n//2)+['B']*(n//2)))
activity=rng.normal(size=n)
# A: ~10% conversion, B: ~11.5%; noise makes inference non-trivial.
logit_base=np.log(.10/.90)
prob=1/(1+np.exp(-(logit_base+0.22*activity+(variant=='B')*.15)))
converted=(rng.random(n)<prob).astype(int)
# Higher purchases are not necessarily greater net profit; this is a toy guardrail.
revenue=np.where(converted==1,rng.gamma(shape=2.5,scale=22,size=n),0).round(2)
df=pd.DataFrame({'user_id':[f'U{i:06d}' for i in range(n)],'variant':variant,
                 'converted':converted,'revenue':revenue})
out=Path(__file__).parent/'data'/'experiment.csv';out.parent.mkdir(parents=True,exist_ok=True)
df.to_csv(out,index=False)
print('Generated',len(df),'users ->',out)
