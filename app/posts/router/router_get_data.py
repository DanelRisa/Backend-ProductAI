from fastapi import Depends
from app.utils import AppModel
from ..service import Service, get_service
from typing import List

from . import router
from ..repository.repository import PostRepository, Product

class Dish(AppModel):
    name: str
    
@router.post("/products/get", response_model=List[Product])
def get_products_by_dish(
    dish: Dish,
    svc: Service = Depends(get_service),
) -> List[Product]: 
    product_list = svc.chatgpt_service.get_products_by_dish(dish.name)
    products = svc.repository.find_products_by_dish(product_list)
    print(products)
    return products

