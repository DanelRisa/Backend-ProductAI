from fastapi import Depends, HTTPException, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router
from typing import List, Any,Optional
from pydantic import Field

from app.utils import AppModel

# class AddToCartRequest(AppModel):
#     title: str
class GetCartResponse(AppModel):
    id: Any = Field(alias="_id")
    user_id: Any
    title: str
    price: str
    image: str
    product_url: Optional[str]

@router.get("/get_cart", response_model=List[GetCartResponse])
def get_cart(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> List[GetCartResponse]:
    cart_items = svc.repository.get_all_carts(user_id=jwt_data.user_id)
    # print(type(cart_items))
    # print("Your items", cart_items)
    return [GetCartResponse(**cart_item) for cart_item in cart_items]
