CREATE TABLE api_keys (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    label       TEXT    NOT NULL,
    created_at  TEXT    NOT NULL
);

INSERT INTO api_keys (customer_id, label, created_at) VALUES
    (1, 'ci', '2025-01-10'),
    (1, 'backup', '2025-02-11'),
    (3, 'etl', '2025-03-12');

SELECT k.label, c.name
FROM api_keys k
JOIN customers c ON c.id = k.customer_id
ORDER BY k.label;
