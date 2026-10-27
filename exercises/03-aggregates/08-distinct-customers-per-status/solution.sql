SELECT status, COUNT(DISTINCT customer_id) AS customers
FROM invoices
GROUP BY status
ORDER BY status;
