#  BookTracker

노벨피아에서 읽은 기록을 기반으로 도서 정보를 자동으로 정리하고  
Notion에 연동하여 시각화하는 도서기록 관리 시스템입니다.

##  주요 기능

- 노벨피아 사이트에서 읽은 기록 크롤링
- SQLite에 읽은 책 정보 저장
- FastAPI를 통한 API 서버 구성
- Notion API를 통해 독서 기록 자동 업데이트

##  사용 기술

- Python
- FastAPI
- Selenium (크롤링)
- SQLite
- Notion API
- Git / GitHub

##  폴더 구조 (예정)

\\\
BookTracker/
 main.py
 crawler/
    novelpia_crawler.py
 db/
    models.py
 notion/
    notion_api.py
 requirements.txt
 README.md
 .gitignore
\\\

##  시작 방법

\\\ash
git clone https://github.com/Hyeon-min-yang/BookTracker.git
cd BookTracker
python -m venv venv
source venv/bin/activate  # Windows면 venv\\Scripts\\activate
pip install -r requirements.txt
\\\

##  제작자

- **양현민**  
- GitHub: [Hyeon-min-yang](https://github.com/Hyeon-min-yang)

