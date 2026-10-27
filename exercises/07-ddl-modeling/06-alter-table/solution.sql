CREATE TABLE surveys (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    score       INTEGER NOT NULL
);

INSERT INTO surveys (customer_id, score) VALUES (1, 9), (2, 7);

ALTER TABLE surveys ADD COLUMN comment TEXT;

UPDATE surveys
SET comment = 'Promoter'
WHERE score >= 9;

SELECT id, customer_id, score, comment
FROM surveys
ORDER BY id;
