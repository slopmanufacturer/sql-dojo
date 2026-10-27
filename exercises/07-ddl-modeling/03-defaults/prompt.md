# Defaults

Create a `tickets` table with `id` (integer primary key), `subject` (required), `priority` (required, defaults to `'normal'`), and `is_open` (required, defaults to 1). Insert two tickets using only `subject`, and one with all three values (`'Data loss'`, `'urgent'`, 0). Return `id`, `subject`, `priority`, `is_open` ordered by `id`.

Expected: 3 rows, 4 columns.
