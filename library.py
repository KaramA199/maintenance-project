"""Library Management System: console menu and borrowing rules.

This module holds the menu (main), the search, and the borrow checks, with the
library rules as named constants. Returning a book and the late fine are in
return_service.py (ReturnService). All data access goes through storage.py,
which uses a JSON file by default or the legacy SQLite database when
LMS_BACKEND=sqlite.

Run with:  python library.py
"""
from datetime import datetime, timedelta

import storage
from return_service import ReturnService

# Library rules (refactoring #26): these values used to be literals inside
# borrow() and return_book().
MAX_BOOKS = 3         # active loans allowed per member
LOAN_DAYS = 14        # normal borrowing period
FINE_PER_DAY = 1      # fine for each full day late
ACTIVE = "ACTIVE"     # member status that may borrow


def setup():
    # MR-02: the database is reached only through the data-access layer in
    # storage.py, which picks the store (JSON by default, or legacy SQLite).
    return storage.open_storage()


def search_books(db, text):
    rows = db.search_books(text)

    for book_id, title, author, available, total_copies in rows:
        print(book_id, title, "-", author,
              "Available:", bool(available),
              "(" + str(available) + " of " + str(total_copies) + " copies)")

    return rows


def validate_member(db, member_id):
    """Validation: the member must exist and be active."""
    member = db.find_member(member_id)

    if not member:
        print("Member not found")
        return False

    _, status = member

    if status != ACTIVE:
        print("Member is not active")
        return False

    return True


def check_availability(db, book_id):
    """Availability check: the book must exist and have a copy on the shelf."""
    book = db.find_book(book_id)

    if not book:
        print("Book not found")
        return False

    (copies_on_shelf,) = book

    if copies_on_shelf <= 0:
        print("Book is unavailable")
        return False

    return True


def check_borrow_limit(db, member_id):
    """Borrow-limit check: a member may have at most MAX_BOOKS active loans."""
    if db.count_active_loans(member_id) >= MAX_BOOKS:
        print("Borrowing limit reached")
        return False

    return True


def create_loan(db, member_id, book_id):
    """Record creation: save the loan with a due date LOAN_DAYS from today."""
    today = datetime.now()
    due = today + timedelta(days=LOAN_DAYS)

    db.add_loan(member_id, book_id, today.isoformat(), due.isoformat())

    print("Book borrowed. Due:", due.date())


def borrow(db, member_id, book_id):
    """Borrow a book: run the three checks in order, then create the loan."""
    if not validate_member(db, member_id):
        return False

    if not check_availability(db, book_id):
        return False

    if not check_borrow_limit(db, member_id):
        return False

    create_loan(db, member_id, book_id)

    return True


def return_book(db, member_id, book_id):
    """Return a book. The return and fine logic is in ReturnService."""
    return ReturnService(db, FINE_PER_DAY).return_book(member_id, book_id)


def read_ids():
    """Ask for the member ID and the book ID (menu choices 2 and 3)."""
    member = input("Member ID: ")
    book = int(input("Book ID: "))
    return member, book


def main():
    db = setup()
    while True:
        print("\nLIBRARY")
        print("1 Search")
        print("2 Borrow")
        print("3 Return")
        print("4 Exit")

        choice = input("Choice: ")

        if choice == "1":
            text = input("Search: ")
            search_books(db, text)

        elif choice == "2":
            member, book = read_ids()
            borrow(db, member, book)

        elif choice == "3":
            member, book = read_ids()
            return_book(db, member, book)

        elif choice == "4":
            db.close()
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
