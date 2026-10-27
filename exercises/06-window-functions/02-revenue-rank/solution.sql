WITH revenue AS (
    SELECT customer_id, SUM(amount_cents) AS cents
    FROM invoices
    WHERE status = 'paid'
    GROUP BY customer_id
)
SELECT c.name,
       r.cents,
       RANK() OVER (ORDER BY r.cents DESC) AS rank
FROM revenue r
JOIN customers c ON c.id = r.customer_id
ORDER BY rank, c.name;
