SELECT name, monthly_price_cents, max_seats
FROM plans
ORDER BY monthly_price_cents DESC, name;
