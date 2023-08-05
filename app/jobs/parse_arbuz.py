import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import os
from pymongo import MongoClient
import json
# imports for galmart
import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient


mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')
collection_name = os.getenv('COLLECTION_NAME')

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]




base_url = 'https://arbuz.kz'
category_urls = [
    {'name': 'Овощи и фрукты', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/225164-svezhie_ovoshi_i_frukty#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D'},
    {'name': 'Напитки и алкогольные напитки', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/14-napitki#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D'},
    {'name': 'Молоко, сливки, растительное молоко, сгущенное молоко, коктейли молочные', 'urls': [
        'https://arbuz.kz/ru/almaty/catalog/cat/20077-slivki#/',
        'https://arbuz.kz/ru/almaty/catalog/cat/20050-moloko#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D',
        'https://arbuz.kz/ru/almaty/catalog/cat/224177-rastitelnoe_moloko#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D',
        'https://arbuz.kz/ru/almaty/catalog/cat/74410-fermerskoe_moloko#/',
        'https://arbuz.kz/ru/almaty/catalog/cat/20072-sgush_nnoe_moloko',
        'https://arbuz.kz/ru/almaty/catalog/cat/224700-suhoe_moloko',
    ]},
    {'name': 'Масло сливочное, спреды, маргарин', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/225446-slivochnoe_maslo#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D'},
    {'name': 'Творог, сметана, кефир и кисломолочные продукты  ', 'urls': ['https://arbuz.kz/ru/almaty/catalog/cat/20016-kislomolochnye_napitki#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D',
        'https://arbuz.kz/ru/almaty/catalog/cat/20089-smetana#/',
        'https://arbuz.kz/ru/almaty/catalog/cat/224761-kurt_zhent#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D',
        'https://arbuz.kz/ru/almaty/catalog/cat/225076-kozhe_shubat',
        'https://arbuz.kz/ru/almaty/catalog/cat/224700-suhoe_moloko']},

    {'name': 'Сыр', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/20160-syry#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D'},
    {'name': 'Йогурты и творожные сырки', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/225171-iogurty_i_tvorozhnye_syrki#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D'},
    {'name': "Мука, соль, сахар, приправы, соусы", 'urls':['https://arbuz.kz/ru/almaty/catalog/cat/225449-muka#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D',
        'https://arbuz.kz/ru/almaty/catalog/cat/224402-specii_i_pripravy#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D']},
    {'name': "Крупы, макаронные изделия", 'urls':['https://arbuz.kz/ru/almaty/catalog/cat/224398-krupy_bobovye#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A2,%22component%22%3A%22pagination%22%7D%5D',
        'https://arbuz.kz/ru/almaty/catalog/cat/224399-makarony_i_lapsha#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D']},
    {'name': 'Яйца', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/225245-yaica#/'},
    {'name': 'Растительное масла', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/225448-rastitelnye_masla#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D'},

    {'name': 'Кондитерские изделия', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/225166-sladosti#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D'},
    {'name': 'Моющие, чистящие средства', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/16-vs_dlya_doma#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D'},
    {'name': 'Мясо и рыба и птица', 'urls': [
        'https://arbuz.kz/ru/almaty/catalog/cat/225162-myaso_ptica#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D', 
        'https://arbuz.kz/ru/almaty/catalog/cat/225163-ryba_i_moreprodukty#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D'
    ]},
    {'name': 'Косметика, средства гигиены', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/224407-krasota#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A1,%22component%22%3A%22pagination%22%7D%5D'},
    {'name': 'Консервы', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/20205-konservy#/'},
    {'name': 'Снеки', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/19820-sneki_i_krekery#/'},
    {'name':'Хлеб и хлебобулочные изделия', 'url': 'https://arbuz.kz/ru/almaty/catalog/cat/225165-hleb_vypechka#/'}

]

products = []

# driver_service = Service(GeckoDriverManager().install())
# options = Options()
# driver = webdriver.Firefox(service=driver_service, options=options)

options = Options()
options.headless = True
service = Service(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

for category in category_urls:
    category_name = category['name']
    
    if 'url' in category:
        category_urls = [category['url']]
    else:
        category_urls = category['urls']
    
    for url in category_urls:
        driver.get(url)

        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article.product-item.product-card')))
        except TimeoutException as te:
            print(f"Timeout occurred while waiting for products in category {category_name}. Skipping to the next category.")
            continue

        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            items = soup.find_all('article', class_='product-item product-card')
            if not items:
                break

            for item in items:
                try:
                    title_elem = item.find('a', class_='product-card__title')
                    price_elem = item.find('span', class_='price--wrapper price--currency_KZT')
                    image_elem = item.find('img', class_='product-card__img')

                    if title_elem and price_elem and image_elem:
                        title = title_elem.get('title')
                        price = price_elem.get_text(strip=True)
                        image_url = image_elem.get('data-src')
                        product_url = base_url + item.find('a', class_='product-card__link').get('href')
                        products.append({'title': title, 'price': price, 'image_url': image_url, 'product_url': product_url, 'supermarket': 'Arbuz', 'category': category_name})
                        collection.insert_one({'title': title,'price': price, 'image_url': image_url, 'product_url': product_url, 'supermarket': 'Arbuz','category': category_name })
                except Exception as e:
                    print(f"Error occurred while parsing an item: {e}")

            # Find pagination elements (if any)
            pagination = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination.flex-wrap')
            if not pagination:
                print(f"No pagination found in category {category_name}. Skipping to the next category.")
                break

            next_page_links = pagination[0].find_elements(By.CSS_SELECTOR, 'li.page-item:not(.disabled) a')
            
            next_page_link = None
            for link in next_page_links:
                if link.text.strip() == '»':
                    next_page_link = link
                    break
            
            if not next_page_link:
                break

            driver.execute_script("arguments[0].click();", next_page_link)
            
driver.quit()
client.close()
