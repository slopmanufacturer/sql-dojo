SELECT c.name, t.total
FROM customers c
JOIN (SELECT customer_id, SUM(amount_cents) AS total
      FROM invoices
      WHERE status = 'paid'
      GROUP BY customer_id) t ON t.customer_id = c.id
WHERE t.total > (SELECT AVG(total)
                 FROM (SELECT SUM(amount_cents) AS total
                       FROM invoices
                       WHERE status = 'paid'
                       GROUP BY customer_id))
ORDER BY t.total DESC;
