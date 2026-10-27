SELECT name, monthly_price_cents / 100.0 AS monthly_price
FROM plans
ORDER BY monthly_price DESC;
