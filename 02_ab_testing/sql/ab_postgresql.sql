-- PostgreSQL. Import data/experiment.csv into experiment
-- (user_id text, variant text, converted integer, revenue numeric).
SELECT variant, COUNT(*) AS users, SUM(converted) AS converters,
       AVG(converted::numeric) AS conversion_rate,
       AVG(revenue) AS revenue_per_user
FROM experiment GROUP BY variant ORDER BY variant;

-- Convert B vs A from conditional aggregation
WITH stats AS (
 SELECT variant, AVG(converted::numeric) AS cr, COUNT(*) AS users
 FROM experiment GROUP BY variant
)
SELECT b.cr-a.cr AS absolute_uplift,
       (b.cr/NULLIF(a.cr,0))-1 AS relative_uplift,
       a.users AS a_users, b.users AS b_users
FROM stats a CROSS JOIN stats b
WHERE a.variant='A' AND b.variant='B';
