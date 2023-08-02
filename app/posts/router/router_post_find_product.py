from fastapi import Depends

from app.utils import AppModel
from ..service import Service, get_service
from typing import List

from . import router
from ..repository.repository import PostRepository, Product

class ProductQuery(AppModel):
    product_name: str
    # category: str 

@router.post("/products/find", response_model=List[Product])
def find_product_by_name_and_category(
    query: ProductQuery,
    svc: Service = Depends(get_service),
) -> List[Product]:
    product_name = query.product_name
    # category = query.category

    return svc.repository.find_products_by_name(product_name)
