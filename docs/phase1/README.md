# Phase 1: Program Comprehension Analysis

Milestone: Commit 02, "02 - Program comprehension analysis". It marks the end of Phase 1. Tasks #12 to #14 were merged into `main` through pull requests, tasks #7 to #11 were merged from their own branches without a pull request, and the legacy `library.py` was not changed during this phase.

The goal was to understand the legacy Library Management System through program comprehension and reverse engineering before changing it.

| Task | Document | Deliverable (project description) | Report section | Owner |
|---|---|---|---|---|
| #7 | [requirements.md](requirements.md) | Identify/confirm the given requirements from the code base | 3.1, Table 2 | Abdulwahab |
| #8 | [business-rules.md](business-rules.md) | Business rules | 3.2 | Abdulwahab |
| #9 | [database-schema.md](database-schema.md) | Database structure / schema | 3.3, Figure 2 | Abdulwahab |
| #10 | [architecture.md](architecture.md) | Current architecture diagram | 3.4, Figure 3 | Abdulwahab |
| #11 | [class-responsibilities.md](class-responsibilities.md) | Class/module responsibility table | 3.5, Table 3 | Abdulwahab |
| #12 | [dependencies.md](dependencies.md) | Dependency analysis | 3.6, Figure 4 | Nasser |
| #13 | [code-smells.md](code-smells.md) | Code-smell identification | 3.7, Table 4 | Nasser |
| #14 | [baseline-metrics.md](baseline-metrics.md) | Baseline measurements for the Phase 5 comparison | 7.1, Table 9 (Legacy column) | Nasser |

Main findings, used in the later phases:
- The system is one procedural module with five functions and no classes. User interface, business rules and SQL are mixed in the same functions (#10, #11, #13).
- The call graph is flat, but the functions are coupled through the database. 17 SQL statements sit in four of the five functions, with no data-access layer (#12, #14). This is the starting point for MR-02.
- `books.available` is one flag per title, so copies cannot be counted (#9, #13). This is the starting point for MR-01.
- `borrow()` has the highest cyclomatic complexity (6) and is the main refactoring target (#13, #14).

Screenshots for this phase are in [`docs/img/phase1/`](../img/phase1/).
