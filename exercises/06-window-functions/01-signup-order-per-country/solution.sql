SELECT country,
       name,
       signup_at,
       ROW_NUMBER() OVER (PARTITION BY country ORDER BY signup_at) AS n
FROM customers
ORDER BY country, n;
