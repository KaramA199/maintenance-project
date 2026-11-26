# SE431 – Legacy Library Management System (Maintenance & Reengineering)

Course project for **SE431 – Software Maintenance and Evolution** (Fall 2026), University of Prince Mugrin.

A small legacy Library Management System (LMS, ~100 LOC, Python + SQLite) that we analyze, maintain, refactor and reengineer, and for which we study reuse with an Equipment Borrowing System.

**Deadline:** 29/11/2026

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

## How to run

Requires Python 3.10+ (standard library only). From the repository root:

```bash
python library.py
```

Menu: `1` Search, `2` Borrow, `3` Return, `4` Exit. The seed data has members `S1` and `S2` and books `1` to `3`.

The data is stored through the data-access layer in `storage.py` (MR-02). The environment variable `LMS_BACKEND` picks the store:

| `LMS_BACKEND` | Store | File (in the current folder) |
|---|---|---|
| not set, or `json` | JSON file (default) | `library.json` |
| `sqlite` | the legacy SQLite database | `library.db` |

```bash
# Git Bash / Linux / macOS
LMS_BACKEND=sqlite python library.py
```

```powershell
# Windows PowerShell
$env:LMS_BACKEND = "sqlite"; python library.py
```

To start again with only the seed data, delete `library.json` or `library.db`. See `docs/00-environment-setup.md` for the original setup notes.

## How to run the tests

The 12 behavior-preservation tests (task #23) use Python's built-in `unittest`. From the repository root:

```bash
python -m unittest discover -s tests -v
```

The result must be `Ran 12 tests` and `OK`. Each test runs in a temporary folder, so your own `library.json` or `library.db` is not touched.

To compare the menu output of two versions, pipe the scripted session into the program in an empty folder, once per store:

```bash
LMS_BACKEND=json python library.py < tests/menu_session.txt
LMS_BACKEND=sqlite python library.py < tests/menu_session.txt
```

## Working agreement

- **Branch, then PR:** do each task on its own branch (`<name>/<short-task>`) and open a pull request into `main`; do not commit directly to `main`.
- Push your own work in your own commits; the milestone commits above only mark the end of each phase.
- Do not change `library.py` until the milestone before your task is pushed.
