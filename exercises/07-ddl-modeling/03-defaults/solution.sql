CREATE TABLE tickets (
    id       INTEGER PRIMARY KEY,
    subject  TEXT    NOT NULL,
    priority TEXT    NOT NULL DEFAULT 'normal',
    is_open  INTEGER NOT NULL DEFAULT 1
);

INSERT INTO tickets (subject) VALUES ('Login fails'), ('Export is slow');
INSERT INTO tickets (subject, priority, is_open) VALUES ('Data loss', 'urgent', 0);

SELECT id, subject, priority, is_open
FROM tickets
ORDER BY id;
