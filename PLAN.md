# PLAN.md: how we work

Read this first, whether you are a team member or an AI agent working for one. The project is the SE431 Fall 2026 legacy Library Management System (LMS) reengineering. The deadline is **22/11/2026, 11:59 PM**.

Source documents in the repo: `README.md` (overview), `docs/01-project-charter.md`, `docs/02-risk-issue-log.md`, `docs/00-environment-setup.md`.
The task list (43 tasks, with owners and dependencies) is the table at the start of `SE431.docx`. The board is https://github.com/users/KaramA199/projects/2.

## 1. Rules

1. **Branch, then pull request.** Never commit to `main`. Create a branch named `<name>/<short-task>` (for example `nasser/baseline-metrics`), push it, and open a pull request into `main`. Another member looks at it before it merges. Keep each pull request to one task.
2. **Your own commits.** Commit your own work under your own name. Do not add other people or an AI tool as a co-author.
3. **Do not edit `library.py` early.** `library.py` stays unchanged until Commit 03 is on `main`, except for Nasser's MR-01 and MR-02 work. Muayyad starts refactoring only after Commit 03.
4. **Measure before changing.** Nasser records the baseline metrics (task #14) on the unchanged legacy code and writes down the tool and settings. Abdulwahab reuses the same tool and settings for the final measurement (task #34).
5. **Behavior must not change** during refactoring. Run the tests from task #23 before and after.
6. **Write your own words and cite sources.** The course treats copied text and uncited AI output as plagiarism, with zero marks. AI tools may help you draft and check, but you must read, verify and rewrite what they produce, and you must be able to explain every line you submit in the Q&A. Add every external source (books, articles, tool docs, and AI tools you used) to your task document under "Sources".
7. **Every task leaves documentation** (section 3) and, where useful, screenshots.
8. **Keep the board current.** Move your card to In Progress when you start and to Done when your pull request merges.
9. **Ask early.** If you are blocked or will miss a date, say so in the group chat the same day.

## 2. Order of work

All tasks below can start now. Tasks #1 to #6 are done.

| Who | Start with, in this order | Then, after the wait |
|---|---|---|
| **Abdulwahab** | #9 database schema, #11 class/module table, #8 business rules, #7 requirements, #10 architecture diagram | #34 final metrics and #35 comparison, after Commit 06 |
| **Nasser** | #14 baseline metrics (first, before any code change), #12 dependencies, #13 code smells | #16 and #19 after Abdulwahab finishes #9 and #11; then #17, #20, #18, #21; #15 (Commit 02) after Abdulwahab finishes #7 to #11; #22 (Commit 03) last |
| **Muayyad** | #23 behavior tests | #28 and #29 after Abdulwahab finishes #7 and #8; #30 after #10; #24 to #27 after Commit 03; then #31, #32, #33 |
| **Karam** | #36 (collect evidence as work happens), keep the board current | #37 to #42 as the others finish |

Why this order: Abdulwahab's #9 and #11 unblock Nasser's maintenance work, so they come first. Nasser's #14 must happen before anyone changes code. Muayyad's tests are needed twice, by Nasser (#21) and by Muayyad (#27).

Target dates: Phase 1 on 17/11, MR-01 and MR-02 on 19/11, refactoring and Equipment analysis on 20/11, final system on 21/11, everything submitted on 22/11.

## 3. Where documentation goes

Each task writes one Markdown file, with screenshots in `docs/img/<phase>/`. Diagrams may be Mermaid in the Markdown file or an exported PNG.

| Task | File |
|---|---|
| #7 | `docs/phase1/requirements.md` |
| #8 | `docs/phase1/business-rules.md` |
| #9 | `docs/phase1/database-schema.md` |
| #10 | `docs/phase1/architecture.md` |
| #11 | `docs/phase1/class-responsibilities.md` |
| #12 | `docs/phase1/dependencies.md` |
| #13 | `docs/phase1/code-smells.md` |
| #14 | `docs/phase1/baseline-metrics.md` |
| #16 to #18 | `docs/phase2/mr01-multiple-copies.md` |
| #19 to #21 | `docs/phase2/mr02-database-replacement.md` |
| #23 | `docs/phase3/behavior-tests.md` (test code in `tests/`) |
| #24 to #27 | `docs/phase3/refactoring-log.md` (one section per refactoring, with before and after) |
| #28 to #30 | `docs/phase4/equipment-system.md`, `docs/phase4/commonality-variability.md`, `docs/phase4/domain-architecture.md` |
| #32 | `docs/phase5/final-architecture.md` |
| #34, #35 | `docs/phase5/final-metrics.md`, `docs/phase5/comparison.md` |
| #37 | `docs/notes/knowledge-<name>.md`, one per member |

Start every file with this header:

```
# <Title>
Task: #<number> | Owner: <name> | Status: draft / done | Date: <dd/mm>

## Report summary
<100 to 200 words, ready to paste into the report>

## Details
<analysis, tables, diagrams>

## Screenshots
<images from docs/img/..., each with a caption>

## Sources
<books, articles, tool docs, AI tools used>
```

The "Report summary" is what Karam copies into the Word report, so write it as finished prose and keep it short.

## 4. Milestone commits

A milestone commit marks the end of a phase. The owner makes it on `main`, after that phase's pull requests are merged, by adding a short `docs/<phase>/README.md` index and using exactly this message:

| Commit | Message | Owner | After |
|---|---|---|---|
| 01 | `01 - Initial legacy system` | Karam | done |
| 02 | `02 - Program comprehension analysis` | Nasser | #7 to #14 merged |
| 03 | `03 - Maintenance Request incorporation` | Nasser | #16 to #21 merged |
| 04 | `04 - Refactor borrowing module` | Muayyad | #24 to #27 merged |
| 05 | `05 - Add Equipment Borrowing System analysis for re-use` | Muayyad | Commit 04 pushed, and #28 to #30 merged |
| 06 | `06 - Final reengineered system` | Muayyad | #32 merged |

Commits 04 and 05 must go in that order, because the course checks that the history shows the evolution in sequence.

## 5. Keeping the Word task table current

The task table at the start of `SE431.docx` shows progress. When a task is done (pull request merged and card moved to Done), **strike through the whole row's text** (Word: select the row, Home, Strikethrough). Karam updates it from the board every evening, so members only need to keep the board right.

## 6. If you use an AI agent

Give the agent this file and your task number. The agent must follow sections 1, 3 and 4, work on a branch, and stop before merging. You review its output before opening the pull request. List the AI tool under "Sources" in your task document.
