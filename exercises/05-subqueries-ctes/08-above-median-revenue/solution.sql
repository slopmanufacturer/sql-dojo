WITH revenue AS (
    SELECT customer_id, SUM(amount_cents) AS cents
    FROM invoices
    WHERE status = 'paid'
    GROUP BY customer_id
),
median AS (
    SELECT cents
    FROM revenue
    ORDER BY cents
    LIMIT 1 OFFSET (SELECT COUNT(*) / 2 FROM revenue)
)
SELECT c.name, r.cents
FROM revenue r
JOIN customers c ON c.id = r.customer_id
WHERE r.cents > (SELECT cents FROM median)
ORDER BY r.cents DESC;
