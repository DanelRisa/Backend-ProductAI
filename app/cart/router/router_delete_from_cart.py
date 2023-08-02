from fastapi import Depends, Response, HTTPException

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router
from bson.objectid import ObjectId



@router.delete("/delete_product/{_id:str}")
def delete_product(
    _id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    _id = ObjectId(_id) 
    delete_result = svc.repository.delete_product_by_id(_id=_id, user_id=jwt_data.user_id)
    if delete_result.deleted_count == 1:
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Product with id {_id} not found")

