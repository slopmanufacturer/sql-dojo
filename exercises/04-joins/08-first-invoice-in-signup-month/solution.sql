SELECT c.name,
       c.signup_at,
       MIN(i.issued_at) AS first_invoice
FROM customers c
JOIN invoices i ON i.customer_id = c.id
GROUP BY c.id, c.name, c.signup_at
HAVING substr(MIN(i.issued_at), 1, 7) = substr(c.signup_at, 1, 7)
ORDER BY c.name;
