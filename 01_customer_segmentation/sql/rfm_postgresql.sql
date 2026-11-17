-- PostgreSQL. Import data/transactions.csv into a table named transactions
-- (customer_id text, order_id text, order_date date, amount numeric).
WITH customer_rfm AS (
    SELECT customer_id,
           DATE '2026-10-01' - MAX(order_date) AS recency,
           COUNT(DISTINCT order_id) AS frequency,
           SUM(amount) AS monetary
    FROM transactions
    GROUP BY customer_id
)
SELECT * FROM customer_rfm ORDER BY monetary DESC LIMIT 20;

-- Window function: rank customers by value within recency bands.
WITH scored AS (
 SELECT customer_id, DATE '2026-10-01'-MAX(order_date) AS recency,
        SUM(amount) AS monetary FROM transactions GROUP BY customer_id
)
SELECT customer_id, recency, monetary,
       DENSE_RANK() OVER (PARTITION BY CASE WHEN recency <= 30 THEN 'recent' ELSE 'older' END
                          ORDER BY monetary DESC) AS spend_rank_within_band
FROM scored;
