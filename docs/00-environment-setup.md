# Environment Setup – Legacy LMS

## Requirements

| Item | Value |
|---|---|
| Language | Python 3.8+ (tested with Python 3.14.3 and SQLite 3.50.4 on Windows 11) |
| Database | SQLite via the standard-library `sqlite3` module |
| External dependencies | None (`sqlite3` and `datetime` are built in) |
| Entry point | `library.py` (single file, ~215 lines including blanks) |

## Run

```bash
git clone https://github.com/KaramA199/maintenance-project.git
cd maintenance-project
python library.py
```

Menu: `1` Search, `2` Borrow, `3` Return, `4` Exit.

## Database

- The database is a file, `library.db`, created in the **current working directory** on first run (`DB = "library.db"`). It is git-ignored.
- `setup()` runs on every start. It creates three tables if they do not exist (`members`, `books`, `loans`) and seeds data with `INSERT OR IGNORE`.
- Seed data: members `S1` Ali and `S2` Sara (both `ACTIVE`); books `1` Clean Code, `2` Refactoring, `3` Design Patterns (all available).
- To reset the data, delete `library.db`.
- Schema is documented in the Phase 1 database analysis.

## Smoke test performed (legacy behavior baseline)

Scripted session run on the unchanged code:

| Action | Output |
|---|---|
| Search `refactor` | `2 Refactoring - Martin Fowler Available: True` |
| Borrow S1 / book 1 | `Book borrowed. Due: <today + 14 days>` |
| Borrow S1 / book 1 again | `Book is unavailable` |
| Borrow S9 / book 2 | `Member not found` |
| Return S1 / book 1 | `Book returned` |
| Return S1 / book 1 again | `Active loan not found` |
| Menu choice `9` | `Invalid choice` |

## Notes

- The original code was supplied as plain text with indentation and the `if __name__ == "__main__":` guard stripped. Both were restored in Commit 01; no logic was changed.
- Delete `library.db` before comparing behavior between versions so every run starts from the same seed data.
