SELECT name
FROM customers
WHERE id IN (SELECT customer_id FROM invoices WHERE status = 'void')
ORDER BY name;
