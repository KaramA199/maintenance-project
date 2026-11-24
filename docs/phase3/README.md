# Phase 3: Refactoring

Milestone: Commit 04, "04 - Refactor borrowing module". It marks the end of Phase 3. The refactorings were merged into `main` through their own pull request (#25), after Commit 03, and each refactoring is its own commit inside it.

The project description asks to refactor the hard-to-maintain `borrow()` function while preserving externally observable behavior, plus at least two more documented refactorings (long methods, mixed responsibilities, direct DB access, primitive data).

| Task | Document | Deliverable | Report section | Owner |
|---|---|---|---|---|
| #23 | [behavior-tests.md](behavior-tests.md) (code in [`tests/`](../../tests/)) | Behavior-preservation tests, written on the legacy code before any change | 5.1 | Karam |
| #24 | [refactoring-log.md](refactoring-log.md), Refactoring 1 | Decompose `borrow()` (Extract Method), smell CS1 | 5.2, Table 7 | Karam |
| #25 | [refactoring-log.md](refactoring-log.md), Refactoring 2 | Move the return and fine logic into `ReturnService` (Extract Class), smell AP1 | 5.2, Table 7 | Karam |
| #26 | [refactoring-log.md](refactoring-log.md), Refactoring 3 | Named constants and unpacked rows (Replace Magic Literal), smells CS6, CS7 | 5.2, Table 7 | Karam |
| #27 | [refactoring-log.md](refactoring-log.md), Verification; this index | Behavior check after each refactoring, and Commit 04 | 5.3 | Karam; Commit 04 by Muayyad |

Main results, used in the later phases:
- `borrow()` went from 33 lines and cyclomatic complexity 6 to 14 lines and complexity 4. It now only calls `validate_member`, `check_availability`, `check_borrow_limit` and `create_loan`.
- The fine rule is in one method, `ReturnService.calculate_fine()`, which does not touch the database or print anything.
- The rules 3, 14, the fine rate and "ACTIVE" are named constants at the top of `library.py`. They are the values that the Phase 4 design moves into `LibraryRules`.
- "Direct DB access" was already solved by MR-02 (`storage.py`), so `storage.py` did not change in this phase.

Verification: the 12 behavior tests (`python -m unittest discover -s tests -v`) pass after every refactoring, and the menu run with `tests/menu_session.txt` gives the same output as Commit 03 on both the SQLite and the JSON store.

Still open for the final clean-up (#32): CS4 (duplicated input code in `main()`) and AP5 (the menu crashes on a non-numeric book ID), listed in [refactoring-log.md](refactoring-log.md) under "Smells not handled here".

Screenshots for this phase are in [`docs/img/phase3/`](../img/phase3/).
