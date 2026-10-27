# Dormant customers

An active customer is dormant when they have gone more than 30 days without an event before 2025-06-30. Customers with no events count from their signup date. Return `name`, `last_seen` (the last event, or the signup date if there is none), and `days_since` (whole days), largest gap first.

Expected: 6 rows, 3 columns.
