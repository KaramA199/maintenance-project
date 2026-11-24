# Commonality and Variability Analysis
Task: #29 | Owner: Karam M. Ali | Status: done | Date: 21/11

## Report summary

We compared the Library Management System with the proposed Equipment Borrowing System to find which features they share and which differ. This is the second step of domain analysis in the course: after identifying the family of products, determine its common and variable features (p.362). The two systems clearly form a program family, a set of programs with many features in common (p.350). Both systems lend an item to a borrower and record the loan. Both check that the borrower is active and the item is available, limit how many items one person may hold, give a due date, charge a fine for late returns, and offer search. What changes between them is mostly data and values: what an item is (a book or a piece of equipment), whether a title has several copies or each unit is single, the borrowing limit, the loan period, the fine rate, and the search fields. Only one feature, the condition check with a damage fee, exists in one system alone. Table 8 lists every feature. The common features become the shared core of the domain architecture in task #30, and the variable features become its extension points.

## Details

### Method

We followed the three domain-analysis steps given in the course (p.362):

1. **Identify the family of products:** the library system and the equipment system (task #28).
2. **Determine the common and variable features:** Table 8 below.
3. **Develop the specification of the family:** the reusable domain architecture in task #30.

The course names FODA (Feature-Oriented Domain Analysis) as a well-known method for documenting what is common and what differs within a domain (p.362). We used the same idea in a simple form, a feature table, instead of a full feature diagram.

**How a feature is classified:**
- **Common:** both systems have the feature, and it works the same way.
- **Variable:** the feature works differently in each system (for example, a different value), or only one system has it.

### Table 8: Common and variable features

| Feature | Library System | Equipment System | Common / Variable |
|---|---|---|---|
| Borrow item | ✓ | ✓ | Common |
| Return item | ✓ | ✓ | Common |
| Borrower must exist and be active | ✓ | ✓ | Common |
| Item must exist and be available | ✓ | ✓ | Common |
| Record each loan (borrow date, due date, returned) | ✓ | ✓ | Common |
| Fine for each day late | ✓ | ✓ | Common |
| Search for items | ✓ | ✓ | Common |
| Item details | Title, author | Name, type, serial number | Variable |
| Units per item | Several copies of a title, kept as a count (MR-01) | One unit per serial number | Variable |
| Borrowing limit | 3 books | 2 items | Variable |
| Borrowing period | 14 days for every book | Depends on type: laptop 7 days, projector and camera 3 days, lab instrument 1 day | Variable |
| Fine amount per day | 1 | 5 | Variable |
| Search fields | Title or author | Name or type | Variable |
| Condition check and damage fee on return | – | ✓ | Variable (equipment only) |

### What the table shows

- **Common:** seven features, which are the whole borrowing process. This is the part worth building once and reusing.
- **Variable:** seven features. Six of them are about item data or policy values (item details, units per item, limit, period, fine, search fields), not about how borrowing works. They can be handled by giving each system its own item type and its own set of rules.
- **Only one variable feature adds new behavior:** the condition check. It belongs to the equipment system alone and is added as an extension, without changing the shared core.

### Report handoff: section 6.2 (70-word budget)

Following the course's domain-analysis steps, we listed the features of both systems and marked each as common or variable (Table 8). The borrowing process itself is common: active-borrower and availability checks, a limit, a due date, late fines, loan records and search. The differences are mostly values (limit, loan period, fine rate) and item data (details, copies or single units). Only the equipment condition check adds new behavior.

## Screenshots

None needed. Table 8 above is copied into the report.

## Sources

- Course PDF `docs/reference/maintenance-course.pdf` (Tripathy & Naik, Chapter 9): p.350 (program families), p.362 (domain analysis steps and FODA).
- `docs/phase4/equipment-system.md` (#28), and `docs/phase1/requirements.md` and `docs/phase1/business-rules.md`, for the features of each system.
- `docs/phase2/mr01-multiple-copies.md` (MR-01), for the library's copies.
- AI tool: Claude (Anthropic), used to help draft this document. Reviewed and edited by the author.
