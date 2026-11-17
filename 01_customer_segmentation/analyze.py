"""Reproducible RFM + K-Means segmentation with descriptive profiling."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

HERE=Path(__file__).parent
DATA=HERE/'data'/'transactions.csv'
OUT=HERE/'outputs'; OUT.mkdir(exist_ok=True)
if not DATA.exists():
    raise SystemExit('Run generate_data.py first')
df=pd.read_csv(DATA, parse_dates=['order_date'])
assert df['order_id'].is_unique and (df['amount']>0).all()
reference=pd.Timestamp('2026-10-01')
rfm=df.groupby('customer_id',as_index=False).agg(
    recency=('order_date',lambda x:(reference-x.max()).days),
    frequency=('order_id','nunique'),
    monetary=('amount','sum'))
features=np.log1p(rfm[['recency','frequency','monetary']])
scaled=StandardScaler().fit_transform(features)
model=KMeans(n_clusters=3,random_state=42,n_init=10)
rfm['cluster']=model.fit_predict(scaled)
profiles=rfm.groupby('cluster').agg(customers=('customer_id','count'),
    median_recency=('recency','median'),median_frequency=('frequency','median'),
    median_monetary=('monetary','median')).round(1)
profiles['customer_share_pct']=(profiles['customers']/len(rfm)*100).round(1)
rfm.to_csv(OUT/'customer_segments.csv',index=False)
profiles.to_csv(OUT/'cluster_profiles.csv')
fig,ax=plt.subplots(figsize=(7,4))
for cluster,frame in rfm.groupby('cluster'):
    ax.scatter(frame['frequency'],frame['monetary'],s=12,alpha=.45,label=f'Cluster {cluster}')
ax.set_xlabel('Orders in period');ax.set_ylabel('Total spending (synthetic units)')
ax.set_title('Customer segmentation: frequency vs monetary')
ax.legend();fig.tight_layout();fig.savefig(OUT/'clusters.png',dpi=150);plt.close(fig)
print('RFM profiles (cluster IDs arbitrary):')
print(profiles.to_string())
print('Outputs saved to',OUT)
