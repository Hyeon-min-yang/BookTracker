import os
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")


def find_page_by_title(title: str):
    response = notion.databases.query(
        **{
            "database_id": database_id,
            "filter": {
                "property": "Title",
                "title": {
                    "equals": title
                }
            }
        }
    )
    results = response.get("results")
    return results[0]["id"] if results else None


def add_book_to_notion(book):
    print(f"Notion에 추가 중: {book['title']}")
    
    # 진행률 계산
    progress = None
    try:
        if book["total_eps"] and book["last_read"]:
            progress = round((book["last_read"] / book["total_eps"]) * 100, 2)
    except ZeroDivisionError:
        progress = 0.0

    # 날짜 포맷 처리
    crawled_at = book["crawled_at"]
    if crawled_at and isinstance(crawled_at, datetime):
        crawled_at = crawled_at.isoformat()
    elif not crawled_at:
        crawled_at = None

    # 기존 페이지 존재 여부 확인
    page_id = find_page_by_title(book["title"])

    try:
        if page_id:
            # 업데이트
            notion.pages.update(
                page_id=page_id,
                properties={
                    "last_read": {"number": book["last_read"]},
                    "total_eps": {"number": book["total_eps"]},
                    "crawled_at": {"date": {"start": crawled_at}},
                    "Progress": {"number": progress},
                }
            )
            print(f"Notion 업데이트 완료: {book['title']}")
        else:
            # 새로 생성
            notion.pages.create(
                parent={"database_id": database_id},
                properties={
                    "title": {
                        "title": [{"text": {"content": book["title"]}}]
                    },
                    "last_read": {"number": book["last_read"]},
                    "total_eps": {"number": book["total_eps"]},
                    "crawled_at": {"date": {"start": crawled_at}},
                    "Progress": {"number": progress}
                }
            )
            print(f"Notion 추가 완료: {book['title']}")
    except Exception as e:
        print(f"실패: {book['title']} | 에러: {e}")
