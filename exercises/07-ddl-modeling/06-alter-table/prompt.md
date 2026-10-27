# Alter a table

Create a `surveys` table with `id` (integer primary key), `customer_id` (required, references `customers`), and `score` (required integer). Insert scores 9 and 7 for customers 1 and 2, add a nullable `comment` column, set `comment = 'Promoter'` for scores of 9 or more, then return `id`, `customer_id`, `score`, `comment` ordered by `id`.

Expected: 2 rows, 4 columns.
