# Legacy Business Rules
Task: #8 | Owner: Abdulwahab Najib | Status: draft | Date: 16/11

## Report summary

Borrowing is permitted only when the member exists, has the exact status ACTIVE, the book exists and its availability value is not zero. The member must have fewer than three loans whose returned value is zero. A successful borrow records the current local timestamp, sets the due timestamp fourteen days later, creates an active loan and marks the book unavailable. Returning requires a matching active loan for the supplied member and book, but does not repeat the active-member check. A return marks that loan returned, restores availability and prints a fine equal to the number of completed overdue days, with a minimum of zero. A return less than twenty-four hours late therefore produces no fine. Searching matches title or author through SQL LIKE and does not validate a member identity. These rules are implemented in Python and SQL statements, not as database constraints or separate policy objects.

## Details

### Evidence and review state

- Source: unchanged `library.py`, revision `abd4b09`; requirements from README.md and the open Word report.
- Task #6's setup and smoke test are documented in `docs/00-environment-setup.md`.
- On 16/11, isolated probes used Python 3.14.6 / SQLite 3.50.4, an in-memory database and a fixed local timestamp (16/11/2026 12:00). No persisted data or source was modified.
- Draft pending Abdulwahab's verification and a task-specific PR; Word updates and task completion marking wait for merge.

### Extracted rules

| ID | Rule as actually implemented | Enforcement / code location |
|---|---|---|
| BR01 | The supplied member ID must identify a stored member | borrow(), lines 78–87; otherwise Member not found and False |
| BR02 | Member status must equal the case-sensitive string ACTIVE | borrow(), lines 89–91; otherwise Member is not active and False |
| BR03 | The supplied book ID must identify a stored book | borrow(), lines 93–102; otherwise Book not found and False |
| BR04 | A book is rejected when available == 0 | borrow(), lines 104–106; otherwise this check passes |
| BR05 | A member may have at most three active loans; the next borrow is rejected when COUNT(*) >= 3 for returned=0 | borrow(), lines 108–116; returned loans do not count |
| BR06 | Each new due timestamp is borrowing time plus exactly timedelta(days=14) | borrow(), lines 118–130; local naive timestamps, not a midnight due date |
| BR07 | Successful borrowing creates a loan with returned=0, sets books.available=0, and commits | borrow(), lines 121–142; prints Book borrowed. Due: followed by the date; returns True |
| BR08 | Returning requires a loan matching both member_id and book_id with returned=0 | return_book(), lines 145–155; otherwise Active loan not found and False |
| BR09 | Fine = max((current local timestamp - due timestamp).days, 0) | return_book(), lines 157–162; one unspecified monetary unit per completed overdue day |
| BR10 | Successful returning marks the selected loan returned=1, restores books.available=1, and commits | return_book(), lines 164–181; always prints Book returned; prints Fine: only if positive; returns True |
| BR11 | Searches use title LIKE pattern OR author LIKE pattern, with pattern = '%' + text + '%' | search_books(), lines 60–75; prints matching rows and returns them without changing storage |

### Important semantics and boundaries

- **Check order:** BR01 → BR02 → BR03 → BR04 → BR05. Only the first failed check prints a rejection; earlier checks can hide a later failure.
- **Availability:** intended data is 0/1, but the guard checks equality to zero, not equality to one. NULL or another nonzero value is not rejected. Search displays `bool(available)`, which can differ from borrowing behavior for NULL. The schema does not constrain this field.
- **Loan state:** active means exactly `returned=0`; there is no stored return timestamp. Return selects a single matching row via fetchone() without ORDER BY if duplicate active loans exist.
- **Return eligibility:** no new member lookup, status check or borrowing-limit check occurs on return. The code allows returning an existing loan after a member becomes inactive.
- **Fine boundary:** Python normalizes timedeltas into whole days plus smaller units [2]. Being 23 hours overdue gives 0; being 24 hours overdue gives 1. Earlier returns are clamped to 0. Currency, collection, a fine cap and payment tracking are not specified or implemented.
- **Search:** no member ID, authentication or ACTIVE check is requested. Empty input matches all non-NULL titles/authors. `%` and `_` remain SQL LIKE wildcards; the text is parameter-bound, not string-interpolated into SQL. Under the default SQLite behavior observed here, ASCII case differences such as refactor/Refactoring match.
- **CLI boundary:** main() converts book IDs using int() (lines 197–205); invalid numeric input raises an uncaught ValueError. Invalid menu choices only print Invalid choice (lines 211–212). These are interface behaviors, not lending-policy requirements.
- **No invented policies:** there is no renewal, reservation, membership expiry, overdue-borrowing ban or member/book management operation in this code. Member status is stored, not derived from fines.

### Fine examples

| Due timestamp | Return timestamp | Fine printed |
|---|---|---|
| 16/11/2026 12:00 | 16/11/2026 11:59 | None (0) |
| 16/11/2026 12:00 | 16/11/2026 12:00 | None (0) |
| 16/11/2026 12:00 | 17/11/2026 11:00 | None (0) |
| 16/11/2026 12:00 | 17/11/2026 12:00 | Fine: 1 |
| 16/11/2026 12:00 | 18/11/2026 13:00 | Fine: 2 |

### Verification record and small reproducer

The executed probes passed 17 exact return-value/output cases: unknown member; inactive member; missing book; three successful borrows; unavailable book; rejected fourth loan; wrong-member return; return after deactivation; repeated return; returns 23 and 24 hours overdue; title search; author search; no-match search; and borrowing a book with NULL availability. Additional assertions checked the 14-day interval, loan/book state changes, active-loan count, empty/wildcard searches, absent foreign keys and acceptance of NULL/orphan data in disposable storage.

These are comprehension probes, not task #23's behavior-preservation suite. Run the following Python snippet from the repository root to recheck the fine boundary without creating a database file:

```python
from contextlib import redirect_stdout
from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import patch
import library

fixed = datetime(2026, 11, 16, 12)
with patch.object(library, "DB", ":memory:"):
    db = library.setup()
try:
    for hours, expected in ((23, "Book returned\n"),
                            (24, "Book returned\nFine: 1\n")):
        db.execute(
            "INSERT INTO loans (member_id,book_id,due_date,returned) VALUES (?,?,?,0)",
            ("S1", 1, (fixed - timedelta(hours=hours)).isoformat()),
        )
        output = StringIO()
        with patch.object(library, "datetime") as clock, redirect_stdout(output):
            clock.now.return_value = fixed
            clock.fromisoformat.side_effect = datetime.fromisoformat
            assert library.return_book(db, "S1", 1) is True
        assert output.getvalue() == expected
    print("PASS: fine boundary at 23 and 24 overdue hours")
finally:
    db.close()
```

### Report handoff: section 3.2 (60-word budget)

Borrowing checks member existence, ACTIVE status, book existence, availability and a maximum of three active loans, in that order. Loans last fourteen days. Returning requires a matching active loan, marks it returned and restores availability. Fines equal completed overdue days, clamped to zero; less than twenty-four hours late incurs none. Search matches title or author without checking membership.

After the PR merges, replace only section 3.2's instruction with a reviewed summary; keep detailed rule locations in this document.

## Screenshots

None captured; the table, fine examples and recorded isolated probes provide textual evidence. No screenshot or production test run is claimed.

## Sources

1. Project primary sources: `library.py`, `README.md`, `PLAN.md` and the three existing setup/charter/risk documents; task #8 and sections 1.2/3.2 in `SE431-ProjectReport.docx` (Microsoft Word MCP, 16/11/2026).
2. Python documentation, [datetime: timedelta objects and datetime.now](https://docs.python.org/3/library/datetime.html#timedelta-objects), accessed 16/11/2026; used to verify completed-day arithmetic and local naive timestamps.
3. OpenAI GPT-6.1 Sol, via OpenCode, 16/11/2026: assisted code tracing, isolated behavior probes and drafting. Reviewed and verified by Abdulwahab.
