# Project Charter – SE431 Legacy LMS Reengineering

| | |
|---|---|
| **Course** | SE431 – Software Maintenance and Evolution, Fall 2026 |
| **Instructor** | Dr. Saima Shaheen |
| **Project manager / team leader** | Karam M. Ali |
| **Start** | 11/11/2026 |
| **Deadline** | 22/11/2026, 11:59 PM (late: -1 mark/day, max 3 days) |
| **Repository** | https://github.com/KaramA199/maintenance-project (private) |
| **Board** | https://github.com/users/KaramA199/projects/2 |

## 1. Objectives

1. Understand the ~100 LOC legacy Library Management System (Python + SQLite) through program comprehension and reverse engineering, without changing it first.
2. Classify and analyze two maintenance requests: **MR-01** (multiple copies per book) and **MR-02** (replace the database), and propose designs (implementation is bonus).
3. Refactor `borrow()` plus at least two more documented refactorings, preserving externally observable behavior.
4. Analyze commonality and variability with an Equipment Borrowing System and propose a reusable domain architecture.
5. Evaluate the reengineered architecture against the legacy one (LOC, functions, classes, cyclomatic complexity, code smells, DB dependencies).
6. Keep a Git history that shows the evolution in six milestone commits.

## 2. Scope

**In scope:** everything in the course project description, Phases 1–6, plus the submission package.
**Out of scope:** new features beyond MR-01/MR-02, a real equipment system implementation (analysis and architecture only), a GUI.

## 3. Deliverables (zipped as `SE431-Project-Fall 26-TeamNo`, submitted on MS Teams)

1. Written report (MS Word, ~2000 words)
2. PowerPoint presentation
3. Demo video covering all evolution steps and the Git history
4. Git repository link (shared)

## 4. Milestones

| Date | Milestone | Git commit |
|---|---|---|
| 15/11 | Repo, legacy code, environment setup | 01 – Initial legacy system |
| 17/11 | Phase 1 analysis and baseline metrics | 02 – Program comprehension analysis |
| 19/11 | MR-01 and MR-02 | 03 – Maintenance Request incorporation |
| 20/11 | Refactoring and Equipment reuse analysis | 04 – Refactor borrowing module; 05 – Add Equipment Borrowing System analysis for re-use |
| 21/11 | Final system, final metrics, comparison | 06 – Final reengineered system |
| 22/11 | Report, slides, video assembled, reviewed and submitted | – |

## 5. Roles and responsibilities

| Member | Responsibilities |
|---|---|
| **Karam M. Ali** (leader/PM) | Repo, charter, board, risk log; legacy setup and requirements confirmation; project-management section of the report; final review and submission |
| **Abdulwahab Najib** | Business rules, DB schema, architecture diagram, class/module table; final metrics and before/after comparison; knowledge-acquired section; assembles report, slides and video |
| **Nasser Ali Atef** | Dependency analysis, code smells, baseline metrics, Commit 02; MR-01 and MR-02 (analysis, design, implementation), Commit 03 |
| **Muayyad Alnouman** | Behavior tests; refactoring; Equipment reuse analysis; final system clean-up; Commits 04–06 |

Everyone writes their own report section and slides, records their own demo part, and prepares for the Q&A on the whole project.

## 6. Resources and tools

GitHub (repo, Projects board, issues), GitHub Desktop, Python 3 + SQLite, a metrics tool (same tool and settings for before/after), MS Teams for communication, MS Word and PowerPoint.

## 7. Working rules

- Push your own work in your own commits; milestone commits only mark the end of a phase.
- Do not change `library.py` before the milestone it depends on is pushed (see risk log).
- Track progress on the board; raise blockers there or in the group chat the same day.
- Cite every external source (plagiarism is zero tolerance).

## 8. Success criteria

All six milestone commits in order; all PDF deliverables present; every member able to answer questions on their own work; submitted before the deadline.

## 9. Risks

See `docs/02-risk-issue-log.md`.
