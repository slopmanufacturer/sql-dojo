SELECT p.name,
       MIN(c.signup_at) AS first_signup,
       MAX(c.signup_at) AS last_signup
FROM plans p
LEFT JOIN customers c ON c.plan_id = p.id
GROUP BY p.id, p.name
ORDER BY p.name;
