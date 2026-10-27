WITH revenue AS (
    SELECT customer_id, SUM(amount_cents) AS cents
    FROM invoices
    WHERE status = 'paid'
    GROUP BY customer_id
),
counts AS (
    SELECT customer_id, COUNT(*) AS invoices
    FROM invoices
    WHERE status = 'paid'
    GROUP BY customer_id
)
SELECT c.name, r.cents, n.invoices
FROM revenue r
JOIN counts n ON n.customer_id = r.customer_id
JOIN customers c ON c.id = r.customer_id
ORDER BY r.cents DESC
LIMIT 5;
