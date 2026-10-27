CREATE TABLE notes (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    body        TEXT    NOT NULL,
    created_at  TEXT    NOT NULL
);

INSERT INTO notes (customer_id, body, created_at) VALUES
    (1, 'Asked about SSO pricing.', '2025-06-01'),
    (2, 'Renewal call scheduled.', '2025-06-02');

SELECT id, customer_id, body
FROM notes
ORDER BY id;
