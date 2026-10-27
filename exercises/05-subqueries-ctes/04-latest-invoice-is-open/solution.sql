SELECT c.name, i.issued_at, i.amount_cents
FROM customers c
JOIN invoices i ON i.customer_id = c.id
WHERE i.id = (SELECT x.id
              FROM invoices x
              WHERE x.customer_id = c.id
              ORDER BY x.issued_at DESC, x.id DESC
              LIMIT 1)
  AND i.status = 'open'
ORDER BY i.issued_at DESC, c.name;
