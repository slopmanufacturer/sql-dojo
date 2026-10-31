# Audit — 2026-10-31

Scope: `dojo.py`, `tools/gen_seed.py`, all 60 exercises, `data/`, README.
Baseline before any change:

```
$ ./dojo.py build
60 exercises rebuilt
$ git status --short
(empty)
$ ./dojo.py list | head -3
01-select-basics
  [ ] 01  all-customers
```

No tests, no CI, no `AGENTS.md`.

| # | Finding | Severity | Status |
| --- | --- | --- | --- |
| F1 | An unordered reference still grades by row order | Low | fixed, `test_unordered_reference_ignores_the_order` |
| F2 | Nothing tested that the 60 solutions agree with their `expected.csv` | Medium | fixed, `test_every_solution_matches_its_expected_csv` |
| F3 | No CI | Medium | fixed |
| F4 | No `AGENTS.md` | Low | fixed |

## F1 — Unordered references are graded by order (Low, latent)

**Claim:** "If the reference solution sorts, your rows must be in the same
order" — the converse, that an unsorted reference does not care about order,
is the whole point of `solution_is_ordered()`.
**Evidence:** `compare()` ran
`if not ordered or Counter(exp) != Counter(got): return False`. When `ordered`
is false that branch always fails, so a correct answer in a different order is
rejected with the confusing `expected 2 rows, got 2`. Reproduced directly:

```
$ python3 -m unittest tests.test_dojo.CompareTest.test_unordered_reference_ignores_the_order
AssertionError: False is not true : expected 2 rows, got 2
```

**Cause:** one `or` where two separate branches were needed.
**Fix:** compare the multisets first, pass when the reference is unordered, and
only walk the rows when it sorts.
**Status:** fixed. `test_unordered_reference_ignores_the_order` fails on the old
code and passes on the new one. **Latent:** the five references without
`ORDER BY` are all single-row aggregates, so no current exercise could expose
it. The next multi-row unsorted exercise would have.

## F2 — Nothing checked that the exercises are correct (Medium)

Sixty `expected.csv` files are generated from `solution.sql`, and nothing
compared them. A wrong solution, a stale CSV, or a renamed column could sit in
`main` indefinitely; the CLI only grades the learner, never the exercise.
**Fix:** `tests/test_dojo.py` runs every `solution.sql` against a fresh
in-memory database and compares it to `expected.csv`, plus a structural check
that every exercise has its five files and a count check against the README.
**Status:** fixed, `test_every_solution_matches_its_expected_csv`.

## F3 — No CI (Medium)

**Fix:** `.github/workflows/checks.yml` runs the tests and `./dojo.py list` on
Python 3.8, 3.11, and 3.13. The 3.8 job is also the proof for the README's
"Python 3.8 or newer" claim, which was previously untested.

## F4 — No AGENTS.md (Low)

**Status:** fixed.

## Verified, no finding

- 60 exercises; per-chapter counts match the README exactly
  (6, 8, 8, 10, 8, 8, 6, 6).
- `./dojo.py build` regenerates all 60 `expected.csv` with no diff, so the
  committed CSVs are current.
- All 60 reference solutions pass their own grader (checked by copying each
  `solution.sql` over `starter.sql` and running `verify`, then restoring).
- Dataset row counts match the README: `plans` 5, `customers` 40, `users` 122,
  `invoices` 277, `events` 577.
- `tools/gen_seed.py` is deterministic: `sha256sum data/seed.sql` is unchanged
  after a re-run, and the file is byte-identical.
- "Every `run` and `verify` starts from a fresh copy": `connect()` builds an
  in-memory database from `schema.sql` and `seed.sql` on every invocation, so a
  learner's `UPDATE` or `DELETE` cannot persist.
- Grading rules are now pinned by tests: column names are not graded, the
  column count is, `NULL` is not the empty string, and floats compare at six
  decimal places.

## Not changed

`norm_row()` strips the displayed value, so a string with leading or trailing
spaces compares equal to one without. That is deliberate for CSV round-tripping
and no exercise depends on the distinction; changing it would be a behaviour
change with no bug behind it.
