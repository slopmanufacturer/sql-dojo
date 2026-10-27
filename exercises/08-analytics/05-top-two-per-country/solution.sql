WITH revenue AS (
    SELECT customer_id, SUM(amount_cents) AS cents
    FROM invoices
    WHERE status = 'paid'
    GROUP BY customer_id
),
ranked AS (
    SELECT c.country,
           c.name,
           r.cents,
           ROW_NUMBER() OVER (PARTITION BY c.country ORDER BY r.cents DESC, c.name) AS n
    FROM revenue r
    JOIN customers c ON c.id = r.customer_id
)
SELECT country, name, cents
FROM ranked
WHERE n <= 2
ORDER BY country, cents DESC;
