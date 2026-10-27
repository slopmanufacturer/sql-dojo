#!/usr/bin/env python3
"""sql-dojo: run and grade SQL exercises against a seeded SQLite database.

    ./dojo.py list [chapter]
    ./dojo.py run <exercise>
    ./dojo.py verify <exercise>
    ./dojo.py hint <exercise> [--solution]
    ./dojo.py progress
    ./dojo.py shell
    ./dojo.py build [exercise]

<exercise> is either a full reference (04-joins/03-customers-without-invoices)
or a short one (04/03).
"""

import csv
import json
import re
import sqlite3
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXERCISES = ROOT / "exercises"
DATA = ROOT / "data"
STATE = ROOT / ".dojo"
PROGRESS = STATE / "progress.json"

USAGE = __doc__.split("\n\n", 1)[1].rstrip()


class DojoError(Exception):
    pass


@dataclass(frozen=True)
class Exercise:
    path: Path
    chapter: str
    number: str
    slug: str

    @property
    def ref(self):
        return f"{self.chapter}/{self.path.name}"

    @property
    def short(self):
        return f"{self.chapter[:2]}/{self.number}"


def exercises():
    found = []
    for prompt in sorted(EXERCISES.glob("*/*/prompt.md")):
        parent = prompt.parent
        number, _, slug = parent.name.partition("-")
        found.append(Exercise(parent, parent.parent.name, number, slug))
    return found


def resolve(ref):
    ref = ref.strip().strip("/")
    items = exercises()

    for ex in items:
        if ex.ref == ref:
            return ex

    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})", ref)
    if m:
        chapter, number = m.group(1).zfill(2), m.group(2).zfill(2)
        hits = [e for e in items if e.chapter.startswith(chapter + "-") and e.number == number]
        if len(hits) == 1:
            return hits[0]

    hits = [e for e in items if e.ref.startswith(ref) or e.path.name.startswith(ref)]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise DojoError(f"no exercise matches '{ref}'")
    listing = "\n".join(f"  {e.short}  {e.ref}" for e in hits[:12])
    if len(hits) > 12:
        listing += f"\n  ... and {len(hits) - 12} more"
    raise DojoError(f"'{ref}' is ambiguous:\n{listing}")


def connect():
    conn = sqlite3.connect(":memory:")
    conn.executescript((DATA / "schema.sql").read_text())
    conn.executescript((DATA / "seed.sql").read_text())
    return conn


def strip_comments(sql):
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.S)
    return re.sub(r"--[^\n]*", "", sql)


def split_statements(sql):
    parts, buf = [], ""
    for line in sql.splitlines(keepends=True):
        buf += line
        if sqlite3.complete_statement(buf):
            parts.append(buf)
            buf = ""
    if buf.strip():
        parts.append(buf)
    return [p for p in parts if strip_comments(p).strip()]


def one_line(sql):
    for line in strip_comments(sql).splitlines():
        line = " ".join(line.split())
        if line:
            return line if len(line) <= 72 else line[:69] + "..."
    return ""


def execute(conn, sql):
    statements = split_statements(sql)
    if not statements:
        raise DojoError("no SQL statements found")

    cur = conn.cursor()
    result = None
    for statement in statements:
        try:
            cur.execute(statement)
        except sqlite3.Error as exc:
            raise DojoError(f"{exc}\n  in: {one_line(statement)}") from None
        if cur.description:
            result = (tuple(d[0] for d in cur.description), cur.fetchall())

    if result is None:
        raise DojoError("no statement returned rows; end the file with a SELECT")
    return result


def display(value):
    if value is None:
        return "NULL"
    if isinstance(value, float):
        text = f"{value:.6f}".rstrip("0").rstrip(".")
        return "0" if text in ("", "-0") else text
    if isinstance(value, bytes):
        return value.hex()
    return str(value)


def norm_row(row):
    return tuple(display(v).strip() for v in row)


def fmt_row(row):
    return "(" + ", ".join(row) + ")"


def print_table(headers, rows, limit=20):
    cells = [[display(v) for v in row] for row in rows[:limit]]
    widths = [min(len(h), 40) for h in headers]
    for row in cells:
        for i, cell in enumerate(row):
            widths[i] = min(max(widths[i], len(cell)), 40)

    def render(row):
        padded = []
        for i, cell in enumerate(row):
            if len(cell) > 40:
                cell = cell[:37] + "..."
            padded.append(cell.ljust(widths[i]))
        return "  " + "  ".join(padded).rstrip()

    print(render(headers))
    print("  " + "  ".join("-" * w for w in widths))
    for row in cells:
        print(render(row))
    if len(rows) > limit:
        print(f"  ... {len(rows) - limit} more rows")
    print(f"\n{len(rows)} rows, {len(headers)} columns")


def load_expected(ex):
    path = ex.path / "expected.csv"
    if not path.exists():
        raise DojoError(f"missing {path.relative_to(ROOT)}; run ./dojo.py build {ex.short}")
    with path.open(newline="") as f:
        table = list(csv.reader(f))
    if not table:
        raise DojoError(f"{path.relative_to(ROOT)} is empty")
    return table[0], table[1:]


def solution_is_ordered(ex):
    return re.search(r"\border\s+by\b", strip_comments((ex.path / "solution.sql").read_text()), re.I) is not None


def row_diff(exp, got):
    missing = list((Counter(exp) - Counter(got)).elements())[:5]
    extra = list((Counter(got) - Counter(exp)).elements())[:5]
    lines = [f"expected {len(exp)} rows, got {len(got)}"]
    lines += ["  missing: " + fmt_row(r) for r in missing]
    lines += ["  extra:   " + fmt_row(r) for r in extra]
    return "\n".join(lines)


def compare(expected, got, ordered):
    exp_headers, exp_rows = expected
    got_headers, got_rows = got

    if len(got_headers) != len(exp_headers):
        return False, (f"expected {len(exp_headers)} columns ({', '.join(exp_headers)}), "
                       f"got {len(got_headers)} ({', '.join(got_headers)})")

    exp = [norm_row(r) for r in exp_rows]
    got = [norm_row(r) for r in got_rows]

    if exp == got:
        return True, ""

    if not ordered or Counter(exp) != Counter(got):
        return False, row_diff(exp, got)

    for i, (a, b) in enumerate(zip(exp, got), start=1):
        if a != b:
            return False, (f"rows are right but the order is not (row {i})\n"
                           f"  expected: {fmt_row(a)}\n  got:      {fmt_row(b)}")
    return False, row_diff(exp, got)


def load_progress():
    if PROGRESS.exists():
        return json.loads(PROGRESS.read_text())
    return {}


def save_progress(progress):
    STATE.mkdir(exist_ok=True)
    PROGRESS.write_text(json.dumps(progress, indent=2, sort_keys=True) + "\n")


def read(path):
    try:
        return path.read_text()
    except FileNotFoundError:
        raise DojoError(f"missing {path.relative_to(ROOT)}") from None


def cmd_list(ref=None):
    items = exercises()
    if ref:
        chapter = resolve_chapter(ref)
        items = [e for e in items if e.chapter == chapter]
    done = load_progress()
    current = None
    for ex in items:
        if ex.chapter != current:
            current = ex.chapter
            print(("\n" if current != items[0].chapter else "") + current)
        mark = "x" if ex.ref in done else " "
        print(f"  [{mark}] {ex.number}  {ex.slug}")
    total = len(exercises())
    print(f"\n{len(done)}/{total} complete")


def resolve_chapter(ref):
    ref = ref.strip().strip("/")
    chapters = sorted({e.chapter for e in exercises()})
    hits = [c for c in chapters if c == ref or c.startswith(ref.zfill(2) + "-") or c.startswith(ref)]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise DojoError(f"no chapter matches '{ref}'")
    raise DojoError("chapter is ambiguous: " + ", ".join(hits))


def cmd_run(ex):
    sql = read(ex.path / "starter.sql")
    if not strip_comments(sql).strip():
        raise DojoError(f"{ex.path.relative_to(ROOT)}/starter.sql is still empty")
    headers, rows = execute(connect(), sql)
    print_table(headers, rows)


def cmd_verify(ex):
    sql = read(ex.path / "starter.sql")
    if not strip_comments(sql).strip():
        raise DojoError(f"{ex.path.relative_to(ROOT)}/starter.sql is still empty")
    got = execute(connect(), sql)
    ok, message = compare(load_expected(ex), got, solution_is_ordered(ex))
    if not ok:
        print(f"FAIL  {ex.short}  {ex.slug}")
        print(message)
        return 1
    progress = load_progress()
    progress[ex.ref] = "solved"
    save_progress(progress)
    rows, cols = len(got[1]), len(got[0])
    print(f"PASS  {ex.short}  {ex.slug}  ({rows} rows, {cols} cols)")
    return 0


def cmd_hint(ex, show_solution):
    print(read(ex.path / "prompt.md").strip())
    print("\nHints")
    print(read(ex.path / "hints.md").strip())
    if show_solution:
        print("\nSolution")
        print(read(ex.path / "solution.sql").strip())
    else:
        print(f"\nRun ./dojo.py hint {ex.short} --solution to see the answer.")


def cmd_progress():
    items = exercises()
    done = load_progress()
    solved = [e for e in items if e.ref in done]
    print(f"{len(solved)}/{len(items)} complete")

    remaining = [e for e in items if e.ref not in done]
    if not remaining:
        print("\nAll exercises solved.")
        return

    print("\nNext up")
    for ex in remaining[:3]:
        print(f"  {ex.short}  {ex.chapter}  {ex.slug}")
    print(f"\nRun ./dojo.py run {remaining[0].short} to start.")


def cmd_shell():
    STATE.mkdir(exist_ok=True)
    path = STATE / "shell.db"
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    conn.executescript((DATA / "schema.sql").read_text())
    conn.executescript((DATA / "seed.sql").read_text())
    conn.commit()
    conn.close()
    print(f"Opening {path.relative_to(ROOT)} (rebuilt from schema.sql + seed.sql)")
    try:
        subprocess.run(["sqlite3", str(path)], check=False)
    except FileNotFoundError:
        print("sqlite3 binary not found; open the file with any SQLite client.")


def cmd_build(ref=None):
    items = [resolve(ref)] if ref else exercises()
    for ex in items:
        headers, rows = execute(connect(), read(ex.path / "solution.sql"))
        with (ex.path / "expected.csv").open("w", newline="") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(headers)
            for row in rows:
                writer.writerow([display(v) for v in row])
        print(f"{ex.short}  {len(rows):>3} rows  {len(headers)} cols  {ex.slug}")
    print(f"\n{len(items)} {'exercise' if len(items) == 1 else 'exercises'} rebuilt")


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print("usage: ./dojo.py <command> [args]\n")
        print(USAGE)
        return 0

    command, args = argv[0], argv[1:]

    try:
        if command == "list":
            cmd_list(args[0] if args else None)
        elif command in ("run", "verify", "hint", "build"):
            if command == "build" and not args:
                cmd_build()
                return 0
            if not args:
                raise DojoError(f"usage: ./dojo.py {command} <exercise>")
            ex = resolve(args[0])
            if command == "run":
                cmd_run(ex)
            elif command == "verify":
                return cmd_verify(ex)
            elif command == "hint":
                cmd_hint(ex, "--solution" in args)
            else:
                cmd_build(ex.ref)
        elif command == "progress":
            cmd_progress()
        elif command == "shell":
            cmd_shell()
        else:
            raise DojoError(f"unknown command '{command}'\n\n{USAGE}")
    except DojoError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
