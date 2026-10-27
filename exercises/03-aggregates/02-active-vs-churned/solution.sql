SELECT COUNT(*) AS total,
       COUNT(churned_at) AS churned,
       COUNT(*) - COUNT(churned_at) AS active
FROM customers;
