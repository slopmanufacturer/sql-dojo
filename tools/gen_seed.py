#!/usr/bin/env python3
"""Regenerate data/seed.sql.

The seed is deterministic: the same script always produces the same file, so
exercise answers stay stable. Run from the repo root:

    python3 tools/gen_seed.py
"""

import random
from datetime import date, timedelta
from pathlib import Path

RNG = random.Random(20241026)
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "seed.sql"

START = date(2024, 1, 1)
END = date(2025, 6, 30)

PLANS = [
    (1, "Starter", 1900, 3),
    (2, "Team", 4900, 10),
    (3, "Business", 14900, 50),
    (4, "Enterprise", 49900, 250),
    (5, "Legacy", 9900, 25),
]
PRICE = {p[0]: p[2] for p in PLANS}

COMPANIES = [
    "Acme Robotics", "Northwind Labs", "Blue Harbor", "Cobalt Systems",
    "Delta Freight", "Ember Analytics", "Fjord Studio", "Granite Works",
    "Helix Bio", "Ironclad Security", "Juniper Retail", "Kestrel Media",
    "Lattice Health", "Meridian Bank", "Nimbus Cloud", "Orbit Logistics",
    "Pinewood Legal", "Quarry Mining", "Redwood Energy", "Sable Fashion",
    "Tidewater Marine", "Umbra Games", "Vertex Manufacturing", "Willow Education",
    "Xenon Research", "Yardstick Consulting", "Zephyr Travel", "Anchor Insurance",
    "Birch & Co", "Copper Kettle", "Driftwood Hotels", "Elm Street Deli",
    "Foundry AI", "Glasswing Design", "Harborline Shipping", "Indigo Textiles",
    "Junction Rail", "Keystone Architecture", "Lumen Optics", "Mosaic Foods",
]

COUNTRIES = ["US"] * 9 + ["DE"] * 5 + ["GB"] * 4 + ["FR"] * 3 + ["NL"] * 3 + \
            ["CA"] * 3 + ["BR"] * 2 + ["IN"] * 3 + ["AU"] * 2 + ["JP"] * 2 + \
            ["SE"] * 2 + ["ES"] * 2

FIRST = ["Ada", "Ben", "Carla", "Dev", "Elena", "Felix", "Gina", "Hugo", "Ines",
         "Jonas", "Kira", "Liam", "Maya", "Nils", "Olga", "Pablo", "Quinn",
         "Rosa", "Sven", "Tara", "Uma", "Viktor", "Wren", "Xavi", "Yara", "Zane"]
LAST = ["Albers", "Bianchi", "Chen", "Dubois", "Eriksen", "Fischer", "Gomez",
        "Hansen", "Ito", "Jansen", "Keller", "Lindqvist", "Moreau", "Novak",
        "Okafor", "Pereira", "Rossi", "Silva", "Tanaka", "Ueda", "Vargas",
        "Weber", "Xu", "Yilmaz", "Zimmerman", "Kowalski"]

EVENT_NAMES = ["login"] * 40 + ["dashboard_view"] * 25 + ["api_call"] * 15 + \
              ["export"] * 8 + ["invite_sent"] * 7 + ["integration_added"] * 5

NO_INVOICE = {3, 17, 28, 35, 39}
NO_EVENTS = {5, 21, 33, 38}


def slug(name):
    keep = [c.lower() if c.isalnum() else "-" for c in name]
    out = "".join(keep)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def month_starts(first, last):
    y, m = first.year, first.month
    while (y, m) <= (last.year, last.month):
        yield date(y, m, 1)
        m += 1
        if m == 13:
            y, m = y + 1, 1


def sql_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, int):
        return str(v)
    return "'" + v.replace("'", "''") + "'"


def emit(table, columns, rows):
    lines = [f"INSERT INTO {table} ({', '.join(columns)}) VALUES"]
    values = ",\n".join("  (" + ", ".join(sql_value(v) for v in r) + ")" for r in rows)
    return lines[0] + "\n" + values + ";\n"


def main():
    plans = PLANS
    customers, users, invoices, events = [], [], [], []

    rng = RNG
    rng.shuffle(COUNTRIES)
    for i, name in enumerate(COMPANIES, start=1):
        country = COUNTRIES[i - 1]
        # Legacy (plan 5) is retired, so new customers only land on plans 1-4.
        plan_id = rng.choices([1, 2, 3, 4], weights=[28, 35, 26, 11])[0]

        if i > 34:
            signup = date(2025, 4, 1) + timedelta(days=rng.randrange(0, 70))
        else:
            signup = START + timedelta(days=rng.randrange(0, 500))

        churned = None
        if i <= 32 and i not in NO_INVOICE and rng.random() < 0.28:
            window = (END - signup).days - 60
            if window > 60:
                churned = signup + timedelta(days=rng.randrange(60, window))

        customers.append((i, name, country, signup.isoformat(), plan_id,
                          churned.isoformat() if churned else None))

        # Users: an owner, sometimes an admin, a few members.
        seats = rng.randrange(2, 5)
        domain = slug(name) + ".example"
        for u in range(seats):
            role = "owner" if u == 0 else ("admin" if u == 1 and seats > 3 else "member")
            first, last = rng.choice(FIRST), rng.choice(LAST)
            email = f"{first.lower()}.{last.lower()}@{domain}"
            created = signup + timedelta(days=rng.randrange(0, 45))
            users.append((len(users) + 1, i, email, role, created.isoformat()))

        # Events: spread across the active window.
        stop = min(churned or END, END)
        if i not in NO_EVENTS:
            for _ in range(rng.randrange(6, 34)):
                span = max((stop - signup).days, 1)
                when = signup + timedelta(days=rng.randrange(0, span + 1))
                events.append((len(events) + 1, i, when.isoformat(), rng.choice(EVENT_NAMES)))

        # Invoices: monthly from the month after signup (or the same month).
        if i in NO_INVOICE:
            continue
        first_month = signup.replace(day=1)
        if rng.random() < 0.45:
            first_month = (first_month + timedelta(days=32)).replace(day=1)
        for month in month_starts(first_month, stop.replace(day=1)):
            day = min(signup.day, 28)
            issued = month.replace(day=day)
            if issued < signup or issued > stop:
                continue
            amount = PRICE[plan_id]
            if rng.random() < 0.07:
                amount = int(amount * 0.85)
            elif rng.random() < 0.03:
                amount = amount * 12
            if issued >= date(2025, 5, 1):
                status = "open" if rng.random() < 0.6 else "paid"
            else:
                status = "void" if rng.random() < 0.05 else "paid"
            invoices.append((len(invoices) + 1, i, issued.isoformat(), amount, status))

    events.sort(key=lambda r: (r[2], r[0]))

    out = [
        "-- Generated by tools/gen_seed.py. Do not edit by hand.\n\n",
        emit("plans", ["id", "name", "monthly_price_cents", "max_seats"], plans),
        "\n",
        emit("customers", ["id", "name", "country", "signup_at", "plan_id", "churned_at"], customers),
        "\n",
        emit("users", ["id", "customer_id", "email", "role", "created_at"], users),
        "\n",
        emit("invoices", ["id", "customer_id", "issued_at", "amount_cents", "status"], invoices),
        "\n",
        emit("events", ["id", "customer_id", "occurred_at", "name"], events),
    ]
    OUT.write_text("".join(out))

    print(f"plans      {len(plans):>5}")
    print(f"customers  {len(customers):>5}")
    print(f"users      {len(users):>5}")
    print(f"invoices   {len(invoices):>5}")
    print(f"events     {len(events):>5}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
