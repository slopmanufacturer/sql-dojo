SELECT status,
       ROUND(AVG(amount_cents) / 100.0, 2) AS avg_dollars
FROM invoices
GROUP BY status
ORDER BY avg_dollars DESC;
