# Final Metrics of the Reengineered System
Task: #34 | Owner: Abdulwahab | Status: draft | Date: 25/11

## Report summary

We measured Commit 06 with the same Radon version, flags and structural metrics script used to reproduce the Commit 01 baseline. The final production code has 438 physical lines, 299 source lines and 245 logical lines. It has 37 functions including methods and three classes. Radon reported an average cyclomatic complexity of 2.4 and a peak of 7 in `JsonStorage.__init__()`. All 20 static SQL call sites are in `SqliteStorage`; the menu, borrowing code and return service do not call SQLite directly. Four of the eight Phase 1 smell findings were resolved and four were partly addressed. All 12 behavior tests passed.

## Details

### Scope and reproduction

The production baseline is `library.py` at Commit 01 (`02366ff`). It was exported as Git blob bytes and verified as `6970928538632438a4cda2cceeac77b2a44d6aee`. The final scope is `library.py`, `return_service.py` and `storage.py` at Commit 06 (`ec8b191`). Tests, tools and generated data are excluded from both measurements.

Both runs used Python 3.14.6, Radon 6.0.1 and the same fixed `tools/metrics.py` from Commit 06, as specified in [task #14](../phase1/baseline-metrics.md). Run the commands below from Commit 06 for the final results. For the baseline, run them against only the exported `library.py`, using the same script from Commit 06.

```sh
python -m pip install radon==6.0.1
python -m radon raw -s library.py return_service.py storage.py
python -m radon cc -s -a --total-average --show-closures library.py return_service.py storage.py
python -m radon hal library.py return_service.py storage.py
python -m radon hal -f library.py return_service.py storage.py
python -m radon mi -s library.py return_service.py storage.py
python tools/metrics.py library.py return_service.py storage.py
```

Halstead and maintainability index were run for consistency with #14, but are not part of Table 9; the displayed module values are not a system-wide measure.

### Final counts

| Module | LOC | SLOC | LLOC | Functions, including methods | Classes | SQL call sites |
|---|---:|---:|---:|---:|---:|---:|
| `library.py` | 154 | 86 | 92 | 10 | 0 | 0 |
| `return_service.py` | 37 | 20 | 22 | 3 | 1 | 0 |
| `storage.py` | 247 | 193 | 131 | 24 | 2 | 20 |
| **Total** | **438** | **299** | **245** | **37** | **3** | **20** |

- **Complexity:** Radon reported an average of 2.4 (A) across 40 blocks (37 functions/methods and three class blocks). `JsonStorage.__init__()` is the peak at 7 (B); `main()` is 6 (B) and `borrow()` is 4 (A).
- **Database dependencies:** The script counts static `execute`, `executemany` and `executescript` call sites, not statements run at runtime. All 20 sites are in `SqliteStorage`: eight for initialization, five for reads, four for loan/copy updates and three for export. Nine of 37 functions/methods contain a direct DB call under the script's definition (SQL, `connect` or `commit`); all nine are `SqliteStorage` methods. JSON can use that adapter for initial migration; neither application module calls SQLite directly.
- **Behavior check:** `python -m unittest discover -s tests -v` passed all 12 tests.

### Phase 1 smell reassessment

Reused the [task #13 inventory](../phase1/code-smells.md) and its rule: one row per distinct finding, even when it has multiple locations. A finding is **resolved** when its original issue no longer applies, **partial** when some of it persists, and **remaining** when it was not materially reduced. Table 9 counts partial and remaining items among the original eight; architectural problems (AP1–AP6) and any new findings are separate.

| ID | Status | Evidence in Commit 06 |
|---|---|---|
| CS1 — Long `borrow()` | Resolved | `library.borrow()` is 14 lines rather than 67 and delegates validation, availability, limit checking and loan creation; CC fell from 6 to 4. |
| CS2 — Long setup routine | Partial | `library.setup()` delegates to storage, but `SqliteStorage.__init__()` still creates the schema, migrates it and seeds the database in one method. |
| CS3 — Duplicate query/check/output in `borrow()` | Resolved | SQL lookup and fetching live in storage methods. `borrow()` calls the rule helpers; its early returns no longer repeat the query/fetch/check/print sequence. |
| CS4 — Duplicate ID reads and seed inserts | Resolved | Both menu branches call `read_ids()`; SQLite seeds members and books in two batches with `executemany()`. |
| CS5 — Repeated active-loan and availability logic | Partial | Business code delegates to storage and JSON shares `_active_loans()`, but the two SQLite queries still repeat `returned=0`. Borrow/return copy updates still have parallel implementations in both stores. |
| CS6 — Magic literals | Partial | `MAX_BOOKS`, `LOAN_DAYS`, `FINE_PER_DAY` and `ACTIVE` name the key rules; storage still uses literal `0`/`1` for loan state and in legacy migration. |
| CS7 — Unclear names and positional fields | Partial | Application code uses names such as `member_id` and `copies_on_shelf` and unpacks rows. Cursor `c`, short JSON variable names and positional access such as `c.fetchone()[0]` remain in storage. |
| CS8 — Missing documentation | Resolved | All three production modules have module docstrings, and the extracted borrowing helpers describe their roles. |

**Total:** four resolved, four partial, zero unchanged. The new `JsonStorage.__init__()` mixes loading, migration, seeding, conversion and saving. That is another instance of the initialization concern (CS2) and the new complexity peak, not a ninth baseline finding. The count does not claim to be an exhaustive audit of new code.

## Screenshots

No screenshots; the measurement commands and results are recorded above.

## Sources

- [Course slides](../reference/maintenance-course.pdf), PDF pp. 167–170 (program metrics), p. 272 (code smells).
- [Radon 6.0.1 documentation](https://radon.readthedocs.io/en/v6.0.1/) and the project’s [`tools/metrics.py`](../../tools/metrics.py).
- [Task #14 baseline](../phase1/baseline-metrics.md) and [task #13 smell inventory](../phase1/code-smells.md).
- OpenAI GPT-6.2 Sol (OpenCode): assisted with measurement, smell reassessment and drafting.
