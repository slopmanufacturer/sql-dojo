SELECT status, COUNT(*) AS invoices
FROM invoices
GROUP BY status
ORDER BY invoices DESC;
