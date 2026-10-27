# Foreign key and join

Create an `api_keys` table: `id` (integer primary key), `customer_id` (required, references `customers`), `label` (required text), and `created_at` (required text). Insert two keys for customer 1 and one for customer 3, then return `label` and the customer `name`, ordered by `label`.

Expected: 3 rows, 2 columns.
