from pymongo.database import Database
from app.utils import AppModel
from bson.objectid import ObjectId
from pymongo.database import Database
from ..adapters.chatgpt_service import ChatGPTService
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
from typing import List, Any
from pydantic import Field
import json

class Product(AppModel):
    id: Any = Field(alias="_id")
    title: str
    price: str
    image_url: str
    product_url: str
    supermarket: str
    category: str

def fuzzy_compare_category(category, target_category):
    return fuzz.token_set_ratio(category.lower(), target_category.lower()) >= 75

class PostRepository:
    def __init__(self, database: Database):
        # self.client = client
        self.db = database
        self.collection = self.db['Products']
        self.chatgpt_service = ChatGPTService(os.environ["OPENAI_API_KEY"])

    def find_products_by_dish(self, dish_name: str) -> List[Product]:
        product_list_str = self.chatgpt_service.get_products_by_dish(dish_name)
        product_list = json.loads(product_list_str)
        print("Product List:", product_list)

        data = list(self.collection.find())
        found_products = []

        for product, category in product_list.items():
            print(product, category)
            matching_products = get_products_by_name(data, product, category)
            found_products.extend(matching_products)

        print("Result:", found_products)
        return [Product(**product) for product in found_products]
    
    def find_products_by_name(self, product_name: str) -> List[Product]:
        category = self.chatgpt_service.get_product_by_category(product_name)
        data = list(self.collection.find())
        print(category)

        # Используем библиотеку fuzzywuzzy для сравнения категорий
        found_products = [product for product in data if fuzzy_compare_category(product["category"], category)]

        # Если имя продукта указано, фильтруем по нему тоже
        if product_name:
            found_products = [product for product in found_products if fuzz.partial_ratio(product_name.lower(), product["title"].lower()) >= 75]

        print(found_products)
        return [Product(**product) for product in found_products]

    
    def get_ingredients_for_dish(self, dish_name: str) -> List[str]:
        product_list_str = self.chatgpt_service.get_products_by_dish(dish_name)
        product_list = json.loads(product_list_str)
        print(product_list)
        return list(product_list.keys())



def get_products_by_name(data, product_name, category=None):
    found_products = []
    for product in data:
        product_title = product["title"]
        product_category = product["category"]
        similarity = fuzz.token_set_ratio(product_name.lower(), product_title.lower())
        if similarity >= 75 and (category is None or category.lower() == product_category.lower()):
            found_products.append(product)
    return found_products



def get_cheapest_product(data, product_name, category=None):
    products = get_products_by_name(data, product_name, category)
    if products:
        try:
            sorted_products = sorted(products, key=lambda p: float(p["price"].replace(" ", "").replace(",", "").replace("₸", "")))
            cheapest_product = sorted_products[0]
            return cheapest_product
        except ValueError:
            return None
    return None

