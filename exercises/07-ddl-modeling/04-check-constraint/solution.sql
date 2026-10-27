CREATE TABLE reviews (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment     TEXT
);

INSERT INTO reviews (customer_id, rating, comment) VALUES
    (1, 5, 'Fast support.'),
    (2, 3, NULL);

SELECT id, customer_id, rating, comment
FROM reviews
ORDER BY id;
