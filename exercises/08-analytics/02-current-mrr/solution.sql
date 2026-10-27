SELECT p.name,
       COUNT(*) AS active_customers,
       SUM(p.monthly_price_cents) AS mrr_cents
FROM customers c
JOIN plans p ON p.id = c.plan_id
WHERE c.churned_at IS NULL
GROUP BY p.id, p.name
ORDER BY mrr_cents DESC;
