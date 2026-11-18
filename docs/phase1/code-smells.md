# Code Smells and Architectural Problems
Task: #13 | Owner: Nasser Ali Atef | Status: draft | Date: 18/11

## Report summary

We looked for code smells in library.py using the course list (Fowler: duplicated code, large class, long method, long parameter list, comments) and for design-level problems, from architecture to control flow and database schema. We found 8 code smells and 6 architectural problems. borrow() is a long method with CC = 6 doing five jobs. Other smells are duplicated code, magic numbers like 3 and 14, poor names and no comments. SQL, business rules and print statements were mixed together, and there was no data-access layer. The database stores availability as one flag per title, so copies of a book cannot be counted. A non-numeric book ID crashes the program, because it must be numeric. Each problem is now linked to the task that fixes it.

## Details

### Method

1. Read every function of `library.py` (commit `b3ed8d3`, unchanged since Commit 01) and compared it with the code-smell examples in the course (p. 272).
2. Checked the design-level entities the course lists as refactoring targets: architecture, global control flow and database schema (p. 273).
3. Used the metrics from task #14 (complexity, length, SQL count) as evidence, and the dependency results from task #12 for coupling.
4. Ran the program once with a non-numeric book ID to confirm the crash in AP5.
5. Linked each finding to the task that will deal with it, so the team can check later that it was fixed.

Counting rule (reuse for task #34): one row per distinct smell. A smell that occurs in several places is one row, with all its locations listed.

### Table 4: code smells

| ID | Smell (course source) | Where | Evidence | Effect | Addressed by |
|---|---|---|---|---|---|
| CS1 | Long Method (p. 272) | `borrow()`, lines 76–142 | 67 lines, cyclomatic complexity 6 (highest), 5 SQL statements, 6 print calls. It does five jobs: validates the member, validates the book, checks the limit, writes the loan and availability, and prints. | Hard to read, test and change. Any change to one rule risks the others. | #24 refactor `borrow()` |
| CS2 | Long Method (p. 272) | `setup()`, lines 5–59 | 55 lines that mix schema creation with seed data | Low risk, because it has no branches. But the schema cannot be reused without the test data. | Refactoring candidate (#25–#27) |
| CS3 | Duplicated Code (p. 272) | `borrow()`, lines 78–106 | The same pattern appears three times: execute a query, `fetchone()`, check, `print`, `return False` | Changing how errors are reported means editing every copy. | #24 |
| CS4 | Duplicated Code (p. 272) | `main()`, lines 198–199 and 203–204; `setup()`, lines 38–56 | Borrow and Return read the member and book ID with identical code. `setup()` repeats five near-identical `INSERT OR IGNORE` calls. | A fix in one copy, such as validating the book ID, is easily missed in the other. | Refactoring candidate (#25–#27) |
| CS5 | Duplicated Code (p. 272) | `borrow()` lines 110, 134; `return_book()` lines 147, 170 | The rule "a loan is active when `returned=0`" and the availability updates are written separately in two functions. | The two functions can drift apart. MR-01 must change both. | #16–#18 (MR-01) |
| CS6 | Magic numbers and strings (Fowler's "Replace Magic Literal", outside the course list) | `borrow()` lines 89, 114, 119; `return_book()` line 162; flags `0`/`1` throughout | Limit `3`, period `14`, status `"ACTIVE"`, availability `0`/`1`, and a fine of 1 per day late that is never named | Business rules are hidden in code. Changing the period or the limit means searching the code. | Refactoring candidate (#25–#27) |
| CS7 | Poor naming (meaningful names, p. 257) | whole file | Cursor `c`; `row[0]`…`row[3]`, `member[1]`, `book[0]` instead of named fields. `member` and `book` hold an ID in `main()` but a database row in `borrow()`. | The reader has to trace the SQL column order to understand a line. | #24, #25–#27 |
| CS8 | No comments or documentation (out-of-date or missing documentation, pp. 254, 270) | whole file | 0 comment lines and 0 docstrings (radon, task #14) | New maintainers must reverse-engineer the rules, which is what Phase 1 had to do. | Covered by Phase 1 documents; docstrings in #32 |

Course smells checked and **not found**:
- Long Parameter List: the most any function takes is three parameters.
- Large Class: there are no classes. The module-level version of this problem is AP1 below.

### Table 4 (continued): architectural problems

| ID | Problem (course level, p. 273) | Where | Evidence | Effect | Addressed by |
|---|---|---|---|---|---|
| AP1 | No separation of concerns (software architecture) | `search_books()`, `borrow()`, `return_book()` | Each function contains SQL, business rules and `print` calls. `main()` ignores every return value because results are printed inside the operations. | The logic cannot be reused, for example by the Equipment system, without its console output. The UI cannot change without touching business code. | #24–#27, #30 |
| AP2 | No data-access layer (software architecture) | 4 of 5 functions | 17 raw SQL statements spread across `setup()`, `search_books()`, `borrow()` and `return_book()`, all bound to `sqlite3` (task #12) | Replacing the database touches almost the whole program. | #19–#21 (MR-02) |
| AP3 | Weak database schema (database schema) | `setup()`, lines 8–34 | `books.available` is one flag per title, so copies cannot be counted. No foreign keys. Nothing stops two active loans for one book except the flag. Dates are stored as text. (Details in task #9.) | Blocks multiple copies. Data integrity depends on the code being correct. | #16–#18 (MR-01), #19–#21 (MR-02) |
| AP4 | Hard-coded configuration | line 4; `borrow()`, `return_book()` | The database path `library.db` is relative to the current folder, so it changes with where the program is started. Business constants are in the code (CS6). | Running from another folder silently creates a new, empty database. | #19–#21 (MR-02) |
| AP5 | Fragile global control flow (global control flow) | `main()`, lines 182–212 | `int(input(...))` at lines 199 and 204 crashes on non-numeric input: the program stopped with `ValueError` at line 199 when we typed `abc`. The connection is closed only on menu choice 4 (no `try`/`finally`). | One typing mistake ends the session with a stack trace. | #24–#27 (keep the same messages for valid input) |
| AP6 | Hard to test, no tests (lack of tests, p. 270) | `borrow()`, `return_book()` | `datetime.now()` is called inside the logic, results are printed rather than returned, and no automated tests exist. | Due dates and fines cannot be tested without waiting or patching the clock. | #23 behavior tests |

### Other observations (not counted as smells)

These are business-rule gaps, passed to Abdulwahab's business-rules work (#8) for confirmation:
- `return_book()` does not check that the member still exists or is active.
- The fine is printed but never stored or charged.
- The fine rate (1 per day) is not stated anywhere in the requirements.

### Totals for Table 9

| Category | Legacy count |
|---|---|
| Code smells (CS) | 8 |
| Architectural problems (AP) | 6 |

### Report handoff: section 3.7 (70-word budget)

Table 4 lists eight code smells and six architectural problems. borrow() is a long method (complexity 6) with duplicated validation blocks. Business values are hard-coded, names are unclear, and there are no comments or tests. User interface, rules and SQL are mixed in the same functions with no data-access layer. Availability is one flag per title, and a non-numeric book ID crashes the program.

## Screenshots

To add: a screenshot of the `ValueError` crash for AP5, saved as `docs/img/phase1/crash-non-numeric-id.png`. To reproduce it, run `python library.py`, choose `2`, enter `S1`, then `abc`.

## Sources

1. Tripathy, P. and Naik, K. *Software Evolution and Maintenance: A Practitioner's Approach*, course slides in `docs/reference/maintenance-course.pdf`: causes of decreased understandability, PDF p. 254; meaningful names, p. 257; causes of technical debt (lack of tests, lack of documentation), p. 270; code smells, p. 272; design-level refactoring entities, p. 273.
2. Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code*, 2nd ed. Addison-Wesley. Chapter 3, "Bad Smells in Code", the smell catalog the course cites on p. 272. For CS6, which is outside the course's list: Fowler, M., "Replace Magic Literal", refactoring catalog, https://refactoring.com/catalog/replaceMagicLiteral.html.
3. Project files: `library.py`, `docs/phase1/database-schema.md` (#9), `docs/phase1/baseline-metrics.md` (#14), `docs/phase1/dependencies.md` (#12).
4. Claude (Anthropic, Claude Code), 18/11/2026: inspected the code, reproduced the crash and drafted the Details section. Nasser went through each section with it, checked the findings against `library.py` and wrote the Report summary.
