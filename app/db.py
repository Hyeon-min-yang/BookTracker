import sqlite3
from typing import List, Dict

def save_books_to_db(book_list: List[Dict]):
    conn = sqlite3.connect("data/books.db")
    c = conn.cursor()

    for book in book_list:
        c.execute("""
            INSERT INTO reading_log (title, last_read, continue_label)
            VALUES (?, ?, ?)
        """, (
            book["title"],
            book["last_read"],
            book.get("continue_label", None)
        ))

    conn.commit()
    conn.close()
