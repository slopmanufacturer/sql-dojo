SELECT p.name AS plan,
       c.country,
       COUNT(cu.id) AS customers
FROM plans p
CROSS JOIN (SELECT DISTINCT country FROM customers) c
LEFT JOIN customers cu ON cu.plan_id = p.id
                     AND cu.country = c.country
GROUP BY p.id, p.name, c.country
ORDER BY plan, c.country;
