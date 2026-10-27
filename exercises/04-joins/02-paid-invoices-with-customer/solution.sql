SELECT i.id, c.name, i.amount_cents
FROM invoices i
JOIN customers c ON c.id = i.customer_id
WHERE i.status = 'paid'
  AND i.issued_at >= '2025-01-01'
ORDER BY i.id;
