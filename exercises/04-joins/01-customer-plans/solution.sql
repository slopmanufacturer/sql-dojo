SELECT c.name, p.name AS plan
FROM customers c
JOIN plans p ON p.id = c.plan_id
ORDER BY c.name;
