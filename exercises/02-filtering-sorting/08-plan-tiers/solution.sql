SELECT name,
       monthly_price_cents,
       CASE
           WHEN monthly_price_cents < 5000 THEN 'cheap'
           WHEN monthly_price_cents < 50000 THEN 'mid'
           ELSE 'enterprise'
       END AS tier
FROM plans
ORDER BY monthly_price_cents;
