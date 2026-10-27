SELECT name, churned_at
FROM customers
WHERE churned_at IS NOT NULL
ORDER BY churned_at;
