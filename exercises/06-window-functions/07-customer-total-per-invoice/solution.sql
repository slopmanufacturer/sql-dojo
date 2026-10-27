SELECT id,
       customer_id,
       amount_cents,
       SUM(amount_cents) OVER (PARTITION BY customer_id) AS customer_total
FROM invoices
WHERE status = 'paid'
  AND issued_at >= '2025-05-01'
ORDER BY customer_id, id;
