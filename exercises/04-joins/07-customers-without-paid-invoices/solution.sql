SELECT c.name
FROM customers c
LEFT JOIN invoices i ON i.customer_id = c.id
                    AND i.status = 'paid'
WHERE i.id IS NULL
ORDER BY c.name;
