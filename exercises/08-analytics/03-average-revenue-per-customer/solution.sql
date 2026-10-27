WITH revenue AS (
    SELECT customer_id, SUM(amount_cents) AS cents
    FROM invoices
    WHERE status = 'paid'
    GROUP BY customer_id
)
SELECT ROUND(AVG(cents) / 100.0, 2) AS arpu_dollars
FROM revenue;
