SELECT c.name, SUM(i.amount_cents) AS paid_cents
FROM customers c
JOIN invoices i ON i.customer_id = c.id
WHERE c.country = 'DE'
  AND i.status = 'paid'
GROUP BY c.id, c.name
ORDER BY paid_cents DESC;
