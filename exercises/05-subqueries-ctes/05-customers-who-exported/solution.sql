SELECT c.name
FROM customers c
WHERE EXISTS (SELECT 1
              FROM events e
              WHERE e.customer_id = c.id
                AND e.name = 'export')
ORDER BY c.name;
