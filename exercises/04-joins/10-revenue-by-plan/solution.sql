SELECT p.name, SUM(i.amount_cents) AS paid_cents
FROM plans p
JOIN customers c ON c.plan_id = p.id
JOIN invoices i ON i.customer_id = c.id
WHERE i.status = 'paid'
GROUP BY p.id, p.name
ORDER BY paid_cents DESC;
