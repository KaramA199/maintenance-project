# Legacy Class and Module Responsibilities
Task: #11 | Owner: Abdulwahab Najib | Status: draft | Date: 16/11

## Report summary

The legacy application is procedural: library.py contains five top-level functions and defines no classes. main() owns the command-line menu, reads user input, opens the database through setup(), dispatches operations and closes the connection on the Exit choice. setup() creates the SQLite schema and inserts missing seed records. search_books() queries titles and authors, prints results and returns database rows. borrow() validates the member, book and active-loan limit, calculates the due timestamp, records the loan and changes availability. return_book() locates an active loan, calculates any whole-day overdue fine, updates the loan and book, and prints the result. The operation functions receive the same SQLite connection from main(). Business decisions, SQL and console output are combined inside those functions; no separate model, service or repository classes exist. The responsibility table therefore describes the actual module and functions rather than inventing classes for the current system.

## Details

### Scope and verification

- Source reference: unchanged `library.py` at revision `abd4b09`.
- AST inspection confirmed the function names and ranges below; there are no class definitions in the source.
- All callers were traced: the script guard calls main(); main() calls setup(), search_books(), borrow() and return_book(). The operation functions do not call one another.
- This is a draft for Abdulwahab's review and a separate task PR; no report section or task-row completion mark has been changed.

### Table 3: class/module responsibility table

| Class / module / function | Responsibilities | Inputs / outputs and notes | Code location |
|---|---|---|---|
| library.py (module) | Houses the CLI, business rules, persistence operations and DB filename | Application-defined classes: none; DB is the relative string library.db | Entire file; imports lines 2–3, DB line 4 |
| setup() | Connect to SQLite; create tables; seed missing members/books; commit initialization | No arguments; returns sqlite3.Connection; does not close it | Lines 5–59 |
| main() | Display menu; read choices and identifiers; convert book IDs to int; dispatch operations; close connection on choice 4 | No arguments; implicit None return; owns the normal CLI connection lifetime | Lines 182–212 |
| search_books(db, text) | Search title or author using parameterized LIKE; print each matching row | Returns fetched list of (id, title, author, available) tuples; [] when no matches | Lines 60–75 |
| borrow(db, member_id, book_id) | Validate member existence/status, book existence/availability and active-loan limit; compute due timestamp; insert loan; mark unavailable; commit; print outcome | True on success; False on business rejection; prints first rejection in check order | Lines 76–142 |
| return_book(db, member_id, book_id) | Find matching active loan; parse due timestamp; calculate fine; mark returned; restore availability; commit; print outcome | True on success; False if no matching active loan; fine printed only when positive | Lines 143–181 |
| Script entry guard | Start CLI only when executed as a script | Importing the module alone does not call setup() or create a DB | Lines 213–214 |

### Standard-library collaborators (not project-defined classes)

| Collaborator | Responsibility in this program | Used by |
|---|---|---|
| sqlite3 module, Connection and Cursor | File connection, SQL execution, row fetching, commits and explicit close | setup(), search_books(), borrow(), return_book(); main() closes the connection |
| datetime class | Obtain local naive timestamps; serialize/parse ISO text; display the due date | borrow(), return_book() |
| timedelta class | Represent the 14-day borrowing duration | borrow() |
| Built-ins input(), print(), int(), bool() | Console interaction, book-ID conversion and availability display | main(); print() also in operation functions; bool() in search_books() |

members, books and loans are database tables, not Python classes. There is no Member, Book, Loan, FineCalculator, DAO or Repository class in the legacy implementation. Validation belongs to borrow() itself; return_book() does not recheck member existence or status. Database and conversion exceptions propagate rather than being converted into the documented True/False business results.

### Connection and data flow

1. The entry guard calls main().
2. main() calls setup() once and retains the returned connection.
3. Each selected operation receives that connection and its console-supplied arguments.
4. Search returns rows, and borrow/return return booleans; main() ignores these return values because the functions print their own results.
5. main() explicitly closes the connection on the normal Exit branch; no try/finally handles abnormal termination.

This table gives Nasser the persistence touchpoints for tasks #16 and #19, and Muayyad the current responsibility boundaries for later refactoring. It does not implement or prescribe those changes.

### Report handoff: section 3.5 (40-word budget)

The system defines no classes. Table 3 lists one module and five functions: setup initializes storage, main handles the menu, search_books retrieves titles/authors, borrow validates and records loans, and return_book calculates fines and restores availability. Operations combine SQL and output.

After the task PR merges, populate the existing Table 3 from the responsibility table, preserving its style; the location column can be folded into Notes.

## Screenshots

None required: the responsibility table is the deliverable. Function ranges were checked directly against the source and its parsed syntax tree.

## Sources

1. Project primary sources: `library.py`, `README.md`, `PLAN.md` and all three existing `docs/00-...`, `01-...`, `02-...` files; task #11 and section 3.5 in `SE431-ProjectReport.docx` (Microsoft Word MCP, 16/11/2026).
2. OpenAI GPT-6.1 Sol, via OpenCode, 16/11/2026: assisted source tracing, AST checks and drafting. Abdulwahab must verify and rewrite the draft before submission under PLAN.md's authorship rule.
