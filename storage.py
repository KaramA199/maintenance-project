"""Data-access layer for the Library Management System (MR-02).

library.py no longer talks to a database directly. It calls the methods
below, and any storage class that offers the same methods can be plugged in.

Two implementations are provided:
- JsonStorage   the replacement store (default): one JSON file, library.json
- SqliteStorage the legacy SQLite database, library.db, kept as a fallback

The backend is chosen with the environment variable LMS_BACKEND
("json" or "sqlite"). When the JSON store is created for the first time and
a legacy library.db exists, its data is converted into the new store.

Rows are returned as tuples in the same column order the legacy SQL used,
so the business logic in library.py did not have to change.
"""
import json
import os
import re
import sqlite3

SQLITE_FILE = "library.db"
JSON_FILE = "library.json"

SEED_MEMBERS = [("S1", "Ali", "ACTIVE"), ("S2", "Sara", "ACTIVE")]
# (id, title, author, available, total_copies), copies from MR-01
SEED_BOOKS = [
    (1, "Clean Code", "Robert Martin", 3, 3),
    (2, "Refactoring", "Martin Fowler", 2, 2),
    (3, "Design Patterns", "Gamma et al.", 2, 2),
]


def open_storage():
    backend = os.environ.get("LMS_BACKEND", "json")
    if backend == "sqlite":
        return SqliteStorage()
    if backend == "json":
        return JsonStorage()
    raise ValueError("Unknown LMS_BACKEND: " + backend)


class SqliteStorage:
    """The legacy database, with every SQL statement of the old library.py."""

    def __init__(self, path=SQLITE_FILE):
        self.db = sqlite3.connect(path)
        c = self.db.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS members(
                id TEXT PRIMARY KEY,
                name TEXT,
                status TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS books(
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                available INTEGER,
                total_copies INTEGER
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS loans(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id TEXT,
                book_id INTEGER,
                borrow_date TEXT,
                due_date TEXT,
                returned INTEGER
            )
        """)
        # MR-01 migration for a database made before copies existed.
        c.execute("PRAGMA table_info(books)")
        if "total_copies" not in [col[1] for col in c.fetchall()]:
            c.execute("ALTER TABLE books ADD COLUMN total_copies INTEGER")
            c.execute("UPDATE books SET total_copies = 1")
        c.executemany("INSERT OR IGNORE INTO members VALUES (?,?,?)", SEED_MEMBERS)
        c.executemany("INSERT OR IGNORE INTO books VALUES (?,?,?,?,?)", SEED_BOOKS)
        self.db.commit()

    def search_books(self, text):
        c = self.db.cursor()
        c.execute(
            """SELECT id,title,author,available,total_copies
               FROM books
               WHERE title LIKE ? OR author LIKE ?""",
            ("%" + text + "%", "%" + text + "%")
        )
        return c.fetchall()

    def find_member(self, member_id):
        c = self.db.cursor()
        c.execute("SELECT id,status FROM members WHERE id=?", (member_id,))
        return c.fetchone()

    def find_book(self, book_id):
        c = self.db.cursor()
        c.execute("SELECT available FROM books WHERE id=?", (book_id,))
        return c.fetchone()

    def count_active_loans(self, member_id):
        c = self.db.cursor()
        c.execute(
            "SELECT COUNT(*) FROM loans WHERE member_id=? AND returned=0",
            (member_id,)
        )
        return c.fetchone()[0]

    def find_active_loan(self, member_id, book_id):
        c = self.db.cursor()
        c.execute(
            """SELECT id,due_date FROM loans
               WHERE member_id=? AND book_id=? AND returned=0""",
            (member_id, book_id)
        )
        return c.fetchone()

    def add_loan(self, member_id, book_id, borrow_date, due_date):
        c = self.db.cursor()
        c.execute(
            """INSERT INTO loans
               (member_id,book_id,borrow_date,due_date,returned)
               VALUES(?,?,?,?,0)""",
            (member_id, book_id, borrow_date, due_date)
        )
        c.execute("UPDATE books SET available=available-1 WHERE id=?", (book_id,))
        self.db.commit()

    def close_loan(self, loan_id, book_id):
        c = self.db.cursor()
        c.execute("UPDATE loans SET returned=1 WHERE id=?", (loan_id,))
        c.execute(
            """UPDATE books SET available=available+1
               WHERE id=? AND available < total_copies""",
            (book_id,)
        )
        self.db.commit()

    def export_all(self):
        """All rows, for converting an old database into the new store."""
        c = self.db.cursor()
        return {
            "members": c.execute("SELECT id,name,status FROM members").fetchall(),
            "books": c.execute(
                "SELECT id,title,author,available,total_copies FROM books").fetchall(),
            "loans": c.execute(
                """SELECT id,member_id,book_id,borrow_date,due_date,returned
                   FROM loans ORDER BY id""").fetchall(),
        }

    def close(self):
        self.db.close()


def _like(text, value):
    """SQLite LIKE '%text%': '%' and '_' are wildcards, ASCII case is ignored."""
    if value is None:
        return False
    pattern = "".join(
        ".*" if ch == "%" else "." if ch == "_" else re.escape(ch) for ch in text
    )
    return re.search(pattern, value, re.IGNORECASE | re.ASCII | re.DOTALL) is not None


class JsonStorage:
    """The replacement store: all data in one JSON file, written on every change."""

    def __init__(self, path=JSON_FILE, legacy_path=SQLITE_FILE):
        self.path = path
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self.data = json.load(f)
            return
        if os.path.exists(legacy_path):
            old = SqliteStorage(legacy_path)
            rows = old.export_all()
            old.close()
        else:
            rows = {"members": SEED_MEMBERS, "books": SEED_BOOKS, "loans": []}
        self.data = {
            "members": [dict(zip(("id", "name", "status"), r)) for r in rows["members"]],
            "books": [dict(zip(("id", "title", "author", "available", "total_copies"), r))
                      for r in rows["books"]],
            "loans": [dict(zip(("id", "member_id", "book_id", "borrow_date",
                                "due_date", "returned"), r)) for r in rows["loans"]],
        }
        self.data["next_loan_id"] = max([l["id"] for l in self.data["loans"]], default=0) + 1
        self._save()

    def _save(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)
        os.replace(tmp, self.path)

    def _book(self, book_id):
        return next((b for b in self.data["books"] if b["id"] == book_id), None)

    def _active_loans(self, member_id):
        return [l for l in self.data["loans"]
                if l["member_id"] == member_id and l["returned"] == 0]

    def search_books(self, text):
        return [(b["id"], b["title"], b["author"], b["available"], b["total_copies"])
                for b in self.data["books"]
                if _like(text, b["title"]) or _like(text, b["author"])]

    def find_member(self, member_id):
        m = next((m for m in self.data["members"] if m["id"] == member_id), None)
        return (m["id"], m["status"]) if m else None

    def find_book(self, book_id):
        b = self._book(book_id)
        return (b["available"],) if b else None

    def count_active_loans(self, member_id):
        return len(self._active_loans(member_id))

    def find_active_loan(self, member_id, book_id):
        loan = next((l for l in self._active_loans(member_id)
                     if l["book_id"] == book_id), None)
        return (loan["id"], loan["due_date"]) if loan else None

    def add_loan(self, member_id, book_id, borrow_date, due_date):
        self.data["loans"].append({
            "id": self.data["next_loan_id"], "member_id": member_id,
            "book_id": book_id, "borrow_date": borrow_date,
            "due_date": due_date, "returned": 0,
        })
        self.data["next_loan_id"] += 1
        self._book(book_id)["available"] -= 1
        self._save()

    def close_loan(self, loan_id, book_id):
        for loan in self.data["loans"]:
            if loan["id"] == loan_id:
                loan["returned"] = 1
        book = self._book(book_id)
        if book and book["available"] < book["total_copies"]:
            book["available"] += 1
        self._save()

    def close(self):
        pass
