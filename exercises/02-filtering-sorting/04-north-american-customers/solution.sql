SELECT name, country
FROM customers
WHERE country IN ('US', 'CA')
ORDER BY country, name;
