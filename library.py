
from datetime import datetime, timedelta
import storage
from return_service import ReturnService
def setup():
    # MR-02: the database is reached only through the data-access layer in
    # storage.py, which picks the store (JSON by default, or legacy SQLite).
    return storage.open_storage()
def search_books(db, text):
    rows = db.search_books(text)

    for row in rows:
        print(row[0], row[1], "-", row[2],
              "Available:", bool(row[3]),
              "(" + str(row[3]) + " of " + str(row[4]) + " copies)")

    return rows
def validate_member(db, member_id):
    """Validation: the member must exist and be active."""
    member = db.find_member(member_id)

    if not member:
        print("Member not found")
        return False

    if member[1] != "ACTIVE":
        print("Member is not active")
        return False

    return True
def check_availability(db, book_id):
    """Availability check: the book must exist and have a copy on the shelf."""
    book = db.find_book(book_id)

    if not book:
        print("Book not found")
        return False

    if book[0] <= 0:
        print("Book is unavailable")
        return False

    return True
def check_borrow_limit(db, member_id):
    """Borrow-limit check: a member may have at most 3 active loans."""
    if db.count_active_loans(member_id) >= 3:
        print("Borrowing limit reached")
        return False

    return True
def create_loan(db, member_id, book_id):
    """Record creation: save the loan with a due date 14 days from today."""
    today = datetime.now()
    due = today + timedelta(days=14)

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
    return ReturnService(db).return_book(member_id, book_id)
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
            member = input("Member ID: ")
            book = int(input("Book ID: "))
            borrow(db, member, book)

        elif choice == "3":
            member = input("Member ID: ")
            book = int(input("Book ID: "))
            return_book(db, member, book)

        elif choice == "4":
            db.close()
            break

        else:
            print("Invalid choice")
if __name__ == "__main__":
    main()
