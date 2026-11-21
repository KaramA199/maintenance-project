# Phase 2: Maintenance Request Incorporation

Milestone: Commit 03, "03 - Maintenance Request incorporation". It marks the end of Phase 2. Both maintenance requests were merged into `main` through their own pull requests, after Commit 02 and after the behavior tests (task 23) existed.

For each request, the project description asks for the maintenance classification, the impact analysis (affected components and database tables), the proposed design, and the implementation (bonus).

| Request | Tasks | Document | Classification | Impact | Design and implementation | Report section |
|---|---|---|---|---|---|---|
| MR-01: multiple copies of each book | 16–18 | [mr01-multiple-copies.md](mr01-multiple-copies.md) | Perfective; an enhancement that modifies requirement 3 | 4 functions, 1 table (`books`); Table 5 | `books.available` counts copies on the shelf, new column `total_copies`; old databases are migrated | 4.1, Table 5 |
| MR-02: replace the database implementation | 19–21 | [mr02-database-replacement.md](mr02-database-replacement.md) | Adaptive; an enhancement that changes the implementation, not the requirements | all 5 functions, all 3 tables, 17 SQL statements; Table 6 | data-access layer `storage.py` with a JSON store (default) and the SQLite store (fallback); `library.py` has no SQL left | 4.2, Table 6 |

Verification:
- The behavior tests (`python -m unittest discover -s tests -v`, task 23) pass 12 of 12 on `main` after both requests.
- Test 07 was updated for MR-01, because that request deliberately changes requirement 3. Details are in [`../phase3/behavior-tests.md`](../phase3/behavior-tests.md).
- A scripted before-and-after scenario gave identical output on the old code and on both MR-02 stores, apart from the intended MR-01 changes.

Code at this milestone: `library.py` (business logic, menu) and `storage.py` (data access). Phase 3 refactoring (tasks 24–27) starts from here. "Direct DB access" is already solved by MR-02, so the refactorings should target the other smells in [`../phase1/code-smells.md`](../phase1/code-smells.md).

Open team decision: whether a JSON file store is acceptable as the new database for MR-02, or whether the instructor expects a DBMS. A DBMS would be one more class in `storage.py`, with no change to `library.py`.
