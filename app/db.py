import sqlite3
from typing import List, Dict
import os
from datetime import datetime
import sqlite3

DB_PATH = os.path.join("data", "books.db")

def save_books_to_db(book_list: List[Dict]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 테이블이 없을 경우 생성
    c.execute("""
        CREATE TABLE IF NOT EXISTS reading_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            last_read INTEGER NOT NULL,
            total_eps INTEGER,
            crawled_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    for book in book_list:
        try:
            c.execute("""
                INSERT INTO reading_log (title, last_read, total_eps, crawled_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(title) DO UPDATE SET
                    last_read = excluded.last_read,
                    total_eps = excluded.total_eps,
                    crawled_at = excluded.crawled_at
            """, (
                book["title"],
                int(book.get("last_read", 0)),
                int(book.get("total_eps", 0)),
                datetime.now().isoformat()
            ))
        except Exception as e:
            print(f"데이터 삽입 실패 {book} {e}")

    conn.commit()
    conn.close()
    

def load_books_from_db(db_path="data/books.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT title, last_read, total_eps, crawled_at FROM reading_log")
    rows = cursor.fetchall()
    conn.close()

    books = []
    for row in rows:
        crawled_at = row[3]
        if crawled_at:
            try:
                crawled_at = datetime.fromisoformat(crawled_at)
            except Exception:
                crawled_at = None
        else:
            crawled_at = None

        books.append({
            "title": row[0],
            "last_read": row[1],
            "total_eps": row[2],
            "crawled_at": crawled_at
        })

    return books
