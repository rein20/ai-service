import os
import re
import time
import urllib

import certifi
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = 'https://www.yogiyo.co.kr/mobile/#/'
URL = [
    'https://www.yogiyo.co.kr/mobile/#/1367138/'
    # 'https://www.yogiyo.co.kr/mobile/#/1222170',
    # 'https://www.yogiyo.co.kr/mobile/#/1023596',
    # 'https://www.yogiyo.co.kr/mobile/#/1244448',
    # 'https://www.yogiyo.co.kr/mobile/#/576188',
    # 'https://www.yogiyo.co.kr/mobile/#/411340/',
]

username = urllib.parse.quote_plus(os.environ['MONGODB_USERNAME'])
password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])

uri = f"mongodb+srv://{username}:{password}@cluster0.61sar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.restaurant_db
collection = db.restaurant_info


def crawl_single_restaurant(restaurant_url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.geolocation": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(BASE_URL)
    time.sleep(3)

    # 검색창 요소 찾아서 변수에 저장
    search_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="search"]/div/form/input')))

    # 검색어 입력
    my_address = '카카오판교'
    search_box.send_keys(my_address)

    # 검색 버튼 누르기
    search_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="button_search_address"]/button[2]')))
    search_btn.click()

    # 주소 관련 검색처가 뜰 때까지 잠시 대기
    time.sleep(2)

    # 검색 실행
    first_address = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '(//li[contains(@class, "ng-scope")])[3]')))
    first_address.click()
    time.sleep(3)
    
    driver.get(restaurant_url)
    time.sleep(5)

    # 클린 리뷰 클릭
    clean_review_btn = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/ul/li[2]')
    clean_review_btn.click()

    while True:
        try:
            more_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="review"]/li/a')))
            more_btn.click()
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(3)
        # 지정된 XPATH 요소를 찾을 수 없는 경우, webdriver 시간내에 조건이 만족되지 않을 경우, 요소가 클릭 가능한 상태가 아닐 경우
        except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    restaurant_name = soup.select_one('#content > div.restaurant-detail.row.ng-scope > div.col-sm-8 > div.restaurant-info > div.restaurant-title > span').get_text(strip=True)
    reviews = soup.select('#review > li > p')
    review_texts = [review.get_text(strip=True) for review in reviews][1:]
    menus = soup.select('#review > li > div.order-items.ng-binding')
    all_menu = [menu.get_text(strip=True) for menu in menus]
    
    document = {
        "restaurant": restaurant_name,
        "url": restaurant_url,
        "reviews": []
    }

    for menu, text in zip(all_menu, review_texts):
        document['reviews'].append({
            "menus" : menu,
            "review_text" : text
        })

    restaurant_id = re.findall(r'\d+', restaurant_url)[0]
    driver.quit()
    return [restaurant_id, document]


def crawl_urls():
    for i in range(len(URL)):
        key, document = crawl_single_restaurant(URL[i])
        result = collection.update_one({"_id": key}, {"$set": document}, upsert=True)
    return result


if __name__ == '__main__':
    crawl_urls()