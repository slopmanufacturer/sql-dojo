WITH revenue AS (
    SELECT customer_id, SUM(amount_cents) AS cents
    FROM invoices
    WHERE status = 'paid'
    GROUP BY customer_id
)
SELECT c.name,
       r.cents,
       NTILE(4) OVER (ORDER BY r.cents DESC) AS quartile
FROM revenue r
JOIN customers c ON c.id = r.customer_id
ORDER BY quartile, r.cents DESC;
