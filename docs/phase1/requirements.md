# Legacy Requirements Confirmation
Task: #7 | Owner: Abdulwahab Najib | Status: draft | Date: 16/11

## Report summary

The six original requirements were traced from README.md and the report template to the unchanged legacy implementation. borrow() checks member existence and ACTIVE status, rejects unavailable books, counts active loans against the three-book limit, and assigns a due timestamp fourteen days after borrowing. return_book() calculates a nonnegative fine from completed overdue days, marks the loan returned and makes the book available again. search_books() matches titles and authors using SQL LIKE. The borrowing requirements hold for the program's normal seeded data and state transitions. Two qualifications matter: the availability column is not restricted to Boolean values, and the fine is zero until a full twenty-four hours has elapsed after the due timestamp. Searching also does not verify membership. Table 2 records these qualifications alongside exact function and line references, so later maintenance and behavior-preservation work can distinguish current behavior from an assumed policy.

## Details

### Scope and confirmation method

- Original requirements: README.md lines 20–27 and the Original Requirements list in `SE431-ProjectReport.docx`.
- Code reference: unchanged `library.py`, revision `abd4b09`. Line numbers below refer to this version, not a future refactoring.
- Each menu path was traced to its function and SQL. Isolated in-memory probes on 16/11/2026 checked representative successful and rejected paths without writing `library.py` or `library.db`.
- "Yes" means the behavior is present; it does not imply authentication, database constraints, concurrency safety or formal acceptance testing.
- Draft pending Abdulwahab's verification and its own PR. Report section 3.1 and the task-table row remain untouched until merge.

### Table 2: requirements traceability

| Req. # | Original requirement | Code location | Confirmed? / qualification |
|---|---|---|---|
| R1 | Active members can borrow books | library.py: borrow(), lines 78–91; successful recording lines 118–142; main() entry lines 197–200 | Yes. Missing members and any status other than exact ACTIVE are rejected. Other borrowing conditions must also pass. |
| R2 | A member can borrow a maximum of 3 books | library.py: borrow(), lines 108–116 | Yes for sequential application-created loans. Counts loans for that member with returned=0; count >=3 rejects the next loan. Returned history does not count. |
| R3 | A book can only be borrowed when available | library.py: borrow(), lines 93–106 and 133–138; return_book(), lines 169–174 | Yes for intended 0/1 availability data. A successful borrow sets 0, and a return restores 1. The guard rejects only 0; NULL/noncanonical values are not constrained. |
| R4 | The normal borrowing period is 14 days | library.py: borrow(), lines 118–130 and 140 | Yes. Due timestamp is datetime.now() + timedelta(days=14), stored as ISO text; the displayed due date omits the time. |
| R5 | A fine is charged for late returns | library.py: return_book(), lines 157–162 and 176–179 | Partial if any overdue interval should incur a fine: only completed overdue days are counted. Zero is charged below 24 hours late; positive fines are printed, not stored or collected. |
| R6 | Members can search for books | library.py: search_books(), lines 60–75; main(), lines 193–195 | Yes. Title or author LIKE search returns and prints matches. The CLI does not ask for or validate a member identity. |

### Observed confirmation evidence

| Requirement | Probe and observed outcome |
|---|---|
| R1 | S9 rejected as Member not found; S1 with INACTIVE status rejected as Member is not active; ACTIVE S1 could borrow an available book |
| R2 | S1 borrowed books 1, 2 and 3; a temporary fourth available book was rejected as Borrowing limit reached and remained available |
| R3 | After S1 borrowed book 1, S2's request for book 1 was rejected as Book is unavailable; return restored available=1 |
| R4 | Fixed borrowing time 16/11/2026 12:00 produced due time 30/11/2026 12:00; the stored timestamp difference was exactly 14 days |
| R5 | At a fixed return time, a due timestamp 23 hours earlier produced only Book returned; one 24 hours earlier additionally produced Fine: 1 |
| R6 | refactor and Fowler each found book 2; a nonexistent title returned [] with no printed message |

The broader comprehension probes passed 17 exact return/output cases plus state and schema assertions. These are not a substitute for Muayyad's task #23 suite. No concurrency, malformed-input acceptance or end-to-end security test is claimed.

### Requirement boundaries for follow-on work

- Confirm the intended rounding and currency with the course specification before treating R5's whole-day behavior as a defect. This task documents the discrepancy; it changes no policy.
- One books row supplies one availability flag. There is no multiple-copy requirement implemented yet; that is MR-01, not an original requirement confirmed here.
- There is no authentication or authorization mechanism. An identifier lookup is not proof of a user's identity.
- No database constraint enforces active-loan uniqueness or the three-loan policy. The evidence above concerns ordinary sequential execution through the current functions.
- Invalid integer book IDs can terminate the CLI with ValueError. This is an observed input boundary, not a new original requirement.

### Report handoff: section 3.1 (50-word budget)

Table 2 traces the six original requirements to the unchanged implementation. Active-member validation, the three-loan limit, fourteen-day period and title/author search are present. Availability assumes normal flag values. Fine handling is qualified: only completed overdue days produce a printed charge, so returns under twenty-four hours late incur no fine.

After the task PR merges, fill all six rows of the existing Table 2, preserving its style; do not modify other members' Phase 1 sections.

## Screenshots

None required: Table 2, exact code ranges and the recorded probe outcomes are the evidence for this tracing task.

## Sources

1. Project primary sources: `library.py`, `README.md`, `PLAN.md`, and all three existing setup/charter/risk documents; task #7, Original Requirements and section 3.1 in `SE431-ProjectReport.docx` (Microsoft Word MCP, 16/11/2026).
2. Python documentation, [datetime: timedelta objects](https://docs.python.org/3/library/datetime.html#timedelta-objects), accessed 16/11/2026; used to interpret the fine qualification.
3. OpenAI GPT-6.1 Sol, via OpenCode, 16/11/2026: assisted requirements tracing, isolated probes and drafting. Abdulwahab must verify and rewrite the draft before submission under PLAN.md's authorship rule.
