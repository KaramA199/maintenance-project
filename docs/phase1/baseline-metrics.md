# Baseline Metrics of the Legacy System
Task: #14 | Owner: Nasser Ali Atef | Status: draft | Date: 18/11

## Report summary

We measured the legacy code before any change to have a baseline for the final comparison. The work was all about the unchanged library.py from Commit 01. The tools are radon 6.0.1 and tools/metrics.py, and the metrics follow Table 4.3 of the course. The size of the code is 214 physical lines (all lines including the blank lines), 170 source lines (all lines excluding the blank lines) and 99 logical lines, which count statements rather than physical lines. The structure of library.py is 5 functions, 0 classes and 1 global variable. The highest cyclomatic complexity is 6, in main() and borrow(), the lowest is 1, in setup(), and the average is 3.8. There are 17 SQL statements scattered across 4 of the 5 functions, with no separate data-access layer, which will make replacing the database difficult. Abdulwahab now needs to use the same tools and settings for the final measurement to ensure a fair judgment.

## Details

### What was measured

| Item | Value |
|---|---|
| File | `library.py` (single module) |
| Revision | commit `b3ed8d3` on `main`; file unchanged since `02366ff` (Commit 01) |
| File hash (`git hash-object library.py`) | `6970928538632438a4cda2cceeac77b2a44d6aee` |
| Environment | Windows 11, Python 3.14.3, SQLite 3.50.4 |
| Date | 18/11/2026, before any change to `library.py` |

### Tool and settings (reuse exactly for task #34)

| Tool | Version | Command | What it gives |
|---|---|---|---|
| radon | 6.0.1 (`python -m pip install radon==6.0.1`) | `python -m radon raw -s library.py` | LOC, LLOC, SLOC, blank and comment lines |
| radon | 6.0.1 | `python -m radon cc -s -a --total-average --show-closures library.py` | cyclomatic complexity per function and the average |
| radon | 6.0.1 | `python -m radon hal library.py` and `python -m radon hal -f library.py` | Halstead metrics, whole file and per function |
| radon | 6.0.1 | `python -m radon mi -s library.py` | maintainability index (extra, see note) |
| `tools/metrics.py` | in this repo | `python tools/metrics.py library.py` | functions, classes, globals, fan-in/fan-out, Henry–Kafura, DB touchpoints, console I/O |

All radon settings are left at their defaults; no files are excluded. For the final system, pass every project `.py` file (not the tests) to both tools in the same way.

### Table 9: Legacy System column

| Metric | Legacy system | How it is counted |
|---|---|---|
| Physical lines (LOC) | 214 | radon `raw`, all lines including blanks |
| Source lines (SLOC) | 170 | radon `raw`, non-blank lines |
| Logical lines (LLOC) | 99 | radon `raw`; closest to the course's "lines of executable code" |
| Comment lines | 0 | radon `raw` |
| Functions | 5 | `tools/metrics.py` |
| Classes | 0 | `tools/metrics.py` |
| Global variables | 1 (`DB`) | `tools/metrics.py` |
| Cyclomatic complexity, average | 3.8 (rank A) | radon `cc` |
| Cyclomatic complexity, highest | 6 (`borrow`, `main`, rank B) | radon `cc` |
| SQL statements in code | 17 | `tools/metrics.py` (`execute` calls) |
| Functions that access the database directly | 4 of 5 | `tools/metrics.py` |
| Functions besides `main()` that print or read input | 3 of 4 | `tools/metrics.py` |
| Halstead volume / effort (whole file) | 257.3 / 1142.8 | radon `hal` |
| Code smells | see task #13 | `docs/phase1/code-smells.md` |

### Per-function results

| Function | Lines | CC | Fan-in | Fan-out | Henry–Kafura (fan-in × fan-out) | DB calls | print/input calls |
|---|---|---|---|---|---|---|---|
| `setup()` | 5–59 | 1 | 1 | 0 | 0 | 11 (connect, 8 SQL, 2 commits) | 0 |
| `search_books()` | 60–75 | 2 | 1 | 0 | 0 | 1 | 1 |
| `borrow()` | 76–142 | 6 | 1 | 0 | 0 | 6 (5 SQL, 1 commit) | 6 |
| `return_book()` | 143–181 | 4 | 1 | 0 | 0 | 4 (3 SQL, 1 commit) | 3 |
| `main()` | 182–212 | 6 | 0 | 4 | 0 | 0 (closes the connection) | menu I/O |

Where the complexity comes from:
- `borrow()` = 1 + five `if` checks: member missing, member inactive, book missing, book unavailable, limit reached.
- `main()` = 1 + the `while` loop + four menu branches.
- `return_book()` = 1 + the missing-loan check + the `late > 0` expression + the fine check.
- `search_books()` = 1 + the result loop.

All Henry–Kafura values are 0. The call structure is flat: `main()` calls the other four, and they call no project functions. So information flow between functions is not where the complexity sits. The complexity sits inside `borrow()`, and in the way every operation goes to SQLite on its own.

### Observations for later tasks

- Every business operation opens its own cursor and writes raw SQL against `library.db`, and no data-access layer exists. This matters for MR-02 (database replacement, #19–#21): 17 statements in 4 functions would need to change.
- `books.available` is a single 0/1 flag, set in `borrow()` and `return_book()`. This matters for MR-01 (multiple copies, #16–#18).
- `borrow()` has the highest complexity and the most output calls. This matches the course project's choice of `borrow()` as the refactoring target (#24).
- There are no comments and no automated tests. Muayyad's tests (#23) are the safety net before any change.

### Report handoff: section 7.1 (50-word budget)

Both versions are measured with radon 6.0.1 (raw, cc and hal, default settings) and the project script tools/metrics.py. These count lines, functions, classes, global variables, cyclomatic complexity, fan-in and fan-out, and SQL statements. The legacy figures, taken before any code change, form the Legacy System column of Table 9.

### Note on the maintainability index

radon also reports a maintainability index of 37.44 (rank A) for `library.py`. The course does not cover this metric, so it is reported only for information and is not in Table 9. The formula is described in the radon documentation.

### Raw tool output

<details>
<summary>radon raw, cc, hal, mi and tools/metrics.py on library.py</summary>

```
$ python -m radon raw -s library.py
    LOC: 214
    LLOC: 99
    SLOC: 170
    Comments: 0
    Single comments: 0
    Multi: 0
    Blank: 44

$ python -m radon cc -s -a --total-average --show-closures library.py
library.py
    F 182:0 main - B (6)
    F 76:0 borrow - B (6)
    F 143:0 return_book - A (4)
    F 60:0 search_books - A (2)
    F 5:0 setup - A (1)
5 blocks (classes, functions, methods) analyzed.
Average complexity: A (3.8)

$ python -m radon hal library.py
    h1: 7  h2: 26  N1: 18  N2: 33
    vocabulary: 33  length: 51
    volume: 257.26  difficulty: 4.44  effort: 1142.85

$ python -m radon mi -s library.py
library.py - A (37.44)

$ python tools/metrics.py library.py
Functions: 5   Classes: 0   Global variables: 1 ['library.py:DB']
SQL statements executed: 17
Functions touching the database: 4 of 5
Functions doing console I/O besides main(): 3

function                 fan-in fan-out  HK fan-in*fan-out  DB calls  print/input
setup                         1       0                  0        11            0
search_books                  1       0                  0         1            1
borrow                        1       0                  0         6            6
return_book                   1       0                  0         4            3
main                          0       4                  0         0            0
```

</details>

## Screenshots

To add: a screenshot of the commands above run in a terminal, saved as `docs/img/phase1/baseline-metrics.png`.

## Sources

1. Tripathy, P. and Naik, K. *Software Evolution and Maintenance: A Practitioner's Approach*, course slides in `docs/reference/maintenance-course.pdf`: Section 4.6.7 Program Metrics, PDF p. 167; Henry–Kafura metric, p. 168; cyclomatic complexity, p. 169 and pp. 241–242; Table 4.3 Commonly Used Software Metrics, p. 170; measuring before and after refactoring, p. 276.
2. radon 6.0.1 documentation, https://radon.readthedocs.io/ (raw metrics, cyclomatic complexity ranks, Halstead metrics, maintainability index).
3. Project files: `library.py`, `PLAN.md`, `docs/01-project-charter.md`, `docs/phase1/class-responsibilities.md`.
4. Claude (Anthropic, Claude Code), 18/11/2026: ran the tools, wrote `tools/metrics.py` and drafted the Details section. Nasser went through each section with it, checked the numbers against `library.py` and wrote the Report summary.
