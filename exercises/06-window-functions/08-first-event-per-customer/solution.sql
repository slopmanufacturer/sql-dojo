SELECT DISTINCT customer_id,
       FIRST_VALUE(name) OVER (PARTITION BY customer_id
                               ORDER BY occurred_at, id) AS first_event
FROM events
ORDER BY customer_id;
