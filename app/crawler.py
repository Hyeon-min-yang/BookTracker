from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
from dotenv import load_dotenv

load_dotenv()

KAKAO_ID = os.getenv("KAKAO_ID")
KAKAO_PW = os.getenv("KAKAO_PW")

#크롬 드라이버 생성
## headless=True 시 브라우저 백그라운드 실행
def get_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument(--headless)
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    return driver

#사이트 카카오 로그인
def login_with_kakao(driver):
    driver.get("https://novelpia.com")
    time.sleep(2)
    
    driver.find_element(By.CSS_SELECTOR, 'div[onclick="pc_s_vue.toggle()"]').click()
    time.sleep(2)
    
    driver.find_element(By.CSS_SELECTOR, 'a.login-btn.kakao').click()
    time.sleep(2)
    
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

def go_to_my_library(driver):
    driver.find_element(By.LINK_TEXT, "내서재").click()
    time.sleep(3)