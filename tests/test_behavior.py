"""Behavior-preservation tests for the Library Management System (task #23).

These tests record how the legacy system behaves today, so the same tests can
be re-run after every later change (MR-01, MR-02 and the refactorings) to show
that the externally observable behavior is preserved.

Each test names the requirement (R1-R6, docs/phase1/requirements.md) and the
business rule (BR01-BR11, docs/phase1/business-rules.md) it checks.

Run from the repository root:
    python -m unittest discover -s tests -v
"""
import contextlib
import io
import os
import tempfile
import unittest
from datetime import datetime, timedelta

# After MR-02 the system can store data in JSON or SQLite. The tests use the
# SQLite store so they can prepare data with SQL. The legacy code ignores this.
os.environ.setdefault("LMS_BACKEND", "sqlite")

import library


class LibraryBehaviorTest(unittest.TestCase):

    def setUp(self):
        # Each test gets its own empty folder, so setup() creates a fresh
        # library.db there and the real database is never touched.
        self.old_dir = os.getcwd()
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        os.chdir(self.tmp.name)
        self.db = library.setup()
        # The legacy setup() returns the SQLite connection itself; after MR-02
        # it returns a storage object that keeps the connection in ".db".
        self.conn = getattr(self.db, "db", self.db)

    def tearDown(self):
        self.db.close()
        os.chdir(self.old_dir)
        self.tmp.cleanup()

    def call(self, function, *args):
        """Run a library function and return (result, printed text)."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            result = function(self.db, *args)
        return result, out.getvalue()

    def run_sql(self, sql, params=()):
        """Change the test data directly (only used to prepare a test)."""
        self.conn.execute(sql, params)
        self.conn.commit()

    # ---------- Search (R6) ----------

    def test_01_search_by_title_finds_book(self):
        """BR11 / R6: searching part of a title finds the book."""
        rows, _ = self.call(library.search_books, "Clean")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], 1)
        self.assertEqual(rows[0][1], "Clean Code")

    def test_02_search_with_no_match_returns_empty_list(self):
        """BR11 / R6: a search with no match returns an empty list."""
        rows, output = self.call(library.search_books, "zzz")
        self.assertEqual(rows, [])
        self.assertEqual(output, "")

    # ---------- Borrow (R1-R4) ----------

    def test_03_active_member_can_borrow_available_book(self):
        """BR07 / R1: an active member can borrow an available book."""
        result, output = self.call(library.borrow, "S2", 1)
        self.assertTrue(result)
        self.assertIn("Book borrowed. Due:", output)

    def test_04_unknown_member_cannot_borrow(self):
        """BR01 / R1: a member ID that does not exist is rejected."""
        result, output = self.call(library.borrow, "S9", 1)
        self.assertFalse(result)
        self.assertIn("Member not found", output)

    def test_05_inactive_member_cannot_borrow(self):
        """BR02 / R1: a member whose status is not ACTIVE is rejected."""
        self.run_sql("UPDATE members SET status='INACTIVE' WHERE id='S2'")
        result, output = self.call(library.borrow, "S2", 1)
        self.assertFalse(result)
        self.assertIn("Member is not active", output)

    def test_06_unknown_book_cannot_be_borrowed(self):
        """BR03 / R3: a book ID that does not exist is rejected."""
        result, output = self.call(library.borrow, "S1", 99)
        self.assertFalse(result)
        self.assertIn("Book not found", output)

    def test_07_borrowed_book_is_unavailable_to_others(self):
        """BR04 / R3: a book that is already borrowed cannot be borrowed again.

        Expected to change after MR-01 (multiple copies), which deliberately
        changes requirement R3.
        """
        self.call(library.borrow, "S1", 1)
        result, output = self.call(library.borrow, "S2", 1)
        self.assertFalse(result)
        self.assertIn("Book is unavailable", output)

    def test_08_fourth_active_loan_is_refused(self):
        """BR05 / R2: a member can have at most 3 active loans."""
        self.run_sql("INSERT INTO books (id, title, author, available) "
                     "VALUES (4, 'Test Book', 'Test Author', 1)")
        for book_id in (1, 2, 3):
            result, _ = self.call(library.borrow, "S1", book_id)
            self.assertTrue(result)
        result, output = self.call(library.borrow, "S1", 4)
        self.assertFalse(result)
        self.assertIn("Borrowing limit reached", output)

    def test_09_loan_period_is_14_days(self):
        """BR06 / R4: the due date is exactly 14 days after borrowing."""
        self.call(library.borrow, "S1", 1)
        borrow_date, due_date = self.conn.execute(
            "SELECT borrow_date, due_date FROM loans").fetchone()
        period = datetime.fromisoformat(due_date) - datetime.fromisoformat(borrow_date)
        self.assertEqual(period, timedelta(days=14))

    # ---------- Return (R5, R3) ----------

    def test_10_return_without_active_loan_fails(self):
        """BR08: returning a book that the member has not borrowed fails."""
        result, output = self.call(library.return_book, "S1", 1)
        self.assertFalse(result)
        self.assertIn("Active loan not found", output)

    def test_11_late_return_is_fined_per_day(self):
        """BR09 / R5: a return 3 days (and 1 hour) late gives a fine of 3."""
        self.call(library.borrow, "S1", 1)
        late_due = (datetime.now() - timedelta(days=3, hours=1)).isoformat()
        self.run_sql("UPDATE loans SET due_date=?", (late_due,))
        result, output = self.call(library.return_book, "S1", 1)
        self.assertTrue(result)
        self.assertIn("Book returned", output)
        self.assertIn("Fine: 3", output)

    def test_12_returned_book_can_be_borrowed_again(self):
        """BR10 / R3: an on-time return has no fine and makes the book available."""
        self.call(library.borrow, "S1", 1)
        result, output = self.call(library.return_book, "S1", 1)
        self.assertTrue(result)
        self.assertNotIn("Fine", output)
        result, _ = self.call(library.borrow, "S2", 1)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
