from app.crawler import crawl_recent_updates
from app.db import save_books_to_db

if __name__ == "__main__":
    book_list = crawl_recent_updates()
    save_books_to_db(book_list)
