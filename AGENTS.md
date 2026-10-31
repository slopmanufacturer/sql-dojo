# AGENTS.md

## What this is

Sixty graded SQL exercises over one seeded SQLite dataset, driven by a single
stdlib-only script. Each exercise is a directory with a prompt, a starter file,
hints, a reference solution, and the CSV that solution produces. `dojo.py` runs
and grades the learner's query against that CSV.

## Entry points

| Question | Where |
| --- | --- |
| What does an exercise ask? | `exercises/<chapter>/<n>-<slug>/prompt.md` |
| What is graded? | `expected.csv`, generated from `solution.sql` |
| How is a result compared? | `compare()` and `norm_row()` in `dojo.py` |
| How is the data built? | `data/schema.sql` + `data/seed.sql`, in memory, per invocation |
| How is the seed regenerated? | `tools/gen_seed.py` (fixed RNG seed) |
| What is tested? | `tests/test_dojo.py` |

## Invariants

1. **Every `solution.sql` matches its `expected.csv`.** Enforced by
   `test_every_solution_matches_its_expected_csv`.
2. **`expected.csv` is generated, never hand-edited.** `./dojo.py build`
   rewrites it from `solution.sql`; a hand edit will be overwritten and is
   caught by the test.
3. **An unordered reference ignores row order; an ordered one requires it.**
   `solution_is_ordered()` decides. Do not collapse the two branches in
   `compare()` — that was F1 in `AUDIT.md`.
4. **Column names are not graded; the column count is.** The README says so.
5. **`NULL` is not the empty string, and floats compare at six decimals.**
   `display()` owns both rules.
6. **Every exercise has five files**: `prompt.md`, `starter.sql`, `hints.md`,
   `solution.sql`, `expected.csv`.
7. **The seed is deterministic.** `tools/gen_seed.py` uses `random.Random(20241026)`;
   re-running it must produce a byte-identical `data/seed.sql`.
8. **The database is in memory and rebuilt per command.** A learner's `UPDATE`
   or `DELETE` must never persist.

## Commands

```bash
python3 -m unittest discover -s tests -v   # the proof
./dojo.py list                             # exercises and progress
./dojo.py build                            # regenerate every expected.csv
./dojo.py verify 04/03                     # grade one exercise
python3 tools/gen_seed.py                  # regenerate data/seed.sql
```

The one command that proves the work: `python3 -m unittest discover -s tests -v`.

## Sharp edges

- **`compare()` has two order branches.** `exp == got` first, then the multiset
  check, then `if not ordered: return True`. Reordering those silently makes
  unsorted exercises order-sensitive again.
- **`norm_row()` strips the display string.** `" a "` and `"a"` compare equal.
  That is deliberate for CSV round-tripping.
- **`display()` rounds floats at six decimals before stripping zeros**, so
  `1.0000001` equals `1`. Integer-valued floats print without a decimal point.
- **`split_statements()` uses `sqlite3.complete_statement`**, so a statement
  containing a semicolon inside a string literal still splits correctly. Do not
  replace it with `split(";")`.
- **`execute()` returns the last statement that produced rows.** A file ending
  in `UPDATE` fails with "no statement returned rows"; the learner needs a
  trailing `SELECT`.
- **Progress lives in `.dojo/progress.json`** (gitignored). Tests must not write
  it.
- **CI runs 3.8.** No `match`, no `X | Y` annotations, no `removeprefix`.
- **The README's chapter table is a claim.** `test_the_readme_count_is_the_real_count`
  pins the total; per-chapter counts are not pinned.

## Definition of done

- [ ] `python3 -m unittest discover -s tests -v` passes.
- [ ] A new or edited exercise has all five files and a rebuilt `expected.csv`.
- [ ] `./dojo.py build` leaves no diff after your change.
- [ ] The README chapter table still matches the directories.

## Do not touch

- `LICENSE`.
- `data/seed.sql` by hand — regenerate it.
- The exercise numbering: refs like `04/03` are derived from directory names.
- `expected.csv` ordering for ordered references; the grader compares sequences.
