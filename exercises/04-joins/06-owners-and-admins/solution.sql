SELECT o.email AS owner_email,
       a.email AS admin_email,
       o.customer_id
FROM users o
JOIN users a ON a.customer_id = o.customer_id
            AND a.role = 'admin'
WHERE o.role = 'owner'
ORDER BY o.customer_id;
