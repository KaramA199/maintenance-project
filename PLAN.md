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
7. **Every task leaves documentation** (section 3) and, where useful, screenshots. When the task is done, write its part of the Word report too (section 5).
8. **Keep the board current.** Move your card to In Progress when you start and to Done when your pull request merges.
9. **Ask early.** If you are blocked or will miss a date, say so in the group chat the same day.
10. **Use the course material as the method reference.** The full course is in `docs/reference/maintenance-course.pdf`. When a task asks for a technique (impact analysis, refactoring, program comprehension, reengineering, reuse and domain engineering), follow how the course teaches it and cite the page number under "Sources". Do not invent methods or use techniques the course did not cover. If you need something outside the course, say so in your task file and cite the outside source.

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

## 5. Writing your part of the report

The report is one shared Word file, `SE431-ProjectReport.docx`. When your task is done (your pull request is merged), you or your agent write the matching section of the report. No two members edit the same place at once, so touch only the sections listed for your tasks.

| Task | Report section | Words |
|---|---|---|
| #7 | 3.1 Requirements Confirmation (Table 2) | 50 |
| #8 | 3.2 Business Rules | 60 |
| #9 | 3.3 Database Structure (Figure 2) | 50 |
| #10 | 3.4 Current Architecture (Figure 3) | 60 |
| #11 | 3.5 Class/Module Responsibilities (Table 3) | 40 |
| #12 | 3.6 Dependency Analysis (Figure 4) | 70 |
| #13 | 3.7 Code Smells and Architectural Problems (Table 4) | 70 |
| #14 | 7.1 Measurement Approach (tool and settings) and the Legacy System column of Table 9 | 50 |
| #16 to #18 | 4.1 MR-01 (4.1.1 to 4.1.3, Table 5) | 170 |
| #19 to #21 | 4.2 MR-02 (4.2.1 to 4.2.3, Table 6) | 170 |
| #23 | 5.1 Behavior-Preservation Tests | 80 |
| #24 to #27 | 5.2 Refactoring Log (Table 7) and 5.3 Verification | 220 |
| #28 | 6.1 Equipment Borrowing System Overview | 60 |
| #29 | 6.2 Commonality and Variability Analysis (Table 8) | 70 |
| #30 | 6.3 Reusable Domain Architecture (Figure 5) | 70 |
| #32 | Figure 6 (final architecture) in 7.2 | caption only |
| #33 | 8.1 Repository and 8.2 Commit History (Table 10, Figure 7) | 100 |
| #34, #35 | 7.2 Results (Table 9, Reengineered System column) and 7.3 Discussion | 150 |
| #37 | 9 Knowledge Acquired (Table 11) | 100 |
| #36, #38, #41 | 1 Introduction, 2 Project Management, 10 Conclusion, References | Karam |

The whole report is about 2000 words, so keep to the budget. Tables, figures and captions do not count toward it.

How to write your section:
- Be brief. Use the "Report summary" from your task file as the starting point, then shorten it. Put the detail in the table or figure, not in the prose.
- Replace the amber placeholder text in your section with your own text. Delete the amber instruction line for your section only. Use the same font and size as the text around it, and keep the heading as it is.
- Fill the existing table for your section. Add rows if you need them. Do not change the table style.
- Insert screenshots and diagrams where the placeholder is, keep the caption, and keep its figure number. Karam fixes any numbering gaps at the end.
- Do not add references yourself. List your sources in your task file, and Karam compiles the References section.
- Check that you have not edited text outside your section before you save. Close the file when you finish, so others can open it.

When you finish a task, also **strike through that task's row** in the task table at the start of the Word file (select the row text, Home, Strikethrough). Strike only your own rows. Karam checks the table against the board.

## 6. If you use an AI agent

Give the agent this file and your task number. The agent must follow sections 1, 3, 4 and 5, read the relevant chapters of `docs/reference/maintenance-course.pdf` before starting, work on a branch, and stop before merging. After the pull request merges, the agent writes your report section as described in section 5. You review its output before opening the pull request and before you save the report. List the AI tool under "Sources" in your task document.
