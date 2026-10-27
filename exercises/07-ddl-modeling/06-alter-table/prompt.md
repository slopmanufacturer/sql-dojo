# Alter a table

Create a `surveys` table: `id` (integer primary key), `customer_id` (required, references `customers`), and `score` (required integer). Insert 9 for customer 1 and 7 for customer 2, add a nullable `comment` column, set `comment = 'Promoter'` for scores of 9 or more, then return `id`, `customer_id`, `score`, `comment` ordered by `id`.

Expected: 2 rows, 4 columns.
