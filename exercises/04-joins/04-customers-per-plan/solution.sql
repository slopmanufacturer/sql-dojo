SELECT p.name, COUNT(c.id) AS customers
FROM plans p
LEFT JOIN customers c ON c.plan_id = p.id
GROUP BY p.id, p.name
ORDER BY customers DESC, p.name;
