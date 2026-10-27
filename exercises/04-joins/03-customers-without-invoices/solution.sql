SELECT c.name, c.country
FROM customers c
LEFT JOIN invoices i ON i.customer_id = c.id
WHERE i.id IS NULL
ORDER BY c.name;
