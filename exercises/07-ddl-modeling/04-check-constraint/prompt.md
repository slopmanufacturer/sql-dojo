# Check constraint

Create a `reviews` table: `id` (integer primary key), `customer_id` (required, references `customers`), `rating` (required, 1 to 5), and a nullable `comment`. Insert two valid reviews, then return `id`, `customer_id`, `rating`, `comment` ordered by `id`.

Expected: 2 rows, 4 columns.
