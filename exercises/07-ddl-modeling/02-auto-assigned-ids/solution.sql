CREATE TABLE tags (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO tags (name) VALUES ('billing'), ('security'), ('reporting');

SELECT id, name
FROM tags
ORDER BY id;
