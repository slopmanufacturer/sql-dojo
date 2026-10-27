SELECT id, issued_at, amount_cents
FROM invoices
WHERE issued_at BETWEEN '2024-01-01' AND '2024-03-31'
ORDER BY issued_at, id;
