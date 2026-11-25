# Before/After Comparison and Quality Evaluation
Task: #35 | Owner: Abdulwahab | Status: draft | Date: 25/11

## Report summary

The reengineered system is larger because it supports multiple copies and keeps two storage backends. Average cyclomatic complexity fell from 3.8 to 2.4, and borrow() dropped from 6 to 4 after its checks were extracted. The peak rose from 6 to 7 in JSON initialization, while main() stayed at 6.

Direct database coupling fell: all 20 SQL call sites are in the SQLite adapter, whereas 17 were spread across four legacy functions. Neither application module issues SQL. JSON is the default; SQLite remains for fallback and initial data migration.

Four of the eight original smell findings were resolved and four were partly addressed. All 12 behavior tests passed. Business operations still print messages, and a non-numeric book ID still crashes the menu. The design is easier to change where borrowing and storage meet, but console separation and startup remain maintenance priorities.

## Details

### Table 9: Before/after quality metrics

| Metric | Legacy: Commit 01 (`02366ff`) | Reengineered: Commit 06 (`ec8b191`) | Change |
|---|---|---|---|
| Physical / source / logical LOC | 214 / 170 / 99 | 438 / 299 / 245 | +224 / +129 / +146 |
| Functions, including methods | 5 | 37 | +32 |
| Classes | 0 | 3 | +3 |
| Cyclomatic complexity | Mean 3.8 (A); peak 6 (B), `main()` and `borrow()` | Mean 2.4 (A); peak 7 (B), `JsonStorage.__init__()` | Mean −1.4; peak +1 |
| Code smells | 8 Phase 1 findings | 4 of 8 still partly present | 4 resolved |
| DB dependencies | 17 static SQL call sites; 4/5 functions touch SQLite directly | 20 static SQL call sites; 9/37 functions or methods touch SQLite directly, all in `SqliteStorage` | +3 sites; no direct DB calls outside the adapter |

### Checks against Phase 1 problems

| Problem | What changed and what remains |
|---|---|
| AP1 — Mixed responsibilities | Persistence moved out of application code, and the fine calculation can be tested separately. Borrow checks and returns still print, so presentation and business behavior are only partly separated. |
| AP2 — No data-access layer | The application uses the same storage methods with either backend. More SQL sites reflect the retained SQLite backend, including migration and export, rather than wider SQL coupling. |
| AP3 — One availability flag per title | MR-01 added copy counts. The SQLite schema still does not declare foreign keys, so the copy model improvement is not a general integrity fix. |
| AP4 — Hard-coded configuration | Rule values are named and the backend is selectable via `LMS_BACKEND`. The default data paths still depend on the working directory. |
| AP5 — Fragile control flow | ID prompting is centralized in `read_ids()`, but `int()` can still raise `ValueError`, and the menu closes the store only on normal exit. |
| AP6 — Hard to test | The 12 automated behavior tests pass, and fine calculation accepts explicit dates. Borrowing and returning still use the current clock for their timestamps. |

Following the course's before/after evaluation (p. 276), these figures support improved maintainability in borrowing and persistence, not a blanket quality improvement. The average covers 40 Radon blocks instead of five, so it does not show that every routine became simpler; cohesion and performance were not measured.

## Screenshots

No screenshots; Table 9 contains the comparison.

## Sources

- [Course slides](../reference/maintenance-course.pdf), PDF p. 276 (before/after refactoring evaluation).
- [Legacy baseline (#14)](../phase1/baseline-metrics.md), [final measurement (#34)](final-metrics.md) and [Phase 1 problems (#13)](../phase1/code-smells.md).
- [Final architecture (#32)](final-architecture.md).
- OpenAI GPT-6.2 Sol (OpenCode): assisted with comparison and drafting.
