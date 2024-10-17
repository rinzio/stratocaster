from http import HTTPStatus as HTTP

from fastapi import APIRouter, Depends, HTTPException

from internal.db.models.user import Role
from typing import Annotated, Any, List, Dict, Optional

from internal.db.repository import UserRepo
from internal.db.models import BaseUserModel
from app.dependencies import is_admin

### DEBUG PURPOSES DELETE IN PROD
### Password must be hashed from frontend
from internal.env import ENV
from ..auth import AuthManager


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}, 403: {"description": "Not authorized to use this resource"}},
)

@router.post(
    "/",
    response_description="Add new user",
    response_model=BaseUserModel,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def post(user: BaseUserModel):
    if ENV == "dev":
        user.password = AuthManager.hash(user.password)
    return UserRepo.create(user.model_dump(by_alias=True, exclude=["id"])) # type: ignore

@router.get(
    "/",
    response_description="List all users",
    response_model=List[BaseUserModel],
    status_code=HTTP.OK,
    response_model_by_alias=False,
)
async def list(
    _: Annotated[BaseUserModel, Depends(is_admin)],
    id_: Optional[str] = None,
    name: Optional[str] = None,
    p_lastname: Optional[str] = None,
    email: Optional[str] = None,
    is_active: Optional[bool] = True,
):
    """
    List all of the users data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    query: Dict[str, Any] = {k: v for k, v in {
        "id": id_,
        "name": name,
        "p_lastname": p_lastname,
        "email": email,
        "is_active": is_active,
    }.items() if v is not None}
    return UserRepo.list(query)

@router.get(
    "/{id}",
    response_description="Get a single user",
    response_model=BaseUserModel,
    status_code=HTTP.OK,
    response_model_by_alias=False,
)
async def get(id: str, is_active: bool = True):
    """
    Get the record for a specific user, looked up by `id`.
    """
    if (user := UserRepo.get(id, is_active=is_active)) is None:
        raise HTTPException(status_code=HTTP.NOT_FOUND, detail=f"Doctor {id} not found")
    return user


@router.delete(
    "/{id}",
    response_description="Delete a single user",
    response_model=BaseUserModel,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def delete(
    _: Annotated[BaseUserModel, Depends(is_admin)],
    id: str
):
    """
    Delete the record for a specific user, looked up by `id`.
    """
    to_delete = UserRepo.delete(id)
    if to_delete is None:
        raise HTTPException(status_code=HTTP.NOT_FOUND, detail=f"User {id} not found")
    return to_delete
