# Project 02 — A/B Testing: Checkout Conversion

**Мета:** оцінити зміну конверсії після умовного редизайну checkout. **Усі 12 000 користувачів синтетичні**. У `generate_data.py` описано механізм їх створення.

**Дизайн:** рандомізація на рівні користувача в дві групи A/B 50/50, бінарна конверсія та виручка на користувача. Primary metric = conversion rate, supplementary guardrail = revenue per user. Фіксоване вікно, один підсумковий аналіз.

**Статистика:** перевірка sample ratio mismatch (chi-square goodness-of-fit), різниця часток (percentage points), відносний uplift, двосторонній z-test для двох часток та приблизний 95% CI на непулінговій дисперсії. Welch t-test для revenue/user — тільки як навчальна ілюстрація за наявності скошеного розподілу.

**Файли:** `data/experiment.csv`, `analyze.py`, `sql/ab_postgresql.sql`, `outputs/results.txt`, `outputs/variant_summary.csv`, `outputs/conversion.png`.

**Питання на співбесіді:** Навіщо рандомізація? Що таке SRM? Різниця між p-value і CI? Як порахувати MDE та sample size? Як контролювати peeking і множинні перевірки? Що робити, коли conversion росте, але revenue/user падає? Коли потрібен bootstrap?
