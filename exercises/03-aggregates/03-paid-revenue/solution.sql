SELECT SUM(amount_cents) AS total_cents,
       AVG(amount_cents) AS avg_cents
FROM invoices
WHERE status = 'paid';
