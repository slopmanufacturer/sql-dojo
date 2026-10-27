SELECT r.name, r.country, r.cents
FROM (
    SELECT c.id,
           c.name,
           c.country,
           SUM(i.amount_cents) AS cents
    FROM customers c
    JOIN invoices i ON i.customer_id = c.id
    WHERE i.status = 'paid'
    GROUP BY c.id, c.name, c.country
) r
WHERE r.cents > (SELECT AVG(x.cents)
                 FROM (SELECT c2.country, SUM(i2.amount_cents) AS cents
                       FROM customers c2
                       JOIN invoices i2 ON i2.customer_id = c2.id
                       WHERE i2.status = 'paid'
                       GROUP BY c2.id, c2.country) x
                 WHERE x.country = r.country)
ORDER BY r.country, r.cents DESC;
