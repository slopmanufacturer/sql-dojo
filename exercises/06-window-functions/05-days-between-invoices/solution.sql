SELECT customer_id,
       issued_at,
       julianday(LEAD(issued_at) OVER (PARTITION BY customer_id ORDER BY issued_at))
         - julianday(issued_at) AS days_to_next
FROM invoices
WHERE customer_id IN (1, 2, 3)
ORDER BY customer_id, issued_at;
