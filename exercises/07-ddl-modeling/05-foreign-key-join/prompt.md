# Foreign key and join

Create an `api_keys` table with `id` (integer primary key), `customer_id` (required, references `customers`), `label` (required text), and `created_at` (required text). Insert three keys for customers 1 and 3, then return `label` and the customer `name`, ordered by `label`.

Expected: 3 rows, 2 columns.
