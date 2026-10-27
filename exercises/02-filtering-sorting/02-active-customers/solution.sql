SELECT name
FROM customers
WHERE churned_at IS NULL
ORDER BY name;
