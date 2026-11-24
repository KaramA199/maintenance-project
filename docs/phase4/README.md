# Phase 4: Reuse and Domain Engineering

Milestone: Commit 05, "05 - Add Equipment Borrowing System analysis for re-use". It marks the end of Phase 4. The analysis was merged into `main` through its own pull request (#22), after Commit 04, so the history shows the refactoring before the reuse analysis.

The project description asks to analyze the common and variable features of the Library Management System and a new Equipment Borrowing System (laptops, projectors, cameras, laboratory instruments), and to propose a reusable domain architecture. This phase is analysis and design only: no code changed.

| Task | Document | Deliverable | Report section | Owner |
|---|---|---|---|---|
| #28 | [equipment-system.md](equipment-system.md) | Requirements of the Equipment Borrowing System, each marked as the same as, a changed version of, or new compared with the library | 6.1 | Karam |
| #29 | [commonality-variability.md](commonality-variability.md) | Common and variable features of the two systems | 6.2, Table 8 | Karam |
| #30 | [domain-architecture.md](domain-architecture.md) | Reusable domain architecture | 6.3, Figure 5 | Karam |
| #31 | this index | Commit 05 | – | Muayyad |

Main findings:
- The two systems are a program family. The borrowing process is common to both: active-borrower and availability checks, a borrowing limit, a due date, late fines, loan records and search.
- The differences are mostly values (limit, loan period, fine rate) and item data (book copies or single serial-numbered units). Only the equipment condition check with a damage fee is new behavior.
- The domain architecture has a shared core (`Item`, `Borrower`, `Loan`, `BorrowingService`, `BorrowingRules`, `LoanStore`) and one extension per system. It follows the extractive reuse model: the core is taken from the library code after Phase 3, whose borrow checks become `BorrowingRules` and whose MR-02 storage layer becomes `LoanStore`.

Diagram for this phase: [`docs/img/phase4/domain-architecture.png`](../img/phase4/domain-architecture.png) (Figure 5).
