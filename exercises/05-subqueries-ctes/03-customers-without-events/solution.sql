SELECT c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1
                  FROM events e
                  WHERE e.customer_id = c.id)
ORDER BY c.name;
