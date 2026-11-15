# SE431 – Legacy Library Management System (Maintenance & Reengineering)

Course project for **SE431 – Software Maintenance and Evolution** (Fall 2026), University of Prince Mugrin.

A small legacy Library Management System (LMS, ~100 LOC, Python + SQLite) that we analyze, maintain, refactor and reengineer, and for which we study reuse with an Equipment Borrowing System.

**Deadline:** 22/11/2026, 11:59 PM

## Team

| Name | Role |
|---|---|
| Karam M. Ali | Team Leader |
| Abdulwahab Najib | Member |
| Muayyad Alnouman | Member |
| Nasser Ali Atef | Member |

Instructor: Dr. Saima Shaheen

## Original requirements

1. Active members can borrow books.
2. A member can borrow a maximum of 3 books.
3. A book can only be borrowed when available.
4. The normal borrowing period is 14 days.
5. A fine is charged for late returns.
6. Members can search for books.

## Evolution milestones

The Git history follows the project phases, one milestone commit per phase:

| # | Commit | Phase |
|---|---|---|
| 01 | Initial legacy system | Starting point |
| 02 | Program comprehension analysis | Phase 1 |
| 03 | Maintenance Request incorporation | Phase 2 (MR-01, MR-02) |
| 04 | Refactor borrowing module | Phase 3 |
| 05 | Add Equipment Borrowing System analysis for re-use | Phase 4 |
| 06 | Final reengineered system | Phase 5 / final |

## Running the legacy system

Requires Python 3.8+ (standard library only).

```bash
python library.py
```

See `docs/00-environment-setup.md` for details.

## Working agreement

- Push your own work in your own commits; the milestone commits above only mark the end of each phase.
- Do not change `library.py` until the milestone before your task is pushed.
