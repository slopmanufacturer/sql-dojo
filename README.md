# sql-dojo

Sixty SQL exercises on a seeded SQLite database. Every exercise runs against real
data and grades itself, so you find out whether your answer is right instead of
flipping to a solutions page.

Python 3.8 or newer. No dependencies, no database server, no setup.

## Quickstart

```console
$ ./dojo.py list
$ ./dojo.py run 04/03
$ ./dojo.py verify 04/03
```

Write your query in the exercise's `starter.sql`, then run it. Here is a real
session for `04/03` (customers without invoices), starting from an inner join:

```console
$ ./dojo.py run 04/03
  name  country
  ----  -------

0 rows, 2 columns

$ ./dojo.py verify 04/03
FAIL  04/03  customers-without-invoices
expected 6 rows, got 0
  missing: (Anchor Insurance, ES)
  missing: (Blue Harbor, US)
  missing: (Harborline Shipping, BR)
  missing: (Keystone Architecture, GB)
  missing: (Lumen Optics, US)

$ ./dojo.py verify 04/03
PASS  04/03  customers-without-invoices  (6 rows, 2 cols)
```

`./dojo.py hint 04/03` prints the hints, and `--solution` prints the answer.

## What's in it

| Chapter | Exercises | Covers |
| --- | --- | --- |
| `01-select-basics` | 6 | projection, aliases, `DISTINCT`, arithmetic, `LIMIT` |
| `02-filtering-sorting` | 8 | `WHERE`, `IN`, `LIKE`, `NULL`, `BETWEEN`, `CASE`, multi-key sorts |
| `03-aggregates` | 8 | `COUNT`, `SUM`, `AVG`, `GROUP BY`, `HAVING`, `COUNT(DISTINCT)` |
| `04-joins` | 10 | inner, left, anti, self, and cross joins, join aggregates |
| `05-subqueries-ctes` | 8 | scalar and correlated subqueries, `EXISTS`, CTEs, median |
| `06-window-functions` | 8 | `ROW_NUMBER`, `RANK`, `NTILE`, `LAG`/`LEAD`, running totals |
| `07-ddl-modeling` | 6 | `CREATE TABLE`, keys, defaults, `CHECK`, `ALTER`, `UPDATE` |
| `08-analytics` | 6 | churn, MRR, ARPU, funnels, top-N per group, dormancy |

## How grading works

- Your result set is compared to `expected.csv`: same number of columns, same rows.
- Column names are not graded, only the number of columns and the values.
- If the reference solution sorts, your rows must be in the same order.
- Numbers compare at six decimal places. `NULL` is distinct from an empty string.
- Every `run` and `verify` starts from a fresh copy of the data, so you cannot
  corrupt the database with an `UPDATE` or `DELETE`.

Exercises are numbered within their chapter. `04/03` and
`04-joins/03-customers-without-invoices` refer to the same exercise.

## Commands

```console
./dojo.py list [chapter]      show exercises and what you have solved
./dojo.py run <exercise>      run starter.sql and print the result
./dojo.py verify <exercise>   grade starter.sql against expected.csv
./dojo.py hint <exercise>     show hints (add --solution for the answer)
./dojo.py progress            what is left
./dojo.py shell               open a scratch copy in the sqlite3 CLI, if installed
./dojo.py build [exercise]    regenerate expected.csv from solution.sql
```

Progress is stored in `.dojo/progress.json`, which is gitignored.

## The dataset

A fictional B2B SaaS company, January 2024 through June 2025.

| Table | Rows | What |
| --- | --- | --- |
| `plans` | 5 | plan name, monthly price in cents, seat limit |
| `customers` | 40 | company, country, signup date, plan, churn date |
| `users` | 122 | people at each customer, with a role |
| `invoices` | 277 | monthly invoices with an amount and status |
| `events` | 577 | product events with a timestamp |

The seed is deterministic. `tools/gen_seed.py` regenerates `data/seed.sql`, and
running it twice produces the same file.

## Editing exercises

Each exercise is a directory:

```
exercises/04-joins/03-customers-without-invoices/
├── prompt.md       the question
├── starter.sql     what you edit
├── hints.md        hints
├── solution.sql    the reference answer
└── expected.csv    generated from solution.sql
```

`./dojo.py build <exercise>` regenerates `expected.csv` from `solution.sql`. Run
it after changing a solution, and run `./dojo.py verify <exercise>` with the
solution pasted into `starter.sql` to confirm the pair still agrees.
