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

from pymongo import MongoClient
import json
# imports for galmart
import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
import os

mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')
collection_name = os.getenv('COLLECTION_NAME')

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

def parse_product_card(card, category):
    title = card.find('h2', class_='woocommerce-loop-product__title').text.strip()
    price_element = card.find('span', class_='woocommerce-Price-amount')
    price = price_element.text.strip() if price_element else "Цена не найдена"
    image_url = card.find('img')['src']
    product_url = card.find('a', class_='ast-loop-product__link')['href']

    return {
        'title': title,
        'price': price,
        'image_url': image_url,
        'product_url': product_url,
        'supermarket': 'Galmart',
        'category': category
    }

categories = {
    'Овощи и фрукты': 'https://store.galmart.kz/product-category/%d0%ba%d0%b70000255/',
    "Напитки и алкогольные напитки": ['https://store.galmart.kz/product-category/%d0%ba%d0%b70000223/%d0%ba%d0%b70000240/',
    'https://store.galmart.kz/product-category/%d0%ba%d0%b70000223/%d0%ba%d0%b70000245/'],
    'Молоко, сливки, растительное молоко, сгущенное молоко, коктейли молочные':['https://store.galmart.kz/product-category/%d0%ba%d0%b70000181/%d0%ba%d0%b70000200/'],
    'Масло сливочное, спреды, маргарин':'https://store.galmart.kz/product-category/%d0%ba%d0%b70000181/%d0%ba%d0%b70000191/',
    'Творог, сметана, кефир и кисломолочные продукты':'https://store.galmart.kz/product-category/%d0%ba%d0%b70000181/%d0%ba%d0%b70000185/',
    'Сыр': 'https://store.galmart.kz/product-category/%d0%ba%d0%b70000048/%d0%ba%d0%b70000055/',
    'Йогурты и творожные сырки':[' https://store.galmart.kz/product-category/%d0%ba%d0%b70000181/%d0%ba%d0%b70000182/',
    'https://store.galmart.kz/product-category/%d0%ba%d0%b70000181/%d0%ba%d0%b70000185/%d0%ba%d0%b70000190/'],
    'Мука, соль, сахар, приправы, соусы': ['https://store.galmart.kz/product-category/%d0%ba%d0%b70000001/%d0%ba%d0%b70000009/',
    'https://store.galmart.kz/product-category/%d0%ba%d0%b70000001/%d0%ba%d0%b70000026/'],
    'Крупы, макаронные изделия':'https://store.galmart.kz/product-category/%d0%ba%d0%b70000001/%d0%ba%d0%b70000002/',
    'Яйца':'https://store.galmart.kz/product-category/%d0%ba%d0%b70000181/%d0%ba%d0%b70000198/',
    'Растительное масла':'https://store.galmart.kz/product-category/%d0%ba%d0%b70000001/%d0%ba%d0%b70000005/',
    "Кондитерские изделия": "https://store.galmart.kz/product-category/%d0%ba%d0%b70000061/",
    "Консервы": "https://store.galmart.kz/product-category/%d0%ba%d0%b70000094/%d0%ba%d0%b70000095/",
    "Моющие, чистящие средства": "https://store.galmart.kz/product-category/%d0%ba%d0%b70000207/",
    "Полуфабрикаты": "https://store.galmart.kz/product-category/%d0%ba%d0%b70000293/",
    "Хлеб и хлебобулочные изделия": "https://store.galmart.kz/product-category/%d0%ba%d0%b70000484/",
    "Чай и кофе и какао": "https://store.galmart.kz/product-category/%d0%ba%d0%b70000499/",
    "Мясо и рыба и птица": "https://store.galmart.kz/product-category/%d0%ba%d0%b70000155/%d0%ba%d0%b70000163/",
    "Косметика, средства гигиены": "https://store.galmart.kz/product-category/%d0%ba%d0%b70000109/"
}

for category, urls in categories.items():
    if not isinstance(urls, list):
        urls = [urls]

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        pagination = soup.find('nav', class_='woocommerce-pagination')
        if pagination:
            last_page_link = pagination.find_all('a', class_='page-numbers')[-2]
            last_page = int(last_page_link.text)
        else:
            last_page = 1

        for page in range(1, last_page + 1):
            page_url = f'{url}page/{page}/'
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            product_cards = soup.find_all('li', class_='ast-col-sm-12')

            for card in product_cards:
                product_data = parse_product_card(card, category)
                collection.insert_one(product_data)  # MongoDB

            print(f"Страница {page} ({category}) обработана.")

client.close()

print('Data removed and updated in MongoDB.')