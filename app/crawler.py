from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
from dotenv import load_dotenv
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from selenium.common.exceptions import NoSuchElementException
import re

load_dotenv()

KAKAO_ID = os.getenv("KAKAO_ID")
KAKAO_PW = os.getenv("KAKAO_PW")

#크롬 드라이버 생성
## headless=True 시 브라우저 백그라운드 실행
def get_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    return driver
# 현재 URL에서 페이지 번호 추출 함수
def get_current_page_number(driver):
    url = driver.current_url
    if 'date/' in url:
        return int(url.split('date/')[-1].split('?')[0])
    return -1

#사이트 카카오 로그인
def login_with_kakao(driver):
    driver.get("https://novelpia.com")
    time.sleep(2)
    
    #팝업 닫기
    try:
        close_btn = driver.find_element(By.CSS_SELECTOR, 'div.layer-close-x3')
        close_btn.click()
        time.sleep(1)
    except NoSuchElementException:
        pass
    
    # 메뉴 버튼 클릭
    try:
        menu_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[onclick="pc_s_vue.toggle()"]'))
        )
        menu_btn.click()
        time.sleep(2)
    except Exception as e:
        print("메뉴 버튼 클릭 실패")
        driver.save_screenshot("error_menu_click.png")
        raise

    try:
        login_entry = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.b-login.s_inv'))
        )
        login_entry.click()
        time.sleep(2)
    except Exception as e:
        print("로그인 진입 버튼 클릭 실패")
        driver.save_screenshot("error_login_block.png")
        raise

    # 카카오 로그인 버튼 클릭
    try:
        kakao_img_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt="카카오로 로그인"]'))
        )
        kakao_img_btn.click()
    except:
        print("카카오 이미지 버튼 클릭 실패")
        driver.save_screenshot("error_kakao_img.png")
        raise
    
    #카카오창 전환
    main_window = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break
    
    driver.find_element(By.ID, "loginId--1").send_keys(KAKAO_ID)
    driver.find_element(By.ID, "password--2").send_keys(KAKAO_PW)
    driver.find_element(By.XPATH, '//button[contains(text(), "로그인")]').click()
    time.sleep(5)
    
    driver.switch_to.window(main_window)
    time.sleep(2)
    
        #알림창 끄기
    try:
        driver.switch_to.alert.accept()
    except NoAlertPresentException:
        pass

        #최근 기록 이동
def go_to_recent_history(driver):
    driver.get("https://novelpia.com/mybook/last_view")
    time.sleep(2)

def get_recent_books_until_repeat(driver, latest_read=None):
    collected = []
    seen = set()

    while True:
        time.sleep(1)
        items = driver.find_elements(By.CLASS_NAME, "novel-list-real-container")

        for item in items:
            try:
                title = item.find_element(By.CLASS_NAME, "novel-name").text.strip()

                # 전체 회차 수
                episode_spans = item.find_elements(By.CLASS_NAME, "novel-numerical-content")
                total_eps = int(episode_spans[1].text.strip()) if len(episode_spans) > 1 else 0

                # 마지막 회차
                continue_label_elem = item.find_element(By.CLASS_NAME, "novel-btn-continue")
                continue_label = continue_label_elem.text.strip()

                #라벨에서 숫자 추출출
                last_read = int(''.join(filter(str.isdigit, continue_label)))
                
                key = (title, last_read)
                if key == latest_read:
                    return collected

                if key not in seen:
                    seen.add(key)
                    collected.append({
                        "title": title,
                        "last_read": last_read,
                        "total_eps": total_eps
                    })
                    print(collected[-1])
            except:
                continue

        # 다음 페이지 이동
        try:
            current_page = get_current_page_number(driver)
            next_btn = driver.find_element(By.CSS_SELECTOR, 'ul.pagination li.page-item.active + li a.page-link')
            next_href = next_btn.get_attribute("href")

            # 다음 페이지 번호가 현재와 같으면 종료
            if 'date/' in next_href:
                next_page = int(next_href.split('date/')[-1].split('?')[0])
                if next_page == current_page:
                    print("마지막 페이지입니다. 크롤링 종료.")
                    break

            next_btn.click()
        except:
            print("다음 페이지 버튼 없음. 종료.")
            break

    return collected

#전체 흐름 실행
def crawl_recent_updates(latest_read=None):
    driver = get_driver()
    try:
        login_with_kakao(driver)
        go_to_recent_history(driver)
        return get_recent_books_until_repeat(driver, latest_read)
    finally:
        driver.quit()
