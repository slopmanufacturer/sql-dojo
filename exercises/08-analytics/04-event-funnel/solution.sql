SELECT
    (SELECT COUNT(DISTINCT customer_id) FROM events WHERE name = 'login') AS logged_in,
    (SELECT COUNT(DISTINCT customer_id) FROM events WHERE name = 'dashboard_view') AS viewed_dashboard,
    (SELECT COUNT(DISTINCT customer_id) FROM events WHERE name = 'export') AS exported;
