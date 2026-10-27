# Create a notes table

Support notes are shipping next sprint. Create a `notes` table with `id` (integer primary key), `customer_id` (required, references `customers`), `body` (required text), and `created_at` (required text). Insert two rows, then return `id`, `customer_id`, `body` ordered by `id`.

Expected: 2 rows, 3 columns.
