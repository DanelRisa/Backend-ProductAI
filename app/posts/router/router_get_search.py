# from fastapi import Depends
# from app.utils import AppModel
# from ..service import Service, get_service
# from typing import List

# from . import router
# from ..repository.repository import PostRepository, Product

# class Dish(AppModel):
#     name: str

# @router.post("/products/search", response_model=List[Product])
# def search_products_by_name_and_category(       
#     product_name: str,
#     category: str,
#     svc: Service = Depends(get_service),
# ) -> List[Product]:
#     products = svc.repository.find_products_by_name(product_name, category)
#     return products

