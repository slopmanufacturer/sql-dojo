WITH monthly AS (
    SELECT substr(issued_at, 1, 7) AS month,
           SUM(amount_cents) AS cents
    FROM invoices
    WHERE status = 'paid'
    GROUP BY month
)
SELECT month,
       cents,
       cents - LAG(cents) OVER (ORDER BY month) AS change_cents
FROM monthly
ORDER BY month;
