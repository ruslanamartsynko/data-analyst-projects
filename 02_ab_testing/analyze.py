"""A/B test: randomisation check, conversion inference and revenue guardrail."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm, ttest_ind
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).parent;OUT=HERE/'outputs';OUT.mkdir(exist_ok=True)
df=pd.read_csv(HERE/'data'/'experiment.csv')
assert df.user_id.is_unique and df.variant.isin(['A','B']).all()
assert df.converted.isin([0,1]).all() and (df.revenue>=0).all()
a=df[df.variant=='A'];b=df[df.variant=='B']
n_a,n_b=len(a),len(b);x_a=int(a.converted.sum());x_b=int(b.converted.sum())
p_a=x_a/n_a;p_b=x_b/n_b;diff=p_b-p_a
# SRM check against 50/50 allocation
from scipy.stats import chisquare
srm_p=chisquare([n_a,n_b], f_exp=[len(df)/2]*2).pvalue
pooled=(x_a+x_b)/(n_a+n_b)
se_null=np.sqrt(pooled*(1-pooled)*(1/n_a+1/n_b))
z=diff/se_null if se_null>0 else np.nan
p_value=2*norm.sf(abs(z))
se_ci=np.sqrt(p_a*(1-p_a)/n_a+p_b*(1-p_b)/n_b)
ci=(diff-1.96*se_ci,diff+1.96*se_ci)
rev_diff=b.revenue.mean()-a.revenue.mean()
rev_p=ttest_ind(b.revenue,a.revenue,equal_var=False).pvalue
summary=pd.DataFrame({'variant':['A','B'],'users':[n_a,n_b],
    'conversions':[x_a,x_b],'conversion_rate':[p_a,p_b],
    'revenue_per_user':[a.revenue.mean(),b.revenue.mean()]})
summary.to_csv(OUT/'variant_summary.csv',index=False)
report=f"""SYNTHETIC EXPERIMENT — exploratory training example
A users={n_a}, B users={n_b}; SRM p-value={srm_p:.4g}
Conversion A={p_a:.3%}, B={p_b:.3%}
Absolute uplift (B-A)={diff:.3%} ({diff*100:.3f} percentage points)
Relative uplift={(diff/p_a):.2%}
Two-sided pooled z-test p-value={p_value:.5f}
Approx. 95% CI for absolute difference=({ci[0]:.3%}, {ci[1]:.3%})
Revenue/user B-A={rev_diff:.3f} synthetic units; exploratory Welch p={rev_p:.5f}
Caveats: synthetic data, fixed-horizon analysis, no power analysis or multiple test adjustment; association under randomization, not real-world impact.
"""
(OUT/'results.txt').write_text(report,encoding='utf-8')
fig,ax=plt.subplots(figsize=(5,4));ax.bar(['A','B'],[p_a*100,p_b*100]);ax.set_ylabel('Conversion rate (%)');ax.set_title('Synthetic A/B conversion');fig.tight_layout();fig.savefig(OUT/'conversion.png',dpi=150);plt.close(fig)
print(report)
