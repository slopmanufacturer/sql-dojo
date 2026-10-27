-- Dataset: a small B2B SaaS company, January 2024 through June 2025.
-- Every exercise starts from this schema plus data/seed.sql.

CREATE TABLE plans (
    id                  INTEGER PRIMARY KEY,
    name                TEXT    NOT NULL,
    monthly_price_cents INTEGER NOT NULL,
    max_seats           INTEGER NOT NULL
);

CREATE TABLE customers (
    id         INTEGER PRIMARY KEY,
    name       TEXT    NOT NULL,
    country    TEXT    NOT NULL,   -- ISO 3166-1 alpha-2
    signup_at  TEXT    NOT NULL,   -- YYYY-MM-DD
    plan_id    INTEGER NOT NULL REFERENCES plans(id),
    churned_at TEXT                -- NULL while the account is active
);

CREATE TABLE users (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    email       TEXT    NOT NULL,
    role        TEXT    NOT NULL,  -- owner, admin, member
    created_at  TEXT    NOT NULL
);

CREATE TABLE invoices (
    id           INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(id),
    issued_at    TEXT    NOT NULL,
    amount_cents INTEGER NOT NULL,
    status       TEXT    NOT NULL  -- paid, open, void
);

CREATE TABLE events (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    occurred_at TEXT    NOT NULL,
    name        TEXT    NOT NULL  -- login, dashboard_view, api_call, export, invite_sent, integration_added
);
