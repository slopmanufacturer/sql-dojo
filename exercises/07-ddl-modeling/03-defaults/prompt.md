# Defaults

Create a `tickets` table: `id` (integer primary key), `subject` (required), `priority` (required, default `'normal'`), and `is_open` (required, default 1). Insert two tickets with only `subject`, plus one with `'Data loss'`, `'urgent'`, 0. Return `id`, `subject`, `priority`, `is_open` ordered by `id`.

Expected: 3 rows, 4 columns.
