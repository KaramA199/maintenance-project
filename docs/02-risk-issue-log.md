# Risk and Issue Log

Impact / likelihood: L = low, M = medium, H = high. Status is updated as the project goes.

| # | Risk / issue | Impact | Likelihood | Mitigation / resolution | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | Only one week between start of the work and the 22/11 deadline | H | H | Internal milestone dates on the board; start parallel tasks as soon as the repo and legacy setup are done | Karam | Open |
| 2 | A member is unavailable or falls behind | H | M | Daily check on the board; tasks reassigned within 24 h of a missed date; everyone reviews all sections | Karam | Open |
| 3 | Merge conflicts on `library.py` (MR-01 changes `borrow()` while it is also refactored) | M | H | Refactoring starts only after Commit 03; each member works in their own files/folders and commits their own work | Nasser, Muayyad | Open |
| 4 | Baseline and final metrics are not comparable (different tool or settings) | M | M | Record tool and settings with the baseline; reuse them unchanged for the final measurement | Nasser, Abdulwahab | Open |
| 5 | Behavior changes during refactoring or the database swap | H | M | Behavior tests written on the legacy code first and re-run after refactoring and MR-02 | Muayyad | Open |
| 6 | Legacy code was supplied as text without indentation | L | – | Indentation and `__main__` guard restored in Commit 01, no logic changed, documented in the commit message and setup doc | Karam | Resolved |
| 7 | Plagiarism or missing citations in the report | H | L | Every member writes their own section; all sources cited; plagiarism check before submission | Abdulwahab | Open |
| 8 | Report, slides or video arrive too late for review | H | M | Templates prepared early; sections written as each phase finishes; final review on 21–22/11 | Abdulwahab, Karam | Open |
| 9 | Git history does not show the six milestones in order | M | L | Milestone commits pushed in order only (Commit 05 after 04); history reviewed before submission | Muayyad | Open |
