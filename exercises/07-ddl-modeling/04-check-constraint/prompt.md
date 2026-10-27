# Check constraint

Create a `reviews` table with `id` (integer primary key), `customer_id` (required, references `customers`), `rating` (required, must be between 1 and 5), and nullable `comment`. Insert two valid reviews, then return `id`, `customer_id`, `rating`, `comment` ordered by `id`.

Expected: 2 rows, 4 columns.
