"""Returning a book and calculating the late fine (refactoring #25).

This logic used to sit inside library.return_book(), mixed with the loan
lookup and the console messages. It now has its own class, so the fine rule
can be read, tested and changed in one place.
"""
from datetime import datetime


class ReturnService:
    def __init__(self, db):
        self.db = db

    def calculate_fine(self, due_date, return_date):
        """The fine is 1 per full day late, and 0 for an on-time return."""
        late = (return_date - due_date).days
        return late if late > 0 else 0

    def return_book(self, member_id, book_id):
        loan = self.db.find_active_loan(member_id, book_id)

        if not loan:
            print("Active loan not found")
            return False

        loan_id = loan[0]
        due = datetime.fromisoformat(loan[1])
        fine = self.calculate_fine(due, datetime.now())

        self.db.close_loan(loan_id, book_id)

        print("Book returned")

        if fine:
            print("Fine:", fine)

        return True
