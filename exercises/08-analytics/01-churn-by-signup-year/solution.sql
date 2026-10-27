SELECT substr(signup_at, 1, 4) AS year,
       COUNT(*) AS customers,
       SUM(CASE WHEN churned_at IS NOT NULL THEN 1 ELSE 0 END) AS churned,
       ROUND(100.0 * SUM(CASE WHEN churned_at IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_pct
FROM customers
GROUP BY year
ORDER BY year;
