from fastapi import Depends
from app.utils import AppModel
from ..service import Service, get_service
from typing import List

from . import router
from ..repository.repository import PostRepository, Product

class Dish(AppModel):
    name: str

@router.post("/ingredients/", response_model=List[str])
def get_ingredients_for_dish(
    dish: Dish,
    svc: Service = Depends(get_service),
) -> List[str]:
    dish_name = dish.name
    return svc.repository.get_ingredients_for_dish(dish_name)

