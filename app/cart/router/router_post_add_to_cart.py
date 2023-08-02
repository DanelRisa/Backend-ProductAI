from fastapi import Depends, HTTPException, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router
from app.utils import AppModel
from typing import Optional,Any
from pydantic import Field


class AddToCartRequest(AppModel):
    id: Any = Field(alias="_id")
    title: str
    price:str
    image: str
    product_url: Optional[str]



@router.post("/add_to_cart/")
def add_to_cart(
    request_body: AddToCartRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    svc.repository.add_item_to_cart(user_id=jwt_data.user_id, item=request_body)
    return {"message": "Item added to cart"}
