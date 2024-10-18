from http import HTTPStatus as HTTP

from fastapi import APIRouter, HTTPException

from internal.db.repository import UserRepo
from internal.db.models import BaseUserModel

from internal.env import ENV
from ..auth import AuthManager


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        HTTP.CREATED: {"description": "User created"},
        HTTP.BAD_REQUEST: {"description": "Something is wrong with the payload"},
        HTTP.FORBIDDEN: {"description": "Not authorized to use this resource"},
        HTTP.NOT_FOUND: {"description": "Not found"},
    },
)

@router.post(
    "/",
    response_description="Add new user",
    response_model=BaseUserModel,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def post(user: BaseUserModel):
    user.password = AuthManager.hash(user.password)
    try:
        return UserRepo.create(user.model_dump(by_alias=True, exclude=["id"])) # type: ignore
    except RuntimeError:
        raise HTTPException(status_code=HTTP.BAD_REQUEST, detail=f"User email already exists")
