# Phase 5: Final Reengineered System and Quality Evaluation

Milestone: Commit 06, "06 - Final reengineered system". It marks the end of the reengineering work. The final clean-up and the to-be architecture (#32) were merged into `main` through pull request #27, after Commit 05. The PNG export of Figure 6 was then committed directly to `main` (`9b74e5e`), by mistake instead of through a pull request. It only adds the image and changes one caption line.

The project description asks for a quality evaluation of the reengineered architecture, based on the problems found in Phase 1, using LOC, the number of functions and classes, cyclomatic complexity, code smells and DB dependencies.

| Task | Document | Deliverable | Report section | Owner |
|---|---|---|---|---|
| #32 | [final-architecture.md](final-architecture.md) | Final clean-up of the code, README "how to run" and "how to run the tests", to-be architecture compared with the as-is one | 7.2, Figure 6 | Muayyad |
| #33 | this index | Commit 06 and the check of the Git history | 8.1, 8.2 (Table 10, Figure 7) | Muayyad |
| #34 | [final-metrics.md](final-metrics.md) | Final measurement with the same tools and settings as the baseline (#14) | 7.2, Table 9 | Abdulwahab |
| #35 | [comparison.md](comparison.md) | Legacy versus reengineered comparison | 7.3 | Abdulwahab |

The final system:
- `library.py`: the menu, the search and the borrow checks, with the rules as named constants.
- `return_service.py`: `ReturnService`, the return and the late fine.
- `storage.py`: the data-access layer from MR-02, a JSON file by default or SQLite with `LMS_BACKEND=sqlite`.
- `tests/`: the 12 behavior tests, which pass at this commit. `tools/metrics.py`: the measuring tool for #34.

How to run the system and the tests: see the [README](../../README.md).

Still open (see [final-architecture.md](final-architecture.md), "Still open"): AP5 (the menu crashes on a non-numeric book ID), and console output inside the business functions (AP1, partly solved).

Diagram for this phase: [`docs/img/phase5/final-architecture.png`](../img/phase5/final-architecture.png) (Figure 6).
