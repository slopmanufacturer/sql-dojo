WITH last_event AS (
    SELECT customer_id, MAX(occurred_at) AS last_seen
    FROM events
    GROUP BY customer_id
)
SELECT c.name,
       COALESCE(l.last_seen, c.signup_at) AS last_seen,
       CAST(julianday('2025-06-30')
            - julianday(COALESCE(l.last_seen, c.signup_at)) AS INTEGER) AS days_since
FROM customers c
LEFT JOIN last_event l ON l.customer_id = c.id
WHERE c.churned_at IS NULL
  AND julianday('2025-06-30')
      - julianday(COALESCE(l.last_seen, c.signup_at)) > 30
ORDER BY days_since DESC;
