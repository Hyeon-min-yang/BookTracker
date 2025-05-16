from app.crawler import crawl_recent_updates
from app.db import save_books_to_db
from app.notion import add_book_to_notion
from app.db import load_books_from_db
from app.notion import add_book_to_notion

def main():
    book_list = crawl_recent_updates()
    save_books_to_db(book_list)
    
    books = load_books_from_db()
    print("책 리스트 크기:", len(books))
    for book in books:
        print("처리 중:", book["title"])
        add_book_to_notion(book)

    
if __name__ == "__main__":
    main()