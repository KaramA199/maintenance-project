# Equipment Borrowing System Requirements
Task: #28 | Owner: Karam M. Ali | Status: done | Date: 21/11

## Report summary

The university wants a second system for lending equipment: laptops, projectors, cameras and laboratory instruments. The project description only names the item types, so we wrote the requirements ourselves, starting from the six library requirements (R1–R6) and the business rules found in Phase 1. Each equipment requirement is marked as the same as a library requirement, a changed version of one, or new. Three of the eight requirements are the same as in the library (active users only, available items only, a fine for late returns). Four are changed versions: a different borrowing limit, a loan period that depends on the type of equipment, search by name or type, and items that are single serial-numbered units instead of several copies of a title (as the library has after MR-01). Only one is completely new: the item's condition is checked when it comes back. This list is the starting point for the commonality and variability analysis in task #29.

## Details

### The system

The university lends equipment to its students and staff. A technician registers each item, users borrow and return items, and the system records every loan. The item types are the ones named in the project description (p.2, Phase 4): laptops, projectors, cameras and laboratory instruments.

In the course's terms, this is the first step of domain analysis: identifying the family of products (p.362). The library system and the equipment system are two members of one family of "borrowing systems".

### Requirements

The project description does not list detailed requirements, so the ones below are our own assumptions. They are kept close to the library system on purpose, so the two systems can be compared.

| ID | Requirement | Compared with the library system |
|---|---|---|
| EQ1 | Only registered users (students and staff) with an active status can borrow equipment. | Same as R1 |
| EQ2 | A user can borrow at most 2 items at a time. | Changed from R2 (limit is 2, not 3) |
| EQ3 | An item can only be borrowed when it is available. | Same as R3 |
| EQ4 | The loan period depends on the type: laptop 7 days, projector and camera 3 days, laboratory instrument 1 day. | Changed from R4 (fixed 14 days) |
| EQ5 | A fine is charged for each day an item is returned late (assumed rate: 5 per day). | Same as R5 (only the rate differs) |
| EQ6 | Users can search for equipment by name or by type. | Changed from R6 (title or author) |
| EQ7 | Each item is a single unit identified by its serial number. | Changed from R3 as updated by MR-01 (the library keeps several copies of a title as a count) |
| EQ8 | When an item is returned, its condition is recorded, and a damage fee is charged if it is damaged. | New |

### Report handoff: section 6.1 (60-word budget)

The university also wants to lend laptops, projectors, cameras and laboratory instruments. We wrote eight requirements for this system, starting from the library's. Active users only, availability and late fines stay the same. Changed: a limit of 2, a loan period per equipment type, search by name or type, and serial-numbered units. New: a condition check on return.

## Screenshots

None needed. The requirements are in the table above.

## Sources

- Course project description, *SE431 Fall-2026 Project Description*, p.2 (Phase 4: Reuse & Domain Engineering).
- Course PDF `docs/reference/maintenance-course.pdf` (Tripathy & Naik, Chapter 9): p.350 (program families), p.362 (domain analysis steps).
- `docs/phase1/requirements.md` (#7) and `docs/phase1/business-rules.md` (#8), for the library requirements R1–R6 and rules.
- `docs/phase2/mr01-multiple-copies.md` (MR-01), for how the library now handles several copies of a title.
- AI tool: Claude (Anthropic), used to help draft this document. Reviewed and edited by the author.
