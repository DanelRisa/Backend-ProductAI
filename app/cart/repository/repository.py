from pymongo.database import Database
from app.utils import AppModel
from bson.objectid import ObjectId
from pymongo.database import Database
import os
from typing import List,Optional,Any
import json
from pymongo.results import DeleteResult
from pydantic import Field


class AddToCartRequest(AppModel):
    id: Any = Field(alias="_id")
    title: str
    price: str
    image: str
    product_url: Optional[str]

class CartRepository:
    def __init__(self, database: Database):
        # self.client = client
        self.db = database
        self.collection = self.db['Cart']

    # def add_item_to_cart(self, user_id: str, item_id: str, ):
    #     self.collection.insert_one({"user_id":user_id, "item_id": item_id})


    def add_item_to_cart(self, user_id: str, item: AddToCartRequest):
        cart_item = {
            "user_id": user_id,
            "title": item.title,
            "price": item.price,
            "image": item.image,
            "product_url": item.product_url,

        }
        self.collection.insert_one(cart_item)

    def get_all_carts(self, user_id: str) -> List[dict]:
        carts = self.collection.find({"user_id": user_id})
        return list(carts)

    # def get_all_carts(self, user_id: str) -> List[dict]:
    #     carts = self.collection.find({"user_id": user_id})
    #     cart_items = list(carts)
    #     return cart_items
    
    # def delete_cart_by_id(self, item_id: str, user_id: str) -> DeleteResult:
        
    #     return self.collection.delete_one(
    #         {"_id": ObjectId(item_id), "user_id": ObjectId(user_id)}
    #     )

    def delete_product_by_id(self, _id: str, user_id: str) -> DeleteResult:
        return self.collection.delete_one({"_id": ObjectId(_id), "user_id": user_id})

    
